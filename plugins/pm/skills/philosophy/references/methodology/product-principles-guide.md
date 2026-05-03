# Product Principles Guide

## What Are Product Principles?

Product principles are the pre-made decisions that guide your team when facing tradeoffs. They are not aspirations or values statements. They are opinionated stances that tell the team which direction to go when two reasonable paths diverge.

## Anti-Patterns: Platitudes That Resolve Nothing

These are not principles. They are wallpaper:

- "We put customers first" -- who would say they put customers last?
- "We build innovative solutions" -- this is a wish, not a decision
- "Quality matters" -- of course it does, this resolves zero tradeoffs
- "We move fast" -- fast compared to what? at the expense of what?
- "Data-driven decisions" -- every company claims this

The problem with platitudes is that they sound good but resolve nothing. When your team disagrees about whether to ship a feature with known rough edges or delay for polish, "quality matters" does not help. It can be used to argue either side.

## The Bar Fight Test

A principle is real only if the opposite of that principle is also a reasonable position that a smart team might hold. This is the "bar fight test":

- "Design for first use, not expert use" -- the opposite ("design for power users, not beginners") is a legitimate stance (see: Bloomberg Terminal). This is a real principle.
- "Be customer-centric" -- the opposite ("ignore customers") is absurd. Nobody would argue for it. This is a platitude.

If you cannot imagine a successful company holding the opposite view, you do not have a principle. You have a platitude.

## Structure of a Good Principle

Each principle should have four components:

**Name**: A short, memorable label (2-5 words)
**Statement**: One sentence declaring the stance
**This means we...**: 2-3 concrete behaviors or decisions that follow from this principle
**This means we don't...**: 2-3 things we explicitly reject or deprioritize

### Example: "Craft Over Speed"

**Statement**: We would rather ship one thing exceptionally well than three things adequately.

**This means we...**
- Allocate time for friction logging before every launch
- Kill features that cannot meet our quality bar, even if they are 80% built
- Invest in design review as a blocking step, not a nice-to-have

**This means we don't...**
- Ship MVPs that embarrass us just to hit a date
- Measure team output by number of features shipped
- Skip accessibility or performance work to "get it out the door"

## Real-World Inspiration

**Stripe -- "Craft over speed"**: Stripe famously obsesses over API design, documentation quality, and developer experience polish. They will delay a launch to get the abstraction right. The opposite ("ship fast, iterate later") is how many successful startups operate -- making Stripe's stance a genuine principle.

**Linear -- "Opinionated over configurable"**: Linear deliberately limits configuration options. They believe that strong defaults and fewer choices create a better product. The opposite ("maximum flexibility for every workflow") is Jira's approach -- and Jira is a very successful product.

**Intercom -- "Ship fast, ship early"**: Intercom prioritizes learning velocity over polish. They would rather put something imperfect in front of customers quickly than perfect it in isolation. The opposite is Stripe's approach -- both are valid.

**Gusto -- "Show customers they're loved"**: Gusto invests in emotional design touches (confetti on first payroll run, handwritten-style onboarding). The opposite ("professional and minimal, no whimsy") is a legitimate B2B stance.

## The Rule of Five

If you have 10 principles, you have zero. Nobody can remember 10 principles, and 10 principles will inevitably contradict each other.

Limit yourself to a maximum of 5. Ideally 3-4. Each one should be significant enough that it meaningfully constrains decisions. If removing a principle would not change any team behavior, it is not earning its place.

## How to Discover Your Principles

1. **Look at past arguments**: What recurring debates does your team have? Principles should pre-resolve those debates.
2. **Look at past decisions**: When you made a hard tradeoff, which direction did you go? That pattern reveals your actual principles.
3. **Look at what you reject**: What do competitors do that you deliberately do not? That boundary is often a principle.
4. **Stress-test with scenarios**: For each candidate principle, construct a realistic scenario where it forces an uncomfortable-but-clear decision. If it does not force anything, it is not a principle.

## Maintaining Principles

Principles should be reviewed annually, not quarterly. They represent deep beliefs that should not shift with the wind. If you are changing principles every quarter, they were not principles -- they were tactics.

When a principle is violated in practice (the team consistently acts against it), you have two choices: recommit to the principle and change behavior, or acknowledge that the principle no longer reflects your beliefs and retire it. Do not maintain zombie principles that nobody follows.
