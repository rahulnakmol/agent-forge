# RBAC Role Design

Least-privilege access via Azure RBAC. This file covers built-in role selection, scope hierarchy, custom role authoring (and when not to), and common patterns. The decision principle: **custom RBAC role only after exhausting built-in roles + ADR justifying the gap**.

---

## Scope Hierarchy

Azure RBAC assignments inherit downward. Assign at the narrowest scope that satisfies the requirement:

```text
Management Group
  └── Subscription
        └── Resource Group
              └── Resource
```

- **Management Group scope**: Reserved for policies and governance roles (Blueprint Contributor, Policy Contributor). Avoid granting data-plane roles at MG scope.
- **Subscription scope**: For platform engineers managing the subscription itself. Owner/Contributor at subscription scope should go through PIM (eligible only).
- **Resource Group scope**: Default for most application identities. A web app's Managed Identity gets `Key Vault Secrets User` on the Key Vault RG, not the subscription.
- **Resource scope**: When you need to isolate access to a single resource within a shared RG (e.g., one Container Registry for multiple apps; each app MI gets `AcrPull` on its specific registry).

---

## Built-In Role Catalog: Common Assignments

Exhaust this list before reaching for a custom role:

| Role | Data plane | Control plane | Use for |
|---|---|---|---|
| `Reader` | No | Read | Auditors, monitoring agents, read-only dashboards |
| `Contributor` | No | Read + Write | App teams owning a resource group (via PIM) |
| `Owner` | No | Full | Subscription owners (PIM eligible only) |
| `Key Vault Secrets User` | Secrets read | None | App MI reading secrets |
| `Key Vault Secrets Officer` | Secrets read/write/delete | None | DevOps/CD pipelines writing secrets |
| `Key Vault Crypto User` | Keys sign/verify/encrypt/decrypt | None | App MI using keys for crypto operations |
| `Storage Blob Data Reader` | Blob read | None | App MI reading blob storage |
| `Storage Blob Data Contributor` | Blob read/write/delete | None | App MI writing blobs |
| `Storage Queue Data Message Sender` | Queue send | None | App MI sending to queues |
| `AcrPull` | Container image pull | None | AKS kubelet MI, Container Apps |
| `AcrPush` | Image push | None | CI/CD pipeline MI |
| `Service Bus Data Sender` | Send messages | None | App MI publishing to Service Bus |
| `Service Bus Data Receiver` | Receive messages | None | App MI consuming from Service Bus |
| `Cognitive Services OpenAI User` | Call Azure OpenAI | None | App MI calling AOAI endpoint |
| `Monitoring Metrics Publisher` | Publish custom metrics | None | App MI writing to Azure Monitor |
| `Website Contributor` | None | App Service R/W | DevOps deploying to App Service |

---

## Terraform Role Assignment Pattern

```hcl
# Prefer deterministic role assignment names using uuid() from known inputs
resource "azurerm_role_assignment" "api_kv_read" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.api.principal_id

  # Prevent Terraform from recreating on every plan due to random suffix
  # Use skip_service_principal_aad_check = true for Managed Identities
  skip_service_principal_aad_check = true
}
```

---

## When to Create a Custom Role

Custom roles have a maintenance cost; they must be kept in sync as Azure adds new actions. Only create one when all three conditions are met:

1. No built-in role matches the required permission set.
2. The gap is not solved by combining two role assignments.
3. An ADR documents the gap and the specific actions required.

Common legitimate gaps:
- "Read + restart" on App Service with no write access to config (built-in Website Contributor includes config write)
- "Manage only alerts on a specific resource" without resource-level write

### Custom Role Template

```json
{
  "Name": "App Service Operator: Read + Restart",
  "IsCustom": true,
  "Description": "Can view App Service properties and restart the application. Cannot modify configuration.",
  "Actions": [
    "Microsoft.Web/sites/read",
    "Microsoft.Web/sites/restart/action",
    "Microsoft.Web/sites/operationresults/read",
    "Microsoft.Web/sites/diagnostics/read"
  ],
  "NotActions": [],
  "DataActions": [],
  "NotDataActions": [],
  "AssignableScopes": [
    "/subscriptions/<subscriptionId>/resourceGroups/myRG"
  ]
}
```

```bash
az role definition create --role-definition custom-role.json
```

Store custom role definitions in your IaC repository alongside the ADR that justifies them.

---

## Least-Privilege Patterns

### Principle: no standing privileged access on production

All Owner, Contributor, and equivalent data-plane roles on production resources should be PIM-eligible, not permanently assigned. See `pim-and-jit.md`.

### Principle: MI identity for every service, no shared identities

One service = one Managed Identity (or one user-assigned MI for a logical service group). Never share an MI across logically separate services; the blast radius on compromise is too wide.

### Principle: scope as narrow as the use case

CI/CD pipeline deploying to App Service gets `Website Contributor` on the specific App Service resource, not `Contributor` on the RG. Verify the actual required actions by testing with `az role assignment check` before widening scope.

### Anti-patterns to call out in reviews

| Anti-pattern | Risk | Correct pattern |
|---|---|---|
| `Owner` on production RG, permanently assigned | Full compromise on breach | PIM eligible only |
| Subscription-scope `Contributor` for app MI | Lateral movement to unrelated resources | RG-scope or resource-scope |
| Shared service principal for all pipelines | Single credential compromise = all pipelines compromised | Per-pipeline user-assigned MI with Workload Identity Federation |
| `Key Vault Contributor` for app reading secrets | Can modify Key Vault access policies (privilege escalation) | `Key Vault Secrets User` (data plane only) |
| Wildcard action (`*`) in custom roles without NotActions | Unintentional permissions on new resource types Azure adds later | List explicit actions; review quarterly |

---

## Access Policy vs RBAC on Key Vault

Azure Key Vault supports two permission models:
- **Vault access policies** (legacy): Tenant-wide, coarse; gives access to all keys OR all secrets OR all certs in a vault. No resource-level granularity.
- **Azure RBAC** (preferred): Standard ARM role assignments scoped to vault or individual secret/key/cert. Consistent with all other Azure RBAC, auditable in the same place.

**Migrate to RBAC**: Enable `enableRbacAuthorization: true` on the vault. Remove legacy access policies after role assignments are in place.

```bash
az keyvault update \
  --name myKeyVault \
  --resource-group myRG \
  --enable-rbac-authorization true
```
