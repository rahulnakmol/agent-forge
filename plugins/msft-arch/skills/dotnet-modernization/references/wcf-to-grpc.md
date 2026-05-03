# WCF to gRPC Migration

**Applies to**: WCF services in .NET Framework codebases being migrated to .NET 8/9.

**Principle**: WCF to gRPC for new internal services; HTTP+OpenAPI for external/integration.

---

## Decision: gRPC vs. HTTP+OpenAPI vs. CoreWCF

| Factor | gRPC | HTTP+OpenAPI | CoreWCF (bridge) |
|---|---|---|---|
| Consumer type | Internal .NET services | External clients, browsers, third-party integrations | Existing WCF clients that cannot be updated |
| Contract format | Protobuf (binary, strongly typed) | JSON/XML over HTTP, OpenAPI spec | Existing WSDL/SOAP (subset) |
| Performance | High (HTTP/2, binary, multiplexed) | Moderate (HTTP/1.1 or HTTP/2, JSON) | Moderate (SOAP overhead retained) |
| Browser support | Via gRPC-Web only | Native | No |
| Streaming | Bidirectional streaming supported | Server-sent events or WebSockets needed separately | No |
| Use as destination | Yes | Yes | No: transition bridge only, not a destination |

**CoreWCF note**: CoreWCF supports a subset of WCF bindings (`BasicHttpBinding`, `NetTcpBinding`, `WSHttpBinding`). It is a community project, not a strategic Microsoft investment. Use it only when existing WSDL-bound clients cannot be updated during the migration window. Set an explicit exit date (target: < 18 months) and plan the gRPC or HTTP+OpenAPI replacement in parallel.

---

## gRPC Migration Steps

### 1. Define the Protobuf contract

Map each WCF service contract (`[ServiceContract]`, `[OperationContract]`) to a `.proto` service definition. WCF data contracts (`[DataContract]`, `[DataMember]`) map to Protobuf messages.

WCF original:
```csharp
[ServiceContract]
public interface IOrderService
{
    [OperationContract]
    Task<OrderResponse> GetOrderAsync(OrderRequest request);
}

[DataContract]
public class OrderRequest
{
    [DataMember]
    public Guid OrderId { get; set; }
}
```

Equivalent `.proto`:
```protobuf
syntax = "proto3";
option csharp_namespace = "Contoso.Orders.Grpc";

service OrderService {
  rpc GetOrder (OrderRequest) returns (OrderResponse);
}

message OrderRequest {
  string order_id = 1; // map Guid to string in proto3
}

message OrderResponse {
  string order_id = 1;
  string status = 2;
}
```

### 2. Create the ASP.NET Core gRPC service

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddGrpc();
// Register domain services
builder.Services.AddScoped<IOrderRepository, OrderRepository>();

var app = builder.Build();
app.MapGrpcService<OrderServiceImpl>();
app.Run();
```

```csharp
// OrderServiceImpl.cs
public class OrderServiceImpl(IOrderRepository repo) : OrderService.OrderServiceBase
{
    public override async Task<OrderResponse> GetOrder(
        OrderRequest request,
        ServerCallContext context)
    {
        var order = await repo.GetByIdAsync(Guid.Parse(request.OrderId), context.CancellationToken);
        return new OrderResponse { OrderId = order.Id.ToString(), Status = order.Status.ToString() };
    }
}
```

### 3. Configure the gRPC client (consuming service)

```csharp
// Register via client factory (DI-friendly)
builder.Services
    .AddGrpcClient<OrderService.OrderServiceClient>(o =>
    {
        o.Address = new Uri("https://orders-grpc-service/");
    })
    .EnableCallContextPropagation(); // propagates deadlines and cancellation
```

### 4. gRPC with JSON transcoding for external callers (hybrid approach)

When a service must be both gRPC (internal) and HTTP+OpenAPI (external) simultaneously, use JSON transcoding:

```csharp
builder.Services.AddGrpc().AddJsonTranscoding();
builder.Services.AddGrpcSwagger();
builder.Services.AddSwaggerGen(c =>
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "Orders API", Version = "v1" }));
```

Add HTTP annotations to the `.proto` file:
```protobuf
import "google/api/annotations.proto";

service OrderService {
  rpc GetOrder (OrderRequest) returns (OrderResponse) {
    option (google.api.http) = {
      get: "/api/orders/{order_id}"
    };
  }
}
```

This exposes the same service as both `grpc://` (internal) and `https://api/orders/{id}` (external) with no duplicate implementation.

---

## WCF Duplex / Streaming to gRPC Streaming

WCF duplex contracts (callback channels) map to gRPC bidirectional streaming:

```protobuf
service NotificationService {
  rpc Subscribe (SubscribeRequest) returns (stream NotificationEvent);
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}
```

---

## HTTP+OpenAPI Migration (External Services)

For WCF services consumed by external clients (browsers, third-party systems, or non-.NET services), replace WCF with Minimal API or ASP.NET Core Web API + Swashbuckle/NSwag:

```csharp
// Minimal API replacement for a simple WCF operation
app.MapGet("/api/orders/{id}", async (Guid id, IOrderRepository repo, CancellationToken ct) =>
{
    var order = await repo.GetByIdAsync(id, ct);
    return order is null ? Results.NotFound() : Results.Ok(order);
})
.WithOpenApi();
```

For the target-state API surface design (Minimal APIs vs. Web API vs. MVC), delegate to `/dotnet-architect`.

---

## References

- gRPC for WCF developers: https://learn.microsoft.com/dotnet/architecture/grpc-for-wcf-developers
- ASP.NET Core gRPC services: https://learn.microsoft.com/aspnet/core/grpc/aspnetcore
- gRPC JSON transcoding + OpenAPI: https://learn.microsoft.com/aspnet/core/grpc/json-transcoding-openapi
- CoreWCF on GitHub: https://github.com/CoreWCF/CoreWCF
