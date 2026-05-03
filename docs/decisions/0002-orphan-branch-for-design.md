# ADR 0002: Orphan Branch for Design Artifacts

**Status:** Accepted (2026-05-03)
**Spec section:** D2

## Context

Design specifications, phase plans, kickoff guides, and architecture decision records
are produced during the design phase of the project and are large artifacts (often
tens of thousands of words) that change on a fundamentally different cadence than the
codebase. They are valuable references during development but are not part of the
installed product. Including them on `main` creates several problems: they inflate the
package size (relevant for PyPI distributions), they muddy the commit history of
functional code changes, and they create confusion about what is "the product" versus
"the design of the product."

## Decision

Store all design artifacts on an orphan `superpowers` branch that never merges to `main`.

The `superpowers` branch has no common ancestor with `main`. It contains only design
documents: phase plans, kickoff specs, ADR drafts, and other planning artifacts.
Contributors reference it via `git fetch origin superpowers` or by browsing the branch
on GitHub. The branch is never merged and its commits are never cherry-picked to `main`.

## Consequences

**Positive:**
- `main` stays clean: only functional code, skills, and user-facing docs
- Design can evolve independently without polluting the code history
- No risk of design artifacts being accidentally bundled into a PyPI release
- CI workflows on `main` do not need to account for or exclude design files

**Negative:**
- Design history is separate from code history; cross-referencing requires switching branches
- New contributors need to know about two branches to get the full picture
- Orphan branch is an unusual Git pattern that some contributors may not be familiar with

## Alternatives considered

- **`docs/design/` subdirectory on `main`** — rejected because design files would be
  included in the PyPI package, pollute install artifacts, and mix with user-facing docs
  that belong on `main`
- **Separate repository (e.g., `agent-forge-design`)** — rejected because it introduces
  too much coordination overhead for a solo maintainer and makes it hard to link design
  decisions to specific code commits
