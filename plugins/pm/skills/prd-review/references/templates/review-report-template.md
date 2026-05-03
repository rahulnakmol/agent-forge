# PRD Review Report Template

Use this template to produce the final review report. Fill every section. If a section is not applicable, state why.

---

## Section 1: Executive Summary

```
# PRD Review Report: [Product Name]

**Reviewed**: [Date]
**PRD Version**: [Version or identifier]
**Reviewer**: pm-prd-reviewer (11-Star Experience Framework)

## Executive Summary

**Overall Score**: [X.X / 10]
**Grade**: [F / D / C+ / B / A- / A / A+]
**Verdict**: [Reject / Major Revision / Minor Revision / Approved with Notes / Exemplary]

### Key Findings
1. [Most important finding -- typically the anchor feature assessment]
2. [Second most important finding -- typically a critical gap or strength]
3. [Third finding -- pattern observation across the PRD]

### Recommendation
[One paragraph: What should happen next? If revision needed, summarize the top 3 changes.
If approved, note what makes it strong and what minor refinements would elevate it further.]
```

---

## Section 2: 11-Star Spectrum Map

```
## 11-Star Spectrum Map

| Feature | Star Level | Classification | Notes |
|---------|-----------|---------------|-------|
| [Feature A] | [N] | Table stakes | [One-line justification] |
| [Feature B] | [N] | Enhanced | [One-line justification] |
| [Feature C] | [N] | Anchor | [One-line justification] |
| ... | | | |

### Distribution
- Stars 1-3 (Broken/Clunky): [count] features
- Stars 4-5 (Baseline/Parity): [count] features
- Stars 6-8 (Sweet Spot): [count] features
- Stars 9-11 (Aspirational): [count] features

### Cluster Pattern
[Which pattern from feature-ambition-mapping.md does this PRD match?
5-Star Cluster / Balanced Portfolio / Ambition Cluster / Bimodal Split / Flat Line]

### Anchor Feature Assessment
- **Identified anchors**: [Feature names]
- **Current star level**: [N]
- **Target star level**: [N] (feasible sweet spot)
- **Gap assessment**: [What would it take to reach the target?]
```

---

## Section 3: Quantitative Scores

```
## Quantitative Assessment

| Dimension | Weight | Score | Weighted | Key Observation |
|-----------|--------|-------|----------|-----------------|
| Completeness | 15% | [N]/10 | [N.NN] | [One-line observation] |
| Clarity | 15% | [N]/10 | [N.NN] | [One-line observation] |
| Feasibility | 15% | [N]/10 | [N.NN] | [One-line observation] |
| Ambition | 15% | [N]/10 | [N.NN] | [One-line observation] |
| Differentiation | 15% | [N]/10 | [N.NN] | [One-line observation] |
| Metric Alignment | 10% | [N]/10 | [N.NN] | [One-line observation] |
| Story Quality | 15% | [N]/10 | [N.NN] | [One-line observation] |
| **Overall** | **100%** | | **[N.NN]** | |

### Dimension Highlights
**Strongest dimension**: [Name] ([N]/10) -- [Why this dimension scored well]
**Weakest dimension**: [Name] ([N]/10) -- [Why this dimension scored low and what would improve it]
```

---

## Section 4: Qualitative Assessment

```
## Qualitative Assessment

### Customer Journey Analysis

| Journey Stage | Features Mapped | Coverage | Star Range | Assessment |
|--------------|----------------|----------|------------|------------|
| Awareness | [Features or "None"] | [Full/Partial/Gap] | [N-N] | [Assessment] |
| Consideration | [Features or "None"] | [Full/Partial/Gap] | [N-N] | [Assessment] |
| Activation | [Features or "None"] | [Full/Partial/Gap] | [N-N] | [Assessment] |
| Retention | [Features or "None"] | [Full/Partial/Gap] | [N-N] | [Assessment] |
| Expansion | [Features or "None"] | [Full/Partial/Gap] | [N-N] | [Assessment] |
| Advocacy | [Features or "None"] | [Full/Partial/Gap] | [N-N] | [Assessment] |

**Journey gaps**: [List stages with no or insufficient coverage]
**Over-indexing**: [List stages with disproportionate feature density]
**Narrative coherence**: [Can the journey be read as a continuous story? Where does it break?]

### Delight Moments

**Existing delight moments**:
1. [Feature and what makes it delightful]
2. [...]

**Missing delight opportunities**:
1. [Journey stage + what a delight moment could look like]
2. [...]

### Chesky Principles Assessment

| Principle | Rating | Evidence |
|-----------|--------|----------|
| Customer Obsession | [Strong/Adequate/Weak] | [Specific evidence from PRD] |
| Do Things That Don't Scale | [Strong/Adequate/Weak] | [Specific evidence from PRD] |
| 11-Star Backward Design | [Strong/Adequate/Weak] | [Specific evidence from PRD] |
| Storytelling | [Strong/Adequate/Weak] | [Specific evidence from PRD] |
| Challenge the Default | [Strong/Adequate/Weak] | [Specific evidence from PRD] |
```

---

## Section 5: Improvement Suggestions

```
## Improvement Suggestions

### P0: Critical ([count] items)

**IMP-001**: [Title]
- **PRD Section**: [Section reference]
- **Type**: [Missing content / Ambiguity / Ambition gap / Metric gap / Story quality]
- **Current -> Target Star**: [N -> N]
- **What**: [Specific change needed]
- **Why**: [Framework rationale]
- **Impact**: [Expected improvement]

[Repeat for each P0 item]

### P1: High ([count] items)

[Same format as P0]

### P2: Medium ([count] items)

[Same format, may be abbreviated]

### P3: Nice-to-Have ([count] items)

[Summary bullets, one per item]
```

---

## Section 6: Rewrite Recommendations

```
## Rewrite Recommendations

**For pm-prd-generator rewrite loop**:

### Priority Actions (must address)
1. [P0 item summary with specific guidance]
2. [P0 item summary with specific guidance]

### Recommended Actions (should address)
1. [P1 item summary with specific guidance]
2. [P1 item summary with specific guidance]

### Anchor Feature Elevation
- **Feature**: [Name]
- **Current star**: [N]
- **Target star**: [N]
- **How to elevate**: [Specific guidance -- what the feature should do differently]
- **Example of target experience**: [Concrete scenario at the target star level]

### Scoring Targets for Revision
| Dimension | Current | Target | Key Change Needed |
|-----------|---------|--------|-------------------|
| [Weakest dimension] | [N]/10 | [N]/10 | [Specific action] |
| [Second weakest] | [N]/10 | [N]/10 | [Specific action] |

### Revision Success Criteria
The revised PRD should achieve:
- Overall score >= [target, typically 7.5]
- No dimension below [floor, typically 6.0]
- Anchor feature at star [target, typically 7-8]
- All P0 items resolved
```
