# PRD Master Template -- Meta Documentation

## Purpose

This document describes the overall structure and philosophy of the PRD template used by pm-prd-generator. It explains how each section should be written, what good looks like, and how sections adapt between SaaS (Mode A) and Consulting (Mode B) paths.

For the actual fill-in template, see: `references/templates/epic-prd-template.md`

---

## Template Architecture

The PRD template has 12 sections. Sections 1-2 and 4-12 are always present. Section 3 (TOM Alignment) is conditional on Mode B (consulting pipeline).

### Section Dependency Flow

```
Section 1 (Problem) --> Section 4 (Epic Definition) --> Section 5 (User Stories)
Section 2 (Personas) --> Section 5 (User Stories) --> Section 6 (Features)
Section 3 (TOM) ------> Section 7 (Metrics) via maturity gap targets
Section 5 (Stories) ---> Section 6 (Features) --> Section 7 (Metrics)
Section 8 (Constraints) <--> Section 9 (Technical) -- bidirectional
Section 10 (Flows) feeds into Sections 5 and 6
Section 11 (Release) depends on Sections 6 and 8
Section 12 (Questions) accumulates throughout
```

---

## Section Writing Guidelines

### Section 1: Problem Statement & Business Context

**Purpose**: Establish why this epic exists and how it connects to the broader initiative.

**Write this section to answer:**
- What business problem does this epic solve?
- Who experiences this problem?
- What happens if we do nothing?
- How does this epic fit into the overall initiative?

**Must include:**
- Initiative classification: New Product | Feature Enhancement | Operational Improvement | Compliance/Regulatory | Technical Debt | Platform Migration
- Business impact: revenue, cost, risk, or efficiency quantified where possible
- Link to understanding document section (Mode A/B)

**Tone**: Business-first. No technical jargon. A non-technical stakeholder should understand this section completely.

### Section 2: Stakeholders & Personas

**Purpose**: Define who cares about this epic and who will use the resulting capability.

**Mode A (SaaS) adaptation:**
- Persona table includes: behavior patterns, feelings/frustrations, journey stage, engagement metrics
- Focus on user segments, activation triggers, and retention signals

**Mode B (Consulting) adaptation:**
- Persona table includes: TOM role mapping, organizational position, process ownership
- Focus on operational roles, approval authorities, and change impact

**Must include:**
- Stakeholder table (name/role, interest, influence, communication needs)
- Persona detail (at least 2 fields beyond name and role)

### Section 3: TOM Alignment (Consulting Only)

**Purpose**: Ground the epic in the Target Operating Model. This section does not exist in SaaS PRDs.

**Must include:**
- L1-L4 process mapping (which TOM processes does this epic address)
- Current maturity level and target maturity level for each mapped process
- Gap closure actions (what changes in the operating model when this epic ships)
- Capability register reference IDs from the TOM workbook

**Write this section as a bridge** between the TOM (strategic) and the user stories (tactical).

### Section 4: Epic Definition

**Purpose**: Precisely define the epic scope.

**Must include:**
- Epic statement in As a/I want/So that format
- Scope In: explicit list of what this epic covers
- Scope Out: explicit list of what this epic does NOT cover (even if someone might assume it does)
- Dependencies: other epics, external systems, team dependencies
- Assumptions: things taken as true that could invalidate scope if wrong

### Section 5: User Stories

**Purpose**: The detailed requirements. Each story follows INVEST and persona-action-value format.

**Must include per story:**
- Story ID (format: `{EPIC-PREFIX}-{NNN}`, e.g., `UO-001`)
- Title
- Persona-action-value statement
- Acceptance criteria (Given-When-Then, 3-8 per story)
- Priority (MH/SH/CH)
- Complexity (S/M/L)
- Notes and dependencies (optional)

**Ordering**: MH stories first, then SH, then CH. Within priority, order by dependency (foundational stories before dependent ones).

### Section 6: Key Features & Business Value

**Purpose**: Summarize features at a higher level than individual stories, with business value articulation.

**Must include:**
- Feature table with columns: Feature, Description, Stories Covered, Business Value, Star Level (1-11)
- Star Level is the 11-star experience rating for reviewer linkage
- Each feature maps to one or more user stories

**Star Level guidance:**
- 1-3: Minimum viable (gets the job done, no delight)
- 4-6: Expected (meets industry standard)
- 7-9: Delightful (exceeds expectations, memorable)
- 10-11: Transformative (redefines what users expect in this category)

### Section 7: Success Metrics

**Purpose**: Define how we know this epic succeeded after launch.

**Must include per metric:**
- Metric name
- Baseline (current value or "N/A -- new capability")
- Target (specific number or range with timeframe)
- Measurement method (tool, query, survey)
- Frequency (real-time, daily, weekly, monthly, quarterly)

**At least 3 metrics per epic.** At least one leading indicator (predicts success) and one lagging indicator (confirms success).

### Section 8: Constraints & Assumptions

**Purpose**: Document the boundaries and unknowns that shape this epic.

**Must include:**
- Constraints table: Technical, Timeline, Budget, Regulatory, Organizational
- Assumptions list: things taken as true that have not been validated
- Risk table: Risk, Likelihood (H/M/L), Impact (H/M/L), Mitigation, Owner

### Section 9: Technical Considerations

**Purpose**: Provide non-prescriptive technical context for the engineering team.

**Critical rule**: This section informs, it does not prescribe. PRDs do not dictate architecture. That is the job of `spec` and `enterprise-architect`.

**May include:**
- Integration points (external APIs, data sources, existing systems)
- Data requirements (volume, sensitivity classification, retention)
- Performance expectations (response time, throughput, concurrent users)
- Security requirements (authentication, authorization, data protection)
- Accessibility requirements (WCAG level, supported devices)

### Section 10: Process Flow References

**Purpose**: Embed visual process flows for the epic's core workflows.

**Source**: Mermaid diagrams from `pm-discovery` process flow documentation.

**If no upstream diagrams exist**, generate simplified flowcharts showing the primary happy path and one alternative/error path for the epic's core workflow.

### Section 11: Release & Rollout

**Purpose**: Define how this epic gets to users.

**Must include:**
- Release strategy: Big bang | Phased rollout | Feature flag | Beta/GA
- Rollout phases (if phased): who gets it first, criteria for expansion
- Rollback criteria: what triggers a rollback, how rollback is executed
- Communication plan: how users are informed (in-app, email, training)

### Section 12: Open Questions

**Purpose**: Track unresolved items that could affect the PRD.

**Must include per question:**
- Question ID (format: `OQ-{NNN}`)
- Question text
- Owner (who is responsible for answering)
- Due date
- Status (Open | In Progress | Resolved)
- Resolution (filled in when resolved)

**Open questions are not a dumping ground.** Each question should be specific, answerable, and have an owner. If a question cannot be assigned to someone, it is too vague.

---

## Template Completeness Validation

Before delivering a PRD, validate:

| Check | Requirement |
|-------|------------|
| All sections present | Sections 1-2, 4-12 always; Section 3 if Mode B |
| Every story has AC | Minimum 3 Given-When-Then per story |
| Every story has priority | MH, SH, or CH assigned |
| Every story has complexity | S, M, or L assigned (no XL) |
| Every feature has Star Level | 1-11 rating in features table |
| At least 3 success metrics | With baseline, target, method, frequency |
| At least 1 risk identified | With likelihood, impact, mitigation |
| No open questions without owner | Every OQ has an assigned owner |

---

*pm-prd-generator v1.0 | PRD Master Template Meta Documentation*
