# EF6 to EF Core Migration

**Applies to**: Projects using `EntityFramework 6.x` (NuGet) targeting migration to EF Core 8/9.

**Principle**: EF6 to EF Core: migration is not always 1:1: review LINQ queries, lazy loading, transaction scopes.

> For EF Core coding patterns (AsNoTracking, compiled queries, migration workflow), see `standards/references/coding-stack/ef-core-checklist.md`. This reference covers the delta: what changes when moving FROM EF6.

---

## EF6 vs. EF Core: Critical Differences

| Area | EF6 | EF Core |
|---|---|---|
| Lazy loading | On by default | Off by default; opt-in via `UseLazyLoadingProxies()` |
| EDMX / Designer | Supported | Not supported: code-first only |
| EntitySQL | Supported | Not supported: use LINQ or `FromSqlInterpolated` |
| Connection strings | Multiple constructor overloads | `DbContextOptions` only |
| Data validation | Built into SaveChanges | Not supported: use FluentValidation or DataAnnotations at the API layer |
| Change tracker mutations | Properties | Backing fields by default |
| Orphan handling | Preserved | Deleted |
| `Database.ExecuteSqlCommand` | Supported | Replaced by `ExecuteSqlAsync` / `ExecuteUpdate` / `ExecuteDelete` |
| `ObjectContext` | Supported | Removed: `DbContext` only |
| Stored procedure support | Full (EDMX mapping) | `FromSqlInterpolated` + manual mapping |

---

## Migration Checklist

### 1. Remove EDMX, switch to code-first

EF6 EDMX-based models must be converted to code-first:
- Scaffold an initial code-first model from the existing database using `dotnet ef dbcontext scaffold`.
- Review the generated entity configuration; entity relationships may differ from EDMX mapping.
- Discard `.edmx`, `.tt`, and `.Designer.cs` files after conversion.

### 2. Replace `DbContext` registration

EF6 (Global.asax / Unity / Autofac):
```csharp
// EF6: connection string constructor
public class AppDbContext : DbContext
{
    public AppDbContext() : base("DefaultConnection") { }
}
```

EF Core (Program.cs, .NET 8/9):
```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection"),
        sqlOptions => sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 5,
            maxRetryDelay: TimeSpan.FromSeconds(30),
            errorNumbersToAdd: null)));
```

Use `UseAzureSql` instead of `UseSqlServer` when targeting Azure SQL Database for Azure-native optimisations.

### 3. Audit lazy loading usage

EF6 enables lazy loading by default; EF Core disables it. Code that relies on lazy navigation property access will produce `null` or empty collections silently in EF Core without the proxies package.

Audit pattern:
```csharp
// EF6: this works silently (lazy load triggered on Orders access)
var customer = db.Customers.Find(id);
var count = customer.Orders.Count; // N+1 hidden here

// EF Core without lazy loading: Orders is null unless explicitly loaded
// Fix: use eager loading
var customer = await db.Customers
    .Include(c => c.Orders)
    .AsNoTracking()
    .FirstOrDefaultAsync(c => c.Id == id, ct);
```

If lazy loading is needed during migration (to reduce N+1 audit scope), opt in explicitly:
```csharp
options.UseLazyLoadingProxies();
// AND install: Microsoft.EntityFrameworkCore.Proxies
```

Disable lazy loading as soon as eager/explicit loading has been audited. Lazy loading is a migration crutch, not a target state.

### 4. Review LINQ queries

EF Core evaluates LINQ differently from EF6. Common issues:

- **Client-side evaluation**: EF6 silently fell back to client evaluation for unsupported LINQ operators. EF Core throws by default (`ConfigureWarnings(...Throw(RelationalEventId.QueryClientEvaluationWarning))`). Every LINQ expression must be translatable to SQL.
- **GroupBy**: EF6 had limited GroupBy SQL translation. EF Core 2.1+ supports GroupBy; verify complex GroupBy expressions still produce the expected SQL.
- **String methods**: `string.IsNullOrEmpty(x.Name)` maps correctly in EF Core; `string.IsNullOrWhiteSpace` may not. Test each.
- **Custom functions**: EF6 custom database functions registered via `[DbFunction]` attributes must be re-registered in EF Core's `HasDbFunction` model configuration.

### 5. Migrate transaction scopes

EF6 `TransactionScope` usage must be reviewed:

```csharp
// EF6 pattern (avoid in EF Core when using connection resilience)
using (var scope = new TransactionScope())
{
    // ...
    scope.Complete();
}
```

EF Core provides its own transaction API and `EnableRetryOnFailure` is incompatible with `TransactionScope`. Use the EF Core execution strategy instead:

```csharp
var strategy = db.Database.CreateExecutionStrategy();
await strategy.ExecuteAsync(async () =>
{
    await using var tx = await db.Database.BeginTransactionAsync(ct);
    // ... operations
    await tx.CommitAsync(ct);
});
```

### 6. Migrate initializers and seed data

EF6 database initializers (`DropCreateDatabaseIfModelChanges`, `MigrateDatabaseToLatestVersion`) do not exist in EF Core. Use:

- `dotnet ef migrations add InitialCreate` to create the initial migration.
- `dotnet ef database update` (or migration bundles) in CI to apply migrations; never `EnsureCreated()` in production.
- `HasData()` in `OnModelCreating` for seed data.

### 7. Scaffolding an initial EF Core migration from the existing schema

When the existing database schema is the source of truth:

```dotnetcli
dotnet ef dbcontext scaffold "Server=...;Database=...;..." Microsoft.EntityFrameworkCore.SqlServer \
    --output-dir Infrastructure/Persistence/Entities \
    --context AppDbContext \
    --no-onconfiguring \
    --project src/Infrastructure \
    --startup-project src/Api
```

Review every generated entity: navigation properties, shadow properties, and cascade delete settings differ from EF6 defaults.

---

## Namespace and Package Changes

| EF6 | EF Core 8/9 |
|---|---|
| `System.Data.Entity` | `Microsoft.EntityFrameworkCore` |
| `System.Data.Entity.Infrastructure` | `Microsoft.EntityFrameworkCore.Infrastructure` |
| `EntityFramework` (NuGet) | `Microsoft.EntityFrameworkCore` + provider (e.g., `Microsoft.EntityFrameworkCore.SqlServer`) |
| `EntityFramework.SqlServer` | `Microsoft.EntityFrameworkCore.SqlServer` |

---

## Side-by-Side Running (During Strangler Fig Transition)

It is valid to run EF6 and EF Core in the same solution during the strangler fig transition. Use namespace aliases to avoid ambiguity:

```csharp
using Microsoft.EntityFrameworkCore; // EF Core DbContext
using EF6 = System.Data.Entity;      // EF6 DbContext
```

Isolate the two contexts in separate assemblies (e.g., `Legacy.Infrastructure` vs. `App.Infrastructure`) to prevent cross-contamination.

---

## References

- EF6 vs. EF Core comparison: https://learn.microsoft.com/ef/efcore-and-ef6/
- Porting from EF6 to EF Core: https://learn.microsoft.com/ef/efcore-and-ef6/porting/
- Detailed porting cases: https://learn.microsoft.com/ef/efcore-and-ef6/porting/port-detailed-cases
- EF Core checklist: `standards/references/coding-stack/ef-core-checklist.md`
