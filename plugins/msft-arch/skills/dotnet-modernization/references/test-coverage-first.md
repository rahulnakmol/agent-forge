# Test Coverage First

**Applies to**: Any .NET Framework codebase before migration work begins.

**Principle**: Test coverage on legacy code first: modernization without tests is rewriting blind.

---

## Why Tests Must Precede Migration

A migration that runs without tests has no automated way to detect regressions introduced by:
- TFM change (from `net4x` to `net8.0`)
- Dependency replacement (EF6 to EF Core, WCF to gRPC, `System.Web` to ASP.NET Core)
- Behavioural differences in EF Core lazy loading, LINQ evaluation, or `TransactionScope` handling
- Configuration system changes (`web.config` to `appsettings.json`)

Even a "mechanical" upgrade can silently change output. Tests are the only mechanism that makes regressions detectable before they reach production.

---

## Characterization Tests: Strategy

Characterization tests capture the EXISTING behaviour of the legacy system, not the intended behaviour. They are not unit tests of business logic; they are regression nets placed around the existing black box.

### Sources for characterization tests

1. **HTTP-level tests against the running legacy app**: record request/response pairs using a tool like `Playwright`, `HttpClient` in xUnit, or `dotnet-httprepl`. Replay against the migrated app to compare.
2. **Output-based tests on domain services**: identify the most-called service methods; write tests that assert on their outputs for representative inputs.
3. **Database round-trip tests**: if EF6 queries are being migrated, write tests that execute the EF6 query against a test database and capture the output; compare the EF Core equivalent.

### Minimum coverage gate

Before any project file is touched:

| Component | Minimum coverage |
|---|---|
| Critical business paths (orders, payments, auth) | 80% line coverage |
| WCF service operations being migrated | 1 characterization test per operation |
| EF6 queries on hot paths (per-request lookups) | 1 test per query shape |
| Web Forms pages being migrated | 1 smoke test per page (HTTP 200, key content present) |
| Overall codebase | 40% line coverage (characterization, not unit) |

These minimums are floors, not targets. Higher coverage reduces migration risk proportionally.

---

## Tooling for Legacy Codebase Testing

### xUnit + WebApplicationFactory (for ASP.NET Core target)

Characterization tests run against the legacy app over HTTP; the same tests are reused as integration tests against the migrated app:

```csharp
public class OrdersCharacterizationTests : IClassFixture<LegacyAppFixture>
{
    private readonly HttpClient _client;

    public OrdersCharacterizationTests(LegacyAppFixture fixture)
        => _client = fixture.CreateClient();

    [Fact]
    public async Task GetOrder_ReturnsExpectedShape()
    {
        var response = await _client.GetAsync("/api/orders/00000000-0000-0000-0000-000000000001");

        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        Assert.Contains("\"status\"", body);       // shape check
        Assert.Contains("\"orderId\"", body);
    }
}
```

After migration, swap `LegacyAppFixture` for `WebApplicationFactory<Program>` pointing at the new .NET 8/9 app.

### Verify (snapshot testing)

`Verify` NuGet package captures serialised output to `.verified.txt` files. On first run it creates the snapshot; on subsequent runs it diffs against it. Ideal for characterizing complex JSON responses or HTML output.

```csharp
[Fact]
public async Task GetOrder_MatchesSnapshot()
{
    var response = await _client.GetAsync("/api/orders/test-order-id");
    var body = await response.Content.ReadAsStringAsync();

    await Verify(body); // creates .verified.txt on first run
}
```

### Coverage measurement

```dotnetcli
dotnet test --collect:"XPlat Code Coverage"
reportgenerator -reports:"coverage.cobertura.xml" -targetdir:"coveragereport" -reporttypes:Html
```

---

## What to Test, What to Skip

**Test:**
- Any code path that touches business rules, pricing, routing logic, auth
- Data access: query shapes and their return types
- HTTP endpoints and their response contracts
- Configuration-dependent behaviour (feature flags, environment-specific settings)

**Skip (for characterization purposes):**
- Logging output (format will change)
- Internal infrastructure wiring (DI registration, middleware order) unless directly testable via HTTP
- Third-party library internals

---

## Integrating Tests into the Migration Phase Plan

1. **Before Phase 0 (strangler fig)**: characterization tests gate the entire migration. No phase starts without meeting the coverage minimums above.
2. **Before each strangler fig phase**: add targeted tests for the component about to be migrated.
3. **After each strangler fig phase**: run the full test suite against the new service; all previously passing tests must still pass.
4. **After full migration**: convert characterization tests to proper unit and integration tests using `WebApplicationFactory<Program>` and Testcontainers.

---

## References

- xUnit documentation: https://xunit.net
- Verify (snapshot testing): https://github.com/VerifyTests/Verify
- WebApplicationFactory integration testing: https://learn.microsoft.com/aspnet/core/test/integration-tests
- FluentAssertions: https://fluentassertions.com
- EF Core testing with Testcontainers: https://learn.microsoft.com/ef/core/testing/
