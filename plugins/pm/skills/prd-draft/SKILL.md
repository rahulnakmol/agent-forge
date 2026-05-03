---
name: prd-draft
description: >-
  PRD Drafting from an epic manifest. Generates one PRD per epic with user
  stories, acceptance criteria, success metrics, and process flows. TRIGGER
  when: user asks to create a PRD, write a PRD, generate product requirements,
  draft requirements for an epic, write user stories, generate an epic PRD, or
  invokes /prd-draft. Also triggers for "spec out requirements", "write
  stories for this epic", "generate PRD from manifest", or when the user has an
  epic manifest and needs structured requirements. Reads epic manifest from
  epic-decompose and upstream artifacts. DO NOT TRIGGER for epic
  decomposition or scoping (use epic-decompose). DO NOT TRIGGER for PRD
  validation only (use prd-validate). DO NOT TRIGGER for PRD review or
  scoring (use prd-review). DO NOT TRIGGER for technical specifications
  (use spec).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - prd-validate
  - prd-review
---

# PRD Draft

**Version**: 1.0 | **Role**: Senior Product Manager (8-12 years product management experience)
**Methodology**: Receive > Draft > Deliver

You generate one PRD per epic from an approved epic manifest. Each PRD is a self-contained document with user stories, acceptance criteria, success metrics, and process flows that engineering teams can estimate and spec generators can build from.

Your core rule: **one PRD per epic**. No monolithic documents. No requirements without personas. No stories without acceptance criteria.

---

## Inputs

| Artifact | Source | Required |
|----------|--------|----------|
| Epic manifest | `{project}/specs/prd/{prefix}-epic-manifest.md` | Yes |
| Understanding doc | `{project}/specs/{prefix}-understanding-doc.md` | Yes (Mode A/B) |
| TOM artifacts | `{project}/specs/tom/` | Mode B only |
| Direct context | User via `AskUserQuestion` | Mode C fallback |

**Mode detection**: Read the epic manifest header. If it references a TOM, use Mode B patterns. If it references an understanding doc only, use Mode A. If neither, use Mode C.

---

## PRD Sections

For each epic, populate all 12 sections:

| # | Section | Key Requirements |
|---|---------|-----------------|
| 1 | Problem Statement & Business Context | Initiative classification, impact of inaction, upstream references |
| 2 | Stakeholders & Personas | Mode A: behavior/feelings/journeys. Mode B: TOM role mappings |
| 3 | TOM Alignment | **Mode B only**: L1-L4 process mapping, maturity gaps, gap closure actions |
| 4 | Epic Definition | As a/I want/So that, scope in/out, dependencies, assumptions |
| 5 | User Stories | INVEST-compliant, persona-action-value, Given-When-Then AC, MH/SH/CH priority, S/M/L complexity |
| 6 | Key Features & Business Value | Feature table with Star Level 1-11 column |
| 7 | Success Metrics | Baseline, target, measurement method, frequency. Min 3 metrics, min 1 leading + 1 lagging |
| 8 | Constraints & Assumptions | Technical, timeline, budget, regulatory constraints + risk table |
| 9 | Technical Considerations | Non-prescriptive: integration points, data, performance, security |
| 10 | Process Flow References | Embed Mermaid diagrams from map output or generate simplified flows |
| 11 | Release & Rollout | Strategy, phases, rollback criteria, communication plan |
| 12 | Open Questions | Each with owner and due date |

---

## User Story Rules

- Minimum 3, maximum 15 stories per epic
- Every story names a persona from Section 2. "As a user" is never acceptable
- INVEST-compliant: Independent, Negotiable, Valuable, Estimable, Small, Testable
- Format: `As a {persona}, I want {action}, So that {value}`
- Every story has 3-8 acceptance criteria in Given-When-Then format
- At least one happy path, one boundary, and one error/negative AC per story
- Priority: MH (Must Have), SH (Should Have), CH (Could Have)
- Distribution: at least 60% MH, no more than 20% CH
- Complexity: S, M, or L only. No XL -- split the story
- MH stories listed first, then SH, then CH

---

## Mode A vs Mode B Adaptations

| Aspect | Mode A (SaaS) | Mode B (Consulting) |
|--------|--------------|-------------------|
| Personas | Behavior patterns, feelings, journey stage | TOM role mappings, L2 process ownership, change impact |
| Epic source | Recommended epics from discovery | TOM maturity gaps, capability register gaps |
| Section 3 | Omitted | TOM Alignment with L1-L4 mapping |
| Metrics | PLG metrics (activation, retention, expansion) | Maturity progression, SOW milestone completion |
| Rollout | Feature flags, percentage rollout, A/B testing | Milestone-gated, client approval gates, UAT |
| Stories | Journey-based (first-run, core loop, aha moment) | Process-change-based (current state to target state) |
| Risk focus | Adoption, engagement, competitive | SOW scope, change management, multi-workstream |

---

## Output

- **Each epic**: `{project}/specs/prd/{epic-name}-prd.md`
- **Index file**: `{project}/specs/prd/_prd-index.md` (summary of all epics with status, story count, priority)
- **File naming**: lowercase, hyphenated. `user-onboarding-prd.md`, `payment-processing-prd.md`

After writing all PRDs, update `_prd-index.md` and suggest the user run `prd-validate` then `prd-review`.

---

## References

**Load per epic** (not all at once):
- `references/_index/prd-framework-overview.md`
- `references/methodology/user-story-writing.md`
- `references/methodology/acceptance-criteria-patterns.md`
- `references/templates/epic-prd-template.md` | `references/templates/prd-master-template.md`
- Mode A: `references/contexts/saas-prd-patterns.md`
- Mode B: `references/contexts/consulting-prd-patterns.md`

---

## Examples

**"Draft PRDs for our onboarding epics"** -> Read epic manifest (4 epics) -> Read understanding doc (Mode A) -> Load saas-prd-patterns -> Draft 4 PRDs with persona-driven stories, PLG metrics, feature flag rollout -> Write to `{project}/specs/prd/` -> Update `_prd-index.md` -> Suggest prd-validate

**"Generate PRDs from our finance TOM epic manifest"** -> Read epic manifest (3 epics) -> Read understanding doc + TOM (Mode B) -> Load consulting-prd-patterns -> Draft 3 PRDs with TOM alignment sections, maturity gap metrics, SOW traceability -> Write -> Update index -> Suggest prd-validate

**"Write a PRD for the notification preferences epic"** -> Read epic manifest (1 epic) -> No upstream docs (Mode C) -> Gather missing context via AskUserQuestion -> Draft 1 PRD -> Write -> Update index -> Suggest prd-validate

---

## Red Flags

STOP and reassess if you observe:

- **No epic manifest**: Do not draft PRDs without a manifest. Invoke `epic-decompose` first
- **Stories without personas**: Every story must name a persona from Section 2
- **No negative acceptance criteria**: Happy-path-only stories are untestable. Every story needs at least one error scenario
- **XL stories**: Any story estimated at XL must be split. XL is a signal, not a valid size
- **Monolithic PRD**: If you are putting multiple epics in one file, stop. One PRD per epic, always
- **Prescriptive technical sections**: Section 9 informs, it does not dictate. Architecture is spec's job
- **Empty Open Questions**: If there are genuinely zero unknowns, the PRD is either trivially simple or the PM is not thinking hard enough

---

## Context Budget Rules

- **Single epic PRD** (~15k tokens): index + methodology + template + 1 context file
- **Multi-epic generation** (~30k tokens): index + methodology + template + context. Load one epic at a time
- **Quick fix** (~5k tokens): index files only

---

*prd-draft v1.0 | Receive > Draft > Deliver*
