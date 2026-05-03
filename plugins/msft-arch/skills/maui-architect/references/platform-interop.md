# .NET MAUI Platform Interop

**Applies to**: .NET MAUI 9. Native APIs via `Platforms/<platform>/` partial classes.

---

## Principle: Single Project, Isolated Platform Code

All cross-platform code lives in the root project. Platform-specific code lives exclusively in `Platforms/<platform>/`. Never scatter `#if ANDROID` / `#if IOS` blocks through shared view models or services.

```
MyApp/
  Services/
    IDeviceOrientationService.cs     // cross-platform interface
  Platforms/
    Android/
      DeviceOrientationService.cs    // Android implementation
    iOS/
      DeviceOrientationService.cs    // iOS implementation
    MacCatalyst/
      DeviceOrientationService.cs    // macOS implementation
    Windows/
      DeviceOrientationService.cs    // Windows implementation
```

## Pattern 1: Partial Classes and Methods (Preferred)

Define the cross-platform API in a shared partial class; implement per platform in the `Platforms/` folder.

**Shared** (`Services/DeviceOrientationService.cs`):

```csharp
namespace MyApp.Services;

public partial class DeviceOrientationService
{
    public partial DeviceOrientation GetOrientation();
}
```

**Android** (`Platforms/Android/DeviceOrientationService.cs`):

```csharp
namespace MyApp.Services;

public partial class DeviceOrientationService
{
    public partial DeviceOrientation GetOrientation()
    {
        var rotation = Platform.CurrentActivity?
            .WindowManager?.DefaultDisplay?.Rotation;
        return rotation switch
        {
            SurfaceOrientation.Rotation90 or SurfaceOrientation.Rotation270
                => DeviceOrientation.Landscape,
            _ => DeviceOrientation.Portrait
        };
    }
}
```

**iOS / Mac Catalyst** (`Platforms/iOS/DeviceOrientationService.cs`):

```csharp
namespace MyApp.Services;

public partial class DeviceOrientationService
{
    public partial DeviceOrientation GetOrientation()
    {
        return UIDevice.CurrentDevice.Orientation.IsLandscape()
            ? DeviceOrientation.Landscape
            : DeviceOrientation.Portrait;
    }
}
```

The build system includes only the correct `Platforms/<platform>/` files for each target.

## Pattern 2: Interface + DI (Recommended for Testability)

When the implementation requires injected dependencies or async operations, use an interface:

**Interface** (`Services/ISecureCredentialService.cs`):

```csharp
public interface ISecureCredentialService
{
    Task<string?> GetTokenAsync(string key, CancellationToken ct);
    Task SetTokenAsync(string key, string value, CancellationToken ct);
    Task RemoveTokenAsync(string key, CancellationToken ct);
}
```

**Shared implementation** (`Services/SecureCredentialService.cs`): Use `SecureStorage` (MAUI abstraction, available on all platforms):

```csharp
public class SecureCredentialService : ISecureCredentialService
{
    public Task<string?> GetTokenAsync(string key, CancellationToken ct) =>
        SecureStorage.Default.GetAsync(key);

    public Task SetTokenAsync(string key, string value, CancellationToken ct) =>
        SecureStorage.Default.SetAsync(key, value);

    public Task RemoveTokenAsync(string key, CancellationToken ct)
    {
        SecureStorage.Default.Remove(key);
        return Task.CompletedTask;
    }
}
```

Use platform-specific implementations only when MAUI's cross-platform abstraction is insufficient.

## MAUI Essentials: Cross-Platform Abstractions First

Before writing platform-specific interop, check whether MAUI Essentials already covers the use case:

| Need | MAUI Essentials API |
|------|---------------------|
| Device info (model, OS) | `DeviceInfo.Current` |
| Secure token storage | `SecureStorage.Default` |
| Connectivity | `Connectivity.Current` |
| File system paths | `FileSystem.AppDataDirectory`, `FileSystem.CacheDirectory` |
| Geolocation | `Geolocation.Default` |
| Permissions | `Permissions.RequestAsync<T>()` |
| Vibration, haptics | `Vibration.Default`, `HapticFeedback.Default` |
| App theme (light/dark) | `Application.Current.RequestedTheme` |
| Browser | `Browser.Default.OpenAsync(url)` |
| Share sheet | `Share.Default.RequestAsync(...)` |

Only write `Platforms/` code for capabilities not covered by MAUI Essentials.

## Handler Customisation

To customise the native rendering of a MAUI control without subclassing, use handler mapper overrides in `MauiProgram.cs`:

```csharp
builder.ConfigureMauiHandlers(handlers =>
{
    handlers.AddHandler<Entry, CustomEntryHandler>();
});

// Or: global mapper for a control type
EntryHandler.Mapper.AppendToMapping(nameof(IEntry.IsEnabled), (handler, view) =>
{
    // Android: customise handler.PlatformView (AppCompatEditText)
    // iOS: customise handler.PlatformView (UITextField)
});
```

Handler customisation is the MAUI-idiomatic replacement for Xamarin.Forms Custom Renderers.

## Native View Embedding

To embed a fully native platform view inside a MAUI layout:

```csharp
// In a MAUI ContentView subclass
var nativeView = new ContentView();
nativeView.Content = new NativeViewWrapper(platformView);
```

Use `NativeViewWrapperRenderer` or the `ToPlatform()` extension method. Reserved for controls that have no MAUI equivalent and where Essentials/handlers are insufficient.

## Accessing Platform Context

| Platform | Accessor |
|----------|----------|
| Android Activity | `Platform.CurrentActivity` |
| iOS View Controller | `Platform.GetCurrentUIViewController()` |
| Windows Window | `(Application.Current.Windows[0].Handler.PlatformView as MauiWinUIWindow)` |

Access platform context only inside `Platforms/` files.

## Conditional Compilation: Rules

- `#if ANDROID`, `#if IOS`, `#if MACCATALYST`, `#if WINDOWS` are permitted only inside `Platforms/` folders.
- Never use conditional compilation in shared `ViewModels/`, `Services/` (shared), or `Views/`.
- Use runtime checks (`DeviceInfo.Current.Platform`) only for minor UI tweaks (e.g., padding adjustments) in XAML converters.

## References

- Invoke platform code: `microsoft_docs_search ".NET MAUI invoke platform code partial classes Platforms folder"`
- Handler architecture: `microsoft_docs_search ".NET MAUI handlers mapper customisation"`
- MAUI Essentials: `microsoft_docs_search ".NET MAUI Essentials cross-platform APIs"`
