# Throttling and Retry

Throttling-aware retry with exponential backoff and jitter. Graph throttles aggressively. Every Graph caller must assume `429 Too Many Requests` will appear in production traffic and handle it correctly. The Graph SDKs ship default middleware that does the right thing: do not disable it without a reason, and do not roll your own retry policy without first understanding what the SDK already does.

---

## How Graph throttles

Microsoft Graph imposes two layers of limits:

1. **Global limit**: 130,000 requests per 10 seconds per app across all tenants.
2. **Service-specific limits**: each service (Outlook, Teams, SharePoint, Identity, etc.) has its own per-app, per-tenant, per-user limits.

Identity and access reads use a token bucket model with `ResourceUnits`:

| Limit type | Resource unit quota | Write quota |
|---|---|---|
| application + tenant pair | S: 3,500 / 10s, M: 5,000 / 10s, L: 8,000 / 10s | 3,000 / 2.5 minutes |
| application | 150,000 / 20s | 35,000 / 5 minutes |
| tenant | n/a | 18,000 / 5 minutes |

(S/M/L: under 50, 50-500, over 500 users in tenant.)

ResourceUnit cost is shaped by query parameters: `$select` reduces cost by 1, `$expand` increases by 1, `$top<20` reduces by 1. Using `$select` on every read is therefore a throttling control as well as a PII control.

---

## Response shape

A throttled response:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 10
Content-Type: application/json
{
  "error": {
    "code": "TooManyRequests",
    "message": "Application is over its first quota."
  }
}
```

The `Retry-After` header carries the number of seconds to wait. Honour it. The fastest recovery path is sleep-then-retry: backing off less than `Retry-After` does not help and may extend the throttle window because Graph still counts the rejected requests.

For `503 Service Unavailable`, treat as transient and apply the same `Retry-After` rule, falling back to exponential backoff with jitter.

---

## The retry policy

```text
1. Send request.
2. If 200..299: return success.
3. If 429 or 503:
   a. If Retry-After header present: sleep that many seconds.
   b. Else: sleep min(base * 2^attempt + random(0, jitter), maxSleep).
   c. Increment attempt counter.
   d. If attempt < maxRetries: goto 1.
   e. Else: surface 429 to caller, emit metric.
4. If 4xx (other): do not retry, surface error.
5. If 5xx (other): retry with exponential backoff + jitter, capped.
```

Recommended defaults:
- `maxRetries`: 3 (interactive flows), 5 (background workers).
- `base`: 1 second.
- `jitter`: 0..1 second uniform random.
- `maxSleep`: 30 seconds.

Beyond the retry cap, surface the error to the caller and emit a metric so operators see throttling pressure.

---

## SDK middleware (default behavior)

The official Graph SDKs ship `RetryHandler` middleware that:

- Honours `Retry-After` automatically.
- Falls back to exponential backoff with jitter when the header is missing.
- Caps retries (3 by default).
- Logs each retry through the SDK telemetry hooks.

**.NET v5+** (`Microsoft.Graph` 5.x):

```csharp
using Microsoft.Graph;
using Microsoft.Kiota.Http.HttpClientLibrary.Middleware;

// Default: GraphServiceClient ctor wires the retry handler in the chain
var graphClient = new GraphServiceClient(credential, scopes);

// Custom: tune retry count or delay
var retryOptions = new RetryHandlerOption
{
    MaxRetry = 5,
    Delay = 2,
    ShouldRetry = (delay, retryCount, response) =>
        response.StatusCode == HttpStatusCode.TooManyRequests
        || response.StatusCode == HttpStatusCode.ServiceUnavailable
};
```

**JS / TS v3+** (`@microsoft/microsoft-graph-client`):

```typescript
import { Client, RetryHandlerOptions } from "@microsoft/microsoft-graph-client";

const client = Client.initWithMiddleware({
  authProvider,
  middlewareOptions: [new RetryHandlerOptions(undefined, 5)] // 5 max retries
});
```

**Python** (`msgraph-sdk`):

The retry handler ships in `kiota_http.middleware.retry_handler.RetryHandler` and is wired automatically.

Do not strip these handlers. If you need custom behavior (e.g. circuit breaker on top of retry), wrap them, do not replace them.

---

## Avoiding throttling: structural moves

1. **`$select` on every read.** Cuts ResourceUnit cost and payload size.
2. **`$filter` aggressively.** Narrow the rowset before paging.
3. **Webhooks > polling.** A `$top=50` poll every 30 seconds across 1,000 mailboxes is a throttling event waiting to happen. Subscribe instead.
4. **Delta queries for cold start.** First call returns the full set, subsequent calls return only deltas. Lower steady-state cost than re-reading.
5. **Batch unrelated reads.** Same throttling cost as separate calls but lower round-trip latency, freeing client-side capacity.
6. **Cache aggressively, with invalidation tied to webhooks.** Tenant data changes notify, application caches read.
7. **Use Microsoft Graph Data Connect for bulk extraction.** If the use case is "weekly full export of every mailbox to a data lake", Graph REST is the wrong tool. Data Connect bypasses throttling for sanctioned bulk ETL.

---

## Headers worth setting

| Header | Purpose |
|---|---|
| `x-ms-throttle-priority` | `low` / `normal` / `high`. Background work sets `low`. User-facing flows set `high`. Throttled requests are dropped low-first. |
| `Prefer: return=minimal` | Tells the service to return only minimum content. Reduces ResourceUnit cost. |
| `Prefer: outlook.timezone="..."` | Outlook-specific time zone normalization. |

Setting priority does not change limits, but it changes which of your requests survive throttling.

---

## Observability

Every Graph caller should emit:

- Counter: total Graph requests by operation.
- Counter: `429` responses by operation.
- Counter: `503` responses by operation.
- Histogram: `Retry-After` values seen.
- Histogram: end-to-end latency (including retries).
- Counter: retries exhausted (request gave up).

Wire these into App Insights or your observability target. The `429` counter is the canary: if it climbs, the integration is over-pressured before users feel it.

---

## Trade-offs and exceptions

- **Aggressive retries can amplify throttling**: adding more retries does not get you out of the throttle window faster. Cap retries and surface the error.
- **Custom HTTP clients**: if you call Graph via raw `HttpClient` (no SDK), you must implement retry yourself. The default `HttpClient` does not honour `Retry-After`.
- **Multi-tenant scaling**: your `application` quota is shared across all tenants the app serves. A misbehaving tenant can starve others. Per-tenant rate-limiting on your side is good hygiene.
- **Bursty workloads**: front the burst with a queue. Worker pulls from queue at a steady rate inside the throttling envelope.
- **Throttle priority headers**: do not set `high` on background work. The priority hint is a coordination tool, not a workaround.
