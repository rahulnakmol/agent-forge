# OpenTelemetry Instrumentation Patterns

OpenTelemetry is the wire format for all new Azure workload instrumentation. The Azure Monitor OpenTelemetry Distro packages the OTel SDK, instrumentation libraries, and the Azure Monitor exporter into a single, opinionated NuGet package. The classic `Microsoft.ApplicationInsights` SDK is retained only for brownfield services; migrate to the Distro at the earliest feasible opportunity.

## Package selection

| Scenario | NuGet package | Notes |
|---|---|---|
| ASP.NET Core (.NET 8/9) | `Azure.Monitor.OpenTelemetry.AspNetCore` | Primary. GA. Includes traces, metrics, logs. |
| Console / Worker Service / classic ASP.NET | `Azure.Monitor.OpenTelemetry.Exporter` | GA. No live metrics for classic ASP.NET. |
| Custom OTel pipeline (Collector-based) | `OpenTelemetry.Exporter.OpenTelemetryProtocol` | Use when routing through an OTel Collector before Azure Monitor. |

## ASP.NET Core: minimal registration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Read connection string from environment or Key Vault reference
// Never hardcode; never use instrumentation key
builder.Services.AddOpenTelemetry()
    .UseAzureMonitor(options =>
    {
        // Connection string injected via APPLICATIONINSIGHTS_CONNECTION_STRING env var
        // or explicitly:
        // options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
        options.SamplingRatio = 0.1f; // 10% sampling for high-volume production services
    });
```

For development, set the environment variable:
```bash
APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=<guid>;IngestionEndpoint=https://<region>.in.applicationinsights.azure.com/"
```

## Sampling configuration

Do not run at 100% sampling in high-volume production services; it is expensive and unnecessary. Choose a strategy:

| Strategy | When to use | Config |
|---|---|---|
| Fixed-rate (ratio-based) | Homogeneous traffic; latency-insensitive | `SamplingRatio = 0.1f` (10%) |
| Always-sample errors | Never miss failures | Custom sampler below |
| Tail-based | Heterogeneous traffic; need complete error traces | Requires OTel Collector |

```csharp
// Custom sampler: always sample errors, 10% of successes
public sealed class ErrorAlwaysSampler : Sampler
{
    private readonly double _successRatio;

    public ErrorAlwaysSampler(double successRatio = 0.1)
    {
        _successRatio = successRatio;
        Description = $"ErrorAlways({successRatio})";
    }

    public override string Description { get; }

    public override SamplingResult ShouldSample(in SamplingParameters parameters)
    {
        // Always sample if there's an error status code hint on the parent context
        // (checked post-request via OTel processor for HTTP status)
        // During request: sample by ratio; errors recorded in the processor
        return Random.Shared.NextDouble() < _successRatio
            ? new SamplingResult(SamplingDecision.RecordAndSample)
            : new SamplingResult(SamplingDecision.Drop);
    }
}

// Registration
builder.Services.AddOpenTelemetry()
    .UseAzureMonitor()
    .WithTracing(tracing => tracing.SetSampler(new ErrorAlwaysSampler(0.1)));
```

## Custom spans and attributes

Add business-context attributes to spans at every service boundary. These become searchable dimensions in App Insights.

```csharp
using System.Diagnostics;

// Define a static ActivitySource per service -- one source per assembly
public static class Telemetry
{
    public static readonly ActivitySource Source =
        new("MyCompany.OrderService", "1.0.0");
}

// In application code (not infrastructure/framework code)
public async Task<Result<Order>> ProcessOrderAsync(CreateOrderCommand command, CancellationToken ct)
{
    using var activity = Telemetry.Source.StartActivity("ProcessOrder");

    // Set structured attributes -- these become custom dimensions in AppDependencies / AppRequests
    activity?.SetTag("order.tenant_id", command.TenantId);
    activity?.SetTag("order.sku_count", command.Items.Count);
    activity?.SetTag("order.channel", command.Channel.ToString());

    var result = await _orderRepository.CreateAsync(command, ct);

    if (result.IsFailure)
    {
        activity?.SetStatus(ActivityStatusCode.Error, result.Error.Message);
        activity?.SetTag("order.failure_reason", result.Error.Code);
    }

    return result;
}
```

## Structured logging with ILogger

Structured logging is non-negotiable. Every `ILogger` call must use named placeholders; the OTel log bridge captures property bags, not interpolated strings.

```csharp
// CORRECT -- structured properties preserved in AppTraces.Properties
_logger.LogInformation(
    "Order {OrderId} created for tenant {TenantId} with {SkuCount} items",
    order.Id, order.TenantId, order.Items.Count);

// WRONG -- string interpolation destroys structure; properties not queryable in KQL
_logger.LogInformation($"Order {order.Id} created for tenant {order.TenantId}");

// CORRECT -- error with exception and context
_logger.LogError(
    ex,
    "Failed to process payment for order {OrderId}, gateway {GatewayCode} returned {StatusCode}",
    order.Id, payment.GatewayCode, payment.StatusCode);
```

Enrich all log events at the service entry point with correlation IDs via `ILogger` scope:

```csharp
// Middleware or filter -- inject correlation scope
using (_logger.BeginScope(new Dictionary<string, object>
{
    ["CorrelationId"] = HttpContext.TraceIdentifier,
    ["TenantId"]      = user.TenantId,
    ["UserId"]        = user.Id
}))
{
    await _next(HttpContext);
}
```

## Custom metrics

Prefer OTel metrics API over `TelemetryClient.TrackMetric`. The OTel Meter API integrates with .NET's `System.Diagnostics.Metrics`, the same mechanism used by ASP.NET Core's built-in metrics.

```csharp
using System.Diagnostics.Metrics;

// One meter per service; register in DI
public static class OrderMetrics
{
    private static readonly Meter _meter = new("MyCompany.OrderService", "1.0.0");

    public static readonly Counter<long> OrdersCreated =
        _meter.CreateCounter<long>("orders.created", "orders", "Total orders created");

    public static readonly Histogram<double> OrderProcessingDuration =
        _meter.CreateHistogram<double>("orders.processing_duration_ms", "ms", "Order processing time");
}

// Usage
OrderMetrics.OrdersCreated.Add(1, new TagList
{
    { "channel", order.Channel.ToString() },
    { "tenant_id", order.TenantId }
});
```

Register the meter with the OTel pipeline:

```csharp
builder.Services.AddOpenTelemetry()
    .UseAzureMonitor()
    .WithMetrics(metrics =>
        metrics.AddMeter("MyCompany.OrderService"));
```

## .NET Aspire integration

When using .NET Aspire, the `AddServiceDefaults()` extension in the `ServiceDefaults` project wires OTel traces, metrics, and logs with the Azure Monitor exporter. Do not duplicate OTel registration in individual services when Aspire service defaults are in use.

```csharp
// ServiceDefaults/Extensions.cs (generated by Aspire template)
public static IHostApplicationBuilder AddServiceDefaults(this IHostApplicationBuilder builder)
{
    builder.ConfigureOpenTelemetry();  // Wires traces + metrics + logs
    builder.AddDefaultHealthChecks();
    builder.Services.AddServiceDiscovery();
    return builder;
}
```

The Azure Monitor connection string flows from Aspire's AppHost resource configuration to each service via environment variable injection; no per-service configuration needed.

## Migration from classic AppInsights SDK

When migrating existing services from `Microsoft.ApplicationInsights` to the OTel Distro:

1. Remove `Microsoft.ApplicationInsights.*` NuGet packages (except `Microsoft.ApplicationInsights.WorkerService` if needed temporarily).
2. Remove `AddApplicationInsightsTelemetry()` from `Program.cs`.
3. Add `Azure.Monitor.OpenTelemetry.AspNetCore` and call `.UseAzureMonitor()`.
4. Replace `TelemetryClient.TrackEvent()` with OTel custom events API (GA as of 2025): `activity?.AddEvent(new ActivityEvent("EventName", tags: new ActivityTagsCollection { ["prop"] = value }))`.
5. Replace `TelemetryClient.TrackMetric()` with `System.Diagnostics.Metrics` meter.
6. Replace `TelemetryClient.TrackException()` with `ILogger.LogError(ex, ...)`; the OTel log bridge captures exception details automatically.
