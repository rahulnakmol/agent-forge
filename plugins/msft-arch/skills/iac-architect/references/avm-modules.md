# AVM Modules

Azure Verified Modules (AVM) is Microsoft's canonical library of pre-built, tested Terraform and Bicep modules. AVM modules first; custom modules only when the AVM catalog has a documented gap and an ADR justifies the deviation.

## What AVM Is

AVM modules are published to the Terraform Registry under the `Azure/` namespace and follow a strict naming scheme:

| Class | Naming pattern | Example |
|---|---|---|
| Resource module | `avm-res-<provider>-<resource>` | `avm-res-keyvault-vault` |
| Pattern module | `avm-ptn-<pattern>` | `avm-ptn-hubnetworking` |
| Utility module | `avm-utl-<utility>` | `avm-utl-regions` |

Every AVM module is owned by a named Microsoft engineer, versioned with semantic versioning, and validated against AVM's specification (TFFR3 requires `azurerm ~> 4.0`, `azapi ~> 2.0`).

## How to Consume AVM Modules

Reference modules directly from the Terraform Registry; do not vendor them into the repo unless airgapped deployments require it.

```hcl
module "key_vault" {
  source  = "Azure/avm-res-keyvault-vault/azurerm"
  version = "~> 0.9"   # pin to minor; allow patch updates

  name                = "kv-orders-prod-eus2"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "premium"

  # Soft-delete and purge protection are AVM defaults; leave enabled
  soft_delete_retention_days = 90
  purge_protection_enabled   = true

  tags = local.tags
}
```

```hcl
module "virtual_network" {
  source  = "Azure/avm-res-network-virtualnetwork/azurerm"
  version = "~> 0.7"

  name                = "vnet-orders-prod-eus2"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = ["10.0.0.0/16"]

  subnets = {
    app = {
      name             = "snet-app"
      address_prefixes = ["10.0.1.0/24"]
    }
    data = {
      name             = "snet-data"
      address_prefixes = ["10.0.2.0/24"]
    }
  }

  tags = local.tags
}
```

## Module Versioning Policy

- Pin to `~> <major>.<minor>` (pessimistic operator). This allows patch updates automatically but blocks breaking minor-version changes from landing without an explicit bump.
- Review AVM module changelogs on each dependency update PR. AVM modules can introduce interface changes in minor versions while the module is pre-1.0.
- Lock `.terraform.lock.hcl` into version control. Re-generate with `terraform providers lock` when updating.

## Checking the AVM Catalog

Before writing any custom module, verify the resource is not already in AVM:

1. Search `azure.github.io/Azure-Verified-Modules/indexes/terraform/tf-resource-modules/` for resource modules.
2. Search `azure.github.io/Azure-Verified-Modules/indexes/terraform/tf-pattern-modules/` for pattern modules.
3. Use `microsoft_docs_search` with "Azure Verified Modules Terraform `<resource type>`" to confirm GA status.

Commonly used AVM resource modules (verified GA as of 2025):
- `avm-res-keyvault-vault`: Key Vault
- `avm-res-network-virtualnetwork`: Virtual Network
- `avm-res-containerregistry-registry`: Azure Container Registry
- `avm-res-compute-virtualmachinescaleset`: VM Scale Set
- `avm-res-network-bastionhost`: Bastion Host
- Pattern: `avm-ptn-hubnetworking`: hub-and-spoke network topology
- Pattern: `avm-ptn-alz`: Azure Landing Zone
- Utility: `avm-utl-regions`: region metadata (short codes, paired regions)

## When AVM Falls Short

An AVM gap is **real** only if:
1. The resource type has no AVM module in the catalog, OR
2. The existing AVM module is in `Orphaned` or `Deprecated` status, OR
3. The module's interface lacks a required configuration that cannot be satisfied via `azapi_update_resource`.

If any of these conditions hold, write an ADR documenting the gap and the custom module design before coding. The ADR must include the AVM module search evidence (URL, status, date checked) and an owner commitment to upstream the module gap to the AVM team.

## Forking vs Extending

Do not fork AVM modules. If an AVM module lacks a feature:
1. Open an issue on the AVM GitHub repo.
2. Use `azapi_update_resource` to patch the missing attribute alongside the AVM module call while the upstream fix is in progress.
3. Remove the `azapi_update_resource` workaround once the AVM module releases the fix.

```hcl
# Temporary: set a property not yet exposed by the AVM module
resource "azapi_update_resource" "kv_network_acl_patch" {
  type        = "Microsoft.KeyVault/vaults@2023-07-01"
  resource_id = module.key_vault.resource_id

  body = {
    properties = {
      networkAcls = {
        defaultAction = "Deny"
        bypass        = "AzureServices"
      }
    }
  }
}
```
