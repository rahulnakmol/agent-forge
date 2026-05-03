# GitHub Backlog Patterns

## Overview

When the user selects GitHub as the target platform, the backlog generator creates
issues directly via the GitHub MCP tools. This document describes how to structure
backlogs in GitHub using issues, sub-issues, labels, and cross-references.

---

## Structural Mapping

| Backlog Concept     | GitHub Construct          | Implementation                         |
|---------------------|---------------------------|----------------------------------------|
| Epic                | Issue + "epic" label      | Top-level issue                        |
| Feature             | Sub-issue of Epic         | Issue with "feature" label, linked     |
| User Story          | Sub-issue of Feature      | Issue with "user-story" label, linked  |
| Technical Story     | Sub-issue of Feature      | Issue with "tech-story" label, linked  |
| Risk                | Issue + "risk" label      | Standalone issue, cross-referenced     |
| Impediment          | Issue + "impediment"      | Standalone issue                       |
| CI Item             | Issue + "ci-item" label   | Standalone issue                       |

---

## Label Taxonomy

Ensure these labels exist in the target repository. Create them via the GitHub API
or instruct the user to create them if the MCP tools do not support label creation.

| Label Name   | Color    | Description                                    |
|-------------|----------|------------------------------------------------|
| epic         | 7C3AED   | Epic-level work item (strategic initiative)    |
| feature      | 2563EB   | Feature-level work item (capability)           |
| user-story   | 059669   | User story (user-facing requirement)           |
| tech-story   | D97706   | Technical user story (infra/API/migration)     |
| risk         | DC2626   | Risk item (potential threat to delivery)        |
| impediment   | E11D48   | Impediment (blocking issue)                    |
| ci-item      | 8B5CF6   | Continuous improvement item                    |
| priority-high | B60205  | Must-have priority                             |
| priority-med  | FBCA04  | Should-have priority                           |
| priority-low  | 0E8A16  | Could-have priority                            |

### Priority Encoding

GitHub issues do not have a native priority field. Use priority labels:

| PRD Priority         | GitHub Label      | Description              |
|---------------------|-------------------|--------------------------|
| MH (Must Have)       | priority-high     | Critical for release     |
| SH (Should Have)     | priority-med      | Important, not blocking  |
| CH (Could Have)      | priority-low      | Nice to have             |

Each issue gets exactly one priority label in addition to its type label.

---

## Issue Body Format

Use structured markdown sections in the issue body. This ensures consistency
and makes issues parseable by automation tools.

### Epic Issue Body Template

```markdown
## Type
Epic

## Overview
[High-level description of the epic and its business context]

## Business Justification
[Why this epic matters to the organization]

## Scope

### In Scope
- [Capability 1]
- [Capability 2]

### Out of Scope
- [Exclusion 1]

## Success Metrics
- [KPI 1]: [Target value]
- [KPI 2]: [Target value]

## PRD Reference
[Link or section reference to source PRD]
```

### Feature Issue Body Template

```markdown
## Type
Feature

## Description
[What this feature does and who it serves]

## Business Drivers
[Business reasons and market context]

## In Scope
- [Capability 1]
- [Capability 2]

## Out of Scope
- [Exclusion 1]

## Parent Epic
- #[epic-issue-number]

## Estimation
- Effort: [hours or t-shirt size]
- Business Value: [1-100]
- Time Criticality: [1-100]
```

### User Story Issue Body Template

```markdown
## Type
User Story

## User Story
As a **[persona]**, I **[want to]** so that **[benefit]**.

## Context
[Additional context about why this story matters]

## Acceptance Criteria
- [ ] Given [precondition], When [action], Then [result]
- [ ] Given [precondition], When [action], Then [result]
- [ ] Given [precondition], When [action], Then [result]

## Story Points
[Fibonacci number: 1, 2, 3, 5, 8, 13, 21]

## Parent Feature
- #[feature-issue-number]

## Notes
[Any assumptions, constraints, or open questions]
```

### Risk Issue Body Template

```markdown
## Type
Risk

## Risk Statement
[Concise description of the risk]

## Business Impact
[What happens if this risk materializes]

## Assessment
- **Likelihood**: [1=Very Likely, 2=Likely, 3=Possible, 4=Unlikely, 5=Very Unlikely]
- **Impact**: [A=Severe, B=Significant, C=Moderate, D=Minor, E=Negligible]
- **Risk Level**: [1=High, 2=Medium High, 3=Medium, 4=Medium Low, 5=Low]

## Mitigation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Related Items
- #[related-epic-or-feature-number]
```

---

## Sub-Issue Hierarchy via sub_issue_write

GitHub supports sub-issues through the `sub_issue_write` MCP tool. This creates a
formal parent-child relationship visible in the GitHub UI.

### Important: Issue ID vs Issue Number

The `sub_issue_write` tool requires the **issue ID** (a node ID), NOT the issue
number. After creating an issue with `issue_write`, the response includes both:
- `number`: The human-readable issue number (e.g., 42)
- `id`: The node ID (e.g., "I_kwDOABC123")

Use the `id` value when calling `sub_issue_write`.

### Creation Order (Critical)

1. Create all Epic-level issues first. Record their issue numbers and IDs.
2. Create all Feature-level issues. Record their numbers and IDs.
3. Link Features as sub-issues of their parent Epics via `sub_issue_write`:
   ```
   sub_issue_write(method="add", owner, repo,
                   issue_number=<epic-number>, sub_issue_id=<feature-id>)
   ```
4. Create all User Story and Technical Story issues. Record their numbers and IDs.
5. Link Stories as sub-issues of their parent Features via `sub_issue_write`.
6. Create Risk, Impediment, and CI Item issues (standalone, no sub-issue link).

---

## Issue Types (Organization Feature)

Some GitHub organizations support typed issues. Check availability:

1. Call `list_issue_types(owner=<org-name>)`.
2. If issue types are available, map backlog types to organization issue types.
3. Pass the `type` parameter in `issue_write` when creating issues.
4. If issue types are not available, rely solely on labels for type classification.

---

## Repository Selection Workflow

### Step 1: Confirm Repository

Ask the user for:
- `owner`: The GitHub organization or user that owns the repository.
- `repo`: The repository name.

### Step 2: Verify Access

Attempt to call `list_issues(owner, repo, state="OPEN")` to verify the tool has
access to the repository. If this fails, ask the user to check permissions.

### Step 3: Check Existing Labels

Call `list_issues` with each expected label to see which labels already exist.
Inform the user of any labels that need to be created manually (since the GitHub
MCP may not have a label creation tool).

### Step 4: Confirm Configuration

Before creating any issues, confirm with the user:
- Repository: `owner/repo`
- Available labels
- Issue type support (if applicable)

---

## Cross-Referencing Existing Issues via search_issues

### Query Strategy

1. Call `search_issues` with keywords from each planned backlog item:
   ```
   search_issues(query="[keywords] repo:<owner>/<repo> is:issue is:open")
   ```
2. Also call `list_issues` with specific label filters to find existing items
   by type:
   ```
   list_issues(owner, repo, state="OPEN", labels=["epic"])
   ```

### Duplicate Detection

- Compare planned item titles against search results.
- Flag matches with title similarity above 70%.
- Check issue body for overlapping acceptance criteria or scope descriptions.

### Handling Duplicates

| Scenario               | Action                                              |
|------------------------|-----------------------------------------------------|
| Exact title match      | Skip creation, add cross-reference comment          |
| High similarity (>70%) | Present to user for decision                        |
| Partial overlap        | Create new issue, add cross-reference in body       |
| No match               | Create new issue normally                           |

### Cross-Reference in Issue Body

When a new issue relates to an existing one, add a "Related Issues" section:

```markdown
## Related Issues
- Related to #42 (existing epic covering partial scope)
- Blocks #55 (depends on this story's API)
```

### Cross-Reference via Comment

To link an existing issue to a newly created one, use `add_issue_comment`:

```
add_issue_comment(owner, repo, issue_number=42,
                  body="Related: #[new-issue-number] created as part of
                  [PRD name] backlog generation.")
```

---

## Estimation Encoding

GitHub issues have no native estimation field. Encode story points in the issue body
under the "Story Points" section and optionally in a label:

| Story Points | Optional Label    |
|-------------|-------------------|
| 1            | sp-1              |
| 2            | sp-2              |
| 3            | sp-3              |
| 5            | sp-5              |
| 8            | sp-8              |
| 13           | sp-13             |
| 21           | sp-21             |

Story point labels are optional. If the user's workflow does not use them, encode
points only in the issue body.
