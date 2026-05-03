# ASP.NET Web Forms to Blazor Migration

**Applies to**: ASP.NET Web Forms applications (`.aspx`, `.ascx`, `.asmx`, code-behind `.aspx.cs`) on .NET Framework.

**Principle**: ASP.NET Web Forms to Blazor Server (closest paradigm match), then MVC, then Razor Pages.

---

## Technology Selection

| Target | When to choose |
|---|---|
| **Blazor Server** (default) | Internal tools, admin dashboards, line-of-business apps with a small-to-medium concurrent user base. Closest paradigm to Web Forms: stateful, event-driven, component-based. Server owns all state; SignalR delivers DOM diffs to the browser. |
| **Blazor Web App (.NET 8+ render-mode-per-component)** | New full-stack Blazor projects that need a mix of server and WASM rendering. Default for new Blazor work per `/dotnet-architect`. |
| **MVC (ASP.NET Core)** | Teams with strong MVC muscle memory; large controller hierarchies already in ASP.NET MVC 4/5 that are being migrated alongside Web Forms; UI does not require fine-grained component interactivity. |
| **Razor Pages** | Form-heavy page-per-feature UIs where page model pattern is a natural fit; simpler than MVC; no component reuse needed. |
| **Blazor WASM** | Public-facing SPAs, offline apps, CDN-hosted static sites. Not a direct Web Forms migration target: the paradigm shift is larger. |

---

## Web Forms to Blazor Conceptual Mapping

| Web Forms concept | Blazor Server equivalent |
|---|---|
| Page (`.aspx`) | Component (`.razor`) with `@page` directive |
| User Control (`.ascx`) | Component (`.razor`, no `@page`) |
| Code-behind (`Page_Load`, event handlers) | Component lifecycle methods (`OnInitializedAsync`, `OnParametersSetAsync`) + event callbacks |
| `ViewState` | Component parameters + `[CascadingParameter]` + scoped services for shared state |
| `ScriptManager` / UpdatePanel | Blazor renders diffs automatically via SignalR; no equivalent needed |
| `HttpModules` / `HttpHandlers` | ASP.NET Core middleware |
| `web.config` system.web section | `appsettings.json` + `IConfiguration` |
| `Session` (in-proc) | Distributed cache (Redis / Azure Cache for Redis) via `IDistributedCache` |
| `Global.asax` Application events | ASP.NET Core middleware pipeline + `IHostedService` |
| Data source controls (`ObjectDataSource`, `SqlDataSource`) | Services injected via DI (`@inject IOrderService OrderService`) |
| Master Pages | Blazor layouts (`MainLayout.razor`) |
| `Response.Redirect` | `NavigationManager.NavigateTo` |
| `Page.IsPostBack` | Not applicable: Blazor components re-render on state change, not postbacks |

---

## Migration Workflow

### Step 0: N-tier architecture prerequisite

Web Forms migration is significantly easier if the business logic is already in a separate class library (N-tier: UI / BLL / DAL separation). If `Page_Load` contains business logic directly, extract it to service classes first, before touching the UI.

### Step 1: Create the ASP.NET Core + Blazor Server project

```dotnetcli
dotnet new blazorserver -n Contoso.Web --framework net8.0
```

Or use the **Blazor Web App** template for .NET 8+ unified hosting:
```dotnetcli
dotnet new blazor -n Contoso.Web --framework net8.0
```

Add Blazor Server services:
```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

// Register domain services
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();
app.UseStaticFiles();
app.UseAntiforgery();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();
app.Run();
```

### Step 2: Convert pages to Razor components

Convert each `.aspx` page to a `.razor` component. Minimal mapping:

```razor
@* Web Forms equivalent: Default.aspx + Default.aspx.cs *@
@page "/"
@inject IOrderService OrderService

<h1>Orders</h1>

@if (_orders is null)
{
    <p>Loading...</p>
}
else
{
    <ul>
        @foreach (var order in _orders)
        {
            <li>@order.Id - @order.Status</li>
        }
    </ul>
}

@code {
    private IReadOnlyList<OrderSummary>? _orders;

    protected override async Task OnInitializedAsync()
    {
        _orders = await OrderService.GetAllAsync(CancellationToken.None);
    }
}
```

### Step 3: Migrate HTTP modules to middleware

```csharp
// Web Forms web.config HttpModule equivalent
app.Use(async (context, next) =>
{
    // Pre-request logic (formerly Application_BeginRequest)
    await next(context);
    // Post-request logic (formerly Application_EndRequest)
});
```

### Step 4: Replace Session with distributed state

```csharp
// Program.cs
builder.Services.AddStackExchangeRedisCache(options =>
    options.Configuration = builder.Configuration.GetConnectionString("Redis"));

// Component
@inject IDistributedCache Cache

var cartJson = await Cache.GetStringAsync($"cart:{userId}", ct);
```

For Blazor Server, prefer scoped services over `IDistributedCache` for in-circuit state (state scoped to a user's active SignalR connection). `IDistributedCache` is for state that must survive circuit reconnection or span multiple nodes.

### Step 5: Replace static file serving

```csharp
// Program.cs
app.UseStaticFiles(); // serves from wwwroot/
```

Move all `.css`, `.js`, images from the Web Forms `App_Themes` and root directory to `wwwroot/`.

---

## Handling Web Forms-Specific Features

| Feature | Migration path |
|---|---|
| `WebMethod` (`[WebMethod]` on `.aspx`) | Minimal API endpoint or gRPC if internal |
| `ScriptService` / Atlas | Replace with API endpoint; consume via `HttpClient` or Blazor JS interop |
| `DataGrid` / `GridView` | Use a .NET component library (`MudBlazor`, `Radzen`, `Telerik Blazor`) |
| `FileUpload` control | `InputFile` component in Blazor |
| Membership / `FormsAuthentication` | ASP.NET Core Identity or Entra ID |
| URL routing (`RouteTable`) | ASP.NET Core routing with `@page "/route"` directives |

---

## Strangler Fig Application

During a strangler fig migration, Web Forms and Blazor Server can coexist by:

1. Keeping the legacy ASP.NET Web Forms app running on IIS.
2. Running the new Blazor Server app behind the YARP facade.
3. Migrating one page or user control at a time; routing that URL path to the new Blazor app.
4. Retiring legacy pages progressively until all traffic routes to Blazor.

---

## References

- Blazor for ASP.NET Web Forms developers (e-book): https://learn.microsoft.com/dotnet/architecture/blazor-for-web-forms-developers
- Migrate from ASP.NET Web Forms to Blazor: https://learn.microsoft.com/dotnet/architecture/blazor-for-web-forms-developers/migration
- Blazor hosting models: https://learn.microsoft.com/aspnet/core/blazor/hosting-models
- ASP.NET Core Blazor Server vs. WASM: see `/dotnet-architect` for target-state Blazor design decisions
