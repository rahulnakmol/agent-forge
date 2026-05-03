# Dependency Injection and Options Patterns

The .NET DI container is the backbone of every ASP.NET Core application. Get the registration model right at the start; lifetime mismatches and service locator usage accumulate into a debugging nightmare at scale.

## Constructor Injection: the Only Pattern

Inject all dependencies through the constructor. Never resolve from `IServiceProvider` inside a domain or application class. Never use `static` service locators. The DI container's purpose is to make dependencies explicit and testable; hiding them in method bodies defeats that purpose.

```csharp
// Good: dependencies explicit, testable without a container
public class OrderService(
    IOrderRepository repository,
    IPaymentGateway gateway,
    IEventPublisher events,
    ILogger<OrderService> logger)
{
    public async Task<Result<Order>> PlaceAsync(CreateOrderCommand cmd, CancellationToken ct)
    {
        logger.LogInformation("Placing order for customer {CustomerId}", cmd.CustomerId);
        // ...
    }
}

// Bad: hides dependencies, breaks testability, violates DI principles
public class OrderService
{
    public async Task<Result<Order>> PlaceAsync(CreateOrderCommand cmd, CancellationToken ct)
    {
        var repo = ServiceLocator.Current.GetInstance<IOrderRepository>(); // never
        // ...
    }
}
```

## Registration by Concern: Extension Methods

Group service registrations by domain concern in extension methods. This keeps `Program.cs` readable and makes it trivial to register the same concern in test fixtures.

```csharp
// Infrastructure/Extensions/ServiceCollectionExtensions.cs
namespace Contoso.Orders.Infrastructure;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddOrderModule(
        this IServiceCollection services,
        IConfiguration config)
    {
        services.AddScoped<IOrderRepository, EfOrderRepository>();
        services.AddScoped<IOrderService, OrderService>();
        services.AddScoped<IOrderQueryService, EfOrderQueryService>();
        services.Configure<OrderSettings>(config.GetSection("Orders"));
        return services;
    }

    public static IServiceCollection AddPaymentModule(
        this IServiceCollection services,
        IConfiguration config)
    {
        services.AddScoped<IPaymentGateway, StripePaymentGateway>();
        services.Configure<StripeSettings>(config.GetSection("Stripe"));
        return services;
    }
}
```

```csharp
// Program.cs: clean, intent-revealing
builder.Services
    .AddOrderModule(builder.Configuration)
    .AddPaymentModule(builder.Configuration);
```

## Lifetime Rules

| Lifetime | When to use | Pitfall |
|---|---|---|
| `Singleton` | Stateless, thread-safe services; caches; compiled query holders | Never capture scoped dependencies (captive dependency) |
| `Scoped` | Per-HTTP-request state; `DbContext`; services that access `HttpContext` | Cannot be injected into Singleton |
| `Transient` | Cheap, stateless objects with no shared state | Avoid for `DbContext` or expensive resources |

Scoped services injected into Singleton services cause the "captive dependency" bug: the scoped instance lives for the singleton's lifetime, not the request's. ASP.NET Core throws on startup when `ValidateScopes = true` (enabled by default in Development). Always run with validation enabled.

## IOptions\<T\>, IOptionsMonitor\<T\>, IOptionsSnapshot\<T\>

Three interfaces for typed configuration. Pick the right one; using `IOptions<T>` everywhere is the most common mistake.

**`IOptions<T>`**: reads configuration once at startup. No hot-reload. Use for settings that never change while the app is running (connection strings, static feature flags).

```csharp
public class EmailService(IOptions<EmailSettings> opts)
{
    private readonly EmailSettings _settings = opts.Value;
}
```

**`IOptionsMonitor<T>`**: Singleton. Reads the current value at the moment `.CurrentValue` is accessed. Supports hot-reload and change notifications. Use in Singleton services that need to pick up configuration changes without restarting.

```csharp
public class FeatureFlagService(IOptionsMonitor<FeatureFlags> monitor)
{
    public bool IsEnabled(string flag)
        => monitor.CurrentValue.EnabledFlags.Contains(flag);
}
```

Subscribe to changes:

```csharp
public class BackgroundPoller(IOptionsMonitor<PollerSettings> monitor)
{
    private PollerSettings _current = monitor.CurrentValue;

    public BackgroundPoller(IOptionsMonitor<PollerSettings> monitor)
    {
        _current = monitor.CurrentValue;
        monitor.OnChange(settings => _current = settings);
    }
}
```

**`IOptionsSnapshot<T>`**: Scoped. Recomputed per request. Use in Scoped or Transient services where you want hot-reload but also per-request consistency (all code within the same request sees the same snapshot).

```csharp
public class TenantSettingsService(IOptionsSnapshot<TenantSettings> snapshot)
{
    // snapshot.Value is consistent for the duration of this request
    public string GetTheme() => snapshot.Value.Theme;
}
```

Note: `IOptionsSnapshot<T>` has a known performance cost (recomputes per request); avoid it in high-throughput services where `IOptionsMonitor<T>` would suffice.

## Named Options

When the same configuration type is used for multiple named instances (e.g., two different queue connections of the same `QueueSettings` type), use named options:

```csharp
// Registration
services.Configure<QueueSettings>("orders", config.GetSection("Queues:Orders"));
services.Configure<QueueSettings>("notifications", config.GetSection("Queues:Notifications"));

// Consumer: inject IOptionsMonitor, request by name
public class OrderPublisher(IOptionsMonitor<QueueSettings> monitor)
{
    private QueueSettings Settings => monitor.Get("orders");
}
```

## Options Validation

Validate options at startup to fail fast rather than producing obscure runtime errors:

```csharp
services.AddOptions<StripeSettings>()
    .Bind(config.GetSection("Stripe"))
    .ValidateDataAnnotations()           // honours [Required], [Url], etc.
    .ValidateOnStart();                  // throws on app start if validation fails
```

For complex validation rules, implement `IValidateOptions<T>`:

```csharp
public class StripeSettingsValidator : IValidateOptions<StripeSettings>
{
    public ValidateOptionsResult Validate(string? name, StripeSettings options)
    {
        if (string.IsNullOrWhiteSpace(options.SecretKey))
            return ValidateOptionsResult.Fail("Stripe:SecretKey is required.");
        if (!options.SecretKey.StartsWith("sk_"))
            return ValidateOptionsResult.Fail("Stripe:SecretKey must begin with 'sk_'.");
        return ValidateOptionsResult.Success;
    }
}

services.AddSingleton<IValidateOptions<StripeSettings>, StripeSettingsValidator>();
```

## Keyed Services (.NET 8+)

When you have multiple implementations of the same interface and need to select one by key (without named options or a factory), use keyed services:

```csharp
// Registration
services.AddKeyedScoped<IPaymentGateway, StripeGateway>("stripe");
services.AddKeyedScoped<IPaymentGateway, PaypalGateway>("paypal");

// Consumer
public class PaymentRouter([FromKeyedServices("stripe")] IPaymentGateway stripe,
                           [FromKeyedServices("paypal")] IPaymentGateway paypal)
{
    public IPaymentGateway Route(string provider) => provider switch
    {
        "stripe" => stripe,
        "paypal" => paypal,
        _ => throw new ArgumentOutOfRangeException(nameof(provider))
    };
}
```

Keyed services are cleaner than the factory pattern for discrete, well-known variants. Use the factory pattern when the key space is dynamic (e.g., resolved at runtime from a database).

## Avoiding Common Pitfalls

- **Captive dependencies**: Singleton holding Scoped; detected by `ValidateScopes = true` in dev.
- **`HttpClient` without `IHttpClientFactory`**: Direct `new HttpClient()` exhausts socket handles. Always register via `AddHttpClient<T>()`.
- **`IServiceProvider` injection in domain classes**: Signals missing abstraction. Introduce an interface and inject the concrete dependency instead.
- **`IConfiguration` injection in domain/application layers**: Inject `IOptions<T>` for the specific settings your class needs. `IConfiguration` is an infrastructure concern.
