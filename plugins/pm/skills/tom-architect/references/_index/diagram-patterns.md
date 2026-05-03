---
category: index
loading_priority: 3
tokens_estimate: 2800
keywords:
  - diagram patterns
  - Mermaid templates
  - capability map
  - process taxonomy
  - maturity assessment
  - role process matrix
  - technology overlay
  - mindmap
  - flowchart
  - quadrant chart
  - block diagram
  - C4 container
version: "1.0"
last_updated: "2026-03-23"
---

# Diagram Patterns — Quick Reference

Copy-paste-ready Mermaid diagram templates for TOM visualization. For full examples with filled-in data, see `templates/tom-diagram-templates.md`.

---

## 1. Capability Map (Mindmap — L1 to L2 Hierarchy)

**Use when**: Presenting the high-level process landscape for a domain.

```mermaid
mindmap
  root((Finance TOM))
    Record to Report
      General Ledger
      Fixed Assets
      Close & Consolidation
      Financial Reporting
    Order to Cash
      Customer Master
      Sales Order
      Billing & Invoicing
      Accounts Receivable
    Procure to Pay
      Purchase Requisition
      Purchase Order
      Invoice Processing
      Payment Processing
```

**Customization**: Replace root label, L1 branches, and L2 leaves per domain.

---

## 2. Process Taxonomy (Flowchart — L1 to L4)

**Use when**: Showing the decomposition of a single L1 process into its hierarchy.

```mermaid
flowchart LR
    L1[Record to Report] --> L2a[General Ledger]
    L1 --> L2b[Fixed Assets]
    L1 --> L2c[Close & Consolidation]
    L2a --> L3a[Journal Entry Processing]
    L2a --> L3b[Chart of Accounts Mgmt]
    L3a --> L4a[Create JE]
    L3a --> L4b[Validate JE]
    L3a --> L4c[Approve JE]
    L3a --> L4d[Post JE]
    style L1 fill:#1a73e8,color:#fff
    style L2a fill:#4285f4,color:#fff
    style L2b fill:#4285f4,color:#fff
    style L2c fill:#4285f4,color:#fff
```

**Customization**: Expand or collapse levels as needed. Color-code by automation status at L4.

---

## 3. Maturity Assessment (Quadrant Chart — Current vs Target)

**Use when**: Visualizing the gap between current and target maturity across process areas.

```mermaid
quadrantChart
    title Maturity Assessment - Finance
    x-axis Low Current Maturity --> High Current Maturity
    y-axis Low Target Maturity --> High Target Maturity
    quadrant-1 Transform
    quadrant-2 Maintain
    quadrant-3 Assess
    quadrant-4 Quick Win
    General Ledger: [0.7, 0.8]
    Accounts Payable: [0.3, 0.9]
    Fixed Assets: [0.5, 0.6]
    Treasury: [0.2, 0.7]
    Financial Reporting: [0.6, 0.9]
    Tax Management: [0.4, 0.5]
```

**Customization**: Plot each L2 process as a point. X = current maturity (0-1 scale mapped from 1-5), Y = target maturity.

---

## 4. Role-Process Matrix (Block Diagram)

**Use when**: Showing which roles are responsible for which processes.

```mermaid
block-beta
    columns 5
    space:1 b1["GL Accountant"] b2["AP Clerk"] b3["AR Analyst"] b4["Controller"]
    a1["Journal Entry"]:1 r1["R"]:1 space:1 space:1 r4["A"]:1
    a2["Invoice Processing"]:1 space:1 r5["R"]:1 space:1 r8["A"]:1
    a3["Collections"]:1 space:1 space:1 r9["R"]:1 r12["A"]:1
    a4["Period Close"]:1 r13["C"]:1 r14["C"]:1 r15["C"]:1 r16["R"]:1
    style r1 fill:#2e7d32,color:#fff
    style r5 fill:#2e7d32,color:#fff
    style r9 fill:#2e7d32,color:#fff
    style r13 fill:#1565c0,color:#fff
    style r14 fill:#1565c0,color:#fff
    style r15 fill:#1565c0,color:#fff
    style r4 fill:#c62828,color:#fff
    style r8 fill:#c62828,color:#fff
    style r12 fill:#c62828,color:#fff
    style r16 fill:#2e7d32,color:#fff
```

**Legend**: R = Responsible (green), A = Accountable (red), C = Consulted (blue). Adapt roles and processes per domain.

---

## 5. Technology Overlay (C4-Style Container Diagram)

**Use when**: Showing the technology platform landscape supporting the TOM.

```mermaid
C4Container
    title Technology Overlay - Finance TOM
    Container_Boundary(erp, "ERP Layer") {
        Container(d365fo, "D365 F&O", "Dynamics 365", "Core finance processes")
        Container(d365scm, "D365 SCM", "Dynamics 365", "Procurement & inventory")
    }
    Container_Boundary(platform, "Platform Layer") {
        Container(pp, "Power Platform", "Power Apps/Automate", "Extensions & automation")
        Container(copilot, "Copilot Studio", "AI", "Conversational AI agents")
    }
    Container_Boundary(data, "Data Layer") {
        Container(fabric, "Microsoft Fabric", "Analytics", "Lakehouse & reporting")
        Container(dv, "Dataverse", "Data Platform", "Master data & integration")
    }
    Container_Boundary(infra, "Infrastructure") {
        Container(azure, "Azure", "Cloud", "Identity, networking, security")
    }
    Rel(d365fo, fabric, "Analytics data")
    Rel(pp, d365fo, "Extends")
    Rel(copilot, d365fo, "AI overlay")
    Rel(d365fo, dv, "Master data sync")
```

**Customization**: Add or remove containers based on the client's technology landscape. Add integration arrows as needed.
