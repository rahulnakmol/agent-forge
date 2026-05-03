Score the output 1-5 on each criterion. Return the AVERAGE.

1. **OpenTelemetry as Wire Format** — Recommends Azure Monitor OpenTelemetry Distro (Azure.Monitor.OpenTelemetry.AspNetCore) for new .NET 8/9 services. The classic Microsoft.ApplicationInsights SDK is only for legacy brownfield. Does not recommend new TelemetryClient usage for new services. Score 5 if OTel Distro is correctly recommended for new services; 1 if the classic AppInsights SDK is recommended for new .NET 8/9 work.

2. **SLO-Driven Burn Rate Alerting** — Replaces raw threshold alerts with SLO-driven burn rate alerting: fast-burn (14x, 1-hour window) and slow-burn (2x, 6-hour window). Does not use raw error rate thresholds for primary SLO alerting. Score 5 if burn rate alerting is correctly designed with both windows; 1 if threshold-based alerting is maintained.

3. **Distributed Tracing W3C Propagation** — Requires W3C TraceContext propagation at every HTTP and messaging boundary. Mandatory for any system with more than 2 services. Structured logs only (JSON with ILogger structured properties). Score 5 if W3C propagation is correctly specified across all boundaries; 1 if tracing is described without propagation standards.

4. **Workspace Topology Design** — Recommends one Log Analytics workspace per environment boundary; never mixes production and non-production telemetry. App Insights co-located in the same region as its workspace. Score 5 if workspace topology correctly separates environments; 1 if single shared workspace is recommended across all environments.

5. **Cost Management Strategies** — Addresses Log Analytics cost: Basic Logs tier for high-volume low-query tables, sampling for high-volume production services (not 100% sampling), and workspace commitment tier selection. Score 5 if ingestion cost is explicitly addressed with specific strategies; 1 if cost considerations are ignored.
