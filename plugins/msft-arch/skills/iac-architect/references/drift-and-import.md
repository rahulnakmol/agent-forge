# Drift Detection and Brownfield Import

Drift is any difference between what Terraform believes exists (state) and what actually exists in Azure. Left undetected, drift causes plan surprises, failed applies, and security regressions. Import is the inverse: teaching Terraform about resources that exist in Azure but are not yet in state.

## Drift Detection: Nightly Refresh

Run a scheduled CI job nightly:

```yaml
# GitHub Actions example
on:
  schedule:
    - cron: "0 2 * * *"   # 02:00 UTC nightly

jobs:
  drift-detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "~1.9"
      - name: Terraform Init
        run: terraform init
        working-directory: environments/prod
      - name: Drift Check
        id: plan
        run: |
          terraform plan -refresh-only -detailed-exitcode -out=drift.tfplan 2>&1 | tee drift.log
          echo "exitcode=$?" >> $GITHUB_OUTPUT
        working-directory: environments/prod
      - name: Alert on Drift
        if: steps.plan.outputs.exitcode == '2'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '[DRIFT] Production infrastructure drift detected',
              body: 'Nightly drift check found unexpected changes. Review drift.log artifact.',
              labels: ['drift', 'infrastructure']
            })
```

Exit code semantics for `terraform plan`:
- `0`: no changes (clean)
- `1`: error
- `2`: changes present (drift or pending intent)

`-refresh-only` updates state to match live Azure without proposing resource modifications; it only proposes state updates. Review and apply the refresh plan to re-baseline state after confirming the drift is legitimate.

## Set-Diff False Positives

Some Azure resource types produce permanent plan noise that is NOT real drift. Recognise these patterns before alerting:

### Application Gateway: backend address pools

The `azurerm_application_gateway` resource shows backend address pool members as changed on every plan if AKS updates the pool via the AGIC ingress controller. These are managed out-of-band; suppress with `lifecycle { ignore_changes = [backend_address_pool, backend_http_settings, http_listener, request_routing_rule, probe] }` when AGIC owns the configuration.

```hcl
resource "azurerm_application_gateway" "main" {
  # ... configuration ...

  lifecycle {
    ignore_changes = [
      backend_address_pool,
      backend_http_settings,
      http_listener,
      request_routing_rule,
      probe,
      tags["last-modified-by-agic"],
    ]
  }
}
```

### NSG Security Rules: Azure-managed rules

Azure injects default security rules and, for some services, service-managed rules into NSGs. These appear as unexpected additions in `terraform plan`. Use `azurerm_network_security_rule` resources (separate from the NSG) rather than inline `security_rule` blocks to avoid replacement noise.

### Role Assignments: GUID non-determinism

Role assignment resource IDs contain a GUID. If the GUID is not pinned in HCL, Terraform may show a replacement on every plan. Always supply a deterministic `name` using `uuid()` seeded from known inputs, or use the AVM pattern which stabilises IDs automatically.

## Brownfield Import: `import {}` Blocks (Terraform 1.5+)

For Terraform 1.5 and later, declare imports as code using `import {}` blocks. This approach is version-controlled, reviewable in PRs, and idempotent (Terraform removes the block from state after the import succeeds).

### Step 1: Discover existing resources

Use `aztfexport` to auto-generate import blocks for an entire resource group:

```bash
aztfexport resource-group \
  --subscription-id <sub-id> \
  rg-orders-prod-eus2 \
  --generate-import-block \
  --output-dir ./import-output
```

This produces `import.tf` (import blocks) and `generated.tf` (resource configurations). Review both files; do not use `generated.tf` verbatim. Refactor to use AVM modules.

### Step 2: Write import blocks

```hcl
import {
  id = "/subscriptions/<sub>/resourceGroups/rg-orders-prod-eus2/providers/Microsoft.KeyVault/vaults/kv-orders-prod-eus2"
  to = module.key_vault.azurerm_key_vault.this
}

import {
  id = "/subscriptions/<sub>/resourceGroups/rg-orders-prod-eus2/providers/Microsoft.Network/virtualNetworks/vnet-orders-prod-eus2"
  to = module.virtual_network.azurerm_virtual_network.this
}
```

### Step 3: Plan and review

```bash
terraform plan -generate-config-out=generated_resources.tf
```

When `to` points to a module resource that already has a configuration, `-generate-config-out` is not needed. Review the plan output: imports show as `# (imported)` in green; any attribute mismatch shows as a proposed change.

### Step 4: Apply and clean up

```bash
terraform apply
```

After a successful apply, remove the `import {}` blocks; they are no longer needed. Commit the cleaned-up code.

### Legacy: `terraform import` CLI

Prefer `import {}` blocks. Use `terraform import` CLI only for Terraform versions below 1.5 or for one-off emergency imports. It is not version-controlled and cannot be reviewed in a PR.

```bash
# Legacy: only when import block is not available
terraform import module.key_vault.azurerm_key_vault.this \
  "/subscriptions/<sub>/resourceGroups/rg-orders-prod-eus2/providers/Microsoft.KeyVault/vaults/kv-orders-prod-eus2"
```
