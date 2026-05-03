# Policy-as-Code

Three-layer policy stack for every Terraform project: tflint (provider lint) → checkov (CIS benchmarks) → OPA/Conftest (org rules). All three run in CI on every PR before the plan is posted.

## tflint: Provider-Specific Lint

tflint with the `terraform_provider_azurerm` plugin catches Azure-specific mistakes that the Terraform core parser cannot: deprecated resource attributes, invalid SKU names, missing required tags at authoring time.

### Configuration

```hcl
# .tflint.hcl
plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

plugin "azurerm" {
  enabled = true
  version = "0.28.0"
  source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
}

rule "terraform_required_version" {
  enabled = true
}

rule "terraform_required_providers" {
  enabled = true
}

rule "azurerm_resource_missing_tags" {
  enabled  = true
  tags     = ["cost-center", "environment", "owner", "project", "expiry"]
}
```

### CI integration

```bash
tflint --init
tflint --recursive --format=compact
```

Fail the pipeline on any tflint error. Warnings are acceptable as informational only.

## checkov: CIS Benchmark Scanning

checkov scans HCL directly (no plan required) against the CIS Microsoft Azure Foundations Benchmark. Run on every PR and on every merge to `main`.

```bash
checkov -d environments/prod \
  --framework terraform \
  --output cli \
  --output junitxml \
  --output-file-path . \
  --compact \
  --quiet \
  --check CKV_AZURE_1,CKV_AZURE_2   # example: only run specific checks
  # or omit --check to run all CIS checks
```

Recommended baseline checks for Azure (do not suppress without documented exception):
- `CKV_AZURE_36`: Storage Account: restrict public access
- `CKV_AZURE_33`: Storage Account: enable HTTPS traffic only
- `CKV_AZURE_41`: Key Vault: enable soft delete
- `CKV_AZURE_42`: Key Vault: enable purge protection
- `CKV_AZURE_109`: Key Vault: ensure access is via Private Endpoint or network ACL
- `CKV_AZURE_13`: App Service: use HTTPS only
- `CKV_AZURE_17`: App Service: disable FTP state
- `CKV2_AZURE_2`: VNet: enable DDoS protection (skip for non-production unless explicitly required)

Suppress individual checks with inline comments only when a compensating control is documented:

```hcl
resource "azurerm_storage_account" "logs" {
  # checkov:skip=CKV2_AZURE_2:DDoS plan not required for internal log storage (cost-benefit ADR-004)
  ...
}
```

## OPA / Conftest: Org-Wide Policy Rules

OPA + Conftest enforces org-specific rules that checkov does not cover: mandatory tags, naming conventions, approved regions, module source restrictions.

### Policy rule examples (Rego)

```rego
# policies/conftest/rules/tags.rego
package main

import future.keywords.in

deny[msg] {
  resource := input.resource_changes[_]
  resource.type in {"azurerm_resource_group", "azurerm_storage_account", "azurerm_key_vault"}
  required_tags := {"cost-center", "environment", "owner", "project", "expiry"}
  provided_tags := {k | resource.change.after.tags[k]}
  missing := required_tags - provided_tags
  count(missing) > 0
  msg := sprintf(
    "Resource '%s' (%s) is missing required tags: %v",
    [resource.address, resource.type, missing]
  )
}
```

```rego
# policies/conftest/rules/regions.rego
package main

approved_regions := {"eastus2", "westus2", "westeurope", "northeurope"}

deny[msg] {
  resource := input.resource_changes[_]
  location := resource.change.after.location
  not location in approved_regions
  msg := sprintf(
    "Resource '%s' deploys to unapproved region '%s'. Approved: %v",
    [resource.address, location, approved_regions]
  )
}
```

```rego
# policies/conftest/rules/modules.rego
package main

deny[msg] {
  module := input.configuration.module_calls[name]
  source := module.source
  not startswith(source, "registry.terraform.io/modules/Azure/avm-")
  not startswith(source, "../")    # allow local relative paths for custom modules
  msg := sprintf(
    "Module '%s' sources from '%s'. Only AVM modules (registry.terraform.io/modules/Azure/avm-*) or local paths are allowed.",
    [name, source]
  )
}
```

### Running Conftest in CI

```bash
# Generate a plan in JSON format (required by Conftest)
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > plan.json

# Run policy checks
conftest test plan.json \
  --policy policies/conftest/rules \
  --data policies/conftest/data \
  --all-namespaces
```

Conftest exits non-zero if any `deny` rule fires. Block the PR merge on non-zero exit.

## Pre-Commit Integration

Enforce lint and documentation locally before commits reach CI:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.1
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
        args:
          - "--args=--config=__GIT_WORKING_DIR__/.tflint.hcl"
      - id: terraform_docs
        args:
          - "--hook-config=--path-to-file=README.md"
          - "--hook-config=--add-to-existing-file=true"
          - "--hook-config=--create-file-if-not-exist=true"
      - id: checkov
        args:
          - "--args=--framework terraform --quiet"
```

`terraform_docs` auto-generates the `## Requirements`, `## Providers`, `## Inputs`, and `## Outputs` sections of every module `README.md`. Enforce in CI with `terraform-docs --check` if the pre-commit hook is not universally adopted.
