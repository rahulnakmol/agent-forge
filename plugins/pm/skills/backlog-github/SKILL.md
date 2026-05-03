---
name: backlog-github
description: >-
  GitHub Issues Backlog Exporter: creates GitHub issues from platform-neutral
  backlog via MCP. TRIGGER when: user asks to create GitHub issues from
  backlog, export backlog to GitHub, push work items to GitHub Issues, or
  invokes /backlog-github. Also triggers for: "create GitHub issues",
  "push to GitHub Issues", "GitHub backlog import", "issues from backlog
  in GitHub". Creates hierarchical issues with labels, milestones, issue
  types, and sub-issue hierarchy via GitHub MCP server.
  DO NOT TRIGGER for backlog decomposition (use backlog-decompose).
  DO NOT TRIGGER for Azure DevOps export (use backlog-ado) or Linear
  export (use backlog-linear).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# GitHub Issues Backlog Exporter

**Version**: 1.0 | **Role**: GitHub Issues Creation Specialist
**Methodology**: Gather Context > Cross-Reference > Create Issues > Verify

You take platform-neutral backlog files produced by `backlog-decompose` and create issues directly in GitHub via the GitHub MCP server.

**MCP tools used** (available via GitHub MCP server, not listed in allowed-tools):
`list_issues`, `search_issues`, `list_issue_types`, `issue_write`, `sub_issue_write`

## Prerequisites

- **Platform-neutral backlog** must exist at `{project}/specs/backlog/{epic-name}-backlog.md`
- If no backlog file exists, invoke `/backlog-decompose` first
- **GitHub MCP server** must be connected

## Phase 1: Gather GitHub Context

Use `AskUserQuestion` to collect:

| Field | Required | Example |
|-------|----------|---------|
| Repository owner/name | Yes | `acme-corp/platform-api` |
| Milestone | No | `v2.1` |

## Phase 2: Cross-Reference

Avoid creating duplicate issues:

1. Call `list_issues` for the target repository to retrieve open issues
2. Compare generated backlog titles against existing issues using fuzzy matching
3. Flag potential duplicates -- ask user: skip, update existing, or create new
4. Call `list_issue_types` to verify available issue types for the repository
5. Confirm label and milestone availability; note any that need manual creation

## Phase 3: Create Issues

Map backlog items to GitHub issue fields:

| Backlog Field | GitHub Field |
|---------------|-------------|
| Title | Title |
| Description + AC | Body (Markdown with acceptance criteria) |
| Work item type | Label (e.g., `epic`, `feature`, `user-story`, `risk`) |
| Priority (1/2/3) | Label (e.g., `priority:must`, `priority:should`, `priority:could`) |
| Story points | Label (e.g., `points:5`) or body metadata |
| Milestone | Milestone |
| Work item type | Issue Type (if available) |

Execute in order:
1. `issue_write` for all parent-level items (epics, then features) -- capture returned issue numbers
2. `issue_write` for all child items (stories, technical stories, risks, impediments, CI items)
3. `sub_issue_write` to establish parent-child hierarchy using captured issue numbers
4. `search_issues` to verify all items were created successfully

## Phase 4: Verify and Deliver

1. Confirm creation count matches expected count from search_issues results
2. Provide summary with issue URLs
3. Update `{project}/specs/backlog/backlog-summary.md` with: PRD reference, generation date, repository, item counts by type, story point totals, issue numbers and URLs for all created items

## Examples

**"Create GitHub issues from the authentication backlog"** -> Read `authentication-backlog.md`, collect owner/repo and milestone, list_issues to check duplicates, list_issue_types to confirm available types, issue_write parents first capturing numbers, issue_write children, sub_issue_write to link hierarchy, search_issues to verify, update `backlog-summary.md` with GitHub issue URLs.

**"Push the payment backlog to GitHub Issues in acme-corp/payments"** -> Read `payment-processing-backlog.md`, confirm repo `acme-corp/payments`, cross-reference existing issues, create all issues in parent-first order, establish sub-issue hierarchy, verify with search_issues, update `backlog-summary.md`.

## References

- `references/platforms/github-backlog-patterns.md`
- `references/mcp-integration/github-mcp-reference.md`

---

*backlog-github v1.0 | Gather Context > Cross-Reference > Create Issues > Verify*
