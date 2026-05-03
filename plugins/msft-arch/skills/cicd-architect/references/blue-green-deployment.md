# Blue-Green Deployment

Blue-green deployment is the release strategy for stateful workloads where ring deployments (progressive traffic percentages) are not viable. Examples: services with database schema migrations, session-aware applications, binary protocol services (SignalR, gRPC streaming), and workloads where two incompatible API versions cannot coexist.

Blue-green keeps two complete environments ("blue" for current and "green" for new) and performs a hard cutover once the green environment has passed all smoke tests.

---

## When to Use Blue-Green Over Ring Deployments

| Signal | Use blue-green |
|---|---|
| Schema migration ships with the release | Yes; two versions cannot share the same schema |
| Session affinity required | Yes; split traffic would route some sessions to the wrong version |
| Binary protocol (SignalR, gRPC streaming) | Yes; mid-connection migration is not safe |
| Stateful service with in-memory state | Yes; ring traffic split would corrupt in-flight state |
| Stateless HTTP microservice | No; use ring deployments |
| Event-driven function with idempotent processing | No; use ring deployments |

---

## Container Apps Blue-Green

Azure Container Apps natively supports blue-green deployment using revision labels. The "blue" label points to the current stable revision; the "green" label points to the candidate revision. Production traffic goes to blue until green is verified, then a label swap redirects all traffic.

### Initial state

```bash
# Create the app -- blue is the initial stable revision
az containerapp create \
  --resource-group rg-app-prod \
  --name my-app \
  --environment aca-env-prod \
  --image myacr.azurecr.io/my-app:1.0.0 \
  --revision-suffix blue-1-0-0 \
  --revisions-mode multiple \
  --ingress external \
  --target-port 8080

# Label the current revision as "blue"
az containerapp revision label add \
  --resource-group rg-app-prod \
  --name my-app \
  --label blue \
  --revision my-app--blue-1-0-0

# Set 100% traffic to blue
az containerapp ingress traffic set \
  --resource-group rg-app-prod \
  --name my-app \
  --label-weight blue=100
```

### Deploy the green revision

```bash
NEW_TAG="$1"    # e.g. 1.1.0 or a SHA
NEW_SUFFIX="${NEW_TAG//[^a-zA-Z0-9]/-}"

# Deploy new revision with 0% traffic -- it starts inactive
az containerapp update \
  --resource-group rg-app-prod \
  --name my-app \
  --image "myacr.azurecr.io/my-app:${NEW_TAG}" \
  --revision-suffix "green-${NEW_SUFFIX}"

GREEN_REVISION=$(az containerapp revision list \
  --name my-app \
  --resource-group rg-app-prod \
  --query "sort_by([?properties.active], &properties.createdTime)[-1].name" \
  -o tsv)

# Label the new revision as "green"
az containerapp revision label add \
  --resource-group rg-app-prod \
  --name my-app \
  --label green \
  --revision "$GREEN_REVISION"

echo "Green revision deployed: $GREEN_REVISION"
echo "Access green via label FQDN for smoke testing before cutover"
```

### Smoke test the green revision via its label URL

The label URL provides direct access to the green revision without affecting production traffic:

```bash
# Get the green label FQDN (accessible without touching production traffic)
GREEN_FQDN=$(az containerapp show \
  --resource-group rg-app-prod \
  --name my-app \
  --query "properties.configuration.ingress.fqdn" -o tsv | \
  sed 's/my-app\./my-app---green./')

# In practice, the label FQDN format is: <app-name>---<label>.<env-fqdn>
# Verify by:
az containerapp revision list \
  --name my-app \
  --resource-group rg-app-prod \
  --query "[?properties.active].{name:name, fqdn:properties.fqdn}" \
  -o table

# Run smoke tests against the green label URL
smoke_test() {
  local url="$1"
  local pass=0
  for i in {1..10}; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "${url}/health")
    if [ "$STATUS" = "200" ]; then
      pass=$((pass + 1))
      echo "Probe ${i}: PASS"
    else
      echo "Probe ${i}: FAIL (HTTP ${STATUS})"
    fi
    sleep 3
  done
  if [ "$pass" -lt 8 ]; then
    echo "Smoke tests failed: only ${pass}/10 probes passed"
    return 1
  fi
  echo "Smoke tests passed: ${pass}/10 probes"
}

smoke_test "https://${GREEN_FQDN}"
```

### Cutover: swap blue and green

```bash
# Cutover: move 100% of production traffic to green
az containerapp ingress traffic set \
  --resource-group rg-app-prod \
  --name my-app \
  --label-weight green=100 blue=0

echo "Cutover complete -- all traffic on green revision"
```

### Verify and finalise

```bash
# Verify production health for 5 minutes post-cutover
PROD_URL="https://my-app.azurecontainerapps.io"
FAILED=0
for i in {1..30}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "${PROD_URL}/health")
  if [ "$STATUS" != "200" ]; then
    FAILED=$((FAILED + 1))
    echo "Probe ${i}: FAIL (HTTP ${STATUS})"
  else
    echo "Probe ${i}: OK"
  fi
  sleep 10
done

if [ "$FAILED" -gt 3 ]; then
  echo "Post-cutover verification failed -- initiating rollback"
  exit 1
fi

# Re-label: green becomes the new blue for the next deployment
az containerapp revision label remove \
  --resource-group rg-app-prod \
  --name my-app \
  --label blue

CURRENT_REVISION=$(az containerapp ingress traffic show \
  --resource-group rg-app-prod \
  --name my-app \
  --query "[?weight==\`100\`].revisionName | [0]" -o tsv)

az containerapp revision label add \
  --resource-group rg-app-prod \
  --name my-app \
  --label blue \
  --revision "$CURRENT_REVISION"

az containerapp revision label remove \
  --resource-group rg-app-prod \
  --name my-app \
  --label green

# Deactivate the old blue revision after a 30-minute post-cutover window
echo "Finalisation complete. Deactivate old revision after 30-minute window."
```

---

## Rollback Procedure

Rollback is a label swap back to the original blue revision. The old blue revision stays active throughout the green deployment, making rollback instant.

```bash
# ROLLBACK -- restore all traffic to previous blue revision
# This must be executable by on-call in under 2 minutes without pipeline access.

BLUE_REVISION=$(az containerapp revision list \
  --name my-app \
  --resource-group rg-app-prod \
  --query "[?properties.active && contains(name, 'blue')].name | [0]" -o tsv)

az containerapp ingress traffic set \
  --resource-group rg-app-prod \
  --name my-app \
  --label-weight blue=100 green=0

echo "Rollback complete -- 100% traffic on blue (${BLUE_REVISION})"

# Deactivate the failed green revision
GREEN_REVISION=$(az containerapp revision list \
  --name my-app \
  --resource-group rg-app-prod \
  --query "[?properties.active && contains(name, 'green')].name | [0]" -o tsv)

az containerapp revision deactivate \
  --name my-app \
  --resource-group rg-app-prod \
  --revision "$GREEN_REVISION"
```

---

## Database Migration Coordination

Blue-green with schema migrations requires a forward-compatible migration strategy. Two versions of the application must be able to run against the same database during the cutover window.

**Expand-contract pattern (non-negotiable for blue-green)**:

| Phase | Action | Both versions compatible? |
|---|---|---|
| Migration PR | Add new column (nullable, no default) | Yes; old version ignores it |
| Green deploy + cutover | Green reads and writes new column | Yes; old version still works |
| Stabilisation (1+ day) | Confirm no rollback needed | n/a |
| Cleanup PR | Remove old column; add NOT NULL constraint | Yes; old version decommissioned |

Never deploy a breaking schema change (rename, drop, NOT NULL on existing) in the same release as the application code change. They must be separate PRs and releases.

---

## Azure DevOps Pipeline: Blue-Green Workflow

```yaml
# Stage in azure-pipelines.yml -- blue-green deployment
- stage: BlueGreenDeploy
  displayName: 'Blue-Green Deploy'
  dependsOn: DeployStaging
  condition: succeeded()
  jobs:
    - deployment: BlueGreenCutover
      displayName: 'Blue-Green Cutover'
      pool:
        vmImage: 'ubuntu-24.04'
      environment: 'production'
      strategy:
        runOnce:
          deploy:
            steps:
              - task: AzureCLI@2
                displayName: 'Deploy Green Revision'
                inputs:
                  azureSubscription: 'sc-platform-prod'
                  scriptType: 'bash'
                  scriptLocation: 'scriptPath'
                  scriptPath: 'scripts/blue-green-deploy.sh'
                  arguments: '$(Build.SourceVersion) my-app rg-app-prod'

              - task: AzureCLI@2
                displayName: 'Smoke Test Green'
                inputs:
                  azureSubscription: 'sc-platform-prod'
                  scriptType: 'bash'
                  scriptLocation: 'scriptPath'
                  scriptPath: 'scripts/smoke-test.sh'
                  arguments: 'green'

              - task: AzureCLI@2
                displayName: 'Cutover to Green'
                inputs:
                  azureSubscription: 'sc-platform-prod'
                  scriptType: 'bash'
                  scriptLocation: 'inlineScript'
                  inlineScript: |
                    az containerapp ingress traffic set \
                      --name my-app \
                      --resource-group rg-app-prod \
                      --label-weight green=100 blue=0

              - task: AzureCLI@2
                displayName: 'Post-Cutover Verification'
                inputs:
                  azureSubscription: 'sc-platform-prod'
                  scriptType: 'bash'
                  scriptLocation: 'scriptPath'
                  scriptPath: 'scripts/post-cutover-verify.sh'
                onError: continue    # Continue to rollback step on failure

              - task: AzureCLI@2
                displayName: 'Rollback on Failure'
                condition: failed()
                inputs:
                  azureSubscription: 'sc-platform-prod'
                  scriptType: 'bash'
                  scriptLocation: 'inlineScript'
                  inlineScript: |
                    echo "Verification failed -- rolling back to blue"
                    az containerapp ingress traffic set \
                      --name my-app \
                      --resource-group rg-app-prod \
                      --label-weight blue=100 green=0
                    echo "Rollback complete"
```

---

## AKS Blue-Green via Service Swap

For AKS workloads, blue-green is implemented with two Deployments and a Service selector swap:

```yaml
# service.yaml -- points to blue initially
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: my-app
spec:
  selector:
    app: my-app
    slot: blue       # Change to "green" for cutover
  ports:
    - port: 80
      targetPort: 8080
```

```bash
# Cutover: patch the Service selector to point to green
kubectl patch service my-app \
  --namespace my-app \
  --type=json \
  --patch='[{"op": "replace", "path": "/spec/selector/slot", "value": "green"}]'

# Rollback: revert selector to blue
kubectl patch service my-app \
  --namespace my-app \
  --type=json \
  --patch='[{"op": "replace", "path": "/spec/selector/slot", "value": "blue"}]'
```

With GitOps (Flux), never use `kubectl patch` directly. Commit the Service manifest change to the config repo and let Flux reconcile; this keeps the rollback auditable.
