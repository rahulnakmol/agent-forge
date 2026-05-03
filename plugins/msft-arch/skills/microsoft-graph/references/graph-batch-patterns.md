# Microsoft Graph Batch Patterns

Batch requests for >5 sequential calls. Webhooks (change notifications) > polling for state changes. Each `$batch` POST combines up to 20 individual requests in one round trip, reducing network latency and simplifying retry logic. The trade-off is that throttling and dependency rules apply individually inside the batch, and the dependency model is restricted to three patterns.

---

## When to batch

| Scenario | Batch? | Notes |
|---|---|---|
| Read user, calendar, and recent messages on app load | Yes | Three unrelated reads, one round trip |
| Create event, then read updated calendar | Yes | Use `dependsOn` to sequence the read after the create |
| Loop over 100 user IDs to fetch each profile | No, page or use `$filter` | Batch is capped at 20; pagination is the right tool |
| Streaming data ingest at high RPS | No | Batches do not raise throttling ceilings; per-request limits apply |
| Bypass URL length limit on a complex `$filter` | Yes | Move the filter into the batch payload |

The 5-call rule of thumb: if a code path makes more than five sequential Graph calls and each adds latency, batch them. If they fan out and can run in parallel from the client, parallel SDK calls are equivalent in throughput; batch wins on round-trip count.

---

## Batch shape

```http
POST https://graph.microsoft.com/v1.0/$batch
Content-Type: application/json

{
  "requests": [
    {
      "id": "1",
      "method": "GET",
      "url": "/me"
    },
    {
      "id": "2",
      "method": "GET",
      "url": "/me/calendarView?startDateTime=2026-05-03T00:00:00Z&endDateTime=2026-05-04T00:00:00Z&$select=subject,start,end"
    },
    {
      "id": "3",
      "method": "POST",
      "url": "/me/events",
      "body": {
        "subject": "Architecture review",
        "start": { "dateTime": "2026-05-03T14:00:00", "timeZone": "UTC" },
        "end": { "dateTime": "2026-05-03T15:00:00", "timeZone": "UTC" }
      },
      "headers": { "Content-Type": "application/json" }
    }
  ]
}
```

The response mirrors the request structure with one entry per `id`. Each entry has its own status code, headers, and body. Do not assume all entries succeeded just because the outer batch returned `200`.

---

## Dependency patterns

Microsoft Graph allows three dependency patterns inside a batch (see learn.microsoft.com/graph/known-issues#json-batching):

1. **Parallel**: no `dependsOn` set on any request. Graph may execute in any order.
2. **Serial**: each request depends on the previous (`"dependsOn": ["1"]`, `"dependsOn": ["2"]`, etc.). Strict ordering.
3. **Same**: many requests depend on the same single request (`"dependsOn": ["1"]` on requests 2, 3, 4). Request 1 runs first, then 2, 3, 4 in declared order.

Other DAG shapes are not supported. If a request that another depends on fails, the dependent request returns `424 Failed Dependency`.

```json
{
  "requests": [
    { "id": "1", "method": "POST", "url": "/me/events", "body": { /* ... */ }, "headers": { "Content-Type": "application/json" } },
    { "id": "2", "method": "GET", "url": "/me/calendarView?startDateTime=...&endDateTime=...", "dependsOn": ["1"] }
  ]
}
```

---

## SDK batching (.NET v5+)

The SDK takes care of the 20-request cap automatically: oversized batches are split behind the scenes.

```csharp
var batch = new BatchRequestContentCollection(graphClient);

var meRequest = graphClient.Me.ToGetRequestInformation();
var calendarRequest = graphClient.Me.CalendarView.ToGetRequestInformation(rc =>
{
    rc.QueryParameters.StartDateTime = "2026-05-03T00:00:00Z";
    rc.QueryParameters.EndDateTime   = "2026-05-04T00:00:00Z";
    rc.QueryParameters.Select        = new[] { "subject", "start", "end" };
});

var meId = await batch.AddBatchRequestStepAsync(meRequest);
var calId = await batch.AddBatchRequestStepAsync(calendarRequest);

var response = await graphClient.Batch.PostAsync(batch);

var me = await response.GetResponseByIdAsync<User>(meId);
var calendar = await response.GetResponseByIdAsync<EventCollectionResponse>(calId);
```

---

## SDK batching (JS / TS v3+)

```typescript
import { Client } from "@microsoft/microsoft-graph-client";

const batchPayload = {
  requests: [
    { id: "1", method: "GET", url: "/me" },
    { id: "2", method: "GET", url: "/me/calendarView?startDateTime=2026-05-03T00:00:00Z&endDateTime=2026-05-04T00:00:00Z&$select=subject,start,end" }
  ]
};

const response = await client.api("/$batch").post(batchPayload);

for (const r of response.responses) {
  if (r.status >= 400) {
    // surface r.body, r.headers["Retry-After"] for 429 handling
    continue;
  }
  // r.body has the entity
}
```

---

## Throttling inside a batch

Each request is evaluated against the applicable throttling limits independently. A batch of 20 reads against the same Outlook mailbox can still receive `429` on individual entries: Outlook caps concurrency at four parallel requests per mailbox even inside a single batch (Graph internally serializes the rest). Use `dependsOn` to be explicit about ordering for same-mailbox writes.

When a request inside a batch returns `429`, it carries its own `Retry-After`. The retry policy must split the batch and retry only the failed entries: do not retry the entire batch as one unit.

---

## Concrete patterns by scenario

| Goal | Pattern |
|---|---|
| Load user dashboard (profile + calendar + recent files) | Parallel batch of three GETs |
| Create folder, upload file, set permissions | Serial batch with dependsOn |
| Fan-out create across N teams | Parallel batch of size 20; loop until all teams processed |
| Cross-resource transactional read (user + manager + group) | Same-pattern batch with id "1" reading user, id "2" / "3" depending on "1" |
| Mass update of users (>20) | Page through caller-side, call SDK batch helper which auto-splits |

---

## Trade-offs and exceptions

- **Latency**: batching reduces round trips but adds payload parsing on both sides. For very small batches (two or three requests with no shared latency), the overhead is not worth it.
- **Error correlation**: a partial-failure batch is harder to log clearly. Always log the per-id status alongside the outer batch ID.
- **Outlook concurrency**: same-mailbox writes serialize internally regardless of batch composition. Test under load before assuming a 20-deep batch hits the wire as 20 parallel writes.
- **`$batch` does not bypass throttling**: it bypasses round-trip cost only.
- **Beta endpoints inside a batch**: the batch endpoint itself is v1.0; individual request URLs may target `/beta/*` if the ADR justifies it, but mixing v1.0 and beta in one batch is supported and explicit.
