# Azure DevOps Pipelines Baseline

Azure DevOps YAML pipelines are the standard for enterprise organisations with strict gate requirements, Azure Boards integration, and on-premises audit obligations. Classic pipelines are retired; disable their creation at the organisation level immediately.

---

## Foundational Decisions

- **YAML pipelines only.** In **Project Settings → Pipelines → Settings**, enable "Disable creation of classic build pipelines" and "Disable creation of classic release pipelines". Existing classic pipelines continue to run but cannot be recreated.
- **Workload Identity Federation for Azure service connections.** As of Azure DevOps sprint 253 (2025), new service connections use the Entra issuer (`https://login.microsoftonline.com/<tenant>/v2.0`) rather than the legacy Azure DevOps issuer. This is the default for all new connections; no client secrets stored.
- **Managed DevOps Pools (ADP) for self-hosted needs.** Generally available (2025). Provides scalable, Azure-hosted runner pools with managed identity, Key Vault certificate injection, and shorter agent-allocation time compared to VMSS pools.
- **Variable Groups linked to Key Vault** for secrets. Do not store secrets as plain-text pipeline variables.

---

## Service Connection Setup (Workload Identity Federation)

```bash
# Option 1: Let Azure DevOps create the federated credential automatically
# In Project Settings → Service Connections → New → Azure Resource Manager
# Select: Identity type = "User-assigned Managed Identity"
# This creates federated credentials on the MI automatically.

# Option 2: Manual setup for an existing managed identity
az identity federated-credential create \
  --name "ado-sc-my-project" \
  --identity-name "mi-ado-deploy" \
  --resource-group "rg-platform-identity" \
  --issuer "https://login.microsoftonline.com/<TENANT_ID>/v2.0" \
  --subject "<entra-prefix>/sc/<ado-org-id>/<service-connection-id>" \
  --audiences "api://AzureADTokenExchange"

# The subject format changed in 2025 (Entra issuer).
# The portal generates this automatically when you create a new service connection.
```

---

## Pipeline Skeleton: azure-pipelines.yml

This skeleton covers a multi-stage .NET 9 pipeline with Conventional Commits enforcement, build, test, staging deployment with smoke test, and production deployment with approval gate.

```yaml
# azure-pipelines.yml -- root of the repository
trigger:
  branches:
    include:
      - main
  paths:
    exclude:
      - '**/*.md'
      - '.github/**'

pr:
  branches:
    include:
      - main

variables:
  - group: platform-kv-vars          # Key Vault-linked variable group
  - name: DOTNET_VERSION
    value: '9.x'
  - name: IMAGE_REPOSITORY
    value: 'my-app'
  - name: REGISTRY
    value: 'myacr.azurecr.io'
  - name: CONTAINER_TAG
    value: '$(Build.SourceVersion)'

stages:
  # ─────────────────────────────────────────────────────────
  # Stage 1: Validate -- runs on every PR and push
  # ─────────────────────────────────────────────────────────
  - stage: Validate
    displayName: 'Validate'
    condition: always()
    jobs:
      - job: CommitLint
        displayName: 'Conventional Commits Lint'
        condition: eq(variables['Build.Reason'], 'PullRequest')
        pool:
          vmImage: 'ubuntu-24.04'
        steps:
          - checkout: self
            fetchDepth: 0

          - task: NodeTool@0
            inputs:
              versionSpec: '22.x'
            displayName: 'Install Node.js'

          - script: npm install --save-dev @commitlint/cli @commitlint/config-conventional
            displayName: 'Install commitlint'

          - script: |
              npx commitlint \
                --from "$(System.PullRequest.TargetBranchName)" \
                --verbose
            displayName: 'Lint commit messages'

      - job: Build
        displayName: 'Build & Unit Test'
        pool:
          vmImage: 'ubuntu-24.04'
        steps:
          - checkout: self

          - task: UseDotNet@2
            inputs:
              version: $(DOTNET_VERSION)
            displayName: 'Install .NET SDK'

          - task: DotNetCoreCLI@2
            inputs:
              command: restore
              projects: '**/*.csproj'
            displayName: 'Restore'

          - task: DotNetCoreCLI@2
            inputs:
              command: build
              projects: '**/*.csproj'
              arguments: '--no-restore --configuration Release'
            displayName: 'Build'

          - task: DotNetCoreCLI@2
            inputs:
              command: test
              projects: '**/*.Tests.csproj'
              arguments: >
                --no-build
                --configuration Release
                --logger "trx;LogFileName=TestResults.trx"
                --collect:"XPlat Code Coverage"
            displayName: 'Unit Tests'

          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'VSTest'
              testResultsFiles: '**/TestResults.trx'
              failTaskOnFailedTests: true
            displayName: 'Publish Test Results'

          - task: PublishCodeCoverageResults@2
            inputs:
              summaryFileLocation: '**/coverage.cobertura.xml'
            displayName: 'Publish Code Coverage'

  # ─────────────────────────────────────────────────────────
  # Stage 2: Package -- main branch only
  # ─────────────────────────────────────────────────────────
  - stage: Package
    displayName: 'Build & Push Image'
    dependsOn: Validate
    condition: |
      and(
        succeeded(),
        eq(variables['Build.SourceBranch'], 'refs/heads/main')
      )
    jobs:
      - job: BuildAndPush
        displayName: 'Build & Push Docker Image'
        pool:
          vmImage: 'ubuntu-24.04'
        steps:
          - checkout: self

          - task: AzureCLI@2
            displayName: 'Login to ACR and Push Image'
            inputs:
              azureSubscription: 'sc-platform-prod'  # WIF service connection
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az acr login --name $(echo "$(REGISTRY)" | cut -d. -f1)
                docker build \
                  --tag "$(REGISTRY)/$(IMAGE_REPOSITORY):$(CONTAINER_TAG)" \
                  --tag "$(REGISTRY)/$(IMAGE_REPOSITORY):latest" \
                  --file src/MyApp/Dockerfile \
                  .
                docker push "$(REGISTRY)/$(IMAGE_REPOSITORY):$(CONTAINER_TAG)"
                docker push "$(REGISTRY)/$(IMAGE_REPOSITORY):latest"

  # ─────────────────────────────────────────────────────────
  # Stage 3: Staging
  # ─────────────────────────────────────────────────────────
  - stage: DeployStaging
    displayName: 'Deploy - Staging'
    dependsOn: Package
    condition: succeeded()
    jobs:
      - deployment: DeployToStaging
        displayName: 'Deploy to Staging Environment'
        pool:
          vmImage: 'ubuntu-24.04'
        environment: 'staging'   # ADO Environment with approval checks
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  displayName: 'Update Container App (Staging)'
                  inputs:
                    azureSubscription: 'sc-platform-staging'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az containerapp update \
                        --name my-app-staging \
                        --resource-group rg-app-staging \
                        --image "$(REGISTRY)/$(IMAGE_REPOSITORY):$(CONTAINER_TAG)"

                - task: PowerShell@2
                  displayName: 'Smoke Test - Staging'
                  inputs:
                    targetType: 'inline'
                    script: |
                      $url = "https://my-app-staging.azurecontainerapps.io/health"
                      for ($i = 1; $i -le 10; $i++) {
                        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
                        if ($response.StatusCode -eq 200) {
                          Write-Host "Smoke test passed on attempt $i"
                          exit 0
                        }
                        Write-Host "Attempt $i: $($response.StatusCode) -- retrying"
                        Start-Sleep -Seconds 10
                      }
                      Write-Error "Smoke test failed after 10 attempts"
                      exit 1

  # ─────────────────────────────────────────────────────────
  # Stage 4: Production -- approval gate required
  # ─────────────────────────────────────────────────────────
  - stage: DeployProduction
    displayName: 'Deploy - Production'
    dependsOn: DeployStaging
    condition: succeeded()
    jobs:
      - deployment: DeployToProduction
        displayName: 'Deploy to Production Environment'
        pool:
          vmImage: 'ubuntu-24.04'
        environment: 'production'   # ADO Environment -- configure required approvers here
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  displayName: 'Update Container App (Production)'
                  inputs:
                    azureSubscription: 'sc-platform-prod'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az containerapp update \
                        --name my-app \
                        --resource-group rg-app-prod \
                        --image "$(REGISTRY)/$(IMAGE_REPOSITORY):$(CONTAINER_TAG)"

                - task: AzureCLI@2
                  displayName: 'Verify Production Health'
                  inputs:
                    azureSubscription: 'sc-platform-prod'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      PROD_URL="https://my-app.azurecontainerapps.io/health"
                      for i in {1..5}; do
                        STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL")
                        if [ "$STATUS" = "200" ]; then
                          echo "Production health check passed"
                          exit 0
                        fi
                        sleep 15
                      done
                      echo "Production health check failed"
                      exit 1
```

---

## ADO Environment Configuration

ADO Environments are the approval gate mechanism. Configure each environment in **Project Settings → Environments**.

| Environment | Approval policy |
|---|---|
| `staging` | Auto-approve (CI gate only; smoke tests are the gate) |
| `production` | Require at least 1 approver from the "release-approvers" group |
| `production` | Check: work item linked (Azure Boards integration, optional) |
| `production` | Check: branch policy; only from `main` |

```bash
# Create environments via Azure DevOps REST API or az devops CLI
az devops configure --defaults organization=https://dev.azure.com/my-org project=my-project

# List existing environments
az pipelines environment list --output table
```

---

## Variable Groups and Key Vault Integration

```yaml
# In the pipeline, reference a variable group linked to Azure Key Vault
variables:
  - group: platform-kv-vars   # Linked to Key Vault -- secrets are injected at runtime

# In ADO Library → Variable Groups → Link secrets from Azure Key Vault
# Map: KEY_VAULT_SECRET_NAME -> pipeline variable name
# The service connection used for Key Vault linkage must have "Key Vault Secrets User" RBAC role.
```

---

## Branch Policy Checklist

Configure these branch policies on `main` in **Repos → Branches → Branch Policies**:

| Policy | Setting |
|---|---|
| Require a minimum number of reviewers | 1 (or 2 for regulated orgs) |
| Check for linked work items | Optional but recommended |
| Check for comment resolution | Required |
| Limit merge types | Squash merge only (keeps history clean) |
| Build validation | Required; trigger the validate stage pipeline |
| Status checks | All stage status checks must pass |

---

## Pipeline as Code: Repository Layout

```text
repo-root/
├── azure-pipelines.yml              # Root pipeline -- main CI/CD
├── .azure/
│   ├── pipelines/
│   │   ├── templates/
│   │   │   ├── build-steps.yml      # Reusable step template
│   │   │   ├── deploy-steps.yml     # Reusable deploy template
│   │   │   └── smoke-test-steps.yml
│   │   ├── pr-validation.yml        # PR-only pipeline (commitlint + build)
│   │   └── nightly-drift.yml        # Nightly Terraform drift detection
│   └── environments/
│       ├── staging.yml              # Environment-specific variable overrides
│       └── production.yml
```

---

## Security Notes

- Never use PATs for Azure resource operations; use WIF service connections exclusively.
- Rotate any remaining PATs that exist for agent registration on a 90-day schedule; store expiry in Key Vault as a tag.
- Enable pipeline-level secret masking: Azure DevOps automatically masks variable-group secrets in logs when the variable is marked secret.
- Audit log: **Organisation Settings → Auditing → Export**; export monthly for compliance retention.
- For Managed DevOps Pools: assign a user-assigned managed identity to the pool (not system-assigned) so the identity is scoped and auditable.
