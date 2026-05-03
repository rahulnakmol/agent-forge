# Viva Extensions

**Scope**: Microsoft Viva surface extensibility. Viva Connections (custom cards via SPFx ACEs, dashboard layout, mobile experience), Viva Engage (community apps, custom integrations via Yammer adapters), Viva Topics (knowledge curation hooks), Viva Learning (content provider integrations), Viva Goals (OKR integrations).

**Opinionated rule**: Viva extensions only when there is a real Viva use case (no shoehorning). Viva is the employee experience layer of M365, not a general-purpose UI host. Do not pick Viva because "it looks nice." Pick Viva when the user task naturally lives in the employee homepage (Viva Connections), the corporate social graph (Viva Engage), the curated knowledge graph (Viva Topics), the learning catalog (Viva Learning), or the OKR tree (Viva Goals).

If the use case does not match any of those, build in SharePoint, Teams, or Outlook directly: do not contort it into a Viva extension.

## Viva Connections

The Viva Connections dashboard is the primary extensibility surface. Custom cards (Adaptive Card Extensions, ACEs) plug into the dashboard alongside Microsoft cards.

Build with SPFx 1.20+:

- Card View templates (1.20+ catalog): Basic, Image, Primary Text, Data Visualization, ImageCard, Dashboard. Choose by content shape (text-heavy, chart, image-led, action-led).
- Quick View options: Adaptive Card Quick View (legacy default, declarative), HTML Quick View (1.20+, full HTML/JS for richer UX).
- Mobile parity: card renders identically on Viva Connections mobile (iOS/Android Teams app). Validate dark mode (`context.app.appInfo.theme` exposed via partial Teams JS SDK in 1.18.1+).
- Dashboard targeting: cards target audiences via SharePoint audience targeting on the dashboard page.

Use SPFx > legacy SharePoint Framework / Add-ins for new SharePoint customizations. ACEs are the only path for Viva Connections custom cards.

Common ACE patterns:

- **Approval card**: Card View shows pending approvals count, Quick View renders the queue with `Action.Execute` buttons backed by a bot.
- **KPI card**: Data Visualization Card View renders a chart from a Graph or REST API call in `onInit`.
- **Quick action card**: Card View shows a single CTA, Quick View collects inputs (start a chat, file a ticket).

## Viva Engage (formerly Yammer)

Viva Engage extensibility:

- **Custom integrations** via Yammer REST APIs: post messages, fetch threads, manage communities. App-only or delegated permissions in Entra ID.
- **Custom apps** via Teams app manifest extensions: surface external content inside Engage communities (similar to Teams tabs).
- **Webhook ingestion**: post external events into Engage as activity stream entries.

Use cases: rolling up community activity into a custom dashboard, syndicating posts from external systems, building a custom moderator tool.

Pre-flight: confirm the tenant has Viva Engage licensed. Yammer brand still appears in some admin surfaces during transition.

## Viva Topics

Viva Topics is in transition (Microsoft 365 Copilot subsumes much of the topic mining). Extensibility today centers on:

- **Topic feedback API** for confirming and rejecting topics programmatically.
- **Knowledge integration** via Graph Connectors: external content with semantic labels feeds into topic candidate generation.
- **Search vertical integration** for surfacing topic pages in Microsoft Search verticals.

Verify Viva Topics availability in the target tenant before scoping: feature changes are ongoing.

## Viva Learning

Viva Learning aggregates content from Microsoft, LinkedIn Learning, and third-party providers. Extensibility:

- **Content provider integration**: register a content source (LRS-like feed) so Viva Learning indexes the catalog.
- **SCORM and xAPI**: standard learning content formats supported as content sources.
- **Custom learning paths**: surfaced via SharePoint lists or Lists app, referenced from Viva Learning home.

Use case: bringing an internal LMS catalog into the Viva Learning home so users see one unified learning surface.

## Viva Goals

Viva Goals extensibility centers on data integration:

- **OKR sync** from external KPI sources (Azure DevOps, Jira, Excel) via built-in or custom integrations.
- **Webhooks** for OKR change events.
- **API** for reading and updating OKRs programmatically.

## Decision tree

```
Is the experience a card on the employee homepage?
  YES -> Viva Connections ACE via SPFx
  NO  -> next question

Is the experience a community feed, conversation, or social graph integration?
  YES -> Viva Engage integration (Yammer API + custom Teams app)
  NO  -> next question

Is the experience a knowledge curation or topic page?
  YES -> Viva Topics (Graph Connectors + topic API). Verify feature availability.
  NO  -> next question

Is the experience a learning catalog or course?
  YES -> Viva Learning content provider integration
  NO  -> next question

Is the experience an OKR or KPI tree?
  YES -> Viva Goals integration
  NO  -> Do NOT use Viva. Build in SharePoint, Teams, or Outlook directly.
```

## Verification with Microsoft Learn MCP

Run `microsoft_docs_search` for:

- `Viva Connections Adaptive Card Extension` for the latest ACE templates and patterns.
- `Viva Engage developer` for current API surface (still labeled as Yammer in some places).
- `Viva Topics` for current availability and Copilot transition guidance.
- `Viva Learning content provider` for integration prerequisites.
- `Viva Goals API` for read/write surface.

## Anti-patterns

- Do not pick Viva Connections for a SharePoint page replacement: keep page-shaped content on a SharePoint page.
- Do not build a custom Yammer client when Viva Engage already covers the experience: integrate, do not replace.
- Do not assume Viva Topics availability: verify per tenant.
- Do not build SCORM content if your audience uses Viva Learning only on web: Viva Learning supports SCORM, but the player UX is consumer-grade. Validate fit.
- Do not skip license check: Viva is a separate license SKU, not bundled with all M365 plans.
