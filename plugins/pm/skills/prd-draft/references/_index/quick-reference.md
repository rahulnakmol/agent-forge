# PRD Generator Quick Reference

## Workflow Phases

| Phase | Name | Key Action | Gate |
|-------|------|-----------|------|
| 1 | **Receive** | Detect input mode, load upstream artifacts | Input source confirmed |
| 2 | **Decompose** | Break understanding doc into epics | Epic list approved by user |
| 3 | **Draft** | Generate one PRD per epic using template | All 12 sections populated |
| 4 | **Validate** | Check completeness, INVEST, testability | Validation checklist passes |
| 5 | **Deliver** | Write PRD files, generate index | Files written to `{project}/prd/` |

## Input Modes

| Mode | Trigger | Reads | Epic Source |
|------|---------|-------|------------|
| A (SaaS) | Understanding doc exists, no TOM | `{project}/discovery/understanding-doc.md` | Personas + recommended epics |
| B (Consulting) | Understanding doc + TOM exist | Understanding doc + `{project}/tom/` | TOM L1-L4 gaps + persona-role maps |
| C (Standalone) | No upstream artifacts | User provides via `AskUserQuestion` | User-defined requirements |

## PRD Sections Checklist

- [ ] 1. Problem Statement & Business Context
- [ ] 2. Stakeholders & Personas
- [ ] 3. TOM Alignment (Mode B only)
- [ ] 4. Epic Definition (As a/I want/So that + scope in/out)
- [ ] 5. User Stories (INVEST-compliant, Given-When-Then AC)
- [ ] 6. Key Features & Business Value (Star Level 1-11)
- [ ] 7. Success Metrics (baseline + target + method + frequency)
- [ ] 8. Constraints & Assumptions (+ risk table)
- [ ] 9. Technical Considerations (non-prescriptive)
- [ ] 10. Process Flow References (Mermaid diagrams)
- [ ] 11. Release & Rollout (strategy + rollback)
- [ ] 12. Open Questions (owner + due date)

## File Naming

```
{project}/prd/{epic-name}-prd.md       # Individual epic PRD
{project}/prd/_prd-index.md            # Summary index of all PRDs
```

Epic names: lowercase, hyphenated. Examples: `user-onboarding-prd.md`, `data-migration-prd.md`.

## INVEST Criteria (User Stories)

| Letter | Criterion | Test |
|--------|-----------|------|
| **I** | Independent | Can be developed without other stories in this epic |
| **N** | Negotiable | Implementation details are not prescribed |
| **V** | Valuable | Delivers clear value to a specific persona |
| **E** | Estimable | Team can estimate effort (S/M/L/XL) |
| **S** | Small | Fits within a single sprint |
| **T** | Testable | Has Given-When-Then acceptance criteria |

## User Story Format

```
As a {persona},
I want {action},
So that {value}.
```

## Acceptance Criteria Format

```
Given {precondition}
When {action}
Then {expected result}
```

## Priority Levels

| Code | Priority | Description |
|------|----------|-------------|
| MH | Must Have | Core functionality, epic fails without it |
| SH | Should Have | Important but epic is viable without it |
| CH | Could Have | Nice-to-have, include if time permits |

## Complexity Levels

| Size | Typical Effort | Guideline |
|------|---------------|-----------|
| S | 1-2 days | Single component, well-understood pattern |
| M | 3-5 days | Multiple components, some unknowns |
| L | 1-2 weeks | Cross-cutting, integration required |
| XL | 2+ weeks | Should be split into smaller stories |

## Star Level Scale (Features Table)

Levels 1-11 rate the feature experience from minimum viable (1) to magical (11). Used by `pm-prd-reviewer` for validation linkage.

| Range | Meaning |
|-------|---------|
| 1-3 | Functional but basic (gets the job done) |
| 4-6 | Good experience (meets expectations) |
| 7-9 | Great experience (exceeds expectations, delightful) |
| 10-11 | Transformative (redefines what users expect) |

## Reference Paths

| Category | Path |
|----------|------|
| Framework overview | `references/_index/prd-framework-overview.md` |
| This cheat sheet | `references/_index/quick-reference.md` |
| Epic decomposition | `references/methodology/epic-decomposition.md` |
| User story writing | `references/methodology/user-story-writing.md` |
| Acceptance criteria | `references/methodology/acceptance-criteria-patterns.md` |
| Master template | `references/templates/prd-master-template.md` |
| Epic PRD template | `references/templates/epic-prd-template.md` |
| User story template | `references/templates/user-story-template.md` |
| SaaS patterns | `references/contexts/saas-prd-patterns.md` |
| Consulting patterns | `references/contexts/consulting-prd-patterns.md` |
| Intercom style example | `references/examples/intercom-prd-style.md` |
| Airbnb style example | `references/examples/airbnb-prd-style.md` |

## Suite Skills

| Skill | When to Invoke |
|-------|---------------|
| `pm-discovery` | Need business understanding doc (upstream) |
| `pm-prd-reviewer` | PRD ready for validation (downstream) |
| `spec` | PRD approved, need technical specs (downstream) |
| `enterprise-architect` | Need solution architecture from PRD collection |
| `tom-architect` | Need TOM for consulting pipeline (upstream) |

---

*pm-prd-generator v1.0 | Quick Reference*
