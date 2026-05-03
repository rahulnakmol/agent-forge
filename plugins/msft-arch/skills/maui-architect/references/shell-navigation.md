# .NET MAUI Shell Navigation

**Applies to**: .NET MAUI 9. Shell is the mandatory navigation pattern for new apps.

---

## Why Shell over NavigationPage

Shell provides:
- URL-based routing with `GoToAsync("//main/orders/detail?id=42")`
- Declarative tab bars, flyout menus, and nested navigation in one `AppShell.xaml`
- Deep-link support (iOS Universal Links, Android App Links) via the same URI scheme
- Visual Shell chrome (tab bar, flyout) controlled from a single file

`NavigationPage` remains available for backward compatibility with existing codebases. Do not start new navigation hierarchies with it.

## AppShell.xaml Structure

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<Shell
    x:Class="MyApp.AppShell"
    xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
    xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
    xmlns:views="clr-namespace:MyApp.Views">

    <!-- Flyout item (left-side drawer on mobile) -->
    <FlyoutItem Title="Catalog" Icon="catalog.png">
        <Tab Title="Browse">
            <ShellContent
                Title="Products"
                ContentTemplate="{DataTemplate views:ProductListPage}"
                Route="products" />
        </Tab>
        <Tab Title="Cart">
            <ShellContent
                Title="Cart"
                ContentTemplate="{DataTemplate views:CartPage}"
                Route="cart" />
        </Tab>
    </FlyoutItem>

    <!-- Tab bar item without flyout -->
    <TabBar>
        <ShellContent
            Title="Orders"
            Icon="orders.png"
            ContentTemplate="{DataTemplate views:OrderListPage}"
            Route="orders" />
        <ShellContent
            Title="Profile"
            Icon="profile.png"
            ContentTemplate="{DataTemplate views:ProfilePage}"
            Route="profile" />
    </TabBar>

</Shell>
```

## Route Registration for Non-Shell Pages

Pages not declared in `AppShell.xaml` (detail pages, modals) are registered via code:

```csharp
// In AppShell.xaml.cs constructor, or MauiProgram.cs before Shell is created
Routing.RegisterRoute("orders/detail", typeof(OrderDetailPage));
Routing.RegisterRoute("products/detail", typeof(ProductDetailPage));
```

Register all routes before navigation. Prefer lowercase, slash-separated URIs.

## Navigation from ViewModel

```csharp
// Navigate forward (pushes onto stack)
await Shell.Current.GoToAsync("orders/detail?orderId=abc123");

// Navigate back
await Shell.Current.GoToAsync("..");

// Navigate to absolute route (resets stack)
await Shell.Current.GoToAsync("//main/catalog");
```

Abstract `Shell.Current.GoToAsync` behind `INavigationService` for testability:

```csharp
public interface INavigationService
{
    Task NavigateToAsync(string route, IDictionary<string, object>? parameters = null);
    Task GoBackAsync();
}
```

Inject `INavigationService` into view models. Register the concrete implementation in `MauiProgram.cs`.

## Passing Parameters

Prefer `IDictionary<string, object>` parameter passing over query strings for complex objects:

```csharp
await Shell.Current.GoToAsync("orders/detail", new Dictionary<string, object>
{
    ["Order"] = selectedOrder   // passed by reference, no serialisation
});
```

Receive in the destination page view model using `[QueryProperty]`:

```csharp
public partial class OrderDetailViewModel : ObservableObject, IQueryAttributable
{
    [ObservableProperty]
    private Order? order;

    public void ApplyQueryAttributes(IDictionary<string, object> query)
    {
        if (query.TryGetValue("Order", out var o) && o is Order ord)
            Order = ord;
    }
}
```

Use `IQueryAttributable` for object passing; use `[QueryProperty]` only for primitive query string values.

## Deep Links

Configure deep links in platform manifests:
- **Android**: `IntentFilter` in `Platforms/Android/AndroidManifest.xml` with `android:scheme` and `android:host`
- **iOS**: `CFBundleURLTypes` in `Platforms/iOS/Info.plist` or Associated Domains for Universal Links

Shell resolves the URI to the registered route automatically when the app is launched from a deep link.

## Modal Navigation

```csharp
// Push modal
await Shell.Current.GoToAsync("payment", animate: true);

// Or: use built-in modal stack
await Shell.Current.Navigation.PushModalAsync(new PaymentPage());
```

Prefer Shell URI navigation even for modals. Reserve `PushModalAsync` for full-screen overlays not suited for URL routing (e.g., OS-controlled permission dialogs).

## Guards and Authentication Redirects

Implement `IShellNavigationObserver` or override `Shell.OnNavigating` to intercept navigation:

```csharp
protected override void OnNavigating(ShellNavigatingEventArgs args)
{
    base.OnNavigating(args);
    if (RequiresAuth(args.Target) && !_authService.IsAuthenticated)
    {
        args.Cancel();
        _ = GoToAsync("//login");
    }
}
```

## References

- Shell overview: `microsoft_docs_search ".NET MAUI Shell navigation overview"`
- Route registration: `microsoft_docs_search ".NET MAUI Shell route registration GoToAsync"`
- Deep links: `microsoft_docs_search ".NET MAUI deep linking Shell"`
