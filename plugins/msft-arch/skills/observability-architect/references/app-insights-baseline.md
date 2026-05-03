# App Insights + Log Analytics Baseline Design

Every Azure workload ships with an App Insights resource backed by a workspace-based Log Analytics workspace. Classic (non-workspace-based) App Insights resources are retired; create only workspace-based resources. The App Insights resource and its backing workspace must reside in the same Azure region; cross-region placement doubles the blast radius for a regional failure.

## Resource topology

**Rule**: one App Insights resource per workload per environment. Never share a single App Insights resource across dev / staging / prod; environment-mixed telemetry makes sampling, alert thresholds, and data retention impossible to tune correctly.

**Rule**: one Log Analytics workspace per environment boundary. Production workspaces are isolated from non-production. A centralised "platform" workspace is acceptable only when a dedicated platform team manages it and workload teams have table-level RBAC (not full workspace access).

```text
Production environment
  ├── law-<workload>-prod       (Log Analytics workspace, sku: PerGB2018)
  │     ├── app-<svc-a>-prod   (App Insights → same workspace)
  │     └── app-<svc-b>-prod   (App Insights → same workspace)
  └── Diagnostic settings (all Azure resources) → law-<workload>-prod

Staging environment
  └── law-<workload>-stg        (separate workspace; same pattern)

Dev environment
  └── law-<workload>-dev        (separate workspace)
```

Multi-region production: replicate the pattern per region. Use cross-workspace KQL queries (`workspace("law-<workload>-prod-eastus")`) for global operational views rather than merging into a single workspace.

## Workspace SKU and retention

| Setting | Recommendation |
|---|---|
| Pricing tier | PerGB2018 (pay-as-you-go) until daily ingest > 100 GB/day; then evaluate commitment tiers (100 / 200 / 300 / 400 / 500 GB/day) |
| Interactive retention | 90 days minimum (App Insights default is 90 days; Log Analytics default is 31, **explicitly set to 90**) |
| Long-term archive | Up to 12 years via archive tier; configure for PCI-DSS / ISO 27001 workloads |
| Daily cap | Set on dev/staging workspaces to prevent runaway ingestion; do not set on production (cap stops all ingestion) |
| Table plan: Analytics Logs | Default; full KQL + alerting support |
| Table plan: Basic Logs | Use for high-volume, low-query-frequency tables (e.g., `ContainerLog`, verbose `AppTraces` below Warning); ~8x cheaper ingestion but limited query capability and no alerting |

## Diagnostic settings: required for every Azure resource

Every resource in the subscription sends diagnostic logs and metrics to the production Log Analytics workspace. Enforce via Azure Policy (`Deploy-Diagnostics-*` built-in initiative or AVM policy modules).

```hcl
resource "azurerm_monitor_diagnostic_setting" "example" {
  name                       = "diag-${var.resource_name}"
  target_resource_id         = azurerm_app_service.example.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.prod.id

  enabled_log {
    category = "AppServiceHTTPLogs"
  }
  enabled_log {
    category = "AppServiceConsoleLogs"
  }
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
```

## App Insights: connection string over instrumentation key

Instrumentation keys are deprecated. Use the connection string exclusively. Store in Key Vault; inject via Key Vault reference or environment variable. Never hardcode it.

```text
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=<guid>;IngestionEndpoint=...
```

With Managed Identity and the OTel Distro, the connection string is still required but no secret key is transmitted; the Distro authenticates the telemetry channel via AAD token when configured. Connection string is not a secret in the traditional sense but should not appear in source control.

## App Insights sampling

Adaptive sampling is on by default in the classic SDK. With the OTel Distro, configure a fixed-rate or tail-based sampler explicitly; do not rely on defaults for high-volume production services.

```csharp
// In Program.cs -- fixed-rate sampler at 10% for high-volume services
builder.Services.AddOpenTelemetry()
    .UseAzureMonitor()
    .WithTracing(tracing =>
        tracing.SetSampler(new TraceIdRatioBasedSampler(0.1)));
```

Tail-based sampling (e.g., always sample errors, sample 5% of 200-OK requests) requires an OTel Collector in the path; see `distributed-tracing.md`.

## Health checks and availability tests

- **Standard availability tests** (HTTP ping, 5 locations, 1-minute frequency) for every public-facing endpoint.
- **Multi-step availability tests** for critical user journeys (login → checkout flow).
- Set alert: `availabilityResults | where success == false` firing after 3 consecutive failures from 2+ locations.

## Workspace RBAC

| Role | Scope | Assigned to |
|---|---|---|
| Log Analytics Reader | Workspace | Developers, SRE on-call |
| Log Analytics Contributor | Workspace | CI/CD service principal (for saved queries and Workbook deployment) |
| Monitoring Reader | Subscription | observability dashboards, Grafana managed identity |
| Monitoring Contributor | Resource group | IaC service principal |

Never grant workspace Owner to application Managed Identities. Restrict `Log Analytics Contributor` to service principals that genuinely need to create/modify saved queries.
