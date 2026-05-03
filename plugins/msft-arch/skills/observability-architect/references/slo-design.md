# SLO Design and Burn-Rate Alerting

SLO-driven alerting is the only acceptable alerting strategy for user-facing services. Raw threshold alerts (e.g., "error rate > 5%") fire at the wrong time; they miss slow-burn budget exhaustion and produce alert fatigue during transient spikes. Alert on error budget burn rate instead.

## Terminology

| Term | Definition |
|---|---|
| SLI (Service Level Indicator) | The measured quantity: e.g., ratio of successful HTTP requests over total requests |
| SLO (Service Level Objective) | The target: e.g., 99.9% availability over a 30-day rolling window |
| Error budget | 100% − SLO target = the allowed failure budget. For 99.9%, the monthly budget is 0.1% × 43,800 min = 43.8 minutes of downtime. |
| Burn rate | The rate at which the error budget is being consumed relative to the allowed rate. Burn rate of 1.0 = consuming budget at exactly the rate that exhausts it at window end. Burn rate of 14 = exhausting in 1/14th of the window. |

## Defining SLOs

Define at least one SLO per user-facing service. A valid SLO requires:

1. **SLI**: expressed as a KQL query over `AppRequests` or a Prometheus metric.
2. **Target**: expressed as a percentage with two decimal places (e.g., 99.90%).
3. **Window**: rolling 30 days (standard); can be 28 days for calendar-aligned reporting.
4. **Exclusions**: planned maintenance windows excluded by tag or time filter.

### SLO template

```yaml
slo:
  name: order-service-availability
  description: "99.9% of HTTP requests to the Order Service return a 2xx or 3xx response"
  sli:
    type: request_based
    kql: |
      AppRequests
      | where AppRoleName == "order-service"
      | summarize
          good  = countif(ResultCode startswith "2" or ResultCode startswith "3"),
          total = count()
  target_percent: 99.9
  window_days: 30
  alerting:
    fast_burn:
      burn_rate_threshold: 14
      window: 1h
      severity: 0  # Critical
    slow_burn:
      burn_rate_threshold: 2
      window: 6h
      severity: 1  # Error
```

## Burn-rate alerting: the Google SRE Workbook formula

The canonical approach from the Google SRE Workbook (Chapter 5: Alerting on SLOs) defines multi-window, multi-burn-rate alerts. These two alert pairs provide both immediacy and sustained-signal properties:

### Error budget consumed

```text
Error budget per window = (1 - SLO target) × window_minutes
Example (99.9% / 30 days): 0.001 × 43,200 = 43.2 minutes
```

### Burn rate formula

```text
burn_rate = (observed_error_rate) / (1 - SLO_target)

At burn_rate = 1: budget exhausted exactly at window end (acceptable)
At burn_rate = 14: budget exhausted in ~51 hours (alert: fast burn over 1h)
At burn_rate = 6: budget exhausted in ~5 days (alert: medium burn over 6h)
At burn_rate = 2: budget exhausted in ~15 days (alert: slow burn over 6h)
```

### Two-window pair definitions

| Alert | Burn rate threshold | Short window | Long window | Budget consumed before alert | Use case |
|---|---|---|---|---|---|
| Page (fast burn) | 14× | 1 h | 5 min | 2% in 1 h | Severe outage; page immediately |
| Page (medium burn) | 6× | 6 h | 30 min | 5% in 6 h | Significant degradation |
| Ticket (slow burn) | 2× | 24 h | n/a | 10% in 24 h | Gradual degradation needing attention |
| No alert | 1× | n/a | n/a | 100% at window end | Normal consumption |

The two-window condition (both short AND long window must exceed the threshold) reduces false positives from transient spikes. Azure Monitor's native SLI feature (preview) wires fast-burn and slow-burn natively; use it when available. For production-grade custom control, implement as paired log search alert rules.

## KQL burn-rate alert query (fast burn, 1-hour window)

```kql
let slo_target   = 0.999;
let lookback     = 1h;
let burn_rate_threshold = 14.0;

let budget_fraction = 1.0 - slo_target;
let window_data = AppRequests
    | where TimeGenerated > ago(lookback)
    | summarize
        good  = countif(Success == true),
        total = count();

window_data
| extend error_rate = 1.0 - todouble(good) / todouble(total)
| extend burn_rate  = error_rate / budget_fraction
| where burn_rate > burn_rate_threshold
| project burn_rate, error_rate, good, total
```

Pair with a 5-minute short window:

```kql
let slo_target   = 0.999;
let lookback     = 5m;
let burn_rate_threshold = 14.0;
let budget_fraction = 1.0 - slo_target;

AppRequests
| where TimeGenerated > ago(lookback)
| summarize good = countif(Success == true), total = count()
| extend burn_rate = (1.0 - todouble(good)/todouble(total)) / budget_fraction
| where burn_rate > burn_rate_threshold
```

Fire the page alert only when BOTH queries return a result (AND condition). Configure via two alert rules sharing the same action group; use alert correlation / alert processing rules to suppress noise when only the short-window fires.

## Azure Monitor alert rule: Terraform definition

```hcl
resource "azurerm_monitor_scheduled_query_rules_alert_v2" "fast_burn" {
  name                = "slo-${var.service_name}-fast-burn"
  resource_group_name = var.resource_group_name
  location            = var.location
  scopes              = [azurerm_application_insights.main.id]
  description         = "SLO fast burn: ${var.service_name} error budget consuming at >14x rate"
  severity            = 0  # Critical
  evaluation_frequency = "PT1M"
  window_duration      = "PT1H"
  enabled              = true

  criteria {
    query = <<-KQL
      let slo_target = 0.999;
      let budget_fraction = 1.0 - slo_target;
      AppRequests
      | where TimeGenerated > ago(1h)
      | summarize good = countif(Success == true), total = count()
      | extend burn_rate = (1.0 - todouble(good)/todouble(total)) / budget_fraction
      | where burn_rate > 14.0
    KQL

    time_aggregation_method = "Count"
    threshold               = 0
    operator                = "GreaterThan"

    failing_periods {
      minimum_failing_periods_to_trigger_alert = 1
      number_of_evaluation_periods             = 1
    }
  }

  action {
    action_groups = [azurerm_monitor_action_group.critical.id]
  }
}
```

## SLO for latency (percentile-based)

Not all SLOs are availability-based. Define latency SLOs using percentile targets:

```yaml
slo:
  name: order-service-p99-latency
  description: "99th percentile latency for POST /orders is under 500ms"
  sli:
    type: latency
    kql: |
      AppRequests
      | where AppRoleName == "order-service" and Name == "POST /orders"
      | summarize p99 = percentile(DurationMs, 99)
  target: 500  # ms
  window_days: 30
```

Latency SLO alerting: burn rate is less intuitive for latency. Use a threshold alert on `percentile(DurationMs, 99) > 500` with a 15-minute aggregation window as an approximation, combined with a trend alert when p99 exceeds 300ms for 30+ minutes (early warning).

## Error budget reporting

Publish an error budget report monthly (or weekly for critical services). Report format:

```text
Service: order-service
Period: 2026-04 (30 days)
SLO: 99.9% availability
Budget: 43.2 minutes
Consumed: 12.1 minutes (28.0%)
Remaining: 31.1 minutes (72.0%)
Status: ON TRACK

Top contributors to budget consumption:
1. 2026-04-07 14:22: DB connection pool exhaustion, 6.3 min
2. 2026-04-19 09:41: Downstream payment gateway timeout, 3.8 min
3. Baseline error rate: 2.0 min
```
