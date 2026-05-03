# Resume agent-forge v1.0.0 implementation

This file lives on the `superpowers` orphan branch. If you (or a fresh Claude
Code session) land here mid-build, here's how to pick up.

## Where things are

| Artifact | Branch | Path |
|---|---|---|
| Spec (the design) | `superpowers` | `docs/superpowers/specs/2026-05-03-agent-forge-marketplace-design.md` |
| Plans (8 phases) | `superpowers` | `docs/superpowers/plans/2026-05-03-phase-*.md` |
| Master index (parallelization strategy) | `superpowers` | `docs/superpowers/plans/2026-05-03-v1.0-master-index.md` |
| Implementation work | `main` | top-level files in `agent-forge/` |

## One-time setup on a new machine

```bash
# 1. Clone the repo
git clone https://github.com/rahulnakmol/agent-forge.git
cd agent-forge

# 2. Add the superpowers worktree alongside main
git worktree add ../agent-forge-superpowers superpowers

# 3. Open Claude Code (or desktop app) in the agent-forge directory
#    The worktree at ../agent-forge-superpowers gives you the plans without
#    polluting the main checkout.
```

## Kickoff prompt (paste this into a fresh Claude Code session)

```
Continue executing the agent-forge v1.0.0 implementation plan.

Setup verification:
1. Confirm cwd is the agent-forge repo root
2. Confirm git worktree list shows ../agent-forge-superpowers on the superpowers branch
3. Read ../agent-forge-superpowers/docs/superpowers/plans/2026-05-03-v1.0-master-index.md

Determine the next incomplete phase by checking git log on main for commits
matching "Phase N:". Start the first phase whose commit doesn't exist yet
(probably Phase 0 if this is a fresh start).

Use superpowers:subagent-driven-development to execute the chosen phase task-by-task.
For each task:
- Read the task from the plan file
- Dispatch fresh subagents in parallel where the plan's parallelization map allows
- Run two-stage review on each subagent's work
- Commit + push after each task (or after each parallel batch)
- Mark the task checkbox `- [x]` in the plan file when done

Continue through all 8 phases. Don't wait for human input unless:
- A task explicitly requires human action (Phase 0 GitHub setup, Phase 6 dogfooding, etc.)
- A test fails in a way that needs human triage
- An external service is unreachable (PyPI, GitHub API)

When you finish a phase, commit a brief "Phase N complete" status update and
move to the next phase.

Memory at ~/.claude/projects/-Users-rahulnakmol-Developer-Github-agent-forge/memory/
has user preferences and prior decisions — apply them.
```

## What's already committed (do NOT redo these)

On the `superpowers` branch:
- ✅ Initial branch setup
- ✅ Design spec written + reviewed (`docs/superpowers/specs/`)
- ✅ All 8 phase plans + master index (`docs/superpowers/plans/`)
- ✅ This RESUME.md

On the `main` branch:
- ✅ Initial commit (LICENSE, README stub, .gitignore)
- ⏳ Phase 0 onwards — TBD

## Status check command

To see what's done from any session:

```bash
cd agent-forge
git log main --oneline | grep -E "^[a-f0-9]+ Phase [0-9]:" | sort -k4
```

This prints one line per completed phase commit, in order. Whatever's missing is what to start next.

## Estimated effort remaining (with parallel subagents)

24–47 wall-clock hours total across all 8 phases (vs. 121–186 sequential). See
the master index for per-phase estimates and parallelization recipes.

## Switching machines mid-build

The local `~/.agent-forge/manifest.json` (built in Phase 3) is per-machine and
doesn't need to sync. The repo state on GitHub is the source of truth. As long
as you `git pull` on the new machine and the latest commit's tests pass, you're
good to continue.

For Claude Code session memory: the `~/.claude/projects/.../memory/` directory
is per-machine. The kickoff prompt above tells the new session where the plans
are; that's enough context. Memory files synced via cloud (Dropbox, iCloud,
etc.) are nice-to-have but not required.
