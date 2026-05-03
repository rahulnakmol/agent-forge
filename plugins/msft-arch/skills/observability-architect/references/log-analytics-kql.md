# Log Analytics KQL Patterns

KQL is the canonical query language for Azure Monitor. Save all operational and SLO queries as Log Analytics saved functions; never leave team-knowledge queries as one-off freehand KQL. Saved functions are version-controlled in Terraform (via `azurerm_log_analytics_saved_search`) or Bicep, and callable from Workbooks, alert rules, and the CLI.

## Fundamental table map

| Table | Contains |
|---|---|
| `AppRequests` | HTTP requests processed by the application (replaces `requests` in workspace-based AI) |
| `AppDependencies` | Outbound calls (HTTP, SQL, Service Bus, etc.) |
| `AppExceptions` | Unhandled + handled exceptions |
| `AppTraces` | `ILogger` output (structured properties preserved) |
| `AppEvents` | Custom events (via `TelemetryClient.TrackEvent` or OTel custom events) |
| `AppMetrics` | Custom metrics |
| `AppPageViews` | Browser page view telemetry |
| `AzureActivity` | Azure control-plane operations |
| `AzureMetrics` | Platform metrics routed via diagnostic settings |
| `ContainerLog` | Stdout/stderr from AKS containers (Basic Logs tier candidate) |
| `KubeEvents` | Kubernetes events |
| `Perf` | OS performance counters from VMs / Arc |
| `_LogOperation` | Workspace operational health |

## Saved function patterns

Save all queries below as Log Analytics functions using the naming convention `fn_<domain>_<metric>`.

### fn_svc_availability: 5-minute availability ratio per operation

```kql
// fn_svc_availability(lookback: timespan = 5m)
AppRequests
| where TimeGenerated > ago(lookback)
| summarize
    total     = count(),
    failures  = countif(Success == false)
  by bin(TimeGenerated, 1m), OperationName
| extend availability = 1.0 - (todouble(failures) / todouble(total))
| project TimeGenerated, OperationName, availability, total, failures
```

### fn_svc_p99_latency: 99th percentile latency per operation

```kql
// fn_svc_p99_latency(lookback: timespan = 1h)
AppRequests
| where TimeGenerated > ago(lookback)
| summarize p99 = percentile(DurationMs, 99)
  by bin(TimeGenerated, 5m), OperationName
| project TimeGenerated, OperationName, p99_ms = p99
```

### fn_dep_slow_calls: slow dependency calls (outlier detection)

```kql
// fn_dep_slow_calls(threshold_ms: long = 2000)
AppDependencies
| where Success == true and DurationMs > threshold_ms
| summarize count = count(), avg_ms = avg(DurationMs), p99_ms = percentile(DurationMs, 99)
  by DependencyType, Target, Name
| order by count desc
```

### fn_exception_rate: exception rate over time

```kql
// fn_exception_rate(lookback: timespan = 1h)
AppExceptions
| where TimeGenerated > ago(lookback)
| summarize exceptions = count()
  by bin(TimeGenerated, 5m), ExceptionType, OuterMessage
| order by TimeGenerated asc
```

### fn_structured_log_errors: structured log errors with all properties

```kql
// fn_structured_log_errors(lookback: timespan = 30m)
AppTraces
| where SeverityLevel >= 3  // Warning = 2, Error = 3, Critical = 4
| extend
    props = tostring(Properties),
    correlation_id = tostring(Properties.CorrelationId),
    user_id = tostring(Properties.UserId),
    operation = OperationName
| project TimeGenerated, SeverityLevel, Message, operation, correlation_id, user_id, props
| order by TimeGenerated desc
```

### fn_burn_rate: error budget burn rate calculation (1h window)

```kql
// fn_burn_rate(slo_target: real = 0.999, lookback: timespan = 1h)
let total = toscalar(AppRequests | where TimeGenerated > ago(lookback) | count);
let errors = toscalar(AppRequests | where TimeGenerated > ago(lookback) and Success == false | count);
let error_rate = errors * 1.0 / total;
let budget_fraction = 1.0 - slo_target;
let burn_rate = error_rate / budget_fraction;
print total=total, errors=errors, error_rate=error_rate, burn_rate=burn_rate
```

### fn_dependency_failures_by_target: identify problematic downstream services

```kql
// fn_dependency_failures_by_target(lookback: timespan = 1h)
AppDependencies
| where TimeGenerated > ago(lookback) and Success == false
| summarize
    failure_count = count(),
    failure_rate  = countif(Success == false) * 1.0 / count()
  by Target, DependencyType, Name
| where failure_rate > 0.01  // >1% failure rate
| order by failure_count desc
```

### fn_trace_waterfall: full distributed trace for a given operation id

```kql
// fn_trace_waterfall(op_id: string)
union AppRequests, AppDependencies, AppExceptions, AppTraces
| where OperationId == op_id
| project TimeGenerated, itemType, Name, DurationMs, Success, Message, SeverityLevel
| order by TimeGenerated asc
```

## Alert rule KQL patterns

Alert rules that target a Log Analytics log search query. Always pin the `TimeGenerated` range to the alert evaluation window.

### High error rate alert (log search alert)

```kql
AppRequests
| where TimeGenerated > ago(5m)
| summarize total = count(), errors = countif(Success == false)
| extend error_rate = todouble(errors) / todouble(total)
| where error_rate > 0.05
```

Threshold: result count > 0. Evaluation frequency: 1 min. Aggregation granularity: 5 min.

### Slow burn rate alert: 6-hour window (for SLO alerting; see slo-design.md)

```kql
let slo_target = 0.999;
let lookback = 6h;
let budget = 1.0 - slo_target;
AppRequests
| where TimeGenerated > ago(lookback)
| summarize total = count(), errors = countif(Success == false)
| extend error_rate = todouble(errors) / todouble(total)
| extend burn_rate = error_rate / budget
| where burn_rate > 2.0
```

## KQL discipline rules

- **No `*` wildcards** on table scans in saved functions or alert queries; always project to needed columns.
- **Always scope with `TimeGenerated > ago(...)`**: do not rely on the portal time picker for alert rule queries.
- **Use `let` bindings** for sub-expressions referenced more than once; avoid re-computing the same sub-query.
- **Pin decimal arithmetic** with `todouble()` or `1.0 *` before division; KQL integer division truncates.
- **Use `bin(TimeGenerated, 5m)`** for time-series summarise; align bin size with alert evaluation granularity.
- **Save to functions, not to Workbooks** for operational queries used in alerts; Workbooks call functions, not the reverse.
