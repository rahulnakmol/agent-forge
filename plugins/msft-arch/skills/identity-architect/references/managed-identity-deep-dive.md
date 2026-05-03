# Managed Identity Deep Dive

Managed Identity is the zero-secret identity for Azure-hosted workloads. This file covers the system vs user-assigned trade-offs, token acquisition patterns, and common troubleshooting scenarios that go beyond the decision tree.

---

## System-Assigned vs User-Assigned: The Real Trade-offs

The decision tree gives you the rule. Here is the reasoning:

| Trade-off | System-assigned | User-assigned |
|---|---|---|
| **Lifecycle** | Tied to the resource; deleted with it | Independent; must be explicitly deleted |
| **Blue/green deployments** | Role assignments must be recreated on new resource | Role assignments survive; new resource just references the MI |
| **IaC (Terraform)** | Identity created implicitly; principal ID available only after apply | Identity pre-created; principal ID known before compute resource creation, enabling deterministic role assignments in the same plan |
| **Shared across resources** | No (1:1 binding) | Yes: one MI, N resources |
| **Audit / governance** | Slightly harder (identity name = resource name) | Explicit name; shows clearly in audit logs |
| **IMDS token endpoint** | Same (`169.254.169.254`) | Same, but must pass `client_id` parameter |

**When to prefer user-assigned despite higher setup cost**:
- Any blue/green or slot-swap deployment pattern
- Multiple Container App revisions that share the same downstream RBAC grants
- Pre-allocation of role assignments in IaC before the compute resource is deployed
- Shared MI across Function App + Logic App in the same logical domain

---

## Enabling Managed Identity

### System-assigned (Azure CLI)

```bash
# App Service
az webapp identity assign \
  --name myapp \
  --resource-group myRG

# Container App
az containerapp identity assign \
  --name myapp \
  --resource-group myRG \
  --system-assigned

# Function App
az functionapp identity assign \
  --name myfunc \
  --resource-group myRG
```

### User-assigned (Terraform, preferred)

```hcl
resource "azurerm_user_assigned_identity" "api" {
  name                = "mi-api-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

resource "azurerm_role_assignment" "api_kv_secrets_user" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.api.principal_id
}

resource "azurerm_linux_web_app" "api" {
  # ...
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.api.id]
  }
}
```

---

## Token Acquisition

### DefaultAzureCredential (recommended for all Azure-hosted code)

`DefaultAzureCredential` tries a chain of credential sources in order: Environment → Workload Identity → Managed Identity → Visual Studio → Azure CLI → Azure PowerShell → Azure Developer CLI. In production (Azure-hosted), it falls through to Managed Identity. In local dev, it uses the developer's CLI login.

```csharp
// System-assigned: no configuration needed
var credential = new DefaultAzureCredential();

// User-assigned: specify the client ID
var credential = new DefaultAzureCredential(
    new DefaultAzureCredentialOptions
    {
        ManagedIdentityClientId = Environment.GetEnvironmentVariable("AZURE_MI_CLIENT_ID")
    });

// Use with any Azure SDK client
var secretClient = new SecretClient(
    new Uri("https://myvault.vault.azure.net/"),
    credential);

var secret = await secretClient.GetSecretAsync("my-secret");
```

### ChainedTokenCredential (explicit control)

Use when you need explicit ordering or want to exclude certain credential types:

```csharp
// Production: MI only. Dev: Azure CLI fallback.
var credential = new ChainedTokenCredential(
    new ManagedIdentityCredential(),
    new AzureCliCredential());

var graphClient = new GraphServiceClient(credential,
    new[] { "https://graph.microsoft.com/.default" });
```

### Direct IMDS Token Acquisition (advanced / diagnostic)

```bash
# From within the Azure resource: useful for debugging
curl -s "http://169.254.169.254/metadata/identity/oauth2/token" \
  -H "Metadata: true" \
  --data-urlencode "resource=https://vault.azure.net" \
  --data-urlencode "api-version=2018-02-01"

# User-assigned: add client_id
curl -s "http://169.254.169.254/metadata/identity/oauth2/token" \
  -H "Metadata: true" \
  --data-urlencode "resource=https://vault.azure.net" \
  --data-urlencode "api-version=2018-02-01" \
  --data-urlencode "client_id=<MI_CLIENT_ID>"
```

---

## Federated Credential Pattern (Managed Identity + External Workload)

User-assigned Managed Identities can act as the trust anchor for Workload Identity Federation. External workloads (GitHub Actions, AKS pods) exchange their OIDC token for an access token scoped to the MI's RBAC grants. This is the preferred pattern over app-registration-based federation when you want to centralise RBAC grants on an MI rather than a service principal.

```bash
az identity federated-credential create \
  --name gha-prod-deploy \
  --identity-name mi-deploy-prod \
  --resource-group myRG \
  --issuer "https://token.actions.githubusercontent.com" \
  --subject "repo:my-org/my-repo:environment:production" \
  --audiences "api://AzureADTokenExchange"
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `DefaultAzureCredential` fails locally | No Azure CLI login / expired token | `az login` or `az account get-access-token` to verify |
| `ManagedIdentityCredential` fails on Azure | MI not enabled on resource | `az webapp identity show`: check `principalId` is non-null |
| RBAC `403 Forbidden` even with MI enabled | Role assignment missing or propagation delay | Verify with `az role assignment list --assignee <principalId>`; allow up to 5 min for propagation |
| User-assigned MI token fails | `client_id` not passed | Pass `ManagedIdentityClientId` in `DefaultAzureCredentialOptions` |
| Token for wrong scope | Missing `/.default` suffix on resource URI | Use `https://vault.azure.net/.default` not `https://vault.azure.net` |
| `403` from Key Vault after role assignment | RBAC model vs access policy model mismatch | Key Vault must be in RBAC permission model; check via `az keyvault show --query properties.enableRbacAuthorization` |
