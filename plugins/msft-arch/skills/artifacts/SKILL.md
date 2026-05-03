---
name: artifacts
description: >-
  Architecture workbook generator for Microsoft projects. TRIGGER when: user
  needs Architecture Decision Records (ADR), effort estimation workbooks,
  RAID logs, solution design documents, or test strategy workbooks, or invokes
  /artifacts. Generates structured Excel workbooks using the xlsx skill.
  DO NOT TRIGGER for HLD/LLD documents (use docs), tech specs (use spec),
  or design work (use specialist skills).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - xlsx
---

# Architecture Artifact Generator

**Version**: 1.0 | **Role**: Workbook artifact producer

You generate structured Excel workbook artifacts for architecture engagements. Read `references/artifacts/artifact-overview.md` for the master catalog.

**Always offer a review checkpoint** before generating each workbook:
> "I've prepared [N] entries for the [artifact name]. Review before generating the Excel file?"

## Artifact Types

### 1. Architecture Decision Records (ADR) Workbook
Read `references/artifacts/adr-workbook-spec.md` for full specification.

| Column | Values/Format |
|--------|--------------|
| ADR Ref No | `MS-[TECH]-[PLATFORM]-[PROJECT]-XXX` |
| Title | Concise decision statement |
| Context | Technical assumptions + key considerations |
| Decision | Chosen approach with rationale |
| Consequence | Risks mitigated + operational impacts |
| Status | In Design / In Review / Supported / Refreshed / Baselines |

**TECH codes**: AI, DATA, INT, SEC, INFRA, APP
**PLATFORM codes**: PP, AZURE, D365, M365, ENTRA

### 2. Effort Estimation Workbook
Read `references/artifacts/effort-estimation-spec.md` for full specification.

| Column | Values/Format |
|--------|--------------|
| Sl No. | Auto-increment |
| Epic/Module/Work stream | Hierarchical grouping |
| RFR Reference | Requirements traceability ID |
| Requirements/User Stories | Detailed description |
| Capability | Azure / Power Platform / Data & AI / Integration / Software Engineering / Testing / D365 CE+PP / D365 F&O (X++) / Databricks / Microsoft Fabric |
| MOSCOW | MH / SH / CH / WH |
| Fit Gap | OOB / Config / Customization / Third Party |
| Complexity | V.Simple / Simple / Medium / Complex / V.Complex |
| Volume/No of Units | Story point measure |

### 3. RAID Log Workbook
Read `references/artifacts/raid-log-spec.md` for full specification.

| Column | Values/Format |
|--------|--------------|
| RAID Name | Descriptive identifier |
| Type | Risk / Assumption / Issue / Dependency |
| Description | Detailed description |
| Mitigation | Action plan |
| Owner | Person/role responsible |
| Referenced ADR | Cross-reference to ADR Ref No |

### 4. Solution Design Document Workbook
Read `references/artifacts/solution-design-doc-spec.md` for full specification.

### 5. Test Strategy Workbook
Read `references/artifacts/test-strategy-spec.md` for full specification.

## Sub-Agent Orchestration

For full engagements, generate all 5 workbooks in parallel:
- Dispatch 5 artifact agents simultaneously (ADR + Effort + RAID + Solution Design + Test Strategy)
- Each uses the xlsx skill independently

## Handoff Protocol

```markdown
## Handoff: artifacts → docs
### Artifacts Produced
- ADR workbook: [N] decisions recorded
- Effort estimation: [N] items with MOSCOW + Fit-Gap + Complexity
- RAID log: [N] entries
- Solution Design: [N] components documented
- Test Strategy: [N] test scenarios defined
### Context for Next Skill
- [ADR references for HLD/LLD cross-referencing]
### Open Questions
- [items needing stakeholder review]
```
