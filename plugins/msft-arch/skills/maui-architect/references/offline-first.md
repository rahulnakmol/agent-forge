# Offline-First Patterns for .NET MAUI

**Applies to**: .NET MAUI 9, sqlite-net-pcl, custom sync layer.

---

## Principle: Cloud as Cache

Design so the app works fully without a network connection. The local SQLite database is the source-of-truth for the device. The cloud sync layer reconciles changes when connectivity is restored. "Offline-first" is not optional for mobile; it is the default contract.

This principle applies where data ownership semantics allow it. Counter-examples: payment processing, real-time collaborative editing. Identify exceptions explicitly in the ADR.

## Package Reference

```xml
<PackageReference Include="sqlite-net-pcl" Version="1.9.*" />
<PackageReference Include="SQLitePCLRaw.bundle_green" Version="2.1.*" />
```

`SQLitePCLRaw.bundle_green` provides the native SQLite binaries for all MAUI platforms.

## Database Setup

```csharp
namespace MyApp.Data;

public class AppDatabase
{
    private readonly SQLiteAsyncConnection _connection;

    public AppDatabase(string dbPath)
    {
        _connection = new SQLiteAsyncConnection(dbPath);
    }

    public async Task InitialiseAsync()
    {
        await _connection.CreateTableAsync<Order>();
        await _connection.CreateTableAsync<OrderLine>();
        await _connection.CreateTableAsync<SyncLog>();
    }
}
```

Register as a singleton in `MauiProgram.cs`:

```csharp
var dbPath = Path.Combine(
    FileSystem.AppDataDirectory, "myapp.db3");

builder.Services.AddSingleton(_ => new AppDatabase(dbPath));
```

## Entity Design for Sync

Every entity that participates in sync must carry:

```csharp
[Table("Orders")]
public class Order
{
    [PrimaryKey]
    public Guid Id { get; set; } = Guid.NewGuid();

    public string CustomerName { get; set; } = string.Empty;
    public decimal Total { get; set; }

    // Sync metadata
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset UpdatedAt { get; set; }   // server timestamp from last sync
    public bool IsDirty { get; set; }               // true = has local changes not yet synced
    public bool IsDeleted { get; set; }             // soft delete for sync propagation
}
```

Use `Guid` primary keys to avoid ID collisions when records are created offline on multiple devices.

## Sync Layer Design

The sync service runs as a background service, triggered by:
1. App resume (foreground transition)
2. Connectivity restored event (`Connectivity.ConnectivityChanged`)
3. Explicit user pull-to-refresh

```csharp
public interface ISyncService
{
    Task SyncAsync(CancellationToken ct);
    event EventHandler<SyncCompletedEventArgs> SyncCompleted;
}

public class SyncService(AppDatabase db, IOrderApiClient api) : ISyncService
{
    public async Task SyncAsync(CancellationToken ct)
    {
        // 1. Push local dirty records to server
        var dirtyOrders = await db.GetDirtyOrdersAsync(ct);
        foreach (var order in dirtyOrders)
        {
            var result = await api.UpsertOrderAsync(order, ct);
            if (result.IsSuccess)
            {
                order.IsDirty = false;
                order.UpdatedAt = result.Value.UpdatedAt;
                await db.UpdateOrderAsync(order, ct);
            }
        }

        // 2. Pull server changes newer than last sync timestamp
        var lastSync = await db.GetLastSyncTimestampAsync(ct);
        var serverChanges = await api.GetOrdersModifiedAfterAsync(lastSync, ct);
        foreach (var change in serverChanges)
        {
            await db.UpsertOrderAsync(change, ct); // conflict resolution below
        }

        await db.SetLastSyncTimestampAsync(DateTimeOffset.UtcNow, ct);
        SyncCompleted?.Invoke(this, new SyncCompletedEventArgs(DateTimeOffset.UtcNow));
    }
}
```

## Conflict Resolution Strategy

| Strategy | When to Use |
|----------|------------|
| Last-write-wins (server timestamp) | Default: server timestamp beats local timestamp |
| Last-write-wins (client wins) | Client is authoritative (e.g., settings, preferences) |
| Merge | Fields are independent; merge field-by-field |
| User-prompted | High-value, irreversible mutations (e.g., financial records) |

Document the chosen strategy in the ADR. Last-write-wins (server) is the default unless domain rules require otherwise.

```csharp
private async Task UpsertWithConflictResolution(Order incoming, AppDatabase db)
{
    var existing = await db.FindOrderAsync(incoming.Id);
    if (existing is null)
    {
        await db.InsertOrderAsync(incoming);
        return;
    }

    // Last-write-wins: server timestamp wins
    if (incoming.UpdatedAt >= existing.UpdatedAt)
    {
        incoming.IsDirty = existing.IsDirty; // preserve dirty flag if local changes are newer
        await db.UpdateOrderAsync(incoming);
    }
    // else: local version is newer; leave it dirty for next push
}
```

## Connectivity Monitoring

```csharp
// In App.xaml.cs or a background service
Connectivity.ConnectivityChanged += async (_, args) =>
{
    if (args.NetworkAccess == NetworkAccess.Internet)
        await _syncService.SyncAsync(CancellationToken.None);
};
```

Use `Connectivity.Current.NetworkAccess` to gate all API calls. Never throw on no-network; queue the operation instead.

## Queuing Writes When Offline

```csharp
public async Task PlaceOrderAsync(Order order, CancellationToken ct)
{
    // Always write locally first
    order.IsDirty = true;
    await _db.InsertOrderAsync(order, ct);

    // Attempt sync only if online
    if (Connectivity.Current.NetworkAccess == NetworkAccess.Internet)
        await _syncService.SyncAsync(ct);
}
```

This pattern ensures the UI responds instantly, regardless of connectivity.

## References

- sqlite-net-pcl: `microsoft_docs_search ".NET MAUI local database SQLite sqlite-net-pcl"`
- Connectivity API: `microsoft_docs_search ".NET MAUI Connectivity NetworkAccess"`
- Sync patterns: `microsoft_docs_search "mobile offline sync Azure App Service delta sync"`
