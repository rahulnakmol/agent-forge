# Consulting Delivery Context Guide

## Purpose

This reference provides context for Mode B (Consulting PM) discovery. It covers the structures, patterns, and considerations that shape how Program Managers approach discovery within Big Four, MBB, or system integrator transformation engagements.

---

## Consulting Engagement Structures

### Big Four Engagement Model

| Phase | Typical Activities | PM Discovery Relevance |
|-------|-------------------|----------------------|
| **Assess** | Current state analysis, maturity assessment, gap identification | Primary discovery input -- leverage existing assessment artifacts |
| **Design** | Target operating model, solution architecture, roadmap | Discovery feeds into this phase via Business Understanding Document |
| **Build** | Solution development, configuration, integration, testing | Discovery outputs become requirements for build teams |
| **Deploy** | Migration, training, cutover, hypercare | Discovery identifies change management and adoption needs |
| **Operate** | Steady-state support, continuous improvement | Discovery success criteria become operational KPIs |

### MBB Engagement Model

| Deliverable | What It Contains | How to Decompose |
|------------|-----------------|-----------------|
| **Diagnostic** | Market analysis, competitive benchmarking, financial modeling | Extract problem statements, strategic context, quantified gaps |
| **Design Blueprint** | High-level transformation design, capability model, value case | Decompose into specific process areas, identify actor personas |
| **Implementation Roadmap** | Phased plan, workstream definitions, resource model | Map to initiative types, identify dependencies |
| **Value Tracking** | KPI framework, benefits realization plan | Extract success criteria and measurement approach |

---

## SOW Structure and Deliverable Milestones

### Typical SOW Components Relevant to Discovery

| SOW Section | Discovery Action |
|------------|-----------------|
| **Scope of Work** | Define initiative boundaries -- what is in scope for this phase? |
| **Assumptions** | Validate or challenge -- which assumptions need testing? |
| **Deliverables** | Map to Business Understanding Document sections |
| **Acceptance Criteria** | Translate to success criteria in discovery output |
| **Dependencies** | Capture in Constraints & Dependencies dimension |
| **Exclusions** | Document as explicit out-of-scope items |

### Milestone-Based Discovery Approach

Align discovery phases to SOW milestones:

| SOW Milestone | Discovery Phase | Deliverable |
|--------------|-----------------|-------------|
| Kickoff | Intake + Clarify | Problem statement, entry mode confirmed |
| Current State Checkpoint | Analyze + Classify | As-is process flows, initiative classification |
| Design Input Checkpoint | Map | Persona profiles, dependency map, process inventory |
| Discovery Signoff | Document + Handoff | Complete Business Understanding Document |

---

## Decomposing an Existing High-Level Transformation Design

When a Big Four or MBB firm has already produced a high-level design, the Consulting PM must decompose it into actionable components.

### Decomposition Steps

1. **Obtain the source artifacts**: Strategy deck, capability model, high-level roadmap, value case
2. **Identify the scope boundary**: Which capabilities, processes, or workstreams are in scope for this phase?
3. **Extract process areas**: Map high-level capabilities to specific business processes (L1-L2 level)
4. **Identify actor personas**: For each process area, who are the actors (process owners, executors, approvers, consumers)?
5. **Map current-state processes**: How do these processes work today? What systems support them?
6. **Identify gaps and pain points**: Where does the current state fall short of the transformation vision?
7. **Document dependencies**: What else must change for this workstream to succeed?

### Common Decomposition Challenges

| Challenge | How to Handle |
|-----------|--------------|
| **Vague capability descriptions** | Ask "what specific processes does this capability include?" |
| **Missing current-state detail** | Conduct as-is process workshops with process owners |
| **Overlapping workstreams** | Map dependencies explicitly, define handoff points |
| **Aspirational target state** | Validate feasibility with IT and process owners |
| **Undefined process ownership** | Escalate to steering committee -- someone must own each process |

---

## Client Engagement Patterns

### Stakeholder Engagement Cadence

| Stakeholder Group | Frequency | Format | Purpose |
|-------------------|-----------|--------|---------|
| **Steering Committee** | Bi-weekly / Monthly | Formal presentation | Decisions, escalations, status |
| **Workstream Leads** | Weekly | Working session | Progress, blockers, design decisions |
| **Process Owners** | As needed (workshops) | Workshop / Interview | Current-state capture, requirements |
| **IT Leadership** | Weekly | Technical review | Integration, platform constraints |
| **Change Management** | Bi-weekly | Alignment session | Adoption readiness, communication |

### Workshop Facilitation for Discovery

**Process Mapping Workshop** (2-4 hours):
1. Confirm scope and boundaries (15 min)
2. Walk through current-state process step by step (60-90 min)
3. Identify pain points and bottlenecks at each step (30 min)
4. Map actors and handoffs (30 min)
5. Discuss target-state aspirations (30 min)
6. Capture open questions and follow-ups (15 min)

**Stakeholder Interview** (45-60 min):
1. Role and responsibilities overview (10 min)
2. Day-in-the-life walkthrough (15 min)
3. Pain point deep-dive (15 min)
4. Aspirations and success criteria (10 min)
5. Dependencies and concerns (10 min)

---

## Change Management Considerations

### Discovery-Phase Change Activities

| Activity | Purpose | Timing |
|----------|---------|--------|
| **Stakeholder assessment** | Understand readiness and resistance | Phase 1-2 (Intake/Clarify) |
| **Impact analysis** | Quantify who is affected and how | Phase 3 (Analyze) |
| **Communication planning** | Determine what to communicate and when | Phase 6 (Document) |
| **Resistance mapping** | Identify and plan for resistance sources | Phase 2-3 |

### Resistance Patterns in Transformation

| Pattern | Signal | Discovery Action |
|---------|--------|-----------------|
| **"This won't work here"** | Cultural resistance to change | Capture specific objections, validate or address |
| **"We tried this before"** | Prior failed initiative trauma | Document what was tried, why it failed, what is different now |
| **"My team is too busy"** | Resource constraint or passive resistance | Validate capacity, escalate if blocking |
| **"The new system won't do X"** | Fear of capability loss | Document current capabilities that must be preserved |
| **"Who asked for this?"** | Missing executive sponsorship visibility | Ensure sponsor communicates mandate clearly |

---

## Stakeholder Alignment in Large Organizations

### Alignment Challenges

| Challenge | Description | Mitigation |
|-----------|-------------|------------|
| **Matrix organization** | Multiple reporting lines create conflicting priorities | Map the informal power structure, not just org chart |
| **Regional variation** | "Global standard" means different things in different regions | Capture regional differences explicitly in discovery |
| **Merger/acquisition history** | Legacy organizations maintain separate processes and culture | Map both legacy processes before designing target state |
| **Outsourcing complexity** | Some processes are performed by third parties | Include outsource vendors as actor personas |
| **Union/works council** | Employee representatives have formal consultation rights | Engage early, document constraints they impose |

### Alignment Techniques

1. **Shared problem statement**: Get all stakeholders to agree on what the problem is before discussing solutions
2. **Visual process mapping**: Use swimlane diagrams in workshops -- visual alignment is faster than document-based
3. **Priority scoring**: When stakeholders disagree, use a structured scoring model (impact vs effort, MoSCoW)
4. **Decision log**: Record who decided what, when, and why. Prevents re-litigation.
5. **RACI publication**: Make the RACI visible to all stakeholders. Ambiguity breeds conflict.

---

## Consulting-Specific Discovery Anti-Patterns

| Anti-Pattern | Risk | Mitigation |
|-------------|------|------------|
| **Accepting the strategy deck at face value** | Design may be aspirational, not grounded in operational reality | Validate with process owners and IT |
| **Skipping current-state analysis** | Target state designed without understanding starting point | Always map as-is before to-be |
| **Single-source interviews** | One stakeholder's view treated as truth | Triangulate across 3+ sources |
| **Ignoring the shadow IT landscape** | Spreadsheets and workarounds are the real system of record | Ask "what do you actually use day-to-day?" |
| **Scope creep via discovery** | Discovery expands beyond SOW boundaries | Refer back to SOW scope, document out-of-scope findings for future phases |
