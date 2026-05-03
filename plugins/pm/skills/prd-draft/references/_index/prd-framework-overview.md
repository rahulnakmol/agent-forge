# PRD Generation Framework Overview

## Philosophy: One PRD Per Epic

The PRD Generator produces one standalone Product Requirements Document per epic. Each PRD is a self-contained specification that can be handed to a reviewer (`pm-prd-reviewer`), then to a technical team or spec generator (`spec`) without additional context gathering.

This is not a monolithic requirements document. It is a collection of focused, epic-scoped PRDs that together cover the full product scope.

**Why one-per-epic?**
- Each epic has a distinct business value proposition that deserves focused articulation
- Reviewers can validate one epic at a time without drowning in scope
- Technical teams can pick up individual PRDs for sprint planning
- PRDs can be prioritized, deferred, or dropped independently
- Downstream `spec` generates per-epic technical specifications aligned 1:1

---

## Three Input Modes

The PRD Generator adapts its behavior based on how it receives input. The mode determines which sections are populated, which upstream artifacts are consumed, and how epics are decomposed.

| Mode | Input Source | Epic Decomposition Driver | Key PRD Differences |
|------|-------------|--------------------------|---------------------|
| **A -- SaaS Pipeline** | Understanding Doc + process flows from `pm-discovery` | User personas (behavior, feelings, journeys), recommended epics | Persona-driven stories, PLG metrics, feature flags, engagement focus |
| **B -- Consulting Pipeline** | Understanding Doc + TOM output from `tom-architect` | TOM process taxonomy (L1-L4), maturity gaps, persona-role mappings | TOM Alignment section populated, SOW-grounded scope, maturity gap closure metrics |
| **C -- Standalone** | Direct user input | User-provided requirements gathered via `AskUserQuestion` | Minimal upstream context, heavier reliance on user clarification |

### Mode Detection Logic

1. Check for `{project}/discovery/understanding-doc.md` -- if present, Modes A or B
2. Check for `{project}/tom/` artifacts -- if present, Mode B (Consulting Pipeline)
3. If neither found, Mode C (Standalone) -- gather requirements via `AskUserQuestion`

---

## Upstream and Downstream Connections

### Upstream (inputs to PRD Generator)

| Source | Artifact | What It Provides |
|--------|----------|-----------------|
| `pm-discovery` | Understanding Document | Business problem, personas, process flows, recommended epics, initiative classification |
| `pm-discovery` | Process Flow Diagrams | Mermaid diagrams embedded in Section 10 of each PRD |
| `tom-architect` | TOM Package | Process taxonomy (L1-L4), maturity assessment, capability register, role mappings, KPI framework |

### Downstream (consumers of PRD output)

| Consumer | What It Reads | Purpose |
|----------|--------------|---------|
| `pm-prd-reviewer` | Individual epic PRDs | Validates completeness, consistency, testability, and business alignment |
| `spec` | Individual epic PRDs | Generates technical design specifications, C4 diagrams, implementation tasks |
| `enterprise-architect` | Epic PRD collection | Informs solution architecture, stack selection, effort estimation |

---

## Quality Standards

Every PRD produced by this skill must meet these criteria:

1. **Complete**: All 12 template sections are present (TOM Alignment conditional on Mode B)
2. **Persona-grounded**: Every user story traces back to an identified persona
3. **Testable**: Every acceptance criterion follows Given-When-Then and is unambiguous
4. **Measurable**: Success metrics have baselines, targets, measurement methods, and frequency
5. **Scoped**: Explicit scope-in and scope-out boundaries for the epic
6. **Traceable**: Features table includes Star Level (1-11) column for reviewer linkage
7. **Actionable**: A product reviewer can validate, and a tech team can estimate, from the PRD alone

---

## File Output Convention

Each epic PRD is written to: `{project}/prd/{epic-name}-prd.md`

Epic names are lowercase, hyphenated: `user-onboarding-prd.md`, `payment-processing-prd.md`, `reporting-dashboard-prd.md`.

When multiple epics are generated, a summary index is written to: `{project}/prd/_prd-index.md`

---

## PRD Template Structure (Summary)

| # | Section | Purpose |
|---|---------|---------|
| 1 | Problem Statement & Business Context | Why this epic exists, initiative classification |
| 2 | Stakeholders & Personas | Who is affected, persona details adapted per mode |
| 3 | TOM Alignment | Consulting path only: L1-L4 mapping, maturity gaps |
| 4 | Epic Definition | As a/I want/So that, scope boundaries, dependencies |
| 5 | User Stories | Persona-action-value, Given-When-Then AC, priority, complexity |
| 6 | Key Features & Business Value | Feature table with Star Level 1-11 column |
| 7 | Success Metrics | Baseline, target, method, frequency |
| 8 | Constraints & Assumptions | Technical, timeline, budget, regulatory + risk table |
| 9 | Technical Considerations | Non-prescriptive: integration points, data, performance, security |
| 10 | Process Flow References | Embedded Mermaid diagrams from pm-discovery |
| 11 | Release & Rollout | Strategy, phases, rollback criteria |
| 12 | Open Questions | Tracked with owner and due date |

Full template: `references/templates/epic-prd-template.md`

---

*pm-prd-generator v1.0 | One PRD Per Epic*
