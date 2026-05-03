# .NET Testing Strategy

The test pyramid for a .NET service has four layers. Invest in unit tests first, integration tests second, and use snapshot and mutation testing to close the gaps that typical assertion-based tests miss.

## The Pyramid

```text
                    /\
                   /  \
                  / E2E \          ← Few; exercise deployed system
                 /--------\
                / Contract  \      ← Per-service boundary; Pact or manual
               /------------\
              / Integration   \    ← WebApplicationFactory; full HTTP pipeline
             /----------------\
            /   Unit Tests      \  ← The bulk; no I/O; fast
           /--------------------\
```

**Unit tests**: Pure logic, domain rules, service methods. Inject test doubles (NSubstitute preferred over Moq: cleaner syntax, fewer setup pitfalls). No EF Core, no HTTP client, no file system.

**Integration tests**: The full ASP.NET Core request pipeline via `WebApplicationFactory`. Real EF Core queries against a Testcontainers database, or an in-memory provider for CRUD paths where SQL semantics are not under test. One `WebApplicationFactory<Program>` per test class or test collection.

**Contract tests**: When a Minimal API is consumed by other services, verify the contract hasn't broken with consumer-driven contract testing (Pact.NET) or a build-time OpenAPI diff.

**E2E tests**: Browser-level via Playwright for Blazor UIs. Limit to critical paths: login, checkout, order submit. Expensive to maintain; run in CI nightly, not on every commit.

## xUnit Conventions

```csharp
// Unit test: no async setup needed; synchronous is fine
public class OrderServiceTests
{
    private readonly IOrderRepository _repo = Substitute.For<IOrderRepository>();
    private readonly OrderService _sut;

    public OrderServiceTests() => _sut = new OrderService(_repo);

    [Fact]
    public async Task PlaceOrder_ReturnsFailure_WhenNoLines()
    {
        var cmd = new CreateOrderCommand { CustomerId = Guid.NewGuid(), Lines = [] };

        var result = await _sut.PlaceAsync(cmd, CancellationToken.None);

        result.IsFailed.Should().BeTrue();
        result.Errors.Should().ContainSingle(e => e.Message.Contains("at least one line"));
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task PlaceOrder_ReturnsFailure_WhenQuantityInvalid(int qty)
    {
        var cmd = new CreateOrderCommand
        {
            CustomerId = Guid.NewGuid(),
            Lines = [new OrderLine(Guid.NewGuid(), qty, 10m)]
        };

        var result = await _sut.PlaceAsync(cmd, CancellationToken.None);

        result.IsFailed.Should().BeTrue();
    }
}
```

Use `IAsyncLifetime` for async fixture setup:

```csharp
public class OrderRepositoryTests : IAsyncLifetime
{
    private AppDbContext _db = null!;

    public async Task InitializeAsync()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        _db = new AppDbContext(options);
        await _db.Database.EnsureCreatedAsync();
    }

    public async Task DisposeAsync() => await _db.DisposeAsync();
}
```

## WebApplicationFactory: Integration Tests

`WebApplicationFactory<Program>` boots the real application in-process. Override `ConfigureWebHost` to swap out infrastructure (database, external services, identity) for test doubles.

```csharp
public class OrdersApiFactory : WebApplicationFactory<Program>
{
    public string ConnectionString { get; private set; } = null!;
    private PostgreSqlContainer _container = null!;

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureTestServices(services =>
        {
            // Replace real DbContext with test database
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.AddDbContext<AppDbContext>(opts =>
                opts.UseNpgsql(ConnectionString));

            // Stub external HTTP dependencies
            services.AddSingleton<IPaymentGateway>(_ =>
                Substitute.For<IPaymentGateway>());
        });
    }

    public async Task InitializeAsync()
    {
        _container = new PostgreSqlBuilder().Build();
        await _container.StartAsync();
        ConnectionString = _container.GetConnectionString();

        // Run migrations against the test DB
        using var scope = Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        await db.Database.MigrateAsync();
    }

    public new async Task DisposeAsync()
    {
        await base.DisposeAsync();
        await _container.DisposeAsync();
    }
}
```

Test class:

```csharp
public class CreateOrderTests(OrdersApiFactory factory)
    : IClassFixture<OrdersApiFactory>
{
    [Fact]
    public async Task Post_Orders_Returns201_WithValidRequest()
    {
        var client = factory.CreateClient();
        var request = new CreateOrderRequest
        {
            CustomerId = Guid.NewGuid(),
            Lines = [new OrderLineRequest(Guid.NewGuid(), 2, 19.99m)]
        };

        var response = await client.PostAsJsonAsync("/orders", request);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        response.Headers.Location.Should().NotBeNull();
    }
}
```

## Testcontainers

Use Testcontainers for integration tests that exercise real SQL semantics (indexes, transactions, JSON operators). The in-memory EF Core provider does not support raw SQL, window functions, or Azure SQL-specific types.

```bash
dotnet add package Testcontainers.PostgreSql
dotnet add package Testcontainers.MsSql
dotnet add package Testcontainers.Redis
```

Testcontainers pulls the Docker image on first run and reuses it across the test session. Keep one `WebApplicationFactory` per test collection; starting a fresh container per test class is expensive.

## Verify: Snapshot Testing

Verify captures the output of a method as a `.verified.txt` (or `.verified.json`, `.verified.html`) file and fails on any diff from the approved snapshot. It is ideal for:
- API response shapes
- Complex serialisation output
- Blazor component render output

```csharp
[Fact]
public async Task GetOrder_MatchesSnapshot()
{
    var client = factory.CreateClient();

    var response = await client.GetFromJsonAsync<OrderDetail>("/orders/seed-id-1");

    await Verify(response);
}
```

On first run, Verify creates `GetOrder_MatchesSnapshot.verified.json`. Review the file, commit it. Subsequent runs fail if the output changes. Approve intentional changes with `dotnet verify accept` or by updating the verified file.

## FluentAssertions

Prefer FluentAssertions over raw `Assert.*`; it produces human-readable failure messages and supports rich object graph comparison.

```csharp
// Raw xUnit: poor failure message
Assert.Equal(OrderStatus.Pending, order.Status);

// FluentAssertions: self-documenting failure
order.Status.Should().Be(OrderStatus.Pending);
order.Lines.Should().HaveCount(2)
    .And.AllSatisfy(l => l.Quantity.Should().BePositive());
```

For collection assertions use `BeEquivalentTo` for unordered comparison and `Equal` for ordered:

```csharp
result.Should().BeEquivalentTo(
    expected,
    options => options.Excluding(x => x.UpdatedAt));
```

## Mutation Testing (Intro)

Mutation testing verifies that your tests actually catch regressions. Stryker.NET introduces small changes (mutations) into the production code and reports which mutations were killed (caught by a test) vs. survived (test suite missed it).

```bash
dotnet tool install --global dotnet-stryker
dotnet stryker --project src/Orders.Application/Orders.Application.csproj
```

A mutation score above 80% is a reasonable target for application-layer logic. Run Stryker against the domain and application layers on a cadence (weekly or before major releases), not on every commit; it is CPU-intensive.

Survivors indicate untested branches. Add tests to kill them, or accept them with a `[ExcludeFromCodeCoverage]` annotation and a justification comment if the branch is unreachable in practice.
