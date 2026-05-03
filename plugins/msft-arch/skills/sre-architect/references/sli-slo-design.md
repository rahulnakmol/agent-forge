# SLI and SLO Design Reference

**Used by**: `sre-architect` Step 2  
**Related**: `observability-architect` (telemetry foundation, signal wiring)

---

## The SLI/SLO/SLA Hierarchy

```
SLI (measured)
  -> SLO (internal target set from SLI data)
    -> SLA (external commitment set below SLO)
```

Customer-facing SLAs are derived from SLOs, not invented separately. Set the SLA at a cushion below the SLO to absorb measurement error, maintenance windows, and the gap between measured availability and customer-perceived availability.

Never commit an SLA before measuring an SLI baseline. A 99.9% SLA with no SLI baseline is a guess that will be disproven in the first incident.

---

## SLI Types and Measurement Patterns

### Availability SLI

Measures: proportion of requests served successfully.

```kusto
// App Insights - availability SLI for an HTTP API
let window = 28d;
requests
| where timestamp > ago(window)
| summarize
    total = count(),
    successful = countif(resultCode startswith "2" or resultCode startswith "3")
| extend availability_sli = todouble(successful) / todouble(total)
```

Success definition varies by service type:
- HTTP APIs: 2xx and 3xx responses; exclude 4xx (client errors) from the denominator if the SLO measures server-side reliability.
- Background jobs: job completed without unhandled exception.
- Message consumers: message processed to final state (ack or dead-letter) within SLA window.

### Latency SLI

Measures: proportion of requests completing within a defined threshold.

```kusto
// App Insights - latency SLI (% of requests completing within 500ms)
let window = 28d;
let threshold_ms = 500.0;
requests
| where timestamp > ago(window)
| summarize
    total = count(),
    within_threshold = countif(duration <= threshold_ms)
| extend latency_sli = todouble(within_threshold) / todouble(total)
```

Thresholds: define per user-facing action, not per service. A payment submit can tolerate 2,000ms; an autocomplete suggestion cannot tolerate more than 100ms.

### Throughput SLI

Measures: fraction of time the system processes at or above a minimum throughput target.

Use custom OTel metrics emitted by the application. Example: `orders.processed.count` per minute vs. a committed minimum rate.

### Durability SLI

Measures: fraction of written objects that remain readable after write.

Applicable to: Blob Storage, Cosmos DB, Azure SQL. Usually very high (99.9999%) and seldom the binding constraint; include when data loss is a contractual concern.

### Correctness SLI

Measures: fraction of responses that are semantically correct.

Applicable to: data pipelines, AI inference, financial calculations. Requires custom assertion logic emitting a metric per result.

---

## SLO Target-Setting Process

1. **Collect baseline**: measure the SLI over the last 30-90 days. Use Log Analytics or App Insights. Do not set targets before measuring.
2. **Find the natural reliability level**: what is the p99.9 availability over the measurement window?
3. **Set the SLO below the natural level with a cushion**: if 30-day availability is 99.95%, set SLO at 99.9%.
4. **Validate the target is achievable**: check that the systems, deployment pipelines, and on-call processes can defend this target.
5. **Set the SLA below the SLO**: if SLO is 99.9%, the SLA is 99.5% or 99.0% depending on commercial context.

### Multi-Dependency SLO Ceiling

If a service depends on N independent components, each with an SLO, the composite availability ceiling is:

```
composite_ceiling = SLO_A * SLO_B * SLO_C * ...
e.g., 99.9% * 99.9% * 99.9% = 99.7%
```

The system SLO must not exceed this ceiling. If it does, reduce dependencies, add redundancy, or accept that the SLO is aspirational.

---

## SLO Register Template

Document each SLO in a register. Store in the repository under `docs/sre/slo-register.md`.

| Field | Value |
|---|---|
| Service | e.g., `orders-api` |
| SLI type | Availability / Latency / Throughput / Durability / Correctness |
| Description | "Proportion of HTTP POST /orders requests returning 2xx within 500ms" |
| Measurement query | KQL query (saved as Log Analytics function: `fn_sli_orders_availability`) |
| SLO target | 99.9% |
| Window | 28 days (rolling) |
| Error budget | 40.3 minutes per window |
| SLA (if committed) | 99.5% |
| Owner | Team/squad name |
| Last reviewed | Date |

---

## SLO Windows

**28-day rolling window** is the default. Advantages: consistent month-over-month comparison; aligns with most commercial SLA billing cycles.

**Calendar-month window**: easier to communicate to business stakeholders but harder to compute continuously.

**Rolling windows** are preferred for alerting: they produce a stable, continuously updated error budget rather than a budget that resets hard on the 1st of each month.

---

## Exclusion Policy

Define what is excluded from SLO measurement:

- Planned maintenance (requires advance customer notice per SLA terms).
- Force majeure: Azure regional outages beyond the team's blast radius (reference Azure Service Health).
- User-side errors: 4xx status codes where the input is provably invalid.

Document exclusions in the SLO register. Do not silently exclude incidents to hit SLO targets.

---

## Azure Monitor SLI (Preview)

Azure Monitor introduced native SLI/SLO tracking via Service Groups (preview as of 2025). Use `microsoft_docs_search "Azure Monitor SLI service level indicators"` to verify current feature status and regional availability before adopting.

When available: create SLI resources under the service group; configure baseline (SLO target), evaluation period (window), fast-burn alert, and slow-burn alert directly in Azure Monitor without managing KQL scheduled query alerts manually.

When not available or not in a supported region: implement SLO tracking via KQL scheduled query alerts (see `burn-rate-alerting.md`) and an Azure Workbook SLO dashboard.
