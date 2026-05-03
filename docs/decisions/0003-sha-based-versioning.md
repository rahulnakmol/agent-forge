# ADR 0003: SHA-Based Versioning with Optional Tags

**Status:** Accepted (2026-05-03)
**Spec section:** D3

## Context

Plugin skills in a content marketplace change continuously. Unlike software libraries,
skills improve incrementally: a prompt gets refined, a voice profile is updated, a
rubric criterion is tightened. Traditional semantic versioning requires a human to
decide when a change warrants a patch, minor, or major version bump — which is
ceremony-heavy for a content-first marketplace. The question "is my installed version
current?" maps more naturally to "is my local commit SHA the same as the remote HEAD?"
than to "is 1.2.3 less than 1.3.0?"

## Decision

Track installed plugins by commit SHA. The `~/.agent-forge/manifest.json` records the
SHA of the commit at which each plugin was installed. Update detection compares the
recorded SHA against the remote `HEAD` SHA. Optional tag pins are available via
`agent-forge pin <plugin>@<tag>` for users who need reproducibility over currency.

The update check is:
```
remote_sha = git ls-remote origin HEAD
if local_sha != remote_sha: report stale
```

## Consequences

**Positive:**
- Always maps exactly to the state of the repo at install time — no ambiguity
- Update detection is trivially correct (compare two strings)
- No versioning ceremony: contributors don't have to bump version numbers
- Pin support (`agent-forge pin`) gives reproducibility when needed

**Negative:**
- SHA is opaque to users: "installed at a1b2c3d" is less readable than "version 1.2.3"
- Staleness detection requires a network call to compare against remote HEAD
- If the repo history is rewritten (force push), recorded SHAs may become unreachable

## Alternatives considered

- **Semantic versioning (semver)** — rejected because it requires release management
  process (who bumps the version? when? for what?) that adds friction to a content
  marketplace where skills change frequently and continuously
- **Date-based versioning (calver)** — rejected because a date does not uniquely
  identify content: two installs on the same day may get different content if the repo
  was updated between them, yet both would record the same version string
