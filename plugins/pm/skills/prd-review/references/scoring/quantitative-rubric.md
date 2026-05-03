# Quantitative Rubric: 7-Dimension Scoring

## Overview

The quantitative rubric evaluates a PRD across 7 weighted dimensions, producing a composite score on a 1-10 scale. Each dimension is scored independently, then combined using the weight formula to produce an overall grade.

**Formula**: Overall Score = Sum of (Dimension Score x Weight) for all 7 dimensions

---

## Dimension 1: Completeness (Weight: 15%)

**What it measures**: Whether all necessary PRD sections are present, populated with sufficient detail, and cover the full scope of the product.

### Scoring Scale

**1-3 (Weak)**:
- Multiple critical sections missing (no problem statement, no user stories, no success metrics)
- Sections present but contain placeholder text or single sentences
- Scope is undefined or contradictory
- No technical considerations, dependencies, or constraints mentioned
- Indicators: "TBD" markers, empty sections, missing entire categories of requirements

**4-6 (Adequate)**:
- All major sections present but some lack depth
- Problem statement exists but is vague or overly broad
- User stories exist but acceptance criteria are inconsistent
- Technical considerations mentioned but not detailed
- Success metrics defined but not all are measurable
- Indicators: Sections feel "checked off" rather than thoroughly considered

**7-8 (Strong)**:
- All sections present with substantive content
- Problem statement is specific, evidence-based, and scoped
- User stories have detailed acceptance criteria covering happy path and edge cases
- Technical architecture, dependencies, and constraints are documented
- Success metrics are measurable with defined targets and timelines
- Indicators: A developer could begin implementation from this document

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- Non-functional requirements fully specified (performance, security, accessibility, scalability)
- Competitive analysis included with specific feature comparisons
- Risk register with mitigation strategies
- Phased rollout plan with success criteria per phase
- Data migration, backward compatibility, and sunset plans if applicable
- Indicators: The PRD anticipates questions before they are asked

---

## Dimension 2: Clarity (Weight: 15%)

**What it measures**: Whether the PRD uses unambiguous language, defines terms precisely, and produces requirements that can be implemented without interpretation.

### Scoring Scale

**1-3 (Weak)**:
- Frequent use of vague terms ("intuitive," "fast," "user-friendly," "seamless") without definition
- Requirements open to multiple interpretations
- Inconsistent terminology (same concept referred to by different names)
- No glossary for domain-specific terms
- Indicators: Two engineers reading the same requirement would build different things

**4-6 (Adequate)**:
- Most requirements are clear but some contain ambiguity
- Occasional vague qualifiers remain ("should be responsive," "needs to be quick")
- Terminology is mostly consistent with minor lapses
- Some requirements are testable, others are aspirational statements
- Indicators: Engineers would need 2-3 clarification conversations to begin work

**7-8 (Strong)**:
- Requirements are specific and testable ("page loads in under 2 seconds on 3G connection")
- Consistent terminology throughout with glossary for domain terms
- Acceptance criteria use Given/When/Then or equivalent structured format
- No ambiguous qualifiers -- every adjective has a measurable definition
- Indicators: Engineers could write test cases directly from the PRD

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- Requirements are traceable (each links to a user need and a success metric)
- Decision log explains why specific approaches were chosen over alternatives
- Diagrams, wireframes, or flow charts supplement text for complex interactions
- Edge cases and error states are described with the same precision as happy paths
- Indicators: The PRD could serve as a test plan with minimal additional work

---

## Dimension 3: Feasibility (Weight: 15%)

**What it measures**: Whether the PRD's requirements can be built with available technology, team capability, budget, and timeline.

### Scoring Scale

**1-3 (Weak)**:
- Requirements assume technology that does not exist or is unproven
- Timeline is wildly unrealistic for the scope described
- No consideration of team size, skills, or availability
- Dependencies on external systems or partners not acknowledged
- Indicators: "AI will automatically..." without specifying approach; scope that would take 10 engineers 12 months assigned to 2 engineers for 3 months

**4-6 (Adequate)**:
- Requirements are technically possible but timeline or resources may be tight
- Some features assume capabilities the team has not demonstrated
- Dependencies identified but integration complexity underestimated
- Performance targets stated but not validated against architecture
- Indicators: Achievable with scope reduction or timeline extension

**7-8 (Strong)**:
- Requirements align with proven technology and team capabilities
- Timeline includes buffer for unknowns and integration challenges
- Dependencies are documented with contingency plans
- Performance targets are validated against proposed architecture
- Phased delivery plan manages risk through incremental release
- Indicators: Engineering team would assess this as "ambitious but achievable"

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- Proof-of-concept or prototype evidence for novel capabilities
- Explicit trade-off documentation (what was descoped and why)
- Resource plan with skill gap analysis and mitigation
- Rollback and fallback strategies for high-risk features
- Indicators: Engineering, design, and product all agree the plan is credible

---

## Dimension 4: Ambition (Weight: 15%)

**What it measures**: Whether the PRD pushes beyond functional parity toward genuine innovation. Informed by the 11-star qualitative assessment.

### Scoring Scale

**1-3 (Weak)**:
- Every feature replicates what competitors already offer
- No vision beyond "match the market"
- User stories describe existing workflows with no improvement
- No evidence of aspirational thinking or backward design
- Indicators: The PRD could be retitled with a competitor's name and still make sense

**4-6 (Adequate)**:
- Most features are at parity with some incremental improvements
- One or two features show creative thinking but are not fully developed
- Vision statement exists but is generic ("best-in-class," "industry-leading")
- Indicators: The product would be slightly better than alternatives in specific areas

**7-8 (Strong)**:
- 1-2 anchor features clearly differentiate from competitors (star 7-8)
- Evidence of 11-star backward design (ambitious vision grounded to feasible scope)
- Features that anticipate user needs, not just respond to them
- Vision articulates how the product changes the user's world
- Indicators: A prospective user would say "I haven't seen this before" about at least one feature

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- The PRD reframes the problem space itself (not just better solutions to the same problem)
- Multiple features at star 7-8 with clear differentiation narrative
- Future vision section showing how v1 features evolve toward star 8-9
- Indicators: The PRD makes reviewers question assumptions about the product category

---

## Dimension 5: Differentiation (Weight: 15%)

**What it measures**: Whether the product described would occupy a distinct market position and whether users would choose it specifically for its unique qualities.

### Scoring Scale

**1-3 (Weak)**:
- No competitive analysis or positioning
- Features are commodity (available everywhere)
- No unique value proposition articulated
- Target audience is "everyone" with no segmentation
- Indicators: Users would choose this product only if it were cheaper

**4-6 (Adequate)**:
- Competitive landscape acknowledged but differentiation is thin
- Value proposition exists but relies on generic advantages ("faster," "easier")
- Target audience defined but not specifically served
- Indicators: Users might choose this product but would not strongly recommend it

**7-8 (Strong)**:
- Clear competitive positioning with specific, defensible advantages
- Value proposition addresses needs competitors do not
- Target audience is specific and the product is designed around their context
- Features create switching costs through unique capabilities, not lock-in
- Indicators: Users would specifically recommend this product for its unique strengths

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- The product creates a new category or redefines an existing one
- Defensible moats (network effects, data advantages, proprietary methodology)
- The differentiation compounds over time (the product gets more unique with use)
- Indicators: Competitors would need to fundamentally rethink their approach to match

---

## Dimension 6: Metric Alignment (Weight: 10%)

**What it measures**: Whether success metrics are defined, measurable, tied to business outcomes, and connected to specific features.

### Scoring Scale

**1-3 (Weak)**:
- No success metrics defined
- Metrics are vanity metrics (page views, sign-ups) with no business outcome connection
- No baseline or target values
- Indicators: "We will track usage" without specifying what constitutes success

**4-6 (Adequate)**:
- Success metrics exist but are a mix of meaningful and vanity metrics
- Some metrics have targets but no timelines
- Metrics are defined at the product level but not traced to specific features
- Indicators: You can tell if the product is "used" but not if it is "successful"

**7-8 (Strong)**:
- Metrics tied to business outcomes (revenue, retention, efficiency, satisfaction)
- Each key feature has associated metrics with baselines, targets, and timelines
- Leading and lagging indicators are distinguished
- Measurement methodology is specified (how data will be collected)
- Indicators: You can definitively answer "was this feature worth building?" after launch

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- Metrics form a hierarchy (input metrics drive output metrics drive business outcomes)
- Guardrail metrics prevent optimization of one metric at the expense of others
- Experimentation plan defined (A/B test methodology for key features)
- Indicators: The metrics framework could run as an automated health dashboard

---

## Dimension 7: Story Quality (Weight: 15%)

**What it measures**: Whether the PRD tells a coherent narrative, whether the user journey is traceable, and whether the document reads as a strategy rather than a feature list.

### Scoring Scale

**1-3 (Weak)**:
- PRD is a disconnected feature list with no narrative thread
- No user journey visible -- features exist in isolation
- No before/after comparison showing the product's impact
- Problem statement is abstract or missing
- Indicators: Features could be reordered randomly without affecting comprehension

**4-6 (Adequate)**:
- Problem statement and user stories provide some narrative structure
- User journey is partially visible but has gaps between stages
- Features are grouped logically but do not flow as a story
- Indicators: You understand what the product does but not why it matters

**7-8 (Strong)**:
- Clear narrative arc: problem -> discovery -> first value -> deepening -> mastery
- User journey is traceable end to end with no gaps
- Before/after comparison is compelling and specific
- The reader can empathize with the user's situation and visualize the solution
- Indicators: A non-technical stakeholder could read this and be genuinely excited

**9-10 (Exceptional)**:
- Everything in 7-8, plus:
- The PRD tells a story that inspires action, not just understanding
- Multiple user personas are woven into a coherent narrative
- The document itself is a pleasure to read -- well-structured, concise, vivid
- Indicators: You would use this PRD as an example for training other product managers

---

## Calculating the Overall Score

### Step 1: Score Each Dimension (1-10)

Assign a score to each dimension based on the rubric above.

### Step 2: Apply Weights

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.15 | _/10 | _ |
| Clarity | 0.15 | _/10 | _ |
| Feasibility | 0.15 | _/10 | _ |
| Ambition | 0.15 | _/10 | _ |
| Differentiation | 0.15 | _/10 | _ |
| Metric Alignment | 0.10 | _/10 | _ |
| Story Quality | 0.15 | _/10 | _ |
| **Overall** | **1.00** | | **_/10** |

### Step 3: Determine Grade

| Overall Score | Grade | Verdict |
|--------------|-------|---------|
| < 4.0 | F | **Reject** -- Fundamental rethink required. PRD does not meet minimum quality threshold. |
| 4.0 - 5.9 | D | **Major Revision** -- Significant gaps in multiple dimensions. Return to pm-prd-generator with detailed recommendations. |
| 6.0 - 7.4 | C+ / B | **Minor Revision** -- Solid foundation with targeted improvements needed. Specify exactly which dimensions need work. |
| 7.5 - 8.9 | A- / A | **Approved with Notes** -- Strong PRD with minor refinements. List specific suggestions as P2/P3 priority. |
| 9.0+ | A+ | **Exemplary** -- Reference-quality PRD. Document what makes it exceptional for calibration purposes. |
