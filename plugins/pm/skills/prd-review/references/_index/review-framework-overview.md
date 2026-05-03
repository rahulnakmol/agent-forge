# PRD Review Framework Overview

## Purpose

The PRD Quality Reviewer validates AI-generated and human-authored PRDs against a dual-assessment framework that combines qualitative experience analysis with quantitative scoring. The goal is to ensure every PRD aspires beyond functional adequacy toward genuine product differentiation.

## Dual-Assessment Model

The review framework operates on two parallel tracks that converge into a single review report:

### Track 1: Qualitative Assessment (11-Star Experience Framework)

Based on Brian Chesky's framework for designing exceptional experiences, the qualitative track maps every PRD feature onto an 11-point experience spectrum. This is not a score -- it is a diagnostic lens that reveals where a PRD's ambition sits relative to what is possible.

- **Stars 1-3**: Broken to clunky. Features are missing, hostile, or require painful workarounds.
- **Stars 4-5**: Baseline/parity. Features work well, meet spec, but are indistinguishable from competitors.
- **Stars 6-8**: The sweet spot. Features anticipate needs, create delight, or change how users think about the problem.
- **Stars 9-11**: Aspirational/magical. Used as thought exercises to challenge default thinking, not as literal targets.

The qualitative assessment traces the customer journey, identifies delight moments, and maps each feature to its star level.

### Track 2: Quantitative Assessment (7-Dimension Scoring Rubric)

The quantitative track evaluates the PRD across 7 weighted dimensions, producing a composite score on a 1-10 scale:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Completeness | 15% | All necessary sections present and populated |
| Clarity | 15% | Unambiguous language, testable requirements |
| Feasibility | 15% | Technically and organizationally achievable |
| Ambition | 15% | Pushes beyond table stakes toward differentiation |
| Differentiation | 15% | Distinct from competitors, defensible position |
| Metric Alignment | 10% | Success metrics tied to business outcomes |
| Story Quality | 15% | Narrative coherence, user journey readability |

## How Tracks Converge

The qualitative track informs the Ambition and Differentiation scores in the quantitative rubric. A PRD that scores 8/10 on Completeness but whose features all sit at 4-5 stars will receive a low Ambition score. Conversely, a PRD at 9-10 stars with no feasibility grounding will score low on Feasibility.

The final review report presents both tracks side by side: the star-level spectrum map alongside the dimension scores.

## Review vs Audit

A **review** is formative. It identifies what can be improved and provides specific, actionable suggestions with priority levels. The output feeds back into the PRD generation loop.

An **audit** is summative. It produces a pass/fail verdict against a fixed standard. This skill performs reviews, not audits.

## The Rewrite Loop

The review report is designed to feed directly back to `pm-prd-generator` for PRD revision:

1. `pm-prd-generator` produces a PRD
2. `pm-prd-reviewer` assesses the PRD and produces a review report
3. The review report's "Rewrite Recommendations" section provides structured input for `pm-prd-generator`
4. `pm-prd-generator` revises the PRD based on recommendations
5. Repeat until the PRD reaches an acceptable quality threshold (typically 7.5+ overall score)

## What Makes a Good PRD Review

A good review is:

- **Specific**: Points to exact PRD sections, not vague generalizations
- **Actionable**: Every criticism includes a concrete suggestion for improvement
- **Balanced**: Acknowledges strengths alongside weaknesses
- **Prioritized**: Distinguishes between critical gaps and nice-to-have improvements
- **Framework-grounded**: Every observation ties back to a star level or scoring dimension
- **Empathetic**: Assumes the PRD author made reasonable choices and explains why alternatives may be stronger
