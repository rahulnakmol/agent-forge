Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Surface-First Framework Selection** — Picks the correct framework for the surface: SPFx 1.20+ for SharePoint, Microsoft 365 Agents Toolkit (atk CLI) for Teams, Office.js for Office add-ins, Action.Execute for Outlook actionable messages. Never recommends legacy SharePoint Add-ins, VSTO, or Action.Http for new work. Score 5 if surface-appropriate framework is selected; 1 if legacy frameworks are recommended.

2. **Bundle Size Compliance** — Addresses SPFx < 500KB gzipped and Teams app < 1MB total package constraints. Recommends lazy loading, externalized React, or isolated web parts when budgets are exceeded. Score 5 if bundle budget is addressed with concrete mitigation strategies; 1 if bundle size is ignored.

3. **Adaptive Card Portability** — For actionable message scenarios, recommends single Adaptive Card payload across Outlook and Teams using Action.Execute (Universal Action Model) with a bot backend. Avoids Action.Http and custom HTML in Outlook. Score 5 if single-payload approach with Action.Execute is correctly recommended; 1 if Outlook-specific approaches are recommended without Teams reuse.

4. **Graph Connector Schema Completeness** — For M365 Search integration scenarios, designs a Graph Connector with proper semantic labels (title, url, createdBy, lastModifiedBy, iconUrl, containerName), content field for free-text, and urlToItemResolver. Score 5 if connector schema is complete with semantic labels; 1 if connector is described generically without schema specifics.

5. **Identity and Security Handoff** — Correctly identifies when to hand off to identity-architect for SSO configuration (SPFx uses AadHttpClient, Teams uses SSO via Toolkit, Office add-ins use getAccessToken). Correctly identifies when to hand off to microsoft-graph for permission scoping. Score 5 if cross-cutting concerns are properly identified and handed off; 1 if identity and permissions are handled inline without proper patterns.
