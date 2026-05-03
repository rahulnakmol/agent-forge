---
category: requirements
loading_priority: 1
tokens_estimate: 4500
keywords: [requirements, elicitation, questions, business process, integration, data, security, compliance, performance, scalability, user experience, reporting, analytics, SMART, AskUserQuestion]
version: 1.0
last_updated: 2026-03-21
---

# Requirements Gathering Question Bank

## Purpose

This reference provides a structured question bank for conducting requirements elicitation via `AskUserQuestion`. Questions are organized by category and designed to be asked in batches of 2-3 for efficient gathering sessions. Each question targets a specific architectural concern that influences stack selection and solution design.

## Requirement ID Format

All requirements must follow the standard ID format:

```
REQ-[CATEGORY]-[NNN]
```

| Category Code | Domain |
|---|---|
| `BP` | Business Process Requirements |
| `INT` | Integration Requirements |
| `DAT` | Data Requirements |
| `SEC` | Security and Compliance Requirements |
| `PRF` | Performance and Scalability Requirements |
| `UX` | User Experience Requirements |
| `RPT` | Reporting and Analytics Requirements |

Examples: `REQ-BP-001`, `REQ-INT-003`, `REQ-SEC-012`

## Requirement Quality Criteria (SMART)

Every captured requirement must satisfy all five SMART criteria before being accepted:

- **Specific**: Clearly defines what is needed without ambiguity. Avoid vague language like "fast" or "user-friendly"; quantify instead.
- **Measurable**: Includes acceptance criteria or metrics that allow objective verification. Example: "Page load time under 2 seconds at P95."
- **Achievable**: Technically feasible within the selected stack and project constraints (timeline, budget, team skills).
- **Relevant**: Directly tied to a business objective or user need. Each requirement should trace to a business goal.
- **Traceable**: Linked to its source (stakeholder, regulation, business process) and downstream artifacts (design decisions, test cases, user stories).

## Batching Strategy for AskUserQuestion

When using `AskUserQuestion`, batch related questions in groups of 2-3 to minimize round trips while keeping cognitive load manageable for the stakeholder:

- **Opening batch**: Start with high-level business context (BP questions 1-3)
- **Follow-up batch**: Drill into specifics based on initial answers
- **Cross-cutting batch**: Combine questions from different categories that relate to the same business area (e.g., ask about a process, its data volume, and its security classification together)
- **Validation batch**: Confirm assumptions and resolve ambiguities from earlier answers

Format each batch as a numbered list within a single `AskUserQuestion` call. Provide brief context for why each question matters.

---

## Category 1: Business Process Requirements

Questions to understand the core business workflows the solution must support.

### Questions

1. **What are the core business processes this solution must support?**
   - Intent: Identify the primary workflows to model. Drives domain decomposition and bounded context design.
   - Follow-up: Ask for process flow diagrams or written SOPs if available.

2. **Which processes are manual today that should be automated?**
   - Intent: Quantify automation opportunity. Manual processes with high volume or error rates are prime automation candidates.
   - Follow-up: What is the current error rate and time spent on each manual process?

3. **What are the key business rules and validation logic?**
   - Intent: Capture domain logic that must be enforced by the system. Complex rules influence whether low-code (Stack A) or pro-code (Stack B/C) is appropriate.
   - Follow-up: Are rules static or do they change frequently? Who manages rule changes?

4. **Who are the primary user personas and their workflows?**
   - Intent: Define user segments, their goals, and interaction patterns. Drives UI/UX decisions and access control design.
   - Follow-up: How many users per persona? What is their technical proficiency?

5. **What approval workflows exist?**
   - Intent: Map multi-step approval chains. Simple approvals fit Power Automate (Stack A); complex conditional routing may need Logic Apps or custom orchestration (Stack B/C).
   - Follow-up: How many approval levels? Are there delegation rules, escalation timeouts, or parallel approvals?

6. **What are the reporting and dashboard requirements for business stakeholders?**
   - Intent: Understand operational visibility needs. Determines whether embedded Power BI, custom dashboards, or D365 analytics are needed.
   - Follow-up: Who consumes reports? What decisions do they drive? Real-time or periodic refresh?

7. **What are the SLA commitments for each business process?**
   - Intent: Establish availability and recovery requirements per process. Critical processes may need higher-tier infrastructure.
   - Follow-up: What is the business impact (revenue, compliance, reputation) if a process is unavailable for 1 hour? 4 hours? 24 hours?

### Suggested Batches

- **Batch 1**: Questions 1, 2, 4 (establish scope and users)
- **Batch 2**: Questions 3, 5 (business logic depth)
- **Batch 3**: Questions 6, 7 (operational requirements)

---

## Category 2: Integration Requirements

Questions to map the integration landscape and data flows.

### Questions

1. **What existing systems must this solution integrate with?**
   - Intent: Build the integration map. List all source/target systems with directionality.
   - Follow-up: For each system, who owns it and what is its roadmap (staying, being replaced, being deprecated)?

2. **What are the integration protocols (REST, SOAP, file-based, event-driven)?**
   - Intent: Determine technical integration patterns. REST/event-driven align with modern stacks; SOAP/file-based may need middleware.
   - Follow-up: Are APIs documented? Are there SDKs available?

3. **What are the data exchange volumes and frequencies?**
   - Intent: Size the integration infrastructure. High-volume real-time flows need Service Bus/Event Grid (Stack B); batch files may use simpler connectors.
   - Follow-up: What are peak vs. average volumes? Are there seasonal spikes?

4. **Are there B2B/EDI integration requirements?**
   - Intent: B2B/EDI patterns (AS2, EDIFACT, X12) require specialized middleware such as Azure Integration Account or BizTalk.
   - Follow-up: How many trading partners? What document types?

5. **What authentication/authorization is needed for integrations?**
   - Intent: Determine whether OAuth 2.0, API keys, certificates, or managed identities are needed. Influences APIM and networking design.
   - Follow-up: Are there IP whitelisting requirements? VPN/private connectivity needs?

6. **What error handling and retry requirements exist for integrations?**
   - Intent: Define dead-letter, retry, and compensation patterns. Drives choice between simple connectors and enterprise integration patterns.
   - Follow-up: What is the acceptable data latency? Is eventual consistency acceptable?

### Suggested Batches

- **Batch 1**: Questions 1, 2 (landscape discovery)
- **Batch 2**: Questions 3, 4 (volume and protocol depth)
- **Batch 3**: Questions 5, 6 (non-functional integration requirements)

---

## Category 3: Data Requirements

Questions to understand data characteristics, governance, and lifecycle.

### Questions

1. **What is the estimated data volume (records, storage)?**
   - Intent: Size the data tier. Dataverse has row/storage limits (Stack A); large volumes may need Azure SQL or Cosmos DB (Stack B/C).
   - Follow-up: What is the current size and projected annual growth?

2. **What are the data retention policies?**
   - Intent: Design archival and purge strategies. Regulatory retention periods drive storage architecture and cost planning.
   - Follow-up: Are there different retention periods for different data types?

3. **What data migration is needed from legacy systems?**
   - Intent: Scope the migration effort. Volume, complexity, and transformation rules influence timeline and tooling.
   - Follow-up: Is a big-bang or phased migration preferred? What is the cutover window?

4. **What are the master data management requirements?**
   - Intent: Identify golden record sources and synchronization patterns. MDM complexity influences whether Dataverse or a dedicated MDM solution is needed.
   - Follow-up: Which system is the system of record for each entity (customer, product, employee)?

5. **What data classification levels exist (public, internal, confidential, restricted)?**
   - Intent: Map data sensitivity to storage and access controls. Restricted data may require encryption, tokenization, or dedicated infrastructure.
   - Follow-up: Is there an existing data classification policy? Who classifies data?

6. **What are the data residency requirements?**
   - Intent: Determine geographic constraints on data storage. Drives Azure region selection and multi-geo Dataverse configuration.
   - Follow-up: Are there specific countries/regions where data must or must not reside?

7. **What data quality rules and validation processes are needed?**
   - Intent: Define data quality gates. Automated validation can be built into ingestion pipelines or enforced at the application layer.
   - Follow-up: What is the current data quality baseline? What are the target quality metrics?

### Suggested Batches

- **Batch 1**: Questions 1, 2, 5 (volume, retention, classification)
- **Batch 2**: Questions 3, 4 (migration and MDM)
- **Batch 3**: Questions 6, 7 (residency and quality)

---

## Category 4: Security and Compliance Requirements

Questions to establish the security posture and regulatory obligations.

### Questions

1. **What regulatory frameworks apply (GDPR, HIPAA, SOX, PCI-DSS)?**
   - Intent: Identify compliance mandates that constrain architecture choices. Certain frameworks require specific controls, audit capabilities, and certifications.
   - Follow-up: Has a compliance gap assessment been done? Are there existing audit findings to address?

2. **What authentication method is required (SSO, MFA, certificate-based)?**
   - Intent: Design the identity architecture. Entra ID supports all methods, but complexity varies.
   - Follow-up: Is there an existing identity provider? Are external users (B2B/B2C) in scope?

3. **What role-based access control model is needed?**
   - Intent: Design the authorization matrix. Simple role models fit Dataverse security roles; complex attribute-based access may need custom implementation.
   - Follow-up: How many roles? Is row-level or field-level security needed?

4. **What data encryption requirements exist (at rest, in transit)?**
   - Intent: Determine encryption scope. Azure provides platform encryption by default; customer-managed keys or double encryption are additional requirements.
   - Follow-up: Are there specific key management requirements (HSM, BYOK, hold-your-own-key)?

5. **What audit logging requirements exist?**
   - Intent: Design the audit trail. Dataverse auditing, Azure Monitor, and Microsoft Purview provide different levels of visibility.
   - Follow-up: What is the audit log retention period? Who reviews audit logs and how frequently?

6. **What network security requirements exist?**
   - Intent: Determine whether private endpoints, VNet integration, WAF, or network isolation are needed.
   - Follow-up: Is there an existing hub-spoke network topology? Are there on-premises connectivity requirements?

### Suggested Batches

- **Batch 1**: Questions 1, 2 (compliance and identity)
- **Batch 2**: Questions 3, 4 (authorization and encryption)
- **Batch 3**: Questions 5, 6 (auditing and network)

---

## Category 5: Performance and Scalability Requirements

Questions to establish performance baselines and growth expectations.

### Questions

1. **What is the expected concurrent user count?**
   - Intent: Size the compute and licensing tiers. Power Platform per-user licensing vs. per-app licensing decisions depend on user counts.
   - Follow-up: What is the distribution across user personas?

2. **What are the peak usage patterns?**
   - Intent: Design for burst capacity. Month-end, quarter-end, or seasonal peaks require auto-scaling or reserved capacity.
   - Follow-up: What is the ratio of peak to average load?

3. **What are the acceptable response times for key operations?**
   - Intent: Set performance SLOs per operation. Sub-second requirements may rule out certain low-code approaches.
   - Follow-up: Which operations are latency-sensitive vs. throughput-sensitive?

4. **What throughput is needed (transactions per second)?**
   - Intent: Size the data and compute tiers. High TPS requirements influence database choice and caching strategy.
   - Follow-up: What is the transaction mix (read-heavy vs. write-heavy)?

5. **What growth projections exist for the next 3-5 years?**
   - Intent: Design for scale-out. Architecture must accommodate projected growth without rearchitecting.
   - Follow-up: Are there planned geographic expansions, product launches, or M&A activities that would drive step-function growth?

6. **What are the availability requirements (uptime SLA)?**
   - Intent: Determine the target availability tier (99.9%, 99.95%, 99.99%). Drives redundancy, failover, and DR architecture.
   - Follow-up: Is active-active or active-passive DR required? What is the RPO/RTO?

### Suggested Batches

- **Batch 1**: Questions 1, 2, 3 (user load and performance targets)
- **Batch 2**: Questions 4, 5, 6 (throughput, growth, availability)

---

## Category 6: User Experience Requirements

Questions to define the user interaction model and accessibility needs.

### Questions

1. **What devices must be supported (desktop, tablet, mobile)?**
   - Intent: Determine the UI platform strategy. Mobile-first may favor Canvas apps or PWAs; desktop-heavy may favor Model-driven apps.
   - Follow-up: Are native mobile apps required or is responsive web sufficient?

2. **Are offline capabilities needed?**
   - Intent: Offline support significantly constrains architecture. Power Apps offline mode has limitations; full offline may need a custom solution.
   - Follow-up: What data and operations must be available offline? How is conflict resolution handled?

3. **What accessibility standards apply (WCAG 2.1 AA)?**
   - Intent: Ensure compliance with accessibility regulations. Power Apps has built-in accessibility support but custom UIs need explicit testing.
   - Follow-up: Is accessibility testing part of the acceptance criteria? Are assistive technology users in scope?

4. **What languages and locales must be supported?**
   - Intent: Design for internationalization. Multi-language support influences data model, UI, and content management.
   - Follow-up: Are right-to-left languages needed? What date/number/currency formats are required?

5. **What branding and theming requirements exist?**
   - Intent: Determine the level of UI customization needed. Power Apps theming is limited compared to custom web applications.
   - Follow-up: Is there a design system or component library to follow? Are there multiple brand variants?

### Suggested Batches

- **Batch 1**: Questions 1, 2 (platform and connectivity)
- **Batch 2**: Questions 3, 4, 5 (accessibility, i18n, branding)

---

## Category 7: Reporting and Analytics Requirements

Questions to define the business intelligence and analytics strategy.

### Questions

1. **What operational reports are needed?**
   - Intent: Identify day-to-day reporting needs. Operational reports are typically embedded in the application and refreshed frequently.
   - Follow-up: Who consumes each report? What actions do they take based on it?

2. **What executive dashboards are required?**
   - Intent: Define strategic KPI visibility. Executive dashboards typically aggregate data from multiple sources.
   - Follow-up: What KPIs matter most? How frequently must they refresh?

3. **What self-service analytics capabilities are needed?**
   - Intent: Determine whether business users need ad-hoc query and exploration capabilities beyond fixed reports.
   - Follow-up: What is the analytics maturity of the user base? Do they use Excel, Power BI, or other tools today?

4. **What data export and download requirements exist?**
   - Intent: Define data portability needs. Bulk export may need dedicated pipelines rather than UI-based downloads.
   - Follow-up: What formats are required (CSV, Excel, PDF)? What volume per export?

5. **Are real-time analytics needed vs. batch reporting?**
   - Intent: Real-time analytics require streaming architecture (Event Hubs, Stream Analytics); batch is simpler and cheaper.
   - Follow-up: What is the acceptable data freshness for each report type?

6. **What predictive or prescriptive analytics are needed?**
   - Intent: Determine whether ML/AI capabilities are required. Drives Azure AI services or custom ML model decisions.
   - Follow-up: Are there existing models or algorithms to incorporate?

### Suggested Batches

- **Batch 1**: Questions 1, 2 (operational and strategic reporting)
- **Batch 2**: Questions 3, 4 (self-service and export)
- **Batch 3**: Questions 5, 6 (real-time and advanced analytics)

---

## Requirements Gathering Workflow

### Step 1: Prepare
- Review any existing documentation (RFP, business case, SOW)
- Identify stakeholder roles and schedule elicitation sessions
- Select relevant question categories based on project scope

### Step 2: Elicit
- Use `AskUserQuestion` with batches of 2-3 questions
- Capture answers verbatim before interpreting
- Ask clarifying follow-ups before moving to the next batch

### Step 3: Analyze
- Assign requirement IDs using the `REQ-[CATEGORY]-[NNN]` format
- Validate each requirement against SMART criteria
- Identify conflicts, gaps, and dependencies between requirements

### Step 4: Confirm
- Present the requirements back to the stakeholder for validation
- Resolve any ambiguities or conflicts
- Obtain sign-off before proceeding to fit-gap analysis

### Step 5: Trace
- Link each requirement to its source stakeholder
- Map requirements to architecture decisions
- Feed requirements into the fit-gap analysis (see `fit-gap-analysis.md`)
