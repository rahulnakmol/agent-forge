# tests/_legacy

Reference-only files migrated from the original `rahulnakmol/agent-marketplace` repo.
**These are NOT executed by the test runner.** They exist for one purpose: to
review for reusable patterns before the v1.0.0 tag, then be deleted.

## Files

- `kpmg_harness_reference.py` — the original test harness that lived inside the
  KPMG plugin in the source repo. Reviewed in Phase 4 of the v1.0 plan; deleted
  in Phase 7 (pre-release hardening) once any reusable patterns are ported into
  `tests/unit/` or `tests/evals/`.

## Why "_legacy" not deleted immediately

The original harness encoded brand-compliance checks specific to KPMG. It also
contained generic patterns (PowerPoint validation, font checking, slide
matching) that may inform agent-forge's own test design. Don't lose them by
deleting too early.

## Deletion gate

This directory MUST be empty before tagging v1.0.0. CI invariant in Phase 7
adds a check.
