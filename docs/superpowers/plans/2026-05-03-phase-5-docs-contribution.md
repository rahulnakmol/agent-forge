# Phase 5 — Documentation + Contribution Infrastructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship complete user-facing documentation, contributor guides, decision records, and the auto-generation tooling (third-party notices aggregator + install index) so the v1.0.0 release is publishable and contributable from day one.

**Architecture:** Two doc trees — `docs/install/` (12 install guides, one per target tool, agent-installable) and `docs/contributing/` (3 deep guides for plugin authors). Decision records under `docs/decisions/` capture every locked architectural call as a one-page ADR. Auto-generators (`scripts/aggregate-notices.py`, `scripts/build-install-index.py`) run on push to main and fail CI if their outputs drift from canonical sources. Top-level `README.md` is rewritten from scratch.

**Tech Stack:** Pure Markdown for guides; Python for generators (uses `agent_forge.canonical` from Phase 2).

**Spec reference:** Section 7 (Contribution Model), Section 5 (CLI surface — referenced in install guides).

**Depends on:** Phases 0–4 complete.

---

## Parallelization map

After Task 1 (write the install-guide template that all 12 follow), the install guides and contributor docs are fully independent:

- **Group A** (12 install guides): Tasks 2–13 — one per target tool, parallel
- **Group B** (3 contributor docs): Tasks 14–16 — parallel
- **Group C** (decision records): Tasks 17–24 — one ADR per major decision, parallel
- **Group D** (auto-generators): Tasks 25–26 — parallel
- **Group E** (top-level files): Tasks 27 (README), 28 (rewritten CONTRIBUTING.md) — parallel

Recommended: 12 parallel subagents for Group A, 3 for B, 8 for C, 2 for D, 2 for E.

---

## Task 1: Write the install-guide template

**Files:**
- Create: `docs/install/_template.md`

- [ ] **Step 1: Write the canonical template that every per-tool guide follows**

```markdown
# Installing agent-forge plugins for <TOOL NAME>

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/docs/install/<filename>.md`

## Prerequisites

- <TOOL NAME> installed (`<install command for the tool itself>`)
- Optional: `agent-forge` Python CLI (`pipx install agent-forge`) for unified update tracking

## Quick install

### Option A: Native install command (recommended)

```bash
<TOOL NAME>'s native command for adding the agent-forge marketplace
```

### Option B: Via the agent-forge CLI

```bash
pipx install agent-forge
agent-forge install <plugin> --tier <tool-name>
```

## Verify

```bash
<command to list installed plugins/skills in the tool>
```
Expected: agent-forge plugins listed.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | <path> | Loaded on demand via frontmatter routing |
| Agents | <path> | <how this tool exposes agents> |
| Commands | <path> | <how this tool exposes slash commands> |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
<tool's native update command, if any>
```

## Removing

```bash
agent-forge remove <plugin>@<tool-name>
```

## Troubleshooting

**Plugin not appearing after install:**
1. <Diagnostic step 1>
2. <Diagnostic step 2>

**See also:** [Loader pattern explainer](/docs/install/_loader-pattern.md), [Contributing](/docs/contributing/adding-a-plugin.md)
```

---

## Tasks 2–13: Per-tool install guides (PARALLEL)

For each of the 12 install targets, fill in the template:

| Task | Tool | Tier | File |
|---|---|---|---|
| 2 | Claude Code | 1a | `docs/install/claude-code.md` |
| 3 | GitHub Copilot CLI | 1a | `docs/install/github-copilot-cli.md` |
| 4 | Codex CLI | 1a | `docs/install/codex-cli.md` |
| 5 | Cursor | 1a | `docs/install/cursor.md` |
| 6 | Amp | 1b | `docs/install/amp.md` |
| 7 | Gemini CLI | 1b | `docs/install/gemini-cli.md` |
| 8 | Kilo Code | 2 | `docs/install/kilocode.md` |
| 9 | OpenCode | 2 | `docs/install/opencode.md` |
| 10 | Crush | 2 | `docs/install/crush.md` |
| 11 | Perplexity | 3 | `docs/install/perplexity.md` |
| 12 | ChatGPT custom GPTs | 3 | `docs/install/chatgpt-gpts.md` |
| 13 | Claude.ai Projects | 3 | `docs/install/claude-projects.md` |

### Per-task template (each subagent runs this for its tool)

- [ ] **Step 1: Copy the template** (`cp docs/install/_template.md docs/install/<tool>.md`)
- [ ] **Step 2: Fill in tool-specific install command** (use the verified commands from spec Section 4)
- [ ] **Step 3: Fill in target paths from `target_paths()` in the tool's translator** (Phase 2 implementations are the source of truth)
- [ ] **Step 4: Fill in troubleshooting** based on Phase 4 integration test failures (most common issues)
- [ ] **Step 5: Verify the doc is agent-readable** — paste into a Claude or Copilot session, ask it to "follow this guide and install agent-forge for <tool>"
- [ ] **Step 6: Commit**

**Specific tool examples:**

For `claude-code.md` (Task 2), the Quick Install section becomes:

```bash
claude plugin marketplace add github:rahulnakmol/agent-forge
claude plugin install writing
```

For `amp.md` (Task 6):

```bash
amp skill add github:rahulnakmol/agent-forge
```

For `perplexity.md` (Task 11), Quick Install becomes:

```bash
agent-forge install writing/humanize --tier prompt-loader > humanize-loader.md
# Open Perplexity Spaces → Create new Space → Paste contents of humanize-loader.md
# into the "Custom Instructions" field
```

(Tier 3 tools never have a CLI command; the loader output is what the user pastes.)

---

## Tasks 14–16: Contributor docs (PARALLEL)

### Task 14: `docs/contributing/adding-a-plugin.md`

The 7-step canonical flow from spec Section 7. Verbatim copy-paste-able commands; no placeholders.

### Task 15: `docs/contributing/skill-authoring-guide.md`

Cover: SKILL.md frontmatter spec, progressive disclosure pattern (`references/`, `scripts/`, `assets/`), naming conventions, eval requirements, the agentskills.io reference. Include 3 worked examples (one prose-only skill, one with scripts, one with assets).

### Task 16: `docs/contributing/testing-locally.md`

Cover: how to run Layer A locally, how to run a single eval, how to update baselines, how to run Layer C in Docker locally before pushing. Include the exact commands from Phase 4 Tasks 1–3.

---

## Tasks 17–24: Decision records (PARALLEL)

Eight ADRs, one per major architectural decision (D1–D16 from spec Section 2). Each is one page (under 500 words):
- Context (one paragraph)
- Decision (the call we made)
- Consequences (positive + negative)
- Alternatives considered

| Task | ADR | File |
|---|---|---|
| 17 | Tier model | `docs/decisions/0001-tier-model.md` |
| 18 | Orphan branch for design artifacts | `docs/decisions/0002-orphan-branch-for-design.md` |
| 19 | SHA-based versioning + optional tags | `docs/decisions/0003-sha-based-versioning.md` |
| 20 | Local manifest as state-of-truth | `docs/decisions/0004-local-manifest.md` |
| 21 | DCO over CLA | `docs/decisions/0005-dco-not-cla.md` |
| 22 | Test harness layered (A/B/C) | `docs/decisions/0006-layered-test-harness.md` |
| 23 | Native marketplaces for 4 CLIs (D13) | `docs/decisions/0007-four-native-marketplaces.md` |
| 24 | Canonical authoring at plugins/<name>/skills/ (D16) | `docs/decisions/0008-canonical-skills-path.md` |

Each follows this skeleton:

```markdown
# ADR <NNN>: <Title>

**Status:** Accepted (2026-05-03)
**Spec section:** D<N>

## Context

<One paragraph: why this decision needed to be made.>

## Decision

<The call we made, stated as a single sentence + supporting bullets.>

## Consequences

**Positive:**
- <bullet>
- <bullet>

**Negative:**
- <bullet>
- <bullet>

## Alternatives considered

- **<Alternative 1>** — rejected because <reason>
- **<Alternative 2>** — rejected because <reason>
```

---

## Task 25: Build `scripts/aggregate-notices.py` (PARALLEL with Task 26)

**Files:**
- Create: `scripts/aggregate-notices.py`
- Create: `THIRD_PARTY_NOTICES.md` (generated)
- Create: `tests/unit/test_aggregate_notices.py`

- [ ] **Step 1: Test**

```python
"""tests/unit/test_aggregate_notices.py"""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def test_third_party_notices_in_sync() -> None:
    result = subprocess.run(
        ["python", "scripts/aggregate-notices.py", "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"THIRD_PARTY_NOTICES.md drifted:\n{result.stdout}"
```

- [ ] **Step 2: Implement `scripts/aggregate-notices.py`**

```python
"""Aggregate per-plugin THIRD_PARTY_NOTICES.md files into the top-level one.

Usage:
  python scripts/aggregate-notices.py            # rewrite the file
  python scripts/aggregate-notices.py --check    # exit 1 if drift detected
"""

import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOP_LEVEL = REPO / "THIRD_PARTY_NOTICES.md"

HEADER = """# Third-Party Notices

This file aggregates per-plugin third-party attributions into one place.
Generated automatically by `scripts/aggregate-notices.py` — do not edit by hand.

## Repository license

The agent-forge project is licensed under BSD-3-Clause (see `LICENSE`).

---

"""


def build() -> str:
    body = HEADER
    for plugin_notices in sorted((REPO / "plugins").glob("*/THIRD_PARTY_NOTICES.md")):
        plugin = plugin_notices.parent.name
        body += f"## Plugin: {plugin}\n\n"
        body += plugin_notices.read_text() + "\n\n---\n\n"
    return body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        actual = TOP_LEVEL.read_text() if TOP_LEVEL.exists() else ""
        if actual != expected:
            print("THIRD_PARTY_NOTICES.md drifted from per-plugin sources")
            raise SystemExit(1)
    else:
        TOP_LEVEL.write_text(expected)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run + commit generated file**

```bash
python scripts/aggregate-notices.py
pytest tests/unit/test_aggregate_notices.py -v
```

- [ ] **Step 4: Wire into `.github/workflows/ci-structural.yml`**

Add a step:

```yaml
      - name: THIRD_PARTY_NOTICES.md in sync
        run: python scripts/aggregate-notices.py --check
```

---

## Task 26: Build `scripts/build-install-index.py` (PARALLEL with Task 25)

**Files:**
- Create: `scripts/build-install-index.py`
- Create: `docs/install/_index.md` (generated)
- Create: `tests/unit/test_install_index.py`

- [ ] **Step 1: Test**

```python
"""tests/unit/test_install_index.py"""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def test_install_index_in_sync() -> None:
    result = subprocess.run(
        ["python", "scripts/build-install-index.py", "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout
```

- [ ] **Step 2: Implement**

```python
"""Generate docs/install/_index.md — catalog of all plugins × all install targets.

Usage:
  python scripts/build-install-index.py [--check]
"""

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "docs/install/_index.md"

INSTALL_TARGETS = [
    ("Claude Code", "claude-code", "1a"),
    ("GitHub Copilot CLI", "github-copilot-cli", "1a"),
    ("Codex CLI", "codex-cli", "1a"),
    ("Cursor", "cursor", "1a"),
    ("Amp", "amp", "1b"),
    ("Gemini CLI", "gemini-cli", "1b"),
    ("Kilo Code", "kilocode", "2"),
    ("OpenCode", "opencode", "2"),
    ("Crush", "crush", "2"),
    ("Perplexity Spaces", "perplexity", "3"),
    ("ChatGPT custom GPTs", "chatgpt-gpts", "3"),
    ("Claude.ai Projects", "claude-projects", "3"),
]


def build() -> str:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = canonical["plugins"]
    out = ["# agent-forge install catalog\n"]
    out.append("> Paste this URL into any LLM agent to install:\n")
    out.append("> `https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/docs/install/<tool>.md`\n\n")
    out.append("## Install targets (12 at v1.0)\n\n")
    out.append("| Tool | Tier | Install guide |\n")
    out.append("|---|---|---|\n")
    for name, slug, tier in INSTALL_TARGETS:
        out.append(f"| {name} | {tier} | [{slug}.md](./{slug}.md) |\n")
    out.append("\n## Plugins (4 at v1.0)\n\n")
    for p in plugins:
        out.append(f"### {p['name']}\n\n{p['description']}\n\n")
        out.append("Install for Claude Code:\n```bash\nclaude plugin install " + p['name'] + "\n```\n\n")
        out.append(f"Install for any other tool — see the [per-tool guide]({INSTALL_TARGETS[0][1]}.md).\n\n")
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        actual = INDEX.read_text() if INDEX.exists() else ""
        if actual != expected:
            print("docs/install/_index.md drifted from canonical sources")
            raise SystemExit(1)
    else:
        INDEX.write_text(expected)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run + commit**

```bash
python scripts/build-install-index.py
pytest tests/unit/test_install_index.py -v
```

---

## Task 27: Rewrite `README.md` (PARALLEL)

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Write the README** (under 200 lines; concrete examples; multi-CLI pitch)

```markdown
# agent-forge

A curated, BSD-3-Clause marketplace of agent skills, plugins, and slash commands.
Works natively with Claude Code, GitHub Copilot CLI, OpenAI Codex CLI, Cursor,
Sourcegraph Amp, and Google Gemini CLI. Adapters for Kilo Code, OpenCode, and
Crush. Portable loader for Perplexity, ChatGPT GPTs, and Claude.ai Projects.

**12 install targets. 4 plugins. ~150 skills. One canonical source.**

## 30-second install

For Claude Code:
```bash
claude plugin marketplace add github:rahulnakmol/agent-forge
claude plugin install writing
```

For GitHub Copilot CLI:
```bash
copilot plugin marketplace add rahulnakmol/agent-forge
```

For Codex CLI:
```bash
codex plugin marketplace add rahulnakmol/agent-forge
```

For Cursor: open `cursor.com/marketplace`, search "agent-forge", click install.

For Amp:
```bash
amp skill add github:rahulnakmol/agent-forge
```

For Gemini CLI:
```bash
gemini skills install github:rahulnakmol/agent-forge
```

For Kilo Code, OpenCode, Crush, or any other tool — install the unified CLI:
```bash
pipx install agent-forge
agent-forge install writing --tier <your-cli>
```

For Perplexity, ChatGPT GPTs, or Claude.ai Projects — see [docs/install/_index.md](./docs/install/_index.md).

## What's in the marketplace

| Plugin | Skills | Description |
|---|---|---|
| `writing` | humanize | Writing transformation: detect AI patterns, calibrate voice, humanize text |
| `prompts` | prompt-forge | Interactive prompt engineering — guides users through structured dialogue |
| `msft-arch` | ~25 skills | Microsoft enterprise architecture: Azure, M365, Power Platform, Dynamics 365 |
| `pm` | 12 skills | Product/Program Management: PRD generation, TOM design, 11-Star quality review |

## Telling an agent to install

Paste this into any LLM agent:

> Install agent-forge plugins from
> https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/docs/install/_index.md

The agent will fetch the catalog, ask which tool you're using, and run the right install command.

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Three flows: typo fix, new skill, new plugin. DCO sign-off required (`git commit -s`).

## License

BSD-3-Clause. Per-plugin assets may carry their own licenses — see `THIRD_PARTY_NOTICES.md`.
```

---

## Task 28: Rewrite `CONTRIBUTING.md` (PARALLEL with Task 27)

Replace the Phase 0 stub with the full contributor overview that funnels to `docs/contributing/`. Cover: forking flow, DCO requirement, PR templates, eval requirements, license attestation. Reference the deeper guides without duplicating their content.

---

## Final task: Smoke + commit Phase 5

- [ ] **Step 1: Verify all 12 install guides exist + render**

```bash
for f in docs/install/*.md; do echo "$f:"; head -5 "$f"; done
```

- [ ] **Step 2: Verify all 8 ADRs exist**

```bash
ls docs/decisions/*.md | wc -l    # should be 8+
```

- [ ] **Step 3: Run all sync invariant tests**

```bash
pytest tests/unit/test_aggregate_notices.py tests/unit/test_install_index.py tests/unit/test_tier1_artifacts_sync.py -v
```

- [ ] **Step 4: Commit**

```bash
git add docs/install/ docs/contributing/ docs/decisions/ scripts/aggregate-notices.py scripts/build-install-index.py THIRD_PARTY_NOTICES.md README.md CONTRIBUTING.md tests/unit/test_aggregate_notices.py tests/unit/test_install_index.py .github/workflows/ci-structural.yml
git commit -s -m "Phase 5: complete user + contributor documentation

Install guides (12, one per target tool):
- Tier 1a: claude-code, github-copilot-cli, codex-cli, cursor
- Tier 1b: amp, gemini-cli
- Tier 2:  kilocode, opencode, crush
- Tier 3:  perplexity, chatgpt-gpts, claude-projects

Each guide is agent-installable: paste its raw URL into an LLM and the LLM
follows the steps directly.

Contributor docs:
- adding-a-plugin.md (7-step canonical flow)
- skill-authoring-guide.md (frontmatter spec + 3 worked examples)
- testing-locally.md (Layer A/B/C local commands)

Decision records (8 ADRs, one per major architectural call):
- 0001 tier model
- 0002 orphan branch for design
- 0003 SHA-based versioning
- 0004 local manifest
- 0005 DCO not CLA
- 0006 layered test harness
- 0007 four native marketplaces
- 0008 canonical skills path

Auto-generators (CI-checked for drift):
- scripts/aggregate-notices.py → THIRD_PARTY_NOTICES.md
- scripts/build-install-index.py → docs/install/_index.md

Top-level rewrites:
- README.md (12-target install matrix; 30-second per-CLI examples)
- CONTRIBUTING.md (full version; funnels to docs/contributing/)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Self-Review

- [ ] All 12 install guides present ✓
- [ ] All 3 contributor docs present ✓
- [ ] Per spec Section 7, ADR for every D-numbered decision ✓
- [ ] Aggregator + index generator both have CI sync invariants ✓

**Done criteria:** every `docs/install/*.md` and `docs/contributing/*.md` exists and is ≥30 lines; all sync invariants pass; README + CONTRIBUTING reflect the v1.0 12-target story.
