# Improvement Categorization

## Purpose

Every review produces improvement suggestions. This reference defines how to categorize, prioritize, and format those suggestions so they are actionable by the PRD author or by `pm-prd-generator` in the rewrite loop.

---

## Priority Levels

### P0: Critical

**Criteria**: Blocks development or fundamentally misaligns the product with user needs. The PRD cannot proceed to implementation without addressing these issues.

**Examples**:
- Core user need identified in discovery is not addressed by any feature
- A feature as described would create a hostile user experience (star 1-2)
- Success metrics contradict the stated product goals
- Critical dependency or technical constraint not acknowledged
- Security or compliance requirement missing for regulated industry

**Expected response**: Must be resolved before the PRD is approved. In the rewrite loop, these are the first items addressed.

### P1: High

**Criteria**: Significant quality gap that materially weakens the PRD. The PRD could technically be implemented without addressing these, but the resulting product would be notably inferior.

**Examples**:
- Anchor feature is at star 5 when star 7-8 is feasible
- Multiple user stories lack acceptance criteria
- Success metrics are vanity metrics with no business outcome connection
- Customer journey has a gap at a critical stage (e.g., no Activation flow)
- Feasibility concerns for a core feature not addressed

**Expected response**: Should be resolved before approval. May require a revision cycle.

### P2: Medium

**Criteria**: Improvement that elevates PRD quality but does not block development. Addressing these makes the product better; ignoring them produces an adequate product.

**Examples**:
- Supporting features could be elevated from star 5 to star 6
- Non-functional requirements (performance, accessibility) under-specified
- Competitive analysis missing or thin
- Error states and edge cases not fully covered
- Narrative flow between sections could be stronger

**Expected response**: Recommended for the current version. Can be deferred if timeline is tight.

### P3: Nice-to-Have

**Criteria**: Polish item that strengthens an already adequate section. These are improvements a senior PM would make but that do not change the product outcome significantly.

**Examples**:
- Glossary of domain terms would improve clarity
- Additional user persona would strengthen the narrative
- Visual wireframes would complement text descriptions
- Experimentation plan for a secondary feature
- Future vision section for v2+ capabilities

**Expected response**: Included in the review for completeness. Addressed if time permits.

---

## Suggestion Types

### Missing Content

**Definition**: A required section, feature, or detail is absent from the PRD.

**Identification signals**:
- Customer journey stage with no mapped features
- Standard PRD section not present (e.g., no success metrics, no technical considerations)
- User need identified in problem statement but no corresponding feature
- Implicit assumption that a capability exists when it does not

**Format**: "Section X is missing. It should include [specific content] because [reason tied to framework]."

### Ambiguity

**Definition**: Language in the PRD is open to multiple interpretations. Two engineers reading the same requirement could build different things.

**Identification signals**:
- Vague qualifiers: "intuitive," "fast," "user-friendly," "seamless," "easy"
- Unmeasurable criteria: "the system should be responsive"
- Undefined terms: domain-specific language without glossary
- Conflicting requirements across sections

**Format**: "Requirement Y uses the term '[vague term].' Define this with a measurable threshold (e.g., [specific suggestion]) to ensure consistent implementation."

### Ambition Gap

**Definition**: A feature targets star 4-5 when star 6-8 is feasible within the product's constraints. The feature meets expectations but does not differentiate.

**Identification signals**:
- Feature matches competitor implementations exactly
- No proactive or contextual behavior described
- Feature solves the stated problem but does not anticipate related needs
- Anchor feature is at the same star level as table-stakes features

**Format**: "Feature Z is currently at star [N]. To reach star [N+1-2], consider [specific enhancement]. This would [impact on user experience]. Feasibility: [assessment]."

### Metric Gap

**Definition**: Success metrics are missing, unmeasurable, or disconnected from business outcomes.

**Identification signals**:
- No metrics defined for a key feature
- Metrics measure activity (page views, clicks) rather than outcomes (retention, revenue, satisfaction)
- Metrics have no baseline or target values
- No leading indicators defined (only lagging indicators)
- No guardrail metrics to prevent over-optimization

**Format**: "Feature Z has no success metric. Recommend measuring [specific metric] with baseline [value] and target [value] because [connection to business outcome]."

### Story Quality Issue

**Definition**: The user journey is unclear, fragmented, or missing emotional arc. The PRD reads as a feature list rather than a narrative.

**Identification signals**:
- Features listed in no discernible order
- User stories that cannot be linked into a coherent journey
- No before/after comparison
- Missing user context (who is this person? what is their day like?)
- Requirements describe system behavior without user experience context

**Format**: "The PRD's narrative is fragmented at the [specific location]. Consider connecting features A and B by describing how the user transitions from [action] to [action], which would strengthen the Story Quality dimension."

---

## Star-Level Impact

Every suggestion should include the expected star-level improvement:

| Current Star | Suggestion Impact | Example |
|-------------|------------------|---------|
| Star 2 -> Star 5 | Quality fix | "Add error handling with helpful messages to make this feature functional" |
| Star 4 -> Star 5 | Polish | "Add keyboard shortcuts and accessibility labels to match competitor quality" |
| Star 5 -> Star 6 | Enhancement | "Add contextual suggestions based on user history instead of empty search" |
| Star 5 -> Star 7 | Differentiation | "Instead of showing raw data, synthesize an insight that tells the user something they did not know" |
| Star 5 -> Star 8 | Transformation | "Reframe from 'search for contacts' to 'relevant people appear automatically based on your current task'" |

---

## Suggestion Format

Each improvement suggestion follows this structure:

```
**ID**: [Sequential, e.g., IMP-001]
**PRD Section**: [Where in the PRD this applies]
**Priority**: [P0 / P1 / P2 / P3]
**Type**: [Missing content / Ambiguity / Ambition gap / Metric gap / Story quality issue]
**Current Star Level**: [1-11 or N/A if missing]
**Target Star Level**: [1-11]

**What to change**: [Specific, actionable description of the improvement]

**Why (framework rationale)**: [Which principle, dimension, or criterion supports this suggestion]

**Expected impact**: [How this improves the user experience and/or the scoring dimensions]
```

---

## Ordering Suggestions

Present suggestions in the review report in the following order:

1. **P0 suggestions** (all types) -- these must be addressed first
2. **P1 suggestions** ordered by star-level impact (highest delta first)
3. **P2 suggestions** ordered by type (ambition gaps first, then metric gaps, then others)
4. **P3 suggestions** grouped by PRD section

This ordering ensures the PRD author or `pm-prd-generator` addresses the most impactful improvements first.

---

## Rewrite Loop Integration

When suggestions feed back to `pm-prd-generator`, format them as a structured input:

1. **Overall verdict**: Approve / Minor revision / Major revision / Reject
2. **Overall score**: X.X/10 with dimension breakdown
3. **P0 items**: Must be addressed (listed with full detail)
4. **P1 items**: Should be addressed (listed with full detail)
5. **P2-P3 items**: May be addressed (listed as summary bullets)
6. **Anchor feature guidance**: Which features should be elevated and to what star level

The `pm-prd-generator` should process P0 items first, then P1, then P2-P3 if context budget allows.
