# Blazor Patterns

Blazor unifies server and client UI under a single C# component model. The hosting choice determines where code executes, not how you write components. Pick the hosting model once and standardise; mixing render modes per-component (.NET 8 Blazor Web App) is powerful but increases cognitive load.

## Hosting Model Decision Matrix

| Criterion | Blazor Server | Blazor WASM | Blazor Hybrid (MAUI) |
|---|---|---|---|
| Internal tooling / admin | First choice | Avoid | N/A |
| Public-facing SPA | Avoid (latency) | First choice | N/A |
| Offline requirement | No | Yes (PWA) | Yes |
| Static CDN hosting | No | Yes | No |
| Full .NET API access | Yes | Partial | Yes |
| Initial load time | Fast | Slow (download) | Fast |
| Mobile / desktop native | No | No | Yes |

**Rule**: Blazor Server for internal apps (network hop latency is acceptable on a corporate LAN); WASM only when offline capability or CDN-only hosting is required; Hybrid when reusing Blazor components in a MAUI native app.

## Component Design Principles

### Keep components thin

A component's responsibility is rendering and capturing user input, not data fetching or business logic. Move service calls into injected services; components hold `@inject` bindings and call them.

```razor
@page "/orders"
@inject IOrderQueryService OrderService
@inject NavigationManager Nav

@if (_orders is null)
{
    <p>Loading...</p>
}
else
{
    <OrderTable Orders="_orders" OnRowSelected="NavigateToOrder" />
}

@code {
    private IReadOnlyList<OrderSummary>? _orders;

    protected override async Task OnInitializedAsync()
        => _orders = await OrderService.ListAsync(CancellationToken.None);

    private void NavigateToOrder(Guid id) => Nav.NavigateTo($"/orders/{id}");
}
```

### Prefer `record` or immutable types for parameters

Component parameters should be immutable. Use `record` or `IReadOnlyList<T>`; mutation inside a component via a parameter property is a frequent source of cascading re-render bugs.

```csharp
// Good: immutable parameter
[Parameter] public required OrderDetail Order { get; set; }

// Bad: mutable list parameter; mutations don't trigger parent re-render
[Parameter] public List<OrderLine> Lines { get; set; } = new();
```

### Use `EventCallback<T>` over direct callbacks

`EventCallback<T>` automatically calls `StateHasChanged` on the parent after the handler completes, preventing missed re-renders.

```razor
<button @onclick="() => OnLineAdded.InvokeAsync(newLine)">Add</button>

@code {
    [Parameter] public EventCallback<OrderLine> OnLineAdded { get; set; }
}
```

## State Management

### Scoped services (Blazor Server)

In Blazor Server, DI scoped services live for the duration of the SignalR circuit, not the HTTP request. This means a scoped `DbContext` persists across the user's session, which causes EF Core change-tracking bugs. Use `IDbContextFactory<T>` to create short-lived contexts per operation.

```csharp
// Good: short-lived context, no stale tracking
public class OrderQueryService(IDbContextFactory<AppDbContext> factory)
{
    public async Task<OrderDetail?> FindAsync(Guid id, CancellationToken ct)
    {
        await using var db = await factory.CreateDbContextAsync(ct);
        return await db.Orders
            .AsNoTracking()
            .Where(o => o.Id == id)
            .Select(o => new OrderDetail(o.Id, o.Status, o.PlacedAt))
            .FirstOrDefaultAsync(ct);
    }
}
```

### Cascading values for cross-component state

Use `CascadingValue` for state that many descendant components need (e.g., current user, tenant context). Avoid prop-drilling more than two levels deep.

```razor
<CascadingValue Value="_currentUser">
    <Router AppAssembly="typeof(App).Assembly" />
</CascadingValue>

@code {
    private CurrentUser? _currentUser;
    protected override async Task OnInitializedAsync()
        => _currentUser = await UserService.GetCurrentUserAsync();
}
```

### Blazor WASM: client-side state

For WASM apps with complex state, use a simple observable state container rather than a third-party state management library. The overhead of Redux-style libraries is rarely justified for Blazor component trees.

```csharp
public class OrderCartState
{
    private readonly List<OrderLine> _lines = new();
    public IReadOnlyList<OrderLine> Lines => _lines.AsReadOnly();
    public event Action? OnChange;

    public void AddLine(OrderLine line)
    {
        _lines.Add(line);
        OnChange?.Invoke();
    }
}
```

Register as Scoped (or Singleton for WASM where Scoped == Singleton):

```csharp
builder.Services.AddScoped<OrderCartState>();
```

## Authentication Integration

### Blazor Server

Authentication flows through the ASP.NET Core middleware pipeline. Inject `AuthenticationStateProvider` and use `<AuthorizeView>` for conditional rendering.

```razor
<AuthorizeView Policy="OrderManager">
    <Authorized>
        <button @onclick="ApproveOrder">Approve</button>
    </Authorized>
    <NotAuthorized>
        <p>You don't have permission to approve orders.</p>
    </NotAuthorized>
</AuthorizeView>
```

For programmatic checks inside `@code`:

```csharp
[CascadingParameter] private Task<AuthenticationState> AuthState { get; set; } = default!;

protected override async Task OnInitializedAsync()
{
    var auth = await AuthState;
    if (!auth.User.IsInRole("OrderManager"))
        Nav.NavigateTo("/access-denied");
}
```

### Blazor WASM

WASM apps authenticate via OIDC redirect flows. Use `Microsoft.AspNetCore.Components.WebAssembly.Authentication`:

```csharp
// Program.cs (WASM)
builder.Services.AddMsalAuthentication(options =>
{
    builder.Configuration.Bind("AzureAd", options.ProviderOptions.Authentication);
    options.ProviderOptions.DefaultAccessTokenScopes.Add("api://contoso-api/.default");
});
```

Attach the token to outgoing API calls using `AuthorizationMessageHandler`:

```csharp
builder.Services.AddHttpClient<IOrderApiClient, OrderApiClient>(client =>
    client.BaseAddress = new Uri("https://api.contoso.com"))
    .AddHttpMessageHandler<BaseAddressAuthorizationMessageHandler>();
```

## Razor Class Libraries (RCL) for Component Reuse

When components need to run in both Blazor Web App and Blazor Hybrid, extract them into an RCL. The RCL must not reference hosting-model-specific APIs directly; abstract them behind interfaces and inject implementations per host.

```csharp
// In RCL: abstract the platform capability
public interface IFilePickerService
{
    Task<Stream?> PickAsync(CancellationToken ct);
}

// Blazor WASM implementation (in WASM project)
public class BrowserFilePickerService : IFilePickerService { ... }

// MAUI implementation (in MAUI project)
public class MauiFilePickerService : IFilePickerService { ... }
```

Register the correct implementation in each host's `Program.cs`. Components in the RCL call `IFilePickerService`; they are agnostic to the host.

## Performance Considerations

- **Avoid `StateHasChanged` in tight loops.** Each call schedules a re-render. Batch state changes and call once.
- **Virtualise long lists** with `<Virtualize>`. Blazor renders only visible rows, avoiding DOM explosion on large datasets.
- **AOT compile WASM for production.** Add `<RunAOTCompilation>true</RunAOTCompilation>` in the release build profile. Initial download increases; runtime performance improves significantly.
- **Use `@key` on list items.** Without a key, Blazor's differ cannot detect moves; it destroys and re-creates components unnecessarily.

```razor
@foreach (var order in Orders)
{
    <OrderRow @key="order.Id" Order="order" />
}
```
