# Cost Anomaly Detection

Azure Cost Management provides built-in ML-based anomaly detection that identifies unexpected cost spikes and drops compared to your historical baseline. This file covers configuration, KQL alert templates, investigation runbooks, and the week-over-week threshold rule.

The canonical definition of the Inform → Optimize → Operate lifecycle and the FinOps Foundation anomaly management capability maturity model lives in `standards/references/operations/finops-framework.md`. This file contains the implementation patterns.

---

## Non-Negotiable Rule

**Alert on >20% week-over-week change.** This is the default alerting threshold for all engagements. A 20% WoW increase on a $10K/week baseline is a $2K surprise, large enough to investigate, small enough not to cry wolf. Tighten to 10% for production workloads with very stable cost profiles. Loosen to 30% only for dev/test environments with known bursty patterns.

---

## Azure Cost Management Anomaly Alerts

### What they detect

Azure Cost Management anomaly detection runs daily against normalized usage (not rated usage). It compares the current day's resource group costs to a rolling 60-day baseline. An anomaly is flagged when the deviation exceeds the ML model's confidence interval.

The anomaly email contains:
- Summary of resource group count and cost changes
- Top resource group cost changes for the day vs previous 60 days
- Direct link to Cost Analysis for investigation

### Configuration via Azure Portal

1. Navigate to **Azure Home → Cost Management**.
2. Select a **subscription scope** (anomaly alerts are subscription-scoped only; resource group anomalies surface within the subscription alert).
3. Left menu → **Cost alerts** → **+ Add**.
4. **Alert type**: Anomaly.
5. **Alert name**: e.g. `prod-subscription-anomaly-alert`.
6. **Recipients**: add the team's email distribution list and an Azure Monitor action group.
7. **Create**.

Limit: five anomaly alert rules per subscription. If you need more granularity, use scheduled alerts with KQL (see below).

### Configuration via Scheduled Actions API

Automate alert creation for large estates using the Scheduled Actions API. Set `kind` to `InsightAlert` and `viewId` to `/scope/providers/Microsoft.CostManagement/views/ms:DailyAnomalyByResourceGroup`.

```bash
PUT https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/scheduledActions/{alertName}?api-version=2023-11-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "kind": "InsightAlert",
  "properties": {
    "displayName": "Production Subscription Anomaly Alert",
    "viewId": "/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/views/ms:DailyAnomalyByResourceGroup",
    "schedule": {
      "frequency": "Daily",
      "hourOfDay": 8
    },
    "notification": {
      "to": ["finops-team@contoso.com", "platform-team@contoso.com"],
      "subject": "[FinOps] Cost anomaly detected: {subscriptionName}"
    },
    "status": "Enabled"
  }
}
```

---

## Week-over-Week Alert: KQL Template

The built-in anomaly detection operates at daily granularity and 60-day baseline. For week-over-week (WoW) cost change detection (the preferred metric for weekly FinOps reviews), use Cost Management exports to Log Analytics and query with KQL.

### Prerequisites

1. Configure a Cost Management export (Actual cost, daily granularity) to a Storage Account.
2. Connect the Storage Account to a Log Analytics workspace via Azure Monitor Data Collection or use the Cost Management Power BI connector.
3. Alternatively, use the `AzureDiagnostics` or `AzureCost` custom table populated via export pipeline.

### KQL: Week-over-Week Cost Change by Resource Group

```kql
// Week-over-week cost change alert -- threshold: 20%
// Table: replace CostExport with your actual Log Analytics table name
let current_week_start  = startofweek(now());
let previous_week_start = startofweek(now()) - 7d;

let current_week = CostExport
    | where TimeGenerated >= current_week_start
    | summarize current_cost = sum(PreTaxCost) by ResourceGroupName;

let previous_week = CostExport
    | where TimeGenerated >= previous_week_start and TimeGenerated < current_week_start
    | summarize previous_cost = sum(PreTaxCost) by ResourceGroupName;

current_week
| join kind=leftouter previous_week on ResourceGroupName
| extend
    previous_cost      = coalesce(previous_cost, 0.0),
    wow_change_pct     = iff(previous_cost > 0,
                             100.0 * (current_cost - previous_cost) / previous_cost,
                             100.0)
| where wow_change_pct > 20 or wow_change_pct < -20
| project
    ResourceGroupName,
    current_cost      = round(current_cost, 2),
    previous_cost     = round(previous_cost, 2),
    wow_change_pct    = round(wow_change_pct, 1)
| order by wow_change_pct desc
```

### KQL: Daily Spend Spike Detection (per service)

```kql
// Detect daily spend spikes > 2x the 14-day moving average per service
let lookback = 14d;

let baseline = CostExport
    | where TimeGenerated > ago(lookback)
    | summarize avg_daily = avg(PreTaxCost) by ServiceName, bin(TimeGenerated, 1d);

let today = CostExport
    | where TimeGenerated >= startofday(now())
    | summarize today_cost = sum(PreTaxCost) by ServiceName;

today
| join kind=inner (
    baseline | summarize avg_baseline = avg(avg_daily) by ServiceName
  ) on ServiceName
| where today_cost > 2.0 * avg_baseline
| extend spike_multiplier = round(today_cost / avg_baseline, 1)
| project ServiceName, today_cost = round(today_cost, 2), avg_baseline = round(avg_baseline, 2), spike_multiplier
| order by spike_multiplier desc
```

### KQL: Top Cost Movers (Resource Group, 7-day window)

```kql
// Top resource groups by absolute cost increase over the last 7 days
let this_week  = CostExport | where TimeGenerated >= ago(7d)  | summarize this_week_cost  = sum(PreTaxCost) by ResourceGroupName;
let last_week  = CostExport | where TimeGenerated >= ago(14d) and TimeGenerated < ago(7d) | summarize last_week_cost = sum(PreTaxCost) by ResourceGroupName;

this_week
| join kind=leftouter last_week on ResourceGroupName
| extend
    last_week_cost = coalesce(last_week_cost, 0.0),
    delta_abs      = this_week_cost - last_week_cost,
    delta_pct      = iff(last_week_cost > 0, 100.0 * (this_week_cost - last_week_cost) / last_week_cost, 100.0)
| top 10 by delta_abs desc
| project ResourceGroupName, this_week_cost = round(this_week_cost, 2), last_week_cost = round(last_week_cost, 2), delta_abs = round(delta_abs, 2), delta_pct = round(delta_pct, 1)
```

---

## Alert Routing

Route anomaly alerts to Azure Monitor action groups, not raw email, so alerts can fan out to multiple channels without reconfiguring individual alert rules.

```text
Anomaly detected
    └── Azure Monitor Action Group: "finops-alerts"
        ├── Email: finops-team@contoso.com
        ├── Teams webhook: https://contoso.webhook.office.com/...
        ├── PagerDuty (for production, business hours): webhook
        └── Azure Automation Runbook (optional): auto-tag anomaly for FinOps review queue
```

---

## Investigation Runbook

When an anomaly alert fires, follow this sequence. Total expected time to root cause: 15 minutes.

```text
Step 1: Identify the scope
  - Open Cost Analysis → Smart Views → Resources view for the flagged subscription.
  - Sort by "Change from previous period" descending.
  - Identify the top 1–3 resource groups driving the change.

Step 2: Identify the resource type
  - Drill into the resource group.
  - Group by "Resource type" to find the service generating the new charges.
  - Common culprits: Log Analytics ingestion, Virtual Machine scale-out, Azure SQL DTU burst,
    Cosmos DB RU spike, Application Gateway + WAF data processed.

Step 3: Correlate with deployments
  - Check the resource group's Activity Log for deployments in the anomaly window.
  - Check the CI/CD pipeline for releases in that window.
  - Runaway autoscale, missing throttling on an API endpoint, or a new deployment with
    verbose logging are the three most common root causes.

Step 4: Take action
  - Runaway autoscale    → add scale-in policy; add max instance cap.
  - Missing throttling   → add APIM rate limit or Azure Functions concurrency limit.
  - Verbose logging      → reduce Log Analytics table diagnostic setting verbosity;
                           move verbose tables to Basic or Auxiliary tier.
  - Unexpected resource  → verify ownership via tags; decommission if orphan.

Step 5: Tag and close
  - Tag the root cause in the anomaly alert thread (Teams / PagerDuty).
  - Record in the monthly FinOps review log: date, resource group, root cause, action taken, saving.
  - Update runbook if a new root cause pattern was discovered.
```

---

## Maturity Progression

| Maturity Level | Anomaly Detection Approach |
|----------------|---------------------------|
| Crawl | Manual weekly cost review in Cost Analysis; no automated alerts |
| Walk | Built-in Azure Cost Management anomaly alerts per subscription; routes to email |
| Run | KQL-based WoW alerts in Log Analytics; auto-notification to incident channel; automated tagging of anomaly root cause; trend compared against FinOps KPIs |

Start at Walk. Reach Run within the first quarter of a new engagement.

---

## Budget Alerts vs Anomaly Alerts

These are complementary, not alternatives. Use both.

| Alert Type | Detects | Cadence | Threshold |
|------------|---------|---------|-----------|
| Budget alert (actual) | Total spend exceeding a set amount | Daily | 90%, 100%, 110% of budget |
| Budget alert (forecast) | Projected spend on track to exceed budget | Daily | 110% of budget |
| Anomaly alert | Unexpected spike/drop vs historical baseline | Daily | ML-driven; configure at subscription scope |
| KQL WoW alert | Week-over-week percent change by resource group | Weekly | >20% WoW (adjust per environment) |

Never replace budget alerts with anomaly alerts. Budget alerts fire when you are about to overspend; anomaly alerts fire when something unexpected changes regardless of budget status.
