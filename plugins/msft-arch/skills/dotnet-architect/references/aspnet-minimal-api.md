# ASP.NET Core Minimal APIs

Minimal APIs are the default choice for new ASP.NET Core services. They eliminate controller boilerplate, keep startup code explicit, and produce OpenAPI documents natively in .NET 9. Use them unless you have a large existing controller hierarchy.

## Route Groups: the primary organisational unit

Route groups (`MapGroup`) replace controller classes. Every group gets a shared prefix and can carry authentication, authorisation, filters, and OpenAPI metadata applied to all endpoints within it.

```csharp
// OrdersApi.cs
namespace Contoso.Orders.Api;

public static class OrdersApi
{
    public static RouteGroupBuilder MapOrdersApi(this RouteGroupBuilder group)
    {
        group.MapGet("/", GetAllOrders);
        group.MapGet("/{id:guid}", GetOrder);
        group.MapPost("/", CreateOrder);
        group.MapPut("/{id:guid}", UpdateOrder);
        group.MapDelete("/{id:guid}", CancelOrder);
        return group;
    }

    static async Task<Ok<PagedResult<OrderSummary>>> GetAllOrders(
        [AsParameters] PaginationQuery query,
        IOrderQueryService svc,
        CancellationToken ct)
    {
        var result = await svc.ListAsync(query, ct);
        return TypedResults.Ok(result);
    }

    static async Task<Results<Ok<OrderDetail>, NotFound>> GetOrder(
        Guid id,
        IOrderQueryService svc,
        CancellationToken ct)
    {
        var order = await svc.FindAsync(id, ct);
        return order is null
            ? TypedResults.NotFound()
            : TypedResults.Ok(order);
    }

    static async Task<Results<Created<OrderDetail>, ValidationProblem>> CreateOrder(
        CreateOrderRequest request,
        IOrderService svc,
        CancellationToken ct)
    {
        var result = await svc.PlaceAsync(request, ct);
        return result.IsSuccess
            ? TypedResults.Created($"/orders/{result.Value.Id}", result.Value)
            : TypedResults.ValidationProblem(result.Errors.ToDictionary(e => e.Code, e => new[] { e.Message }));
    }
}
```

Register in `Program.cs`:

```csharp
var orders = app.MapGroup("/orders")
    .RequireAuthorization()
    .WithTags("Orders")
    .ProducesProblem(StatusCodes.Status500InternalServerError);

orders.MapOrdersApi();
```

### Nested groups

Groups can nest. Outer group metadata applies to all inner endpoints:

```csharp
var api = app.MapGroup("/api/v1").WithOpenApi();
var secured = api.MapGroup("").RequireAuthorization();

secured.MapGroup("/orders").MapOrdersApi();
secured.MapGroup("/customers").MapCustomersApi();
```

## TypedResults: always prefer over Results

`TypedResults` returns strongly typed `IResult` implementations. This matters for two reasons: OpenAPI metadata is inferred automatically, and unit tests can verify the exact return type without parsing HTTP responses.

```csharp
// Testable: returns Ok<OrderDetail>, not IResult
static async Task<Ok<OrderDetail>> GetOrderHandler(Guid id, IOrderQueryService svc, CancellationToken ct)
    => TypedResults.Ok(await svc.FindAsync(id, ct));
```

Use `Results<T1, T2, T3>` as the return type for endpoints with multiple outcomes; the OpenAPI generator emits each status code:

```csharp
static async Task<Results<Ok<OrderDetail>, NotFound, ForbidHttpResult>> GetOrder(
    Guid id, ClaimsPrincipal user, IOrderQueryService svc, CancellationToken ct)
{ ... }
```

## Endpoint Filters: cross-cutting concerns without middleware

Endpoint filters are the Minimal API equivalent of action filters. They run before and after the route handler and are scoped to the endpoint or group, unlike middleware, which affects the entire pipeline.

```csharp
// Validation filter using IEndpointFilter
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var argument = context.GetArgument<T>(0);
        var validator = context.HttpContext.RequestServices
            .GetRequiredService<IValidator<T>>();

        var validation = await validator.ValidateAsync(argument);
        if (!validation.IsValid)
        {
            return TypedResults.ValidationProblem(
                validation.ToDictionary());
        }

        return await next(context);
    }
}
```

Apply to a group so validation runs on every `POST`/`PUT` handler in the group:

```csharp
group.AddEndpointFilter<ValidationFilter<CreateOrderRequest>>();
```

## OpenAPI Integration (.NET 9 built-in)

.NET 9 ships `Microsoft.AspNetCore.OpenApi` as a first-party package. No Swashbuckle required for basic scenarios.

```csharp
// Program.cs
builder.Services.AddOpenApi();

// after app.Build()
app.MapOpenApi();           // serves /openapi/v1.json
```

Enrich endpoint metadata with extension methods; the OpenAPI document picks them up:

```csharp
group.MapPost("/", CreateOrder)
    .WithName("CreateOrder")
    .WithSummary("Place a new order")
    .WithDescription("Validates lines, reserves inventory, raises OrderPlaced event.")
    .Produces<OrderDetail>(StatusCodes.Status201Created)
    .ProducesValidationProblem()
    .ProducesProblem(StatusCodes.Status409Conflict);
```

For build-time document generation (useful for contract testing):

```xml
<!-- .csproj -->
<PackageReference Include="Microsoft.Extensions.ApiDescription.Server" Version="9.*" />
<PropertyGroup>
  <OpenApiDocumentsDirectory>$(MSBuildProjectDirectory)/openapi</OpenApiDocumentsDirectory>
</PropertyGroup>
```

## Validation Strategy

Prefer FluentValidation registered against the DI container, invoked via an endpoint filter (see above). Avoid DataAnnotations for complex validation; they scale poorly and hide logic in attributes.

```csharp
// Registration in extension method
services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>();
```

For simple scalar validation (route constraints, query parameter guards), use `Results.Problem` or `TypedResults.ValidationProblem` inline:

```csharp
static IResult GetPage([AsParameters] PaginationQuery q)
{
    if (q.PageSize is < 1 or > 100)
        return TypedResults.ValidationProblem(
            new Dictionary<string, string[]>
            {
                ["pageSize"] = ["Must be between 1 and 100."]
            });
    // ...
}
```

## Parameter Binding

Minimal API parameter binding is positional and attribute-driven. The framework infers binding source from context:

| Parameter type | Inferred source |
|---|---|
| Simple scalar (int, Guid, string) | Route, then query string |
| Record / class with `[FromBody]` | Request body (JSON) |
| `[AsParameters]` struct or record | Binds each property from its own source |
| `IFormFile` | Multipart form |
| `HttpContext`, `CancellationToken` | Injected by framework; never from request |

Use `[AsParameters]` for query-string filter objects to avoid parameter explosion:

```csharp
record PaginationQuery(int Page = 1, int PageSize = 20, string? Search = null);

// Handler signature: clean, no [FromQuery] noise
static Task<Ok<PagedResult<T>>> ListAsync([AsParameters] PaginationQuery q, ...) { }
```

## Testing Minimal API Endpoints

Unit test handlers directly; they are static methods or local functions, testable without a running server:

```csharp
[Fact]
public async Task GetOrder_ReturnsOk_WhenOrderExists()
{
    var svc = Substitute.For<IOrderQueryService>();
    svc.FindAsync(Arg.Any<Guid>(), Arg.Any<CancellationToken>())
       .Returns(new OrderDetail { Id = Guid.NewGuid() });

    var result = await OrdersApi.GetOrder(Guid.NewGuid(), svc, CancellationToken.None);

    result.Result.Should().BeOfType<Ok<OrderDetail>>();
}
```

Integration test the full route group via `WebApplicationFactory`; see `testing-strategy.md`.
