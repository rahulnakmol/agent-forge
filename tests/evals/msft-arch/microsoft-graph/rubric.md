Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Application vs Delegated Permission Clarity** — Correctly distinguishes: application permissions for daemon/service/background jobs (no user context); delegated permissions for acting on behalf of a signed-in user. Never confuses these models in the same flow. Score 5 if permission model is correctly classified per actor; 1 if application and delegated permissions are confused or mixed inappropriately.

2. **Change Notifications over Polling** — Recommends webhooks (change notifications) over polling for state changes. Includes subscription lifecycle management (expiration tracking, renewal jobs, lifecycleNotificationUrl). Score 5 if change notifications are recommended with subscription lifecycle design; 1 if polling is maintained without recommending webhooks.

3. **Batch Requests for Multiple Calls** — Recommends $batch for 5 or more sequential Graph calls. Does not accept multiple sequential single calls when batching is available. Score 5 if batching is correctly recommended and designed; 1 if multiple sequential calls are accepted without batching.

4. **Throttling-Aware Retry** — Requires honouring the Retry-After response header on 429/503, exponential backoff with jitter, circuit breaker for persistent throttling, and metrics on throttling events. The Graph SDK middleware handles this by default and should not be disabled. Score 5 if throttling strategy is comprehensive; 1 if throttling is handled with simple sleep or ignored.

5. **Granular Permissions and $select** — Applies granular permissions (Sites.Selected for SharePoint, Mail.Read vs Mail.Read.All, Resource-Specific Consent for Teams). Requires $select on every read to minimize PII exposure and reduce throttling cost. Score 5 if least-privilege scope and $select are applied correctly; 1 if tenant-wide permissions are recommended without Sites.Selected or $select is omitted.
