# ADR 0007: Four Native Marketplaces

**Status:** Accepted (2026-05-03)
**Spec section:** D7

## Context

Several agent CLIs have native plugin or marketplace concepts that allow users to
install plugins with a single command: Claude Code, GitHub Copilot CLI, Codex CLI,
and Cursor. These native mechanisms require the plugin to be registered in a
marketplace registry and to have committed, tool-specific manifest files present in
the repository. Without these committed artifacts, native `plugin install` commands
cannot discover or install agent-forge plugins. The alternative — requiring users to
use the agent-forge CLI for these tools — abandons the primary value proposition
of native marketplace integration.

## Decision

Maintain committed Tier 1a artifacts in the repository so native marketplace
registrations work without a separate install step. Four artifact directories are
maintained:

- `.claude-plugin/` — Claude Code marketplace manifest
- `.github/plugin/` — GitHub Copilot CLI plugin manifest
- `.codex-plugin/` — OpenAI Codex CLI plugin manifest
- `.cursor-plugin/` — Cursor marketplace manifest

These files are generated from the canonical `plugins/` source by
`scripts/regenerate-tier1-artifacts.py` and must be committed and kept in sync.
CI enforces sync via `tests/unit/test_tier1_artifacts_sync.py`.

## Consequences

**Positive:**
- Zero-friction install for the most popular CLIs: one command, no additional tools required
- Integrates with each tool's existing update mechanism (e.g., `claude plugin update --all`)
- Marketplace search and discovery works natively for Claude Code and Cursor
- Contributors to the repo get agent-forge skills automatically if they use these CLIs

**Negative:**
- Generated files must be kept in sync with the canonical source — enforced by CI, but
  contributors must remember to run `python scripts/regenerate-tier1-artifacts.py` before
  committing plugin changes
- Repository size increases as the number of plugins and skills grows (each skill has
  multiple format-specific representations)
- Four different manifest formats to maintain (one per Tier 1a tool)

## Alternatives considered

- **Dynamic generation at install time** — rejected because it requires a network call and
  the agent-forge CLI to be installed; breaks offline install and makes native `plugin install`
  commands unusable without a separate prerequisite
- **No native marketplace support** — rejected because it abandons the primary use case for
  Tier 1a CLIs; users of Claude Code and Cursor expect to use native commands
