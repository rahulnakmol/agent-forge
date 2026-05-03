# .NET Aspire Orchestration

Aspire is a dev-time orchestration stack for distributed .NET applications. It wires service discovery, connection string injection, health checks, and OpenTelemetry between all resources in the AppHost, replacing a folder of docker-compose files and a pile of manual `appsettings.Development.json` edits. It is not a production runtime; `azd` or Terraform/AVM carry the same topology to Azure.

## The AppHost Project

The AppHost is the entry point for the distributed application. It models every resource (.NET projects, containers, databases, queues) and declares their dependencies. The `DistributedApplication` runtime starts them in the correct order and injects connection information automatically.

```csharp
// AppHost/Program.cs
var builder = DistributedApplication.CreateBuilder(args);

// Infrastructure resources
var postgres = builder.AddPostgres("postgres")
    .WithDataVolume()
    .AddDatabase("ordersdb");

var redis = builder.AddRedis("cache")
    .WithRedisCommander();

var serviceBus = builder.AddAzureServiceBus("messaging")
    .AddQueue("orders-created");

// .NET projects: Aspire injects connection strings automatically
var api = builder.AddProject<Projects.Orders_Api>("orders-api")
    .WithReference(postgres)
    .WithReference(redis)
    .WithReference(serviceBus)
    .WaitFor(postgres);

builder.AddProject<Projects.Orders_Worker>("orders-worker")
    .WithReference(postgres)
    .WithReference(serviceBus)
    .WaitFor(postgres);

builder.AddProject<Projects.Orders_Web>("orders-web")
    .WithReference(api)
    .WaitFor(api);

builder.Build().Run();
```

Running `dotnet run --project AppHost` starts all resources, opens the Aspire Dashboard, and streams structured logs and traces from every component.

## Service Defaults: telemetry by default

Every project in an Aspire solution should reference the `ServiceDefaults` project and call `AddServiceDefaults()` in its `Program.cs`. This wires OpenTelemetry (traces, metrics, logs), health check endpoints, and service discovery in a single call.

```csharp
// ServiceDefaults/Extensions.cs
public static class Extensions
{
    public static IHostApplicationBuilder AddServiceDefaults(this IHostApplicationBuilder builder)
    {
        builder.ConfigureOpenTelemetry();
        builder.AddDefaultHealthChecks();
        builder.Services.AddServiceDiscovery();
        builder.Services.ConfigureHttpClientDefaults(http =>
        {
            http.AddStandardResilienceHandler();
            http.AddServiceDiscovery();
        });
        return builder;
    }
}
```

```csharp
// Orders.Api/Program.cs
builder.AddServiceDefaults();   // one line: telemetry, health, service discovery configured
```

Never skip `AddServiceDefaults`; an Aspire component missing this call produces no traces in the dashboard, making debugging distributed flows significantly harder.

## Polyglot Orchestration

Aspire orchestrates more than .NET projects. Any container image, Node/Bun process, or Python script can be a named resource. This is where the "Bun > Node for tooling" rule applies: if you have a TypeScript-based BFF or script, add it via `AddNpmApp` (or a custom executable) and reference it from the AppHost just like a .NET project.

```csharp
// Adding a containerised Redis with a management UI
var redis = builder.AddRedis("cache")
    .WithRedisCommander();   // adds RedisCommander container alongside

// Adding a standalone container image
var otel = builder.AddContainer("otel-collector", "otel/opentelemetry-collector-contrib")
    .WithArgs("--config=/etc/otel/config.yaml")
    .WithBindMount("./otel-config.yaml", "/etc/otel/config.yaml");
```

## Connection String Injection

When a project declares `.WithReference(postgres)`, Aspire injects a `ConnectionStrings__ordersdb` environment variable at launch. EF Core picks this up via `IConfiguration` without any manual wiring.

```csharp
// Infrastructure project
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("ordersdb")));
```

For Azure resources provisioned via Aspire's Azure hosting integrations, the injected connection string uses Managed Identity automatically in production mode and local emulators/connection strings in development; no code change required.

## Health Checks

`AddDefaultHealthChecks()` registers `/healthz` (liveness) and `/alive` endpoints. Extend with resource-specific checks:

```csharp
builder.Services.AddHealthChecks()
    .AddNpgsql(builder.Configuration.GetConnectionString("ordersdb")!)
    .AddRedis(builder.Configuration.GetConnectionString("cache")!)
    .AddAzureServiceBusQueue(
        builder.Configuration.GetConnectionString("messaging")!,
        "orders-created");
```

The Aspire Dashboard displays health status for every registered resource in real time.

## Dev/Production Parity

Aspire's Azure hosting integrations provision real Azure resources locally via the Azure Developer CLI during inner-loop development, or use local emulators where available (Azure Storage Emulator, Azurite, Service Bus emulator). This gives closer parity between dev and production than docker-compose alone.

For production deployment, `azd provision && azd deploy` reads the AppHost's resource model and generates Bicep. Review the generated Bicep; it is a starting point, not a production-ready template. Hand off to `iac-architect` for Terraform-first IaC once the topology is validated.

```bash
# Generate infrastructure from Aspire model (azd)
azd infra gen

# Provision and deploy to Azure
azd up
```

## What Aspire Is Not

- **Not a production container orchestrator.** Do not run the AppHost in AKS or Container Apps. Aspire is a developer experience tool.
- **Not a replacement for health probes in Kubernetes.** The health check endpoints Aspire wires are input to K8s liveness/readiness probes; they are complementary, not redundant.
- **Not a service mesh.** Aspire service discovery uses DNS naming conventions. mTLS, traffic shaping, and advanced resilience belong to the service mesh layer (Dapr, Envoy, or ASB-based patterns).

## Dashboard

The Aspire Dashboard is a local observability UI that aggregates structured logs, distributed traces, and metrics from every resource. It listens on OTLP and is the first stop when debugging cross-service call failures in the inner loop.

Access it at `https://localhost:15000` (default) after `dotnet run --project AppHost`. The dashboard shows:
- Structured log streams per resource with severity filtering
- Distributed trace waterfall across service boundaries
- Resource health and environment variable snapshot per project
