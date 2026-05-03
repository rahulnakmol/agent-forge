# User Story Writing Standards

## The Persona-Action-Value Format

Every user story follows this structure:

```
As a {persona},
I want {action},
So that {value}.
```

### Rules

1. **Persona** must be a named persona from the understanding document or TOM role mapping -- never "a user" or "the system"
2. **Action** describes what the persona wants to do, not how the system implements it
3. **Value** explains the business benefit, not the technical outcome

### Examples

**Good:**
```
As a warehouse manager,
I want to receive automated low-stock alerts for critical items,
So that I can reorder before stockouts impact production schedules.
```

**Bad:**
```
As a user,
I want the system to send notifications,
So that the database is updated.
```

Problems: generic persona, system-focused action, technical value statement.

---

## INVEST Criteria

Every user story must satisfy all six INVEST criteria before inclusion in a PRD.

### Independent

The story can be developed, tested, and deployed without requiring other stories in the same epic to be complete first.

**Test**: Can this story be moved to a different sprint without breaking anything?

**Fix**: If stories are coupled, either merge them or extract the shared dependency into a foundation story.

### Negotiable

The story describes the what and why, not the how. Implementation details are left to the development team.

**Test**: Could the team implement this three different ways and still satisfy the acceptance criteria?

**Fix**: Remove implementation prescriptions. Replace "Build a REST API endpoint that..." with "Enable the system to..."

### Valuable

The story delivers measurable value to the persona named in the story. Technical stories (refactoring, infrastructure) must be reframed to show persona impact.

**Test**: Can you explain to the persona why this story matters to them?

**Fix**: If the story is purely technical, wrap it in persona value: "As an operations manager, I want the report to load in under 3 seconds, so that I can make real-time decisions during shift changes."

### Estimable

The team can estimate the effort required. If unknowns prevent estimation, the story needs a spike or investigation story first.

**Test**: Can the team assign S/M/L/XL complexity without extensive research?

**Fix**: Break out unknowns into a separate spike story. The investigation story delivers a recommendation; the implementation story follows.

### Small

The story fits within a single sprint. If it cannot be completed in one sprint, it is too large and must be split.

**Test**: Can a single developer complete this in 1-5 days?

**Fix**: Split by workflow step, data scope, persona variant, or complexity tier.

### Testable

The story has acceptance criteria that can be verified with a specific test. No subjective or unmeasurable criteria.

**Test**: Can you write an automated test for every acceptance criterion?

**Fix**: Replace vague criteria ("should be fast", "user-friendly") with measurable ones ("loads in < 2 seconds", "completes in < 3 clicks").

---

## Story Splitting Techniques

When a story is too large (L or XL complexity), split using these patterns:

### By Workflow Step
Original: "As a customer, I want to complete a purchase"
Split:
- "As a customer, I want to add items to my cart"
- "As a customer, I want to enter payment information"
- "As a customer, I want to receive order confirmation"

### By Data Variation
Original: "As an admin, I want to import user data"
Split:
- "As an admin, I want to import users from CSV"
- "As an admin, I want to import users from Active Directory"

### By Business Rule
Original: "As a manager, I want to approve purchase orders"
Split:
- "As a manager, I want to approve POs under $10,000 (single approval)"
- "As a manager, I want to route POs over $10,000 for director approval"

### By Interface
Original: "As a field worker, I want to submit inspection reports"
Split:
- "As a field worker, I want to submit reports via mobile app"
- "As a field worker, I want to submit reports via web portal"

### By Performance/Quality
Original: "As an analyst, I want to search historical records"
Split:
- "As an analyst, I want to search records by keyword (basic)"
- "As an analyst, I want to filter search results by date range, status, and category"

---

## Priority Assignment

| Priority | Code | Inclusion Rule | MoSCoW Equivalent |
|----------|------|---------------|-------------------|
| Must Have | MH | Epic fails without this story | Must |
| Should Have | SH | Epic is viable but diminished without it | Should |
| Could Have | CH | Nice-to-have, include if capacity permits | Could |

**Assignment rules:**
- At least 60% of stories in an epic should be MH
- No more than 20% should be CH
- If over 80% are MH, the epic may be too tightly scoped (consider adding stretch goals)

---

## Complexity Estimation

| Size | Effort | Characteristics |
|------|--------|----------------|
| S | 1-2 days | Single component, well-known pattern, no integrations |
| M | 3-5 days | 2-3 components, some complexity, one integration point |
| L | 1-2 weeks | Cross-cutting concern, multiple integrations, unknowns |
| XL | 2+ weeks | Must be split -- XL stories are not acceptable in a PRD |

**XL is a signal, not a size.** If estimation yields XL, the story must be split before inclusion. Document the split rationale in the PRD.

---

## AI/Agent Initiative Story Patterns

For products involving AI agents, copilots, or autonomous workflows, use these adapted patterns:

### Agent-as-Persona
```
As the order-processing agent,
I want to validate incoming orders against inventory levels,
So that I can auto-approve valid orders without human intervention.
```

### Human-Agent Collaboration
```
As a customer service representative,
I want the support agent to draft response suggestions based on ticket context,
So that I can respond to customers faster while maintaining quality.
```

### Agent Oversight
```
As a compliance officer,
I want to review and approve agent decisions that exceed the $50,000 threshold,
So that high-value transactions maintain human oversight.
```

### Fallback/Escalation
```
As the claims-processing agent,
I want to escalate ambiguous claims to a human adjuster with full context,
So that edge cases are handled correctly without losing processing history.
```

---

## Anti-Patterns

### Too Large
"As a user, I want a complete dashboard with real-time analytics, customizable widgets, export functionality, and role-based access."

**Fix**: Split into 4+ stories, one per capability.

### Too Technical
"As the system, I want to implement a message queue for asynchronous processing."

**Fix**: Reframe around persona value. Who benefits from async processing? What do they experience?

### No Persona
"Create an API endpoint for user data retrieval."

**Fix**: Who calls this API? Why? "As a mobile app user, I want to view my profile information, so that I can verify my account details are correct."

### Vague Acceptance Criteria
"The feature should work well and be user-friendly."

**Fix**: Define "well" and "user-friendly" with Given-When-Then criteria and measurable thresholds.

### Solution-Prescriptive
"As a user, I want a React dropdown component with typeahead search."

**Fix**: Describe the need, not the implementation. "As a user, I want to quickly find and select my country from a list of 200+ options."

---

*pm-prd-generator v1.0 | User Story Writing Standards*
