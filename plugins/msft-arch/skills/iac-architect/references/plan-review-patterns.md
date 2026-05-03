# Plan Review Patterns

A `terraform plan` output is the contract between the IaC author and the infrastructure reviewer. Reading it correctly is a learnable skill. This file documents how to interpret plans, what to look for in a PR review, and how to automate plan comment posting.

## Reading a Terraform Plan

Terraform uses four symbols and several action types:

| Symbol | Meaning | Reviewer action |
|---|---|---|
| `+` (green) | Resource will be created | Confirm it should exist; verify name and region |
| `-` (red) | Resource will be destroyed | STOP: confirm destruction is intentional |
| `~` (yellow) | Resource will be updated in-place | Review changed attributes |
| `-/+` (red+green) | Resource will be replaced (destroy then create) | HIGH RISK: downtime may occur; confirm or refactor |
| `<=` | Data source will be read | Normal; verify the data source config |

### Additions: what to check
- Name matches naming conventions (`references/terraform-azure-baseline.md`)
- Region is in the approved list
- Mandatory tags present: `cost-center`, `environment`, `owner`, `project`, `expiry`
- SKU / tier is appropriate for the environment (not prod-grade SKU in dev)
- Depends on the right VNet / subnet if network-isolated

### Destroys: what to check
- Is this intentional? A rename in HCL causes a destroy+create.
- Is there data that will be lost? (Storage accounts, databases, Key Vaults)
- Is there a `prevent_destroy = true` lifecycle rule that should exist but does not?
- Is soft-delete or backup configured so the resource can be recovered?

```hcl
resource "azurerm_key_vault" "main" {
  # ...
  lifecycle {
    prevent_destroy = true   # blocks accidental destroy; must be removed explicitly to delete
  }
}
```

### Replacements: what to check
- Which attribute changed caused the replacement? (`forces replacement` annotation in plan)
- Can the attribute be set with `lifecycle { ignore_changes }` to avoid replacement?
- Is there a zero-downtime path? (e.g., blue-green for App Service, snapshot-restore for databases)
- Does the replacement plan include dependent resources that will also be destroyed?

## Automated Plan Posting

### Atlantis (self-hosted)

Atlantis listens for PR events, runs `terraform plan` per changed directory, and posts the output as a PR comment. Configuration:

```yaml
# atlantis.yaml at repo root
version: 3
automerge: false
parallel_plan: true
parallel_apply: false

projects:
  - name: orders-dev
    dir: environments/dev
    workspace: default
    terraform_version: v1.9.8
    autoplan:
      when_modified: ["**/*.tf", "**/*.tfvars"]
      enabled: true
    apply_requirements:
      - approved
      - mergeable

  - name: orders-prod
    dir: environments/prod
    workspace: default
    terraform_version: v1.9.8
    autoplan:
      when_modified: ["**/*.tf", "**/*.tfvars"]
      enabled: true
    apply_requirements:
      - approved
      - mergeable
```

Atlantis applies only after a PR is approved and has the `atlantis apply` comment; no auto-apply in production projects.

### tfcmt (GitHub Actions, lightweight)

For teams that do not run Atlantis, `tfcmt` posts formatted plan output as a GitHub PR comment from a GitHub Actions workflow:

```yaml
# .github/workflows/terraform-pr.yml
name: Terraform PR
on:
  pull_request:
    paths:
      - "environments/**"

permissions:
  id-token: write       # OIDC
  contents: read
  pull-requests: write  # tfcmt needs this

jobs:
  plan:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "~1.9"

      - name: Terraform Init
        run: terraform init
        working-directory: environments/${{ matrix.env }}

      - name: tflint
        run: tflint --recursive
        working-directory: environments/${{ matrix.env }}

      - name: checkov
        run: checkov -d . --framework terraform --quiet
        working-directory: environments/${{ matrix.env }}

      - name: Conftest
        run: |
          terraform plan -out=tfplan.binary
          terraform show -json tfplan.binary > plan.json
          conftest test plan.json --policy ../../policies/conftest/rules
        working-directory: environments/${{ matrix.env }}

      - name: tfcmt Plan
        run: |
          tfcmt --owner ${{ github.repository_owner }} \
                --repo ${{ github.event.repository.name }} \
                --pr ${{ github.event.number }} \
                -- terraform plan -no-color -out=tfplan.binary
        working-directory: environments/${{ matrix.env }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Apply runs in a separate workflow triggered on `push` to `main` (after PR merge), requiring the same policy gates to pass again.

## Human Review Checklist

Before approving a Terraform plan PR, verify:

```text
[ ] No unexpected destroys: all destroys are documented in the PR description
[ ] No unexpected replacements: replacement items have been assessed for downtime impact
[ ] Naming conventions match standards (CAF / org conventions)
[ ] All new resources have mandatory tags in the plan output
[ ] Region is approved for the environment
[ ] AVM modules used where available (no raw azurerm_ resources for AVM-covered types)
[ ] No secrets in tfvars (check changed .tfvars files)
[ ] SKU / tier appropriate for environment (no Premium in dev, no Basic in prod)
[ ] State backend key is environment-scoped (not shared across environments)
[ ] Policy gates (tflint, checkov, conftest) all passed in CI (visible as green checks)
[ ] Drift baseline is current (if brownfield): plan is additive only, no surprise removals
```

## Plan Analysis Tips

### Spot resource count regressions

```bash
# Count additions, changes, destructions from plan output
terraform plan -no-color 2>&1 | grep -E "^Plan:" 
# Plan: 3 to add, 1 to change, 0 to destroy.
```

Any non-zero destroy count in a production PR requires an explicit acknowledgment comment from the PR author explaining why the destruction is safe.

### Narrow a large plan to changed resources only

```bash
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary | jq '
  .resource_changes[]
  | select(.change.actions | map(. != "no-op") | any)
  | {address, actions: .change.actions}
'
```

This pipes the JSON plan through jq to surface only resources with actual changes. Useful when a large module produces 100+ resources and you need to find the 3 that changed.
