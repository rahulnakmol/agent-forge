# Customer Experience Philosophy Guide

## What is a CX Philosophy?

A CX philosophy is your product team's explicit stance on the quality of experience you commit to delivering. It answers: "How good does this need to be before we ship it, and where do we invest extra effort to create delight?"

## The 11-Star Framework

The 11-star framework (originated by Brian Chesky at Airbnb, adapted in prd-review) provides a shared vocabulary for experience quality:

| Stars | Level | Description |
|-------|-------|-------------|
| 1-2 | Broken | Functional failures, hostile UX, customer actively harmed |
| 3 | Minimum viable | It works, barely. Customer tolerates it. |
| 4-5 | Competent | Meets expectations. No complaints, no praise. Industry standard. |
| 6 | Good | Noticeably better than alternatives. Customers mention it positively. |
| 7 | Great | Customers recommend you specifically because of the experience. |
| 8 | Remarkable | Customers tell stories about it. "You have to try this." |
| 9-10 | Magical | Feels like the product reads your mind. Effortless and delightful. |
| 11 | Impossible ideal | A thought exercise -- what would perfection look like with no constraints? |

The sweet spot for most products is **6-8 stars**. Below 6 and you are undifferentiated. Above 8 and you are likely over-investing relative to what customers will pay for.

### Where Does YOUR Product Aim?

Not every feature deserves the same star level. Define your target by journey stage:

| Journey Stage | Target Stars | Rationale |
|---------------|-------------|-----------|
| First-time experience | {X} stars | First impressions determine whether users come back |
| Core workflow | {X} stars | This is where users spend 80% of their time |
| Edge cases / admin | {X} stars | Functional correctness matters more than delight here |
| Error recovery | {X} stars | How you handle failure defines trust |

Be explicit about where you aim high and where "good enough" is genuinely good enough. Aiming for 8-star error messages while your core workflow is 5 stars is a misallocation.

## Kano Model Integration

The Kano model categorizes features by their relationship to customer satisfaction:

**Must-Be (Basic)**: Expected. Presence does not delight; absence causes outrage. Examples: data does not get lost, pages load within 3 seconds, login works.

**Performance (Linear)**: More is better, in a predictable way. Examples: faster search results, more storage, better uptime. Customer satisfaction scales linearly with investment.

**Attractive (Delighters)**: Unexpected features that create disproportionate delight. Examples: Gusto's payroll confetti, Superhuman's speed, Linear's keyboard shortcuts. Absence does not disappoint because customers did not expect them.

### How to Apply Kano to Your CX Philosophy

1. **Identify your must-be features** and ensure they are at minimum 5-6 stars. Never ship below this bar.
2. **Pick 1-2 performance dimensions** where you will out-invest competitors. These are your competitive moat.
3. **Choose 1-2 attractive features** where you invest in delight. These become your signature -- the thing customers talk about.

Do not try to delight everywhere. Delighting on 20 features means delighting on zero. Pick your moments.

## Experience Quality Bar

Define your minimum acceptable star level before shipping. This is a hard rule, not a guideline:

- **Hard floor**: No feature ships below {X} stars. Period. If it cannot meet this bar, it does not ship.
- **Aspiration target**: We aim for {X} stars on core workflows.
- **Delight target**: We invest in {X} stars for {specific moments}.

The quality bar should be documented, agreed upon by engineering/design/product, and enforced in review processes.

## Customer Journey Investment

Where you invest most reveals your CX philosophy. Most products cannot invest equally across all stages:

**Acquisition-heavy**: Invest in first impressions, onboarding, wow moments. Best for: products with free trials, low switching costs, viral loops.

**Activation-heavy**: Invest in time-to-value, setup experience, first success moment. Best for: products where the aha moment is complex (developer tools, enterprise software).

**Retention-heavy**: Invest in core workflow speed, reliability, depth. Best for: products with high switching costs, daily-use tools.

**Advocacy-heavy**: Invest in shareable moments, referral experiences, community. Best for: products with network effects, community-driven growth.

Pick one primary and one secondary. Document why.

## Design for Delight vs. Design for Reliability

This is a foundational CX choice:

**Design for delight** (primary): You believe emotional connection drives retention and word-of-mouth. You invest in animation, copy, surprise moments, and emotional design. Risk: reliability gaps erode trust faster than delight builds it.

**Design for reliability** (primary): You believe consistency and predictability build trust. You invest in performance, uptime, error handling, and data integrity. Risk: the product becomes forgettable -- reliable but not remarkable.

Most great products do both, but one is always primary. Stripe designs for reliability first, then adds craft. Notion designs for delight first, then hardens reliability. Know which you are.

Document your choice and the reasoning behind it. This single decision cascades through every design review and engineering prioritization.
