# ADR 0004: Local Manifest as State-of-Truth

**Status:** Accepted (2026-05-03)
**Spec section:** D4

## Context

A user may have the same skill installed for multiple CLIs simultaneously. For example,
the `writing/humanize` skill might be installed for Claude Code (via native marketplace),
Kilo Code (via file copy to `~/.claude/skills/`), and Amp (via git URL clone to
`~/.amp/skills/`). Without a unified record, the agent-forge CLI cannot perform a
cross-CLI update sweep, audit what is installed where, or detect when a manually deleted
file has caused drift from the expected state. A per-CLI record would require the CLI
to enumerate all possible install locations without a central index.

## Decision

Maintain `~/.agent-forge/manifest.json` as the authoritative record of all installs.
The manifest records: plugin name, installed skills, target CLI tier, install path,
commit SHA at install time, and an operation log for auditing. All writes to the manifest
use file-level locking and atomic writes (write to temp file, then rename) to prevent
corruption from concurrent `agent-forge` invocations. The `agent-forge doctor` command
validates the manifest against the filesystem and repairs drift.

```json
{
  "version": 1,
  "installs": [
    {
      "plugin": "writing",
      "skill": "humanize",
      "tier": "claude-code",
      "path": "~/.claude/skills/writing/humanize/",
      "sha": "a1b2c3d4e5f6",
      "installed_at": "2026-05-03T12:00:00Z"
    }
  ],
  "operation_log": []
}
```

## Consequences

**Positive:**
- Single source of truth enables cross-CLI update sweeps with one command
- `agent-forge update --check` can report on all installed skills across all CLIs
- Audit log (`operation_log`) provides install/update/remove history
- `agent-forge doctor` can detect and repair manifest–filesystem drift

**Negative:**
- If the manifest diverges from the filesystem (e.g., user manually deletes skill files),
  `doctor` must be run to repair — the manifest is not self-healing automatically
- File locking uses POSIX `fcntl` — not available on native Windows (Windows Subsystem
  for Linux works fine)
- If `~/.agent-forge/` is deleted, all tracking is lost (skills remain installed, but
  manifest must be rebuilt via `agent-forge doctor --rebuild`)

## Alternatives considered

- **Per-CLI manifest files** — rejected because there would be no cross-CLI view; update
  sweeps would require reading N separate files and aggregating
- **Remote registry** — rejected because it requires authentication, introduces a network
  dependency for every operation, and creates a privacy concern (tracking what users install)
