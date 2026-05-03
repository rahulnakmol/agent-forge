---
category: stack-selection
loading_priority: 2
tokens_estimate: 2400
keywords:
  - power platform
  - low-code
  - model-driven apps
  - canvas apps
  - power automate
  - power pages
  - power bi
  - copilot studio
  - dataverse
  - CoE starter kit
  - DLP policies
  - ALM
  - managed environments
version: "1.0"
last_updated: "2026-03-21"
---

# Stack A: Low-Code (Power Platform Only)

Stack A uses Microsoft Power Platform as the sole application platform. It delivers the fastest time-to-market for business applications, the lowest operational burden, and the broadest access to citizen developers. Stack A is the default starting point for all enterprise application requests unless specific technical requirements force a higher stack.

## Model-Driven Apps

Model-driven apps are the primary pattern for data-centric business applications. They auto-generate UI from the Dataverse data model, which means schema changes propagate automatically to forms, views, and dashboards.

**When to use:** Applications that manage structured business data with CRUD operations, approval workflows, role-based access, and reporting. Examples: case management, asset tracking, compliance registers, request management, partner portals (internal).

**Dataverse data modeling principles:**
- Design tables around business entities, not screens. Each table should represent a single business concept (e.g., Inspection, Finding, Corrective Action).
- Use lookup columns for 1:N relationships. Use N:N relationships only when true many-to-many semantics exist.
- Prefer choice columns over related lookup tables for simple enumerated values (status, category, priority).
- Use calculated columns for derived values that depend on data in the same row (e.g., Days Since Created). Use rollup columns for aggregated child data (e.g., Total Line Items Amount).
- Apply alternate keys for natural business identifiers (e.g., Policy Number, Asset Tag) to support upsert operations in integrations.
- Keep table names prefixed with a publisher prefix to avoid naming conflicts with other solutions.

**Business rules:** Apply field-level validation, show/hide fields, set default values, and lock fields based on conditions. Business rules execute on the server (for API-submitted data) and on the client (for form interactions). Use them as the first choice before writing JavaScript.

**Views and dashboards:** Create system views for shared filtered lists. Use personal views for ad-hoc user queries. Build interactive dashboards with visual filters, streams, and charts. Use Power BI embedded dashboards for advanced analytics within the model-driven app shell.

## Canvas Apps

Canvas apps provide pixel-perfect UI control and are the right choice for task-oriented, mobile-first, or highly branded experiences.

**When to use:** Mobile field apps, kiosk interfaces, lightweight task apps, apps that integrate multiple data sources in a single screen, apps requiring custom visual layouts that model-driven forms cannot achieve.

**Connectors:** Canvas apps access over 1,000 pre-built connectors. Standard connectors (SharePoint, Outlook, Excel) are included with base licenses. Premium connectors (SQL Server, HTTP, Dataverse) require Power Apps premium licensing.

**Offline capability:** Canvas apps support offline mode by caching data locally using the `SaveData` and `LoadData` functions. Design offline-capable apps by: (1) loading reference data on app start, (2) queuing write operations locally, (3) syncing on reconnection using conflict resolution logic. Offline works on mobile devices; browser-based canvas apps have limited offline support.

**Responsive design:** Use containers with flexible layouts. Design for the smallest target device first, then use `App.Width` and `App.Height` to conditionally show/hide elements. Avoid absolute pixel positioning; use relative sizing with `Parent.Width` calculations.

**Performance optimization:**
- Use `Concurrent()` to parallelize data calls on screen load.
- Delegate filtering and sorting to the data source; avoid in-memory collection processing for large datasets.
- Limit gallery items with explicit `Top(N)` when full dataset is not needed.
- Use named formulas (App.Formulas) for values computed once at app start.

## Power Pages

Power Pages (formerly Power Apps Portals) expose Dataverse data to external users through authenticated or anonymous web experiences.

**When to use:** Customer self-service portals, partner collaboration sites, community forums, public-facing forms and surveys, external case submission.

**Authentication options:** Local authentication (email/password), Azure AD B2C, OAuth 2.0 providers (Google, Facebook, LinkedIn), SAML 2.0, OpenID Connect. For enterprise external portals, Azure AD B2C (now Entra External ID) is the recommended identity provider.

**Web API:** Power Pages exposes a REST API for Dataverse tables enabled for portal access. Use table permissions to control CRUD access by web role. Apply column permissions for field-level security on the portal.

**Liquid templates:** Custom page layouts use the Liquid templating language. Liquid provides access to Dataverse data, conditional rendering, and iteration. Use Liquid for server-side rendering; use JavaScript for client-side interactivity.

## Power Automate

Power Automate handles process automation across three modalities.

**Cloud flows:**
- *Instant flows:* Triggered manually from apps, buttons, or Teams. Use for on-demand operations like "Submit for Approval" or "Generate Report."
- *Automated flows:* Triggered by events: Dataverse row created/updated, email received, file uploaded, HTTP webhook. Use for event-driven business logic.
- *Scheduled flows:* Run on time-based triggers (recurrence). Use for batch operations: nightly data sync, weekly report generation, daily cleanup.

**Desktop flows (RPA):** Automate legacy applications that have no API. Power Automate Desktop records and replays UI interactions (clicks, keystrokes, screen scraping). Use attended mode for user-assisted automation; unattended mode for fully automated processing on dedicated machines.

**Process mining:** Discover, analyze, and optimize business processes by importing event logs from source systems. Process mining visualizes actual process flows, identifies bottlenecks, and measures cycle times. Use insights to prioritize automation targets.

**Flow design best practices:**
- Use child flows for reusable logic. Parent flows call child flows with input parameters and receive outputs.
- Apply `Configure run after` settings to handle failures gracefully (run after failed, run after timed out).
- Use Scope actions to group related steps and apply error handling at the scope level with try/catch patterns.
- Store configuration values in environment variables, not hardcoded in flow actions.
- Apply concurrency controls on loops to avoid API throttling.

## Power BI

Power BI delivers analytics and reporting across the organization.

**Embedded analytics:** Embed Power BI reports directly in model-driven apps, canvas apps, Teams, and SharePoint. Use row-level security (RLS) to filter data by the signed-in user's role or attributes.

**Paginated reports:** Use Power BI paginated reports (via Report Builder) for pixel-perfect, print-ready documents: invoices, regulatory reports, inventory lists. Paginated reports support parameters, subreports, and export to PDF/Excel/Word.

**Dataflows:** Power BI dataflows perform ETL in the cloud using Power Query Online. Use dataflows to standardize data transformations centrally so multiple reports consume the same prepared dataset.

**Composite models:** Combine DirectQuery (live connection to source) with Import (cached) tables in a single model. Use composite models when some data must be real-time (e.g., current inventory) while other data can be refreshed periodically (e.g., historical sales).

## Copilot Studio

Copilot Studio (formerly Power Virtual Agents) builds conversational AI agents.

**Agent patterns:** Design agents for specific business scenarios: IT helpdesk, HR FAQ, customer support triage, order status lookup. Each agent contains topics (conversation paths) triggered by user phrases.

**Topics and generative AI:** Classic topics use authored conversation trees. Generative answers use a connected knowledge source (SharePoint, website, Dataverse) to answer questions without pre-authored topics. Use generative answers for broad FAQ scenarios; use classic topics for transactional flows (create a ticket, reset a password).

**Plugin actions:** Extend agents with plugin actions that call Power Automate flows, custom connectors, or pre-built connector actions. Plugin actions enable agents to perform write operations (create records, send emails, update statuses) in response to user requests.

## Dataverse

Dataverse is the data backbone of Stack A. Every model-driven app, most canvas apps, and all D365 CE applications store data in Dataverse.

**Data model design:** Follow a normalized schema. Tables represent entities; columns represent attributes; relationships represent associations. Use standard tables (Account, Contact, Activity) when they fit the business concept to leverage pre-built features (timeline, connections, activities).

**Relationships:**
- 1:N (Lookup): Parent-child. Cascade behaviors define what happens to child rows when parent is reassigned, deleted, or shared.
- N:N: Junction table auto-created by the platform. Use for peer associations (e.g., Skill-to-Employee).

**Calculated and rollup fields:** Calculated fields compute in real-time from same-row data. Rollup fields aggregate child data on a schedule (every 12 hours by default, or on-demand via the recalculate button). Plan rollup refresh timing into your SLA commitments.

**Business rules:** Server-side logic that validates data on create/update. Business rules apply regardless of whether data enters through the UI, API, or import. Use business rules for field-level validation; use plugins for complex multi-table logic.

## Governance

**CoE Starter Kit:** A set of Power Platform solutions that provide visibility into tenant-wide Power Platform usage. Components include: inventory (apps, flows, connectors), analytics dashboards, cleanup policies for orphaned apps, and developer compliance workflows.

**DLP policies:** Data Loss Prevention policies control which connectors can be used together. Group connectors into Business, Non-Business, and Blocked categories. Apply DLP policies at the tenant or environment level. Strategy: create a restrictive tenant-level policy, then create more permissive environment-level policies for trusted maker groups.

**Environment strategy:** Use separate environments for dev, test, UAT, and production. Apply managed environments for production workloads to enable: pipeline enforcement, sharing limits, solution checker enforcement, and weekly digest emails. Use developer environments (free, per-developer) for experimentation.

## ALM (Application Lifecycle Management)

**Solutions:** Package all customizations (tables, apps, flows, security roles) into Dataverse solutions. Use a single publisher for your organization. Use segmented solutions for large projects (core data model, app module, integration flows).

**Environment variables:** Store configuration values (URLs, feature flags, thresholds) as environment variables within solutions. Values are set per-environment during deployment, avoiding hardcoded references.

**Connection references:** Abstract connection identity from solution components. When a solution is deployed to a new environment, connection references are mapped to environment-specific connections without modifying the solution.

**Pipelines:** Power Platform pipelines automate solution deployment across environments. Configure pipeline stages (dev -> test -> prod) with approval gates. Pipelines export managed solutions, validate with solution checker, and import to target environments.

## Limitations and Ceiling Indicators

Stack A has explicit boundaries. Monitor these triggers to know when to escalate to Stack B:

- **Custom API requirements:** Available connectors do not cover the target system, and the custom connector framework (HTTP-based, OpenAPI definition) cannot handle the integration complexity (e.g., requires WebSocket, gRPC, or long-running connections).
- **User scale:** Application usage exceeds 2,000 concurrent active users, or API request limits (6,000 requests per 5 minutes per user) are consistently hit even after optimization.
- **Computational complexity:** Business logic requires complex algorithms, machine learning inference, large file processing, or real-time stream processing that Power Fx and cloud flows cannot perform efficiently.
- **Data volume:** Dataverse table approaching millions of rows with degrading query performance despite indexing and view optimization.
- **Integration patterns:** Need for pub/sub messaging, event streaming, guaranteed delivery queues, or complex orchestration with compensation logic that Power Automate's sequential flow model cannot express cleanly.
- **Custom UI requirements:** Front-end needs exceed canvas app capabilities (e.g., real-time collaboration, 3D rendering, complex data visualization, embedded video processing).

When any of these ceilings are hit, the specific bottleneck determines which Azure PaaS service from Stack B addresses it. Do not move entirely to Stack B; instead, add only the Azure services needed to resolve the specific limitation.
