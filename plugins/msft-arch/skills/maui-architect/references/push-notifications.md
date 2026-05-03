# Push Notifications via Azure Notification Hubs

**Applies to**: .NET MAUI 9, Azure Notification Hubs, APNs (iOS/macOS), FCM v1 (Android), WNS (Windows).

---

## Principle: Single Hub, Multi-Platform Fan-Out

Azure Notification Hubs abstracts APNs, FCM v1, and WNS behind a single SDK and a single backend call. Do not integrate APNs or FCM directly into the MAUI app. Always route through a Notification Hub.

Benefits:
- One registration model across all platforms (device installation with tags).
- One backend API call sends to thousands of devices across platforms.
- Tag-based targeting: send to `user:abc123`, `segment:premium`, or broadcast.
- Template support for per-language/per-platform message customisation.

## Architecture

```
MAUI App (iOS/Android/Windows)
    |
    | 1. Get PNS token (APNs, FCM, WNS)
    | 2. Register token + tags with backend API
    v
Backend API (ASP.NET Core)
    |
    | 3. Upsert device installation in Notification Hub
    v
Azure Notification Hub
    |
    | 4. Fan-out to APNs / FCM v1 / WNS
    v
Device (delivers notification)
```

The MAUI app never calls the Notification Hub directly. The backend API owns hub credentials.

## Backend NuGet Package

```xml
<PackageReference Include="Microsoft.Azure.NotificationHubs" Version="4.*" />
```

## MAUI App: Platform Registration

### Interface (cross-platform, in `Services/`)

```csharp
public interface IDeviceInstallationService
{
    string? Token { get; set; }
    bool NotificationsSupported { get; }
    string GetDeviceId();
    DeviceInstallation? GetDeviceInstallation(params string[] tags);
}

public record DeviceInstallation(
    string InstallationId,
    string Platform,
    string PushChannel,
    string[] Tags);
```

### iOS Implementation (`Platforms/iOS/DeviceInstallationService.cs`)

```csharp
public class DeviceInstallationService : IDeviceInstallationService
{
    public string? Token { get; set; }
    public bool NotificationsSupported => UIDevice.CurrentDevice.CheckSystemVersion(10, 0);

    public string GetDeviceId() =>
        UIDevice.CurrentDevice.IdentifierForVendor?.ToString()
        ?? throw new InvalidOperationException("Cannot retrieve device ID on iOS.");

    public DeviceInstallation? GetDeviceInstallation(params string[] tags)
    {
        if (!NotificationsSupported || string.IsNullOrWhiteSpace(Token))
            return null;

        return new DeviceInstallation(
            GetDeviceId(), "apns", Token, tags);
    }
}
```

### Android Implementation (`Platforms/Android/DeviceInstallationService.cs`)

```csharp
public class DeviceInstallationService : IDeviceInstallationService
{
    public string? Token { get; set; }
    public bool NotificationsSupported => true;

    public string GetDeviceId() =>
        Settings.Secure.GetString(
            Android.App.Application.Context.ContentResolver,
            Settings.Secure.AndroidId)
        ?? throw new InvalidOperationException("Cannot retrieve device ID on Android.");

    public DeviceInstallation? GetDeviceInstallation(params string[] tags)
    {
        if (string.IsNullOrWhiteSpace(Token))
            return null;

        return new DeviceInstallation(
            GetDeviceId(), "fcmv1", Token, tags);
    }
}
```

### iOS AppDelegate: APNs Registration

```csharp
// Platforms/iOS/AppDelegate.cs
public override void RegisteredForRemoteNotifications(
    UIApplication application, NSData deviceToken)
{
    // Convert NSData token to hex string
    var token = string.Concat(
        deviceToken.ToArray().Select(b => b.ToString("x2")));

    _deviceInstallationService.Token = token;
    _ = _notificationRegistrationService.RefreshRegistrationAsync();
}
```

Request permission in `FinishedLaunching`:

```csharp
UNUserNotificationCenter.Current.RequestAuthorization(
    UNAuthorizationOptions.Alert | UNAuthorizationOptions.Badge | UNAuthorizationOptions.Sound,
    (granted, error) =>
    {
        if (granted)
            UIApplication.SharedApplication.RegisterForRemoteNotifications();
    });
```

## Backend API: Registration Endpoint

```csharp
[ApiController]
[Route("api/notifications")]
public class NotificationsController(INotificationHubClient hub) : ControllerBase
{
    [HttpPost("installations")]
    public async Task<IActionResult> RegisterDevice(
        [FromBody] DeviceInstallationRequest request,
        CancellationToken ct)
    {
        var installation = new Installation
        {
            InstallationId = request.InstallationId,
            Platform = request.Platform switch
            {
                "apns"   => NotificationPlatform.Apns,
                "fcmv1"  => NotificationPlatform.FcmV1,
                "wns"    => NotificationPlatform.Wns,
                _        => throw new ArgumentException("Unknown platform")
            },
            PushChannel = request.PushChannel,
            Tags = request.Tags
        };

        await hub.CreateOrUpdateInstallationAsync(installation, ct);
        return NoContent();
    }

    [HttpPost("send")]
    public async Task<IActionResult> SendNotification(
        [FromBody] SendNotificationRequest request,
        CancellationToken ct)
    {
        // Tag expression targeting: e.g., "user:abc123 && segment:premium"
        await hub.SendNotificationAsync(
            new TemplateNotification(request.Properties),
            request.TagExpression,
            ct);
        return Accepted();
    }
}
```

## Notification Hub Configuration

Configure APNs and FCM v1 in the Azure portal before testing:
- **APNs**: Use token-based authentication (`.p8` key + Key ID + Team ID). Prefer token over `.p12` certificate (tokens do not expire annually).
- **FCM v1**: Upload the service account JSON private key from Firebase project settings.
- **WNS**: Package SID + Client Secret from Windows Dev Center.

Store hub connection string in Key Vault. Inject `INotificationHubClient` via:

```csharp
builder.Services.AddSingleton<INotificationHubClient>(
    NotificationHubClient.CreateClientFromConnectionString(
        config["NotificationHub:ConnectionString"],
        config["NotificationHub:Name"]));
```

## Tags and Targeting

| Pattern | Tag Example | Use Case |
|---------|-------------|----------|
| User-specific | `user:abc123` | Send to one user's all devices |
| Segment | `segment:premium` | Broadcast to a cohort |
| Locale | `locale:en-AU` | Localised campaigns |
| Broadcast | (no tag expression) | All registered devices |

Tags are set at device registration time by the backend service. The MAUI app passes requested tags in the registration payload.

## References

- Push notifications tutorial: `microsoft_docs_search "Send push notifications .NET MAUI Azure Notification Hubs backend service"`
- APNs token auth: `microsoft_docs_search "Azure Notification Hubs APNs token-based authentication"`
- FCM v1 migration: `microsoft_docs_search "Azure Notification Hubs FCM v1 migration"`
