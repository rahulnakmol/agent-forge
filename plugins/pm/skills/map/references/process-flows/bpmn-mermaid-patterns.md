# BPMN-Style Mermaid Flowchart Patterns

## Core BPMN Elements in Mermaid

### Start and End Events

```mermaid
flowchart LR
    Start([Start: Trigger Name]) --> A[First Activity]
    A --> End([End: Outcome Name])
```

Use `([...])` for rounded rectangles representing start/end events. Always label with the trigger (start) or outcome (end).

### Activities (Tasks)

```mermaid
flowchart LR
    A[Manual Task] --> B[System Task]
    B --> C[[Sub-Process]]
```

| Syntax | BPMN Element | When to Use |
|--------|-------------|-------------|
| `[Text]` | Task | Standard activity step |
| `[[Text]]` | Sub-process | Activity that expands into its own flow |
| `[/Text/]` | Manual input | User provides data |
| `[(Text)]` | Database operation | Read/write to data store |

### Gateways

#### Exclusive Gateway (XOR) -- Only one path

```mermaid
flowchart TD
    A[Review Application] --> G{Approved?}
    G -->|Yes| B[Process Payment]
    G -->|No| C[Send Rejection]
```

#### Parallel Gateway (AND) -- All paths execute

```mermaid
flowchart TD
    A[Receive Order] --> P1{{"Parallel Split"}}
    P1 --> B[Check Inventory]
    P1 --> C[Verify Payment]
    P1 --> D[Validate Address]
    B --> P2{{"Parallel Join"}}
    C --> P2
    D --> P2
    P2 --> E[Fulfill Order]
```

Use `{{" "}}` (hexagon) to represent parallel gateways. Label as "Parallel Split" or "Parallel Join".

#### Inclusive Gateway (OR) -- One or more paths

```mermaid
flowchart TD
    A[Assess Risk] --> G{Risk Level}
    G -->|High| B[Full Audit]
    G -->|Medium| C[Spot Check]
    G -->|Low| D[Auto-Approve]
    G -->|High or Medium| E[Notify Compliance]
```

### Sub-Processes

```mermaid
flowchart LR
    A[Receive Invoice] --> B[[Three-Way Match]]
    B --> C{Match OK?}
    C -->|Yes| D[Approve Payment]
    C -->|No| E[Flag Exception]
```

Use `[[...]]` to indicate a sub-process that has its own detailed diagram elsewhere.

---

## Common Business Process Templates

### Approval Process

```mermaid
flowchart TD
    Start([Request Submitted]) --> A[Validate Completeness]
    A --> G1{Complete?}
    G1 -->|No| B[Return to Requester]
    B --> Start
    G1 -->|Yes| C[Route to Approver]
    C --> D[Review Request]
    D --> G2{Decision}
    G2 -->|Approve| E[Execute Action]
    G2 -->|Reject| F[Notify Requester]
    G2 -->|Request Info| G[Send Clarification Request]
    G --> D
    E --> End([Request Fulfilled])
    F --> End2([Request Closed])
```

### Procurement Process (P2P)

```mermaid
flowchart TD
    Start([Need Identified]) --> A[Create Requisition]
    A --> B[Submit for Approval]
    B --> G1{Budget Available?}
    G1 -->|No| C[Return to Requester]
    G1 -->|Yes| D[Manager Approval]
    D --> G2{Approved?}
    G2 -->|No| C
    G2 -->|Yes| E[Create Purchase Order]
    E --> F[Send to Vendor]
    F --> G[Receive Goods/Services]
    G --> H[[Three-Way Match]]
    H --> G3{Match OK?}
    G3 -->|Yes| I[Process Payment]
    G3 -->|No| J[Resolve Exception]
    J --> H
    I --> End([PO Closed])
```

### Incident Management

```mermaid
flowchart TD
    Start([Incident Reported]) --> A[Log Incident]
    A --> B[Categorize & Prioritize]
    B --> G1{Known Resolution?}
    G1 -->|Yes| C[Apply Known Fix]
    G1 -->|No| D[Investigate Root Cause]
    D --> E[Develop Fix]
    C --> F[Test Resolution]
    E --> F
    F --> G2{Resolved?}
    G2 -->|No| D
    G2 -->|Yes| G[Notify Stakeholders]
    G --> H[Close Incident]
    H --> End([Incident Closed])
```

---

## Current-State vs Target-State Styling

### Current-State (As-Is) Diagram

Use gray tones and annotate pain points with red borders.

```mermaid
flowchart TD
    Start([Order Received]) --> A[Manual Data Entry]
    A --> B[Email Approval Request]
    B --> C[Wait for Response]
    C --> D{Approved?}
    D -->|Yes| E[Manual PO Creation]
    D -->|No| F[Email Rejection]
    E --> End([PO Sent])
    F --> End2([Order Cancelled])

    style A fill:#fadbd8,stroke:#e74c3c,color:#922b21
    style B fill:#e0e0e0,stroke:#666,color:#333
    style C fill:#fadbd8,stroke:#e74c3c,color:#922b21
    style E fill:#fadbd8,stroke:#e74c3c,color:#922b21
```

**Style conventions:**
- `fill:#e0e0e0,stroke:#666,color:#333` -- Standard current-state step (gray)
- `fill:#fadbd8,stroke:#e74c3c,color:#922b21` -- Pain point / bottleneck (red)
- Add a note below the diagram listing each pain point with its impact

### Target-State (To-Be) Diagram

Use blue tones and annotate improvements with green borders.

```mermaid
flowchart TD
    Start([Order Received]) --> A[Auto-Capture via Integration]
    A --> B[System Routes to Approver]
    B --> C[Mobile Approval]
    C --> D{Approved?}
    D -->|Yes| E[Auto-Generate PO]
    D -->|No| F[System Notification]
    E --> End([PO Sent via EDI])
    F --> End2([Order Cancelled])

    style A fill:#d5f5e3,stroke:#27ae60,color:#1e8449
    style B fill:#d4e6f1,stroke:#2980b9,color:#1a5276
    style C fill:#d5f5e3,stroke:#27ae60,color:#1e8449
    style E fill:#d5f5e3,stroke:#27ae60,color:#1e8449
```

**Style conventions:**
- `fill:#d4e6f1,stroke:#2980b9,color:#1a5276` -- Standard target-state step (blue)
- `fill:#d5f5e3,stroke:#27ae60,color:#1e8449` -- Improvement / automation (green)

---

## Annotation Conventions

### Pain Point Annotation

After a current-state diagram, include a pain point register:

```markdown
**Pain Points Identified:**
1. **PP-01**: Manual data entry (Step A) -- 15 min per order, 5% error rate
2. **PP-02**: Email-based approval (Step C) -- Average 3-day wait time
3. **PP-03**: Manual PO creation (Step E) -- Duplicate entry, no audit trail
```

### Improvement Annotation

After a target-state diagram, include an improvement register:

```markdown
**Improvements:**
1. **IMP-01**: Auto-capture via API integration -- Eliminates PP-01
2. **IMP-02**: Mobile approval workflow -- Reduces PP-02 from 3 days to 2 hours
3. **IMP-03**: Auto-generated PO -- Eliminates PP-03, adds audit trail
```
