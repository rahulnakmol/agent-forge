# ADR 0001: Tier Model

**Status:** Accepted (2026-05-03)
**Spec section:** D1

## Context

Agent CLIs have wildly different plugin ecosystems. Some tools (Claude Code, GitHub
Copilot CLI, Codex CLI, Cursor) have native marketplace registries that index plugins
centrally and allow one-command install. Others (Amp, Gemini CLI) support plugin
installation from a git URL but have no central registry. A third group (Kilo Code,
OpenCode, Crush) has no plugin mechanism at all but reads skill files from a known
filesystem location. Finally, pure LLM interfaces (Perplexity Spaces, ChatGPT custom
GPTs, Claude.ai Projects) have no install mechanism whatsoever — only custom instructions.
A single installation strategy cannot serve all four cases well.

## Decision

Classify all 12 supported CLIs into four tiers based on installation mechanism:

- **Tier 1a — Native registry:** Claude Code, GitHub Copilot CLI, Codex CLI, Cursor. These
  tools have committed marketplace artifacts in the repo and support `plugin install` or
  equivalent native commands.
- **Tier 1b — Git URL install:** Amp, Gemini CLI. These tools install from a GitHub URL,
  cloning the repo to a local skills directory.
- **Tier 2 — File copy:** Kilo Code, OpenCode, Crush. These tools read skills from a known
  directory (`~/.claude/skills/`) that the agent-forge CLI populates by copy.
- **Tier 3 — Prompt loader:** Perplexity Spaces, ChatGPT custom GPTs, Claude.ai Projects.
  No install mechanism; skills are loaded via a generated prompt that instructs the LLM to
  fetch the skill definition from GitHub at invocation time.

## Consequences

**Positive:**
- Each tier gets an optimized installation path matched to the tool's actual capabilities
- New CLIs can be slotted into the correct tier without changing the implementation for other tiers
- Tier 1a CLIs get zero-friction native install; Tier 3 users still get full skill functionality
- Tier boundaries make it easy to communicate to users what level of integration to expect

**Negative:**
- Tier boundaries may shift as CLIs evolve (e.g., a Tier 2 CLI adding native marketplace support)
- Tier 3 is a degraded experience: no tracking, no update detection, no version pinning
- Four different code paths to maintain (though they share common abstractions)

## Alternatives considered

- **Single unified install path** — rejected because one command cannot serve both native
  marketplaces (which require registry commits) and file-copy adapters (which require
  filesystem writes to a known path)
- **Per-CLI bespoke installers** — rejected because the N × M maintenance burden (12 CLIs × 4
  plugins = 48 combinations) is unmanageable; tier abstraction reduces this to 4 × 4 = 16
