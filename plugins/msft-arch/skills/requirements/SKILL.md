---
name: requirements
description: >-
  Structured requirements gathering and fit-gap analysis for Microsoft architecture
  projects. TRIGGER when: user needs to elicit requirements, perform fit-gap analysis,
  capability mapping, MOSCOW prioritization, or invokes /requirements. Gathers
  functional and non-functional requirements, classifies fit-gap (OOB/Config/Custom/3rd
  Party), applies MOSCOW prioritization, and outputs a requirements register.
  DO NOT TRIGGER for discovery (use discover) or design (use specialist skills).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - AskUserQuestion
---

# Requirements Gathering

**Version**: 1.0 | **Role**: Structured requirements elicitation and analysis

You gather, classify, and prioritize requirements. Your output is a requirements register that feeds into specialist skills and artifact generation.

## Requirements Protocol

Use `AskUserQuestion` in batches of 2-3 related items. Do not ask all questions at once.

### Step 1: Functional Requirements
Read `references/requirements/requirements-gathering.md` for the full question bank:
- Business process requirements
- Integration requirements
- Data requirements
- Security and compliance requirements
- Performance and scalability requirements
- User experience requirements
- Reporting and analytics requirements

### Step 2: Non-Functional Requirements (NFRs)
For each NFR category, capture specific targets:
- **Availability**: target uptime (99.9%, 99.95%, 99.99%)
- **Performance**: response time, throughput, concurrent users
- **Scalability**: growth projections, burst capacity
- **Security**: authentication method, data classification, encryption
- **Compliance**: regulatory frameworks, data residency
- **Disaster Recovery**: RTO, RPO targets

### Step 3: Fit-Gap Analysis
Read `references/requirements/fit-gap-analysis.md` and classify each requirement:
- **OOB** (Out of Box): Available in platform with no changes
- **Config**: Available via configuration/settings
- **Customization**: Requires development
- **Third Party**: Requires ISV/partner solution

### Step 4: Capability Mapping
Read `references/requirements/capability-mapping.md` to map requirements to stack capabilities.

### Step 5: MOSCOW Prioritization
Assign each requirement a priority:
- **MH** (Must Have): Critical for go-live, non-negotiable
- **SH** (Should Have): Important but not blocking
- **CH** (Could Have): Desirable if time/budget permits
- **WH** (Won't Have): Explicitly out of scope for this phase

Push back if ALL requirements are Must Have: prioritization has failed.

## Output: Requirements Register

Output a markdown table with columns:
| ID | Requirement | Category | MOSCOW | Fit-Gap | Capability | NFR Target | Notes |

Then produce:

```markdown
## Handoff: requirements → [artifacts / specialist skills]
### Decisions Made
- [N] requirements gathered, classified, and prioritized
- Fit-gap: [X] OOB, [Y] Config, [Z] Custom, [W] Third Party
### Artifacts Produced
- Requirements register (inline above)
### Context for Next Skill
- [structured requirements data]
### Open Questions
- [requirements needing further clarification]
```
