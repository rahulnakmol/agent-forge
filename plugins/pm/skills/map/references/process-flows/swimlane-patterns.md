# Swimlane Diagram Patterns

## Overview

Swimlane diagrams show multi-actor processes with clear responsibility boundaries. In Mermaid, swimlanes are built using `subgraph` blocks. Each subgraph represents one persona or organizational role.

## Core Conventions

- **One subgraph per persona/role**: Never mix actors in a single lane
- **Handoffs are cross-lane edges**: Arrows crossing subgraph boundaries represent handoffs
- **Decision points in the decision-maker's lane**: Place the gateway in the subgraph of the person who makes the decision
- **Direction**: Use `TB` (top-to-bottom) for vertical layouts, `LR` (left-to-right) for horizontal
- **Subgraph naming**: Use the persona role name as both ID and label

---

## 3-Lane Process Template

Use for simple processes with a requester, approver, and executor.

```mermaid
flowchart TB
    subgraph Requester["Requester"]
        A[Identify Need] --> B[Submit Request]
    end

    subgraph Approver["Approver / Manager"]
        C[Review Request] --> D{Approve?}
        D -->|Reject| E[Provide Feedback]
    end

    subgraph Executor["Fulfillment Team"]
        F[Process Request] --> G[Deliver Outcome]
        G --> H[Confirm Completion]
    end

    B --> C
    D -->|Approve| F
    E --> A
    H --> B

    style A fill:#e0e0e0,stroke:#666
    style B fill:#e0e0e0,stroke:#666
    style C fill:#e0e0e0,stroke:#666
    style F fill:#e0e0e0,stroke:#666
```

### Handoff Points
- **Requester -> Approver**: Request submission (B -> C)
- **Approver -> Executor**: Approval (D -> F)
- **Approver -> Requester**: Rejection with feedback (E -> A)
- **Executor -> Requester**: Completion confirmation (H -> B)

---

## 4-Lane Process Template

Use for processes involving a requester, system, approver, and external party.

```mermaid
flowchart TB
    subgraph EndUser["End User"]
        A[Submit Order] --> B[Receive Confirmation]
    end

    subgraph System["System / Platform"]
        C[Validate Order] --> D{Inventory Available?}
        D -->|No| E[Notify Backorder]
        D -->|Yes| F[Reserve Inventory]
        F --> G[Calculate Total]
    end

    subgraph Finance["Finance / Billing"]
        H[Process Payment] --> I{Payment OK?}
        I -->|No| J[Flag Payment Issue]
        I -->|Yes| K[Generate Invoice]
    end

    subgraph Warehouse["Warehouse / Logistics"]
        L[Pick & Pack] --> M[Ship Order]
        M --> N[Update Tracking]
    end

    A --> C
    E --> B
    G --> H
    J --> B
    K --> L
    N --> B
```

---

## 5-Lane Process Template

Use for complex enterprise processes with multiple organizational roles.

```mermaid
flowchart TB
    subgraph Employee["Employee"]
        A[Identify Need] --> B[Create Requisition]
    end

    subgraph Manager["Line Manager"]
        C[Review Requisition] --> D{Within Budget?}
        D -->|No| E[Reject / Modify]
        D -->|Yes| F[Approve]
    end

    subgraph Procurement["Procurement"]
        G[Source Vendor] --> H[Negotiate Terms]
        H --> I[Create Purchase Order]
    end

    subgraph Vendor["External Vendor"]
        J[Acknowledge PO] --> K[Deliver Goods/Services]
    end

    subgraph Finance["Finance / AP"]
        L[Receive Invoice] --> M[[Three-Way Match]]
        M --> N{Match OK?}
        N -->|Yes| O[Process Payment]
        N -->|No| P[Resolve Exception]
    end

    B --> C
    E --> A
    F --> G
    I --> J
    K --> L
    P --> G
    O --> B
```

---

## Swimlane Styling for Current vs Target State

### Current-State Swimlane

Add pain point styling to bottleneck steps and annotate handoff delays.

```mermaid
flowchart TB
    subgraph Requester["Requester"]
        A[Fill Paper Form] --> B[Walk to Manager Office]
    end

    subgraph Manager["Manager"]
        C[Review Paper Form] --> D{Approve?}
        D -->|No| E[Write Notes on Form]
    end

    subgraph Admin["Admin Team"]
        F[Re-enter Data in System] --> G[File Paper Copy]
    end

    B --> C
    D -->|Yes| F
    E --> A

    style A fill:#fadbd8,stroke:#e74c3c
    style B fill:#fadbd8,stroke:#e74c3c
    style F fill:#fadbd8,stroke:#e74c3c
```

### Target-State Swimlane

Highlight automated steps and eliminated handoffs.

```mermaid
flowchart TB
    subgraph Requester["Requester"]
        A[Submit Digital Form] --> B[Track Status Online]
    end

    subgraph System["Automated System"]
        C[Validate & Route] --> D[Notify Approver]
    end

    subgraph Manager["Manager"]
        E[Review on Mobile] --> F{Approve?}
        F -->|No| G[Add Comments]
    end

    A --> C
    D --> E
    F -->|Yes| B
    G --> A

    style C fill:#d5f5e3,stroke:#27ae60
    style D fill:#d5f5e3,stroke:#27ae60
    style E fill:#d4e6f1,stroke:#2980b9
```

---

## Cross-Lane Decision Impact

When a decision in one lane affects multiple other lanes, show the branching edges clearly.

```mermaid
flowchart TB
    subgraph RiskTeam["Risk Assessment"]
        A[Evaluate Application] --> B{Risk Level}
    end

    subgraph StandardProcessing["Standard Processing"]
        C[Auto-Approve] --> D[Generate Contract]
    end

    subgraph EnhancedReview["Enhanced Review"]
        E[Manual Underwriting] --> F{Underwriter Decision}
        F -->|Approve| G[Generate Contract with Conditions]
        F -->|Decline| H[Send Decline Notice]
    end

    subgraph Compliance["Compliance"]
        I[Regulatory Check] --> J[File Report]
    end

    B -->|Low| C
    B -->|Medium| E
    B -->|High| I
    I --> E
```

---

## Tips for Effective Swimlane Diagrams

1. **Limit to 5 lanes maximum**: More than 5 becomes unreadable. Group minor roles.
2. **Order lanes by process flow**: Top lane starts the process, bottom lane finishes.
3. **Minimize cross-lane edges**: Too many crossing arrows create visual clutter. Redesign the lane order to reduce crossings.
4. **Label every cross-lane edge**: What is being handed off? Data, approval, physical goods?
5. **Highlight the critical path**: Use bold edges or color for the primary happy-path flow.
6. **Annotate wait times**: Add notes on edges where delays typically occur (e.g., `-->|avg 3 days|`).
