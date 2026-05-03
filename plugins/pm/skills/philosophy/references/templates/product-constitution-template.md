# Product Constitution Template

This template provides the structure for both the compact summary file and the seven detailed section files. Fill in the placeholders, remove the instructional comments, and adapt to your product.

---

## Part A: Compact Summary Template

**File**: `product-constitution.md`

This is the single-page overview that every team member reads. Keep each section to 1-2 sentences.

```markdown
# Product Constitution: {Product Name}

_Version {X.Y} | Last updated: {YYYY-MM-DD} | Next review: {YYYY-MM-DD}_

## Product Principles
{1-2 sentence summary of each principle, e.g., "We prioritize craft over speed -- we ship fewer things but ship them exceptionally well. We design for first use, not expert use."}

## Core Value Propositions
{1-2 sentence summary of value delivered and to whom, e.g., "We help early-stage engineering teams ship production-ready infrastructure in hours instead of weeks, eliminating the need for dedicated DevOps hires."}

## Product Positioning
{1-2 sentence positioning statement, e.g., "For startup engineering leads who need production infrastructure without a platform team, InfraKit is a deployment platform that eliminates ops complexity. Unlike AWS/GCP consoles or Terraform, we provide opinionated defaults that just work."}

## Customer Experience Philosophy
{1-2 sentence CX quality bar and star level target, e.g., "We target 7-star experiences on first-time setup and core deployment workflows, with a hard floor of 5 stars on everything we ship. We design for reliability first, delight second."}

## Product Building Approach
{1-2 sentence methodology and quality summary, e.g., "We run 6-week Shape Up cycles with 2-week cool-downs. Every PR requires tests for business logic, one approval, and passes CI. We reserve 20% of each cycle for tech debt."}

## Prioritization Framework
{1-2 sentence framework name and key criteria, e.g., "We use RICE as our primary framework, scored quarterly during roadmap planning. Cost of Delay is used for time-sensitive escalations."}

## Product Research Bets
{1-2 sentence current bet portfolio summary, e.g., "Three active bets this quarter: enterprise SSO (high conviction, executing), AI-assisted config (medium conviction, validating), marketplace integrations (low conviction, exploring)."}

---
_Section details: `constitution/{section-name}.md` | Review cadence: quarterly_
```

---

## Part B: Section File Templates

Each section file lives in `constitution/` and contains the full detail behind the compact summary.

---

### Section 1: Product Principles

**File**: `constitution/product-principles.md`

```markdown
# Product Principles

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Principle 1: {Name}

**Statement**: {One sentence declaring the stance}

**This means we...**
- {Concrete behavior or decision 1}
- {Concrete behavior or decision 2}
- {Concrete behavior or decision 3}

**This means we don't...**
- {Explicitly rejected behavior 1}
- {Explicitly rejected behavior 2}
- {Explicitly rejected behavior 3}

## Principle 2: {Name}

**Statement**: {One sentence declaring the stance}

**This means we...**
- {Concrete behavior 1}
- {Concrete behavior 2}

**This means we don't...**
- {Rejected behavior 1}
- {Rejected behavior 2}

<!-- Repeat for up to 5 principles. No more than 5. -->

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```

---

### Section 2: Core Value Propositions

**File**: `constitution/value-propositions.md`

```markdown
# Core Value Propositions

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Value Proposition 1: {Short label}

**For** {target customer segment}
**who need to** {job-to-be-done}
**our product** {product name}
**delivers** {key outcome / benefit}
**unlike** {primary alternative}
**because** {unique differentiator}

**Primary segment**: {Segment name}
**Primary job type**: Functional / Emotional / Social
**Validation status**: Validated / Assumed / Testing

## Value Proposition 2: {Short label}

<!-- Same structure as VP1 -->

## Value Proposition Map

| Value Proposition | Primary Segment | Primary Job | Validation Status |
|-------------------|----------------|-------------|-------------------|
| {VP1} | {Segment} | {Job} | {Status} |
| {VP2} | {Segment} | {Job} | {Status} |

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```

---

### Section 3: Product Positioning

**File**: `constitution/positioning.md`

```markdown
# Product Positioning

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Positioning Statement

For {target segment} who {situation/need}, {product} is a {market category} that {key benefit}. Unlike {competitive alternative}, we {primary differentiator}.

## Competitive Alternatives
| Alternative | Type | Why customers use it | Our advantage |
|-------------|------|---------------------|---------------|
| {name} | Direct / Indirect / Status quo | {reason} | {differentiator} |

## Unique Attributes
| Attribute | Value ("so what?") | Evidence |
|-----------|-------------------|----------|
| {attribute} | {customer outcome} | {proof point} |

## Target Segment Profile
- **Who**: {description}
- **Size**: {estimated market}
- **Why they care most**: {connection to our unique value}
- **Where to find them**: {channels}

## Market Category
- **Category**: {name}
- **Strategy**: Compete in existing / Create new
- **Category expectations (table stakes)**: {what customers expect from this category}

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```

---

### Section 4: Customer Experience Philosophy

**File**: `constitution/cx-philosophy.md`

```markdown
# Customer Experience Philosophy

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Star Level Targets

| Journey Stage | Target Stars | Rationale |
|---------------|-------------|-----------|
| First-time experience | {X} | {why} |
| Core workflow | {X} | {why} |
| Edge cases / admin | {X} | {why} |
| Error recovery | {X} | {why} |

**Hard floor**: No feature ships below {X} stars.

## Primary CX Orientation
{Delight-first / Reliability-first} -- {1-2 sentence rationale}

## Kano Feature Map

| Feature Area | Category | Investment Level |
|-------------|----------|-----------------|
| {feature} | Must-Be / Performance / Attractive | {High/Med/Low} |

## Journey Investment Priority
1. **Primary**: {Acquisition / Activation / Retention / Advocacy} -- {why}
2. **Secondary**: {stage} -- {why}

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```

---

### Section 5: Product Building Approach

**File**: `constitution/building-approach.md`

```markdown
# Product Building Approach

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Methodology
{Scrum / Kanban / Shape Up / Custom} -- {1-2 sentence rationale}

### Ceremonies
| Ceremony | Frequency | Purpose | Attendees |
|----------|-----------|---------|-----------|
| {name} | {cadence} | {why} | {who} |

## Quality Bar
- **Testing**: {what is required before merge}
- **Code review**: {approval requirements}
- **Accessibility**: {WCAG level and enforcement}
- **Performance**: {load time / response time budgets}

## Craft Standards
- **Friction logging**: {yes/no, cadence}
- **Dogfooding**: {practice and feedback loop}
- **Design review**: {blocking/advisory, who decides}

## Release Philosophy
{Continuous deployment / Release trains / Hybrid} -- {details}
- **Feature flags**: {yes/no, tool, when to use}
- **Rollout strategy**: {canary / percentage / instant}

## Tech Debt Approach
{Percentage allocation / Dedicated sprints / Continuous refactoring}
- **Current allocation**: {X% or cadence}
- **Tracking**: {how debt is tracked and prioritized}

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```

---

### Section 6: Prioritization Framework

**File**: `constitution/prioritization.md`

```markdown
# Prioritization Framework

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Primary Framework
**{Framework name}** (e.g., RICE, ICE, WSJF, Opportunity Scoring)

### How We Score
| Component | Definition | Scale |
|-----------|-----------|-------|
| {component} | {what it measures} | {how scored} |

### Scoring Cadence
{When and how often items are scored -- e.g., "quarterly during roadmap planning, ad-hoc for urgent requests"}

## Secondary Framework (if any)
**{Framework name}** -- used for {specific context}

## Decision Rules
- Items scoring above {X} are auto-approved for the next cycle
- Items scoring below {Y} are deferred unless escalated
- Ties are broken by {criterion}
- Framework overrides require {who} approval with documented rationale

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```

---

### Section 7: Product Research Bets

**File**: `constitution/research-bets.md`

```markdown
# Product Research Bets

_Last reviewed: {YYYY-MM-DD} | Version: {X.Y} | Owner: {name/role}_

## Portfolio Summary

| Conviction | Target % | Actual % | # of Bets |
|------------|---------|---------|-----------|
| High (70%+) | 60-70% | {X}% | {N} |
| Medium (40-70%) | 20-30% | {X}% | {N} |
| Low (<40%) | 5-10% | {X}% | {N} |

## Active Bets

### Bet 1: {Name}

| Field | Detail |
|-------|--------|
| **Status** | Active / Validating / Validated / Invalidated / Paused |
| **Conviction** | High / Medium / Low |
| **DIBB** | Data: {observation} / Insight: {interpretation} / Belief: {hypothesis} |
| **Thesis** | {One sentence} |
| **Success criteria** | {Measurable outcome} |
| **Time box** | {Start date} - {Evaluation date} |
| **Kill criteria** | {What would cause early abandonment} |
| **Owner** | {Name/role} |

### Bet 2: {Name}

<!-- Same structure -->

## Recently Closed Bets

| Bet | Outcome | Key Learning | Date Closed |
|-----|---------|-------------|-------------|
| {name} | Validated / Invalidated | {what we learned} | {date} |

## Next Review Date
{YYYY-MM-DD} -- {quarterly review cadence}

---

### Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| {date} | {ver} | {description} | {who} |
```
