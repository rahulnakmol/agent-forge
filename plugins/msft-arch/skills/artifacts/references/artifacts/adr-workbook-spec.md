---
category: artifacts
loading_priority: 2
tokens_estimate: 1800
keywords:
  - ADR
  - architecture decision record
  - workbook
  - xlsx
  - design decisions
  - ADR reference number
  - status tracking
version: "1.0"
last_updated: "2026-03-21"
---

# ADR Workbook Specification

This document defines the complete specification for the Architecture Decision Records (ADR) Excel workbook. The ADR Workbook is generated during Phase 3 (Design) and captures every architectural decision with full context, rationale, consequences, and status.

## Sheet: "Architecture Decisions"

### Column Specifications

#### Column A: ADR Ref No (width: 30)

**Format:** `MS-[TECH]-[PLATFORM]-[PROJECT]-XXX`

| Segment   | Values                                                       |
| --------- | ------------------------------------------------------------ |
| TECH      | AI, DATA, INT, SEC, INFRA, APP                                |
| PLATFORM  | PP (Power Platform), AZURE, D365, M365, ENTRA                |
| PROJECT   | Uppercase, no spaces (e.g., CALLCENTER, ANALYTICS, FIELDOPS) |
| XXX       | Sequential zero-padded integer: 001, 002, 003...              |

**Examples:**
- `MS-AI-AZURE-CALLCENTER-001`
- `MS-INT-D365-FIELDOPS-003`
- `MS-SEC-ENTRA-ANALYTICS-001`

#### Column B: Title (width: 40)

- Concise decision statement.
- Must start with a verb: **Adopt**, **Use**, **Implement**, **Select**, **Configure**, **Deploy**, **Enable**, **Migrate**.
- Keep under 80 characters.
- Examples:
  - "Adopt Azure OpenAI with RAG Pattern for Customer Service Copilot"
  - "Use Entra ID Conditional Access for Zero-Trust Authentication"
  - "Implement Dataverse as Unified Data Store for D365 CE"

#### Column C: Context (width: 60, wrap text enabled)

Bullet-point format using line breaks within the cell. Must include the following categories:

```
• Current state: Legacy on-premises CRM with no AI capabilities
• Assumption: Azure OpenAI GPT-4o available in required region
• Consideration: Data sovereignty requirements limit to EU regions
• Constraint: Budget cap of $50k/month for AI services
• Driver: Customer satisfaction scores dropped 15% year-over-year
```

Minimum of 3 bullets per entry. Each bullet is prefixed with `•` followed by a category label and colon.

#### Column D: Decision (width: 50, wrap text enabled)

- State the chosen approach clearly in 2-4 sentences.
- Reference the alternatives that were considered and why they were rejected.
- Example:
  ```
  Adopt Azure OpenAI Service with GPT-4o model using a Retrieval-Augmented Generation (RAG) pattern backed by Azure AI Search. AWS Bedrock was considered but rejected due to existing Microsoft EA and Azure-first strategy. On-premises LLM hosting was rejected due to GPU infrastructure costs exceeding $200k annually.
  ```

#### Column E: Consequence (width: 60, wrap text enabled)

Structured bullet-point format with labeled sections:

```
Risks Mitigated:
• Reduced customer wait times by 60%
• Eliminated manual ticket routing errors
• Improved first-call resolution rate

Operational Impacts:
• Requires Azure OpenAI monitoring dashboard
• Monthly token usage review process needed
• Team requires prompt engineering training

Trade-offs Accepted:
• Higher per-query cost vs. traditional rule-based routing
• Vendor lock-in to Azure OpenAI service
```

Must include at least "Risks Mitigated" and "Operational Impacts" sections.

#### Column F: Status (width: 20)

Data validation dropdown with the following allowed values:
- **In Design**: Decision is being formulated
- **In Review**: Decision is under stakeholder review
- **Supported**: Decision is approved and active
- **Refreshed**: Decision was revisited and updated
- **Baselines**: Decision is locked into the project baseline

**Color coding:**
| Status     | Background Color |
| ---------- | ---------------- |
| In Design  | Yellow (#FFFF00) |
| In Review  | Orange (#FFA500) |
| Supported  | Green (#00B050)  |
| Refreshed  | Blue (#4472C4)   |
| Baselines  | Gray (#BFBFBF)   |

### Formatting Rules

- **Header row:** Bold, dark blue background (#003366), white text (#FFFFFF), freeze pane on row 1.
- **Alternating row colors:** Odd rows white (#FFFFFF), even rows light gray (#F2F2F2).
- **All text columns (C, D, E):** Wrap text enabled.
- **Auto-filter:** Enabled on all columns (A through F).
- **Font:** Calibri 10pt for data rows, Calibri 11pt bold for headers.
- **Border:** Thin border on all cells, medium border on header row bottom.

### xlsx Skill Invocation Pattern

```
Invoke the xlsx skill to create an Excel workbook with:
- Sheet name: "Architecture Decisions"
- Columns:
  - A: "ADR Ref No" (width: 30)
  - B: "Title" (width: 40)
  - C: "Context" (width: 60, wrap text)
  - D: "Decision" (width: 50, wrap text)
  - E: "Consequence" (width: 60, wrap text)
  - F: "Status" (width: 20)
- Data validation on column F: ["In Design", "In Review", "Supported", "Refreshed", "Baselines"]
- Header formatting: bold, #003366 background, white text
- Freeze top row
- Auto-filter enabled on all columns
- Alternating row colors: white/#F2F2F2
- Data: [provide rows as array of objects]
```

### Example Data Rows

| ADR Ref No                    | Title                                                          | Context                                                                                                                                                                                                              | Decision                                                                                                                                                          | Consequence                                                                                                                                                                                    | Status    |
| ----------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| MS-AI-AZURE-CALLCENTER-001   | Adopt Azure OpenAI with RAG Pattern for Customer Service Copilot | • Current state: Legacy IVR with no AI\n• Assumption: GPT-4o available in EU West\n• Constraint: $50k/month budget cap\n• Driver: CSAT dropped 15% YoY                                                              | Adopt Azure OpenAI with RAG backed by Azure AI Search. AWS Bedrock rejected due to EA alignment. On-prem LLM rejected due to $200k+ GPU costs.                   | Risks Mitigated:\n• 60% reduction in wait times\n• Eliminated manual routing\nOperational Impacts:\n• Monitoring dashboard required\n• Monthly token review needed                             | Supported |
| MS-SEC-ENTRA-CALLCENTER-002  | Use Entra ID Conditional Access for Zero-Trust Authentication    | • Current state: Basic AD authentication\n• Assumption: All users have Entra ID P2 licenses\n• Consideration: MFA fatigue concerns\n• Constraint: Must support B2C guest users                                       | Implement Entra ID Conditional Access with risk-based MFA. Okta considered but rejected for native Microsoft integration benefits and reduced licensing costs.     | Risks Mitigated:\n• Prevents credential-based attacks\n• Complies with ISO 27001\nOperational Impacts:\n• Conditional Access policies need quarterly review\n• Help desk training for MFA issues | In Review |
| MS-DATA-AZURE-CALLCENTER-003 | Implement Azure SQL with Elastic Pools for Multi-Tenant Data     | • Current state: Single SQL Server on-prem\n• Assumption: Peak load 10k concurrent users\n• Consideration: Cost optimization across tenants\n• Driver: 3 new tenants onboarding in Q3                                | Deploy Azure SQL Elastic Pools with per-tenant databases. Cosmos DB evaluated but rejected due to relational query requirements. Managed Instance rejected on cost. | Risks Mitigated:\n• Elastic scaling for tenant spikes\n• Tenant data isolation\nTrade-offs Accepted:\n• Higher complexity vs. single database\n• DTU monitoring overhead                           | In Design |
| MS-INT-D365-CALLCENTER-004   | Select Azure Service Bus for Asynchronous Integration            | • Current state: Point-to-point REST APIs\n• Assumption: Message volume under 1M/day\n• Consideration: Guaranteed delivery required for billing events\n• Constraint: Must integrate with D365 CE and legacy ERP    | Adopt Azure Service Bus Premium tier with topic/subscription pattern. RabbitMQ rejected due to managed service preference. Event Grid evaluated but lacks FIFO guarantee. | Risks Mitigated:\n• Guaranteed message delivery\n• Decoupled system dependencies\nOperational Impacts:\n• Dead-letter queue monitoring required\n• Namespace capacity planning quarterly         | Supported |
