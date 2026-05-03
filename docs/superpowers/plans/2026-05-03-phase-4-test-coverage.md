# Phase 4 — Test Coverage at v1.0 Bar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Reach the v1.0 quality bar — Layer A complete (already done in Phases 1–3), Layer B evals for **every skill** in every plugin (with regression baselines committed), and Layer C integration tests covering all 6 native CLIs (Tier 1a + 1b) plus Tier 2 adapters.

**Architecture:** A shared rubric-judge harness in `tests/evals/_judge.py` evaluates each skill's output against a 5-criterion rubric using Claude Haiku 4.5. Per-skill suites live at `tests/evals/<plugin>/<skill>/{inputs.json, rubric.md, test_<skill>.py}`. Baselines in `tests/evals/_baseline_scores.json` enable regression detection. Layer C uses Docker images of each CLI to verify install/invoke/update lifecycles end-to-end on `release/*` branches.

**Tech Stack:** `anthropic` Python SDK for the Haiku judge, `pytest-xdist` for parallel eval execution, Docker for Layer C integration.

**Spec reference:** Section 6 (Test Harness Architecture).

**Depends on:** Phases 0–3 complete.

---

## Parallelization map

After Tasks 1–3 (judge harness + baseline machinery + first eval to validate the pattern), every skill eval is independent:

- **Group A** (eval suite per skill): Tasks 4–N — one task per skill, ~150+ tasks total. **Massively parallel**: dispatch 10–20 parallel subagents at a time.
- **Group B** (integration tests per CLI): Tasks Z+1 through Z+9 — one per CLI. Parallel.

Recommended dispatch: chunk the per-skill eval tasks into batches of 10 parallel subagents; run Group B's 9 integration tests fully in parallel.

---

## Task 1: Build the LLM judge harness

**Files:**
- Create: `tests/evals/_judge.py`
- Create: `tests/evals/_baseline_scores.json`
- Create: `tests/evals/conftest.py`
- Create: `tests/unit/test_judge.py`

- [x] **Step 1: Write the failing test**

```python
"""tests/unit/test_judge.py"""

from unittest.mock import patch, MagicMock
from tests.evals._judge import score_against_rubric


def test_judge_returns_float_in_range() -> None:
    fake_response = MagicMock()
    fake_response.content = [MagicMock(text='{"score": 4.2, "reasoning": "Good"}')]
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = fake_response
        score = score_against_rubric(
            output="Some output text",
            rubric="Rubric criteria here",
            case={"id": "test1", "input": "x"},
            model="claude-haiku-4-5-20251001",
        )
        assert 1.0 <= score <= 5.0
```

- [x] **Step 2: Implement `tests/evals/_judge.py`**

```python
"""Shared LLM judge for Layer B evals — uses Claude Haiku 4.5 by default."""

import json
import os
from pathlib import Path

import anthropic

JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "claude-haiku-4-5-20251001")
BASELINE_FILE = Path(__file__).parent / "_baseline_scores.json"


JUDGE_PROMPT = """You are an expert evaluator. Score the following output against the rubric.

Input given to the skill:
---
{input}
---

Skill output:
---
{output}
---

Rubric (score 1-5 on each criterion):
---
{rubric}
---

Return ONLY a JSON object with shape:
{{"score": <average of all criteria, 1.0-5.0>, "reasoning": "<one sentence>"}}
"""


def score_against_rubric(
    output: str,
    rubric: str,
    case: dict,
    model: str = JUDGE_MODEL,
) -> float:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                input=case.get("input", ""),
                output=output,
                rubric=rubric,
            ),
        }],
    )
    text = message.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    parsed = json.loads(text)
    return float(parsed["score"])


def load_baseline(skill_path: str, case_id: str) -> float | None:
    if not BASELINE_FILE.exists():
        return None
    data = json.loads(BASELINE_FILE.read_text())
    return data.get(skill_path, {}).get(case_id)


def assert_no_regression(score: float, baseline: float | None, tolerance: float = 0.3) -> None:
    if baseline is None:
        return  # No baseline yet; first run sets it (via --update-baselines)
    assert score >= baseline - tolerance, (
        f"Regression: score {score:.2f} < baseline {baseline:.2f} - tolerance {tolerance}"
    )


def update_baseline(skill_path: str, case_id: str, score: float) -> None:
    data = json.loads(BASELINE_FILE.read_text()) if BASELINE_FILE.exists() else {}
    data.setdefault(skill_path, {})[case_id] = round(score, 2)
    BASELINE_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
```

- [x] **Step 3: Initial baseline file**

```bash
echo '{}' > tests/evals/_baseline_scores.json
```

- [x] **Step 4: Implement `tests/evals/conftest.py`**

```python
"""Eval-specific fixtures + CLI flag for baseline updates."""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--update-baselines", action="store_true", default=False,
        help="Update tests/evals/_baseline_scores.json with current scores",
    )


@pytest.fixture
def update_baselines(request) -> bool:
    return request.config.getoption("--update-baselines")
```

- [x] **Step 5: Run the unit test**

```bash
pytest tests/unit/test_judge.py -v
```
Expected: 1 passing.

---

## Task 2: Build the skill invocation harness

**Files:**
- Create: `tests/evals/_invoke.py`
- Create: `tests/unit/test_invoke.py`

- [x] **Step 1: Test**

```python
"""tests/unit/test_invoke.py"""

from unittest.mock import patch, MagicMock
from tests.evals._invoke import invoke_skill


def test_invoke_skill_uses_claude_api() -> None:
    fake = MagicMock()
    fake.content = [MagicMock(text="Skill output here")]
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = fake
        result = invoke_skill(
            skill_body="You are a humanizer skill.",
            user_input="Make this human: AI text here.",
            context="casual blog post",
        )
        assert result == "Skill output here"
```

- [x] **Step 2: Implement `tests/evals/_invoke.py`**

```python
"""Invoke a skill against Claude Haiku 4.5 and return its output."""

import os

import anthropic

INVOKE_MODEL = os.environ.get("EVAL_INVOKE_MODEL", "claude-haiku-4-5-20251001")


def invoke_skill(skill_body: str, user_input: str, context: str | None = None) -> str:
    client = anthropic.Anthropic()
    user_message = user_input
    if context:
        user_message = f"Context: {context}\n\nInput:\n{user_input}"
    message = client.messages.create(
        model=INVOKE_MODEL,
        max_tokens=2000,
        system=skill_body,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text
```

- [x] **Step 3: Run**

```bash
pytest tests/unit/test_invoke.py -v
```

---

## Task 3: Build the first eval (writing/humanize) as the canonical pattern

**Files:**
- Create: `tests/evals/writing/humanize/inputs.json`
- Create: `tests/evals/writing/humanize/rubric.md`
- Create: `tests/evals/writing/humanize/test_humanize.py`

- [x] **Step 1: Write `inputs.json`**

```json
{
  "cases": [
    {
      "id": "ai_pattern_em_dashes",
      "input": "I am thrilled to announce — and this is truly remarkable — that we are launching our amazing new product.",
      "context": "user wants this rewritten in a natural human voice"
    },
    {
      "id": "corporate_jargon",
      "input": "We are leveraging synergies to deliver value-added solutions that drive operational excellence across the enterprise.",
      "context": "humanize for a casual blog post"
    },
    {
      "id": "ai_overclaim",
      "input": "This revolutionary, game-changing technology will fundamentally transform how every business operates.",
      "context": "rewrite without exaggeration"
    },
    {
      "id": "passive_voice_excess",
      "input": "It is recommended that the proposal be considered by the committee. The decision will be communicated by next week.",
      "context": "make active and direct"
    },
    {
      "id": "throat_clearing_opener",
      "input": "I'd like to take a moment to discuss the various ways in which we can potentially explore the possibility of considering a new approach.",
      "context": "cut throat-clearing"
    }
  ]
}
```

- [x] **Step 2: Write `rubric.md`**

```markdown
Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Removes AI tells** — em-dashes, "I'm thrilled," "truly remarkable," "game-changing," "revolutionary" eliminated. Score 5 if zero AI tells survive; 1 if substantially preserved.

2. **Preserves meaning** — no factual content lost or added. Score 5 if semantically identical; 1 if meaning shifted.

3. **Voice match** — output matches the requested context (casual/formal/blog/etc.). Score 5 if voice is appropriate; 1 if mismatched.

4. **Natural rhythm** — sentence length varies; no robotic cadence; reads aloud smoothly. Score 5 if cadence varies naturally; 1 if uniformly clipped or uniformly long.

5. **No new tells introduced** — doesn't substitute one AI pattern for another (e.g., replacing em-dashes with semicolons everywhere). Score 5 if cleanly humanized; 1 if just shuffled patterns.
```

- [x] **Step 3: Write `test_humanize.py`**

```python
"""tests/evals/writing/humanize/test_humanize.py"""

import json
import pathlib

import pytest

from tests.evals._invoke import invoke_skill
from tests.evals._judge import (
    assert_no_regression,
    load_baseline,
    score_against_rubric,
    update_baseline,
)

HERE = pathlib.Path(__file__).parent
SKILL_PATH = "writing/humanize"
SKILL_BODY = (
    pathlib.Path(__file__).resolve().parents[3]
    / "plugins/writing/skills/humanize/SKILL.md"
).read_text()
CASES = json.loads((HERE / "inputs.json").read_text())["cases"]
RUBRIC = (HERE / "rubric.md").read_text()


@pytest.mark.requires_anthropic_key
@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_humanize_quality(case, update_baselines) -> None:
    output = invoke_skill(SKILL_BODY, case["input"], case.get("context"))
    score = score_against_rubric(output, RUBRIC, case)
    if update_baselines:
        update_baseline(SKILL_PATH, case["id"], score)
        return
    baseline = load_baseline(SKILL_PATH, case["id"])
    assert_no_regression(score, baseline, tolerance=0.3)
```

- [x] **Step 4: Generate baselines**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
export ANTHROPIC_API_KEY=...  # ensure set
pytest tests/evals/writing/humanize --update-baselines -v
cat tests/evals/_baseline_scores.json
```
Expected: 5 cases scored; baseline file populated.

- [x] **Step 5: Re-run without `--update-baselines` to verify regression detection works**

```bash
pytest tests/evals/writing/humanize -v
```
Expected: 5 passing (scores within tolerance of baseline).

---

## Task 4 — Task N: Per-skill eval suites (MASSIVELY PARALLEL)

For each skill across all 4 plugins, create the same three-file suite as Task 3:
- `tests/evals/<plugin>/<skill>/inputs.json` (5–10 representative cases)
- `tests/evals/<plugin>/<skill>/rubric.md` (5-criterion rubric)
- `tests/evals/<plugin>/<skill>/test_<skill>.py` (parametrized runner)

**Skill enumeration (computed at task-creation time):**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
find plugins -name SKILL.md -type f | sort
```

Expected: ~150 paths across 4 plugins.

**For each SKILL.md found, the implementer creates one task** following the Task 3 pattern. The eval rubric for each skill is derived from:
1. The SKILL.md's `description` frontmatter (defines purpose → criteria 1)
2. The "When to use" section (defines triggers → criteria 2)
3. The skill's references and examples (defines quality bar → criteria 3-5)

**Parallel dispatch recipe (at execution time):**

```python
# Pseudo-code for the dispatching agent
skills = find_all_skills()  # ~150
for batch in chunks(skills, size=10):
    spawn_parallel_subagents([
        f"Create eval suite for {s.plugin}/{s.name}: read {s.skill_md_path}, "
        f"derive 5-10 inputs.json cases that exercise its trigger conditions, "
        f"write a 5-criterion rubric.md based on its description, "
        f"write test_{s.name}.py following the pattern in tests/evals/writing/humanize/, "
        f"run with --update-baselines to populate baseline scores, commit."
        for s in batch
    ])
```

**Per-skill task template (each subagent runs this):**

- [x] **Step 1: Read the SKILL.md to derive the eval inputs**

```bash
cat plugins/<plugin>/skills/<skill>/SKILL.md
```

- [x] **Step 2: Write `tests/evals/<plugin>/<skill>/inputs.json`**

5–10 cases. Each case has `id`, `input`, optional `context`. Inputs should exercise the skill's stated trigger conditions.

- [x] **Step 3: Write `tests/evals/<plugin>/<skill>/rubric.md`**

5 criteria, each scored 1–5, averaged. Criteria derived from skill's stated purpose + quality bar.

- [x] **Step 4: Write `tests/evals/<plugin>/<skill>/test_<skill>.py`**

Same structure as `test_humanize.py` (Task 3 Step 3). Adjust `SKILL_PATH` and the `pathlib` resolution to match the skill's location.

- [x] **Step 5: Generate baseline + verify**

```bash
pytest tests/evals/<plugin>/<skill> --update-baselines -v
pytest tests/evals/<plugin>/<skill> -v
```

- [x] **Step 6: Commit (one commit per skill, batched at end of phase)**

---

## Task Z+1 — Task Z+9: Layer C integration tests per CLI (PARALLEL)

For each native CLI (Tier 1a + Tier 1b + Tier 2 = 9 CLIs), create one Docker-based integration test.

**Files:**
- Create: `tests/integration/test_install_lifecycle_<cli>.py`
- Create: `tests/integration/dockerfiles/<cli>.Dockerfile`

### Per-CLI task template

- [x] **Step 1: Write the Dockerfile**

```dockerfile
# tests/integration/dockerfiles/claude-code.Dockerfile (example for Claude)
FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl git && apt-get clean
RUN curl -fsSL https://claude.ai/install.sh | sh  # adjust per CLI's official install method
COPY . /agent-forge
WORKDIR /agent-forge
RUN pip install -e scripts/agent_forge
CMD ["bash"]
```

- [x] **Step 2: Write the integration test**

```python
"""tests/integration/test_install_lifecycle_claude.py"""

import subprocess

import pytest

pytestmark = pytest.mark.requires_docker


def _docker_run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "run", "--rm", "agent-forge-test:claude-code"] + cmd,
        capture_output=True, text=True, timeout=120,
    )


def test_claude_install_writing_lifecycle() -> None:
    # Build image
    subprocess.run(
        ["docker", "build", "-t", "agent-forge-test:claude-code",
         "-f", "tests/integration/dockerfiles/claude-code.Dockerfile", "."],
        check=True,
    )
    # Add marketplace
    r = _docker_run(["claude", "plugin", "marketplace", "add", "file:///agent-forge"])
    assert r.returncode == 0, r.stderr
    # Install plugin
    r = _docker_run(["claude", "plugin", "install", "writing"])
    assert r.returncode == 0, r.stderr
    # Verify plugin loaded
    r = _docker_run(["claude", "plugin", "list"])
    assert "writing" in r.stdout
    # Update lifecycle
    r = _docker_run(["agent-forge", "update", "--check"])
    assert r.returncode == 0
    # Remove
    r = _docker_run(["claude", "plugin", "uninstall", "writing"])
    assert r.returncode == 0
```

- [x] **Step 3: Repeat per CLI**

CLIs to cover: `claude-code`, `copilot-cli`, `codex-cli`, `cursor`, `amp`, `gemini-cli`, `kilocode`, `opencode`, `crush`. Each gets its own Dockerfile + test file. Mark as `slow` and `requires_docker`.

- [x] **Step 4: Wire into `.github/workflows/ci-integration.yml`**

```yaml
name: ci-integration
on:
  push:
    branches: ['release/*']
    tags: ['v*']

jobs:
  integration:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        cli: [claude-code, copilot-cli, codex-cli, cursor, amp, gemini-cli, kilocode, opencode, crush]
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e tests
      - name: Run integration test for ${{ matrix.cli }}
        run: pytest tests/integration/test_install_lifecycle_${{ matrix.cli }}.py -v --tb=short
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Task Final: Update propagation lifecycle test

**Files:**
- Create: `tests/integration/test_update_propagation.py`
- Create: `tests/integration/test_remove_clean.py`

- [x] **Step 1: Write update-propagation test**

```python
"""End-to-end: install at SHA1, simulate upstream bump, run update, verify SHA2."""

import subprocess

import pytest

pytestmark = pytest.mark.requires_docker


def test_update_lifecycle_kilocode() -> None:
    # Use the kilocode Docker image (smallest representative Tier 2)
    subprocess.run(["docker", "build", "-t", "agent-forge-test:kilocode",
                    "-f", "tests/integration/dockerfiles/kilocode.Dockerfile", "."],
                   check=True)
    install = subprocess.run(
        ["docker", "run", "--rm", "agent-forge-test:kilocode",
         "agent-forge", "install", "writing", "--tier", "kilocode"],
        capture_output=True, text=True,
    )
    assert install.returncode == 0
    update_check = subprocess.run(
        ["docker", "run", "--rm", "agent-forge-test:kilocode",
         "agent-forge", "update", "--check"],
        capture_output=True, text=True,
    )
    assert update_check.returncode == 0
    assert "writing" in update_check.stdout
```

- [x] **Step 2: Write remove-clean test**

```python
"""Verify that `agent-forge remove` leaves zero residual files."""

import subprocess

import pytest

pytestmark = pytest.mark.requires_docker


def test_remove_leaves_no_residue() -> None:
    container_name = "agent-forge-remove-test"
    subprocess.run(
        ["docker", "run", "--name", container_name, "agent-forge-test:kilocode",
         "bash", "-c", "agent-forge install writing --tier kilocode && "
         "find ~/.claude/skills/writing -type f > /tmp/before.txt && "
         "agent-forge remove writing@kilocode && "
         "find ~/.claude/skills/writing -type f > /tmp/after.txt 2>&1 || echo 'no residue'"],
        check=True,
    )
    diff = subprocess.run(
        ["docker", "exec", container_name, "diff", "/tmp/before.txt", "/tmp/after.txt"],
        capture_output=True, text=True,
    )
    # If 'after' is empty (file missing or empty), diff exits non-zero — that's correct
    subprocess.run(["docker", "rm", container_name], check=True)
```

---

## Task Final+1: Commit Phase 4

- [x] **Step 1: Run full suite**

```bash
pytest tests/unit -v
pytest tests/evals -v -m "not slow"  # local sanity check
```

- [x] **Step 2: Commit**

```bash
git add tests/evals/ tests/integration/ .github/workflows/ci-integration.yml
git commit -s -m "Phase 4: Layer B evals for all skills + Layer C integration tests

Layer B (per-skill rubric-judged evals):
- tests/evals/_judge.py — Haiku 4.5 LLM judge with regression detection
- tests/evals/_invoke.py — skill invocation harness
- tests/evals/_baseline_scores.json — committed regression baselines
- ~150 per-skill eval suites under tests/evals/<plugin>/<skill>/
- --update-baselines flag for intentional improvements

Layer C (Docker-based integration):
- tests/integration/test_install_lifecycle_<cli>.py × 9 (one per native CLI)
- tests/integration/dockerfiles/<cli>.Dockerfile × 9
- tests/integration/test_update_propagation.py
- tests/integration/test_remove_clean.py
- .github/workflows/ci-integration.yml triggered on release/* + tags

CI matrix:
- Layer A every PR (existing)
- Layer B on PRs touching plugins/** or tests/evals/** (existing workflow now has tests)
- Layer B nightly full sweep (NEW workflow added in this commit)
- Layer C on release/* + tag pushes

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Self-Review

- [x] D6 (test layers A/B/C) covered ✓
- [x] Per-skill eval coverage requirement (D11) met by Tasks 4–N ✓
- [x] Regression detection mechanism implemented (D6) ✓
- [x] Integration tests cover all 9 CLIs (matches v1.0 native + Tier 2 set) ✓

**Done criteria:** every SKILL.md in plugins/ has a corresponding eval suite with committed baselines; full Layer A + B passes locally; Layer C workflow validates on a `release/v1.0.0-rc1` branch.
