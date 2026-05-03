# Research Bets Guide

## What Are Product Research Bets?

Research bets are the explicit hypotheses your team is investing in -- the things you believe might be true and are willing to spend resources to validate. They represent the frontier of your product strategy: not what you know works, but what you think could work.

## Spotify DIBB Framework

Spotify's DIBB framework provides a structured path from observation to action:

**Data**: What have we observed? Raw facts, metrics, signals from the market or customers.
- Example: "40% of new users drop off during onboarding before completing setup."

**Insight**: What does the data mean? Interpretation that connects observations to understanding.
- Example: "Our onboarding asks for too much information upfront. Users want to see value before investing effort."

**Belief**: What do we now believe to be true? The hypothesis formed from the insight.
- Example: "If we let users experience the core product before completing setup, activation will increase significantly."

**Bet**: What are we going to do about it? The investment decision, with clear scope and success criteria.
- Example: "We will build a guided demo mode that lets users try the product with sample data before creating an account. Success: 25% improvement in Day-1 activation."

Every bet should trace back through this chain. If you cannot articulate the Data and Insight behind a Bet, you are guessing, not betting.

## Conviction Levels

Not all bets deserve equal investment. Categorize by conviction:

### High Conviction (70%+ confident)

You have strong evidence this will work. Multiple data points, customer validation, competitive proof.

**Action**: Bet big. Dedicate a full team. Set ambitious timelines. This is execution, not experimentation.

**Time horizon**: This quarter. Ship it.

### Medium Conviction (40-70% confident)

You have suggestive evidence but meaningful uncertainty. Some positive signals, but key assumptions are untested.

**Action**: Run a structured experiment. Define a hypothesis, success criteria, and time box. Allocate a small team or a portion of a team's capacity.

**Time horizon**: 2-6 weeks to validate, then decide to promote to High or kill.

### Low Conviction (<40% confident)

You have a hunch, an interesting signal, or a provocative idea. Limited evidence.

**Action**: Explore cheaply. Prototype, fake-door test, customer interview spike, competitive analysis. Spend days, not weeks.

**Time horizon**: 1-2 weeks to generate enough signal to either promote to Medium or discard.

## Bet Portfolio Balance

A healthy product team maintains a portfolio across conviction levels:

| Conviction | % of Capacity | Purpose |
|------------|--------------|---------|
| High | 60-70% | Reliable delivery, predictable outcomes |
| Medium | 20-30% | Structured learning, pipeline for future High bets |
| Low | 5-10% | Exploration, option creation, innovation pipeline |

If 100% of your capacity is on High-conviction bets, you are optimizing the present at the expense of the future. If more than 20% is on Low-conviction bets, you are exploring instead of shipping.

## Teresa Torres' Opportunity Solution Tree

The OST provides a visual framework for connecting bets to outcomes:

```
Desired Outcome
    |
    +-- Opportunity A
    |       +-- Solution 1 --> Experiment 1a, 1b
    |       +-- Solution 2 --> Experiment 2a
    |
    +-- Opportunity B
    |       +-- Solution 3 --> Experiment 3a
    |       +-- Solution 4 --> Experiment 4a, 4b
    |
    +-- Opportunity C
            +-- Solution 5 --> Experiment 5a
```

Key rules:
- Start from a measurable **outcome** (not a feature or solution)
- Identify multiple **opportunities** (customer needs, pain points) that could drive that outcome
- Generate multiple **solutions** for each opportunity (avoid fixating on the first idea)
- Design **experiments** to test each solution cheaply before building fully

The tree forces breadth of thinking and prevents premature commitment to a single solution.

## Thesis-Driven Development

For each bet, document a thesis with these components:

**Thesis**: One sentence stating what you believe.
**Evidence for**: What data supports this belief?
**Evidence against**: What data contradicts it? What are you ignoring?
**Success criteria**: How will you know if the bet paid off? Be specific and measurable.
**Time box**: When will you evaluate? Do not let bets run indefinitely.
**Kill criteria**: What would cause you to abandon this bet early?

### Example

**Thesis**: Enterprise customers will pay 3x for a self-hosted deployment option.
**Evidence for**: 5 of our last 8 lost deals cited "no on-prem option" as the reason. Competitor X offers on-prem at 2.5x pricing.
**Evidence against**: Our best customers are cloud-native companies. On-prem support is operationally expensive.
**Success criteria**: 3 signed LOIs at the 3x price point within 90 days.
**Time box**: 90 days from start of sales outreach.
**Kill criteria**: Fewer than 5 qualified prospects in the pipeline after 30 days.

## Bet Status Tracking

Track every active bet with a clear status:

| Status | Meaning |
|--------|---------|
| **Active** | Currently being executed. Team is working on it. |
| **Validating** | Experiment is running. Waiting for results. |
| **Validated** | Success criteria met. Ready to promote to full investment. |
| **Invalidated** | Failed to meet success criteria. Learning documented. Bet closed. |
| **Paused** | Deprioritized but not killed. Will revisit at specified date. |

Every bet must have exactly one status. Review all bet statuses at least monthly.

## Quarterly Review

At the end of each quarter, review the entire bet portfolio:

1. **Which bets validated?** Promote to roadmap items or scale investment.
2. **Which bets invalidated?** Document the learning. What did you get wrong? Update your beliefs.
3. **Which bets need more data?** Extend the time box or redesign the experiment. Do not extend indefinitely -- max one extension.
4. **Which bets to kill?** Paused bets that have been paused for two quarters should be killed, not carried forward.
5. **What new bets to add?** Based on new data, insights, and market signals.

The quarterly review is also when you rebalance the portfolio. If too many bets are High-conviction, you are not exploring enough. If too many are Low-conviction, you are not committing enough.
