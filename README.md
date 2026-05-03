# Superpowers branch

This branch holds design specs and implementation plans for agent-forge.

It is intentionally NOT merged into `main` — `main` ships only deployable artifacts and user-facing docs.

Layout:
- `docs/superpowers/specs/`  — design specs (output of brainstorming)
- `docs/superpowers/plans/`  — implementation plans (output of writing-plans)

CI on `main` rejects any PR whose diff touches `docs/superpowers/**`.

