# State Management

Terraform state is the source of truth for what Azure resources exist. Mismanage it and you get drift, duplicate resources, or leaked secrets. Every rule here is non-negotiable for any environment beyond a developer sandbox.

## Remote State Setup

State lives in an Azure Storage blob container. The storage account is itself managed by Terraform (bootstrap exception: the state account is created once with az CLI and its config is recorded in an ADR).

### Bootstrap the state storage account

```bash
LOCATION="eastus2"
RG="rg-tfstate-shared"
SA="satfstate$(head -c4 /dev/urandom | xxd -p)"   # 4-byte random suffix
CONTAINER="tfstate"

az group create --name $RG --location $LOCATION
az storage account create \
  --name $SA \
  --resource-group $RG \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2 \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false \
  --https-only true

az storage container create \
  --name $CONTAINER \
  --account-name $SA \
  --auth-mode login

# Grant the pipeline identity Storage Blob Data Contributor
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee "<pipeline-managed-identity-or-sp-object-id>" \
  --scope "$(az storage account show --name $SA --resource-group $RG --query id -o tsv)"
```

### Backend configuration block

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate-shared"
    storage_account_name = "satfstate<suffix>"
    container_name       = "tfstate"
    key                  = "orders/prod/terraform.tfstate"
    use_azuread_auth     = true   # RBAC; no access key in config
  }
}
```

`use_azuread_auth = true` requires `Storage Blob Data Contributor` on the container for reads/writes. The pipeline identity (OIDC or Managed Identity) holds this role. Developers working locally need `Storage Blob Data Reader` for plan; `Contributor` for apply (production: require PIM elevation).

## State Locking

The `azurerm` backend implements state locking via blob lease. When `terraform plan` or `terraform apply` starts, it acquires an exclusive lease on the blob. A second concurrent operation waits or errors with a lock-held message.

Blob lease duration defaults to 60 seconds and is refreshed automatically while the operation runs. If a pipeline run dies unexpectedly, the lease expires automatically; no manual break-lease is needed under normal conditions.

If a lock is genuinely stuck (a run was killed mid-operation):

```bash
az storage blob lease break \
  --account-name satfstate<suffix> \
  --container-name tfstate \
  --blob-name "orders/prod/terraform.tfstate" \
  --auth-mode login
```

Only a platform engineer with `Storage Blob Data Contributor` should break leases. Document every manual lease break in the incident log.

## State Segmentation

Segment state by: **environment** × **blast-radius boundary**.

Recommended segmentation:

| State file key | Blast radius |
|---|---|
| `shared/networking/terraform.tfstate` | Hub VNet, DNS, Private DNS zones |
| `shared/identity/terraform.tfstate` | Managed Identities, role assignments |
| `orders/dev/terraform.tfstate` | Orders workload, dev |
| `orders/prod/terraform.tfstate` | Orders workload, prod |

Never put all environments in one state file. A corrupt or deleted state file would affect all environments simultaneously.

Cross-stack references use `terraform_remote_state` data source, read-only, authenticated by the same RBAC role:

```hcl
data "terraform_remote_state" "networking" {
  backend = "azurerm"
  config = {
    resource_group_name  = "rg-tfstate-shared"
    storage_account_name = "satfstate<suffix>"
    container_name       = "tfstate"
    key                  = "shared/networking/terraform.tfstate"
    use_azuread_auth     = true
  }
}

# consume the output
resource "azurerm_subnet" "app" {
  virtual_network_name = data.terraform_remote_state.networking.outputs.vnet_name
  ...
}
```

## Sensitive Values in State

State stores ALL resource attributes, including computed secrets returned by the Azure API (e.g., storage account connection strings, primary access keys). Mitigate:

1. **Mark outputs sensitive**: `output "primary_key" { value = azurerm_storage_account.main.primary_access_key; sensitive = true }`. Terraform redacts these in logs.
2. **Do not emit secrets as outputs at all** if consumers can obtain them from Key Vault directly.
3. **Encrypt state at rest**: the Azure Storage blob is encrypted by default (Microsoft-managed keys). For stricter compliance, configure a customer-managed key on the storage account.
4. **Restrict state access**: only the pipeline identity and break-glass platform engineers should have `Storage Blob Data Contributor`. Developers get `Reader` on the storage account and `Storage Blob Data Reader` on the container for plan operations only.
5. **Audit state access**: enable Diagnostic Settings on the storage account to route access logs to Log Analytics.
