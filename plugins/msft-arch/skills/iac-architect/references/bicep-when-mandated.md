# Bicep: When Mandated

Bicep is the secondary IaC tool. Use it only when an explicit org policy prohibits non-Microsoft tooling. If that mandate exists, this file covers everything needed to build production-grade Bicep deployments with the same quality bar as the Terraform baseline.

## When Bicep is Acceptable

Confirmed acceptable scenarios:
1. **Microsoft-only tooling mandate**: org policy prohibits HashiCorp-licensed or third-party tooling on company-managed infrastructure.
2. **Azure Government / sovereign cloud**: some sovereign deployments have compliance requirements that restrict toolchain sourcing.
3. **Azure Arc or Microsoft Fabric deployments**: a small number of Azure control-plane resources have Bicep-native support before `azurerm` provider support lands.

In all other cases: Terraform. Do not choose Bicep because "the team knows it"; that is a training gap, not an architectural decision.

## Parity Gaps with Terraform

Bicep lacks several Terraform features that matter for production IaC:

| Terraform capability | Bicep equivalent | Gap |
|---|---|---|
| Remote state with locking | No native state (ARM tracks deployment history) | Bicep has no queryable state; re-running a deployment re-evaluates from live Azure |
| Workspace / environment isolation | Separate parameter files per deployment scope | Workable but more verbose |
| `for_each` over complex objects | `@batchSize` + `for` loops | Limited; object iteration is less ergonomic |
| Data sources (read existing resources) | `existing` keyword | Equivalent |
| Provider plugins (azapi, azuread) | ARM API calls via `extensionResourceType` | More verbose; requires knowing ARM API versions |
| `lifecycle { ignore_changes }` | No equivalent | Harder to suppress drift noise for out-of-band managed attributes |
| `terraform plan -refresh-only` | `az deployment group what-if` | what-if is close but not stateful |
| Import brownfield resources | No native import; use ARM Export → Bicep decompile | Lower fidelity; decompiled Bicep needs manual cleanup |

## AVM Bicep Modules

AVM publishes both Terraform and Bicep modules. The Bicep registry is the [Bicep Public Module Registry](https://github.com/Azure/bicep-registry-modules). Consume via the `br/public:` registry alias:

```bicep
// main.bicep
module keyVault 'br/public:avm/res/key-vault/vault:0.11.0' = {
  name: 'keyVaultDeployment'
  params: {
    name: 'kv-orders-prod-eus2'
    location: location
    sku: 'premium'
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true
    tags: tags
  }
}
```

Check module versions at `mcr.microsoft.com/bicep/avm/res/`; versions are independently published for Bicep vs Terraform AVM modules.

## What-If and Preflight Validation

Bicep's equivalent of `terraform plan` is `az deployment group what-if`. Always run it before apply and post the output as a PR comment.

```bash
# Preview changes (equivalent of terraform plan)
az deployment group what-if \
  --resource-group rg-orders-prod-eus2 \
  --template-file main.bicep \
  --parameters @params.prod.json \
  --validation-level Provider   # full validation including RBAC preflight
```

Validation levels (Azure CLI 2.76+):
- `Provider` (default): full validation + RBAC permission checks
- `ProviderNoRbac`: full resource validation, read-only permission check (useful in dev)
- `Template`: static syntax check only; skips preflight and permission checks

```bash
# Deploy (gated by CI approval)
az deployment group create \
  --resource-group rg-orders-prod-eus2 \
  --template-file main.bicep \
  --parameters @params.prod.json \
  --confirm-with-what-if        # shows what-if output and prompts before applying
```

For CI, suppress the interactive prompt:

```bash
az deployment group create \
  --resource-group rg-orders-prod-eus2 \
  --template-file main.bicep \
  --parameters @params.prod.json \
  --mode Incremental             # never Complete mode in production
```

## Bicep CI/CD Pipeline Structure

Mirror the Terraform PR workflow:

```text
lint (bicep build --lint)
  └─> preflight validate (az deployment group validate)
        └─> what-if (post output as PR comment)
              └─> human approval gate
                    └─> deploy (az deployment group create)
                          └─> smoke test
```

```yaml
# GitHub Actions: Bicep CI snippet
- name: Bicep Lint
  run: az bicep build --file main.bicep

- name: Preflight Validate
  run: |
    az deployment group validate \
      --resource-group rg-orders-prod-eus2 \
      --template-file main.bicep \
      --parameters @params.prod.json

- name: What-If
  run: |
    az deployment group what-if \
      --resource-group rg-orders-prod-eus2 \
      --template-file main.bicep \
      --parameters @params.prod.json \
      --validation-level Provider \
      --no-pretty-print | tee whatif.json
```

## Parameter File Hygiene

Use separate `.bicepparam` files per environment (Bicep 0.18+) rather than plain JSON parameter files:

```bicep
// params.prod.bicepparam
using 'main.bicep'

param environment = 'prod'
param location = 'eastus2'
param costCenter = 'eng-platform'
param owner = 'platform-team@example.com'
param project = 'orders-api'
param expiry = 'permanent'
```

Secrets use `az keyvault secret show` in the pipeline; never inline in parameter files.
