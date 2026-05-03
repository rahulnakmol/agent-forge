# ADR 0006: Layered Test Harness A/B/C

**Status:** Accepted (2026-05-03)
**Spec section:** D6

## Context

Plugin quality must be verified across three dimensions that have fundamentally different
cost and capability profiles. Structural quality (does the SKILL.md have valid frontmatter?
are all artifacts in sync?) can be verified with pure Python in milliseconds and no
external dependencies. Semantic output quality (does the humanize skill actually produce
human-sounding prose?) requires an LLM call to evaluate and costs money. Install lifecycle
quality (does `agent-forge install writing --tier kilocode` correctly place files?) requires
a realistic Docker environment and takes minutes. A single test layer cannot serve all
three dimensions without either being prohibitively slow/expensive or missing real failures.

## Decision

Three test layers, each with different triggers, cost profiles, and capability:

- **Layer A — Structural (pure Python, no LLM):** `pytest tests/unit`. Checks frontmatter
  validity, schema conformance, artifact sync, reference link resolution, and boundary
  guards. Runs in under 10 seconds on any machine. Required to pass on every PR.

- **Layer B — Semantic evals (LLM-judged rubric):** `pytest tests/evals`. Runs each skill
  against its `inputs.json` and scores outputs against `rubric.md` using an LLM judge.
  Requires `ANTHROPIC_API_KEY`. Maintains score baselines; fails if score regresses.
  Triggered on PRs via CI secret.

- **Layer C — Docker integration (install lifecycle):** `pytest tests/integration`. Builds
  a Docker image for each Tier 2 target, runs `agent-forge install`, and verifies that
  the target CLI sees the installed skills. Triggered on release tags only.

## Consequences

**Positive:**
- Layer A runs on every PR: fast, cheap, catches structural regressions immediately
- Layer B catches skill quality regression: a rewrite that scores 0.6 on the rubric
  fails before merge, not after users complain
- Layer C catches install failures before a tag is published to PyPI
- Contributors without an API key can still run Layer A locally

**Negative:**
- Layer B requires an Anthropic API key; most contributors only run Layer A locally
  and rely on CI for Layer B verification
- Layer C requires Docker; not all maintainers have Docker available in their CI quota
- Maintaining three test configurations adds cognitive overhead to the test infrastructure

## Alternatives considered

- **Only structural tests (Layer A only)** — rejected because structural validity says
  nothing about whether the skill actually produces good output; a perfectly valid
  SKILL.md could still produce unhelpful responses
- **LLM evals for everything (Layer B for structural too)** — rejected because it is
  too slow (minutes) and too expensive (API cost) to run on every PR; structural checks
  are deterministic and should be free
