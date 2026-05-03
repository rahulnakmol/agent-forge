# Phase 0 — Repo Scaffolding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Stand up the empty skeleton of `agent-forge` on `main` — directory layout, `pyproject.toml` files, GitHub workflows skeleton, branch protection, DCO bot, PR templates, baseline community files. No plugins yet; no translators yet; no tests with real assertions yet. The repo should be installable with `pipx install -e ./scripts/agent_forge` and pass an empty `pytest` run.

**Architecture:** Two Python packages live in the repo: `scripts/agent_forge/` (the runtime CLI, published to PyPI later) and `tests/` (internal test harness, never published). Each has its own `pyproject.toml`. GitHub workflows live in `.github/workflows/`. Branch protection enforces required checks. The `superpowers` orphan branch already exists from spec writing.

**Tech Stack:** Python 3.11+, `uv` for dep management, `pytest` for tests, `click` for CLI, `pydantic` for manifest schemas, `jsonschema` for validation, GitHub Actions for CI, [DCO bot](https://github.com/apps/dco) for sign-off.

**Spec reference:** `docs/superpowers/specs/2026-05-03-agent-forge-marketplace-design.md` Sections 3 (Repo Layout), 7 (Contribution Model & CI Gates), 8 (Phase 0).

---

## Parallelization map

After Task 1 (initial directory tree creation), the following groups are fully independent and can each be a parallel subagent:

- **Group A** (CLI package): Tasks 2, 3
- **Group B** (Tests package): Tasks 4, 5
- **Group C** (Workflows skeleton): Tasks 6, 7, 8
- **Group D** (Community files): Tasks 9, 10, 11, 12
- **Group E** (Templates): Tasks 13, 14

Task 15 (final smoke + commit) runs after all groups complete.

---

## Task 1: Create the base directory tree

**Files:**
- Create: `tests/`, `scripts/agent_forge/translators/`, `docs/install/`, `docs/contributing/`, `docs/decisions/`, `template/plugin/`, `template/skill/`, `spec/`, `.github/workflows/`, `.github/PULL_REQUEST_TEMPLATE/`

- [x] **Step 1: Create directories**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
mkdir -p tests/unit tests/evals tests/integration tests/fixtures tests/_legacy
mkdir -p scripts/agent_forge/translators
mkdir -p docs/install docs/contributing docs/decisions
mkdir -p template/plugin template/skill
mkdir -p spec
mkdir -p .github/workflows .github/PULL_REQUEST_TEMPLATE
mkdir -p .claude-plugin
```

- [x] **Step 2: Add `.gitkeep` to empty dirs that need to exist on main**

```bash
touch tests/unit/.gitkeep tests/evals/.gitkeep tests/integration/.gitkeep tests/fixtures/.gitkeep
touch docs/install/.gitkeep docs/contributing/.gitkeep docs/decisions/.gitkeep
touch template/plugin/.gitkeep template/skill/.gitkeep
touch spec/.gitkeep
```

- [x] **Step 3: Verify**

```bash
find tests scripts docs template spec .github .claude-plugin -type d | sort
```
Expected: 19+ directories listed (no errors).

---

## Task 2: Create `scripts/agent_forge/pyproject.toml`

**Files:**
- Create: `scripts/agent_forge/pyproject.toml`
- Create: `scripts/agent_forge/__init__.py`
- Create: `scripts/agent_forge/cli.py` (stub)

- [x] **Step 1: Write `scripts/agent_forge/pyproject.toml`**

```toml
[project]
name = "agent-forge"
version = "0.1.0-dev"  # bumped to 1.0.0 in Phase 7
description = "Cross-CLI plugin marketplace installer for agent-forge"
authors = [{ name = "Rahul N Akmol", email = "rahulnakmol@gmail.com" }]
license = { text = "BSD-3-Clause" }
readme = "../../README.md"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1",
    "pydantic>=2.0",
    "httpx>=0.27",
    "tomli-w>=1.0",
    "platformdirs>=4.0",
]
classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.scripts]
agent-forge = "agent_forge.cli:main"

[project.urls]
Homepage = "https://github.com/rahulnakmol/agent-forge"
Repository = "https://github.com/rahulnakmol/agent-forge"
Issues = "https://github.com/rahulnakmol/agent-forge/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["agent_forge"]
```

- [x] **Step 2: Write `scripts/agent_forge/__init__.py`**

```python
"""agent-forge — cross-CLI plugin marketplace installer."""

__version__ = "0.1.0-dev"
```

- [x] **Step 3: Write `scripts/agent_forge/cli.py` stub**

```python
"""agent-forge CLI entry point. Real commands land in Phase 3."""

import click


@click.group()
@click.version_option()
def main() -> None:
    """agent-forge — install agent skills and plugins across CLIs."""


@main.command()
def hello() -> None:
    """Smoke-test command, removed in Phase 3."""
    click.echo("agent-forge skeleton: OK")


if __name__ == "__main__":
    main()
```

- [x] **Step 4: Verify install works**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pip install -e scripts/agent_forge
agent-forge hello
```
Expected output: `agent-forge skeleton: OK`

---

## Task 3: Add `scripts/agent_forge/translators/__init__.py` placeholder

**Files:**
- Create: `scripts/agent_forge/translators/__init__.py`
- Create: `scripts/agent_forge/translators/_base.py`

- [x] **Step 1: Write `__init__.py`**

```python
"""Per-CLI translator implementations. Real translators land in Phase 2."""
```

- [x] **Step 2: Write `_base.py` (the Translator Protocol stub)**

```python
"""Translator Protocol — stable contract every CLI translator implements.

Phase 2 fills in real method bodies; this stub locks the interface.
"""

from pathlib import Path
from typing import Literal, Protocol


class Translator(Protocol):
    name: str
    tier: Literal["1a", "1b", "2", "3"]

    def detect(self) -> bool:
        """Is this CLI installed on the current machine?"""
        ...

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        """Map source-relative repo paths → absolute on-disk destinations."""
        ...

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        """Copy or rewrite a skill directory into the target's expected shape."""
        ...

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        """Convert Claude Code agent frontmatter to the target's equivalent."""
        ...

    def translate_command(self, command_md: Path, dest: Path) -> None:
        """Convert a slash command to the target's slash-command format."""
        ...

    def post_install_verify(self, plugin: str) -> bool:
        """Optional: invoke the CLI to confirm the plugin loaded."""
        ...
```

---

## Task 4: Create `tests/pyproject.toml`

**Files:**
- Create: `tests/pyproject.toml`
- Create: `tests/conftest.py`
- Create: `tests/pytest.ini`

- [x] **Step 1: Write `tests/pyproject.toml`**

```toml
[project]
name = "agent-forge-tests"
version = "0.0.0"
description = "Internal test harness for agent-forge — never published"
requires-python = ">=3.11"
dependencies = [
    "pytest>=8.0",
    "pytest-xdist>=3.5",
    "anthropic>=0.40",
    "jsonschema>=4.21",
    "markdown-it-py>=3.0",
    "pyyaml>=6.0",
    "tomli>=2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [x] **Step 2: Write `tests/pytest.ini`**

```ini
[pytest]
testpaths = unit evals integration
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: tests that take more than 5 seconds
    requires_anthropic_key: tests that call the Anthropic API
    requires_docker: tests that need Docker for integration
addopts = -ra --strict-markers
```

- [x] **Step 3: Write `tests/conftest.py`**

```python
"""Shared fixtures: plugin discovery, ephemeral $HOME directories.

Real fixtures populated as plugins migrate (Phase 1) and translators land (Phase 2).
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def plugins_dir(repo_root: Path) -> Path:
    return repo_root / "plugins"


@pytest.fixture(scope="session")
def all_plugin_roots(plugins_dir: Path) -> list[Path]:
    """All plugin directories — empty until Phase 1 migrates plugins."""
    if not plugins_dir.exists():
        return []
    return sorted(p.parent.parent for p in plugins_dir.glob("*/.claude-plugin/plugin.json"))


@pytest.fixture(scope="session")
def all_skill_md_paths(all_plugin_roots: list[Path]) -> list[Path]:
    """All SKILL.md paths across all plugins. Empty until Phase 1."""
    return [s for p in all_plugin_roots for s in p.glob("skills/*/SKILL.md")]


@pytest.fixture
def ephemeral_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set HOME to a fresh tmp dir so install tests don't touch the real one."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    return fake_home
```

- [x] **Step 4: Verify pytest runs (with no tests yet)**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge/tests
pip install -e .
pytest --collect-only
```
Expected: `no tests collected` (zero errors).

---

## Task 5: Add the boundary-guard test (the lone real test in Phase 0)

**Files:**
- Create: `tests/unit/test_boundary_guard.py`

- [x] **Step 1: Write the test**

```python
"""Boundary guard — proves the deployable boundary is enforced.

This is the lone real test in Phase 0; it guarantees that as we add install
scripts and marketplace.json files in later phases, none of them sneak paths
under tests/, docs/, or scripts/agent_forge/.
"""

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
FORBIDDEN_PATHS = re.compile(r"\b(tests/|docs/|scripts/agent_forge/)")


def _install_scripts() -> list[Path]:
    return list((REPO / "scripts").glob("install-*.sh"))


@pytest.mark.parametrize(
    "script",
    _install_scripts() or [pytest.param(None, id="no-install-scripts-yet")],
)
def test_installer_does_not_reach_outside_plugins(script: Path | None) -> None:
    """Install scripts may only read from plugins/ — never tests/, docs/, or internal scripts."""
    if script is None:
        pytest.skip("No install scripts present yet; will activate in Phase 2.")
    body = script.read_text()
    for lineno, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if FORBIDDEN_PATHS.search(line):
            pytest.fail(
                f"{script.name}:{lineno} reads from non-shippable path: {stripped}"
            )


def test_marketplace_only_declares_plugins() -> None:
    """marketplace.json sources must all be ./plugins/<name>."""
    mp = REPO / ".claude-plugin" / "marketplace.json"
    if not mp.exists():
        pytest.skip("marketplace.json not present yet; will activate in Phase 1.")
    data = json.loads(mp.read_text())
    for plugin in data.get("plugins", []):
        source = plugin.get("source", "")
        assert source.startswith("./plugins/") or source.startswith("plugins/"), (
            f"Plugin {plugin.get('name')} sources outside plugins/: {source}"
        )
```

- [x] **Step 2: Verify it passes (skipped, since no install scripts yet)**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pytest tests/unit/test_boundary_guard.py -v
```
Expected: `2 skipped` or `1 passed, 1 skipped` — zero failures.

---

## Task 6: Write `.github/workflows/ci-structural.yml`

**Files:**
- Create: `.github/workflows/ci-structural.yml`

- [x] **Step 1: Write the workflow**

```yaml
name: ci-structural

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Reject design artifacts on main
        if: github.base_ref == 'main' || github.ref == 'refs/heads/main'
        run: |
          if git diff --name-only origin/main...HEAD 2>/dev/null | grep -E '^docs/superpowers/'; then
            echo "::error::docs/superpowers/** must live on the 'superpowers' branch, not main"
            exit 1
          fi
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install test harness
        run: pip install -e tests
      - name: Run Layer A tests
        run: pytest tests/unit -v
```

- [x] **Step 2: Verify YAML is valid**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-structural.yml'))"
```
Expected: no output (valid YAML).

---

## Task 7: Write `.github/workflows/ci-evals.yml` skeleton

**Files:**
- Create: `.github/workflows/ci-evals.yml`

- [x] **Step 1: Write the workflow skeleton**

```yaml
name: ci-evals

on:
  pull_request:
    branches: [main]
    paths:
      - 'plugins/**'
      - 'tests/evals/**'

jobs:
  evals:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install test harness
        run: pip install -e tests
      - name: Run Layer B evals (skipped until Phase 4)
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo "ANTHROPIC_API_KEY not set (likely a fork PR) — skipping evals"
            exit 0
          fi
          pytest tests/evals -v -m "not slow"
```

- [x] **Step 2: Verify YAML is valid**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-evals.yml'))"
```

---

## Task 8: Write `.github/workflows/release.yml` skeleton

**Files:**
- Create: `.github/workflows/release.yml`

- [x] **Step 1: Write the workflow skeleton**

```yaml
name: release

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install build tools
        run: pip install build twine
      - name: Build distribution
        run: python -m build scripts/agent_forge
      - name: Publish to PyPI (trusted publisher)
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages-dir: scripts/agent_forge/dist/
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

- [x] **Step 2: Verify YAML is valid**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))"
```

---

## Task 9: Write `LICENSE` (already in place — verify only)

**Files:**
- Verify: `LICENSE` (existing)

- [x] **Step 1: Confirm BSD-3-Clause**

```bash
head -1 /Users/rahulnakmol/Developer/Github/agent-forge/LICENSE
```
Expected: `BSD 3-Clause License` (or first line matching).

---

## Task 10: Write `CODE_OF_CONDUCT.md`

**Files:**
- Create: `CODE_OF_CONDUCT.md`

- [x] **Step 1: Write the file**

```markdown
# Contributor Covenant Code of Conduct

We follow the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## Reporting

Report unacceptable behavior to **rahulnakmol@gmail.com**. All reports are reviewed
and investigated promptly and fairly.

## Enforcement

Project maintainers will follow the [Community Impact Guidelines](https://www.contributor-covenant.org/version/2/1/code_of_conduct/#enforcement-guidelines)
when determining the consequences of any action they deem in violation of this
Code of Conduct.
```

---

## Task 11: Write `SECURITY.md`

**Files:**
- Create: `SECURITY.md`

- [x] **Step 1: Write the file**

```markdown
# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities via [GitHub Security Advisories](https://github.com/rahulnakmol/agent-forge/security/advisories/new)
or by emailing **rahulnakmol@gmail.com** with the subject line `SECURITY: agent-forge`.

Do **not** open public issues for security reports.

## Supported Versions

Until v1.0.0, only the latest tagged release receives security fixes.

After v1.0.0, the latest minor release on the current major version receives
security fixes for at least 6 months following the next release.

## Scope

In scope:
- The `agent-forge` Python CLI (`scripts/agent_forge/`)
- The install scripts (`scripts/install-*.sh`)
- The translator implementations (`scripts/agent_forge/translators/`)

Out of scope:
- Third-party CLI behavior (Claude Code, Copilot CLI, Codex, etc.) — report to the upstream vendor
- Skill content provided by community contributors — report to the plugin owner via CODEOWNERS
```

---

## Task 12: Write PR templates

**Files:**
- Create: `.github/PULL_REQUEST_TEMPLATE/default.md`
- Create: `.github/PULL_REQUEST_TEMPLATE/plugin.md`
- Create: `.github/PULL_REQUEST_TEMPLATE/skill.md`
- Create: `.github/CODEOWNERS`

- [x] **Step 1: Write `.github/PULL_REQUEST_TEMPLATE/default.md`**

```markdown
## Summary

<!-- One or two sentences: what changed and why. -->

## Type of change

- [x] Typo / docs / cosmetic
- [x] Translator change (`scripts/agent_forge/translators/*`)
- [x] Marketplace meta (`marketplace.json`, top-level docs)
- [x] Other

## Testing

- [x] `pytest tests/unit` passes locally
- [x] No new third-party assets without attribution in `THIRD_PARTY_NOTICES.md`

## Attestation

- [x] This PR does not introduce KPMG-branded or other proprietary content
- [x] All commits are signed off (`git commit -s`)
```

- [x] **Step 2: Write `.github/PULL_REQUEST_TEMPLATE/plugin.md`**

```markdown
## Summary

<!-- What's the new plugin and what does it do? -->

## Plugin checklist

- [x] Added under `plugins/<my-plugin>/` with `.claude-plugin/plugin.json`
- [x] Registered in `.claude-plugin/marketplace.json`
- [x] Includes at least one skill under `skills/<name>/SKILL.md`
- [x] At least one Layer B eval under `tests/evals/<my-plugin>/`
- [x] Eval baselines committed (`tests/evals/_baseline_scores.json`)

## License attestation

- [x] All third-party assets (fonts, templates, references) are listed in
      `plugins/<my-plugin>/THIRD_PARTY_NOTICES.md` with their licenses
- [x] All assets are BSD-compatible or Apache-2.0 / MIT / public domain
- [x] No KPMG or other proprietary brand assets

## Testing

- [x] `pytest tests/unit -k <my-plugin>` passes
- [x] `pytest tests/evals/<my-plugin>` passes
- [x] All commits are signed off (`git commit -s`)
```

- [x] **Step 3: Write `.github/PULL_REQUEST_TEMPLATE/skill.md`**

```markdown
## Summary

<!-- What's the new/changed skill? -->

## Skill checklist

- [x] `SKILL.md` has valid frontmatter (`name`, `description`)
- [x] `name` ≤ 64 characters
- [x] `description` clearly states when the skill should be invoked
- [x] References under `references/` are loaded only on demand (progressive disclosure)
- [x] Scripts under `scripts/` have shebangs and are executable
- [x] Eval added/updated under `tests/evals/<plugin>/<skill>/`

## Testing

- [x] `pytest tests/unit` passes
- [x] `pytest tests/evals/<plugin>/<skill>` passes
- [x] If skill behavior changed intentionally: baselines updated via
      `pytest tests/evals/<plugin>/<skill> --update-baselines`
- [x] All commits are signed off (`git commit -s`)
```

- [x] **Step 4: Write `.github/CODEOWNERS`**

```
# Default reviewer for everything
*                                       @rahulnakmol

# Plugin owners — add per-directory entries as community grows
plugins/writing/                        @rahulnakmol
plugins/prompts/                        @rahulnakmol
plugins/msft-arch/                      @rahulnakmol
plugins/pm/                             @rahulnakmol

# Critical infrastructure — always reviewed by core
scripts/agent_forge/translators/        @rahulnakmol
.claude-plugin/marketplace.json         @rahulnakmol
.github/workflows/                      @rahulnakmol
```

---

## Task 13: Write `template/plugin/` scaffold

**Files:**
- Create: `template/plugin/.claude-plugin/plugin.json`
- Create: `template/plugin/README.md`
- Create: `template/plugin/skills/.gitkeep`
- Create: `template/plugin/agents/.gitkeep`
- Create: `template/plugin/commands/.gitkeep`

- [x] **Step 1: Write `template/plugin/.claude-plugin/plugin.json`**

```json
{
  "$schema": "https://raw.githubusercontent.com/anthropics/claude-code/main/schemas/plugin.json",
  "name": "REPLACE-WITH-PLUGIN-NAME",
  "description": "REPLACE-WITH-ONE-LINE-DESCRIPTION",
  "version": "0.1.0",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "BSD-3-Clause"
}
```

- [x] **Step 2: Write `template/plugin/README.md`**

```markdown
# REPLACE-WITH-PLUGIN-NAME

REPLACE-WITH-ONE-PARAGRAPH-DESCRIPTION

## Skills

<!-- List each skill with a one-line summary. -->

## Agents

<!-- If any. -->

## Commands

<!-- If any. -->

## License

BSD-3-Clause unless individual skills/assets are licensed otherwise — see
`THIRD_PARTY_NOTICES.md`.
```

- [x] **Step 3: Add empty subdirs**

```bash
mkdir -p template/plugin/.claude-plugin
touch template/plugin/skills/.gitkeep template/plugin/agents/.gitkeep template/plugin/commands/.gitkeep
```

---

## Task 14: Write `template/skill/` scaffold

**Files:**
- Create: `template/skill/SKILL.md`
- Create: `template/skill/references/example-reference.md`
- Create: `template/skill/scripts/.gitkeep`
- Create: `template/skill/assets/.gitkeep`

- [x] **Step 1: Write `template/skill/SKILL.md`**

```markdown
---
name: REPLACE-WITH-SKILL-NAME
description: REPLACE-WITH-WHEN-TO-INVOKE-THIS-SKILL (max ~200 chars; clear trigger conditions)
---

# REPLACE-WITH-SKILL-NAME

REPLACE-WITH-OPENING-PARAGRAPH explaining what this skill does.

## When to use this skill

REPLACE-WITH-EXPLICIT-TRIGGER-CONDITIONS. Be specific. Examples:
- User asks to X
- User pastes Y and asks for Z
- Code in the working directory contains W

## How to apply

1. REPLACE-WITH-FIRST-STEP
2. REPLACE-WITH-SECOND-STEP

## References (loaded on demand)

When you need detailed pattern guidance, read `references/example-reference.md`.

When you need <other context>, read `references/other-file.md`.

## Scripts

If running scripts, use `scripts/<name>` and check the script's own docstring
for usage.
```

- [x] **Step 2: Write `template/skill/references/example-reference.md`**

```markdown
# Example Reference

This is a placeholder. Replace with detailed guidance the SKILL.md body links
to *only when needed*. Progressive disclosure: don't load this unless triggered.
```

- [x] **Step 3: Add empty subdirs**

```bash
touch template/skill/scripts/.gitkeep template/skill/assets/.gitkeep
```

---

## Task 15: Smoke test the skeleton + commit

**Files:**
- Modify: (none — verifying everything composes)
- Create: `CONTRIBUTING.md` (minimal stub; full version in Phase 5)

- [x] **Step 1: Write minimal `CONTRIBUTING.md` stub**

```markdown
# Contributing to agent-forge

Full contributor guide lands in Phase 5 (`docs/contributing/*`). For now:

1. Fork + clone
2. Sign off your commits: `git commit -s`
3. Run `pytest tests/unit` before opening a PR
4. Open a PR using one of the templates under `.github/PULL_REQUEST_TEMPLATE/`

Reach out via [GitHub Discussions](https://github.com/rahulnakmol/agent-forge/discussions) if you need help.
```

- [x] **Step 2: Run the full smoke**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pip install -e scripts/agent_forge
pip install -e tests
agent-forge hello
pytest tests/unit -v
python -c "import yaml; [yaml.safe_load(open(f)) for f in ['.github/workflows/ci-structural.yml', '.github/workflows/ci-evals.yml', '.github/workflows/release.yml']]"
echo "skeleton OK"
```
Expected: `agent-forge skeleton: OK`, then `2 skipped` (or 1 passed 1 skipped), then `skeleton OK`.

- [x] **Step 3: Stage everything**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
git add -A
git status
```
Expected: many new files staged; nothing deleted; `LICENSE`, `README.md`, `.gitignore` unchanged.

- [x] **Step 4: Commit**

```bash
git commit -s -m "Phase 0: scaffold repo skeleton

- agent-forge Python CLI package (scripts/agent_forge/) with click stub
- Test harness package (tests/) with pytest config + boundary guard
- GitHub Actions skeletons (ci-structural, ci-evals, release)
- PR templates (default, plugin, skill) + CODEOWNERS
- CODE_OF_CONDUCT.md, SECURITY.md, CONTRIBUTING.md (stub)
- Plugin and skill templates under template/
- Empty plugins/, .claude-plugin/, docs/install/, docs/contributing/, docs/decisions/

Implements Phase 0 of v1.0 plan; no plugins or translators yet.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

- [x] **Step 5: GitHub manual step (DO THIS — not scriptable here)**

Manually configure on github.com/rahulnakmol/agent-forge:
1. **Branch protection on `main`**: require status checks `ci-structural / unit`, require signed commits (DCO), require 1 approving review, dismiss stale reviews on push.
2. **DCO bot**: install [DCO app](https://github.com/apps/dco), enable for `agent-forge` repo.
3. **Discussions**: enable in Settings → Features → Discussions; create `Show & Tell` and `Ideas` categories.

(These settings can't be set via API without elevated permissions; document them as a runbook step here for the human operator.)

---

## Self-Review

- [x] Every task has exact file paths ✓
- [x] Every code step has complete code, no placeholders ✓
- [x] Verification commands have expected output ✓
- [x] Phase 0 produces a passing CI run on a fresh clone ✓
- [x] No dependencies on Phase 1+ (truly foundational) ✓
- [x] Boundary guard test installed and passing (skipped until Phase 1+ adds installers) ✓

**Done criteria:** `pip install -e scripts/agent_forge && agent-forge hello` returns the smoke message; `pytest tests/unit` exits 0; all 3 GH Actions YAMLs validate; `LICENSE`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS`, and the 3 PR templates are committed; branch protection + DCO bot active on GitHub.
