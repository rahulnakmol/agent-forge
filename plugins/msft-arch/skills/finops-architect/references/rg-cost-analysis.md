# Resource Group Cost Analysis

Resource groups are the primary unit of cost governance in Azure. They map naturally to applications, teams, and environments. This file covers how to structure resource group boundaries for cost visibility, how to query cost data at RG scope via API and KQL, and how to build the right-sizing playbook.

---

## Resource Group Design for Cost Visibility

### Principle: one resource group per workload per environment

```text
orders-platform-prod-rg        ← production workload
orders-platform-staging-rg     ← staging workload
orders-platform-dev-rg         ← development workload
shared-infra-prod-rg           ← shared services (Log Analytics, APIM, hub VNet)
platform-security-prod-rg      ← security resources (Key Vault, Defender workspace)
```

Why this matters for FinOps:
- Cost Management can scope to a resource group; you get an exact spend figure per workload per environment.
- Budget alerts at resource group scope fire before the subscription budget is exhausted.
- Anomaly alerts surface per-resource-group deltas in the daily email.
- Tags inherit from resource group to resources via Azure Policy `modify` effect (see `references/tagging-strategy.md`).

### Anti-patterns to avoid

| Anti-pattern | FinOps Impact |
|--------------|--------------|
| One resource group for all environments | Cannot separate production cost from dev/test without tag filtering; dev costs inflate production reports |
| Mixed workloads in one resource group | Cannot attribute cost to a single team or product line |
| Resource group per Azure service type (e.g. "all-storage-rg") | Destroys workload-level cost allocation; useless for showback |
| Resources outside resource groups (classic deployment) | Cost Management cannot attribute these costs to tags |

---

## Cost Analysis via Azure Portal

Quick steps for a resource group cost breakdown:

1. **Azure portal → Resource group → Cost analysis**.
2. Set **Time range**: current month or last 30 days.
3. **Group by**: Service name → see which Azure service is the top spend driver.
4. Switch to **Tag** grouping → confirm all resources have the mandatory cost-center and owner tags.
5. **Download → CSV** → import to the weekly showback report.

---

## Cost Analysis via REST API

The Cost Management Query API supports programmatic cost queries at resource group scope. Use API version `2023-11-01` or later.

```bash
# Query actual cost for a resource group, grouped by service name, for the last 30 days
POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CostManagement/query?api-version=2023-11-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "type": "ActualCost",
  "timeframe": "MonthToDate",
  "dataset": {
    "granularity": "Daily",
    "grouping": [
      { "type": "Dimension", "name": "ServiceName" }
    ],
    "aggregation": {
      "totalCost": {
        "name": "PreTaxCost",
        "function": "Sum"
      }
    }
  }
}
```

```bash
# Query amortised cost (for RI/Savings Plan chargeback) for last month, grouped by resource
POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CostManagement/query?api-version=2023-11-01

{
  "type": "AmortizedCost",
  "timeframe": "LastMonth",
  "dataset": {
    "granularity": "Monthly",
    "grouping": [
      { "type": "Dimension", "name": "ResourceId" },
      { "type": "Dimension", "name": "ResourceType" }
    ],
    "aggregation": {
      "totalCost": {
        "name": "PreTaxCost",
        "function": "Sum"
      }
    }
  }
}
```

```python
# Python -- Cost Management Query API with Azure SDK
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryGrouping, QueryAggregation

credential = DefaultAzureCredential()
client = CostManagementClient(credential)

scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}"

result = client.query.usage(
    scope=scope,
    parameters=QueryDefinition(
        type="ActualCost",
        timeframe="MonthToDate",
        dataset=QueryDataset(
            granularity="Daily",
            grouping=[QueryGrouping(type="Dimension", name="ServiceName")],
            aggregation={"totalCost": QueryAggregation(name="PreTaxCost", function="Sum")}
        )
    )
)

for row in result.rows:
    print(f"Date: {row[1]}, Service: {row[2]}, Cost: ${row[0]:.2f}")
```

---

## Right-Sizing Playbook

**Rule: right-size from day 1. Hot-swap SKUs after 30-day baseline if over-provisioned.** Never right-size before a baseline; you need P95 consumption data before downsizing a production resource.

### Step 1: Establish the 30-day baseline

```bash
# Pull P95 CPU and memory for all VMs in a resource group (Azure Monitor Metrics API)
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{vmName}/providers/microsoft.insights/metrics?api-version=2019-07-01&metricnames=Percentage%20CPU,Available%20Memory%20Bytes&timespan=P30D&interval=P1D&aggregation=Maximum,Percentile&percentile=95
```

Collect P95 CPU utilisation and P95 memory utilisation for 30 days. Record results in the right-sizing worksheet.

### Step 2: Apply the right-sizing decision rules

```text
P95 CPU < 20% AND P95 Memory < 40% → severely over-provisioned → downsize 2 tiers
P95 CPU < 40% AND P95 Memory < 60% → over-provisioned → downsize 1 tier
P95 CPU 40–70% AND P95 Memory 40–70% → correctly provisioned → no change
P95 CPU > 70% OR P95 Memory > 70% → correctly provisioned or under-provisioned → do not downsize
P95 CPU > 85% OR P95 Memory > 85% → under-provisioned → upsize (and review autoscale)
```

### Step 3: Azure Advisor cross-reference

Azure Advisor Cost recommendations run their own right-sizing model. Cross-reference Advisor suggestions with your P95 baseline. If Advisor recommends a downsize but your P95 is above 70%, investigate; Advisor may use a 7-day or 14-day window that misses your peak.

```bash
# List Advisor cost recommendations for a resource group
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Advisor/recommendations?api-version=2023-01-01&$filter=Category eq 'Cost'
```

### Step 4: Estimate the saving

```text
Current SKU:     Standard_D8s_v5   →  8 vCPU, 32 GiB  →  ~$0.384/hr PAYG
Recommended SKU: Standard_D4s_v5   →  4 vCPU, 16 GiB  →  ~$0.192/hr PAYG
Monthly saving:  ($0.384 - $0.192) × 730 hrs = ~$140/month per VM
```

Document the saving in the right-sizing register (CSV, one row per resource).

```csv
ResourceId,CurrentSKU,RecommendedSKU,P95CPU,P95MemGB,EstimatedMonthlySavingUSD,ReviewDate,Status
/subscriptions/.../vms/app-vm-01,Standard_D8s_v5,Standard_D4s_v5,18%,28%,140,2025-06-01,Pending
/subscriptions/.../vms/db-vm-01,Standard_E8s_v5,Standard_E4s_v5,22%,35%,165,2025-06-01,Pending
```

### Step 5: Hot-swap the SKU (Azure Compute)

For VMs, resize requires a deallocation (brief downtime). For App Service Plans, resize is online.

```bash
# Resize a VM (requires deallocation first for cross-family resize)
az vm deallocate --resource-group {rg} --name {vmName}
az vm resize --resource-group {rg} --name {vmName} --size Standard_D4s_v5
az vm start --resource-group {rg} --name {vmName}

# Resize an App Service Plan (online, no downtime)
az appservice plan update --resource-group {rg} --name {planName} --sku P1V3
```

Schedule resizes during the maintenance window. Validate P95 metrics again 7 days post-resize.

---

## KQL: Top Spend by Resource Group (Log Analytics + Cost Export)

```kql
// Top 10 resource groups by spend in the last 30 days
CostExport
| where TimeGenerated > ago(30d)
| summarize total_cost = sum(PreTaxCost) by ResourceGroupName
| top 10 by total_cost desc
| project ResourceGroupName, total_cost = round(total_cost, 2)
```

```kql
// Cost trend by resource group -- week over week
let this_week = CostExport | where TimeGenerated >= ago(7d) | summarize this_week = sum(PreTaxCost) by ResourceGroupName;
let last_week = CostExport | where TimeGenerated >= ago(14d) and TimeGenerated < ago(7d) | summarize last_week = sum(PreTaxCost) by ResourceGroupName;

this_week
| join kind=leftouter last_week on ResourceGroupName
| extend
    last_week = coalesce(last_week, 0.0),
    wow_pct   = iff(last_week > 0, 100.0 * (this_week - last_week) / last_week, 100.0)
| project ResourceGroupName, this_week = round(this_week,2), last_week = round(last_week,2), wow_pct = round(wow_pct,1)
| order by wow_pct desc
```

---

## Budget Alerts at Resource Group Scope

Set budget alerts at resource group scope for high-spend workloads. This provides a safety net before the subscription-level budget is exhausted.

```bash
# Create a resource group budget via Azure CLI
az consumption budget create \
  --budget-name "orders-platform-prod-monthly" \
  --resource-group "orders-platform-prod-rg" \
  --category Cost \
  --amount 5000 \
  --time-grain Monthly \
  --start-date "2025-06-01" \
  --end-date "2026-05-31" \
  --threshold 90 \
  --contact-emails "finops-team@contoso.com" "platform-team@contoso.com"
```

Set thresholds at:
- 90% actual: early warning; review spend.
- 100% actual: budget exhausted; escalate.
- 110% forecast: projected to overspend; take action before month-end.

---

## Carbon Optimization Integration

As of 2025, the Azure Carbon Optimization service (GA, `api-version=2025-04-01`) provides per-resource-group emissions data. Include carbon metrics alongside cost in the resource group analysis when sustainability reporting is in scope.

```bash
# Query carbon emissions by resource group (requires Carbon Optimization Reader role)
POST https://management.azure.com/providers/Microsoft.Carbon/carbonEmissionReports?api-version=2025-04-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "reportType": "ItemDetailsReport",
  "subscriptionList": ["{subscriptionId}"],
  "dateRange": {
    "start": "2025-04-01",
    "end": "2025-04-30"
  },
  "categoryType": "ResourceGroup"
}
```

Carbon data is updated monthly; previous month's data is available by day 19 of the current month. Do not poll daily; schedule the report pull monthly.
