# Improvement Suggestions Template

## Per-Suggestion Structure

Use this template for every improvement suggestion in the review report. All fields are required.

```
---

### IMP-[NNN]: [Short descriptive title]

**PRD Section**: [Exact section name or path in the PRD being reviewed]
**Priority**: [P0 / P1 / P2 / P3]
**Type**: [Missing content / Ambiguity / Ambition gap / Metric gap / Story quality issue]
**Current Star Level**: [1-11, or "N/A" if the feature/section is missing entirely]
**Target Star Level**: [1-11]

**Description**:
[2-4 sentences describing exactly what needs to change. Be specific enough that the
PRD author could implement this suggestion without asking clarifying questions.]

**Rationale**:
[Which framework principle, scoring dimension, or review criterion supports this
suggestion. Reference specific elements: "Per the Clarity dimension, requirements
should be testable..." or "Per Chesky's customer obsession principle, user needs
should be grounded in evidence..."]

**Expected Impact**:
[How this suggestion improves the PRD. Reference both the star-level change and
the scoring dimension(s) affected. Example: "Elevates feature from star 5 to star 6.
Improves Ambition score by approximately +1 point and Differentiation by +0.5."]

---
```

## Batch Summary Template

When generating the full list of suggestions for the review report, use this summary format at the top:

```
## Improvement Summary

| ID | Title | Priority | Type | Star Change | Dimensions Affected |
|----|-------|----------|------|-------------|-------------------|
| IMP-001 | [Title] | P0 | [Type] | [N -> N] | [Dims] |
| IMP-002 | [Title] | P1 | [Type] | [N -> N] | [Dims] |
| IMP-003 | [Title] | P2 | [Type] | [N -> N] | [Dims] |
| ... | | | | | |

**Total suggestions**: [N]
**By priority**: P0: [N] | P1: [N] | P2: [N] | P3: [N]
**By type**: Missing: [N] | Ambiguity: [N] | Ambition gap: [N] | Metric gap: [N] | Story: [N]
**Estimated score impact if all addressed**: [Current] -> [Projected]
```

## Examples

### Example P0: Missing Content

```
### IMP-001: Add error handling for receipt OCR failure

**PRD Section**: Feature 1 -- Receipt Capture
**Priority**: P0
**Type**: Missing content
**Current Star Level**: N/A (not addressed)
**Target Star Level**: 5

**Description**:
The receipt capture feature describes the happy path (OCR successfully extracts data)
but does not address what happens when OCR fails. Given that OCR accuracy is targeted
at 95%, 1 in 20 receipts will fail. The PRD must specify the fallback experience:
manual entry form pre-populated with any partial data extracted, option to retake the
photo with guidance on lighting/angle, and graceful error messaging that does not blame
the user.

**Rationale**:
Per the Completeness dimension, a feature without error handling is incomplete.
Per Chesky's customer obsession principle, the 5% failure case is where user trust is
won or lost. A hostile error experience at this point would drop the feature from
star 5 to star 2.

**Expected Impact**:
Prevents star-level regression from 5 to 2 in failure scenarios. Improves Completeness
score by approximately +1 point. Addresses a critical UX risk that would generate
negative user sentiment.
```

### Example P1: Ambition Gap

```
### IMP-004: Elevate dashboard from data display to insight synthesis

**PRD Section**: Feature 5 -- Analytics Dashboard
**Priority**: P1
**Type**: Ambition gap
**Current Star Level**: 5
**Target Star Level**: 7

**Description**:
The dashboard currently displays charts of expense data (spend by category, trend over
time, top vendors). This matches every competitor. To differentiate, the dashboard
should synthesize insights: "Your team's travel spend increased 34% this quarter,
driven by 3 reps attending the same conference separately. Coordinating attendance
could save $12,400 next quarter." Move from showing data to telling stories with
the data.

**Rationale**:
Per the 11-star framework, star 5 features display information while star 7 features
create moments users share with others. Per Chesky's challenge-the-default principle,
the assumption that "dashboards show charts" should be questioned. Per the
Differentiation dimension, data display is commodity while insight synthesis is
defensible.

**Expected Impact**:
Elevates the analytics feature from star 5 to star 7, creating a potential anchor
feature. Improves Ambition score by +1.5, Differentiation by +1, and Story Quality
by +0.5. This could become the feature users describe when recommending the product.
```

### Example P2: Ambiguity

```
### IMP-007: Define "responsive" with specific performance thresholds

**PRD Section**: Non-Functional Requirements
**Priority**: P2
**Type**: Ambiguity
**Current Star Level**: 5
**Target Star Level**: 5 (no star change; clarity improvement)

**Description**:
The NFR section states "the application should be responsive." Define this with
specific thresholds: page load < 2 seconds on 4G, interaction response < 200ms,
search results < 1 second for datasets up to 10,000 records. Specify measurement
methodology (Lighthouse score, p95 latency, synthetic monitoring).

**Rationale**:
Per the Clarity dimension, "responsive" is a vague qualifier that two engineers
would interpret differently. One might target 500ms, another 5 seconds. Specific
thresholds enable testable acceptance criteria and prevent post-launch disputes
about whether the requirement was met.

**Expected Impact**:
No star-level change (this is a clarity improvement, not an ambition improvement).
Improves Clarity score by approximately +0.5 points. Prevents implementation
ambiguity that could lead to rework.
```

### Example P3: Nice-to-Have

```
### IMP-012: Add glossary of expense management domain terms

**PRD Section**: Document-wide
**Priority**: P3
**Type**: Story quality issue
**Current Star Level**: N/A
**Target Star Level**: N/A

**Description**:
The PRD uses several domain-specific terms (per diem, T&E policy, GL code, cost center
allocation) without definition. A glossary section would improve accessibility for
engineering team members who may not have finance domain expertise.

**Rationale**:
Per the Clarity dimension, domain terms should be defined to prevent misinterpretation.
This is a polish item -- the terms are likely understood by the immediate team but a
glossary future-proofs the document for new team members or cross-functional reviewers.

**Expected Impact**:
Marginal improvement to Clarity score (+0.25). Improves document accessibility
and reduces onboarding time for new team members reading the PRD.
```

## Ordering Rules

Present suggestions in the review report using this order:

1. All P0 suggestions, ordered by type: Missing content > Ambiguity > Ambition gap > Metric gap > Story quality
2. All P1 suggestions, ordered by star-level delta (largest improvement first)
3. All P2 suggestions, ordered by type
4. All P3 suggestions, grouped by PRD section

Within the same priority and type, order by the scoring dimension most affected (highest-weight dimension first).
