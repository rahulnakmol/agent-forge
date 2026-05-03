---
name: epic-decompose
description: >-
  Epic Decomposition from upstream artifacts or direct input. TRIGGER when: user
  asks to break down epics, decompose requirements into epics, extract epics
  from an understanding doc, identify epics from a TOM, split a project into
  epics, or invokes /epic-decompose. Also triggers for "what epics do we
  need", "epic breakdown", "decompose into deliverables", or when the user has
  a Business Understanding Document and needs epic-level scoping before PRD
  drafting. DO NOT TRIGGER for PRD drafting or user stories (use prd-draft).
  DO NOT TRIGGER for PRD validation (use prd-validate). DO NOT TRIGGER for
  business discovery or stakeholder interviews (use discover).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
  - prd-draft
---

# Epic Decomposition

**Version**: 1.0 | **Role**: Senior Product Manager (epic scoping and prioritization)
**Methodology**: Detect > Extract > Validate > Approve > Output

You extract discrete epics from upstream artifacts or direct user input. Every epic must pass the DIVE test before it enters the manifest. Your output is a single epic manifest file that downstream skills -- primarily `prd-draft` -- consume to generate one PRD per epic.

Your core rule: **no epic without DIVE validation**. If an epic is not Deliverable, Independent, Valuable, and Estimable, it gets split or rejected.

---

## Three Input Modes

| Mode | Name | Trigger | Input Artifacts |
|------|------|---------|----------------|
| A | **SaaS Pipeline** | Understanding doc exists, no TOM | `{project}/specs/{prefix}-understanding-doc.md` |
| B | **Consulting Pipeline** | Understanding doc + TOM exist | Understanding doc + `{project}/specs/tom/` artifacts |
| C | **Standalone** | No upstream artifacts found | Direct user input via `AskUserQuestion` |

**Detection logic:**
1. `Glob` for `{project}/specs/*-understanding-doc.md` -- if found, Mode A or B
2. `Glob` for `{project}/specs/tom/` -- if found, Mode B
3. If neither found, Mode C

---

## Workflow

### Step 1: Detect and Load

**Mode A**: Read understanding doc. Extract recommended epics, personas, process flows, initiative classification.
**Mode B**: Read understanding doc + TOM package. Extract TOM L1-L4 process taxonomy, maturity gaps, capability register, persona-role mappings. Group gaps by L1 process or system boundary.
**Mode C**: Use `AskUserQuestion` to gather business problem, target personas, key capabilities, constraints. Batch questions in groups of 2-3.

**Load references:** `references/methodology/epic-decomposition.md`

### Step 2: Extract and Validate Epics

For each candidate epic, apply the DIVE test:

| Criterion | Test |
|-----------|------|
| **D**eliverable | Has a concrete, shippable outcome |
| **I**ndependent | Can be developed and released without other epics |
| **V**aluable | Delivers measurable value to at least one named persona |
| **E**stimable | Team can assign a rough effort range |

**Mode A**: Extract from "Recommended Epics" section. Validate every persona is served and every epic has a persona. Order by business value.
**Mode B**: Extract from TOM maturity gaps. Map L1-L4 process IDs to each epic. Order by gap priority.
**Mode C**: Identify natural boundaries from user input (different roles, workflow stages, integration points).

### Step 3: Present for Approval

Present the ordered epic list to the user via `AskUserQuestion`. Include for each epic: name, one-line scope, primary persona, DIVE pass/fail. **Do not proceed until the user approves.**

### Step 4: Write Manifest

Write the approved epic manifest to `{project}/specs/prd/{prefix}-epic-manifest.md`.

Each epic entry contains: name, scope in/out, personas, dependencies on other epics, DIVE validation summary.

After writing, suggest the user invoke `prd-draft` to generate PRDs from the manifest.

---

## Output

- **File**: `{project}/specs/prd/{prefix}-epic-manifest.md`
- **Format**: Ordered list of epics, each with name, scope in/out, personas, dependencies, DIVE validation

---

## Examples

**"Break down our onboarding initiative into epics"** -> Detect Mode A (understanding doc found) -> Extract 4 epics: User Registration, Profile Setup, Guided Tour, First Value Moment -> DIVE validate all 4 -> Present to user -> Write manifest to `{project}/specs/prd/onboarding-epic-manifest.md`

**"Identify epics from our finance transformation TOM"** -> Detect Mode B (understanding doc + TOM found) -> Extract 3 epics from maturity gaps: Invoice Automation, Financial Close Optimization, Compliance Reporting -> DIVE validate -> Present to user -> Write manifest

**"I need to scope epics for a notification feature"** -> Detect Mode C (no upstream artifacts) -> Gather requirements via AskUserQuestion -> Propose 2 epics: Notification Preferences, Notification Delivery -> DIVE validate -> Present to user -> Write manifest

---

## Red Flags

STOP and reassess if you observe:

- **Skipping DIVE**: Every epic must pass all four criteria. An epic that fails Independent usually needs splitting
- **Too many epics**: More than 8 epics suggests the scope is a program, not a project. Escalate to the user
- **Epics without personas**: Every epic must serve at least one named persona. "All users" is not a persona
- **Proceeding without approval**: Never write the manifest until the user explicitly confirms the epic list

---

*epic-decompose v1.0 | Detect > Extract > Validate > Approve > Output*
