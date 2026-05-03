# Ring Deployments

Ring deployments (canary → 1% → 10% → 50% → 100%) are the production release strategy for all stateless services on AKS and Azure Container Apps. Every release goes through rings, no exceptions. The ring gate is automated: a health check and configurable soak time must pass before the pipeline advances traffic to the next ring.

---

## Ring Model

| Ring | Traffic | Soak Time | Audience | Rollback trigger |
|---|---|---|---|---|
| Canary | < 1% (internal) | 5 min | Internal team, feature-flag users | Any error > baseline |
| Ring 1 | 1% | 15 min | Random 1% of users | Error rate > 0.5% OR p99 latency > 2× baseline |
| Ring 2 | 10% | 30 min | Random 10% of users | Same as Ring 1 |
| Ring 3 | 50% | 60 min | Half of production traffic | Same as Ring 1 |
| Ring 4 | 100% | Ongoing | Full production | Incident / SLO breach |

Soak times are minimum values. The gate automation checks health metrics at the end of the soak period. If metrics are degraded, the pipeline fails and human action is required to either rollback or manually advance.

---

## Container Apps Ring Deployment

Azure Container Apps supports traffic splitting via revision weights. The pipeline progresses through rings by updating the ingress traffic configuration.

### Initial setup: enable multiple revision mode

```bash
# Create the app with multiple revision mode enabled
az containerapp create \
  --resource-group rg-app-prod \
  --name my-app \
  --environment aca-env-prod \
  --image myacr.azurecr.io/my-app:1.0.0 \
  --revisions-mode multiple \
  --ingress external \
  --target-port 8080 \
  --min-replicas 2 \
  --max-replicas 20

# Or enable multiple revisions on an existing app
az containerapp revision set-mode \
  --resource-group rg-app-prod \
  --name my-app \
  --mode multiple
```

### Deploy new revision (ring start)

```bash
NEW_TAG="${GITHUB_SHA:-$(git rev-parse --short HEAD)}"
NEW_SUFFIX="${NEW_TAG:0:8}"

# Deploy new revision with 0% traffic (it starts inactive, accessible via label URL)
az containerapp update \
  --resource-group rg-app-prod \
  --name my-app \
  --image "myacr.azurecr.io/my-app:${NEW_TAG}" \
  --revision-suffix "${NEW_SUFFIX}"

# Label the new revision as "canary" for direct access
az containerapp revision label add \
  --resource-group rg-app-prod \
  --name my-app \
  --label canary \
  --revision "my-app--${NEW_SUFFIX}"
```

### Ring progression script

```bash
#!/usr/bin/env bash
# ring-deploy.sh -- called from CI/CD pipeline
# Usage: ./ring-deploy.sh <app-name> <resource-group> <new-revision-name>

set -euo pipefail

APP_NAME="$1"
RESOURCE_GROUP="$2"
NEW_REVISION="$3"
OLD_REVISION=$(az containerapp revision list \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "sort_by([?properties.active], &properties.createdTime)[-2].name" \
  -o tsv)

HEALTH_URL="https://${APP_NAME}.azurecontainerapps.io/health"
CANARY_URL=$(az containerapp revision show \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --revision "$NEW_REVISION" \
  --query "properties.fqdn" -o tsv 2>/dev/null || echo "")

wait_and_check_health() {
  local soak_seconds="$1"
  local ring_name="$2"
  echo "--- Ring ${ring_name}: soaking for ${soak_seconds}s ---"
  sleep "$soak_seconds"

  local pass=0
  for i in {1..5}; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$HEALTH_URL")
    if [ "$STATUS" = "200" ]; then
      pass=$((pass + 1))
    fi
    sleep 5
  done

  if [ "$pass" -lt 4 ]; then
    echo "Health check failed at ring ${ring_name} -- ${pass}/5 probes passed. Aborting."
    exit 1
  fi
  echo "Ring ${ring_name} health check passed (${pass}/5 probes)"
}

set_traffic() {
  local new_weight="$1"
  local old_weight=$((100 - new_weight))
  echo "Setting traffic: new=${new_weight}% old=${old_weight}%"
  az containerapp ingress traffic set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --revision-weight "${NEW_REVISION}=${new_weight}" "${OLD_REVISION}=${old_weight}"
}

# Ring 1: 1%
set_traffic 1
wait_and_check_health 900 "1%"    # 15-minute soak

# Ring 2: 10%
set_traffic 10
wait_and_check_health 1800 "10%"  # 30-minute soak

# Ring 3: 50%
set_traffic 50
wait_and_check_health 3600 "50%"  # 60-minute soak

# Ring 4: 100%
set_traffic 100
echo "Ring deployment complete -- 100% traffic on ${NEW_REVISION}"

# Deactivate old revision
az containerapp revision deactivate \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --revision "$OLD_REVISION"

echo "Old revision ${OLD_REVISION} deactivated."
```

### GitHub Actions ring deployment workflow

```yaml
# .github/workflows/ring-deploy.yml
name: Ring Deployment

on:
  workflow_dispatch:
    inputs:
      image-tag:
        description: 'Docker image tag to deploy'
        required: true

permissions:
  id-token: write
  contents: read

jobs:
  ring-deploy:
    name: Progressive Ring Deployment
    runs-on: ubuntu-24.04
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy new revision (0% traffic)
        id: deploy
        run: |
          SUFFIX="${{ inputs.image-tag }}"
          az containerapp update \
            --name my-app \
            --resource-group rg-app-prod \
            --image "myacr.azurecr.io/my-app:${{ inputs.image-tag }}" \
            --revision-suffix "${SUFFIX:0:8}"

          NEW_REVISION=$(az containerapp revision list \
            --name my-app \
            --resource-group rg-app-prod \
            --query "sort_by([?properties.active], &properties.createdTime)[-1].name" \
            -o tsv)
          echo "new-revision=$NEW_REVISION" >> "$GITHUB_OUTPUT"

      - name: Run ring deployment
        run: |
          chmod +x ./scripts/ring-deploy.sh
          ./scripts/ring-deploy.sh \
            my-app \
            rg-app-prod \
            "${{ steps.deploy.outputs.new-revision }}"

      - name: Notify on failure - auto rollback
        if: failure()
        run: |
          OLD_REVISION=$(az containerapp revision list \
            --name my-app \
            --resource-group rg-app-prod \
            --query "sort_by([?properties.active], &properties.createdTime)[-2].name" \
            -o tsv)
          az containerapp ingress traffic set \
            --name my-app \
            --resource-group rg-app-prod \
            --revision-weight "${OLD_REVISION}=100"
          echo "Rollback complete -- 100% traffic restored to ${OLD_REVISION}"
```

---

## AKS Ring Deployment with Gateway API

For AKS, use the Kubernetes Gateway API (HTTPRoute) for progressive traffic splitting. This requires the Gateway API CRDs and a compatible ingress controller (Cilium Gateway API, NGINX Gateway Fabric, or Azure Application Gateway for Containers).

```yaml
# gateway-httproute-ring.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app-ring
  namespace: my-app
spec:
  parentRefs:
    - name: aks-gateway
      namespace: gateway-system
  hostnames:
    - my-app.example.com
  rules:
    - backendRefs:
        - name: my-app-stable    # Current stable Service
          port: 8080
          weight: 99
        - name: my-app-canary    # New revision Service
          port: 8080
          weight: 1
```

Progress rings by patching the HTTPRoute weights. With GitOps, update the manifest in the config repo and let Flux reconcile.

```bash
# Patch via kubectl (direct; not recommended for GitOps -- prefer config repo commit)
kubectl patch httproute my-app-ring \
  --namespace my-app \
  --type=json \
  --patch='[
    {"op": "replace", "path": "/spec/rules/0/backendRefs/0/weight", "value": 90},
    {"op": "replace", "path": "/spec/rules/0/backendRefs/1/weight", "value": 10}
  ]'
```

---

## Health Gate Implementation

The health gate queries Azure Monitor / Application Insights for error rate and latency metrics. This is the automation that makes rings safe.

```bash
# health-gate.sh -- checks error rate and p99 latency against baseline
# Requires az CLI with monitor extension and Application Insights workspace

APP_INSIGHTS_ID="/subscriptions/<sub>/resourceGroups/rg-app/providers/microsoft.insights/components/ai-my-app"
WINDOW_MINUTES=5
MAX_ERROR_RATE=0.5   # percent
MAX_P99_LATENCY=2000 # milliseconds

check_error_rate() {
  ERROR_RATE=$(az monitor metrics list \
    --resource "$APP_INSIGHTS_ID" \
    --metric "requests/failed" \
    --interval PT${WINDOW_MINUTES}M \
    --aggregation Average \
    --query "value[0].timeseries[0].data[-1].average" \
    -o tsv 2>/dev/null || echo "0")

  TOTAL=$(az monitor metrics list \
    --resource "$APP_INSIGHTS_ID" \
    --metric "requests/count" \
    --interval PT${WINDOW_MINUTES}M \
    --aggregation Total \
    --query "value[0].timeseries[0].data[-1].total" \
    -o tsv 2>/dev/null || echo "1")

  RATE=$(echo "scale=2; $ERROR_RATE / $TOTAL * 100" | bc)
  echo "Error rate: ${RATE}%"
  if (( $(echo "$RATE > $MAX_ERROR_RATE" | bc -l) )); then
    echo "ERROR: Error rate ${RATE}% exceeds threshold ${MAX_ERROR_RATE}%"
    return 1
  fi
}

check_p99_latency() {
  P99=$(az monitor metrics list \
    --resource "$APP_INSIGHTS_ID" \
    --metric "requests/duration" \
    --interval PT${WINDOW_MINUTES}M \
    --aggregation Percentile99 \
    --query "value[0].timeseries[0].data[-1].percentile99" \
    -o tsv 2>/dev/null || echo "0")

  echo "p99 latency: ${P99}ms"
  if (( $(echo "$P99 > $MAX_P99_LATENCY" | bc -l) )); then
    echo "ERROR: p99 latency ${P99}ms exceeds threshold ${MAX_P99_LATENCY}ms"
    return 1
  fi
}

check_error_rate && check_p99_latency
```

---

## Rollback Procedure

A rollback is a traffic re-weight, not a redeploy. The old revision is still active until explicitly deactivated.

```bash
# Immediate rollback -- restore 100% to previous revision
PREV_REVISION="my-app--a1b2c3d4"

az containerapp ingress traffic set \
  --name my-app \
  --resource-group rg-app-prod \
  --revision-weight "${PREV_REVISION}=100"

# Deactivate the failed new revision
az containerapp revision deactivate \
  --name my-app \
  --resource-group rg-app-prod \
  --revision "my-app--<failed-suffix>"

echo "Rollback complete"
```

Document the rollback command as a runbook in the team wiki. The on-call engineer must be able to execute it in under 2 minutes without pipeline access.
