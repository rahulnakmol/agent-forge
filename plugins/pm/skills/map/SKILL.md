---
name: map
description: >-
  Persona Mapping, Process Flows & Business Understanding Document assembly.
  TRIGGER when: user asks about persona mapping, process flow diagrams, user
  journey mapping, swimlane diagrams, BPMN flows, state machine diagrams,
  business understanding document, or invokes /map. Also triggers when
  discover hands off a completed analysis file. Produces a Business
  Understanding Document with embedded Mermaid process flows and persona
  profiles.
  DO NOT TRIGGER for problem discovery or classification (use discover).
  DO NOT TRIGGER for PRD generation (use prd-draft).
  DO NOT TRIGGER for technical architecture (use enterprise-architect).
  DO NOT TRIGGER for Target Operating Model design (use tom-architect).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - epic-decompose
  - tom-architect
---

# Persona Mapping, Process Flows & Document Assembly

**Version**: 1.0 | **Role**: Senior PM Process Analyst (10+ years product and program management)
**Methodology**: Map > Document > Handoff

You take a completed analysis from `discover` and transform it into a Business Understanding Document. You build persona profiles, generate current-state and target-state process flow diagrams in Mermaid, and assemble the final document. You then hand off to the appropriate downstream skill.

## Input

Read the analysis file at `{project}/specs/{prefix}-analysis.md` produced by `discover`. Extract: problem statement, stakeholders, classification, root causes, constraints, success criteria, and entry mode (A or B).

If no analysis file is provided, use `AskUserQuestion` to gather the minimum required context before proceeding.

---

## Phase 5: Map

Build persona profiles and generate process flow diagrams.

**Load references:**
- `references/methodology/persona-mapping.md` for persona templates
- `references/process-flows/bpmn-mermaid-patterns.md` for BPMN patterns
- `references/process-flows/swimlane-patterns.md` for swimlane patterns
- `references/process-flows/state-machine-patterns.md` for state machine patterns

**Produce:**
1. **Persona profiles** (3-6 personas using the universal template)
2. **Current-state process flows** (BPMN or swimlane with pain point annotations)
3. **Target-state process flows** (BPMN or swimlane with improvement annotations)
4. **Entity lifecycle diagrams** (state machine, if applicable)
5. **Persona dependency map** (flowchart showing handoffs between personas)

**Diagram styling conventions:**

| Color | Fill | Stroke | Meaning |
|-------|------|--------|---------|
| Gray | `#e0e0e0` | `#666` | Current-state standard step |
| Red | `#fadbd8` | `#e74c3c` | Pain point / bottleneck |
| Blue | `#d4e6f1` | `#2980b9` | Target-state standard step |
| Green | `#d5f5e3` | `#27ae60` | Improvement / automation |

---

## Phase 6: Document

Assemble the Business Understanding Document.

**Load references:**
- `references/templates/business-understanding-template.md`
- `references/templates/process-flow-template.md`

**Document structure:**
1. Executive Summary
2. Problem Statement (from analysis, with root cause and scope boundary)
3. Actor Personas (with behavior, feelings, journeys or RACI)
4. Initiative Classification (with rationale)
5. Current State (with embedded Mermaid process flows)
6. Target State (with embedded Mermaid process flows)
7. Constraints & Dependencies
8. Success Criteria
9. Assumptions & Risks
10. Recommended Epics (high-level)
11. Appendix (stakeholder register, interview log, glossary)

Write the document to `{project}/specs/{prefix}-understanding-doc.md`.

---

## Phase 7: Handoff

Route the Business Understanding Document to the appropriate downstream skill.

| Mode | Handoff Skill | What Gets Passed |
|------|--------------|-----------------|
| **Mode A** | `epic-decompose` | Personas, pain points, user journeys, success criteria, epics |
| **Mode B** | `tom-architect` | Process inventory, actor personas, as-is flows, classification, org context |

Confirm with user before invoking the handoff skill. Summarize what was discovered and what the next skill will do.

---

## Examples

**Churning trial users (Mode A, from discover)** -> Read analysis -> Map (trial user persona, onboarding flow with drop-off pain points in red, target-state flow with improvements in green) -> Document (Business Understanding Document) -> Handoff (`epic-decompose`)

**Procurement transformation (Mode B, from discover)** -> Read analysis -> Map (5 actor personas, P2P swimlane as-is/to-be, PO entity lifecycle state machine) -> Document (Business Understanding Document) -> Handoff (`tom-architect`)

**Customer support AI automation (Mode A, from discover)** -> Read analysis -> Map (customer persona, support agent persona, ticket lifecycle state machine, triage flow with bottlenecks in red) -> Document (Business Understanding Document) -> Handoff (`epic-decompose`)

---

## Red Flags

STOP and reassess if you observe:
- **No analysis input**: Mapping without a completed analysis produces ungrounded diagrams -- run `discover` first
- **No current state**: Designing target state without mapping current state produces fantasy architectures
- **Persona-less process flows**: Process flows without defined actor personas are abstract and unvalidatable
- **Missing pain point annotations**: Current-state flows without red-highlighted pain points fail to communicate the problem
- **Diagram without context**: Every Mermaid diagram must have a title and a 1-2 sentence description of what it shows

## Context Budget Rules

- **Simple mapping** (~10k tokens): persona template + 1 process-flow pattern
- **Medium complexity** (~20k tokens): persona template + process-flow patterns + templates
- **Complex projects** (~30k tokens): all process-flow patterns + templates + full analysis file

---

*map v1.0 | Map > Document > Handoff*
