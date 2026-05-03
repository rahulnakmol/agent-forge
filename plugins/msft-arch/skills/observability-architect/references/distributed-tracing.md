# Distributed Tracing Design

Distributed tracing is required for any system with more than 2 services, no exceptions. Without end-to-end trace correlation, root-cause analysis during incidents becomes detective work across disconnected logs. W3C TraceContext is the mandatory propagation format; all Azure services and OTel SDKs support it natively.

## W3C TraceContext: the only propagation standard

The W3C TraceContext specification defines two HTTP headers:

| Header | Format | Purpose |
|---|---|---|
| `traceparent` | `{version}-{trace-id}-{parent-id}-{flags}` | Links requests into a single trace tree |
| `tracestate` | `key=value` pairs | Vendor-specific metadata (optional) |

Example:
```text
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

The OTel SDK propagates these headers automatically on all outbound `HttpClient` calls when the ASP.NET Core instrumentation library is registered. No application code change is required for HTTP propagation.

## Propagation across Azure messaging services

HTTP propagation is automatic. Messaging propagation requires explicit code.

### Azure Service Bus

```csharp
// Sender -- inject traceparent into message properties
using System.Diagnostics;

var message = new ServiceBusMessage(Encoding.UTF8.GetBytes(payload));

// Propagate current span context into the message application properties
var activity = Activity.Current;
if (activity is not null)
{
    message.ApplicationProperties["traceparent"] = activity.Id;
    message.ApplicationProperties["tracestate"]  = activity.TraceStateString;
}

await sender.SendMessageAsync(message, ct);
```

```csharp
// Receiver -- extract traceparent and link the consumer span
var processor = client.CreateProcessor(queueName);

processor.ProcessMessageAsync += async args =>
{
    // Extract upstream trace context
    ActivityContext parentContext = default;
    if (args.Message.ApplicationProperties.TryGetValue("traceparent", out var tp))
    {
        ActivityContext.TryParse(tp.ToString()!, null, out parentContext);
    }

    // Start a linked consumer activity
    using var activity = Telemetry.Source.StartActivity(
        "ServiceBus.Process",
        ActivityKind.Consumer,
        parentContext);

    activity?.SetTag("messaging.system", "servicebus");
    activity?.SetTag("messaging.destination", args.EntityPath);

    // ... process message
    await args.CompleteMessageAsync(args.Message);
};
```

### Azure Event Hubs

```csharp
// Producer -- inject into EventData properties
var eventData = new EventData(Encoding.UTF8.GetBytes(payload));
var activity = Activity.Current;
if (activity is not null)
{
    eventData.Properties["traceparent"] = activity.Id;
}
await producerClient.SendAsync(new[] { eventData }, ct);
```

```csharp
// Consumer -- restore context in EventProcessorClient handler
async Task ProcessEventAsync(ProcessEventArgs args)
{
    ActivityContext parentContext = default;
    if (args.Data.Properties.TryGetValue("traceparent", out var tp))
    {
        ActivityContext.TryParse(tp.ToString()!, null, out parentContext);
    }

    using var activity = Telemetry.Source.StartActivity(
        "EventHub.Process",
        ActivityKind.Consumer,
        parentContext);

    // ... process event
    await args.UpdateCheckpointAsync(args.CancellationToken);
}
```

## OTel Collector for advanced tracing scenarios

When services run in AKS or require tail-based sampling, route telemetry through an OTel Collector sidecar or DaemonSet rather than sending directly to Azure Monitor.

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: "0.0.0.0:4317"
      http:
        endpoint: "0.0.0.0:4318"

processors:
  batch:
    timeout: 10s
    send_batch_size: 1000

  # Tail-based sampling: always sample errors; 10% of success
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors-policy
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: rate-limiting
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }

exporters:
  azuremonitor:
    connection_string: "${APPLICATIONINSIGHTS_CONNECTION_STRING}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [azuremonitor]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [azuremonitor]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [azuremonitor]
```

Application services send to the Collector over OTLP gRPC (port 4317), not directly to Azure Monitor:

```csharp
// When routing through OTel Collector (AKS sidecar scenario)
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing =>
        tracing
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddSource("MyCompany.OrderService")
            .AddOtlpExporter(options =>
            {
                // Collector endpoint -- localhost when sidecar; service name when DaemonSet
                options.Endpoint = new Uri("http://localhost:4317");
                options.Protocol = OtlpExportProtocol.Grpc;
            }));
```

## Trace correlation in KQL

Find all telemetry for a given trace using the operation ID (= W3C trace ID, hex form):

```kql
// fn_trace_waterfall: full trace reconstruction
let op_id = "<trace-id>";
union AppRequests, AppDependencies, AppExceptions, AppTraces
| where OperationId == op_id
| project
    TimeGenerated,
    itemType,
    Name,
    Target,
    DurationMs,
    Success,
    ResultCode,
    Message,
    SeverityLevel,
    OperationParentId
| order by TimeGenerated asc
```

Reconstruct the waterfall by nesting on `OperationParentId`, the span ID of the parent span.

## Application Map

App Insights Application Map automatically builds the service dependency graph from distributed trace data. For this to work correctly:

- Every service must set a distinct Cloud Role Name (automatically set by the OTel Distro from the service name, or manually via `OTEL_SERVICE_NAME` environment variable).
- All services must share the same App Insights resource (or cross-resource query must be used).

```bash
# Set the service name via environment variable (preferred for container deployments)
OTEL_SERVICE_NAME=order-service
OTEL_SERVICE_VERSION=1.4.2
```

Verify the Application Map is populated correctly before declaring the distributed tracing design complete.

## Span attribute conventions

Follow OpenTelemetry semantic conventions for attribute naming. Consistent naming is required for App Insights query filtering and Application Map edge labelling.

| Domain | Key attributes |
|---|---|
| HTTP server | `http.request.method`, `url.path`, `http.response.status_code`, `network.protocol.version` |
| HTTP client | `http.request.method`, `server.address`, `server.port`, `http.response.status_code` |
| Database | `db.system`, `db.name`, `db.statement` (sanitised, no PII), `db.operation.name` |
| Messaging | `messaging.system`, `messaging.destination.name`, `messaging.operation.type` |
| Business | `order.id`, `tenant.id`, `user.id` (custom; prefix with your domain namespace) |

Never include PII in span attributes. Sanitise `db.statement` to remove literal values (use bind parameter placeholders). The OTel SQL Client instrumentation does this automatically.
