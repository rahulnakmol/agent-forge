# Value Proposition Mapping

## Jobs-to-be-Done Framework

Customers do not buy products. They "hire" products to make progress in specific circumstances. This insight, from Clayton Christensen and Bob Moesta, is the foundation of value proposition mapping.

The famous milkshake example: McDonald's customers were not buying milkshakes because they wanted a milkshake. Morning commuters hired the milkshake for the job of "make my boring commute more interesting and keep me full until lunch." The competition was not other milkshakes -- it was bananas, bagels, and boredom.

### Three Types of Jobs

**Functional Jobs**: The practical task the customer needs to accomplish.
- "Help me send invoices to clients and get paid faster"
- "Let me deploy code to production without breaking things"

**Emotional Jobs**: How the customer wants to feel (or avoid feeling).
- "Make me feel confident that my finances are under control"
- "Remove the anxiety of deploying on Friday afternoon"

**Social Jobs**: How the customer wants to be perceived by others.
- "Make me look competent to my manager when I present metrics"
- "Signal to my team that I use modern, professional tools"

Most products are hired for a blend of all three. Ignoring emotional and social jobs is a common mistake -- they often drive purchasing decisions more than functional jobs.

## Outcome-Driven Innovation (Ulwick)

Tony Ulwick's framework focuses on identifying underserved outcomes within each job. For every job, customers have 10-50 desired outcomes. The opportunity lies where outcomes are important to customers but poorly satisfied by current solutions.

**Opportunity Score** = Importance + max(Importance - Satisfaction, 0)

Outcomes with high importance and low satisfaction are your target. Outcomes with high importance and high satisfaction are table stakes. Outcomes with low importance are distractions.

## Value Proposition Structure

Use this formula to articulate each value proposition clearly:

> **For** [target customer segment]
> **who need to** [job-to-be-done]
> **our product** [product name]
> **delivers** [key outcome / benefit]
> **unlike** [primary alternative]
> **because** [unique differentiator]

### Example

> **For** early-stage startup founders
> **who need to** ship a product before their runway expires
> **our product** LaunchKit
> **delivers** a production-ready app in days instead of months
> **unlike** hiring a dev agency or building from scratch
> **because** we provide opinionated, pre-integrated modules that eliminate architectural decisions

## Value Proposition Canvas

Map the customer side to the product side:

```
CUSTOMER SIDE                    PRODUCT SIDE
+---------------------------+    +---------------------------+
| Jobs-to-be-Done           |    | Products & Services       |
| - Functional jobs         |    | - Features offered        |
| - Emotional jobs          |    | - Services provided       |
| - Social jobs             |    |                           |
+---------------------------+    +---------------------------+
| Pains                     |    | Pain Relievers            |
| - Frustrations            | <- | - How you eliminate pains |
| - Risks                   |    | - Risk reduction          |
| - Obstacles               |    | - Obstacle removal        |
+---------------------------+    +---------------------------+
| Gains                     |    | Gain Creators             |
| - Desired outcomes        | <- | - How you create gains    |
| - Expected benefits       |    | - Unexpected delights     |
| - Aspirations             |    | - Performance boosts      |
+---------------------------+    +---------------------------+
```

**Fit** exists when your pain relievers and gain creators directly address the most important pains and gains for your target customer's primary job.

## Mapping Value Props to Segments

Each value proposition should map to exactly one primary customer segment and one primary job. If a single value prop tries to serve three segments, it is too vague.

| Value Proposition | Primary Segment | Primary Job | Secondary Segments |
|-------------------|----------------|-------------|-------------------|
| {VP1 summary} | {Segment A} | {Job description} | {Segments B, C} |
| {VP2 summary} | {Segment B} | {Job description} | {Segment A} |

Limit yourself to 2-4 core value propositions. If you have more, you either have multiple products or you have not made hard choices about what you truly deliver.

## Validation Signals

A value proposition is validated when:
- Customers describe the job in their own words (not your marketing language)
- Customers compare you to the alternatives you identified (not different ones)
- Willingness to pay correlates with the job importance you assumed
- Churn correlates with failure to deliver the promised outcome

A value proposition is invalidated when:
- Customers hire your product for a different job than you designed for
- The "unlike alternatives" you identified are not what customers actually compare you to
- Customers cannot articulate what your product does for them
