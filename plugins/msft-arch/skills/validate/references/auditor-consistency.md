# Auditor #2: Consistency

Independent reviewer of architecture artifacts. This file contains the dispatch prompt and engineer checklist for the Consistency auditor in the Council-of-Three validation pattern.

## Dispatch Prompt

Pass this prompt verbatim as the Task subagent system prompt when dispatching Auditor #2.

```text
You are Auditor #2: Consistency. Independent reviewer of architecture artifacts.

Inputs you are given:
- All files in spec/design/
- All files in spec/decisions/ (ADRs produced this run)
- Discovery brief, requirements doc, stack-select decision

Your job: assert artifacts are mutually consistent.

Specific checks:
- Do ADRs contradict requirements? (e.g., requirement says "no PII in logs",
  ADR says "log full request body")
- Does the C4 Container diagram match the stack-select decision? (every
  container's technology must come from the selected stack)
- Are handoff blocks intact between skills? Each skill's handoff lists
  decisions; the next skill's input must reference those decisions explicitly.
- Do component names in diagrams match the components table in design.md
  exactly? (string-equal, case-sensitive)
- Do API contracts in api-contracts.md match the endpoints referenced in
  diagrams.md sequence diagrams?
- Do data models in design.md match the schemas in api-contracts.md?

Output format: same as Auditor #1 (severity, artifact, location, remediation).

DO NOT raise completeness gaps (that's auditor #1).
DO NOT raise speculative concerns (that's auditor #3).
```

## Consistency Check Matrix

The following checks are authoritative. Auditor #2 runs all of them.

### Check 1: ADRs vs. Requirements

```text
For each ADR in spec/decisions/:
  - Extract every constraint or technology choice it records.
  - Cross-reference against requirements.md.
  - Flag any ADR clause that directly contradicts a stated requirement.

Example contradictions to look for:
  - Requirement: "no PII in logs" / ADR: "log full request body"
  - Requirement: "data must remain in AU regions" / ADR: "use globally replicated Cosmos DB"
  - Requirement: "open-source stack only" / ADR: "use Azure Cognitive Search"
```

### Check 2: C4 Container Diagram vs. Stack-Select Decision

```text
For each container in context.md's C4 Level 2 diagram:
  - Extract the labeled technology (e.g., "Azure App Service", "PostgreSQL Flexible Server").
  - Verify it appears in the approved stack in spec/decisions/stack-select.md.
  - Flag any container whose technology is absent from the approved stack.
```

### Check 3: Handoff Blocks Between Skills

```text
For each skill handoff block found in any artifact:
  - Identify the "Decisions Made" list in the outgoing handoff.
  - Verify the receiving skill's artifact explicitly references each decision.
  - Flag missing references as consistency gaps (the chain is broken).
```

### Check 4: Component Names: Diagrams vs. Design Table

```text
For each component named in diagrams.md:
  - Find the corresponding row in the components table in design.md.
  - Assert string equality (case-sensitive, including punctuation).
  - Flag any name mismatch.

Example: "API Management" in diagram vs "APIM" in design table = FAIL.
```

### Check 5: API Contracts vs. Sequence Diagrams

```text
For each endpoint referenced in diagrams.md sequence diagrams:
  - Verify a matching entry exists in api-contracts.md.
  - Assert method, path, and actor match.
  - Flag missing or mismatched entries.
```

### Check 6: Data Models: Design vs. API Contracts

```text
For each entity in the data model section of design.md:
  - Find the corresponding schema in api-contracts.md.
  - Compare field names and types.
  - Flag any field that is present in one artifact but absent in the other.
  - Flag any field whose type differs between artifacts.
```

## Engineer Checklist

Pre-flight checks before dispatching Auditor #2.

```text
[ ] ADRs reviewed against requirements.md for direct contradictions
[ ] Every container in C4 diagram uses a technology from stack-select.md
[ ] All skill handoff blocks present and downstream skills reference upstream decisions
[ ] Component names in diagrams.md match design.md components table (case-sensitive)
[ ] Every sequence diagram endpoint exists in api-contracts.md with matching method + path
[ ] Entity field names and types match between design.md data model and api-contracts.md schemas
[ ] No orphan component: every component in design.md appears in at least one diagram
[ ] No orphan diagram element: every element in diagrams.md maps to a component in design.md
```

## Severity Guidance

| Severity | Meaning | Action |
|----------|---------|--------|
| blocker | Directly contradictory artifacts; will cause implementation errors | Must fix before merge |
| major | Significant naming or structural mismatch; teams will build different things | Fix before merge; document if deferred |
| minor | Minor naming drift; low immediate risk but accumulates as tech debt | Track in RAID log |
| nit | Cosmetic inconsistency (whitespace, punctuation in names) | Capture only if trivially fixable |

## DO NOT Boundaries

Auditor #2 is scoped strictly to **consistency between existing artifacts**:

- DO NOT flag missing sections or missing artifacts; that is Auditor #1 (Completeness).
- DO NOT raise failure-mode, scale, or security speculation; that is Auditor #3 (Adversarial).
- DO NOT suggest whether the chosen architecture is correct; only assert whether the artifacts agree with each other.
- DO NOT flag differences that are intentional and documented (e.g., an ADR that explicitly overrides a default requirement).

## Example Finding

```text
severity: major
artifact: spec/design/context.md vs spec/decisions/stack-select.md
section: C4 Container diagram: "Order Processing Service" container
finding: Container labeled technology "RabbitMQ" but stack-select.md approves
         only Azure Service Bus for message queuing.
remediation: Update C4 diagram technology label to "Azure Service Bus" or raise
             an ADR documenting the RabbitMQ exception with rationale.
```
