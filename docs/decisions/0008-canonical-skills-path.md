# ADR 0008: Canonical Authoring at plugins/<name>/skills/

**Status:** Accepted (2026-05-03)
**Spec section:** D8

## Context

agent-forge supports 12 install targets, each with a different skill format. A skill
authored natively for Claude Code uses YAML frontmatter SKILL.md; a skill for Codex CLI
uses TOML agents; a skill for Gemini CLI uses its own schema. If authors had to write a
separate file for each target, one skill would require 12 files per skill, and any update
to the skill content would need to be applied in 12 places — a divergence risk that grows
with the number of contributors. Claude Code's SKILL.md format is the richest available:
it supports frontmatter-based routing, progressive disclosure via subdirectories, tool
permission declarations, and references. It is the natural authoring surface.

## Decision

Authors write skills once in Claude Code SKILL.md format at
`plugins/<name>/skills/<skill-name>/SKILL.md`. Translators in
`tests/unit/translators/` generate all other CLI formats from this canonical source.
The `scripts/regenerate-tier1-artifacts.py` script runs all translators and writes
the output to the appropriate artifact directories. No author ever touches the generated
files directly.

The translator contract:
- Input: a `SKILL.md` file with valid frontmatter
- Output: one or more format-specific files written to the target artifact directory
- Idempotent: running the translator twice produces identical output

## Consequences

**Positive:**
- Single source of truth: updating a skill in `plugins/<name>/skills/` propagates to
  all 12 install targets via translators
- New CLIs get full coverage by adding one translator — no author action required
- Authors don't need to know any format except Claude Code SKILL.md
- Diff reviews are clean: the canonical change is in one file; generated changes are
  automatically produced and committed together

**Negative:**
- Translator quality determines output quality for non-Claude Code CLIs: if a translator
  has a bug, all skills for that target have the same bug
- Some CLIs lose features that don't map from SKILL.md: for example, Claude Code's
  `allowed-tools` has no equivalent in some Tier 2 targets, so tool restrictions are
  silently dropped in translation
- Authors cannot fine-tune per-CLI output without modifying the translator, which
  requires understanding the translation layer

## Alternatives considered

- **Author per-CLI format natively** — rejected because N files per skill (where N = 12)
  creates immediate divergence risk; in practice, authors update the canonical file and
  forget to update the other 11
- **Common reduced format** — rejected because reducing to the lowest common denominator
  across all 12 CLIs would strip Claude Code's rich routing, progressive disclosure, and
  tool permission features — the features that make the skills work well in Claude Code
