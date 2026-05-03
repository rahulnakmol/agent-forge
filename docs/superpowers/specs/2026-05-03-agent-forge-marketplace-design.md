---
title: agent-forge — Multi-CLI Plugin Marketplace
date: 2026-05-03
status: approved
target_release: v1.0.0
authors:
  - Rahul N Akmol (@rahulnakmol)
brainstorming_session: 2026-05-03
---

# agent-forge — Multi-CLI Plugin Marketplace

## 1. Context and Goals

`agent-forge` is a public BSD-3-Clause marketplace of agent skills, plugins, and slash commands. It is intended to serve as the canonical home for the author's published agent content and to accept community contributions over time.

The marketplace ships natively for Claude Code and GitHub Copilot CLI, ships with adapter installers for Kilo Code, OpenCode, Codex, and Cursor, and ships with a portable loader pattern for prompt-only tools (Perplexity Spaces, ChatGPT custom GPTs, Claude.ai Projects).

**Source of content:** the existing private repository `rahulnakmol/agent-marketplace`, with the proprietary `kpmg` plugin excluded.

**Primary use cases:**
- A user (or an LLM agent acting on a user's behalf) can install a plugin/skill into any supported CLI with one command or one paste-able URL.
- Updates to skills propagate to every install regardless of which CLI hosts it, via a local manifest.
- The same content is authored once (in Claude Code's plugin format) and reaches all targets.
- An internal test harness validates structural correctness and behavioural quality before any release.

### Goals

1. **One canonical source.** `plugins/<name>/` is the single source of truth, authored in Claude Code format. Translators read from it; nothing mutates it.
2. **Tiered support honesty.** Each CLI's level of support (native / adapter / loader) is named explicitly. Users know what they are getting.
3. **Agent-installable.** An LLM agent can install any item by following a single canonical URL pattern: `https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/docs/install/<plugin-or-skill>.md`.
4. **Update propagation across all tiers.** A local manifest tracks every install; one command (`agent-forge update`) refreshes them all.
5. **High quality bar from day one.** Structural validation on every PR, behavioural evals on plugin-touching PRs, integration tests on release branches.
6. **Stable v1.0.0 release.** Schemas (`marketplace.json`, `~/.agent-forge/manifest.json`), CLI surface, and install-URL pattern become public APIs at tag time.

### Non-goals

- A web UI or hosted catalog service. The repo + GitHub UI is the catalog.
- Real-time skill execution as a service. Skills are content, not infrastructure.
- A custom plugin format that diverges from Claude Code's. We adopt Claude Code's format as canonical.
- Support for every conceivable AI tool. Aider and Amp are explicitly deferred to v1.1 due to less mature plugin models.

## 2. Architectural Decisions (TL;DR)

| # | Decision | Rationale |
|---|---|---|
| D1 | Author canonical content in Claude Code format under `plugins/<name>/` | Matches existing reference repo; primary CLI; richest format. |
| D2 | Tier model: 1 (native) / 2 (adapter) / 3a (filesystem loader) / 3b (prompt loader) | Honest grouping by mechanism; sets user expectations. |
| D3 | Distribution: bash one-liners + optional `agent-forge` Python CLI (pipx) | Zero-build for agent-install path; clean UX for humans. Python matches existing scripts. |
| D4 | Versioning: SHA-based with optional semver tags | Truthful by construction; tags layered for stable channels. |
| D5 | Local manifest (`~/.agent-forge/manifest.json`) drives update propagation | Single source of state; replays operation log on corruption. |
| D6 | Test harness layered: A (structural, every PR) + B (behavioural evals, plugin PRs) + C (integration, release branches) | Cost-proportional; quality bar appropriate to risk. |
| D7 | Test harness lives at `tests/` outside `plugins/`; CI guard prevents leakage | Boundary enforced by tests, not convention. |
| D8 | Design specs + implementation plans live on orphan branch `superpowers`; never merged to `main` | Keeps `main` clean; preserves design history; CI guard rejects accidental merges. |
| D9 | KPMG plugin and all proprietary content excluded; verified by `test_no_kpmg_residue.py` | Public repo cannot contain proprietary brand assets. |
| D10 | DCO over CLA | Lighter-weight contributor friction; sufficient for BSD. |
| D11 | v1.0.0 ships 6 CLI adapters + 3 prompt-tool loaders; Aider/Amp deferred to v1.1 | Plugin formats for Aider/Amp not stable enough for a v1.0 commitment. |
| D12 | Public schemas (`marketplace.json`, `manifest.json`, CLI surface, install-URL pattern) frozen at v1.0.0 | After v1.0, breaking changes require v2.0.0. |

## 3. Repository Layout

```
agent-forge/
├── .claude-plugin/
│   └── marketplace.json                    Tier 1: Claude Code marketplace manifest
├── .github/
│   ├── prompts/                            Tier 1: Copilot CLI slash commands (translator-generated, committed)
│   ├── copilot-instructions.md             Tier 1: Copilot CLI global instructions (translator-generated, committed)
│   ├── CODEOWNERS
│   ├── PULL_REQUEST_TEMPLATE/
│   │   ├── plugin.md
│   │   ├── skill.md
│   │   └── default.md
│   └── workflows/
│       ├── ci-structural.yml               Layer A — every PR
│       ├── ci-evals.yml                    Layer B — PRs touching plugins/ or tests/evals/
│       ├── ci-integration.yml              Layer C — release/* branches and tag pushes
│       ├── ci-evals-nightly.yml            Full Layer B sweep, scheduled nightly
│       └── release.yml                     Tag push → PyPI publish + GitHub Release
│
├── plugins/                                Canonical source of truth (Claude Code format)
│   ├── writing/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   ├── skills/<name>/
│   │   │   ├── SKILL.md                    Frontmatter + body
│   │   │   ├── references/                 Loaded only when SKILL.md instructs
│   │   │   ├── scripts/
│   │   │   └── assets/
│   │   ├── agents/
│   │   └── commands/
│   ├── prompts/
│   ├── msft-arch/
│   └── pm/
│
├── scripts/                                Installers and CLI library code (not shipped via marketplace)
│   ├── agent_forge/                        The Python CLI package — `pipx install agent-forge`
│   │   ├── __init__.py
│   │   ├── cli.py                          Entry point: install/update/list/etc.
│   │   ├── manifest.py                     Read/write ~/.agent-forge/manifest.json
│   │   ├── detectors.py                    Identify which CLIs are present
│   │   ├── github.py                       Tarball fetch + SHA resolution
│   │   ├── translators/
│   │   │   ├── __init__.py
│   │   │   ├── _base.py                    Translator Protocol + helpers
│   │   │   ├── claude_code.py              Tier 1
│   │   │   ├── copilot_cli.py              Tier 1
│   │   │   ├── kilocode.py                 Tier 2
│   │   │   ├── opencode.py                 Tier 2
│   │   │   ├── codex.py                    Tier 3a
│   │   │   ├── cursor.py                   Tier 3a
│   │   │   └── prompt_loader.py            Tier 3b — generates loader for Perplexity/GPTs/Projects
│   │   └── pyproject.toml
│   ├── install-claude-code.sh              Bash one-liner shims that delegate to the CLI
│   ├── install-copilot-cli.sh
│   ├── install-kilocode.sh
│   ├── install-opencode.sh
│   ├── install-codex.sh
│   ├── install-cursor.sh
│   ├── pack-skill-loader.py                Tier 3b: emit loader text for a single skill
│   ├── aggregate-notices.py                Build top-level THIRD_PARTY_NOTICES.md
│   └── build-install-index.py              Generate docs/install/_index.md
│
├── tests/                                  INTERNAL ONLY — never shipped to users
│   ├── pyproject.toml                      Test-only deps (pytest, anthropic, jsonschema)
│   ├── pytest.ini
│   ├── conftest.py                         Shared fixtures (plugin discovery, tmp HOME)
│   ├── unit/                               Layer A
│   │   ├── test_marketplace_schema.py
│   │   ├── test_plugin_json_schema.py
│   │   ├── test_skill_md_frontmatter.py
│   │   ├── test_skill_md_size.py
│   │   ├── test_reference_links_resolve.py
│   │   ├── test_install_scripts_dry_run.py
│   │   ├── test_translator_protocol.py
│   │   ├── test_no_test_paths_in_installers.py    BOUNDARY GUARD
│   │   └── test_no_kpmg_residue.py
│   ├── evals/                              Layer B — per-skill rubric-judged behaviour
│   │   ├── conftest.py
│   │   ├── _judge.py                       Shared rubric scorer (Haiku 4.5 default)
│   │   ├── _baseline_scores.json           Committed regression baselines
│   │   ├── writing/humanize/
│   │   ├── prompts/prompt_forge/
│   │   ├── msft-arch/<skill>/
│   │   └── pm/<skill>/
│   ├── integration/                        Layer C — real CLI binaries in Docker
│   │   ├── test_install_lifecycle_claude.py
│   │   ├── test_install_lifecycle_copilot.py
│   │   ├── test_install_lifecycle_kilocode.py
│   │   ├── test_install_lifecycle_opencode.py
│   │   ├── test_install_lifecycle_codex.py
│   │   ├── test_install_lifecycle_cursor.py
│   │   ├── test_update_propagation.py
│   │   └── test_remove_clean.py
│   └── fixtures/
│       ├── ephemeral_homes/
│       └── corrupted_manifests/
│
├── docs/
│   ├── install/                            Agent-installable URL targets
│   │   ├── _index.md                       Auto-generated catalog + paste-into-LLM prompt
│   │   ├── _loader-pattern.md              Shared explainer for Tier 3b technique
│   │   ├── claude-code.md                  Tier 1
│   │   ├── github-copilot-cli.md           Tier 1
│   │   ├── kilocode.md                     Tier 2
│   │   ├── opencode.md                     Tier 2
│   │   ├── codex.md                        Tier 3a
│   │   ├── cursor.md                       Tier 3a
│   │   ├── perplexity.md                   Tier 3b
│   │   ├── chatgpt-gpts.md                 Tier 3b
│   │   └── claude-projects.md              Tier 3b
│   ├── contributing/
│   │   ├── adding-a-plugin.md
│   │   ├── skill-authoring-guide.md
│   │   └── testing-locally.md
│   └── decisions/                          Short public ADRs (one per locked architectural call)
│       ├── 0001-tier-model.md
│       ├── 0002-orphan-branch-for-design.md
│       ├── 0003-sha-based-versioning.md
│       └── ...
│
├── template/                               Scaffolds for new contributors
│   ├── plugin/                             cp -r template/plugin plugins/my-plugin
│   └── skill/                              cp -r template/skill plugins/foo/skills/my-skill
│
├── spec/
│   └── agent-skills-spec.md                Canonical skill format specification
│
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md                      Contributor Covenant 2.1
├── LICENSE                                 BSD-3-Clause
├── README.md                               Multi-CLI pitch + 30-second install
├── SECURITY.md
└── THIRD_PARTY_NOTICES.md                  Auto-aggregated from per-plugin notices
```

### CI-enforced invariants

1. `marketplace.json` only references paths under `plugins/<name>`.
2. No `install-*.sh` script reads from `tests/`, `docs/`, or `scripts/agent_forge/translators/`.
3. Every `plugins/<name>/.claude-plugin/plugin.json` validates against Claude Code's published schema.
4. Every `SKILL.md` has valid frontmatter (`name`, `description`); `name` ≤ 64 chars.
5. Every reference linked from a `SKILL.md` body resolves to an actual file on disk.
6. PRs to `main` whose diff touches `docs/superpowers/**` are rejected.
7. No file path or string under `plugins/` references "kpmg" (case-insensitive).

### Branch separation

- `main` ships everything users see and consume. Clean, minimal, no design noise.
- `superpowers` is an orphan branch (independent commit history) holding `docs/superpowers/specs/` and `docs/superpowers/plans/`. Discoverable via GitHub branch dropdown. Never merged to `main`.
- Contributors doing design work use `git worktree add ../agent-forge-superpowers superpowers` to keep both checked out side-by-side.
- `release/v1.X.Y` branches are short-lived; cut from `main`, run Layer C, tag, then deleted.

## 4. Cross-CLI Tier Model and Translator Interface

### The translator contract

Every CLI translator (`scripts/agent_forge/translators/<cli>.py`) implements:

```python
from typing import Protocol, Literal
from pathlib import Path

class Translator(Protocol):
    name: str                              # e.g., "kilocode"
    tier: Literal[1, 2, 3]

    def detect(self) -> bool:
        """Is this CLI installed on the current machine?"""

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        """Map of source-relative path in repo → absolute destination on disk."""

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        """Copy or rewrite a skill directory into the target's expected shape."""

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        """Convert Claude Code agent frontmatter to the target's equivalent."""

    def translate_command(self, command_md: Path, dest: Path) -> None:
        """Convert a slash command to the target's slash-command format."""

    def post_install_verify(self, plugin: str) -> bool:
        """Optional: invoke the CLI to confirm the plugin loaded."""
```

The `agent-forge install <plugin>` command dispatches to the right translator and writes a manifest entry. Adding a new CLI is "implement the protocol, register the translator." That is the entire extension surface.

### Tier assignments — v1.0.0 commitment

| CLI | Tier | Detect by | Target install path | Status at v1.0.0 |
|---|---|---|---|---|
| Claude Code | 1 | `claude` binary on `$PATH` or `~/.claude/` | Native — Claude reads from cloned repo via `marketplace.json` | Native, fully supported |
| GitHub Copilot CLI | 1 | `gh copilot` subcommand or `~/.copilot/` | `.github/prompts/*.prompt.md` + `.github/copilot-instructions.md` (translator-generated, committed in-repo; user `git pull`s) | Native, fully supported |
| Kilo Code | 2 | `kilocode` binary or `.kilocode/` directory | `.kilocode/rules/<plugin>/*.md` (skill bodies as rules) + `.kilocode/modes/<plugin>.yaml` (agents as custom modes) | Adapter + integration test |
| OpenCode | 2 | `opencode` binary or `~/.config/opencode/` | `~/.config/opencode/agent/<name>.md` + `~/.config/opencode/command/<name>.md` (per-project AND global supported via flag) | Adapter + integration test |
| Codex (OpenAI) | 3a | `codex` binary or `AGENTS.md` in cwd | `AGENTS.md` (root) + sub-files referenced via include | Adapter + integration test |
| Cursor | 3a | `cursor` binary or `.cursor/` directory | `.cursor/rules/<plugin>/*.md` | Adapter + integration test |
| Aider | 3a | `aider` on `$PATH` or `.aider.conf.yml` | `~/.aider/conventions/<plugin>.md` | **Deferred to v1.1** — plugin model not stable enough |
| Amp (Sourcegraph) | 3a | `amp` binary | TBD | **Deferred to v1.1** — needs format research |
| Perplexity Spaces | 3b | User-asserted (no detection possible) | N/A — `agent-forge install <plugin> --target perplexity` prints loader to stdout | Loader generator + paste-ready guide |
| ChatGPT custom GPTs | 3b | User-asserted | N/A — same UX | Loader generator + paste-ready guide |
| Claude.ai Projects | 3b | User-asserted | N/A — same UX | Loader generator + paste-ready guide |

**v1.0.0 totals: 6 CLIs with adapters/native + 3 prompt-tool loaders = 9 install targets.**

### The Tier 3b loader template

For prompt-only tools, `scripts/agent_forge/translators/prompt_loader.py` emits this for each skill:

```markdown
---
name: humanize
description: Transform AI-generated text to read more naturally...
source: https://github.com/rahulnakmol/agent-forge/tree/main/plugins/writing/skills/humanize
---

# Humanize Skill (loader)

This is a thin loader. The actual skill body and references are fetched on demand
to preserve progressive disclosure (UNIX-style — load only what you need).

**When to invoke this skill:** [description from frontmatter]

**Skill body** (read first when triggered):
https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/plugins/writing/skills/humanize/SKILL.md

**References** (load only when SKILL.md instructs you to):
- pattern-library: https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/plugins/writing/skills/humanize/references/pattern-library.md
- voice-profiles: https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/plugins/writing/skills/humanize/references/voice-profiles.md

**Instructions to the host LLM:** When this skill is triggered, fetch the body
above. Do NOT eagerly fetch references — only retrieve a reference when the
body's instructions explicitly tell you to.
```

This preserves progressive disclosure across tools that have no native concept of it. The host LLM gets the same loading semantics it would in Claude Code: thin SKILL.md → on-demand reference fetches.

## 5. Manifest Format and Update Propagation

### Manifest schema (`~/.agent-forge/manifest.json`)

```json
{
  "schema_version": 1,
  "agent_forge_version": "1.0.0",
  "last_check": "2026-05-03T14:22:01Z",
  "remote": "https://github.com/rahulnakmol/agent-forge",
  "remote_branch": "main",
  "installs": [
    {
      "id": "writing@kilocode",
      "plugin": "writing",
      "scope": "plugin",
      "tier": "kilocode",
      "installed_sha": "a1b2c3d4...",
      "installed_tag": null,
      "pinned": false,
      "pin_target": null,
      "installed_at": "2026-05-01T10:14:33Z",
      "files": [
        "/Users/rahul/.kilocode/rules/writing/humanize.md",
        "/Users/rahul/.kilocode/modes/writing.yaml"
      ]
    }
  ],
  "operation_log": [
    { "ts": "2026-05-01T10:14:33Z", "op": "install", "id": "writing@kilocode", "sha": "a1b2c3d4..." }
  ]
}
```

**Two top-level structures:**
- `installs` — current state, derived from log. Read for "what do I have?"
- `operation_log` — append-only history. Read for "what happened, when?" Used to reconstruct `installs` if corrupted, and to power `agent-forge history`.

**Key fields:**
- `id` — globally unique. Format: `<plugin>[/<subpath>]@<tier>`. Allows the same plugin across multiple CLIs simultaneously.
- `scope` — `"plugin"` (whole plugin) or `"skill"` (cherry-picked single skill).
- `installed_sha` — git SHA of `plugins/<name>/` at install time. Drives staleness detection.
- `installed_tag` — release tag if installed via tag.
- `pinned` + `pin_target` — when true, `update` skips this install.
- `files` — full list of paths written, used by `agent-forge remove` for clean uninstall.

### Update flow

```
agent-forge update [<plugin>] [--check]
│
├─ 1. Lock the manifest (~/.agent-forge/manifest.lock — fcntl flock)
├─ 2. Resolve remote HEAD (GitHub REST API; no full git clone)
├─ 3. For each install in manifest:
│      ├─ Skip if pinned and pin_target matches installed_sha/tag
│      ├─ Compute upstream SHA for plugins/<plugin>/ at remote_branch HEAD
│      └─ If upstream_sha ≠ installed_sha → mark stale
├─ 4. If --check → print stale list, exit
├─ 5. Else, for each stale install:
│      ├─ Download fresh plugin tarball at upstream SHA
│      ├─ Dispatch to translator.translate_*  for the install's tier
│      ├─ Compute file diff: paths-to-add, paths-to-remove
│      ├─ Atomic apply: write to staging dir → rename into place → delete removed paths
│      ├─ Append `update` op to operation_log with new SHA
│      └─ Update install record
├─ 6. Update manifest.last_check
└─ 7. Release lock
```

**Atomicity guarantees:**
- One install fails → that install stays at its previous SHA (staging dir discarded). Other installs continue.
- Process killed mid-update → next `agent-forge update` notices and is safe to re-run.

### Soft-nudge mechanism

```python
# scripts/agent_forge/cli.py — runs at the top of every command
def maybe_nudge():
    last_check = manifest.last_check
    if last_check and (now() - last_check) > timedelta(days=7):
        click.echo(f"💡 You haven't checked for updates in {(now()-last_check).days}d. "
                   f"Run `agent-forge update --check` to see what's new.", err=True)
```

Cheap, non-blocking, only on stderr so it does not break scripted usage.

### Tier-specific update behaviour

| Tier | Update mechanism |
|---|---|
| 1 (Claude Code) | `agent-forge update` may invoke `claude plugin marketplace update` for unified UX; Claude itself auto-updates marketplace plugins on next launch. We mainly refresh our manifest entry. |
| 1 (Copilot CLI) | If installed via committed `.github/` files in user's repo, update means `git pull` in their config repo. Manifest tracks last known SHA so we warn on drift. |
| 2 / 3a | Full re-install via translator. Old files at old paths explicitly removed (we have the file list). |
| 3b | Loader file rarely changes; *content* (raw GitHub URLs) auto-refreshes on every fetch. Update is mostly a no-op unless the loader template itself was rewritten. |

### `agent-forge` CLI surface (frozen at v1.0.0)

```
agent-forge list                                # what's installed locally + tier
agent-forge available [--cli <tier>]            # what's in the marketplace I could install
agent-forge detect                              # which CLI(s) are on this machine
agent-forge install <plugin>[/<skill>] [--tier <cli>] [--tag v1.0.0]
agent-forge update [<plugin>] [--check]
agent-forge pin <plugin> <version>              # version = tag or sha
agent-forge unpin <plugin>
agent-forge sync                                # force-reinstall everything at HEAD
agent-forge remove <plugin> [--tier <cli>]
agent-forge history [<plugin>]                  # replay operation_log
agent-forge doctor                              # validate manifest, check file integrity
```

## 6. Test Harness Architecture

### Layered approach

| Layer | What it tests | Trigger | Cost |
|---|---|---|---|
| **A — Structural** | Schemas, frontmatter, references resolve, install scripts dry-run, boundary guards | Every PR | Free, ~30s |
| **B — Behavioural evals** | Per-skill rubric-judged output quality vs. committed baseline | PRs touching `plugins/**` or `tests/evals/**` (paths-filtered per skill) | ~$0.05–0.25 per PR via Anthropic API |
| **B nightly** | Full Layer B sweep across every skill | `cron: nightly` + manually via workflow_dispatch | ~$1–3 per run |
| **C — Integration** | Real CLI binaries in Docker; install / invoke / update / remove lifecycle | Push to `release/*` branches and version tags | Higher; runs only on release prep |

### Layer A — structural validation

Pure pytest, no network, no LLM. Fixtures auto-discover plugins by walking `plugins/`:

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def all_plugins() -> list[Path]:
    repo_root = Path(__file__).parent.parent
    return sorted(p.parent.parent for p in (repo_root / "plugins").glob("*/.claude-plugin/plugin.json"))

@pytest.fixture(scope="session")
def all_skills(all_plugins) -> list[Path]:
    return [s for p in all_plugins for s in p.glob("skills/*/SKILL.md")]
```

Each test parameterizes over the discovered set. Failures show exactly which plugin/skill broke. Run time <30s for the entire current ref-repo content.

### Layer B — behavioural evals (rubric-judged)

Each eval has three files: `inputs.json`, `rubric.md`, `test_<skill>.py`.

Rubric scoring uses Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) as the judge — cheap, deterministic enough at low temperature, fast. A 5-criterion rubric (no more — large rubrics become noise) scores each output 1–5 per criterion, averaged.

Regression detection: baseline scores live in `tests/evals/_baseline_scores.json`, committed. PRs fail if a skill's score drops > 0.3 below baseline (allows for natural jitter, catches real regressions). Maintainers update baselines intentionally with `pytest tests/evals --update-baselines` and commit the diff.

**Cost model:** ~10 cases × 5 skills evaluated per affected plugin × ~$0.005 per Haiku judge call ≈ $0.25 per full evals run. Per-skill PRs pay ~$0.05.

### Layer C — integration

Docker-based per-CLI tests. Each pulls a CLI binary from its official source, runs `agent-forge install <plugin>`, invokes a known skill, and asserts on output. Slow (5–10 min total) and requires API keys — gated to `release/*` branches and tag pushes.

### CI matrix

| Workflow | Trigger | Runs | Cost |
|---|---|---|---|
| `ci-structural.yml` | Every PR + push to main | Layer A | Free (~30s) |
| `ci-evals.yml` | PRs that touch `plugins/**` or `tests/evals/**` | Layer A + B (paths-filtered to changed skills) | $0.05–0.25 per run |
| `ci-evals-nightly.yml` | Nightly cron + workflow_dispatch | Full Layer B sweep | $1–3 per run |
| `ci-integration.yml` | Push to `release/*` + version tags | Layers A + B + C | Higher; release-only |
| `release.yml` | Tag push (`v*`) | Build/sign/publish `agent-forge` to PyPI; create GitHub Release | n/a |

PRs from forks lack secrets → forks see Layer A only. Maintainers re-trigger evals after review with a `/run-evals` label that triggers a workflow_dispatch.

### Local dev workflow

```bash
cd tests
uv sync                                  # one-time (or pip install -e .)

pytest tests/unit                        # fast inner loop (<30s)
pytest tests/unit -k humanize            # filter to one skill

export ANTHROPIC_API_KEY=...
pytest tests/evals/writing/humanize      # one eval, ~5s + a few cents
pytest tests/evals -m "not slow"         # all fast evals

pytest tests/evals/writing/humanize --update-baselines    # after intentional improvement
git add tests/evals/_baseline_scores.json
```

`docs/contributing/testing-locally.md` documents this verbatim.

### The boundary guard test

```python
# tests/unit/test_no_test_paths_in_installers.py
INSTALLERS = list((REPO / "scripts").glob("install-*.sh"))
FORBIDDEN = re.compile(r"\b(tests/|docs/|scripts/agent_forge/)")

@pytest.mark.parametrize("script", INSTALLERS, ids=lambda p: p.name)
def test_installer_does_not_reach_outside_plugins(script):
    body = script.read_text()
    for lineno, line in enumerate(body.splitlines(), 1):
        if FORBIDDEN.search(line) and not line.strip().startswith("#"):
            pytest.fail(f"{script.name}:{lineno} reads from non-shippable path: {line.strip()}")

def test_marketplace_only_declares_plugins():
    mp = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    for plugin in mp["plugins"]:
        assert plugin["source"].startswith("./plugins/"), \
            f"Plugin {plugin['name']} sources outside plugins/: {plugin['source']}"
```

## 7. Contribution Model and CI Gates

### Contributor tiers

| PR type | Required checks | Reviewers | CI workflows |
|---|---|---|---|
| Typo / docs / cosmetic | Layer A | 1 maintainer | structural only |
| New skill in existing plugin | A + B (eval added for the new skill) | 1 plugin owner + 1 maintainer | structural + evals |
| New plugin | A + B (eval suite for ≥ 1 representative skill) + manual review | 2 maintainers | structural + evals + manual sign-off |
| Translator change (`scripts/agent_forge/translators/*`) | A + tests against fixture plugins + integration smoke | 1 maintainer | structural + integration smoke |
| Marketplace meta (`marketplace.json`, top-level docs) | A + visual review | 2 maintainers | structural |

### CODEOWNERS (initial)

```
*                                       @rahulnakmol
plugins/writing/                        @rahulnakmol
plugins/prompts/                        @rahulnakmol
plugins/msft-arch/                      @rahulnakmol
plugins/pm/                             @rahulnakmol
scripts/agent_forge/translators/        @rahulnakmol
.claude-plugin/marketplace.json         @rahulnakmol
```

(Plugin owners get added per directory as community grows.)

### "Adding a new plugin" workflow

`docs/contributing/adding-a-plugin.md` documents the canonical 7-step flow:

```bash
gh repo fork rahulnakmol/agent-forge --clone
cp -r template/plugin/ plugins/my-new-plugin/
cd plugins/my-new-plugin/
# edit .claude-plugin/plugin.json (name, description, version)
cp -r ../../template/skill/ skills/my-skill/
# edit SKILL.md frontmatter (name, description) and body
# add references/, scripts/, assets/ as needed
# register in marketplace.json
cd ../../tests && pytest tests/unit -k my-new-plugin
mkdir -p tests/evals/my-new-plugin/my-skill
# create inputs.json + rubric.md + test_my_skill.py
pytest tests/evals/my-new-plugin --update-baselines
gh pr create --template plugin
```

`template/plugin/` and `template/skill/` are pre-filled with placeholders, frontmatter templates, README boilerplate, and example references.

### Required CI checks (branch protection on `main`)

- `ci-structural / unit`
- `ci-structural / boundary-guard`
- `ci-evals / evals` (only when paths-filter triggers it)
- `DCO`

PRs cannot merge until required checks pass. Layer C is *not* required on PRs — runs only on release branches.

### License & DCO

- Repo license: BSD-3-Clause.
- Per-plugin `LICENSE` file: optional override if a plugin uses different licensing for its content.
- Per-asset attribution: any third-party asset (font, template, reference) must be listed in `plugins/<name>/THIRD_PARTY_NOTICES.md`, aggregated into top-level `THIRD_PARTY_NOTICES.md` by CI.
- **DCO**: every commit must include `Signed-off-by: Name <email>`. CI uses the [DCO bot](https://github.com/apps/dco). No CLA required.

### PR templates

Three templates selectable via `?template=`:
- `.github/PULL_REQUEST_TEMPLATE/plugin.md` — new plugins
- `.github/PULL_REQUEST_TEMPLATE/skill.md` — new/modified skills
- `.github/PULL_REQUEST_TEMPLATE/default.md` — everything else

Each enforces minimum context: what changed, what testing tier applies, license source for new assets, and a "no proprietary content" attestation.

### Auto-generated content

| File | Generator | Trigger |
|---|---|---|
| `THIRD_PARTY_NOTICES.md` (top-level) | `scripts/aggregate-notices.py` | CI on push to main; fails if drift |
| `docs/install/_index.md` | `scripts/build-install-index.py` | CI on push to main |
| `CHANGELOG.md` | `release-please` or `git-cliff` | Release tag |

### Decisions of architectural impact

Land as ADRs under `docs/decisions/0NNN-<title>.md` on `main`. The full deliberation lives on the `superpowers` branch; the ADR is the public, locked-in version.

### Community surface

- `README.md`: project pitch + 30-second install (one example per Tier 1 CLI) + link to full docs.
- `CONTRIBUTING.md`: top-level overview that funnels to `docs/contributing/*`.
- `CODE_OF_CONDUCT.md`: Contributor Covenant 2.1.
- `SECURITY.md`: vulnerability reporting (private email or GitHub security advisories).
- GitHub Discussions enabled for "show and tell" + "ideas" categories — separate from issues.

## 8. Migration Plan and v1.0.0 Release Scope

### Imports from `rahulnakmol/agent-marketplace`

| Source | Destination | Notes |
|---|---|---|
| `plugins/{writing,prompts,msft-arch,pm}/**` | Same paths | Verbatim copy |
| `plugins/kpmg/**` | ❌ EXCLUDED | Proprietary; verified excluded by `test_no_kpmg_residue.py` |
| `plugins/kpmg/test_harness.py` | `tests/_legacy/kpmg_harness_reference.py` (temp) | Reviewed for reusable patterns; **deleted before v1.0.0 tag** |
| `.claude-plugin/marketplace.json` | Same | KPMG entry stripped, version reset to `1.0.0` |
| `spec/agent-skills-spec.md` | Same | Verbatim |
| `template/SKILL.md` | `template/skill/` (reorganized) | Expanded into directory with example references, scripts, assets stubs |
| `CONTRIBUTING.md`, `README.md`, `THIRD_PARTY_NOTICES.md` | Same paths | All rewritten from scratch for multi-CLI / v1.0 / no-KPMG |
| `LICENSE`, `.gitignore`, `.gitattributes` | Same | Adjusted |
| ❌ `docs/superpowers/specs/*` | **SKIPPED** | `superpowers` branch starts empty per author preference |
| ❌ `docs/superpowers/plans/*` | **SKIPPED** | Same |

### Created fresh (not in ref repo)

- `scripts/agent_forge/` — Python CLI (manifest, translators, detectors).
- `scripts/install-*.sh` — Bash one-liner shims.
- `scripts/aggregate-notices.py`, `scripts/build-install-index.py`.
- `tests/` directory with Layer A, B, C structure.
- `.github/workflows/ci-*.yml`, `CODEOWNERS`, PR templates.
- `docs/install/*.md`, `docs/contributing/*.md`, `docs/decisions/*.md`.
- `template/plugin/` scaffold.
- `CODE_OF_CONDUCT.md`, `SECURITY.md`.

### Branch initialization (already complete)

The `superpowers` orphan branch has been created and pushed. Worktree at `../agent-forge-superpowers/` is the working directory for future design/plan documents.

### v1.0.0 scope summary

- 4 plugins migrated, validated, KPMG-free
- 6 CLI adapters (2 Tier 1 native, 2 Tier 2, 2 Tier 3a) + 3 prompt-tool loaders (Tier 3b) = **9 install targets**
- Full `agent-forge` CLI (all 11 commands)
- Layer A complete; Layer B for **every skill**; Layer C for every CLI on release branches
- All install guides, contributor docs, decision records
- DCO bot live; branch protection enforced
- PyPI release pipeline functional
- Schema commitments frozen: `marketplace.json`, `manifest.json`, CLI surface, install-URL pattern

### Implementation phasing (all phases lead to one v1.0.0 tag)

1. **Phase 0 — Repo scaffolding**
   - Create empty `superpowers` orphan branch ✅ (done as part of writing this spec)
   - Base layout on main: `tests/`, `scripts/`, `docs/`, `template/`, `.github/`
   - `pyproject.toml` for CLI + `tests/pyproject.toml` for harness
   - Branch protection + DCO bot wired up

2. **Phase 1 — Plugin migration + Tier 1 Claude Code**
   - Copy 4 plugins, strip KPMG, rebuild `marketplace.json` (v1.0.0)
   - Layer A tests passing on all 4 plugins
   - Verify `claude plugin marketplace add file://./` → install + invoke each plugin

3. **Phase 2 — All 6 translators built**
   - Tier 1: Copilot CLI (writes `.github/prompts/`, `copilot-instructions.md`)
   - Tier 2: Kilo Code translator
   - Tier 2: OpenCode translator
   - Tier 3a: Codex translator
   - Tier 3a: Cursor translator
   - Tier 3b: Prompt-loader generator (one generator → 3 prompt tools)

4. **Phase 3 — Full `agent-forge` CLI surface**
   - All 11 commands, manifest read/write, atomic update flow

5. **Phase 4 — Test coverage at v1.0 bar**
   - Layer A: 100% plugin coverage
   - Layer B: eval suite for every skill; baselines committed
   - Layer C: integration test per CLI on release workflow

6. **Phase 5 — Documentation + contribution infrastructure**
   - All 9 install guides + `_loader-pattern.md` + `_index.md` generator
   - Contributor docs (3 files)
   - Decision records for every locked architectural call
   - README rewrite, `THIRD_PARTY_NOTICES.md` aggregator + CI check

7. **Phase 6 — Pre-release hardening**
   - `release/v1.0.0` branch cut
   - Layer C across all 6 CLIs in Docker
   - Dogfood on a fresh laptop, every install target
   - Security review (third-party content audit, secrets scan, supply-chain checks)
   - Release notes drafted

8. **Phase 7 — Tag v1.0.0**
   - Tag pushed → `release.yml` publishes `agent-forge` to PyPI
   - GitHub Release created with categorized changelog
   - Announcement

### Schema stability commitments at v1.0.0

These become public APIs — breaking changes require v2.0.0:

- `marketplace.json` schema (already follows Claude Code's published schema)
- `~/.agent-forge/manifest.json` schema (`schema_version: 1`)
- `agent-forge` CLI command surface + flags
- The install-URL pattern: `https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/docs/install/<plugin-or-skill>.md`
- `template/plugin/` and `template/skill/` skeleton structure

## 9. Open Questions to Resolve During Implementation

These are blockers before the v1.0.0 tag, but do not block the implementation plan:

- Exact current GitHub Copilot CLI slash-command path convention (the spec floor moved twice since Sept 2025 GA; verify against current `gh copilot` documentation in Phase 2).
- OpenCode v0.4+ global vs. per-project config split conventions (verify in Phase 2).
- Codex CLI's current `AGENTS.md` include syntax + MCP integration path (verify in Phase 2).
- Cursor 0.50+ skill/rule capability — has it added a "skill" concept beyond `.cursor/rules/`? (verify in Phase 2).
- Whether `plugins/kpmg/test_harness.py` has reusable patterns worth porting before deletion (decided in Phase 0).
- Whether to add `release-please` vs. `git-cliff` for changelog generation (decided in Phase 5).

## 10. Glossary

- **Plugin** — a top-level unit under `plugins/<name>/` containing a `.claude-plugin/plugin.json` manifest, plus `skills/`, `agents/`, and/or `commands/` subdirectories.
- **Skill** — a `SKILL.md` with frontmatter (`name`, `description`) and optional `references/`, `scripts/`, `assets/`. Designed for progressive disclosure: SKILL.md body is loaded on activation; references are loaded on demand.
- **Agent** — a Markdown file under `agents/` defining an autonomous task executor with frontmatter (`name`, `description`, `tools`, etc.).
- **Slash command** — a Markdown file under `commands/` invoked by the user with `/<name>`.
- **Tier** — an integer (1, 2, 3a, 3b) describing how natively a CLI is supported.
  - Tier 1: native; manifests committed in-repo at the CLI's expected path.
  - Tier 2: adapter; install scripts translate from canonical format to the CLI's filesystem layout.
  - Tier 3a: filesystem-enabled tools that accept Markdown but lack a true plugin system; install scripts copy directories.
  - Tier 3b: prompt-only tools; install emits a paste-ready loader Markdown that fetches references from raw GitHub URLs on demand.
- **Translator** — a Python class under `scripts/agent_forge/translators/` implementing the `Translator` Protocol for one CLI.
- **Manifest** — `~/.agent-forge/manifest.json`; the local record of every install across every CLI on a given machine.
- **Install URL pattern** — `https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/docs/install/<plugin-or-skill>.md`; the agent-installable entry point.
- **Loader (Tier 3b)** — a thin SKILL.md generated for a prompt-only tool; contains frontmatter for routing and links to raw GitHub URLs for the actual body and references.
- **Boundary guard** — the CI test (`tests/unit/test_no_test_paths_in_installers.py`) that ensures install scripts never read from `tests/`, `docs/`, or `scripts/agent_forge/`.
- **Operation log** — append-only history of install/update/pin/remove operations within `manifest.json`.
- **DCO** — Developer Certificate of Origin; per-commit `Signed-off-by` requirement, enforced by GitHub bot.
- **superpowers branch** — orphan branch holding all design specs and implementation plans; never merged to `main`.
