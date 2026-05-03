# .NET MAUI Blazor Hybrid

**Applies to**: .NET MAUI 9, ASP.NET Core 9, CommunityToolkit.Mvvm 8.x.

---

## Decision Gate: 70% Reuse Rule

Adopt Blazor Hybrid only when 70% or more of the app's UI can be shared with an existing or planned web app. Measure by screen count or component count. Below that threshold, native MAUI XAML delivers better performance, platform-native feel, and simpler debugging.

Document the reuse estimate explicitly in the ADR before committing to Blazor Hybrid.

## Architecture: Three-Project Solution

```
Solution
  MyApp.Shared     (Razor Class Library: all shared Razor components)
  MyApp.Web        (Blazor Web App: references MyApp.Shared)
  MyApp.Mobile     (.NET MAUI app: references MyApp.Shared, hosts BlazorWebView)
```

The `MyApp.Shared` RCL is platform-agnostic. It must not reference MAUI APIs directly. Platform-specific capabilities (file access, push token, biometrics) are provided via DI interfaces.

Create the solution from the official template:

```bash
dotnet new maui-blazor-web -o MyApp -I Server
```

Replace `Server` with `WebAssembly` or `Auto` depending on the desired Blazor render mode for the web project.

## BlazorWebView in MAUI

In the MAUI project's main page:

```xaml
<ContentPage xmlns:bwv="clr-namespace:Microsoft.AspNetCore.Components.WebView.Maui;assembly=Microsoft.AspNetCore.Components.WebView.Maui">
    <bwv:BlazorWebView HostPage="wwwroot/index.html">
        <bwv:BlazorWebView.RootComponents>
            <bwv:RootComponent Selector="#app" ComponentType="{x:Type shared:App}" />
        </bwv:BlazorWebView.RootComponents>
    </bwv:BlazorWebView>
</ContentPage>
```

`HostPage` points to `wwwroot/index.html` in the MAUI project. Static web assets (CSS, JS) live in `wwwroot/`.

## MauiProgram.cs Registration

```csharp
builder.Services.AddMauiBlazorWebView();

#if DEBUG
builder.Services.AddBlazorWebViewDeveloperTools();
#endif

// Register the platform-specific service implementations
builder.Services.AddSingleton<IDeviceService, MauiDeviceService>();

// Register shared services (same interfaces as web project)
builder.Services.AddSingleton<IOrderService, OrderService>();
```

## Platform Interfaces for DI

Shared components that need platform capabilities declare interfaces in `MyApp.Shared`:

```csharp
// In MyApp.Shared/Services/IDeviceService.cs
public interface IDeviceService
{
    string GetDeviceId();
    Task<string?> GetPushTokenAsync();
}
```

MAUI project implements with native APIs in `Services/MauiDeviceService.cs`:

```csharp
public class MauiDeviceService : IDeviceService
{
    public string GetDeviceId() => DeviceInfo.Current.Idiom.ToString();
    public Task<string?> GetPushTokenAsync() => /* platform token retrieval */;
}
```

Web project implements with web-specific logic or stubs. The shared Razor components receive `IDeviceService` via `@inject` without knowing the runtime platform.

## Browser Engine Differences

| Platform | Engine | Key Consideration |
|----------|--------|-------------------|
| Windows | WebView2 (Chromium/Edge) | Modern web standards; update via Windows Update |
| Android | `android.webkit.WebView` (Chromium) | Version depends on system component; test on API 24+ |
| iOS | `WKWebView` (WebKit/Safari) | Same engine as Safari; CSS and JS compatibility differs from Chromium |
| macOS | `WKWebView` (WebKit) | Same as iOS; test CSS grid and flexbox separately |

Test on all four platforms before finalising CSS. Avoid CSS that is Chromium-only.

## When NOT to Use BlazorWebView

- Native gestures (swipe-to-delete, pinch-to-zoom on custom controls): use MAUI XAML controls.
- Pixel-perfect platform-native navigation chrome: Shell + native pages.
- Performance-critical list views (large data sets): `CollectionView` with native handlers outperforms web-rendered tables.
- Anything requiring direct access to platform-native UI APIs: partial classes in `Platforms/` with native MAUI views.

## HybridWebView (Non-Blazor HTML/JS)

For React, Vue, or Angular apps embedded in MAUI, use `HybridWebView` (new in .NET MAUI 9) rather than `BlazorWebView`. `HybridWebView` does not require Razor components; it hosts arbitrary HTML/JS/CSS packaged in `wwwroot/`:

```xaml
<HybridWebView DefaultFile="index.html" HybridAssetRoot="wwwroot" />
```

C# and JavaScript communicate via `InvokeJavaScriptAsync` and `SendRawMessageToCSharpAsync`.

## References

- Blazor Hybrid with MAUI: `microsoft_docs_search "ASP.NET Core Blazor Hybrid .NET MAUI BlazorWebView"`
- MAUI Blazor Web solution template: `microsoft_docs_search ".NET MAUI Blazor Hybrid and Web App solution template maui-blazor-web"`
- RCL host-agnostic design: `microsoft_docs_search "Blazor Hybrid Razor class library host-agnostic best practices"`
