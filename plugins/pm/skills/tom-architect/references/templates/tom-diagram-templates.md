---
category: templates
loading_priority: 3
tokens_estimate: 5500
keywords:
  - Mermaid diagrams
  - capability map
  - process taxonomy
  - maturity assessment
  - role process matrix
  - technology overlay
  - data flow
  - KPI structure
  - diagram templates
  - filled examples
  - mindmap
  - flowchart
  - quadrant chart
  - block diagram
  - C4 container
  - sankey
  - pie chart
version: "1.0"
last_updated: "2026-03-23"
---

# TOM Diagram Templates — Full Mermaid Examples

Complete, filled-in Mermaid diagram templates for all 7 TOM diagram types. Each template includes the diagram type, when to use it, a full working example, and customization guidance.

---

## 1. Capability Map

**Diagram type**: Mindmap

**When to use**: Present the high-level process landscape for a domain at the L1/L2 level. Best for executive audiences and TOM overview slides. Use on Slide 5 of the TOM deck.

**Complete example**:

```mermaid
mindmap
  root((Finance Target
    Operating Model))
    Record to Report
      General Ledger
      Fixed Assets
      Close & Consolidation
      Financial Reporting
      Intercompany
    Order to Cash
      Customer Master Data
      Sales Order Management
      Billing & Invoicing
      Accounts Receivable
      Credit Management
      Collections
    Procure to Pay
      Purchase Requisition
      Purchase Order Mgmt
      Goods Receipt
      Invoice Processing
      Payment Processing
    Treasury & Cash Mgmt
      Cash Positioning
      Bank Reconciliation
      Cash Forecasting
      Debt & Investment Mgmt
    Tax Management
      Tax Determination
      Tax Reporting
      Transfer Pricing
      Indirect Tax
    Financial Planning
      Budgeting
      Forecasting
      Variance Analysis
      Cost Allocation
```

**Customization guidance**:
- Replace the root label with the domain name
- Add or remove L1 branches based on scope
- Add a third level (L3) for focused discussions, but limit to 3–4 items per L2 to avoid clutter
- For multi-domain views, use the domain name as L1 and L1 processes as L2

---

## 2. Process Taxonomy

**Diagram type**: Flowchart (left-to-right)

**When to use**: Show the hierarchical decomposition of a single L1 process. Best for workshops and detailed design sessions. Use on Slide 7 of the TOM deck.

**Complete example**:

```mermaid
flowchart LR
    L1["<b>Record to Report</b>"]

    L1 --> GL["General Ledger"]
    L1 --> FA["Fixed Assets"]
    L1 --> CC["Close &<br/>Consolidation"]
    L1 --> FR["Financial<br/>Reporting"]

    GL --> GL1["Journal Entry<br/>Processing"]
    GL --> GL2["Chart of Accounts<br/>Management"]
    GL --> GL3["Intercompany<br/>Accounting"]
    GL --> GL4["Allocations &<br/>Accruals"]

    GL1 --> GL1a["Create JE"]
    GL1 --> GL1b["Validate JE<br/><i>automated</i>"]
    GL1 --> GL1c["Approve JE"]
    GL1 --> GL1d["Post JE<br/><i>automated</i>"]

    FA --> FA1["Asset Acquisition"]
    FA --> FA2["Depreciation<br/><i>automated</i>"]
    FA --> FA3["Transfer &<br/>Disposal"]

    CC --> CC1["Subledger Close"]
    CC --> CC2["Currency<br/>Revaluation"]
    CC --> CC3["Consolidation"]
    CC --> CC4["Elimination<br/>Entries"]

    FR --> FR1["Management<br/>Reporting"]
    FR --> FR2["Statutory<br/>Reporting"]
    FR --> FR3["Regulatory<br/>Filing"]

    style L1 fill:#0d47a1,color:#fff,stroke:#0d47a1
    style GL fill:#1565c0,color:#fff
    style FA fill:#1565c0,color:#fff
    style CC fill:#1565c0,color:#fff
    style FR fill:#1565c0,color:#fff
    style GL1b fill:#2e7d32,color:#fff
    style GL1d fill:#2e7d32,color:#fff
    style FA2 fill:#2e7d32,color:#fff
```

**Customization guidance**:
- Green nodes indicate automated activities — apply `fill:#2e7d32` to any L4 node flagged as fully automated or AI-augmented
- Add `<i>AI-augmented</i>` or `<i>automated</i>` tags below activity names for visual clarity
- For very large processes, split across multiple diagrams (one per L2)
- Limit L4 detail to processes targeted for redesign or automation

---

## 3. Maturity Assessment

**Diagram type**: Quadrant Chart

**When to use**: Visualize the current vs target maturity gap across L2 processes. Helps prioritize improvement actions. Use on Slide 6 of the TOM deck.

**Complete example**:

```mermaid
quadrantChart
    title Finance Process Maturity — Current vs Target
    x-axis Low Current Maturity --> High Current Maturity
    y-axis Low Target Ambition --> High Target Ambition
    quadrant-1 Strategic Investment
    quadrant-2 Maintain & Optimize
    quadrant-3 Low Priority
    quadrant-4 Quick Win
    General Ledger: [0.70, 0.85]
    Fixed Assets: [0.55, 0.65]
    Close & Consolidation: [0.50, 0.90]
    Financial Reporting: [0.60, 0.95]
    Accounts Payable: [0.35, 0.85]
    Accounts Receivable: [0.40, 0.80]
    Credit Management: [0.30, 0.70]
    Collections: [0.25, 0.60]
    Treasury: [0.20, 0.75]
    Tax Determination: [0.45, 0.55]
    Budgeting: [0.65, 0.70]
    Cost Allocation: [0.50, 0.50]
```

**Customization guidance**:
- X-axis values map maturity scores: Level 1 = 0.20, Level 2 = 0.40, Level 3 = 0.60, Level 4 = 0.80, Level 5 = 1.00
- Y-axis values map target maturity using the same scale
- Quadrant labels:
  - Top-left (Strategic Investment): Low current, high target — requires significant transformation
  - Top-right (Maintain & Optimize): High current, high target — sustain and fine-tune
  - Bottom-left (Low Priority): Low current, low target — deprioritize
  - Bottom-right (Quick Win): High current, low target — already performing, easy to maintain
- Add or remove L2 processes based on domain scope

---

## 4. Role-Process Matrix

**Diagram type**: Block-Beta

**When to use**: Show RACI-style responsibility assignments for roles against processes. Best for organizational design discussions. Use alongside Slide 8 of the TOM deck.

**Complete example**:

```mermaid
block-beta
    columns 6
    space:1 h1["GL<br/>Accountant"] h2["AP<br/>Clerk"] h3["AR<br/>Analyst"] h4["Controller"] h5["CFO"]

    p1["Journal Entry"]:1 r1["R"]:1 space:1 space:1 r4["A"]:1 space:1
    p2["Invoice Processing"]:1 space:1 r6["R"]:1 space:1 r8["A"]:1 space:1
    p3["Collections"]:1 space:1 space:1 r10["R"]:1 r11["A"]:1 space:1
    p4["Period Close"]:1 r13["R"]:1 r14["C"]:1 r15["C"]:1 r16["A"]:1 space:1
    p5["Financial Reporting"]:1 r17["C"]:1 space:1 space:1 r20["R"]:1 r21["A"]:1
    p6["Budgeting"]:1 r22["I"]:1 r23["I"]:1 r24["I"]:1 r25["R"]:1 r26["A"]:1

    style r1 fill:#2e7d32,color:#fff
    style r6 fill:#2e7d32,color:#fff
    style r10 fill:#2e7d32,color:#fff
    style r13 fill:#2e7d32,color:#fff
    style r20 fill:#2e7d32,color:#fff
    style r25 fill:#2e7d32,color:#fff
    style r4 fill:#c62828,color:#fff
    style r8 fill:#c62828,color:#fff
    style r11 fill:#c62828,color:#fff
    style r16 fill:#c62828,color:#fff
    style r21 fill:#c62828,color:#fff
    style r26 fill:#c62828,color:#fff
    style r14 fill:#1565c0,color:#fff
    style r15 fill:#1565c0,color:#fff
    style r17 fill:#1565c0,color:#fff
    style r22 fill:#e0e0e0,color:#333
    style r23 fill:#e0e0e0,color:#333
    style r24 fill:#e0e0e0,color:#333
```

**Customization guidance**:
- R (Responsible) = green (#2e7d32), A (Accountable) = red (#c62828), C (Consulted) = blue (#1565c0), I (Informed) = gray (#e0e0e0)
- Add or remove role columns based on the domain's role catalog
- Add or remove process rows based on scope
- Verify SoD: no role should have both R and A on the same row
- For large matrices (10+ roles, 15+ processes), split into multiple diagrams by L2 process area

---

## 5. Technology Overlay

**Diagram type**: C4 Container

**When to use**: Show the technology platform landscape and integrations supporting the TOM. Best for technology discussions and architecture reviews. Use on Slide 10 of the TOM deck.

**Complete example**:

```mermaid
C4Container
    title Finance TOM — Technology Overlay

    Person(user, "Finance User", "GL Accountant, AP Clerk, Controller")

    Container_Boundary(erp, "ERP Platform") {
        Container(d365fo, "D365 Finance", "X++, Dynamics 365", "GL, AP, AR, FA, Tax, Budgeting")
        Container(d365scm, "D365 SCM", "X++, Dynamics 365", "Procurement, Inventory, Warehouse")
    }

    Container_Boundary(ai, "AI & Automation") {
        Container(copilot, "M365 Copilot", "LLM, GPT-4", "Document summarization, drafting")
        Container(copilotStudio, "Copilot Studio", "Custom Agents", "Process-specific AI agents")
        Container(powerAutomate, "Power Automate", "Low-code", "Workflow automation, RPA")
    }

    Container_Boundary(analytics, "Data & Analytics") {
        Container(fabric, "Microsoft Fabric", "Lakehouse", "Financial analytics, reporting")
        Container(powerbi, "Power BI", "Embedded", "Dashboards, KPI monitoring")
        Container(dataverse, "Dataverse", "Data Platform", "Master data, integration hub")
    }

    Container_Boundary(infra, "Infrastructure & Security") {
        Container(entra, "Entra ID", "Identity", "SSO, MFA, conditional access")
        Container(sentinel, "Sentinel", "SIEM", "Security monitoring, audit logs")
        Container(keyvault, "Key Vault", "Secrets", "Certificates, encryption keys")
    }

    Rel(user, d365fo, "Performs finance processes")
    Rel(user, copilot, "AI-assisted tasks")
    Rel(d365fo, dataverse, "Dual-write sync")
    Rel(d365fo, fabric, "Analytics pipeline")
    Rel(powerAutomate, d365fo, "Automated workflows")
    Rel(copilotStudio, d365fo, "Process automation")
    Rel(fabric, powerbi, "Serves dashboards")
    Rel(d365fo, entra, "Authentication")
    Rel(d365fo, sentinel, "Audit logs")

    UpdateRelStyle(d365fo, dataverse, $offsetX="-40", $offsetY="-10")
```

**Customization guidance**:
- Add or remove containers based on the actual technology landscape
- Group containers into logical boundaries (ERP, AI, Analytics, Infrastructure)
- Add relationships for all significant data flows and integrations
- For non-Microsoft components, add them as `Container_Ext` with a different style
- Include the Person element to show primary user roles

---

## 6. Data Flow

**Diagram type**: Flowchart (top-down)

**When to use**: Show how data flows between systems, processes, and data stores. Best for data architecture discussions and MDM design. Use alongside Slide 13 of the TOM deck.

**Complete example**:

```mermaid
flowchart TD
    subgraph Sources["Source Systems"]
        ERP["D365 F&O<br/><i>Transactional Data</i>"]
        CRM["D365 CE<br/><i>Customer Data</i>"]
        HR["D365 HR<br/><i>Employee Data</i>"]
        EXT["External Sources<br/><i>Bank Feeds, Market Data</i>"]
    end

    subgraph Integration["Integration Layer"]
        DV["Dataverse<br/><i>Master Data Hub</i>"]
        DW["Dual-Write<br/><i>Real-time Sync</i>"]
        ETL["Data Pipeline<br/><i>Fabric Pipelines</i>"]
    end

    subgraph Storage["Data Platform"]
        LAKE["Fabric Lakehouse<br/><i>Bronze / Silver / Gold</i>"]
        WH["Fabric Warehouse<br/><i>Curated Data</i>"]
        MDM["Master Data<br/><i>Golden Records</i>"]
    end

    subgraph Consumption["Analytics & Reporting"]
        PBI["Power BI<br/><i>Dashboards</i>"]
        EXCEL["Excel<br/><i>Ad-hoc Analysis</i>"]
        AI["AI Models<br/><i>Predictions & Insights</i>"]
    end

    ERP -->|"Dual-Write"| DW
    CRM -->|"Dual-Write"| DW
    HR -->|"API"| ETL
    EXT -->|"File/API"| ETL
    DW --> DV
    DV -->|"Master Data"| MDM
    ETL -->|"Batch"| LAKE
    DV -->|"Sync"| LAKE
    LAKE -->|"Transform"| WH
    MDM -->|"Golden Records"| WH
    WH --> PBI
    WH --> EXCEL
    WH --> AI
    AI -->|"Predictions"| PBI

    style Sources fill:#e3f2fd,stroke:#1565c0
    style Integration fill:#fff3e0,stroke:#e65100
    style Storage fill:#e8f5e9,stroke:#2e7d32
    style Consumption fill:#f3e5f5,stroke:#6a1b9a
```

**Customization guidance**:
- Adjust source systems based on the client's actual landscape
- Add or remove integration patterns (Dual-Write, API, Batch, Event-based)
- The Bronze/Silver/Gold medallion architecture in Fabric is standard — customize layer names if the client uses different terminology
- Add data volume annotations (e.g., "~10K records/day") for sizing discussions
- For complex flows, split by data domain (financial data flow, master data flow, analytics data flow)

---

## 7. KPI Structure

**Diagram type**: Flowchart (top-down with grouping)

**When to use**: Show the hierarchical KPI framework from strategic objectives down to operational metrics. Best for KPI design sessions and executive dashboards. Use on Slide 12 of the TOM deck.

**Complete example**:

```mermaid
flowchart TD
    subgraph Strategic["Strategic KPIs — CFO Dashboard"]
        S1["Working Capital Ratio<br/><b>Target: 1.5x</b>"]
        S2["Days Sales Outstanding<br/><b>Target: 35 days</b>"]
        S3["Cost of Finance Function<br/><b>Target: 0.8% of revenue</b>"]
    end

    subgraph Tactical["Tactical KPIs — Controller Dashboard"]
        T1["Close Cycle Time<br/><b>Target: 5 days</b>"]
        T2["Invoice Processing Cost<br/><b>Target: $2.50/invoice</b>"]
        T3["Forecast Accuracy<br/><b>Target: 95%</b>"]
        T4["Touchless Invoice Rate<br/><b>Target: 80%</b>"]
    end

    subgraph Operational["Operational KPIs — Team Dashboards"]
        O1["JE Error Rate<br/><b>Target: <1%</b>"]
        O2["Reconciliation<br/>Completion<br/><b>Target: 100%</b>"]
        O3["Aging > 90 Days<br/><b>Target: <5%</b>"]
        O4["Payment On-Time<br/><b>Target: 98%</b>"]
        O5["Budget Variance<br/><b>Target: +/- 3%</b>"]
        O6["Automated JE %<br/><b>Target: 70%</b>"]
    end

    S1 --> T1
    S1 --> T4
    S2 --> T2
    S2 --> T4
    S3 --> T2
    S3 --> T3
    T1 --> O1
    T1 --> O2
    T2 --> O4
    T2 --> O6
    T3 --> O5
    T4 --> O3
    T4 --> O6

    style Strategic fill:#0d47a1,color:#fff,stroke:#0d47a1
    style Tactical fill:#1565c0,color:#fff,stroke:#1565c0
    style Operational fill:#42a5f5,color:#fff,stroke:#42a5f5
    style S1 fill:#0d47a1,color:#fff
    style S2 fill:#0d47a1,color:#fff
    style S3 fill:#0d47a1,color:#fff
    style T1 fill:#1565c0,color:#fff
    style T2 fill:#1565c0,color:#fff
    style T3 fill:#1565c0,color:#fff
    style T4 fill:#1565c0,color:#fff
```

**Customization guidance**:
- Three tiers: Strategic (C-suite), Tactical (management), Operational (team)
- Each KPI shows the metric name and target value in bold
- Arrows show causal relationships — operational KPIs drive tactical KPIs, which drive strategic KPIs
- Replace metric names, targets, and relationships based on the domain's KPI catalog (from Section 5.1)
- For multi-domain views, add domain color coding to distinguish Finance KPIs from HR KPIs, etc.
- Keep Strategic tier to 3–5 KPIs, Tactical to 5–8, Operational to 8–15

---

## Diagram Selection Guide

| Scenario | Recommended Diagram | Template # |
|----------|-------------------|-----------|
| Executive overview of scope | Capability Map | 1 |
| Process design workshop | Process Taxonomy | 2 |
| Prioritization discussion | Maturity Assessment | 3 |
| Org design / RACI review | Role-Process Matrix | 4 |
| Architecture review | Technology Overlay | 5 |
| Data architecture / MDM design | Data Flow | 6 |
| KPI design / dashboard planning | KPI Structure | 7 |
| Combined TOM deck | All 7 (one per relevant slide) | All |

---

## Rendering Notes

- All diagrams use standard Mermaid syntax compatible with Mermaid v10+
- Color codes use Material Design palette for consistency
- Diagrams are designed for 16:9 slide embedding — keep node text concise
- For PPTX generation, diagrams can be rendered as SVG and inserted as images
- Test rendering at https://mermaid.live before finalizing
