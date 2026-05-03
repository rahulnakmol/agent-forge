# Consulting PRD Patterns

## How PRDs Differ in Consulting Engagements

Consulting PRDs are deliverable-driven, SOW-aligned, and governance-heavy. They serve as contractual artifacts that bridge the Target Operating Model (strategic) with implementation specifications (tactical). The PRD must satisfy both the client's business stakeholders and the delivery team's technical leads.

---

## SOW Alignment

Every consulting PRD must trace back to the Statement of Work. This is not optional -- it is contractual.

### SOW Traceability Template

Include in Section 1 (Business Context):

```markdown
### SOW Alignment

| SOW Reference | Deliverable | PRD Epic | Status |
|---------------|------------|----------|--------|
| {SOW clause/ID} | {deliverable name as written in SOW} | {this epic name} | {Mapped / Partially Mapped / Gap} |
```

### Rules

- Every epic must map to at least one SOW deliverable
- If an epic is needed but not in the SOW, flag it as a change request in Open Questions
- If a SOW deliverable spans multiple epics, document the coverage split
- SOW deliverable names must be used verbatim in the traceability table

---

## Deliverable-Based Milestones

Consulting PRDs tie release phases to contractual milestones, not sprint cadences.

### Milestone Integration in Section 11 (Release & Rollout)

```markdown
### Delivery Milestones

| Milestone | SOW Reference | Deliverables | Acceptance Criteria | Client Approver | Date |
|-----------|--------------|-------------|-------------------|----------------|------|
| M1: Design Complete | {SOW ref} | PRD approved, HLD signed off | Client PM sign-off | {name} | {date} |
| M2: Build Complete | {SOW ref} | Features developed, unit tested | QA pass rate > 95% | {name} | {date} |
| M3: UAT Complete | {SOW ref} | Client acceptance testing passed | UAT sign-off form | {name} | {date} |
| M4: Go-Live | {SOW ref} | Production deployment, hypercare | Go-live checklist complete | {name} | {date} |
```

---

## Client Approval Gates

Consulting PRDs include explicit approval gates that do not exist in SaaS PRDs.

### Gate Structure

| Gate | When | Who Approves | What They Approve | Artifact |
|------|------|-------------|-------------------|----------|
| G1: PRD Review | After draft | Client PM + Business Owner | Scope, stories, personas | Signed PRD |
| G2: Design Review | After spec | Client Technical Lead | Architecture, integrations | Signed design doc |
| G3: UAT Entry | After build | Client QA Lead | Test readiness, environments | UAT entry form |
| G4: Go-Live | After UAT | Client Steering Committee | Production readiness | Go-live checklist |

Include approval gates in Section 11 and reference them in the Open Questions section for any pending approvals.

---

## TOM-Backed Requirements

The defining characteristic of Mode B (Consulting Pipeline) PRDs is that requirements are grounded in the Target Operating Model.

### How TOM Shapes Each PRD Section

| PRD Section | TOM Input | How It Manifests |
|-------------|-----------|-----------------|
| 1. Problem Statement | TOM maturity gaps | Problem quantified as maturity gap (e.g., "L2 Process X at maturity 2, target 4") |
| 2. Personas | TOM role mappings + GPO overlay | Personas are operational roles with L2 process ownership |
| 3. TOM Alignment | Full TOM traceability | L1-L4 process IDs, maturity scores, gap closure actions |
| 4. Epic Definition | TOM capability register | Scope defined by capability IDs covered |
| 5. User Stories | TOM process activities (L3-L4) | Stories derived from L4 activity changes |
| 7. Success Metrics | TOM KPI framework | Metrics mapped to TOM KPIs with maturity progression targets |
| 9. Technical | TOM technology mapping | Integration points from TOM capability-to-technology map |

### Maturity-Based Success Metrics

Consulting PRDs include maturity progression as a success metric category:

```markdown
### Maturity Progression Metrics

| Process (L2) | Current Maturity | Target Maturity | Intermediate Target (this epic) | Measurement |
|--------------|-----------------|----------------|-------------------------------|-------------|
| {process name} | {1-5} | {1-5} | {target after this epic ships} | {how maturity is assessed} |
```

---

## Change Management Integration

Consulting PRDs must address organizational change, not just system change.

### Change Impact Section

Add to Section 11 (Release & Rollout) or as a subsection of Section 8 (Constraints):

```markdown
### Change Management

| Impact Area | Current State | Future State | Change Magnitude | Readiness Actions |
|-------------|-------------|--------------|-----------------|-------------------|
| Process | {how it works today} | {how it will work} | {High / Medium / Low} | {training, documentation, pilot} |
| People | {current roles/skills} | {new roles/skills needed} | {High / Medium / Low} | {training plan, hiring, reorg} |
| Technology | {current tools} | {new tools} | {High / Medium / Low} | {deployment, migration, support} |
```

### Training Story Pattern

Consulting PRDs often include explicit training stories:

```
As a finance team member transitioning to the new process,
I want step-by-step guided training on the new invoice approval workflow,
So that I can perform my daily tasks confidently from day one of go-live.
```

---

## Multi-Workstream Coordination

Enterprise consulting engagements often run multiple workstreams in parallel. PRDs must account for cross-workstream dependencies.

### Workstream Dependency Map

Include in Section 4 (Epic Definition) or Section 8 (Constraints):

```markdown
### Cross-Workstream Dependencies

| This Epic Needs | From Workstream | Dependency | Timeline | Risk if Delayed |
|----------------|----------------|-----------|----------|----------------|
| {what we need} | {workstream name} | {Hard / Soft} | {when we need it by} | {impact} |
| {what we provide} | {to workstream name} | {Hard / Soft} | {when they need it} | {their impact} |
```

---

## Big Four / MBB Delivery Methodology Alignment

Consulting PRDs should align with the delivery firm's methodology where applicable.

### Common Methodology Touchpoints

| Firm Style | PRD Adaptation |
|-----------|---------------|
| **Waterfall-heavy** (traditional Big Four) | More detailed upfront, fewer open questions, formal change control |
| **Agile transformation** (modern consulting) | Iterative PRDs, feedback loops built into milestones, sprint-aligned stories |
| **Design thinking** (MBB) | Heavier persona section, journey maps referenced, prototype-validated stories |
| **SAFe/Scaled Agile** | Epics map to SAFe epics, stories to SAFe features, PI planning alignment |

### Deliverable Packaging

Consulting PRDs are often packaged into larger deliverables:

| Package | Contents | Audience |
|---------|----------|----------|
| Business Requirements Document (BRD) | Collection of all epic PRDs + executive summary | Steering committee |
| Functional Specification Document (FSD) | PRDs + spec output combined | Implementation team |
| Solution Design Document (SDD) | enterprise-architect + spec outputs referencing PRDs | Architecture review board |

---

## Consulting-Specific Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| No SOW traceability | Scope disputes, unpaid work | Map every epic to SOW deliverables |
| Missing approval gates | Client surprises at review | Define gates upfront in PRD Section 11 |
| Ignoring TOM | Requirements disconnected from operating model | Ground every story in L3-L4 process changes |
| No change management | System delivered but not adopted | Include change impact and training stories |
| Single-workstream thinking | Dependencies discovered late | Map cross-workstream dependencies explicitly |
| Gold-plating beyond SOW | Scope creep, margin erosion | Scope Out section must reference SOW boundaries |
| No maturity metrics | Cannot prove transformation value | Include maturity progression in success metrics |

---

*pm-prd-generator v1.0 | Consulting PRD Patterns*
