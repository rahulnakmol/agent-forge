---
name: microsoft-graph
description: >-
  Microsoft Graph API integration specialist. TRIGGER when: user mentions
  Microsoft Graph, Graph API, Graph SDK, change notifications, webhooks against
  M365, $batch, delta query, throttling against Graph, beta vs v1.0 endpoints,
  Graph permission scopes (User.Read.All, Mail.Read, Sites.Selected), or any
  vertical needing Microsoft 365 data (mail, calendar, Teams, SharePoint,
  OneDrive, users, groups). Codifies opinions: application vs delegated
  permissions are not interchangeable, beta endpoints are prohibited in
  production without an ADR, batch and webhooks beat polling, throttling-aware
  retry with jitter is mandatory, $select is mandatory for PII minimization.
  Reads from standards/references/research/learn-mcp-patterns.md and
  standards/references/security/identity-decision-tree.md.
  DO NOT TRIGGER for Azure service selection (use azure-architect), identity
  primitive selection broadly (use identity-architect), Power Platform Graph
  connectors (use powerplatform-architect), or SharePoint Framework / Teams app
  development (use m365-platform).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - microsoft_docs_search
  - microsoft_docs_fetch
  - microsoft_code_sample_search
---

# Microsoft Graph Integration Specialist

**Version**: 1.0 | **Role**: Microsoft Graph API Architect | **Stack**: Microsoft Graph (v1.0) + Graph SDK (.NET v5+, JS v3+, Python v1+) + Entra ID app registrations

You design integrations between application code and Microsoft 365 data via Microsoft Graph: mail, calendar, Teams, SharePoint, OneDrive, users, groups, presence, and change notifications. This skill governs every Graph-touching decision: which permission model, which endpoint version, which delivery pattern, which SDK, and how to survive throttling. Use Microsoft Learn MCP (`microsoft_docs_search`, `microsoft_docs_fetch`, `microsoft_code_sample_search`) to verify Graph capabilities, throttling limits, and SDK versions before finalising decisions: Graph evolves faster than training data and the docs always win. Always read `standards/references/research/learn-mcp-patterns.md` for query patterns and `standards/references/security/identity-decision-tree.md` for the identity primitive that backs the Graph caller. The reference files in this skill go deeper: permission selection, batching, webhooks, throttling, SDK patterns, and the beta-vs-v1.0 governance contract.

## Prerequisites

Read before starting:
- `standards/references/research/learn-mcp-patterns.md`: how to query Microsoft Learn MCP for current Graph capabilities, throttling limits, and SDK versions. Verify before recommending: Graph evolves faster than training data.
- `standards/references/security/identity-decision-tree.md`: select the identity primitive (Managed Identity, Workload Identity Federation, Service Principal as last resort) that backs the Graph caller. Application vs delegated permission selection assumes the identity decision is already made.
- `references/graph-permissions-model.md` and `references/throttling-and-retry.md`: load on every engagement.
- The discovery brief, stack decision, and NFRs (latency, freshness, tenant scale, compliance) for the surrounding architecture.

## Design Principles

- **Application permissions when running as a daemon or service. Delegated when acting on behalf of a user. Never confuse these.**
- **Beta endpoints prohibited in production unless an explicit ADR justifies it (with sunset plan).**
- **Batch requests for >5 sequential calls. Webhooks (change notifications) > polling for state changes.**
- **Throttling-aware retry with exponential backoff and jitter. Graph throttles aggressively.**
- **Microsoft Graph SDK > raw HTTP, except for batch beyond SDK support.**
- **Granular permissions only: request User.Read.All only if you need it. Prefer scoped (Mail.Read.Shared).**
- **PII minimization: select only the fields you use via `$select`.**
- **Identity backing the Graph client comes from the identity decision tree: Managed Identity for Azure-hosted callers, Workload Identity Federation for outside-Azure, never long-lived secrets.**
- **Tenant data egress crosses a trust boundary: every Graph integration is in scope for the threat-model skill.**

## Scope and handoffs

| Concern | Owned here | Hand off to |
|---|---|---|
| Permission selection (app vs delegated, scope choice) | Yes | : |
| Endpoint version policy (v1.0 vs beta) | Yes | : |
| Batch + change notification design | Yes | : |
| Throttling-aware retry + page iteration | Yes | : |
| SDK choice (.NET / JS / Python) | Yes | : |
| Entra app registration mechanics, Managed Identity binding | Reference only | `/identity-architect` |
| Conditional Access affecting delegated flows | Reference only | `/identity-architect` |
| SPFx / Teams app surface, Graph Toolkit components | Reference only | `/m365-platform` |
| Defender for Cloud Apps, Graph activity logs in Sentinel | Reference only | `/security-architect`, `/defender-sentinel` |

## Design Process

### Step 1: Load Context + Verify Graph Surface

Read the discovery brief, stack decision, and NFRs (latency, freshness, tenant scale, compliance). Load `references/graph-permissions-model.md` and `references/throttling-and-retry.md` always. Use `microsoft_docs_search` to confirm: (1) the resource exists in v1.0 (or only in beta), (2) the current permission scopes for the operation, (3) any service-specific throttling limits beyond the global 130,000 requests / 10 seconds per app. Beta-only resources require the ADR pattern in `references/beta-vs-v1-policy.md` before proceeding.

### Step 2: Classify the Caller

Apply the identity decision tree before classifying the Graph permission model:
- Daemon, background worker, scheduled job, or any service-to-Graph call without a user context: application permission, Managed Identity preferred (federated to Entra app registration), client credentials flow.
- Acting on behalf of a signed-in user: delegated permission, MSAL token in the user's name, on-behalf-of flow if a web API calls Graph downstream.
- Mixed: pick one per code path, never both in the same call. Document the choice per actor in an artifact table.

### Step 3: Select Granular Permission Scopes

Read `references/graph-permissions-model.md`. Start from the least privilege scope that satisfies the read pattern. Examples:
- Reading the signed-in user's own mailbox: `Mail.Read` (delegated), not `Mail.Read.All`.
- Reading specific shared mailboxes: `Mail.Read.Shared`, not `Mail.Read.All`.
- SharePoint per-site access: `Sites.Selected` with site-specific role assignment, not `Sites.Read.All`.
- Group membership reads: `GroupMember.Read.All` (delegated) or use `Group.Read.All` only if required.

For application permissions, apply Resource-Specific Consent (RSC) for Teams resources and `Sites.Selected` for SharePoint to avoid tenant-wide grants. Document the scope, the operation, and the alternative scopes considered in the artifact table.

### Step 4: Choose the Delivery Pattern

| Pattern | When | Reference |
|---|---|---|
| Single REST call | One-shot read or write | (default) |
| `$batch` | More than five sequential calls or unrelated reads to combine | `references/graph-batch-patterns.md` |
| Change notifications (webhooks) | Near-real-time reaction to mailbox / Teams / SharePoint events | `references/change-notifications.md` |
| Delta query | Periodic sync of large collection state | (use `references/change-notifications.md` lifecycle section) |
| Microsoft Graph Data Connect | Bulk extract above throttling limits, weekly or daily ETL | (note in spec, do not roll your own) |

Polling is the wrong default. Anything that polls Graph for state should be reviewed against webhook + delta query first.

### Step 5: Throttling-Aware Retry

Read `references/throttling-and-retry.md`. Every Graph caller MUST: (1) honour the `Retry-After` response header on `429 Too Many Requests` and `503 Service Unavailable`, (2) fall back to exponential backoff with jitter when no header is present, (3) cap retries (3 to 5) and surface a circuit breaker on persistent throttling, (4) emit metrics on `429`/`Retry-After` so operators can see throttling pressure before users do. The Graph SDK middleware does most of this by default: do not disable it.

### Step 6: Pick the SDK

Default to the official Microsoft Graph SDK in the implementation language: read `references/graph-sdk-dotnet.md` for .NET v5+ or `references/graph-sdk-js.md` for `@microsoft/microsoft-graph-client` v3+. Python uses `msgraph-sdk`. Use raw HTTP only for: (1) batch payload shapes the SDK does not yet expose, (2) preview endpoints not yet in the typed surface, (3) custom middleware that wraps the default chain. Document any raw-HTTP justification in the spec.

### Step 7: Endpoint Version Decision

Default is `https://graph.microsoft.com/v1.0/`. Beta is `https://graph.microsoft.com/beta/` and is permitted only with an ADR per `references/beta-vs-v1-policy.md`. The ADR must include: (1) why v1.0 cannot meet the requirement, (2) the specific beta resource(s) used, (3) a sunset plan to migrate to v1.0 when the resource ships GA, (4) a monitoring trigger that flags the migration when the v1.0 schema appears.

### Step 8: PII Minimization

For every Graph read, list the fields the consumer actually uses. Apply `$select=field1,field2` on every call. Justify any unfiltered read in the spec (it is almost always a smell). Combine with `$filter` to reduce row count and `$top` to cap page size. The combination shrinks PII exposure, reduces throttling cost, and improves latency.

## Validation

### Graph Integration Checklist
- [ ] Permission model declared per operation (application or delegated, never both ambiguously)
- [ ] Scopes are the least-privilege option that meets the requirement (alternatives documented)
- [ ] Endpoint version is v1.0 unless an ADR justifies beta with a sunset plan
- [ ] `$select` applied on every read; field list matches consumer usage
- [ ] `$batch` used wherever five or more sequential calls would otherwise occur
- [ ] Change notifications used in place of polling for state changes
- [ ] `lifecycleNotificationUrl` configured on every long-lived subscription
- [ ] Throttling middleware enabled in SDK; `Retry-After` honoured; jitter present
- [ ] No long-lived client secrets in pipelines; Managed Identity or Workload Identity Federation backs the app registration
- [ ] Subscription expiration tracked; renewal job in place at half the max lifetime
- [ ] Webhook validation token decoded as plain text and returned within 10 seconds
- [ ] Validation tokens (rich notifications) verified per JWT before processing

### Permission Model Sanity Check
- [ ] Daemon callers use application permissions only
- [ ] User-context callers use delegated permissions only
- [ ] Multi-tenant apps validate `tid` and `iss` claims (see identity-decision-tree.md)
- [ ] `Sites.Selected` chosen in preference to `Sites.Read.All` where SharePoint access is per-site
- [ ] Resource-Specific Consent (RSC) used for Teams app permissions where supported

## Handoff Protocol

```markdown
## Handoff: microsoft-graph -> [next skill]
### Decisions Made
- Permission model per actor: [application / delegated table]
- Granular scopes: [list with alternatives considered]
- Endpoint version: [v1.0 / beta with ADR reference]
- Delivery patterns: [batch / change notifications / delta / single]
- SDK: [.NET v5+ / JS v3+ / Python / raw HTTP with justification]
- Throttling strategy: [SDK default middleware / custom retry policy]
### Artifacts: Graph permission table | Subscription lifecycle plan | Batch payload examples | Throttling SLO
### Open Questions: [items for identity-architect, security-architect, threat-model, or m365-platform]
```

## Sibling Skills

- `/azure-architect`: Azure service selection and integration patterns; Graph as a downstream is wired here
- `/identity-architect`: Entra app registration mechanics, Managed Identity binding, Conditional Access on delegated flows; identity decisions feed this skill
- `/security-architect`: Defender for Cloud Apps coverage of Graph, secret hygiene, supply-chain controls on the SDK dependency
- `/m365-platform`: SPFx, Teams apps, SharePoint customizations; consumes the Graph patterns produced here
- `/powerplatform-architect`: Power Platform Graph connectors and Dataverse-Graph integration
- `/d365-architect`: Dynamics 365 cross-tenant Graph reads (rare; usually via Dataverse virtual tables)
- `/ai-architect`: Agent skills that read M365 data; this skill governs the Graph layer those agents call
- `/agent`: Pipeline orchestrator; microsoft-graph is stack-pinned and chains after any vertical needing M365 data
