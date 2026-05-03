# Beta vs v1.0 Endpoint Policy

Beta endpoints prohibited in production unless an explicit ADR justifies it (with sunset plan). The Graph beta surface (`https://graph.microsoft.com/beta/`) ships features ahead of GA, and Microsoft explicitly warns that beta APIs may change without notice. Production code that depends on beta is a future incident waiting to happen unless the team has agreed in writing what they are paying for and how they will exit.

---

## The default is v1.0

| Endpoint | Default for | Promise |
|---|---|---|
| `https://graph.microsoft.com/v1.0/` | All production code | API stable; breaking changes go through deprecation cycle and prior notice |
| `https://graph.microsoft.com/beta/` | Prototypes, internal tools, ADR-justified production | API may change without notice; deprecation may be silent; throttling and SLOs not guaranteed at the same level |

If a feature is in v1.0, use v1.0. There is no scenario where "but the beta version has a slightly nicer shape" justifies the trade-off.

---

## When beta is acceptable in production

A beta dependency is acceptable in production only when **all** of the following are true:

1. The required feature does not exist in v1.0 at any level (verified via Microsoft Learn MCP search at the time of decision).
2. The team has produced an ADR (`adr-NNN-graph-beta-{resource}.md`) covering the required content (template below).
3. The ADR has a named owner who is on call for the resource's GA migration.
4. Telemetry monitors the resource for GA availability (a probe call to v1.0 that flags when the schema appears).
5. The feature flag wrapping the beta call has a documented exit plan when GA ships.

If any of these are false, the answer is no. Pick a different feature, polyfill on top of v1.0, or wait.

---

## ADR template

```markdown
# ADR-NNN: Use Microsoft Graph beta endpoint for {resource}

## Status

Accepted on {date} by {owner}, due for review on {date + 6 months}.

## Context

Production code in {component} requires {capability}. The capability is currently
exposed only at `https://graph.microsoft.com/beta/{resource}`. v1.0 does not
offer an equivalent (verified via `microsoft_docs_search` on {date}).

## Decision

Adopt the beta endpoint behind feature flag `graph_beta_{resource}` for the
specific operation `{operation}`. Wrap calls in a single client adapter so the
v1.0 migration is a one-file change.

## Consequences

- The beta API can change without notice. Mitigation: schema-checked tests run
  daily against `/beta/{resource}` and alert on deviation.
- Throttling and SLOs at beta are not guaranteed. Mitigation: feature flag can
  be turned off without code change; degraded UX path defined.
- Regulatory or compliance review may flag beta as unsupported. Mitigation:
  flag's risk register entry includes the data classification and the residency
  posture is unchanged from v1.0.

## Sunset plan

- Trigger: v1.0 ships an equivalent resource. Detected by daily probe at
  `https://graph.microsoft.com/v1.0/{resource}`.
- Migration: switch the adapter from beta to v1.0, run regression suite, ship
  flag flip in next deployment.
- Deadline: within 90 days of GA, regardless of perceived API parity.
- Verification: feature flag removed within 30 days of v1.0 cutover; beta
  reference deleted from the codebase.

## Alternatives considered

- Polyfill on top of v1.0: rejected because {reason}.
- Wait for GA: rejected because {reason and timeline pressure}.
- Use a different resource that satisfies the requirement at v1.0: rejected
  because {gap}.

## Owner

{name}, accountable for the migration trigger and on-call for beta breakage.
```

Store ADRs in `spec/decisions/` per the spec skill's ADR-as-output pattern. Reference the ADR ID in code comments next to the beta call.

---

## Implementation pattern

```csharp
public interface IGraphInsightsClient
{
    Task<IReadOnlyList<UsedInsight>> GetUsedDocumentsAsync(string userId);
}

// Behind feature flag: graph_beta_insights
public sealed class BetaInsightsClient(BetaGraph.GraphServiceClient beta) : IGraphInsightsClient
{
    public async Task<IReadOnlyList<UsedInsight>> GetUsedDocumentsAsync(string userId)
    {
        // ADR-014-graph-beta-insights: this call lives at /beta/users/{id}/insights/used
        // until v1.0 parity ships. Migration probe runs daily.
        var page = await beta.Users[userId].Insights.Used.GetAsync();
        return page?.Value?.AsReadOnly() ?? Array.Empty<UsedInsight>();
    }
}
```

The wrapping interface keeps the migration to a single class swap. Do not let beta types leak into your domain model.

---

## Migration probe

A daily job calls the v1.0 path with a tolerant client and emits a metric:

```csharp
// Background service, runs once daily
try
{
    var probe = await v1Client.Users["me"].Insights.Used.GetAsync();
    metrics.Emit("graph.beta.migration.available", 1, tags: new() { ["resource"] = "insights.used" });
    logger.LogWarning("v1.0 parity detected for insights.used. Trigger ADR-014 migration.");
}
catch (ODataError ex) when (ex.ResponseStatusCode == 404 || ex.Error?.Code == "ResourceNotFound")
{
    metrics.Emit("graph.beta.migration.available", 0, tags: new() { ["resource"] = "insights.used" });
}
```

When the metric flips to 1 and stays there for three consecutive runs, open the migration work item.

---

## Common pitfalls

- **Importing both `Microsoft.Graph` and `Microsoft.Graph.Beta` in the same DI scope**: the typed clients are separate. Keep them in separate registrations and never inject both into the same component.
- **Beta entities in API responses**: do not let beta types reach the public API of your service. Map to your own domain types so the beta dependency is fully internal.
- **Long-lived beta dependencies**: an ADR with a six-month review date that gets rubber-stamped indefinitely is the failure mode. The reviewer must check the migration trigger and update the deadline.
- **"Beta is fine because Microsoft uses it internally"**: not a justification. Internal Microsoft consumption does not extend the public stability contract.

---

## Review cadence

Every ADR-justified beta dependency carries a review date no later than six months from the decision. The review answers:

1. Is the v1.0 equivalent now available?
2. If yes: has the team migrated? If not, why not, and what is the new deadline?
3. If no: has the resource shape changed in beta since the last review? If yes, did our schema tests catch it?
4. Is the named owner still on call for this dependency?

A failed review (no v1.0 path AND no working schema tests AND no clear owner) is a blocker for the next release until resolved.

---

## Trade-offs and exceptions

- **Internal-only tools**: ADR still required, but the consequences section is simpler. The discipline is in the habit, not in the prose volume.
- **Customer demos / proof-of-concept**: beta is fine without ADR. Mark the codebase clearly as PoC and never roll it into production without the ADR step.
- **Resources that have lived in beta for years**: the durability does not make them GA. Some `/beta/security/*` and `/beta/identityGovernance/*` resources have been beta for two-plus years and are still beta. Treat them as beta until v1.0 ships.
- **Pinning a Graph SDK version that still exposes a removed beta surface**: not a workaround. If Microsoft removes the API server-side, the call fails at runtime regardless of SDK version.
