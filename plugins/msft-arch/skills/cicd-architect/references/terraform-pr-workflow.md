# Terraform Plan-in-PR Workflow

Terraform plan output must appear as a PR comment before any human approves infrastructure changes. No one should approve a plan they have not read. Apply runs exclusively in the post-merge pipeline; never locally, never in a PR branch, never with `-auto-approve` outside the CI/CD system.

Two tools implement this pattern:

- **tfcmt**: lightweight GitHub comment posting; pairs naturally with GitHub Actions; no server required.
- **Atlantis**: self-hosted server with deeper PR integration; supports Azure DevOps; handles concurrent plan/apply locking.

---

## Tool Selection

| Dimension | tfcmt | Atlantis |
|---|---|---|
| Architecture | CLI binary; runs inside any CI step | Self-hosted server; webhook-driven |
| GitHub Actions | Natural fit; call `tfcmt plan` in a workflow step | Requires Atlantis server to be running and accessible |
| Azure DevOps | Possible via inline posting; less native | Native ADO PR comment support |
| Concurrent plan locking | No; rely on Terraform state locking | Yes; Atlantis serialises plans per repo+workdir |
| Auto-apply | No built-in; apply is a separate workflow | `atlantis apply` in PR comment; configurable |
| Self-hosted requirement | No | Yes; needs a VM or Container App to host |
| Best for | GitHub Actions, small/mid teams, simple pipelines | Larger teams, ADO + GitHub, complex workspace graphs |

**Decision rule**: Use tfcmt for GitHub Actions pipelines. Use Atlantis for Azure DevOps pipelines or teams that need concurrent-plan locking across multiple PRs.

---

## tfcmt Configuration

### Installation

```bash
# Install tfcmt (latest release from GitHub)
TFCMT_VERSION="v4.14.2"
curl -sSL "https://github.com/suzuki-shunsuke/tfcmt/releases/download/${TFCMT_VERSION}/tfcmt_linux_amd64.tar.gz" \
  | tar xzf - tfcmt
chmod +x tfcmt
sudo mv tfcmt /usr/local/bin/
```

### tfcmt.yaml

Place at the repository root or specify with `--config`:

```yaml
# tfcmt.yaml
ci:
  pr:
    variables:
      - PR_NUMBER
  vars:
    - PLAN_WORKFLOW_NAME

terraform:
  plan:
    template: |
      ## Terraform Plan - {{ .WorkingDir }}

      {{if .Result}}
      **Result**: `{{ .Result }}`
      {{end}}

      {{if .HasChanges}}
      <details>
      <summary>Plan output (expand)</summary>

      ```hcl
      {{ .CombinedOutput }}
      ```

      </details>
      {{else}}
      No changes. Infrastructure is up-to-date.
      {{end}}

      {{if .HasErrors}}
      **Errors:**
      ```
      {{ .CombinedOutput }}
      ```
      {{end}}

      ---
      *Planned by: {{ .Vars.PLAN_WORKFLOW_NAME }} | SHA: `{{ .Vars.GITHUB_SHA }}`*

  apply:
    template: |
      ## Terraform Apply - {{ .WorkingDir }}

      {{if .Result}}
      **Result**: `{{ .Result }}`
      {{end}}

      <details>
      <summary>Apply output (expand)</summary>

      ```
      {{ .CombinedOutput }}
      ```

      </details>
```

---

## GitHub Actions: Terraform PR Workflow

This workflow runs on every PR that touches `.tf` files. It posts the plan as a PR comment. Apply is a separate job that runs only after the PR is merged to `main`.

```yaml
# .github/workflows/terraform-pr.yml
name: Terraform Plan on PR

on:
  pull_request:
    paths:
      - 'infrastructure/**/*.tf'
      - 'infrastructure/**/*.tfvars'
      - '.github/workflows/terraform-pr.yml'

permissions:
  id-token: write
  contents: read
  pull-requests: write   # Required for tfcmt to post PR comments

env:
  TF_VERSION: '1.9.8'
  WORKING_DIR: infrastructure/environments/production

jobs:
  terraform-plan:
    name: Terraform Plan
    runs-on: ubuntu-24.04

    defaults:
      run:
        working-directory: ${{ env.WORKING_DIR }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
          terraform_wrapper: false   # Disable wrapper -- tfcmt needs raw exit codes

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Install tfcmt
        run: |
          TFCMT_VERSION="v4.14.2"
          curl -sSL \
            "https://github.com/suzuki-shunsuke/tfcmt/releases/download/${TFCMT_VERSION}/tfcmt_linux_amd64.tar.gz" \
            | tar xzf - tfcmt
          chmod +x tfcmt
          sudo mv tfcmt /usr/local/bin/

      - name: Terraform Init
        env:
          ARM_USE_OIDC: true
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        run: terraform init -input=false

      - name: Run tflint
        uses: terraform-linters/setup-tflint@v4
        with:
          tflint_version: latest
      - run: |
          tflint --init
          tflint --format compact
        working-directory: ${{ env.WORKING_DIR }}

      - name: Run checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: ${{ env.WORKING_DIR }}
          framework: terraform
          output_format: cli
          soft_fail: false

      - name: Terraform Plan (via tfcmt)
        env:
          ARM_USE_OIDC: true
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PLAN_WORKFLOW_NAME: ${{ github.workflow }}
          GITHUB_SHA: ${{ github.sha }}
        run: |
          tfcmt \
            --config ../../tfcmt.yaml \
            -var "PLAN_WORKFLOW_NAME=$PLAN_WORKFLOW_NAME" \
            -var "GITHUB_SHA=$GITHUB_SHA" \
            plan -- \
            terraform plan \
              -input=false \
              -no-color \
              -var-file=terraform.tfvars \
              -out=tfplan.binary

      - name: Upload plan artifact
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: ${{ env.WORKING_DIR }}/tfplan.binary
          retention-days: 3
```

---

## GitHub Actions: Terraform Apply Workflow (Post-Merge Only)

Apply runs only after the PR is merged to `main`. It downloads the plan artifact from the plan workflow run and applies it.

```yaml
# .github/workflows/terraform-apply.yml
name: Terraform Apply

on:
  push:
    branches: [main]
    paths:
      - 'infrastructure/**/*.tf'
      - 'infrastructure/**/*.tfvars'

permissions:
  id-token: write
  contents: read
  actions: read     # Required to download artifact from the plan workflow

env:
  TF_VERSION: '1.9.8'
  WORKING_DIR: infrastructure/environments/production

jobs:
  terraform-apply:
    name: Terraform Apply
    runs-on: ubuntu-24.04

    defaults:
      run:
        working-directory: ${{ env.WORKING_DIR }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
          terraform_wrapper: false

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Terraform Init
        env:
          ARM_USE_OIDC: true
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        run: terraform init -input=false

      - name: Terraform Apply
        env:
          ARM_USE_OIDC: true
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        run: |
          # Apply using a fresh plan (re-plan at apply time for safety)
          # This ensures no drift between plan and apply if branch was stale.
          terraform plan \
            -input=false \
            -no-color \
            -var-file=terraform.tfvars \
            -out=tfplan.binary

          terraform apply \
            -input=false \
            -no-color \
            tfplan.binary
```

---

## Atlantis Configuration

Atlantis is self-hosted. Deploy it as an Azure Container App or AKS workload. Configure it via `atlantis.yaml` at the repository root.

### atlantis.yaml

```yaml
# atlantis.yaml -- root of the repository
version: 3
automerge: false    # Never auto-merge after apply -- humans approve the PR

projects:
  - name: production
    dir: infrastructure/environments/production
    workspace: default
    autoplan:
      when_modified:
        - '**/*.tf'
        - '**/*.tfvars'
        - '../../../modules/**/*.tf'
      enabled: true
    apply_requirements:
      - approved              # Require at least one PR approval before apply
      - mergeable             # PR must be mergeable (all status checks green)

  - name: staging
    dir: infrastructure/environments/staging
    workspace: default
    autoplan:
      when_modified:
        - '**/*.tf'
        - '**/*.tfvars'
      enabled: true
    apply_requirements:
      - mergeable             # Staging auto-apply after CI passes
```

### Atlantis server deployment: Container Apps

```bash
# Deploy Atlantis to Container Apps with Managed Identity for Azure auth
az containerapp create \
  --resource-group rg-platform-ops \
  --name atlantis \
  --environment aca-env-ops \
  --image ghcr.io/runatlantis/atlantis:latest \
  --ingress external \
  --target-port 4141 \
  --min-replicas 1 \
  --max-replicas 1 \
  --env-vars \
    ATLANTIS_REPO_ALLOWLIST="github.com/my-org/*" \
    ATLANTIS_GH_USER="atlantis-bot" \
    ATLANTIS_GH_WEBHOOK_SECRET="secretref:atlantis-gh-webhook-secret" \
    ATLANTIS_GH_TOKEN="secretref:atlantis-gh-token" \
    ARM_USE_OIDC="true" \
    ARM_CLIENT_ID="secretref:azure-client-id" \
    ARM_TENANT_ID="secretref:azure-tenant-id" \
    ARM_SUBSCRIPTION_ID="secretref:azure-subscription-id" \
  --secrets \
    atlantis-gh-webhook-secret=keyvaultref:<kv-uri>/secrets/atlantis-gh-webhook-secret \
    atlantis-gh-token=keyvaultref:<kv-uri>/secrets/atlantis-gh-token \
    azure-client-id=keyvaultref:<kv-uri>/secrets/azure-client-id \
    azure-tenant-id=keyvaultref:<kv-uri>/secrets/azure-tenant-id \
    azure-subscription-id=keyvaultref:<kv-uri>/secrets/azure-subscription-id
```

### Atlantis workflow

Users interact with Atlantis via PR comments:

| Comment | Action |
|---|---|
| `atlantis plan` | Trigger a plan for the PR's changed projects |
| `atlantis plan -p production` | Plan a specific project |
| `atlantis apply` | Apply all planned projects (requires approval) |
| `atlantis apply -p production` | Apply a specific project |
| `atlantis unlock` | Unlock the PR workspace if it gets stuck |

---

## Nightly Drift Detection

Drift detection runs nightly regardless of whether a PR is open. It uses `terraform plan -refresh-only` to detect any out-of-band changes to Azure resources.

```yaml
# .github/workflows/terraform-drift.yml
name: Terraform Drift Detection

on:
  schedule:
    - cron: '0 2 * * *'   # 2 AM UTC nightly
  workflow_dispatch:

permissions:
  id-token: write
  contents: read
  issues: write

jobs:
  drift-check:
    name: Check for Drift
    runs-on: ubuntu-24.04

    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: '1.9.8'
          terraform_wrapper: false

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Terraform Init
        env:
          ARM_USE_OIDC: true
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        working-directory: infrastructure/environments/production
        run: terraform init -input=false

      - name: Drift Detection
        id: plan
        env:
          ARM_USE_OIDC: true
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        working-directory: infrastructure/environments/production
        run: |
          set +e
          terraform plan \
            -refresh-only \
            -input=false \
            -no-color \
            -var-file=terraform.tfvars \
            -detailed-exitcode
          EXIT_CODE=$?
          echo "exit-code=$EXIT_CODE" >> "$GITHUB_OUTPUT"
          set -e
          # Exit code 2 means there are changes (drift)
          # Exit code 0 means no changes
          # Exit code 1 means error
          if [ "$EXIT_CODE" = "1" ]; then exit 1; fi

      - name: Open GitHub Issue on Drift
        if: steps.plan.outputs.exit-code == '2'
        run: |
          gh issue create \
            --title "Infrastructure drift detected -- $(date +'%Y-%m-%d')" \
            --body "The nightly Terraform drift check detected out-of-band changes in production. Review the workflow run and apply the plan or remediate manually." \
            --label "infrastructure,drift"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Coordinate the drift detection schedule with `/iac-architect`; the nightly cadence and alerting channel are defined by the IaC design, not the CI/CD pipeline alone.
