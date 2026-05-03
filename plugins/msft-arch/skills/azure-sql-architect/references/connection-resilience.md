# Connection Resilience (client-side)

**Applies to**: .NET applications using Microsoft.Data.SqlClient and EF Core 8/9 against Azure SQL Database, Azure SQL Managed Instance, and Azure SQL Edge.

> Codified opinion: Connection resilience: SqlClient retry logic + circuit breaker pattern.

Azure SQL is a network-attached PaaS service. Transient failures are not exceptional; they are expected. Treat connection resilience as a hard requirement of every production code path that talks to SQL.

App-side EF Core data-access patterns (DbContext lifetime, AsNoTracking, projection, ExecuteUpdate, migration workflow) are governed by `standards/references/coding-stack/ef-core-checklist.md`. This document is platform-tuning-side: SqlClient retry, circuit breaker, transient fault classification, and how those interact with EF Core's `EnableRetryOnFailure`. Do not duplicate the EF Core checklist; reference it.

## Two layers of resilience

1. SqlClient connection retry (the connection-open path).
2. Application retry plus circuit breaker (the operation path).

Both are required. SqlClient retry only addresses connection-open failures; once the connection is live, a transient query failure is the application's problem.

## SqlClient connection retry

`Microsoft.Data.SqlClient` supports `ConnectRetryCount` and `ConnectRetryInterval` connection-string parameters: the driver retries connection-open after transient errors before surfacing.

```csharp
var connectionString =
    "Server=tcp:<group>.database.windows.net,1433;" +
    "Database=AppDb;" +
    "Authentication=Active Directory Default;" +
    "Encrypt=True;" +
    "ConnectRetryCount=5;" +
    "ConnectRetryInterval=10;" +
    "Connect Timeout=30;";
```

Defaults (1 retry, 10 second interval) are too lax for production. 5 retries at 10-second intervals is a reasonable starting point; tune based on observed failover behavior.

## Application retry: Polly + circuit breaker

For the operation path, use Polly (or the equivalent in your stack) with two policies wrapped: retry inside circuit breaker.

```csharp
using Polly;
using Polly.Retry;
using Polly.CircuitBreaker;

var retry = Policy
    .Handle<SqlException>(IsTransient)
    .WaitAndRetryAsync(
        retryCount: 5,
        sleepDurationProvider: attempt =>
            TimeSpan.FromMilliseconds(Math.Pow(2, attempt) * 100));

var breaker = Policy
    .Handle<SqlException>(IsTransient)
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 8,
        durationOfBreak: TimeSpan.FromSeconds(30));

// Wrap: retries happen, but once the breaker opens, the next call short-circuits.
var policy = Policy.WrapAsync(retry, breaker);
```

The circuit breaker prevents thundering-herd retries from a downed primary; the retry handles individual blips. Tune the thresholds against your soak-test traffic shape.

## Transient fault classification

A SqlException is transient if its number is in the recoverable list. Microsoft publishes the list; the canonical short set used in production:

| SQL error number | Meaning | Retryable |
|---|---|---|
| 4060 | Cannot open database (often config) | No |
| 40197 | Service is busy | Yes |
| 40501 | Service is currently busy (throttle) | Yes |
| 40613 | Database unavailable (often during failover) | Yes |
| 49918, 49919, 49920 | Cannot process create/alter operation | Yes |
| 11001 | DNS lookup failed (often during regional event) | Yes |
| 18456 | Login failed | No (authentication problem, not transient) |
| 53 | Network path not found | Yes |

```csharp
static bool IsTransient(SqlException ex) =>
    ex.Errors.Cast<SqlError>().Any(e => e.Number is
        40197 or 40501 or 40613 or 49918 or 49919 or 49920 or 11001 or 53);
```

Verify the current list with `microsoft_docs_search` before relying on a hard-coded set; new transient codes appear over time.

## Interaction with EF Core's EnableRetryOnFailure

EF Core's execution strategy retries entire operations. The interaction with the patterns above:

- `EnableRetryOnFailure` is the right default for query operations. Configure with conservative limits (5 retries, 30 second cap) per `standards/references/coding-stack/ef-core-checklist.md`.
- `EnableRetryOnFailure` is incompatible with bare `BeginTransaction`. Use `db.Database.CreateExecutionStrategy().ExecuteAsync(...)` for read-modify-write blocks. The EF Core checklist is the canonical reference here.
- Do not stack EF Core retry on top of Polly retry on top of SqlClient retry. Pick a layer per operation. Typical division: SqlClient handles connection-open; EF Core retry handles entity-framework-managed query operations; Polly handles raw `SqlCommand` paths and cross-service workflows.
- For Hyperscale and Cosmos DB-style serverless tiers that already retry internally, double-retry adds latency without value. Reduce app-side retry count when targeting these tiers.

## Read-only routing and the connection string

When using read-only routing on Hyperscale or Business Critical:

```text
Server=tcp:<group>.database.windows.net,1433;
Database=AppDb;
ApplicationIntent=ReadOnly;
Authentication=Active Directory Default;
Encrypt=True;
```

A separate connection string with `ApplicationIntent=ReadOnly` is the supported way to route reads. Do not implement this with two app-side connections that branch on operation type unless the platform genuinely does not support routing.

## Identity

Use Entra ID authentication via Managed Identity wherever possible:

- App on App Service / Container Apps / Functions / AKS: `Authentication=Active Directory Default` (or `Active Directory Managed Identity`) plus a system-assigned or user-assigned managed identity granted DB-level role membership.
- No SQL logins, no connection-string secrets, no Key Vault references for SQL passwords. Push back on any design that routes around this.

Hand off identity wiring to `/identity-architect`.

## Operational observability

- Surface SqlException numbers and counts in App Insights as a custom metric (`/observability-architect`). A spike in 40613 in one region is the early signal of a failover event.
- Log the circuit-breaker state transitions; an open breaker is a paging signal, not an info-level event.
- Run a quarterly drill: kill connections, throttle artificially, confirm the retry plus breaker behavior matches the documented runbook.

## Don'ts

- Do not catch `SqlException` and swallow it. Rethrow or fail fast.
- Do not retry on non-transient errors (login failures, permission denials, schema errors). Retrying a login failure is a brute-force authentication pattern.
- Do not retry an INSERT without idempotency: use a deterministic key, an upsert, or `MERGE` with care.
- Do not duplicate the EF Core checklist content here. Reference `standards/references/coding-stack/ef-core-checklist.md`.
