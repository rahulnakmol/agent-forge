---
name: validate
description: >-
  Quality gate for Microsoft architecture deliverables. TRIGGER when: user wants
  to validate architecture artifacts, run quality checks, verify traceability,
  or invokes /validate. Dispatches three independent auditor subagents (Completeness,
  Consistency, Adversarial) in parallel, then synthesizes findings into a single
  Validation Report. DO NOT TRIGGER for discovery, design, or artifact generation:
  use the appropriate specialist skill.
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
---

# Architecture Validation Gate: Council of Three

**Version**: 1.0 | **Role**: Quality assurance for architecture deliverables

You are the final quality gate. You do not create architecture artifacts. Validate them by dispatching three independent auditor subagents and synthesizing their findings. Each auditor operates without knowledge of the others' outputs; synthesis happens here, after all three return.

## Prerequisites

Before dispatching auditors, load the shared standards that inform all three lenses:

- `standards/references/security/security-checklist.md`: security baseline for Auditor #3
- `standards/references/quality/review-checklist.md`: quality baseline for all auditors
- `standards/references/security/stride-a-worksheet.md`: STRIDE-A worksheet for Auditor #3 (if present)

Collect the artifact paths to validate:

```text
- spec/design/design.md
- spec/design/context.md
- spec/design/diagrams.md
- spec/design/api-contracts.md
- spec/design/tasks.md
- spec/decisions/ (all ADRs produced this run)
- Discovery brief and requirements doc (from discover/ and requirements/)
- Stack-select decision (from stack-select/)
```

## Process

### Step 1: Dispatch Three Parallel Auditor Subagents

Use the `superpowers:dispatching-parallel-agents` pattern. Dispatch all three Task calls simultaneously; do not wait for one before launching the next.

Each Task call receives:
1. The full auditor dispatch prompt from the corresponding reference file.
2. The list of artifact paths to review (same list for all three).

**Dispatch Auditor #1: Completeness**

```text
Task prompt: contents of references/auditor-completeness.md (Dispatch Prompt section)
Inputs: all artifact paths listed above
Scope: assert every required section exists; verify NFR traceability from
       requirements through to design.md §4
```

**Dispatch Auditor #2: Consistency**

```text
Task prompt: contents of references/auditor-consistency.md (Dispatch Prompt section)
Inputs: same artifact paths
Scope: assert artifacts are mutually consistent (ADRs vs requirements, C4 vs
       stack-select, component names, API contracts vs sequence diagrams,
       data models vs schemas, handoff block integrity)
```

**Dispatch Auditor #3: Adversarial**

```text
Task prompt: contents of references/auditor-adversarial.md (Dispatch Prompt section)
Inputs: same artifact paths
Scope: skeptical-CTO lens (failure modes, 10x scale, STRIDE-A security,
       cost model, operability, data governance, vendor lock-in, day-2 ops)
```

All three Task calls run in parallel. The `superpowers:dispatching-parallel-agents` pattern is the canonical way to do this; do not serialize the dispatches.

### Step 2: Wait for All Three to Return

Capture each auditor's full findings list. Each finding has:
- severity: blocker | major | minor | nit
- artifact path
- specific section / line reference
- remediation (one sentence) or question (Auditor #3)

Do not proceed to synthesis until all three auditors have returned their complete output.

### Step 3: Run Synthesis Protocol

Follow `references/synthesis-protocol.md` exactly:

1. **Collect** all raw findings, assign temporary IDs (C-xxx, K-xxx, A-xxx).
2. **Deduplicate**: same artifact + section + root cause across two auditors = merge into one row with both auditor IDs in "Raised by".
3. **Handle conflicts**: contradictory findings from different auditors: keep both, tag with auditor ID, note the conflict; the architect resolves.
4. **Assign ownership**: each finding maps to the skill that produced the artifact (see synthesis-protocol.md §S4).
5. **Sort**: blocker -> major -> minor -> nit; within severity, alphabetical by artifact.
6. **Write summary**: PASSED (zero blockers, zero majors) or FAILED (any blocker or major).
7. **Write output** to `validate/output.md`.

## Output: Validation Report

Write the final report to `validate/output.md` using this exact structure:

```markdown
## Validation Report: Council of Three

### Summary
- Status: [PASSED / FAILED: N blockers, M majors]
- Auditors: Completeness, Consistency, Adversarial
- Artifacts validated: [list]

### Findings (sorted by severity)
| # | Severity | Artifact | Section | Finding | Owner | Raised by |
|---|----------|----------|---------|---------|-------|-----------|
| 1 | blocker  | ...      | ...     | ...     | ...   | ...       |
```

Status is `PASSED` only when blockers = 0 AND majors = 0. A `FAILED` report blocks progression to the next pipeline stage. Minors and nits in a `PASSED` report are tracked in the RAID log.

## Handoff Protocol

```markdown
## Handoff: validate -> [consumer]
### Decisions Made
- Validation complete; Council-of-Three findings synthesized into validate/output.md
- Status: [PASSED / FAILED: N blockers, M majors]
### Artifacts: validate/output.md (Validation Report)
### Open Questions: [any unresolved conflicts flagged for architect]
```

The Validation Report uses a new schema in this version (Severity / Artifact / Section / Finding / Owner / Raised by). The v1 schema (Check / Status / Notes) is retired.

## Sibling Skills

- `/azure-architect`: Azure PaaS/IaaS architecture design
- `/identity-architect`: Identity & access depth (Entra ID, B2C, Managed Identity)
- `/security-architect`: Security depth (Defender, Sentinel, Key Vault, supply chain)
- `/iac-architect`: Infrastructure-as-Code depth (Terraform-first, Bicep secondary)
- `/dotnet-architect`: .NET implementation stack
- `/spec`: Specification and design artifact generation
- `/agent`: Pipeline orchestrator for cross-stack engagements
