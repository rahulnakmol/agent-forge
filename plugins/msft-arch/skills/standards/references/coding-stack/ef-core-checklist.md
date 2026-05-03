# EF Core Checklist

**Applies to**: EF Core 8 and EF Core 9. Check each item before merging any data-access code.

> Async conventions (ConfigureAwait, CancellationToken propagation, no .Result/.Wait()) are governed by [csharp-standards.md](./csharp-standards.md).

---

## DbContext Lifetime

Register `DbContext` as **Scoped**: one instance per HTTP request (or unit of work). Never Singleton.

```csharp
// Correct
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString));

// Wrong: Singleton DbContext causes concurrency exceptions and connection leaks
services.AddSingleton<AppDbContext>(...);
```

For background services (hosted services, workers), use `IDbContextFactory<T>` to create short-lived contexts per operation:

```csharp
public class OrderSyncWorker(IDbContextFactory<AppDbContext> factory)
{
    public async Task RunAsync(CancellationToken ct)
    {
        await using var db = await factory.CreateDbContextAsync(ct);
        // ... work
    }
}
```

---

## Read-Only Queries: AsNoTracking

Add `.AsNoTracking()` on every query that does not produce entities you plan to update in the same DbContext scope. This eliminates change-tracker overhead and can halve memory usage on large result sets.

```csharp
var products = await db.Products
    .AsNoTracking()
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync(ct);
```

Use `.AsNoTrackingWithIdentityResolution()` when the result set has related entities that appear multiple times and you need object-graph deduplication without tracking.

---

## Projection Before Materialization

Never load full entities when you only need a subset of columns. Use `Select` to project before calling `ToListAsync()` or `FirstOrDefaultAsync()`:

```csharp
// Good: two columns, no change tracking needed
var summary = await db.Orders
    .AsNoTracking()
    .Where(o => o.Status == OrderStatus.Pending)
    .Select(o => new OrderSummary(o.Id, o.PlacedAt))
    .ToListAsync(ct);

// Bad: loads all columns including blobs
var orders = await db.Orders.Where(o => o.Status == OrderStatus.Pending).ToListAsync(ct);
```

---

## Include: Load Only What You Need

`Include` adds a JOIN. Every unnecessary `Include` widens the result set and increases latency.

Checklist:
- Include only navigation properties consumed in the current use case.
- Never chain more than 2–3 levels deep in a single query; consider separate queries instead.
- Use `.AsSplitQuery()` when loading collections to avoid Cartesian explosion (one large join → multiple smaller queries):

```csharp
var orders = await db.Orders
    .AsNoTracking()
    .Include(o => o.Lines)
    .Include(o => o.Customer)
    .AsSplitQuery()
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(ct);
```

Use `UseSplitQuery()` globally as the default if your queries routinely include collections. Revert to single-query when you need atomic snapshot semantics.

---

## Compiled Queries

For queries executed on every request (e.g., lookup-by-ID, tenant resolution), use compiled queries to avoid repeated LINQ-to-SQL translation:

```csharp
private static readonly Func<AppDbContext, Guid, Task<Customer?>> GetCustomerById =
    EF.CompileAsyncQuery((AppDbContext db, Guid id) =>
        db.Customers.AsNoTracking().FirstOrDefault(c => c.Id == id));

// Usage
var customer = await GetCustomerById(db, customerId);
```

Compiled queries cannot be parameterized with collections or complex predicates; use regular queries for those.

---

## Indexes

Define indexes in `OnModelCreating` or via data annotations. Never rely on EF to infer indexes beyond the primary key and foreign keys.

```csharp
// Data annotation
[Index(nameof(Email), IsUnique = true)]
public class Customer { ... }

// Fluent API: composite index
modelBuilder.Entity<Order>()
    .HasIndex(o => new { o.CustomerId, o.Status })
    .HasDatabaseName("IX_Orders_Customer_Status");
```

Review the generated migration for `CREATE INDEX` statements. Every foreign key that appears in a `WHERE` clause should have an index.

---

## Raw SQL: Safe Parameterization

Use `FromSqlInterpolated`; EF parameterizes the interpolated values automatically, preventing SQL injection:

```csharp
// Safe: EF creates @p0 parameter
var results = await db.Products
    .FromSqlInterpolated($"SELECT * FROM Products WHERE Category = {category}")
    .AsNoTracking()
    .ToListAsync(ct);
```

Never use `FromSqlRaw` with user-supplied strings without explicit parameterization via `SqlParameter`. Treat `FromSqlRaw` as a code-review red flag requiring justification.

---

## Connection Resilience

Enable retry-on-failure for transient SQL errors (network blips, Azure SQL throttling):

```csharp
options.UseSqlServer(connectionString, sqlOptions =>
    sqlOptions.EnableRetryOnFailure(
        maxRetryCount: 5,
        maxRetryDelay: TimeSpan.FromSeconds(30),
        errorNumbersToAdd: null));
```

Do not use `EnableRetryOnFailure` alongside explicit `DbContextTransaction`; retries are incompatible with manual transactions. Use `ExecutionStrategy` with an explicit retry block instead.

---

## Migration Workflow

1. Make model changes.
2. `dotnet ef migrations add <DescriptiveName> --project src/Infrastructure --startup-project src/Api`
3. Review the generated migration file; verify `Up()` and `Down()` are correct and idempotent.
4. Apply in CI with `dotnet ef database update` or via a migration bundle, not at application startup.
5. Never use `EnsureCreated()` in production; it bypasses migrations.
6. Keep `MigrationHistory` table in source control review. Squash migrations only at major version boundaries.

---

## EF Core 9: Features to Adopt

**Complex types** (value objects without identity): map types like `Address` or `Money` as complex types instead of owned entities. No surrogate key column is created:

```csharp
modelBuilder.Entity<Customer>().ComplexProperty(c => c.BillingAddress);
```

EF9 supports `GroupBy` and `ExecuteUpdate` on complex type properties.

**ExecuteUpdate / ExecuteDelete**: for bulk mutations, avoid loading entities:

```csharp
// No entity load, single UPDATE statement
await db.Orders
    .Where(o => o.Status == OrderStatus.Pending && o.PlacedAt < cutoff)
    .ExecuteUpdateAsync(s => s.SetProperty(o => o.Status, OrderStatus.Expired), ct);
```

**UseAzureSql / UseAzureSynapse**: use the specific method instead of `UseSqlServer` to unlock Azure-native SQL optimizations.

**Parameterized primitive collections**: EF9 defaults to parameterizing `Contains` on in-memory collections, improving query plan reuse. Use `EF.Constant(ids)` to force inlining when cardinality is low and stable.

---

## Bulk Operations

For imports exceeding ~500 rows, do not loop with `db.Add()`:

- Use `ExecuteUpdate` / `ExecuteDelete` for set-based changes.
- For inserts, use `BulkInsert` from the `EFCore.BulkExtensions` NuGet package (third-party; evaluate licensing for commercial projects) or `SqlBulkCopy` directly.
- Batch regular `SaveChanges` calls: process entities in chunks of 500–1000 and call `SaveChangesAsync` per chunk.

---

## Trade-offs and Exceptions

| Rule | When to break it |
|---|---|
| AsNoTracking everywhere | When the same DbContext scope both reads and then updates the entity; tracking is needed for change detection |
| Compiled queries | Low-frequency queries or those with dynamic predicates; compilation overhead exceeds savings |
| SplitQuery | When you need a consistent snapshot across tables (split queries use separate roundtrips) |
| ExecuteUpdate/Delete | When you need domain event side-effects; load entities and use `SaveChanges` to trigger interceptors |
| EnableRetryOnFailure | Serverless (Azure SQL Hyperscale, Cosmos DB) already has built-in retries; double-retry adds latency |
