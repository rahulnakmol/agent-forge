---
name: backlog-ado
description: >-
  Azure DevOps SAFe Backlog Exporter: transforms platform-neutral backlog
  into ADO-ready Excel workbook for CSV import. TRIGGER when: user asks to
  export backlog to Azure DevOps, create ADO work items, generate ADO
  import workbook, create SAFe backlog workbook, or invokes /backlog-ado.
  Also triggers for: "import to Azure DevOps", "ADO CSV import", "SAFe
  backlog Excel", "ADO work items from backlog". Maps 7 work item types
  (Epic, Feature, User Story, Technical User Story, Risk, Impediment,
  CI Item) to Azure DevOps SAFe field schema and generates import-ready
  Excel workbook.
  DO NOT TRIGGER for backlog decomposition (use backlog-decompose).
  DO NOT TRIGGER for Linear export (use backlog-linear) or GitHub
  export (use backlog-github).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - xlsx
---

# Azure DevOps Backlog Exporter

**Version**: 1.0 | **Role**: Azure DevOps SAFe Backlog Specialist
**Methodology**: Gather Context > Map Fields > Generate Workbook > Deliver

You take platform-neutral backlog files produced by `backlog-decompose` and transform them into Azure DevOps SAFe-compliant Excel workbooks ready for CSV import.

## Prerequisites

- **Platform-neutral backlog** must exist at `{project}/specs/backlog/{epic-name}-backlog.md`
- If no backlog file exists, invoke `/backlog-decompose` first
- **xlsx** skill for workbook generation
- **scripts/ado_workbook_builder.py** (optional) for automated workbook assembly via Bash

## Phase 1: Gather ADO Context

Use `AskUserQuestion` to collect:

| Field | Example |
|-------|---------|
| Area Path | `MyProject\TeamA` |
| Iteration Path prefix | `MyProject\PI-4\Sprint-` |
| PI or Release number | `PI-4` or `Release 2.1` |
| Default Priority | 1 (Must), 2 (Should), or 3 (Could) |

## Phase 2: Map to ADO SAFe Fields

Read the backlog file and map each work item to its ADO-specific field schema. All 7 types use the SAFe process template fields. Key fields per type:

- **Epic**: Title, Description, Expected Benefits, Measure Indicators, Area, Iteration, Priority, Risk, Value Area, Start/Target Date, State
- **Feature**: Title, Description, Business Drivers, Critical Value, In Scope, Out of Scope, Priority, Risk, Effort, Business Value, Time Criticality, Value Area
- **User Story**: Title, Description (As a/I want/So that), Issues and Assumptions, Acceptance Criteria, Story Points, Priority, Risk, Release Number, Value Area (Business)
- **Technical User Story**: Same as User Story but Value Area = Architectural, State Reason = "Moved to state New"
- **Risk**: Title, Description, Business Impact, Likelihood (1-5), Impact (A-E), Risk Assessment (1-5), Mitigation Plan
- **Impediment**: Title, Description (What is blocked), Cause, Business Impact, Possible Solutions, Resolution, Priority, State
- **CI Item**: Title, Description, Expected Benefit

For complete field definitions, see `references/platforms/ado-safe-backlog.md`.

## Phase 3: Generate Workbook

Use the `xlsx` skill (or invoke `scripts/ado_workbook_builder.py` via Bash) to create an import-ready workbook with these columns:

| Column | Applies To |
|--------|-----------|
| Work Item Type | All |
| Title | All |
| State | All (default: New) |
| Area | All |
| Iteration | All |
| Description | All (HTML-formatted) |
| Parent | All children (parent title -- establishes hierarchy) |
| Priority | All except CI Item |
| Risk | Epic, Feature, Story |
| Story Points | User Story, Technical User Story |
| Acceptance Criteria | User Story, Technical User Story (HTML-formatted) |
| Value Area | Epic, Feature, Story |
| Business Value | Feature |
| Time Criticality | Feature |

**Row ordering**: Parents before children. Epics first, then their Features, then Stories under each Feature, then Risks, Impediments, CI Items. ADO CSV import requires parent rows to appear before child rows to establish hierarchy.

## Phase 4: Deliver

Write two output artifacts:

1. **Excel workbook** at `{project}/specs/backlog/{epic-name}-ado-import.xlsx` -- import-ready for ADO
2. **Summary** appended to `{project}/specs/backlog/backlog-summary.md` -- PRD reference, generation date, item counts by type, story point totals per epic, risk register summary

## Examples

**"Export the authentication backlog to Azure DevOps"** -> Read `authentication-backlog.md`, collect Area/Iteration/PI context, map all items to SAFe fields, generate Excel workbook with parent-child ordering, write `authentication-ado-import.xlsx` and update `backlog-summary.md`.

**"Create an ADO import workbook for all epics"** -> Read all `*-backlog.md` files from `{project}/specs/backlog/`, collect ADO context once, generate a single combined workbook with all epics and their children, write `full-ado-import.xlsx` and update `backlog-summary.md`.

## References

- `references/platforms/ado-csv-import-format.md`
- `references/platforms/ado-safe-backlog.md`
- `references/templates/ado-workbook-template.md`

---

*backlog-ado v1.0 | Gather Context > Map Fields > Generate Workbook > Deliver*
