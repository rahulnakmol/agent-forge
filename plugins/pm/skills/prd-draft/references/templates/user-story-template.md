# User Story Template

## Standard Story Block

Use this template for every user story within a PRD. Copy and populate for each story.

---

```markdown
### Story {EPIC-PREFIX}-{NNN}: {Story Title}

**Priority**: {MH / SH / CH} | **Complexity**: {S / M / L}

```
As a {persona name -- must match a persona defined in Section 2},
I want {specific action the persona takes -- describe what, not how},
So that {specific value the persona receives -- business benefit, not technical outcome}.
```

**Acceptance Criteria:**

```gherkin
AC-1: {Short descriptive name for this criterion}
Given {precondition -- the system state before the action}
  And {additional precondition, if needed}
When {single action the user or system performs}
Then {observable, verifiable outcome}
  And {additional outcome, if needed}

AC-2: {Short descriptive name}
Given {precondition}
When {action -- typically an edge case or boundary condition}
Then {expected handling}

AC-3: {Short descriptive name}
Given {precondition}
When {action that triggers an error or failure}
Then {error handling behavior -- message shown, state preserved, recovery path}
```

**Notes:** {Optional. Implementation hints, design system references, links to mockups, or clarifications. Do not prescribe technical approach.}

**Dependencies:** {Optional. Other story IDs this story depends on, e.g., "Requires UO-001 complete for user account to exist." Or "None."}
```

---

## Field Reference

### Story ID

Format: `{EPIC-PREFIX}-{NNN}`

- EPIC-PREFIX: 2-4 character abbreviation derived from the epic name
  - User Onboarding -> `UO`
  - Payment Processing -> `PP`
  - Reporting Dashboard -> `RD`
  - Data Migration -> `DM`
- NNN: Sequential three-digit number starting at 001

### Title

Short, descriptive title that communicates the story's essence. Use verb-noun format.

**Good**: "Filter Orders by Date Range", "Export Report as PDF", "Bulk Import Users from CSV"
**Bad**: "Order Filtering", "Reports", "Import Feature"

### Priority

| Code | Name | Criteria |
|------|------|----------|
| MH | Must Have | Epic cannot deliver its core value without this story |
| SH | Should Have | Epic is functional without this but significantly diminished |
| CH | Could Have | Enhances the epic but can be deferred without impact to core value |

### Complexity

| Size | Effort | When to Assign |
|------|--------|---------------|
| S | 1-2 days | Single component, well-understood pattern, no external integration |
| M | 3-5 days | 2-3 components, moderate complexity, up to one integration point |
| L | 1-2 weeks | Cross-cutting, multiple integrations, significant unknowns |

**XL is not a valid assignment.** If estimation yields XL, the story must be split. Document the split rationale in the Notes field of the resulting smaller stories.

### Persona-Action-Value Statement

Three mandatory parts:

1. **Persona**: Must reference a persona defined in Section 2 of the PRD by name. Never use "a user", "the system", or "the admin" generically.

2. **Action**: What the persona wants to do. Describe the capability, not the implementation.
   - Good: "receive a notification when my order ships"
   - Bad: "have the system send a push notification via Firebase"

3. **Value**: Why the persona cares. Must be a business or personal benefit.
   - Good: "so that I can plan to be home for delivery"
   - Bad: "so that the notification table is updated"

### Acceptance Criteria

Minimum 3, maximum 8 per story. Must include at least:

1. One **happy path** criterion (the primary success scenario)
2. One **boundary/validation** criterion (edge cases, input validation)
3. One **negative/error** criterion (what happens when things go wrong)

Additional categories as appropriate:
- Authorization (who can and cannot do this)
- Performance (measurable response time or throughput)
- State transition (how entity status changes)
- Data integrity (what is persisted, audited, or preserved)

### Notes

Optional field for context that does not fit elsewhere:
- Links to Figma mockups or design specs
- References to existing similar features
- Regulatory context that shaped the criteria
- Known technical risks (informational, not prescriptive)

### Dependencies

Optional field for story-level dependencies:
- Other story IDs within the same epic
- Stories from other epics
- External system availability
- Third-party API readiness

Format: "Requires {STORY-ID}: {reason}" or "Blocked by {external dependency}: {context}"

---

## Story Ordering Rules

Within a PRD, stories are ordered by:

1. **Priority tier**: All MH stories before SH stories before CH stories
2. **Dependency**: Within a tier, foundational stories (that others depend on) come first
3. **Persona flow**: Within equal dependency, follow the natural user journey order

---

## Story Count Guidelines

| Epic Size | Story Range | Signal |
|-----------|------------|--------|
| Small epic | 3-5 | Focused, single-persona, single-workflow |
| Medium epic | 5-10 | Normal -- multiple personas or branching workflows |
| Large epic | 10-15 | Maximum -- verify each story passes INVEST |
| Too many | 15+ | Epic must be split before PRD generation |

---

*pm-prd-generator v1.0 | User Story Template*
