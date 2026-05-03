# Cross-Reference Strategy

## Overview

Before creating new backlog items on any platform, the skill must check for existing
issues that overlap with the planned backlog. This prevents duplicates, ensures
continuity with ongoing work, and creates traceability links between related items.

---

## Why Cross-Referencing Matters

1. **Duplicate prevention**: Avoids creating issues that already exist, which
   confuses the team and inflates metrics.
2. **Context preservation**: Existing issues may have comments, attachments, and
   history that provide valuable context.
3. **Relationship building**: Linking new items to existing ones creates a
   navigable web of related work.
4. **Scope awareness**: Existing items may partially cover new requirements,
   reducing the scope of new work.

---

## Platform-Specific Query Strategies

### Linear

#### Step 1: List Existing Issues in the Target Project

```
list_issues(
  team: "<team-id>",
  project: "<project-id>",
  state: "backlog,todo,in_progress"
)
```

This returns all open issues in the target project. If no project is selected,
query at the team level.

#### Step 2: Filter by Labels (Optional Narrowing)

```
list_issues(
  team: "<team-id>",
  label: "epic"
)
```

Repeat for each label type (feature, user-story, tech-story, risk, impediment,
ci-item) to get categorized existing items.

#### Step 3: Keyword Search (If Available)

```
list_issues(
  team: "<team-id>",
  query: "<keyword from planned item title>"
)
```

Use 2-3 key words from the planned item title as the query string.

#### Step 4: Compare Results

For each planned backlog item:
1. Extract key words from the planned title (remove stop words: "as a", "I want",
   "so that", articles, prepositions).
2. Compare against each existing issue title.
3. Calculate similarity using word overlap:
   - `similarity = (matching words) / (total unique words in both titles)`
4. Flag matches above 0.5 (50%) similarity for review.

---

### GitHub

#### Step 1: Search for Existing Issues

```
search_issues(
  query: "<keywords> repo:<owner>/<repo> is:issue is:open"
)
```

Use the most distinctive 3-5 words from the planned item title.

#### Step 2: List Issues by Label

```
list_issues(
  owner: "<owner>",
  repo: "<repo>",
  state: "OPEN",
  labels: ["epic"]
)
```

Repeat for each backlog type label to get categorized existing items.

#### Step 3: Compare Results

Same comparison algorithm as Linear (word overlap similarity).

#### Step 4: Deep Check (If Needed)

For high-similarity matches, read the full issue body:

```
issue_read(
  method: "get",
  owner: "<owner>",
  repo: "<repo>",
  issue_number: <number>
)
```

Compare acceptance criteria and scope descriptions for semantic overlap.

---

### Azure DevOps

ADO mode generates offline files (CSV/Excel), so live cross-referencing is not
possible via MCP tools. Instead:

1. Instruct the user to export their current ADO backlog as a CSV.
2. If the user provides an exported CSV, parse it and compare titles.
3. Flag potential duplicates in the generated workbook with a "POSSIBLE DUPLICATE"
   tag.
4. Include a "Duplicate Check" column in the Excel workbook.

---

## Duplicate Detection Algorithm

### Title Similarity Calculation

```
function calculateSimilarity(title1, title2):
    words1 = normalize(title1).split(" ")
    words2 = normalize(title2).split(" ")

    # Remove stop words
    stopWords = ["as", "a", "an", "the", "i", "want", "to", "so", "that",
                 "for", "in", "on", "of", "is", "be", "and", "or"]
    words1 = words1.filter(w => !stopWords.includes(w))
    words2 = words2.filter(w => !stopWords.includes(w))

    # Calculate Jaccard similarity
    intersection = words1.filter(w => words2.includes(w)).length
    union = new Set([...words1, ...words2]).size

    return intersection / union

function normalize(text):
    return text.toLowerCase()
               .replace(/[^a-z0-9\s]/g, "")
               .replace(/\s+/g, " ")
               .trim()
```

### Similarity Thresholds

| Similarity | Classification     | Action                                    |
|-----------|--------------------|--------------------------------------------|
| >= 0.9     | Almost certain dup | Auto-skip, link to existing                |
| 0.7 - 0.89| Probable duplicate | Present to user, recommend skip            |
| 0.5 - 0.69| Possible overlap   | Present to user, recommend review          |
| < 0.5     | Likely distinct    | Create new item, no action needed          |

### Description Overlap Check

When title similarity is in the 0.5-0.7 range, perform a deeper check:

1. Extract acceptance criteria from the existing issue body.
2. Compare each criterion against the planned item's criteria.
3. If more than 50% of criteria overlap, escalate to "probable duplicate."

---

## Linking Strategies

### Linear: relatedTo Relations

When a new item is related to (but not a duplicate of) an existing item:

```
save_issue(
  title: "New item title",
  ...,
  relatedTo: ["<existing-issue-id>"]
)
```

This creates a bidirectional "Related" link visible on both issues.

### GitHub: Cross-Reference in Body

Add a "Related Issues" section to the new issue body:

```markdown
## Related Issues
- Related to #42 - [Existing issue title]
- See also #55 - [Another related issue]
```

GitHub auto-creates backlinks when an issue references another by number.

### GitHub: Cross-Reference via Comment

For existing issues that should know about the new item:

```
add_issue_comment(
  owner: "<owner>",
  repo: "<repo>",
  issue_number: 42,
  body: "New related issue created: #[new-number] - [title]\n\n
         Created as part of [PRD name] backlog generation."
)
```

### ADO: Tag-Based Linking

In the CSV, add a tag to items that have potential existing counterparts:

```
Tags: "cross-ref:existing-item-title;backlog-gen"
```

---

## Handling Partial Overlaps

When an existing issue covers part of a new requirement:

### Scenario 1: Existing Issue Covers a Subset

The existing issue handles part of the new requirement but not all of it.

**Action:**
1. Create the new issue with reduced scope (only the uncovered portion).
2. Add a cross-reference to the existing issue.
3. Note in the description: "Partial coverage exists in [link]. This item covers
   the remaining scope: [specifics]."

### Scenario 2: Existing Issue Covers a Superset

The existing issue is broader than the new requirement.

**Action:**
1. Do not create a new issue.
2. If the existing issue lacks specific acceptance criteria that the PRD provides,
   suggest adding them as a comment on the existing issue.
3. Log this in the backlog summary as "Covered by existing item [link]."

### Scenario 3: Overlapping but Different Angle

The existing issue addresses a similar area but from a different perspective
(e.g., existing is user-facing, new is technical).

**Action:**
1. Create the new issue.
2. Link as relatedTo (Linear) or cross-reference (GitHub).
3. Note the complementary relationship in both descriptions.

---

## User Interaction During Cross-Reference

The skill should present cross-reference findings to the user before proceeding:

### Presentation Format

```
## Cross-Reference Results

### Probable Duplicates (recommend skip)
| Planned Item                        | Existing Item           | Similarity |
|-------------------------------------|-------------------------|------------|
| [planned title]                     | [existing title] (#42)  | 85%        |

### Possible Overlaps (recommend review)
| Planned Item                        | Existing Item           | Similarity |
|-------------------------------------|-------------------------|------------|
| [planned title]                     | [existing title] (#55)  | 62%        |

### No Matches Found
- [planned title 1]
- [planned title 2]

**Action needed:** Please confirm which items to skip, link, or create.
```

### User Response Options

For each flagged item, the user can choose:
1. **Skip**: Do not create the new item.
2. **Link**: Create the new item and link it to the existing one.
3. **Create**: Create the new item without linking (overrides the recommendation).
4. **Merge**: Add the new item's details as a comment on the existing item.
