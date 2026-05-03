---
category: stack-selection
loading_priority: 5
tokens_estimate: 3200
keywords:
  - dynamics 365
  - customer engagement
  - finance and operations
  - business central
  - sales
  - customer service
  - field service
  - supply chain
  - dataverse
  - dual-write
  - virtual entities
  - fit-gap analysis
  - ISV
  - AppSource
  - D365 licensing
  - plugins
  - PCF controls
  - x++
  - chain of command
  - fabric
  - databricks
  - data analytics
version: "1.0"
last_updated: "2026-03-21"
---

# Stack D: Dynamics 365

Stack D provides pre-built ERP and CRM business applications. Unlike Stacks A-C, which build custom applications, Stack D starts with Microsoft's standard business processes and customizes them to fit organizational needs. Stack D always combines with at least Stack A (Power Platform) since Dynamics 365 Customer Engagement runs natively on Dataverse. Complex implementations add Stack B (custom integrations, advanced data) or Stack C (microservices, high-scale compute).

The fundamental principle of Stack D: maximize use of out-of-the-box (OOB) capabilities before customizing. Every customization increases upgrade cost, implementation timeline, and long-term maintenance burden.

## Dynamics 365 Customer Engagement (CE)

CE applications run on Dataverse and use the model-driven app framework. They share a common data model, security model, and extensibility framework.

### D365 Sales

**Opportunity management:** Track sales opportunities from lead qualification through close. Stages map to a Business Process Flow (BPF) that guides sellers through qualification, proposal, negotiation, and close. Custom stages can be added for industry-specific sales processes.

**Forecasting:** Built-in revenue forecasting with configurable forecast categories (Pipeline, Best Case, Committed, Closed). Forecasts roll up the org hierarchy. Manual adjustments enable manager overrides. Snapshots track forecast changes over time for accuracy analysis.

**Sequences:** Automated seller engagement cadences. Define a sequence of activities (email, phone call, task, wait) that sellers follow for each lead or opportunity. Sequences enforce consistent sales methodology and provide activity compliance metrics.

**Copilot for Sales:** AI capabilities embedded in the sales workflow: meeting summarization, email drafting, opportunity summaries, conversation intelligence from Teams calls. Copilot for Sales integrates with Outlook and Teams to capture customer interactions automatically.

### D365 Customer Service

**Case management:** Create, route, and resolve customer service cases. Automatic case creation from email, portal, chat, social channels. Routing rules (basic or unified routing) assign cases to queues or agents based on skills, capacity, and priority.

**Omnichannel:** Unified agent desktop for handling interactions across chat, voice, email, SMS, social media, and Microsoft Teams. Agents see full customer context (previous cases, recent interactions, account details) in a single view. Real-time sentiment analysis helps agents adjust approach.

**Knowledge articles:** Structured knowledge base with lifecycle management (draft, review, publish, archive). Articles support rich text, images, and embedded videos. AI-powered knowledge search suggests relevant articles during case handling. Portal-published articles enable customer self-service.

**Copilot for Customer Service:** Drafts case responses based on knowledge base content. Summarizes case history for agent handoffs. Suggests resolution steps based on similar historical cases.

### D365 Marketing / Customer Insights

**Customer Insights - Journeys (formerly D365 Marketing):** Real-time customer journey orchestration. Trigger-based journeys respond to customer actions (website visit, form submission, email click) with personalized communications. Segment-based journeys target groups with scheduled campaigns.

**Customer Insights - Data:** Customer data platform (CDP) that unifies customer data from multiple sources into unified profiles. Identity resolution merges records from different systems. Segments, measures, and predictions power personalized engagement across all channels.

**Real-time marketing:** Event-based triggers fire within seconds of customer action. Push notifications, SMS, and custom channels extend beyond email. A/B testing optimizes message content and timing. Consent management ensures regulatory compliance (GDPR, CAN-SPAM).

### D365 Field Service

**Work orders:** Manage field service jobs from creation through completion. Work orders capture: service account, incident type (problem category), products consumed, services performed, and technician time. Work order lifecycle: unscheduled -> scheduled -> in progress -> completed -> posted.

**Scheduling:** Resource Scheduling Optimization (RSO) automatically assigns and routes technicians based on skills, location, availability, and priority. Schedule Board provides manual drag-and-drop scheduling. Schedule Assistant suggests optimal technician for a specific work order.

**IoT integration:** Azure IoT Hub integration enables proactive field service. IoT devices report telemetry (temperature, vibration, pressure). Alert rules trigger automatic work order creation when thresholds are breached. Technicians see device telemetry history when arriving on-site.

**Mobile:** Field Service mobile app (model-driven, offline-capable) provides technicians with: work order details, customer history, knowledge articles, inventory lookup, and time/expense capture. Offline mode syncs when connectivity returns. Inspections feature enables configurable checklists.

## Dynamics 365 Finance & Operations (F&O)

F&O applications run on a separate technical stack from CE (Azure SQL-backed, X++ language), though Microsoft is converging the platforms through Dataverse virtual entities and dual-write.

### X++ Development and Customization

F&O customization is done in X++ using Visual Studio with the Dynamics 365 development tools. The extension model (Chain of Command) is the only supported customization approach; overlayering base code is blocked in modern versions.

**Development approach:**
- X++ class extensions with `[ExtensionOf]` attribute to wrap existing methods with pre/post logic
- Table extensions to add custom fields, indexes, and relations
- Form extensions for UI modifications and event handlers
- Data entities as the primary integration surface (OData-enabled CRUD)

**Build and deploy pipeline:**
- Source control in Azure DevOps (Git or TFVC)
- CI/CD pipelines build deployable packages from X++ models
- Deploy through LCS (Lifecycle Services): Dev → Tier 2+ sandbox → Production
- RSAT (Regression Suite Automation Tool) for automated acceptance testing
- One Version model requires extension-based customization to avoid blocking Microsoft updates

**Key patterns:** SysOperation framework for batch operations, business events for external integration, electronic reporting (ER) for configurable documents, feature management for controlled rollout.

### Data Analytics for F&O

F&O data analytics leverages Microsoft Fabric and/or Azure Databricks:

- **Fabric Mirroring**: Continuously replicate F&O database tables to OneLake with near-real-time CDC. No ETL pipelines needed. Enables Power BI DirectLake for instant dashboards over F&O data.
- **Azure Synapse Link for Dataverse**: Export Dataverse-synced F&O data to OneLake for analytics. Strategic replacement for Entity Store (BYOD).
- **Databricks**: Advanced analytics and ML over F&O data exports. Use for demand forecasting, anomaly detection, and custom ML models over financial/supply chain data.
- **Power BI DirectLake**: Query F&O data in OneLake directly without import. Fastest path from F&O operational data to executive dashboards.

### D365 Finance

**General ledger:** Chart of accounts, financial dimensions, journal entries, allocations, consolidation. Multi-company and multi-currency support. Financial reporting (Management Reporter) generates balance sheets, income statements, and custom financial reports.

**Accounts Payable (AP):** Vendor management, purchase invoice processing, three-way matching (PO, receipt, invoice), payment proposals, vendor payment journals. Invoice automation with AI-powered invoice capture from scanned documents.

**Accounts Receivable (AR):** Customer billing, free-text invoices, credit management, collections, payment processing. Revenue recognition for complex contracts (multi-element arrangements, variable consideration).

**Fixed assets:** Asset lifecycle from acquisition through disposal. Depreciation methods (straight-line, declining balance, custom). Asset books for financial and tax reporting. Asset leasing module for IFRS 16/ASC 842 compliance.

**Budgeting:** Budget registers for operating and capital budgets. Budget control prevents over-spending by blocking or warning on transactions that exceed budget. Budget planning workflows for collaborative budget preparation.

### D365 Supply Chain Management

**Procurement:** Purchase requisitions, RFQs, purchase orders, vendor evaluation. Procurement categories and policies enforce compliance. Integration with vendor portals for external collaboration.

**Inventory management:** Multi-warehouse inventory tracking with batch, serial, and license plate dimensions. Inventory visibility service provides real-time cross-channel inventory. Inventory journals for adjustments, transfers, and counting.

**Warehouse management:** Advanced warehousing with mobile device-driven processes. Wave processing for pick, pack, and ship optimization. Slotting for optimal product placement. Integration with material handling equipment (conveyors, sorters) via warehouse app.

**Manufacturing:** Discrete, process, and lean manufacturing modes. Bills of materials (BOMs), routes, production orders, kanban boards. Production scheduling (operations and job scheduling). Quality management with sampling plans and quality orders.

### D365 Human Resources

**Employee self-service:** Leave requests, benefits enrollment, personal information updates, team calendars. Manager self-service for team management, performance reviews, and absence approvals.

**Benefits management:** Open enrollment, life event processing, flexible credit programs. Benefits workspace shows enrollment status, costs, and coverage details.

**Compensation management:** Fixed and variable compensation plans. Compensation events for merit increases, promotions, and adjustments. Budget controls ensure compensation changes stay within allocated budgets.

### D365 Project Operations

**Project-based services:** End-to-end project management for professional services firms. Project contracts, project plans (WBS), resource assignments, time and expense entry, project invoicing.

**Resource management:** Resource requests, resource matching based on skills and availability, resource utilization dashboards. Soft-book and hard-book reservations. Generics for planning before named resources are identified.

## Dynamics 365 Business Central

Business Central (BC) is the SMB ERP offering, covering finance, supply chain, manufacturing, project management, and service management in a single application.

### When BC vs F&O

| Factor | Business Central | Finance & Operations |
|---|---|---|
| Company size | SMB (10-500 employees) | Enterprise (500+ employees) |
| Complexity | Standard business processes | Complex, multi-entity, multi-country operations |
| Manufacturing | Basic (assembly, simple production) | Advanced (discrete, process, lean) |
| Warehouse | Basic (bins, picks, put-aways) | Advanced (wave processing, slotting, MHE integration) |
| Customization language | AL (modern, VS Code-based) | X++ (legacy, Visual Studio-based; migrating to unified platform) |
| Deployment | SaaS-only (cloud) | Cloud-primary; on-premises available (legacy) |
| Cost | $70-$100/user/month | $210/user/month (first); $30/user/month (subsequent) |
| Implementation timeline | 2-4 months (typical) | 6-18 months (typical) |

### AL Language Extensions

Business Central customization uses the AL language in Visual Studio Code. Extensions package customizations as AppSource apps or per-tenant extensions. Extensions modify base application behavior through events (subscribers), page extensions, table extensions, and report extensions without modifying base code. This ensures upgradeability.

### Integration with Power Platform and Azure

BC connects to Power Platform through: Power Automate connectors (trigger flows on BC events), Power BI templates (pre-built financial and operational reports), and Power Apps (custom UI over BC APIs). BC exposes standard REST APIs (OData v4) and custom API pages for programmatic access.

## D365 Solution Architecture Composition

When solutioning on Dynamics 365, the platform is never used in isolation. D365 is always composed with surrounding Microsoft platforms. Use `AskUserQuestion` to determine the user's composition pattern.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│  FRONT OFFICE (User-Facing)                             │
│  Power Pages portal | Model-driven apps | Canvas apps   │
│  TanStack React custom portals (Stack B/C)              │
├─────────────────────────────────────────────────────────┤
│  BACK OFFICE (Business Operations)                      │
│  D365 CE: Sales, Service, Field Service, Project Ops    │
│  D365 F&O: Finance, Supply Chain, HR, Warehouse         │
│  D365 Customer Insights: Data + Journeys (Marketing)    │
├─────────────────────────────────────────────────────────┤
│  PROCESS AUTOMATION (Orchestration)                     │
│  Power Platform: Power Automate + Copilot Studio        │
│  Dual-write (CE ↔ F&O real-time sync)                   │
├─────────────────────────────────────────────────────────┤
│  INTEGRATION LAYER (Best-of-Breed)                      │
│  Azure: Logic Apps + Azure Functions + API Management   │
│  Web Application Firewall (WAF) for public endpoints    │
│  Service Bus / Event Grid for async messaging           │
├─────────────────────────────────────────────────────────┤
│  DATA PLATFORM (Analytics & AI)                         │
│  Microsoft Fabric: Data Factory + Lakehouse + Warehouse │
│  Azure Databricks: Advanced ML + data engineering       │
│  Azure ML: Forecasting + ML-based workloads             │
│  Power BI: Visualization (DirectLake over Fabric)       │
└─────────────────────────────────────────────────────────┘
```

### Composition Patterns (Ask User)

When Stack D is selected, ask the user which composition pattern applies:

**Pattern D1: D365 + Power Platform only (D+A)**
- D365 CE/F&O as back office
- Power Platform for process automation (Power Automate flows)
- Power Pages for external portals (customer/vendor self-service)
- Model-driven apps for custom front-office experiences
- Canvas apps for task-specific mobile/tablet experiences
- Dual-write for CE ↔ F&O synchronization
- Power BI for analytics (import/DirectQuery to Dataverse)
- **Best for**: Standard business processes, minimal external integration

**Pattern D2: D365 + Power Platform + Azure Integration (D+A+B)**
- Everything in D1, plus:
- Azure Logic Apps for complex B2B integrations (EDI, partner APIs, legacy systems)
- Azure Functions for custom business logic exposed via API Management
- API Management (APIM) as the integration gateway with WAF protection
- Service Bus for reliable async messaging between D365 and external systems
- Azure Data Factory for bulk data migration and ETL from legacy ERP/CRM
- **Best for**: Enterprise with best-of-breed integrations, external partner APIs, legacy migration

**Pattern D3: D365 + Power Platform + Azure + Data Platform (D+A+B+Fabric/Databricks)**
- Everything in D2, plus:
- Microsoft Fabric as the unified data platform:
  - Data Factory pipelines for cross-system data orchestration
  - Lakehouse for operational + analytical data convergence
  - Fabric Mirroring for near-real-time F&O data replication to OneLake
  - Synapse Link for Dataverse → OneLake (CE data)
  - Data Warehouse (T-SQL) for cross-system analytics
  - Power BI DirectLake for zero-import dashboards
- Azure Databricks (optional, for advanced scenarios):
  - ML-based demand forecasting over supply chain data
  - Anomaly detection on financial transactions
  - Custom Spark jobs for complex data transformations
  - Unity Catalog governance over D365 + external data
- Azure ML for predictive workloads (churn prediction, lead scoring, inventory optimization)
- **Best for**: Data-driven enterprises, advanced analytics, ML/AI use cases

**Pattern D4: D365 + Full Stack (D+A+B+C+Fabric)**
- Everything in D3, plus:
- Container workloads (AKS/Container Apps) for:
  - High-throughput integration brokers
  - Custom microservices that complement D365 (e.g., pricing engine, tax calculation)
  - Event-driven processing at scale
  - Polyglot services (Go for system, .NET for business logic, Python for ML)
- **Best for**: Large-scale enterprises with complex, high-volume integration needs

### Front Office Patterns

D365 is always the back office. The front office (user-facing) is built with:

| Front Office Need | Recommended Approach | Technology |
|---|---|---|
| Customer self-service portal | Power Pages | Model-driven, authenticated, Dataverse-backed |
| Vendor/partner portal | Power Pages + custom entities | Partner-specific views, approval workflows |
| Internal departmental app | Model-driven app | Custom app module over D365 entities |
| Mobile field app | Canvas app or D365 mobile | Offline-capable, camera/GPS |
| Custom branded portal | TanStack React + Dataverse Web API | Full design control, Stack B required |
| E-commerce storefront | D365 Commerce or custom (Stack B/C) | Full retail capabilities or headless commerce |

### Data Platform for D365

When D365 is the back office, the data layer follows this architecture:

```
D365 CE (Dataverse) ──→ Synapse Link ──→ OneLake (Fabric)
                                              │
D365 F&O (SQL) ──→ Fabric Mirroring ────→ OneLake (Fabric)
                                              │
External Systems ──→ Data Factory ──────→ OneLake (Fabric)
                                              │
                                    ┌─────────┴──────────┐
                                    │                     │
                              Fabric Warehouse      Databricks
                              (T-SQL analytics)    (ML/Advanced)
                                    │                     │
                                    └─────────┬──────────┘
                                              │
                                         Power BI
                                      (DirectLake)
```

**Key decisions for the user:**
1. **Fabric only** (most common): Use for unified analytics, self-service BI, standard reporting
2. **Fabric + Databricks**: Use when advanced ML, custom Spark, or multi-cloud data strategy is needed
3. **Databricks only** (rare for D365): Only when organization is Databricks-standardized and wants single platform

## Integration with Power Platform

### Native Dataverse Connection

D365 CE applications (Sales, Customer Service, Marketing, Field Service) run natively on Dataverse. Their entities (Account, Contact, Opportunity, Case, Work Order) are Dataverse tables. Power Platform components access CE data directly without connectors or APIs.

### Model-Driven Apps Extending D365

Create custom model-driven apps that surface D365 CE entities alongside custom entities. Example: a Partner Management app that shows Accounts (from D365 Sales), Cases (from D365 Customer Service), and custom Partner Agreement entities in a unified experience. Custom app modules control which entities, forms, views, dashboards, and sitemap navigation users see.

### Power Automate Flows Triggered by D365 Events

Common automation patterns:
- Opportunity stage change triggers notification to finance team.
- Case created with high priority triggers escalation workflow.
- Work order completed triggers customer satisfaction survey.
- Invoice approved in F&O triggers payment notification in CE.

Use Dataverse connector triggers (When a row is added, modified, or deleted) for CE events. Use F&O connector or Business Events for F&O triggers.

### Power BI Dashboards Over D365 Data

Pre-built Power BI template apps provide immediate analytics for each D365 module. Custom dashboards connect to Dataverse via the TDS (Tabular Data Stream) endpoint for real-time CE data. For F&O data, use Azure Synapse Link for Dataverse or Entity Store (BYOD) for analytical queries without impacting transactional performance.

## Data Integration Patterns

### Dual-Write

Real-time bidirectional synchronization between Dataverse (CE) and F&O. Dual-write maps specific tables between platforms with row-level sync triggered by create/update events. Latency is near-real-time (seconds).

**When to use:** Customer/vendor master sync (Account in CE maps to Customer/Vendor in F&O), product catalog sync, sales order flow from CE to F&O. Dual-write is the strategic integration for organizations running both CE and F&O.

**Limitations:** Not suitable for bulk/batch data. Initial data sync for large tables requires careful planning. Conflict resolution can be complex for bidirectional updates to the same field.

### Virtual Entities

Virtual entities expose external data in Dataverse without data replication. F&O entities appear as Dataverse tables; queries are executed in real-time against F&O. Users interact with virtual entities in model-driven apps as if the data were native to Dataverse.

**When to use:** Read-heavy scenarios where F&O data needs to be visible in CE but does not need to be stored in Dataverse. Examples: viewing inventory levels from CE, looking up F&O vendor details from a CE form.

**Limitations:** Virtual entities are read-only in most scenarios (write-back is limited). Performance depends on F&O API response time. Not suitable for offline scenarios or complex filtering.

### Data Export Service

Near-real-time replication of Dataverse data to Azure SQL Database. Data Export Service maintains a synchronized copy of selected Dataverse tables in an Azure SQL database. Analytical workloads query Azure SQL instead of Dataverse, preserving platform API limits for transactional use.

**When to use:** Reporting and analytics that require SQL query flexibility beyond what Dataverse views and FetchXML provide. Useful for cross-referencing D365 data with non-D365 data in a common SQL environment.

**Note:** Data Export Service is being superseded by Azure Synapse Link for Dataverse for new implementations.

### Dataverse Web API

RESTful API for programmatic access to Dataverse data. Supports CRUD operations, batch requests, function/action invocation, and change tracking. Used by custom applications (App Service APIs, Azure Functions) to read and write D365 CE data.

**Authentication:** OAuth 2.0 with Entra ID (Azure AD). Application user (S2S) for background services; delegated user for applications acting on behalf of users.

**Throttling:** 6,000 API requests per 5 minutes per user. Use batch operations (up to 1,000 requests per batch) to maximize throughput. Implement retry with exponential backoff on 429 (Too Many Requests) responses.

### Azure Synapse Link for Dataverse

Continuous data export from Dataverse to Azure Synapse Analytics (formerly Azure Data Lake). Provides a managed data pipeline for analytics at scale without impacting Dataverse performance.

**When to use:** Enterprise analytics, data warehousing, machine learning training data, cross-system reporting that combines D365 data with other enterprise data. This is the strategic pattern for large-scale D365 analytics, replacing both Data Export Service and BYOD for new implementations.

**Architecture:** Dataverse change data flows to Azure Data Lake Storage (Parquet format) via managed pipeline. Azure Synapse serverless SQL pool queries Parquet files directly. Power BI connects to Synapse for reporting.

## Fit-Gap Analysis for D365

Fit-gap analysis determines how well D365 OOB capabilities match business requirements. The analysis categorizes each requirement into one of five levels, with strong preference for earlier levels.

### OOB (Out-of-the-Box)

Standard functionality that requires no changes. D365 entities, forms, views, business rules, workflows, and dashboards used as delivered. Examples: basic case management, standard opportunity pipeline, inventory transactions.

**Always start here.** Adjust business processes to match the software when the OOB capability is functionally equivalent. Do not customize for user preference alone; reserve customization for genuine business needs.

### Configuration

Changes made through the application's administrative UI without code. Examples: security roles and business unit hierarchy, form layout adjustments (reorder fields, show/hide sections), view definitions and chart configurations, option set values, business process flow modifications, email templates, SLA definitions.

**Safe and upgrade-compatible.** Configuration changes ride through platform upgrades without rework.

### Customization

Changes that require developer tools but stay within the supported extensibility framework. These are upgrade-compatible if built within supported boundaries.

**Plugins (C#):** Server-side business logic triggered on Dataverse operations (Create, Update, Delete, Retrieve). Register plugins on pre-validation (before platform validation), pre-operation (before database write, within transaction), or post-operation (after database write) stages. Use plugins for: complex validation spanning multiple tables, auto-numbering, integration event publishing, data transformation.

**JavaScript web resources:** Client-side form scripting for model-driven app forms. Use for: dynamic form behavior beyond business rules, calling external APIs from the form, custom notifications, field formatting. Register on form events (OnLoad, OnSave) or field events (OnChange).

**Custom workflow activities:** Reusable C# code blocks invocable from Power Automate cloud flows or classic workflows. Use for: complex computations, external system calls, data transformations that need to be reusable across multiple flows.

**PCF (PowerApps Component Framework) controls:** Custom UI controls that replace standard form controls. Use for: data visualization (charts, maps, timelines), specialized input (color pickers, rich text, multi-select), embedded experiences (iframe wrappers with enhanced integration). PCF controls render in model-driven apps, canvas apps, and Power Pages.

### ISV Solutions

Third-party solutions from the AppSource marketplace that extend D365 with specialized functionality.

**Evaluation criteria for ISV solutions:**
- **Functional fit:** Does the ISV solution cover the gap without over-engineering? Evaluate features against requirements, not marketing material.
- **Certification:** Is the solution Microsoft-certified on AppSource? Certification verifies quality, security, and supportability standards.
- **Vendor viability:** Is the ISV financially stable with a track record? Check customer references in your industry.
- **Update cadence:** Does the ISV release updates compatible with D365 wave releases? Lagging ISV updates block platform upgrades.
- **Support model:** What SLA does the ISV provide? Is support available in your time zones and languages?
- **Data model impact:** Does the ISV add custom tables that integrate cleanly with standard D365 entities, or does it create a parallel data model?
- **License cost:** Per-user, per-transaction, or flat fee? How does ISV licensing compound with D365 base licensing?
- **Exit strategy:** What happens if you discontinue the ISV solution? Is data exportable? Are customizations dependent on the ISV's proprietary components?

### Extend (Custom Development)

Fully custom development for requirements that cannot be met through OOB, configuration, customization, or ISV solutions. Custom web applications (Stack B/C), custom integrations, bespoke functionality.

**Last resort.** Every custom extension increases implementation cost, upgrade risk, and maintenance burden. Document the business justification for each custom extension and reassess annually whether D365 platform evolution has made the custom component unnecessary.

## ISV Ecosystem and AppSource

AppSource is Microsoft's marketplace for business applications. Categories relevant to D365:

- **Industry solutions:** Vertical accelerators for healthcare, financial services, manufacturing, retail, nonprofit.
- **Functional extensions:** Document management, electronic signatures, address validation, tax calculation, advanced pricing.
- **Integration connectors:** Pre-built integrations to popular SaaS platforms (Salesforce migration, SAP integration, Shopify sync).
- **Analytics:** Pre-built Power BI template apps, AI/ML solutions for forecasting and anomaly detection.

**ISV due diligence process:**
1. Define requirements the ISV solution must address.
2. Shortlist 2-3 ISV solutions from AppSource.
3. Request demo in a sandbox environment with your data.
4. Check references (at least 2 customers in similar scale/industry).
5. Review ISV's D365 certification status and version compatibility.
6. Negotiate licensing terms, including renewal pricing and user tier thresholds.
7. Test in a dedicated trial environment for 2-4 weeks before committing.

## D365 Licensing Model

### Per-User Licenses

Most D365 applications are licensed per-user:

| Application | Professional | Enterprise | Notes |
|---|---|---|---|
| Sales | $65/user/month | $105/user/month | Professional lacks sequences, forecasting, LinkedIn integration |
| Customer Service | $50/user/month | $105/user/month | Professional lacks omnichannel, unified routing |
| Field Service | -- | $105/user/month | Single tier |
| Marketing (Customer Insights - Journeys) | -- | $1,500/tenant/month | Capacity-based, not per-user |
| Customer Insights - Data | -- | $1,700/tenant/month | Capacity-based (unified profiles) |
| Finance | $210/user/month (base) | $30/user/month (attach) | Attach pricing for subsequent users |
| Supply Chain | $210/user/month (base) | $30/user/month (attach) | Attach pricing for subsequent users |
| Human Resources | $120/user/month | -- | Single tier |
| Business Central Essentials | $70/user/month | -- | Core financials, supply chain |
| Business Central Premium | $100/user/month | -- | Adds manufacturing, service management |
| Project Operations | $120/user/month | -- | Single tier |

### Team Member Licenses

$8/user/month. Limited functionality: read access to all D365 data, light write access (time/expense entry, approval actions, personal information updates). Use Team Member licenses for employees who need visibility into D365 data but do not perform primary business operations.

### Per-Device Licenses

Available for scenarios where multiple users share a device (kiosk, shop floor terminal). One license per device regardless of user count. Pricing varies by application.

### Capacity Add-Ons

- **Dataverse database capacity:** $40/GB/month above included entitlements.
- **Dataverse file capacity:** $2/GB/month.
- **Dataverse log capacity:** $10/GB/month.
- **AI Builder credits:** Included with some D365 licenses; additional capacity at $500/1M credits/month.
- **Power Automate unattended RPA:** $150/bot/month.
- **Power Pages authenticated users:** $100/100 users/month.

### Licensing Optimization Strategies

- **Attach pricing:** After the first D365 app license (base), subsequent D365 apps for the same user qualify for attach (discounted) pricing. Strategy: license the most expensive app as the base; attach others.
- **Team Member maximization:** Audit user roles to identify users who only need read access or light write. Move them to Team Member licenses.
- **Enterprise Agreement negotiations:** Organizations with 500+ users should negotiate EA pricing directly with Microsoft. Volume discounts can reduce per-user costs by 15-30%.
- **Trial and sandbox licensing:** Non-production environments use separate licensing. Developer environments are free for individual developers. Sandbox environments may require reduced-cost licenses depending on EA terms.
- **License true-up:** D365 licenses are assigned, not concurrent. Ensure license counts match actual named users. Run quarterly license audits using the Power Platform admin center and D365 admin center reports.
