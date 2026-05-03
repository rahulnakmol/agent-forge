# State Machine Diagram Patterns

## Overview

State machine diagrams model the lifecycle of an entity (order, request, case, approval) by defining the valid states it can be in and the transitions between them. Use Mermaid `stateDiagram-v2` syntax.

## Core Syntax

```mermaid
stateDiagram-v2
    [*] --> InitialState
    InitialState --> NextState : trigger_action()
    NextState --> FinalState : complete()
    FinalState --> [*]
```

### Key Elements

| Element | Syntax | Purpose |
|---------|--------|---------|
| Start | `[*] -->` | Entry point |
| End | `--> [*]` | Terminal state |
| State | `StateName` | Named entity state |
| Transition | `--> : action()` | State change with trigger |
| Guard | `[condition]` | Condition that must be true for transition |
| Note | `note right of State` | Annotation on a state |
| Composite | `state "Name" as alias { ... }` | Nested states within a parent state |

---

## Entity Lifecycle Templates

### Order Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted : submit_order()
    Submitted --> Validated : validate()
    Submitted --> Rejected : validation_fail()
    Rejected --> Draft : revise()
    Validated --> Confirmed : confirm_payment()
    Validated --> Cancelled : cancel()
    Confirmed --> InFulfillment : start_fulfillment()
    InFulfillment --> Shipped : ship()
    Shipped --> Delivered : confirm_delivery()
    Delivered --> Closed : close()
    Delivered --> ReturnRequested : request_return()
    ReturnRequested --> Returned : process_return()
    Returned --> Refunded : issue_refund()
    Refunded --> [*]
    Closed --> [*]
    Cancelled --> [*]

    note right of Confirmed
        Payment verified.
        Inventory reserved.
    end note

    note right of InFulfillment
        Pick, pack, and
        prepare for shipping.
    end note
```

### Request / Ticket Lifecycle

```mermaid
stateDiagram-v2
    [*] --> New
    New --> Triaged : triage()
    Triaged --> Assigned : assign_to_agent()
    Assigned --> InProgress : start_work()
    InProgress --> PendingInfo : request_info()
    PendingInfo --> InProgress : info_received()
    PendingInfo --> Stale : timeout_7_days()
    Stale --> Closed : auto_close()
    InProgress --> Resolved : resolve()
    Resolved --> Closed : confirm_resolution()
    Resolved --> Reopened : reject_resolution()
    Reopened --> InProgress : resume_work()
    Closed --> [*]

    note right of PendingInfo
        Waiting for requester
        to provide information.
    end note
```

### Approval Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> PendingApproval : submit_for_approval()
    PendingApproval --> UnderReview : reviewer_opens()
    UnderReview --> Approved : approve()
    UnderReview --> Rejected : reject()
    UnderReview --> ChangesRequested : request_changes()
    ChangesRequested --> Draft : revise()
    Approved --> Executed : execute_action()
    Executed --> [*]
    Rejected --> [*]

    note right of UnderReview
        Reviewer has opened
        and is actively reviewing.
    end note
```

### Case / Investigation Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Reported
    Reported --> UnderInvestigation : open_investigation()
    UnderInvestigation --> EvidenceGathering : begin_evidence_collection()
    EvidenceGathering --> Analysis : complete_evidence()
    Analysis --> FindingsDocumented : document_findings()

    state Decision {
        FindingsDocumented --> ActionRequired : findings_warrant_action()
        FindingsDocumented --> NoActionNeeded : findings_clear()
    }

    ActionRequired --> RemediationInProgress : initiate_remediation()
    RemediationInProgress --> Verified : verify_remediation()
    Verified --> Closed : close_case()
    NoActionNeeded --> Closed : close_case()
    Closed --> [*]

    note right of Analysis
        Root cause analysis
        and impact assessment.
    end note
```

---

## Composite (Nested) States

Use composite states when a high-level state contains sub-states.

```mermaid
stateDiagram-v2
    [*] --> Intake

    state Intake {
        [*] --> ReceiveRequest
        ReceiveRequest --> ValidateData : validate()
        ValidateData --> Complete : data_valid()
        ValidateData --> RequestCorrection : data_invalid()
        RequestCorrection --> ReceiveRequest : correction_received()
        Complete --> [*]
    }

    Intake --> Processing : intake_complete()

    state Processing {
        [*] --> Analyze
        Analyze --> Implement : analysis_done()
        Implement --> Test : implementation_done()
        Test --> Analyze : test_failed()
        Test --> [*] : test_passed()
    }

    Processing --> Delivery : processing_complete()
    Delivery --> [*]
```

---

## Transition Patterns

### Guard Conditions

Guards restrict when a transition can fire.

```
StateA --> StateB : action() [guard_condition]
```

Example:
```
PendingApproval --> AutoApproved : submit() [amount < 1000]
PendingApproval --> ManagerReview : submit() [amount >= 1000]
```

### Timeout Transitions

Model time-based state changes for SLA enforcement.

```
Waiting --> Escalated : timeout_24h()
Escalated --> Critical : timeout_48h()
```

### Parallel States (Fork/Join)

Model concurrent sub-processes within a state.

```mermaid
stateDiagram-v2
    [*] --> Received

    state Processing {
        state fork_state <<fork>>
        state join_state <<join>>

        fork_state --> VerifyIdentity
        fork_state --> CheckCredit
        fork_state --> ValidateAddress

        VerifyIdentity --> join_state
        CheckCredit --> join_state
        ValidateAddress --> join_state
    }

    Received --> fork_state
    join_state --> Decision
    Decision --> Approved : all_checks_pass()
    Decision --> Denied : any_check_fails()
    Approved --> [*]
    Denied --> [*]
```

---

## Styling Conventions

### Current-State Entity Lifecycle
- Use plain state names (no special styling needed)
- Annotate problematic transitions with notes explaining the pain point

### Target-State Entity Lifecycle
- Add new states that represent automation or improvement
- Use notes to highlight what changed from current state

### Annotation Pattern

After the diagram, include a state transition register:

```markdown
**State Transition Register:**

| From | To | Trigger | Actor | SLA | Notes |
|------|----|---------|-------|-----|-------|
| Draft | Submitted | submit_order() | Requester | N/A | Requires all mandatory fields |
| Submitted | Validated | validate() | System | 5 min | Automated validation rules |
| Validated | Confirmed | confirm_payment() | Payment Gateway | 30 sec | Real-time payment verification |
```

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Missing terminal states** | Entity can never reach completion | Ensure every path leads to `[*]` |
| **Orphan states** | State with no incoming transition | Remove or connect to the flow |
| **Ambiguous transitions** | Same trigger from same state to different targets without guards | Add guard conditions |
| **Too many states** | Diagram becomes unreadable (>15 states) | Use composite states to group related states |
| **No error/exception states** | Only models the happy path | Add Rejected, Failed, Cancelled, Escalated states |
