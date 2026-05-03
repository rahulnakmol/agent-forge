# Synthesis Protocol: Council of Three

This file governs the merge step after all three auditor subagents return. Follow it precisely to produce the final Validation Report.

## Protocol

```text
After all three auditors return, merge findings into a single Validation Report
ordered by severity then artifact.

Severity hierarchy:
- blocker: ship-stops. Must be resolved before merge.
- major: should be resolved before merge; document deferral if deferred.
- minor: track in RAID log; resolve in next iteration.
- nit: optional; capture only if fix is cheap.

Deduplication: if two auditors raise the same finding, merge into one entry
with both auditor IDs in the "raised by" column.

Conflict handling: if auditors disagree (rare; different lenses), keep both
findings and tag with auditor ID. Do not pick a winner; the architect resolves.

Ownership: each finding gets an owner, the skill that produced the artifact
in question (e.g., azure-architect, spec). Cross-cutting findings owned by agent.

Output is a single Validation Report file at validate/output.md with this header:

  ## Validation Report: Council of Three
  ### Summary
  - Status: [PASSED / FAILED: N blockers, M majors]
  - Auditors: Completeness, Consistency, Adversarial
  - Artifacts validated: [list]

  ### Findings (sorted by severity)
  | # | Severity | Artifact | Section | Finding | Owner | Raised by |
  |---|----------|----------|---------|---------|-------|-----------|
```

## Step-by-Step Synthesis Procedure

### Step S1: Collect All Findings

```text
Gather the raw finding lists from:
- Auditor #1 (Completeness) output
- Auditor #2 (Consistency) output
- Auditor #3 (Adversarial) output

Assign a temporary ID to each raw finding: C-001, C-002... (Completeness),
K-001, K-002... (Consistency), A-001, A-002... (Adversarial).
```

### Step S2: Deduplicate

```text
Compare all findings pairwise across auditor outputs.

Two findings are duplicates if:
- They reference the same artifact AND the same section/line AND the same root cause.
- The finding description is substantially identical despite different wording.

When a duplicate pair is found:
- Keep one entry.
- Merge the "raised by" field to include both auditor IDs.
  Example: "Completeness, Adversarial"
- Use the higher severity from the two entries.
- Use the more specific remediation of the two.
```

### Step S3: Handle Conflicts

```text
Two findings conflict if:
- They reference the same artifact and section AND reach opposite conclusions.
  Example: Auditor #2 says "C4 matches stack-select" and Auditor #3 says
  "C4 technology choice creates vendor lock-in risk inconsistent with requirements."

When a conflict is identified:
- Keep BOTH findings as separate rows.
- Tag each row's "raised by" column with the specific auditor ID.
- Add a note in the Finding column: "[Conflict: see row N]"
- Do not resolve the conflict; the architect decides.
```

### Step S4: Assign Ownership

```text
For each finding, assign an owner using this mapping:

Artifact path                   → Owner skill
spec/design/design.md           → spec
spec/design/context.md          → azure-architect (or relevant vertical)
spec/design/diagrams.md         → azure-architect (or relevant vertical)
spec/design/api-contracts.md    → spec
spec/design/tasks.md            → spec
spec/decisions/adr-*.md         → the skill named in the ADR title
standards/references/**         → agent (cross-cutting)
Multiple artifacts              → agent (cross-cutting)
```

### Step S5: Sort

```text
Sort all findings by:
1. Severity (blocker → major → minor → nit)
2. Within same severity: sort by artifact path (alphabetical)
3. Within same artifact: sort by section/line reference
```

### Step S6: Write Summary

```text
Count: blockers = B, majors = M.
Status = PASSED if B == 0 and M == 0, else FAILED.

Status line: "PASSED" or "FAILED: {B} blockers, {M} majors"

List all artifact paths that were reviewed in the "Artifacts validated" field.
```

### Step S7: Write Validation Report

```text
Write validate/output.md with the structure shown in the worked example below.
```

## Worked Example

This example shows a complete Validation Report produced by the synthesis step.

```markdown
## Validation Report: Council of Three

### Summary
- Status: FAILED: 2 blockers, 1 major
- Auditors: Completeness, Consistency, Adversarial
- Artifacts validated:
  - spec/design/design.md
  - spec/design/context.md
  - spec/design/diagrams.md
  - spec/design/api-contracts.md
  - spec/design/tasks.md
  - spec/decisions/adr-001-stack.md
  - spec/decisions/adr-002-data.md
  - spec/decisions/adr-003-messaging.md

### Findings (sorted by severity)

| # | Severity | Artifact | Section | Finding | Owner | Raised by |
|---|----------|----------|---------|---------|-------|-----------|
| 1 | blocker | spec/design/design.md | §4 NFRs | NFR "99.9% availability" in requirements.md has no "how met" entry in design.md §4. | spec | Completeness |
| 2 | blocker | spec/design/context.md vs spec/decisions/adr-001-stack.md | C4 Container diagram | Container "Order Processor" labeled "RabbitMQ" but stack-select approves only Azure Service Bus. Remediation: update diagram label or raise exception ADR. | azure-architect | Consistency |
| 3 | major | spec/design/design.md + spec/decisions/adr-003-messaging.md | §7 Assumptions & Risks | "What happens when Azure Service Bus is unavailable? No fallback, circuit breaker, or dead-letter strategy is documented. At 5,000 msg/hr peak a 15-min outage accumulates 1,250 unprocessed messages with no recovery path." | azure-architect | Adversarial |
| 4 | minor | spec/design/diagrams.md | Sequence diagram: Login flow | Endpoint POST /auth/token referenced in sequence diagram is absent from api-contracts.md. | spec | Completeness, Consistency |
| 5 | nit | spec/decisions/adr-002-data.md | Alternatives Considered | Alternatives Considered field contains only "N/A". Recommend brief rationale for at least one alternative evaluated. | spec | Completeness |
```

## Deduplication Example

```text
Completeness raised: "POST /auth/token missing from api-contracts.md (completeness gap)"
Consistency raised:  "POST /auth/token in sequence diagram has no matching api-contracts entry (consistency gap)"

Both reference same artifact (api-contracts.md) + same root cause (missing endpoint entry).
→ Merged into finding #4 above.
→ Raised by: Completeness, Consistency
→ Severity: minor (both rated minor; no upgrade needed)
→ Remediation: from Consistency finding (more specific: "add POST /auth/token with
  full request/response/auth/errors schema to api-contracts.md")
```

## Output File Location

The final Validation Report is written to:

```bash
validate/output.md
```

If that path does not exist yet, create it. Overwrite if it exists from a prior run.

## Quality Gate Rules

```text
PASSED  → all blockers = 0 AND majors = 0
FAILED  → any blocker >= 1 OR any major >= 1

A FAILED report MUST NOT proceed to the next pipeline stage.
A PASSED report with minors or nits may proceed; findings are tracked in RAID log.
```
