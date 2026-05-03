# C# Coding Standards

**Applies to**: .NET 8 (LTS) and .NET 9 (LTS when released Nov 2025). All new projects MUST target one of these. .NET 6 is EOL; avoid unless a hard dependency prevents migration.

---

## Target Framework and Language Version

Set `<TargetFramework>net9.0</TargetFramework>` (or `net8.0` for LTS stability) in every `.csproj`. Never leave `<LangVersion>` unset; pin it explicitly:

```xml
<PropertyGroup>
  <TargetFramework>net9.0</TargetFramework>
  <LangVersion>13.0</LangVersion>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>
```

## Nullable Reference Types (NRT)

`<Nullable>enable</Nullable>` is mandatory on all new projects and must be enabled when migrating existing ones. Never use `#nullable disable` to suppress; fix the root cause.

Rules:
- Return `T?` only when null is a valid, meaningful result, not as a lazy shorthand for "might fail."
- Annotate parameters: `string? name` signals optionality at the call site.
- Use `!` (null-forgiving) only when you can prove nullability via an invariant the compiler cannot see. Add a comment explaining why.

## Modern Language Features (C# 12 / C# 13)

**File-scoped namespaces**: mandatory on all new files. One namespace per file, no braces:

```csharp
namespace Contoso.Orders.Application;

public class OrderService { }
```

**Primary constructors** (C# 12+): prefer for services and domain objects where the parameters are used only for initialization or captured directly:

```csharp
public class PaymentProcessor(IPaymentGateway gateway, ILogger<PaymentProcessor> logger)
{
    public async Task<Result<PaymentId>> ProcessAsync(PaymentRequest request, CancellationToken ct)
    {
        logger.LogInformation("Processing payment {Amount}", request.Amount);
        return await gateway.ChargeAsync(request, ct);
    }
}
```

Do not use primary constructors when you need parameter validation logic; use a standard constructor with a guard clause.

**`required` keyword**: use on DTO properties that have no sensible default:

```csharp
public class CreateOrderCommand
{
    public required Guid CustomerId { get; init; }
    public required IReadOnlyList<OrderLine> Lines { get; init; }
}
```

**`record` for DTOs and value objects**: use `record` (positional or with `init` setters) for any type that is logically immutable after construction:

```csharp
public record OrderLine(Guid ProductId, int Quantity, decimal UnitPrice);
```

**`readonly struct`**: use for small, allocation-sensitive value types on hot paths. Pair with `Span<T>` and `Memory<T>` for buffer manipulation:

```csharp
public readonly struct Money(decimal amount, string currency)
{
    public decimal Amount { get; } = amount;
    public string Currency { get; } = currency;
}
```

## Async Rules

- Never call `.Result` or `.Wait()` on a `Task`; deadlocks in ASP.NET contexts are guaranteed.
- Always propagate `CancellationToken` from the outermost handler inward. If a method does async I/O, it must accept `CancellationToken ct`.
- Prefer `ConfigureAwait(false)` in library code; in application code (controllers, Blazor components) it is not needed.
- Use `IAsyncEnumerable<T>` instead of `Task<List<T>>` for streams, search results, or any sequence that can be yielded incrementally:

```csharp
public async IAsyncEnumerable<Product> SearchAsync(
    string query,
    [EnumeratorCancellation] CancellationToken ct)
{
    await foreach (var item in _repository.StreamAsync(query, ct))
        yield return item;
}
```

## Error Handling: Result Types Over Exceptions

Exceptions are for exceptional, unrecoverable situations. For expected failure paths (validation failure, not-found, conflict), use `Result<T>` or `OneOf<TSuccess, TError>`:

```csharp
// Prefer
public async Task<Result<Order>> PlaceOrderAsync(CreateOrderCommand cmd, CancellationToken ct)
{
    if (cmd.Lines.Count == 0)
        return Result.Fail<Order>("Order must have at least one line.");

    var order = Order.Create(cmd);
    await _repo.AddAsync(order, ct);
    return Result.Ok(order);
}
```

Never use exceptions for control flow across service boundaries. Callers should not need try/catch for business logic branches.

## Functional-Leaning Patterns

- Prefer immutable types (`record`, `readonly struct`, `IReadOnlyList<T>`). Mutability should be opt-in.
- Write pure methods where possible: no side effects, same output for same input.
- Prefer LINQ for data transformation pipelines on in-memory collections. Use explicit loops when: the LINQ chain exceeds ~4 operations, you need early exit with `break`, or performance profiling shows allocation pressure.
- Do not mix LINQ and side effects (e.g., `list.Where(x => { _log.Log(x); return true; })`).

## Dependency Injection

- Constructor injection only. Never use `IServiceLocator`, `ServiceLocator.Current`, or the anti-pattern of resolving from `IServiceProvider` inside a domain class.
- Register services at startup in extension methods grouped by concern: `services.AddOrderModule()`.
- Use `IOptions<T>` for typed configuration; never inject `IConfiguration` into domain or application layer classes.
- Scope lifetimes deliberately: `Singleton` for stateless services, `Scoped` for per-request state, `Transient` for cheap stateless objects.

## Configuration

```csharp
// Bind in Program.cs or extension method
services.Configure<PaymentSettings>(config.GetSection("Payment"));

// Inject in consumer
public class PaymentProcessor(IOptions<PaymentSettings> opts) { }
```

Never read `Environment.GetEnvironmentVariable` directly in production code; always go through `IConfiguration`.

## Logging

Use `Microsoft.Extensions.Logging` with structured logging. Never concatenate strings for log messages:

```csharp
// Correct: structured, filterable, cheap when the level is disabled
logger.LogInformation("Order {OrderId} placed by {CustomerId}", order.Id, order.CustomerId);

// Wrong: string allocation occurs even when log level is off
logger.LogInformation($"Order {order.Id} placed by {order.CustomerId}");
```

Use compile-time log source generation (`[LoggerMessage]`) for hot-path logging.

## XML Documentation

All public API surface must have XML doc-comments. Minimum:

```csharp
/// <summary>
/// Places a new order and raises the <see cref="OrderPlacedEvent"/> domain event.
/// </summary>
/// <param name="cmd">The validated create-order command.</param>
/// <param name="ct">Propagated cancellation token.</param>
/// <returns>The created order, or a failure result describing the validation error.</returns>
public Task<Result<Order>> PlaceOrderAsync(CreateOrderCommand cmd, CancellationToken ct);
```

> For EF Core-specific patterns (AsNoTracking, compiled queries, migration workflow), see [ef-core-checklist.md](./ef-core-checklist.md).

## Trade-offs and Exceptions

| Rule | When to break it |
|---|---|
| NRT enabled | Interop with older third-party SDKs that return `object`; suppress per-file with comment |
| `Result<T>` over exceptions | Cross-cutting infrastructure failures (DB down, disk full); throw and let them propagate to global handlers |
| Primary constructors | When guard clauses, complex property initialization, or multiple overloads are needed; use standard constructor |
| `IAsyncEnumerable` for streams | When the caller always needs the full set and count (e.g., paginated API responses returning `PagedResult<T>`) |
| LINQ over loops | Tight inner loops processing millions of items; measure first, then switch to explicit loops with `Span<T>` |
| No `.Result` / `.Wait()` | Synchronous entry points (console `Main` before `async Main` was available, test frameworks with limited async); isolate and document |
