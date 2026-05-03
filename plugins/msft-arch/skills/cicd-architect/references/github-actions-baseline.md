# GitHub Actions Baseline

The baseline workflow pattern for all Azure-targeting GitHub Actions pipelines. Every repository that deploys to Azure uses OIDC; no PAT, no client secret, no long-lived credential stored as a GitHub Secret for Azure authentication.

---

## Authentication: Workload Identity Federation (OIDC)

GitHub Actions and Azure Entra ID support secretless authentication via OIDC. The pipeline requests a short-lived token from GitHub's OIDC provider; Entra ID validates the token against a preconfigured federated identity credential and issues an Azure access token. No secret is stored anywhere.

### Federated credential setup

Two patterns are supported. Prefer the **user-assigned managed identity** pattern for new work; it avoids the need for app registrations when those are restricted in the tenant.

**Option A: User-assigned managed identity (preferred)**

```bash
# 1. Create a user-assigned managed identity
az identity create \
  --name "gha-deploy-prod" \
  --resource-group "rg-platform-identity" \
  --location "australiaeast"

# 2. Capture the client ID and object ID
CLIENT_ID=$(az identity show \
  --name "gha-deploy-prod" \
  --resource-group "rg-platform-identity" \
  --query "clientId" -o tsv)

OBJECT_ID=$(az identity show \
  --name "gha-deploy-prod" \
  --resource-group "rg-platform-identity" \
  --query "principalId" -o tsv)

# 3. Assign the required role (Contributor scoped to a specific RG -- use least-privilege)
az role assignment create \
  --assignee "$OBJECT_ID" \
  --role "Contributor" \
  --scope "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/rg-app-prod"

# 4. Add a federated identity credential for the GitHub environment
#    Subject format: repo:<org>/<repo>:environment:<environment-name>
az identity federated-credential create \
  --name "gha-prod-environment" \
  --identity-name "gha-deploy-prod" \
  --resource-group "rg-platform-identity" \
  --issuer "https://token.actions.githubusercontent.com" \
  --subject "repo:my-org/my-repo:environment:production" \
  --audiences "api://AzureADTokenExchange"
```

**Option B: Entra app registration**

```bash
# 1. Create an app registration and service principal
az ad app create --display-name "gha-deploy-ci"
APP_ID=$(az ad app list --display-name "gha-deploy-ci" --query "[0].appId" -o tsv)
az ad sp create --id "$APP_ID"

# 2. Add federated credential (PR workflow -- scoped to pull_request event)
az ad app federated-credential create \
  --id "$APP_ID" \
  --parameters '{
    "name": "gha-pr-federated",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:my-org/my-repo:pull_request",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

**Federated credential subject formats**

| Trigger | Subject |
|---|---|
| Environment-scoped deploy | `repo:<org>/<repo>:environment:<name>` |
| Branch push | `repo:<org>/<repo>:ref:refs/heads/<branch>` |
| Tag push | `repo:<org>/<repo>:ref:refs/tags/<tag>` |
| Pull request | `repo:<org>/<repo>:pull_request` |

---

## Baseline Workflow: Build, Test, and Deploy

This workflow covers a .NET 9 application deployed to Azure App Service. Adapt service-specific steps for AKS (use `azure/aks-set-context` + `kubectl`) or Container Apps (use `azure/container-apps-deploy`).

Store the following in GitHub Secrets / Variables at the repository or environment level:

| Name | Scope | Value |
|---|---|---|
| `AZURE_CLIENT_ID` | Environment: production | Client ID of the user-assigned MI |
| `AZURE_TENANT_ID` | Repository | Entra tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Repository | Target subscription ID |

```yaml
# .github/workflows/ci-cd.yml
name: CI / CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  id-token: write   # Required for OIDC token request
  pull-requests: write  # Required for PR comments (tfcmt, test results)

jobs:
  # ─────────────────────────────────────────────
  # Job 1: Conventional Commits lint
  # ─────────────────────────────────────────────
  commitlint:
    name: Conventional Commits Lint
    runs-on: ubuntu-24.04
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install commitlint
        run: npm install --save-dev @commitlint/cli @commitlint/config-conventional

      - name: Lint commit messages
        run: npx commitlint \
          --from ${{ github.event.pull_request.base.sha }} \
          --to ${{ github.event.pull_request.head.sha }} \
          --verbose

  # ─────────────────────────────────────────────
  # Job 2: Build and unit test
  # ─────────────────────────────────────────────
  build:
    name: Build & Test
    runs-on: ubuntu-24.04
    needs: [commitlint]
    if: always() && (github.event_name == 'push' || needs.commitlint.result == 'success')

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.x'
          cache: true

      - name: Restore dependencies
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore --configuration Release

      - name: Run tests
        run: >
          dotnet test
          --no-build
          --configuration Release
          --logger "trx;LogFileName=test-results.trx"
          --collect:"XPlat Code Coverage"

      - name: Publish test results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: .NET Tests
          path: '**/TestResults/*.trx'
          reporter: dotnet-trx

      - name: Build Docker image
        run: |
          docker build \
            --tag "${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:${{ github.sha }}" \
            --file src/MyApp/Dockerfile \
            .

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: docker-tag
          path: |
            echo "${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:${{ github.sha }}" > docker-tag.txt
            cat docker-tag.txt

  # ─────────────────────────────────────────────
  # Job 3: Push image (main branch only)
  # ─────────────────────────────────────────────
  push-image:
    name: Push to ACR
    runs-on: ubuntu-24.04
    needs: [build]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: staging      # Environment-scoped OIDC token

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Login to Azure Container Registry
        run: az acr login --name ${{ vars.REGISTRY_NAME }}

      - name: Push Docker image
        run: |
          docker push "${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:${{ github.sha }}"
          docker tag "${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:${{ github.sha }}" \
                     "${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:latest"
          docker push "${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:latest"

  # ─────────────────────────────────────────────
  # Job 4: Deploy to staging (App Service example)
  # ─────────────────────────────────────────────
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-24.04
    needs: [push-image]
    environment: staging

    steps:
      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to App Service staging slot
        uses: azure/webapps-deploy@v3
        with:
          app-name: my-app-staging
          slot-name: staging
          images: ${{ vars.REGISTRY_LOGIN_SERVER }}/my-app:${{ github.sha }}

      - name: Run smoke tests against staging
        run: |
          STAGING_URL="https://my-app-staging-staging.azurewebsites.net"
          for i in {1..10}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_URL/health")
            if [ "$STATUS" = "200" ]; then
              echo "Smoke test passed (attempt $i)"
              exit 0
            fi
            echo "Attempt $i: HTTP $STATUS -- retrying in 10s"
            sleep 10
          done
          echo "Smoke test failed after 10 attempts"
          exit 1

  # ─────────────────────────────────────────────
  # Job 5: Deploy to production (requires approval)
  # ─────────────────────────────────────────────
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-24.04
    needs: [deploy-staging]
    environment: production     # Required reviewers configured in GitHub Environments

    steps:
      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Swap staging slot to production
        run: |
          az webapp deployment slot swap \
            --name my-app \
            --resource-group rg-app-prod \
            --slot staging \
            --target-slot production

      - name: Verify production health
        run: |
          PROD_URL="https://my-app.azurewebsites.net"
          for i in {1..5}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL/health")
            if [ "$STATUS" = "200" ]; then
              echo "Production health check passed"
              exit 0
            fi
            sleep 15
          done
          echo "Production health check failed -- consider swap rollback"
          exit 1
```

---

## Commitlint Configuration

Place at repository root. References Conventional Commits as defined in `standards/references/tooling/repo-baseline.md`.

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Enforce the types defined in repo-baseline.md
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'chore', 'docs', 'refactor',
        'test', 'build', 'ci', 'perf', 'style'
      ]
    ],
    'subject-case': [2, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']],
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 120],
  }
};
```

---

## Reusable Workflow Pattern

Extract the Azure Login + deploy steps into a reusable callable workflow for use across multiple repos in the org.

```yaml
# .github/workflows/reusable-azure-deploy.yml
name: Reusable Azure Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
      app-name:
        required: true
        type: string
    secrets:
      AZURE_CLIENT_ID:
        required: true
      AZURE_TENANT_ID:
        required: true
      AZURE_SUBSCRIPTION_ID:
        required: true

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-24.04
    environment: ${{ inputs.environment }}
    steps:
      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ inputs.app-name }}
          images: ${{ inputs.image-tag }}
```

---

## Runner Selection

| Scenario | Runner |
|---|---|
| Standard builds | `ubuntu-24.04` (Microsoft-hosted) |
| Windows-only builds | `windows-2025` (Microsoft-hosted) |
| Private network access, custom tooling | Self-hosted runner or Managed DevOps Pools (ADP) |
| Large compute (build caches, ML) | Managed DevOps Pools with custom Azure VM SKU |

Managed DevOps Pools (generally available, 2025) provide Azure-hosted self-managed runners with pool-level identity, Key Vault certificate integration, and standby agent pre-warming. Prefer over self-hosted VMs for enterprise scenarios that need private network access without the operational overhead of managing runner VMs.

---

## Security Hardening Checklist

- Pin all third-party Actions to a full commit SHA, not a tag: `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` (not `@v4`)
- Set `permissions: contents: read` at the workflow level; grant only what each job needs
- Never log secrets; use `::add-mask::` for any dynamically constructed sensitive values
- Enable GitHub's secret scanning and push protection on every repository
- Use `GITHUB_TOKEN` for intra-repo operations; use OIDC for Azure operations; avoid PATs
- Scope federated credential subjects to the narrowest applicable value (environment > branch > repo)
