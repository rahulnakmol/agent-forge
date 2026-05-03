# Workload Identity Federation

Zero-secret authentication for workloads running outside Azure. The workload exchanges its OIDC token (issued by GitHub, Kubernetes, GitLab, etc.) for an Entra access token via a federation trust; no long-lived secret is ever stored.

---

## How the Exchange Works

1. The external system (GitHub Actions runner, K8s pod) holds an OIDC token issued by its own IdP.
2. The workload calls Microsoft identity platform with this token + the client ID of the trusted app registration or user-assigned MI.
3. Entra validates the token against the registered OIDC issuer, checks the `subject` claim against the federated credential configuration, and issues an Azure access token.
4. The workload uses the Azure token to access Azure resources.

No secret is ever stored. The OIDC token is short-lived and audience-restricted. This is strictly better than a service principal with a rotating secret.

---

## GitHub Actions Setup

### Step 1: Create federated credential on an app registration

```bash
az ad app create --display-name "GitHub-Deploy-Prod"
# note the appId

az ad app federated-credential create \
  --id <appId> \
  --parameters '{
    "name": "gha-prod-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:my-org/my-repo:environment:production",
    "description": "GitHub Actions production deployment",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Create service principal for the app, assign RBAC
az ad sp create --id <appId>
az role assignment create \
  --assignee <appId> \
  --role "Contributor" \
  --scope /subscriptions/<subscriptionId>/resourceGroups/myRG
```

### Alternatively: federate directly to a user-assigned MI (preferred, cleaner RBAC)

```bash
az identity federated-credential create \
  --name gha-prod-deploy \
  --identity-name mi-deploy-prod \
  --resource-group myRG \
  --issuer "https://token.actions.githubusercontent.com" \
  --subject "repo:my-org/my-repo:environment:production" \
  --audiences "api://AzureADTokenExchange"
```

### Step 2: GitHub Actions workflow

```yaml
name: Deploy

on:
  push:
    branches: [main]

permissions:
  id-token: write    # required: requests the OIDC JWT from GitHub
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production   # matches the subject claim "environment:production"

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC, no secret)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          # No client-secret: uses OIDC token exchange

      - name: Deploy
        run: az webapp deploy --name myapp --resource-group myRG --src-path ./dist
```

**Secrets stored in GitHub** (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`) are not sensitive; they are identifiers, not secrets. The actual trust is in the federated credential configuration in Entra. An attacker with only these values cannot get a token unless they are running from the exact matching GitHub repository + environment.

---

## Subject Claim Patterns

The `subject` claim in the federated credential must exactly match what GitHub puts in the OIDC token:

| Scenario | Subject value |
|---|---|
| Branch trigger | `repo:org/repo:ref:refs/heads/main` |
| Tag trigger | `repo:org/repo:ref:refs/tags/v1.0.0` |
| Environment | `repo:org/repo:environment:production` |
| Pull request | `repo:org/repo:pull_request` |
| Reusable workflow | `repo:org/shared-workflows:.github/workflows/deploy.yml@main` |

Use **environment-scoped subjects** for production deployments; this enforces that deployments only happen through approved environments with their own protection rules and reviewers.

---

## AKS Workload Identity (Pod-to-MI Binding)

Azure Workload Identity for AKS binds a Kubernetes ServiceAccount to a user-assigned Managed Identity using OIDC federation. Pods with the annotated service account receive an Azure access token as a projected volume; no SDK changes are needed for `DefaultAzureCredential`.

### Step 1: Enable OIDC issuer on AKS cluster

```bash
az aks update \
  --name myCluster \
  --resource-group myRG \
  --enable-oidc-issuer \
  --enable-workload-identity

# Get the OIDC issuer URL
OIDC_ISSUER=$(az aks show \
  --name myCluster \
  --resource-group myRG \
  --query "oidcIssuerProfile.issuerUrl" -o tsv)
```

### Step 2: Create MI and federated credential

```bash
az identity create \
  --name mi-myapp \
  --resource-group myRG

MI_CLIENT_ID=$(az identity show --name mi-myapp --resource-group myRG --query clientId -o tsv)
MI_PRINCIPAL_ID=$(az identity show --name mi-myapp --resource-group myRG --query principalId -o tsv)

# Federated credential: AKS SA in namespace myapp, service account myapp-sa
az identity federated-credential create \
  --name aks-myapp-sa \
  --identity-name mi-myapp \
  --resource-group myRG \
  --issuer "$OIDC_ISSUER" \
  --subject "system:serviceaccount:myapp:myapp-sa" \
  --audiences "api://AzureADTokenExchange"

# Assign RBAC to the MI
az role assignment create \
  --assignee-object-id "$MI_PRINCIPAL_ID" \
  --role "Key Vault Secrets User" \
  --scope /subscriptions/.../vaults/myKeyVault \
  --assignee-principal-type ServicePrincipal
```

### Step 3: Kubernetes resources

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: myapp
  annotations:
    azure.workload.identity/client-id: "<MI_CLIENT_ID>"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
spec:
  template:
    metadata:
      labels:
        azure.workload.identity/use: "true"   # injects token volume
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: myapp
          image: myapp:latest
          # DefaultAzureCredential picks up the projected token automatically
          # No AZURE_CLIENT_ID env var needed when using system-assigned WI
```

---

## Terraform Module Pattern

```hcl
module "workload_identity" {
  source = "Azure/avm-res-managedidentity-userassignedidentity/azurerm"

  name                = "mi-${var.app_name}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location

  federated_credentials = {
    github_prod = {
      name    = "gha-${var.environment}"
      issuer  = "https://token.actions.githubusercontent.com"
      subject = "repo:${var.github_org}/${var.github_repo}:environment:${var.environment}"
      audiences = ["api://AzureADTokenExchange"]
    }
  }
}
```

---

## Security Boundary Considerations

- **Subject claim is the security boundary**: scope it as narrowly as possible (environment > branch > repo-wildcard).
- **Audience should always be `api://AzureADTokenExchange`** unless an alternate audience is explicitly required; restricts the token to Azure exchange only.
- **One federated credential per deployment environment**: do not share a single federation trust across production and staging; a staging pipeline compromise must not be able to deploy to production.
- **MI over app registration**: User-assigned MI federations keep RBAC on the MI itself; app-registration federations create a service principal in your tenant that is harder to audit at scale. Prefer MI for infrastructure deployments.
