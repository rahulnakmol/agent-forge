# Prioritization Frameworks

## Why This Matters

Without a shared prioritization framework, every roadmap discussion becomes a battle of opinions, loudest voices, and HiPPO (Highest Paid Person's Opinion). A framework does not remove judgment -- it structures it so that tradeoffs are visible and decisions are repeatable.

## Framework Comparison

### RICE (Intercom)

**Formula**: (Reach x Impact x Confidence) / Effort

| Component | Definition | Scale |
|-----------|-----------|-------|
| Reach | How many customers will this affect in a given time period? | Absolute number (e.g., 500 users/quarter) |
| Impact | How much will it affect each person? | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| Confidence | How sure are we about these estimates? | 100% = high, 80% = medium, 50% = low |
| Effort | Person-months of work | Absolute number |

**Best for**: Data-rich teams that need cross-functional comparison across diverse initiatives.
**Strengths**: Forces quantification, comparable across teams, explicit confidence factor.
**Weaknesses**: Garbage-in-garbage-out -- bad Reach estimates produce bad scores. Teams learn to game Confidence ratings.

### ICE (Sean Ellis)

**Formula**: Impact x Confidence x Ease

| Component | Definition | Scale |
|-----------|-----------|-------|
| Impact | Expected effect on the target metric | 1-10 |
| Confidence | How sure are we? | 1-10 |
| Ease | How easy is this to implement? | 1-10 |

**Best for**: Growth teams, experiment prioritization, early-stage companies.
**Strengths**: Fast to score, low overhead, good for rapid experiment cycles.
**Weaknesses**: Subjective 1-10 scales invite inconsistency. No explicit Reach component.

### WSJF -- Weighted Shortest Job First (SAFe)

**Formula**: Cost of Delay / Job Duration

Cost of Delay = User/Business Value + Time Criticality + Risk Reduction/Opportunity Enablement

**Best for**: Enterprise teams, SAFe environments, deadline-driven work.
**Strengths**: Explicitly values time sensitivity. Prioritizes high-value, short-duration work.
**Weaknesses**: Complex to score. Cost of Delay is genuinely hard to estimate. Requires SAFe fluency.

### Kano Model

**Categories**: Must-Be / Performance / Attractive / Indifferent / Reverse

Not a scoring formula -- a categorization system. Map features to categories through customer research (surveys asking both functional and dysfunctional questions).

**Best for**: Feature satisfaction mapping, understanding which features drive delight vs. prevent churn.
**Strengths**: Grounded in customer perception, reveals non-obvious dynamics (attractive features that become must-be over time).
**Weaknesses**: Requires primary research to categorize correctly. Does not produce a ranked list.

### Cost of Delay

**Formula**: Quantify the economic cost of NOT doing something, per unit of time.

Three profiles:
- **Standard**: linear cost accumulation (most features)
- **Urgent**: exponential cost (compliance deadlines, security vulnerabilities)
- **Fixed date**: cliff function (trade shows, regulatory dates, partner launches)

**Best for**: Executive decision-making, comparing apples-to-oranges initiatives, communicating priority to stakeholders.
**Strengths**: Forces economic thinking. Makes delay visible as a cost, not just an opportunity.
**Weaknesses**: Hard to quantify accurately. Teams often handwave the numbers.

### Opportunity Scoring (Teresa Torres)

**Formula**: Plot features on Importance (x-axis) vs. Satisfaction (y-axis)

The opportunity space lives in the upper-left quadrant: high importance, low satisfaction. These are the underserved needs.

**Best for**: Discovery-driven teams, continuous discovery cadence, validating where to invest.
**Strengths**: Customer-grounded, visual, pairs naturally with continuous discovery habits.
**Weaknesses**: Requires ongoing customer research. Does not account for effort.

## Comparison Table

| Framework | Best For | Complexity | Data Needed | Team Size |
|-----------|----------|-----------|-------------|-----------|
| RICE | Cross-team comparison | Medium | Usage metrics, estimates | 10+ |
| ICE | Growth experiments | Low | Judgment calls | 3-10 |
| WSJF | Enterprise, SAFe | High | Value estimates, durations | 20+ |
| Kano | Feature satisfaction | Medium | Customer surveys | Any |
| Cost of Delay | Executive decisions | Medium-High | Revenue/cost data | Any |
| Opportunity Scoring | Discovery teams | Low-Medium | Customer interviews | 3-15 |

## Building a Custom Framework

If no standard framework fits, build your own scoring model:

1. **Define 3-5 scoring dimensions** relevant to your strategy (e.g., strategic alignment, revenue impact, customer urgency, technical risk, learning value)
2. **Weight the dimensions** based on current company priorities (weights should sum to 100%)
3. **Define clear scales** for each dimension (avoid 1-10 -- use 3-5 levels with written descriptions)
4. **Calibrate with examples** -- score 5-10 past initiatives to validate the model produces sensible rankings
5. **Review quarterly** -- adjust weights as strategy shifts

## The Cardinal Rule

**Pick ONE primary framework and use it consistently.** Do not mix RICE for some initiatives and ICE for others. Mixing frameworks makes comparison impossible and reintroduces the opinion-driven debates the framework was supposed to eliminate.

You may use a secondary framework for specific contexts (e.g., Kano for feature planning, RICE for roadmap prioritization), but every team member should know which framework is primary and how to apply it.

## When the Framework Says No

The hardest discipline is respecting the framework's output when it conflicts with your intuition. If the framework consistently produces rankings you override, either:
1. Your intuition is wrong and you should trust the data, or
2. The framework is miscalibrated and you should fix the inputs/weights

Do not maintain a framework you routinely ignore. That is worse than having no framework at all.
