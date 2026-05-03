# GitHub MCP Tool Reference

## Overview

This document provides a complete reference for the GitHub MCP tools used by the
PM Backlog Generator skill. These tools are invoked via the GitHub MCP server
connection to create and query issues in GitHub repositories.

---

## Tool: issue_write

### Purpose
Create a new issue or update an existing issue in a GitHub repository.

### Parameters

| Parameter | Type     | Required | Description                                      |
|----------|----------|----------|--------------------------------------------------|
| method    | string   | Yes      | "create" for new issues, "update" for existing   |
| owner     | string   | Yes      | Repository owner (org or username)               |
| repo      | string   | Yes      | Repository name                                  |
| title     | string   | Yes*     | Issue title (* required for create)              |
| body      | string   | No       | Issue body in markdown                           |
| labels    | string[] | No       | Array of label names (not IDs)                   |
| assignees | string[] | No       | Array of GitHub usernames to assign              |
| type      | string   | No       | Issue type name (if org supports typed issues)   |

For updates, additional parameter:
| Parameter     | Type   | Required | Description                             |
|--------------|--------|----------|-----------------------------------------|
| issue_number  | integer| Yes      | Issue number to update                  |

### Response

Returns the created/updated issue object including:
- `number`: Issue number (human-readable, e.g., 42)
- `id`: Node ID (e.g., "I_kwDOABC123") -- REQUIRED for sub_issue_write
- `title`: Issue title
- `html_url`: Direct URL to the issue on GitHub
- `labels`: Array of label objects
- `state`: Issue state ("open")

### Usage Notes

1. The `labels` parameter takes label **names** (not IDs), unlike Linear.
2. Labels must already exist in the repository. If a label does not exist,
   the issue creation may fail or silently skip the label.
3. Always include the work item type label AND a priority label.
4. The `type` parameter only works if the organization has issue types enabled.
   Check with `list_issue_types` first.
5. The `body` field supports full GitHub-flavored markdown including task lists,
   tables, and code blocks.

### Example: Create an Epic Issue

```json
{
  "method": "create",
  "owner": "my-org",
  "repo": "my-project",
  "title": "Customer Onboarding Platform",
  "body": "## Type\nEpic\n\n## Overview\nPlatform for customer self-service onboarding...\n\n## Success Metrics\n- Registration conversion rate > 80%",
  "labels": ["epic", "priority-high"]
}
```

### Example: Create a User Story Issue

```json
{
  "method": "create",
  "owner": "my-org",
  "repo": "my-project",
  "title": "As a customer, I want to register with my email so that I can access the platform",
  "body": "## Type\nUser Story\n\n## User Story\nAs a **customer**...\n\n## Acceptance Criteria\n- [ ] Given...\n\n## Story Points\n5\n\n## Parent Feature\n- #12",
  "labels": ["user-story", "priority-high"]
}
```

---

## Tool: issue_read

### Purpose
Get full details of a specific issue. Used for deep cross-reference checks and
verifying created issues.

### Parameters

| Parameter     | Type    | Required | Description                              |
|--------------|---------|----------|------------------------------------------|
| method        | string  | Yes      | "get"                                    |
| owner         | string  | Yes      | Repository owner                         |
| repo          | string  | Yes      | Repository name                          |
| issue_number  | integer | Yes      | Issue number to retrieve                 |

### Response

Returns the full issue object including:
- `number`: Issue number
- `id`: Node ID
- `title`: Issue title
- `body`: Full issue body (markdown)
- `labels`: Array of label objects with name, color, description
- `state`: "open" or "closed"
- `assignees`: Array of assigned users
- `created_at`: ISO 8601 timestamp
- `html_url`: Direct URL

### Usage Notes

1. Use this to verify issues were created correctly after `issue_write`.
2. Use during cross-referencing to read the full body of potential duplicates.
3. The `body` field contains raw markdown that can be parsed for acceptance
   criteria and scope comparison.

---

## Tool: list_issues

### Purpose
List issues in a repository with optional filters. Used for cross-referencing
before creating new issues.

### Parameters

| Parameter | Type     | Required | Description                                  |
|----------|----------|----------|----------------------------------------------|
| owner     | string   | Yes      | Repository owner                             |
| repo      | string   | Yes      | Repository name                              |
| state     | string   | No       | "OPEN", "CLOSED", or "ALL" (default: "OPEN") |
| labels    | string[] | No       | Filter by label names                        |

### Response

Returns an array of issue summary objects:
- `number`: Issue number
- `id`: Node ID
- `title`: Issue title
- `state`: Issue state
- `labels`: Array of label names
- `created_at`: ISO 8601 timestamp

### Usage Notes

1. Always filter by `state="OPEN"` when cross-referencing to avoid matching
   completed work.
2. Use `labels` filter to get issues by type (e.g., `labels=["epic"]`).
3. Results may be paginated. Check response for pagination indicators.
4. This tool returns summaries, not full bodies. Use `issue_read` for full details.

---

## Tool: search_issues

### Purpose
Search issues across a repository using GitHub's search syntax. More powerful
than `list_issues` for keyword-based cross-referencing.

### Parameters

| Parameter | Type   | Required | Description                                     |
|----------|--------|----------|-------------------------------------------------|
| query     | string | Yes      | GitHub search query string                      |
| owner     | string | No       | Scope search to a specific owner                |
| repo      | string | No       | Scope search to a specific repository           |

### Query Syntax

The query parameter supports GitHub's full search syntax:

| Query Component        | Example                          | Description              |
|-----------------------|----------------------------------|--------------------------|
| Keywords              | `customer registration`          | Full-text search         |
| Repository scope      | `repo:my-org/my-project`         | Limit to one repo        |
| State filter          | `is:open` or `is:closed`         | Filter by state          |
| Type filter           | `is:issue` (not PR)              | Issues only              |
| Label filter          | `label:epic`                     | Filter by label          |
| Author filter         | `author:username`                | Filter by creator        |
| Assignee filter       | `assignee:username`              | Filter by assignee       |
| Combined              | `customer is:issue is:open repo:org/repo` | Multiple filters |

### Response

Returns an array of matching issues with:
- `number`: Issue number
- `title`: Issue title
- `body`: Issue body (may be truncated)
- `repository`: Repository full name
- `html_url`: Direct URL

### Usage Notes

1. Always include `is:issue is:open` to avoid matching PRs and closed issues.
2. Use 3-5 distinctive keywords from the planned item title.
3. If `owner` and `repo` are provided as parameters, you do not need
   `repo:owner/repo` in the query string.
4. Search results are ranked by relevance.
5. Use this tool before `list_issues` when you need keyword-based matching.

---

## Tool: sub_issue_write

### Purpose
Add a sub-issue relationship between two existing issues. This creates a formal
parent-child hierarchy visible in the GitHub UI.

### Parameters

| Parameter     | Type    | Required | Description                                    |
|--------------|---------|----------|------------------------------------------------|
| method        | string  | Yes      | "add" to create the relationship               |
| owner         | string  | Yes      | Repository owner                               |
| repo          | string  | Yes      | Repository name                                |
| issue_number  | integer | Yes      | Parent issue NUMBER (the human-readable number)|
| sub_issue_id  | string  | Yes      | Child issue NODE ID (NOT the number)           |

### CRITICAL: Issue ID vs Issue Number

This tool uses DIFFERENT identifier types for parent and child:

- `issue_number`: The human-readable issue number (e.g., 42). This identifies the
  PARENT issue.
- `sub_issue_id`: The node ID (e.g., "I_kwDOABC123"). This identifies the CHILD
  issue. You MUST use the `id` field from the `issue_write` response, NOT the
  `number` field.

### Example

After creating:
- Epic issue: number=10, id="I_kwDOABC_epic"
- Feature issue: number=11, id="I_kwDOABC_feat"

To make the feature a sub-issue of the epic:
```json
{
  "method": "add",
  "owner": "my-org",
  "repo": "my-project",
  "issue_number": 10,
  "sub_issue_id": "I_kwDOABC_feat"
}
```

### Usage Notes

1. Both issues must already exist before creating the sub-issue relationship.
2. The parent issue is identified by NUMBER, the child by NODE ID.
3. An issue can be a sub-issue of only one parent.
4. Sub-issue relationships can span across repository boundaries (in some cases).
5. If the sub_issue_id is invalid, the tool returns an error. Verify the ID
   was correctly captured from the `issue_write` response.

---

## Tool: list_issue_types

### Purpose
Get the available issue types for an organization. Some GitHub organizations have
issue types enabled (e.g., "Bug", "Feature", "Task").

### Parameters

| Parameter | Type   | Required | Description                          |
|----------|--------|----------|--------------------------------------|
| owner     | string | Yes      | Organization name                    |

### Response

Returns an array of issue type objects:
- `id`: Issue type ID
- `name`: Issue type name (e.g., "Bug", "Feature")
- `description`: Issue type description
- `color`: Issue type color

### Usage Notes

1. Call this during Phase 2 to check if the organization supports typed issues.
2. If types are available, map backlog types to organization types.
3. If no types are returned (or the call fails), rely on labels for classification.
4. Issue types are an organization-level feature, not repository-level.
5. Pass the matched type name in the `type` parameter of `issue_write`.

---

## Tool: add_issue_comment

### Purpose
Add a comment to an existing issue. Used for cross-referencing and linking
related items.

### Parameters

| Parameter     | Type    | Required | Description                            |
|--------------|---------|----------|----------------------------------------|
| owner         | string  | Yes      | Repository owner                       |
| repo          | string  | Yes      | Repository name                        |
| issue_number  | integer | Yes      | Issue number to comment on             |
| body          | string  | Yes      | Comment body in markdown               |

### Response

Returns the created comment object:
- `id`: Comment ID
- `body`: Comment body
- `created_at`: ISO 8601 timestamp

### Usage Notes

1. Use this to add cross-reference notes to existing issues.
2. Keep comments concise and informative.
3. Include the new issue number as a `#reference` so GitHub auto-links it.

---

## Invocation Sequence for Backlog Creation

### Phase 2: Platform Configuration

```
1. Confirm owner and repo with the user.

2. list_issues(owner, repo, state="OPEN")
   -> Verify repository access and get existing issue count.

3. list_issue_types(owner)
   -> Check for typed issues. If available, map types.
   -> Store type mapping or set useTypes=false.

4. list_issues(owner, repo, state="OPEN", labels=["epic"])
   -> Check which backlog labels exist.
   -> Repeat for: feature, user-story, tech-story, risk, impediment, ci-item
   -> Report missing labels to user for manual creation.
```

### Phase 3: Cross-Reference

```
5. For each planned backlog item:
   search_issues(query="<keywords> repo:<owner>/<repo> is:issue is:open")
   -> Collect potential matches.

6. For high-similarity matches:
   issue_read(method="get", owner, repo, issue_number=<match>)
   -> Read full body for detailed comparison.

7. Present cross-reference results to user.
```

### Phase 5: Issue Creation

```
8. For each Epic (in priority order):
   issue_write(method="create", owner, repo, title, body, labels=["epic", priority])
   -> Store returned {number, id} as epicRef.

9. For each Feature (grouped by parent Epic):
   issue_write(method="create", owner, repo, title, body,
               labels=["feature", priority])
   -> Store returned {number, id} as featureRef.
   sub_issue_write(method="add", owner, repo,
                   issue_number=epicRef.number, sub_issue_id=featureRef.id)

10. For each Story (grouped by parent Feature):
    issue_write(method="create", owner, repo, title, body,
                labels=[storyType, priority])
    -> Store returned {number, id} as storyRef.
    sub_issue_write(method="add", owner, repo,
                    issue_number=featureRef.number, sub_issue_id=storyRef.id)

11. For each Risk / Impediment / CI Item:
    issue_write(method="create", owner, repo, title, body,
                labels=[typeLabel, priority])

12. For cross-referenced existing issues:
    add_issue_comment(owner, repo, issue_number=existingNum,
                      body="Related: #newNum - created from [PRD name] backlog")
```

---

## Error Handling Patterns

### Common Errors and Recovery

| Error                          | Cause                              | Recovery                           |
|-------------------------------|------------------------------------|------------------------------------|
| "Not Found" (404)             | Invalid owner/repo or no access    | Verify repo name and permissions   |
| "Validation Failed" (422)     | Invalid label or field value       | Check label exists, fix field      |
| "Resource not accessible"     | Insufficient permissions           | Ask user to check token scopes     |
| "Rate limit exceeded" (403)   | Too many API calls                 | Wait for reset, retry with backoff |
| "Sub-issue not found"         | Invalid sub_issue_id               | Verify node ID from issue_write    |

### Rate Limit Management

GitHub has different rate limits:
- REST API: 5,000 requests/hour (authenticated)
- Search API: 30 requests/minute
- GraphQL API: 5,000 points/hour

For a typical backlog (20-40 issues):
1. Issue creation: 20-40 requests (well within limits).
2. Sub-issue linking: 15-30 requests.
3. Search queries: 5-10 requests (watch the 30/minute limit).
4. Add 1-second delay between search queries to stay within limits.

### Partial Failure Handling

1. Continue creating remaining issues after a failure.
2. If a parent issue fails, skip all its children.
3. If a sub_issue_write fails, the issues still exist -- just not linked.
   Note this in the summary for manual linking.
4. Report all failures with issue titles and error messages in the summary.
5. Provide manual instructions for any items that need to be created by hand.
