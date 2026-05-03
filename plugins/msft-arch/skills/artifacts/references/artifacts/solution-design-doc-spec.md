---
category: artifacts
loading_priority: 2
tokens_estimate: 1400
keywords:
  - solution design
  - component mapping
  - technology selection
  - workbook
  - xlsx
  - NFR
  - integration points
  - data flow
  - stack selection
version: "1.0"
last_updated: "2026-03-21"
---

# Solution Design Document Workbook Specification

This document defines the complete specification for the Solution Design Document Excel workbook. The workbook is generated during Phase 3 (Design) and maps solution components to Microsoft technologies, linking each to its governing ADR, non-functional requirement coverage, and integration topology.

## Sheet: "Solution Design"

### Column Specifications

#### Column A: Section (width: 25)
- HLD section name that groups related components.
- Standard sections:
  - Application Architecture
  - Integration Architecture
  - Data Architecture
  - Security Architecture
  - Infrastructure Architecture
  - AI & Cognitive Services
  - Identity & Access Management
  - Monitoring & Operations
- Used for row grouping and outline levels.

#### Column B: Component (width: 30)
- The solution component or service capability being designed.
- Use clear, specific names that a technical stakeholder can immediately understand.
- Examples: "API Gateway", "Identity Provider", "Message Broker", "Vector Store", "Data Lake", "CI/CD Pipeline".

#### Column C: Technology (width: 30)
- The specific Microsoft service or technology selected for this component.
- Use official Microsoft service names.
- Examples: "Azure API Management", "Entra ID", "Azure Service Bus", "Azure AI Search", "Azure Data Lake Storage Gen2", "Azure DevOps Pipelines".

#### Column D: Stack (width: 10)
- Data validation dropdown indicating the recommended technology stack tier:
  - **A**: Primary recommended stack (best fit, fully validated)
  - **B**: Alternative stack (viable, minor trade-offs)
  - **C**: Conditional stack (suitable under specific constraints)
  - **D**: Not recommended (included for completeness, significant trade-offs)

**Conditional formatting:**
| Stack | Background Color  |
| ----- | ----------------- |
| A     | Green (#00B050)   |
| B     | Blue (#4472C4)    |
| C     | Yellow (#FFFF00)  |
| D     | Red (#FF0000)     |

#### Column E: Design Decision (width: 50, wrap text enabled)
- Summary of the key design decision for this component.
- Keep to 2-3 sentences explaining the "what" and "why."
- Should align with the corresponding ADR entry.

#### Column F: Referenced ADR (width: 25)
- ADR Ref No from the ADR Workbook.
- Format: `MS-[TECH]-[PLATFORM]-[PROJECT]-XXX`.
- Every component should reference at least one ADR. Multiple ADRs separated by semicolons.

#### Column G: NFR Coverage (width: 35)
- Non-functional requirements addressed by this component.
- Multi-value field; values separated by comma and space.
- Allowed values: **Reliability**, **Security**, **Performance**, **Cost**, **Ops** (Operational Excellence).
- Example: "Reliability, Security, Performance".

#### Column H: Integration Points (width: 40, wrap text enabled)
- Upstream and downstream systems that this component connects to.
- Format: directional description.
- Example:
  ```
  Upstream: D365 CE (customer data)
  Downstream: Power BI (analytics feed)
  Lateral: Azure Service Bus (event mesh)
  ```

#### Column I: Data Flow (width: 15)
- Data validation dropdown:
  - **Inbound**: Component receives data from external systems
  - **Outbound**: Component sends data to external systems
  - **Bidirectional**: Component both sends and receives data

### Formatting Rules

- **Header row:** Bold, dark blue background (#003366), white text (#FFFFFF), freeze pane on row 1.
- **Alternating row colors:** Odd rows white (#FFFFFF), even rows light gray (#F2F2F2).
- **Row grouping:** Group rows by Column A (Section) using Excel outline/grouping.
- **Conditional formatting:** Applied to Column D (Stack) with colors defined above.
- **Wrap text:** Enabled on Columns E, H.
- **Auto-filter:** Enabled on all columns (A through I).
- **Font:** Calibri 10pt for data rows, Calibri 11pt bold for headers.

### Example Data Rows

| Section                    | Component              | Technology                  | Stack | Design Decision                                                                                                    | Referenced ADR                | NFR Coverage                      | Integration Points                                                                  | Data Flow     |
| -------------------------- | ---------------------- | --------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------- | --------------------------------- | ----------------------------------------------------------------------------------- | ------------- |
| AI & Cognitive Services    | Customer Service Copilot | Azure OpenAI Service        | A     | Deploy GPT-4o with RAG pattern for AI-assisted agent responses. Chosen for native Azure integration and EU compliance. | MS-AI-AZURE-CALLCENTER-001   | Reliability, Performance, Cost    | Upstream: Azure AI Search (knowledge base)\nDownstream: D365 CE (ticket resolution) | Bidirectional |
| Security Architecture      | Identity Provider       | Entra ID                    | A     | Implement Entra ID with Conditional Access for zero-trust authentication across all application tiers.               | MS-SEC-ENTRA-CALLCENTER-002  | Security, Reliability, Ops        | Upstream: User directories\nDownstream: All application services                     | Bidirectional |
| Data Architecture          | Operational Data Store  | Azure SQL Elastic Pools     | A     | Multi-tenant Azure SQL with elastic pools for cost-efficient scaling. Per-tenant database isolation maintained.       | MS-DATA-AZURE-CALLCENTER-003 | Reliability, Performance, Cost    | Upstream: D365 CE (CRUD operations)\nDownstream: Power BI (reporting)                | Bidirectional |
| Integration Architecture   | Message Broker          | Azure Service Bus Premium   | A     | Asynchronous messaging with topic/subscription pattern for event-driven integration between D365 and legacy ERP.     | MS-INT-D365-CALLCENTER-004   | Reliability, Performance, Ops     | Upstream: D365 CE (business events)\nDownstream: Legacy ERP (order sync)             | Bidirectional |
| Monitoring & Operations    | Observability Platform  | Azure Monitor + App Insights | A     | Centralized monitoring with Application Insights for distributed tracing and Azure Monitor for infrastructure metrics. |                               | Ops, Reliability, Performance     | Upstream: All application services\nDownstream: Azure Logic Apps (alerting)          | Inbound       |

### xlsx Skill Invocation Pattern

```
Invoke the xlsx skill to create an Excel workbook with:
- Sheet name: "Solution Design"
- Columns:
  - A: "Section" (width: 25)
  - B: "Component" (width: 30)
  - C: "Technology" (width: 30)
  - D: "Stack" (width: 10)
  - E: "Design Decision" (width: 50, wrap text)
  - F: "Referenced ADR" (width: 25)
  - G: "NFR Coverage" (width: 35)
  - H: "Integration Points" (width: 40, wrap text)
  - I: "Data Flow" (width: 15)
- Data validation on D: ["A", "B", "C", "D"]
- Data validation on I: ["Inbound", "Outbound", "Bidirectional"]
- Conditional formatting on D: A=Green, B=Blue, C=Yellow, D=Red
- Header formatting: bold, #003366 background, white text
- Row grouping by Column A
- Freeze top row, auto-filter enabled
- Data: [provide rows]
```
