# EF Core Deep Dive

This file covers advanced EF Core patterns not in the baseline checklist at `standards/references/coding-stack/ef-core-checklist.md`. Read the checklist first; it owns `AsNoTracking`, compiled queries basics, migration workflow, and `ExecuteUpdate`/`ExecuteDelete`. This file goes deeper on compiled query design, EF Core 9 complex types, `DbContext` pooling, interceptors, and multi-tenancy.

## Compiled Queries: Design Rules

The checklist introduces compiled queries. Here is when and how to design them well.

**When to use**: Any query executed more than once per process lifetime on a hot path: tenant resolution, per-request user lookups, permission checks, product catalogue reads. The EF Core LINQ-to-SQL translation happens once at the point `EF.CompileAsyncQuery` is called (typically as a static field), then the cached query plan is reused.

**Constraints**:
- Parameters must be primitive scalars or simple types. Collections and complex expressions cannot be parameterised in a compiled query; fall back to regular LINQ for those.
- The `DbContext` type is baked in. If you have a hierarchy of `DbContext` types, compile against the concrete type.
- Use `static readonly` at class scope: one compilation per type, shared across all instances.

```csharp
public class TenantRepository(AppDbContext db)
{
    // Compiled query: static readonly, compiled once
    private static readonly Func<AppDbContext, string, CancellationToken, Task<TenantConfig?>> GetBySlug =
        EF.CompileAsyncQuery((AppDbContext ctx, string slug, CancellationToken ct) =>
            ctx.Tenants
               .AsNoTracking()
               .Where(t => t.Slug == slug && t.IsActive)
               .Select(t => new TenantConfig(t.Id, t.Slug, t.SubscriptionTier))
               .FirstOrDefault());

    public Task<TenantConfig?> ResolveAsync(string slug, CancellationToken ct)
        => GetBySlug(db, slug, ct);
}
```

**Projected compiled queries**: Always project to a DTO inside the compiled query rather than returning full entities. This keeps the result set small and avoids change-tracker interaction.

**Parameterised collections**: If you need an `IN (...)` clause on a compiled hot path, EF Core 9 inlines the values by default (good for small, stable sets). Use `EF.Constant(ids)` to force inlining when you know the cardinality is fixed:

```csharp
// EF9: forces inlining of the ids array into the SQL, improving plan reuse
var statuses = EF.Constant(new[] { OrderStatus.Pending, OrderStatus.Processing });
var orders = await db.Orders.Where(o => statuses.Contains(o.Status)).ToListAsync(ct);
```

## EF Core 9: Complex Types

Complex types map a C# value object to a set of columns in the owning entity's table, without a surrogate key column. Use them for types like `Address`, `Money`, `GeoPoint`: types that have value semantics and no identity.

```csharp
// Value object: no Id property, value semantics
public record Address(string Street, string City, string PostalCode, string Country);

// Entity
public class Customer
{
    public Guid Id { get; set; }
    public required string Name { get; set; }
    public required Address BillingAddress { get; set; }
    public required Address ShippingAddress { get; set; }
}
```

Configuration in `OnModelCreating` or via a `IEntityTypeConfiguration<T>`:

```csharp
modelBuilder.Entity<Customer>(entity =>
{
    entity.ComplexProperty(c => c.BillingAddress, a =>
    {
        a.Property(x => x.Street).HasMaxLength(200);
        a.Property(x => x.PostalCode).HasMaxLength(20);
    });
    entity.ComplexProperty(c => c.ShippingAddress);
});
```

EF9 also supports `GroupBy` and `ExecuteUpdate` on complex type properties; you can update `BillingAddress.City` in a bulk statement without loading entities.

**When not to use**: If the value object appears in multiple entity types and you want it in its own table with a shared key (reference data, lookup tables), use an owned entity or a regular entity with a foreign key instead.

## DbContext Pooling

`DbContext` construction allocates. For high-throughput APIs where the overhead is measurable, enable context pooling. The pool recycles context instances between requests, resetting state rather than garbage-collecting and reallocating.

```csharp
// Replace AddDbContext with AddDbContextPool
services.AddDbContextPool<AppDbContext>(options =>
    options.UseNpgsql(connectionString), poolSize: 128);
```

Constraints on pooled contexts:
- The `DbContext` constructor must not perform work beyond setting up options. Pooled instances are reset via `ResetState()`; custom constructor logic does not re-run.
- Do not store request-scoped state (user ID, tenant ID) as a field on a pooled `DbContext`. Inject it via `IHttpContextAccessor` inside the method that needs it, or use a context factory with a custom `DbContext` subclass that accepts the tenant via an initialisation method.

For multi-tenant scenarios with per-tenant connection strings, use `IDbContextFactory<T>` with a factory that selects the connection string per-tenant rather than pooling:

```csharp
public class TenantDbContextFactory(IHttpContextAccessor http, IConfiguration config)
    : IDbContextFactory<AppDbContext>
{
    public AppDbContext CreateDbContext()
    {
        var tenantId = http.HttpContext!.User.FindFirst("tid")!.Value;
        var cs = config[$"Tenants:{tenantId}:ConnectionString"]!;
        var opts = new DbContextOptionsBuilder<AppDbContext>()
            .UseNpgsql(cs)
            .Options;
        return new AppDbContext(opts);
    }
}
```

## Interceptors

EF Core interceptors let you hook into the query pipeline without touching call sites. Common uses: soft-delete filtering, automatic `UpdatedAt` stamping, query logging, Azure SQL retry correlation.

```csharp
public class AuditInterceptor : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken ct)
    {
        var ctx = eventData.Context!;
        var now = DateTimeOffset.UtcNow;

        foreach (var entry in ctx.ChangeTracker.Entries<IAuditableEntity>())
        {
            if (entry.State == EntityState.Added)
                entry.Entity.CreatedAt = now;
            if (entry.State is EntityState.Added or EntityState.Modified)
                entry.Entity.UpdatedAt = now;
        }

        return base.SavingChangesAsync(eventData, result, ct);
    }
}
```

Register in `AddDbContext`:

```csharp
services.AddSingleton<AuditInterceptor>();
services.AddDbContext<AppDbContext>((sp, opts) =>
{
    opts.UseNpgsql(cs)
        .AddInterceptors(sp.GetRequiredService<AuditInterceptor>());
});
```

## Global Query Filters: Soft Deletes and Multi-Tenancy

Global query filters apply a `WHERE` clause to every query for an entity type. This is the right tool for soft deletes and tenant isolation.

```csharp
// In OnModelCreating
modelBuilder.Entity<Order>()
    .HasQueryFilter(o => !o.IsDeleted && o.TenantId == _currentTenantId);
```

The `_currentTenantId` value is resolved via a scoped service injected into the `DbContext` constructor. This is the primary reason the `DbContext` is scoped: it captures per-request context (tenant, user) at construction time.

To bypass the filter for admin or cross-tenant queries:

```csharp
var allTenantOrders = await db.Orders.IgnoreQueryFilters()
    .Where(o => o.Status == OrderStatus.Pending)
    .AsNoTracking()
    .ToListAsync(ct);
```

## Migration Workflow: Production Patterns

The checklist covers basic `dotnet ef migrations add`. For production systems:

**Migration bundles**: package the migration runner as a self-contained executable for CI deployment, avoiding a full SDK install on the build agent:

```bash
dotnet ef migrations bundle \
  --project src/Infrastructure \
  --startup-project src/Api \
  --output migrationbundle \
  --self-contained

# Deploy and run in CI
./migrationbundle --connection "..."
```

**Idempotent SQL scripts**: for teams that apply migrations via DBA-reviewed SQL scripts rather than the CLI tool:

```bash
dotnet ef migrations script --idempotent \
  --project src/Infrastructure \
  --startup-project src/Api \
  --output migrations.sql
```

**Squashing migrations**: only squash at major version boundaries where the entire team can coordinate a clean migration baseline. Squashing removes history and makes rollbacks harder in running production environments.

**Never `EnsureCreated` in production**: it creates the schema without migration history, making future `dotnet ef database update` commands fail. The only valid use of `EnsureCreated` is in test fixture setup where you want a throw-away schema.
