# Process Flow Documentation Template

## Purpose

This template defines how to structure, name, and annotate process flow diagrams within the Business Understanding Document. It ensures consistency across current-state and target-state flows and provides conventions for marking bottlenecks, pain points, and automation opportunities.

---

## Diagram Organization Structure

### File Naming Convention

Process flows are embedded in the Business Understanding Document, not separate files. Use section headers and IDs to organize them.

### Process ID Format

```
{Domain}-{Type}-{Number}
```

| Component | Values | Example |
|-----------|--------|---------|
| Domain | FIN, HR, PROC, SCM, SALES, CUST, OPS | FIN |
| Type | AP (Accounts Payable), AR, GL, ONB (Onboarding), ORD, REQ, etc. | AP |
| Number | 001, 002, ... | 001 |

**Example**: `FIN-AP-001` = Finance, Accounts Payable, Process #1

### Section Structure per Process

```markdown
### Process: [Process ID] -- [Process Name]

**Owner**: [Role]
**Frequency**: [Daily / Weekly / Monthly / Event-driven]
**Actors**: [List of personas involved]
**Systems**: [List of systems touched]
**SLA**: [Expected completion time]

#### Current State (As-Is)

[Mermaid diagram with gray/red styling]

**Pain Points:**
- **PP-{ID}-01**: [Description] -- Impact: [quantified]
- **PP-{ID}-02**: [Description] -- Impact: [quantified]

#### Target State (To-Be)

[Mermaid diagram with blue/green styling]

**Improvements:**
- **IMP-{ID}-01**: [Description] -- Eliminates: PP-{ID}-01 -- Benefit: [quantified]
- **IMP-{ID}-02**: [Description] -- Eliminates: PP-{ID}-02 -- Benefit: [quantified]

#### Gap Analysis

| Aspect | Current State | Target State | Gap |
|--------|--------------|-------------|-----|
| Automation level | [%] | [%] | [Delta] |
| Cycle time | [Duration] | [Duration] | [Delta] |
| Error rate | [%] | [%] | [Delta] |
| Actors involved | [N] | [N] | [Delta] |
| Systems touched | [N] | [N] | [Delta] |
```

---

## Current-State vs Target-State Flow Conventions

### Current-State (As-Is) Rules

1. **Document what actually happens**, not what is supposed to happen
2. Include workarounds, manual steps, and shadow processes
3. Mark pain points with red styling: `fill:#fadbd8,stroke:#e74c3c,color:#922b21`
4. Mark standard steps with gray styling: `fill:#e0e0e0,stroke:#666,color:#333`
5. Include wait times on edges where delays occur: `-->|avg 3 days|`
6. Note where data is re-entered, emailed, or printed

### Target-State (To-Be) Rules

1. **Show the desired future process**, not every intermediate step
2. Mark automated steps with green styling: `fill:#d5f5e3,stroke:#27ae60,color:#1e8449`
3. Mark standard improved steps with blue styling: `fill:#d4e6f1,stroke:#2980b9,color:#1a5276`
4. Show where pain points have been eliminated
5. Include new system integrations and automation points
6. Note where human approval is still required (do not assume full automation)

### Side-by-Side Comparison Pattern

When presenting to stakeholders, structure as:

```markdown
#### Current State
[As-is diagram]
[Pain point register]

#### Target State
[To-be diagram]
[Improvement register]

#### Change Summary
| What Changes | From | To | Benefit |
|-------------|------|-----|---------|
| [Step/handoff] | [Current behavior] | [Target behavior] | [Quantified benefit] |
```

---

## Annotating Bottlenecks

### Bottleneck Identification Criteria

A step is a bottleneck if any of the following are true:
- It has the longest average processing time in the flow
- It has the highest queue/wait time before it
- It is a single point of failure (one person, one system)
- It has the highest error/rework rate

### Bottleneck Annotation Pattern

In the Mermaid diagram:
```
style BottleneckStep fill:#fadbd8,stroke:#e74c3c,stroke-width:3px
```

Below the diagram:
```markdown
**Bottleneck Analysis:**
| Step | Wait Time | Process Time | Queue Depth | Root Cause |
|------|-----------|-------------|-------------|------------|
| [Step name] | [Duration] | [Duration] | [N items] | [Why this is slow] |
```

---

## Annotating Pain Points

### Pain Point Severity Scale

| Severity | Definition | Diagram Style |
|----------|-----------|---------------|
| **Critical** | Process cannot complete; business impact is immediate | `stroke:#c0392b,stroke-width:4px` (dark red, thick border) |
| **High** | Process completes but with significant waste or error | `fill:#fadbd8,stroke:#e74c3c` (red background) |
| **Medium** | Process is inefficient but functional | `fill:#fdebd0,stroke:#e67e22` (orange background) |
| **Low** | Minor inconvenience, does not affect outcomes | `fill:#fef9e7,stroke:#f1c40f` (yellow background) |

---

## Annotating Automation Opportunities

### Automation Opportunity Classification

| Type | Symbol in Diagram | Description |
|------|------------------|-------------|
| **Full automation** | `[/Step Name/]` (parallelogram) | No human intervention needed |
| **Semi-automation** | `[Step Name]` with green fill | Human triggers, system executes |
| **AI-assisted** | `[Step Name]` with purple fill | AI recommends, human decides |
| **Manual (keep)** | `[Step Name]` with blue fill | Human judgment required, no automation |

### Automation Annotation Below Diagram

```markdown
**Automation Opportunities:**

| Step | Current | Target | Type | Complexity | Prerequisite |
|------|---------|--------|------|-----------|-------------|
| [Step] | Manual | Automated | Full automation | Low / Medium / High | [What must exist first] |
| [Step] | Manual | AI-assisted | AI recommendation | Medium / High | [Data, model, integration] |
```

---

## Diagram Type Selection Guide

| Process Characteristic | Recommended Diagram | Why |
|----------------------|-------------------|-----|
| Sequential with decisions | BPMN Flowchart | Clear decision paths and outcomes |
| Multiple actors with handoffs | Swimlane | Shows responsibility boundaries |
| Entity with lifecycle states | State Machine | Valid state transitions and triggers |
| Complex with sub-processes | BPMN with sub-process blocks | Manages complexity via decomposition |
| Current vs target comparison | Two BPMN flowcharts | Side-by-side visual comparison |

---

## Quality Checklist

Before including a process flow in the Business Understanding Document:

- [ ] Every path from start reaches an end state (no dead ends)
- [ ] Decision gateways have all branches labeled
- [ ] Actors are consistent with the persona definitions in Section 3
- [ ] Pain points in the diagram match the pain point register
- [ ] Styling conventions are applied consistently
- [ ] Mermaid syntax renders correctly (test before including)
- [ ] Process ID follows naming convention
- [ ] Owner, frequency, actors, and systems are documented
- [ ] Current-state reflects reality (validated with process owners)
- [ ] Target-state is achievable (validated with IT and stakeholders)
