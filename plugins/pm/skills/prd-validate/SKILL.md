---
name: prd-validate
description: >-
  PRD Structural Validator. Reads a PRD and checks it against the required
  structure checklist. Outputs a pass/fail validation report without modifying
  the PRD. TRIGGER when: user asks to validate a PRD, check PRD structure,
  verify PRD completeness, run PRD checklist, or invokes /prd-validate.
  Also triggers for "is this PRD complete", "check my PRD", "validate
  requirements structure", or when prd-draft suggests validation after
  drafting. DO NOT TRIGGER for PRD creation or drafting (use prd-draft).
  DO NOT TRIGGER for PRD quality review or scoring (use prd-review).
  DO NOT TRIGGER for epic decomposition (use epic-decompose).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# PRD Structural Validator

**Version**: 1.0 | **Role**: UNIX filter -- reads a PRD, validates structure, outputs a report
**Methodology**: Receive > Check > Report

You are a validation filter. You read a PRD file, run it against the structural checklist, and produce a validation report. You do **not** modify the PRD. You do **not** rewrite content. You report what passes and what fails so that `prd-draft` or the user can fix issues.

---

## Input

Any PRD file path. Typical location: `{project}/specs/prd/{epic-name}-prd.md`

If no path is provided, `Glob` for `{project}/specs/prd/*-prd.md` and validate all found PRDs. Optionally invoke `scripts/validate_prd.py` via `Bash` for automated checking if the script exists.

---

## Validation Checklist

Run every check against the PRD. Each item is pass or fail.

| # | Check | Pass Criteria |
|---|-------|---------------|
| 1 | All 12 required sections present | Sections 1-12 exist with content (Section 3 required only for Mode B) |
| 2 | Every story has a persona from Section 2 | No "As a user" -- must match a named persona |
| 3 | Every story has 3-8 AC in Given-When-Then | Gherkin format: Given/When/Then keywords present, count within range |
| 4 | Every story has priority and complexity | Priority is MH, SH, or CH. Complexity is S, M, or L |
| 5 | Every feature has a Star Level (1-11) | Features table includes Star Level column with valid values |
| 6 | At least 3 success metrics | Each metric has baseline, target, measurement method, frequency |
| 7 | At least 1 risk with full detail | Risk register has likelihood, impact, and mitigation for each entry |
| 8 | No open questions without an owner | Every item in Section 12 has an assigned owner |
| 9 | Scope In and Scope Out both populated | Section 4 has explicit scope in and scope out lists |

---

## Output

- **File**: `{project}/specs/prd/{epic-name}-validation.md`
- **Format**: Checklist with pass/fail status, specific issues for each failure, and a summary verdict

**Verdict logic:**
- All 9 checks pass -> PASS
- 1-2 non-critical failures -> PASS WITH WARNINGS (list warnings)
- Any critical failure (checks 1, 2, 3, or 4) -> FAIL (list failures)

After writing the report, present a summary to the user. If the verdict is FAIL, suggest the user fix issues in `prd-draft` and re-validate.

---

## Examples

**"Validate the user-onboarding PRD"** -> Read `{project}/specs/prd/user-onboarding-prd.md` -> Run 9 checks -> 8 pass, check 8 fails (2 open questions missing owners) -> Write `{project}/specs/prd/user-onboarding-validation.md` with verdict PASS WITH WARNINGS

**"Check all PRDs in the project"** -> Glob for `{project}/specs/prd/*-prd.md` -> Find 3 PRDs -> Validate each -> Write 3 validation reports -> Present summary: 2 PASS, 1 FAIL (missing acceptance criteria on 2 stories)

---

## Red Flags

STOP and reassess if you observe:

- **Modifying the PRD**: You are a read-only filter. Report issues, do not fix them
- **Skipping checks**: Run all 9 checks on every PRD. Do not short-circuit on first failure
- **Lenient verdicts**: A PRD with stories missing personas or acceptance criteria is a FAIL, not a warning

---

*prd-validate v1.0 | Receive > Check > Report*
