# PRD Reviewer Quick Reference

## Workflow Phases

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | **Receive** | Ingest the PRD, identify format, confirm scope |
| 2 | **Assess** | Qualitative 11-star mapping + customer journey trace |
| 3 | **Score** | Quantitative 7-dimension scoring with weighted composite |
| 4 | **Recommend** | Prioritized improvement suggestions with star-level impact |
| 5 | **Report** | Consolidated review report with rewrite recommendations |

## 7 Scoring Dimensions

| Dimension | Weight | Quick Test |
|-----------|--------|------------|
| Completeness | 15% | Are all required PRD sections present and populated? |
| Clarity | 15% | Could an engineer implement from this without asking questions? |
| Feasibility | 15% | Can this be built with available resources and timeline? |
| Ambition | 15% | Does this go beyond what competitors already offer? |
| Differentiation | 15% | Would a user choose this over alternatives because of these features? |
| Metric Alignment | 10% | Are success metrics tied to business outcomes, not vanity metrics? |
| Story Quality | 15% | Can you narrate the user's journey from problem to resolution? |

## 11-Star Levels Summary

| Stars | Label | PRD Indicator |
|-------|-------|---------------|
| 1 | Broken/missing | Feature not addressed at all |
| 2 | Exists but hostile | Feature mentioned but UX is punishing |
| 3 | Works but clunky | Feature works with friction and workarounds |
| 4 | Meets minimum | Feature satisfies basic expectations |
| 5 | Works well / parity | Feature matches competitor baseline |
| 6 | Anticipates needs | Feature proactively addresses what user needs next |
| 7 | Wow moments | Feature makes users tell others about it |
| 8 | Changes thinking | Feature makes the old way feel broken |
| 9 | Feels like magic | Feature delivers eerily accurate predictions |
| 10 | 10x workflow | Feature transforms the entire workflow, not just the task |
| 11 | Problem vanishes | The problem ceases to exist entirely |

## Grade Thresholds

| Score | Verdict | Action |
|-------|---------|--------|
| < 4.0 | Reject | Fundamental rethink required |
| 4.0 - 5.9 | Major Revision | Significant gaps in multiple dimensions |
| 6.0 - 7.4 | Minor Revision | Solid foundation, targeted improvements needed |
| 7.5 - 8.9 | Approved with Notes | Strong PRD, minor refinements suggested |
| 9.0+ | Exemplary | Reference-quality PRD |

## Priority Categories

| Priority | Label | Criteria |
|----------|-------|----------|
| P0 | Critical | Blocks development or fundamentally misaligns with user needs |
| P1 | High | Significant quality gap that weakens the PRD materially |
| P2 | Medium | Improvement that elevates quality but is not blocking |
| P3 | Nice-to-have | Polish item that strengthens an already adequate section |

## Suggestion Types

- **Missing content**: Required section or detail absent from PRD
- **Ambiguity**: Language open to multiple interpretations
- **Ambition gap**: Feature targets 4-5 stars when 6-8 is feasible
- **Metric gap**: Success metric missing, unmeasurable, or vanity-driven
- **Story quality issue**: User journey unclear, fragmented, or missing emotional arc

## Reference Paths

| Category | Path |
|----------|------|
| Index | `references/_index/review-framework-overview.md` |
| Index | `references/_index/quick-reference.md` |
| 11-Star Framework | `references/eleven-star/framework-overview.md` |
| Star Levels 1-5 | `references/eleven-star/star-levels-1-to-5.md` |
| Star Levels 6-8 | `references/eleven-star/star-levels-6-to-8.md` |
| Star Levels 9-11 | `references/eleven-star/star-levels-9-to-11.md` |
| Sweet Spot Analysis | `references/eleven-star/sweet-spot-analysis.md` |
| Chesky Principles | `references/eleven-star/chesky-principles.md` |
| Qualitative Rubric | `references/scoring/qualitative-rubric.md` |
| Quantitative Rubric | `references/scoring/quantitative-rubric.md` |
| Scoring Calibration | `references/scoring/scoring-calibration.md` |
| Customer Journey | `references/methodology/customer-journey-analysis.md` |
| Feature Ambition | `references/methodology/feature-ambition-mapping.md` |
| Improvement Categories | `references/methodology/improvement-categorization.md` |
| Review Report Template | `references/templates/review-report-template.md` |
| Improvement Template | `references/templates/improvement-suggestions-template.md` |

## Chesky's 5 Principles (Review Lenses)

1. **Customer obsession** -- Does the PRD describe real human needs, not abstract personas?
2. **Do things that don't scale** -- Is the PRD optimizing for scale prematurely?
3. **Design the 11-star, work backward** -- Does the PRD show evidence of aspirational thinking?
4. **Storytelling** -- Can you narrate the user's journey end to end?
5. **Challenge the default** -- Does the PRD question "how it's always done"?
