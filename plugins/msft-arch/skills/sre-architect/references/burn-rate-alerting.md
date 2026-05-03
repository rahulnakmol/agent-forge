# Burn-Rate Alerting Reference

**Used by**: `sre-architect` Step 4  
**Related**: `sli-slo-design.md`, `error-budgets.md`  
**Source methodology**: Google SRE Workbook, Chapter 5 (Alerting on SLOs)

---

## Principle

Alert on burn rate, not raw metric thresholds. A 1% error rate on a 99.9% SLO is a problem only if it persists; a 5% error rate for 2 minutes may be within budget. Burn-rate alerting surfaces the relationship between current error rate and error budget consumption speed.

**Burn rate** = (current error rate) / (1 - SLO target)

A burn rate of 1.0 means the budget is consumed at exactly the rate that exhausts it over the full window. A burn rate of 14.0 means the budget will exhaust in 2 days (1/14 of 28 days).

---

## Multi-Window Multi-Burn-Rate Configuration

Configure two alert windows per SLO. Both must fire to reduce noise (use AND logic: both windows exceeded). This is the Google SRE Workbook approach.

| Alert | Window | Burn multiplier | Interpretation | Severity | Action |
|---|---|---|---|---|---|
| Fast-burn | 1 hour | 14x | Budget exhausts in ~2 days | Critical | Page on-call immediately |
| Fast-burn confirm | 5 minutes | 14x | Short window confirms it is not a transient spike | Critical | AND with above |
| Slow-burn | 6 hours | 5x | Budget exhausts in ~5.6 days | Warning | Create ticket |
| Slow-burn confirm | 30 minutes | 5x | Sustained, not a blip | Warning | AND with above |

**Why two windows per alert level:** a single long-window alert misses sudden regressions. A single short-window alert fires on transient spikes that resolve within minutes. The AND of short + long filters both failure modes.

---

## Burn-Rate Thresholds by SLO Target

| SLO target | Error budget (28d) | Fast-burn threshold (14x exhausts in) | Slow-burn threshold (5x exhausts in) |
|---|---|---|---|
| 99.0% | 6h 43m | 28.8h | 80.6h |
| 99.5% | 3h 22m | 14.4h | 40.3h |
| 99.9% | 40.3 min | 2.9h (see note) | 8.1h |
| 99.95% | 20.2 min | 1.4h | 4.0h |
| 99.99% | 4.0 min | 17.1 min | 48 min |

Note: for high-SLO targets (99.99%), a 5-minute fast-burn window may already be longer than the budget. Adjust the fast-burn multiplier and windows to ensure the short window is always shorter than `error_budget / burn_multiplier`.

---

## KQL Implementation (Azure Monitor Scheduled Query Alert)

### Fast-Burn Alert (Availability SLO, 99.9%)

Save as a Log Analytics scheduled query alert with:
- Evaluation frequency: 1 minute
- Window size: 1 hour
- Threshold: count > 0 (the query returns a row only when burn rate exceeds threshold)

```kusto
let slo_target = 0.999;
let fast_burn_multiplier = 14.0;
let window_size = 1h;
requests
| where timestamp > ago(window_size)
| summarize
    total = count(),
    failed = countif(success == false)
| extend
    error_rate = iff(total > 0, todouble(failed) / todouble(total), 0.0),
    budget_rate = 1.0 - slo_target,
    burn_rate = iff(total > 0, (todouble(failed) / todouble(total)) / (1.0 - slo_target), 0.0)
| where burn_rate > fast_burn_multiplier and total > 100
// Minimum sample size (total > 100) prevents false positives during low-traffic periods
```

### Slow-Burn Alert (Availability SLO, 99.9%)

Save as a Log Analytics scheduled query alert with:
- Evaluation frequency: 5 minutes
- Window size: 6 hours
- Threshold: count > 0

```kusto
let slo_target = 0.999;
let slow_burn_multiplier = 5.0;
let window_size = 6h;
requests
| where timestamp > ago(window_size)
| summarize
    total = count(),
    failed = countif(success == false)
| extend
    burn_rate = iff(total > 0, (todouble(failed) / todouble(total)) / (1.0 - slo_target), 0.0)
| where burn_rate > slow_burn_multiplier and total > 500
```

### Latency SLI Burn-Rate Alert

For a latency SLI (% of requests completing within 500ms), the "error" is a request exceeding the threshold.

```kusto
let slo_target = 0.999;
let latency_threshold_ms = 500.0;
let fast_burn_multiplier = 14.0;
let window_size = 1h;
requests
| where timestamp > ago(window_size)
| summarize
    total = count(),
    slow = countif(duration > latency_threshold_ms)
| extend
    burn_rate = iff(total > 0, (todouble(slow) / todouble(total)) / (1.0 - slo_target), 0.0)
| where burn_rate > fast_burn_multiplier and total > 100
```

---

## Azure Monitor SLI (Preview) Burn-Rate Alerts

Azure Monitor's native SLI feature (preview) supports fast-burn and slow-burn alert configuration in the portal:

1. Create an SLI resource in the Azure Monitor service group.
2. Set the baseline target (SLO %).
3. Enable "Fast burn rate" alert: configure lookback period (1 hour) and burn-rate multiplier (14).
4. Enable "Slow burn rate" alert: configure lookback period (6 hours) and multiplier (5 or 2).
5. Attach action groups to each alert severity.

Use `microsoft_docs_search "Azure Monitor SLI service level indicators baseline alert"` to verify current feature status and exact configuration steps before implementing.

---

## Action Group Configuration

**Critical (fast-burn):**
- Notification: Azure Monitor action group with Teams webhook (immediate channel notification).
- On-call page: PagerDuty or Opsgenie integration (webhook action type). Set severity = P1.
- Auto-ticket: create work item in Azure DevOps or GitHub Issue via Logic App webhook.

**Warning (slow-burn):**
- Notification: Teams webhook (channel only, no page).
- Auto-ticket: create work item directly. No on-call page.

Never configure email-only action groups for critical alerts. Email is not a reliable paging channel.

---

## Alert Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Threshold alert on raw error count | Fires on any error; ignores traffic volume | Alert on error rate, not count |
| Single-window burn-rate alert | Too many false positives (transient spikes) | Use AND of two windows (short + long) |
| Alerting on infrastructure metrics only (CPU, memory) | Does not measure customer impact | Alert on SLI-derived burn rate |
| No minimum sample size | Alert fires during quiet hours with 1/5 requests failing | Add `total > N` guard clause |
| Alert fires but has no runbook | On-call doesn't know what to do | Every alert rule links to a runbook |
| Slow-burn alert pages on-call | Creates alert fatigue; slow-burn is not urgent | Slow-burn creates a ticket; does not page |

---

## Terraform: Azure Monitor Scheduled Query Alert

```hcl
resource "azurerm_monitor_scheduled_query_rules_alert_v2" "slo_fast_burn" {
  name                = "slo-fast-burn-orders-api"
  resource_group_name = var.resource_group_name
  location            = var.location

  evaluation_frequency = "PT1M"
  window_duration      = "PT1H"
  scopes               = [var.log_analytics_workspace_id]
  severity             = 1 # Critical

  criteria {
    query                   = file("${path.module}/queries/fast-burn-orders.kql")
    time_aggregation_method = "Count"
    threshold               = 0
    operator                = "GreaterThan"
  }

  action {
    action_groups = [azurerm_monitor_action_group.oncall_critical.id]
  }
}
```

All alert rules in IaC. No manually created alert rules in production.
