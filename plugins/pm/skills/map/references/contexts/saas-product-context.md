# SaaS Product Context Guide

## Purpose

This reference provides context for Mode A (SaaS PM) discovery. It covers the frameworks, metrics, and patterns that shape how SaaS Product Managers approach problem discovery.

---

## Product Lifecycle Stages

Discovery approach varies based on where the product sits in its lifecycle.

| Stage | Characteristics | Discovery Focus |
|-------|----------------|-----------------|
| **Pre-launch / MVP** | No existing users, hypothesis-driven | Market validation, early adopter interviews, competitive positioning |
| **Early Growth** | First paying users, finding product-market fit | Activation metrics, churn reasons, feature adoption patterns |
| **Growth / Scale** | Rapid user acquisition, expanding use cases | Segmentation, power user vs casual user needs, scalability pain points |
| **Maturity** | Stable user base, incremental improvements | Retention optimization, upsell/cross-sell opportunities, platform plays |
| **Renewal / Reinvention** | Market shifts, competitive pressure | Strategic pivots, new persona discovery, adjacent market analysis |

## Product-Led Growth (PLG) Metrics

When discovering problems in a PLG context, map pain points to the pirate metrics framework (AARRR).

| Metric | Question | Discovery Relevance |
|--------|----------|-------------------|
| **Acquisition** | How do users find the product? | Channel analysis, first-touch experience |
| **Activation** | Do users reach the "aha moment"? | Onboarding friction, time-to-value |
| **Retention** | Do users come back? | Habit loops, recurring pain points, churn signals |
| **Revenue** | Do users pay (more)? | Pricing friction, upgrade triggers, value perception |
| **Referral** | Do users invite others? | Delight moments, sharing mechanics, viral loops |

### Key Activation Metrics to Explore

- **Time to first value**: How long from signup to first meaningful action?
- **Setup completion rate**: What % of users complete onboarding?
- **Feature discovery rate**: What % of users find and use core features?
- **Activation threshold**: What action, when completed, predicts long-term retention?

### Key Retention Metrics to Explore

- **DAU/MAU ratio**: Daily active / Monthly active (engagement intensity)
- **Churn rate**: % of users who stop using the product per period
- **Net revenue retention (NRR)**: Revenue retained including expansion and contraction
- **Feature stickiness**: Which features drive repeated use?

---

## User Journey Mapping for SaaS

### Standard SaaS User Journey Stages

| Stage | User Action | System Touchpoint | Emotional State |
|-------|------------|-------------------|----------------|
| **Discover** | Finds product via search, referral, ad | Landing page, free trial signup | Curious, evaluating |
| **Onboard** | Creates account, configures settings | Setup wizard, documentation | Hopeful but potentially overwhelmed |
| **Activate** | Completes first meaningful action | Core feature, integration setup | Excited or frustrated |
| **Engage** | Uses product regularly for intended purpose | Dashboard, workflows, notifications | Productive or struggling |
| **Expand** | Discovers additional features, invites team | Advanced features, admin panel | Empowered or confused |
| **Advocate** | Recommends to others, writes reviews | Referral program, community | Loyal or indifferent |

### Discovery Questions by Journey Stage

**Discover stage issues:**
- Where do potential users first hear about the product?
- What expectations are set before signup?
- What is the competitive comparison experience like?

**Onboard stage issues:**
- Where do users get stuck during setup?
- What is the average time from signup to first use?
- What % of signups never complete onboarding?

**Activate stage issues:**
- What is the "aha moment" for this product?
- How many steps to reach first value?
- What are the top support tickets in the first 7 days?

**Engage stage issues:**
- What is the core loop (the action users repeat)?
- What triggers users to come back?
- Where do users report friction in their daily workflow?

**Expand stage issues:**
- What features do power users adopt that casual users miss?
- What drives team adoption vs individual use?
- What triggers upgrade from free to paid tier?

---

## Competitive Landscape Analysis

### Framework for Discovery

| Dimension | What to Capture |
|-----------|----------------|
| **Direct competitors** | Products solving the same problem for the same persona |
| **Indirect competitors** | Products solving the same problem differently (spreadsheets, manual processes) |
| **Substitute solutions** | Workarounds users have built (scripts, integrations, hiring) |
| **Emerging threats** | New entrants, AI-native solutions, platform plays |

### Competitive Positioning Questions

- What do users currently use before adopting this product?
- What do users praise about competitor products?
- What do users complain about regarding competitors?
- What switching costs exist (data migration, retraining, integrations)?

---

## SaaS-Specific Pain Point Categories

| Category | Description | Examples |
|----------|-------------|---------|
| **Integration friction** | Product does not connect to user's existing tools | "I have to copy data from X to Y manually" |
| **Configuration complexity** | Setup requires technical expertise users lack | "I need an engineer to configure this" |
| **Pricing misalignment** | Pricing model does not match value perception | "I pay for 100 seats but only 20 are active" |
| **Performance at scale** | Product slows or breaks as usage grows | "Reports take 5 minutes to load with our data volume" |
| **Multi-tenant limitations** | Product does not support organizational complexity | "We need separate workspaces per department" |
| **Missing self-service** | Users depend on support for routine tasks | "I have to email support to change my plan" |

---

## How SaaS PMs Approach Discovery Differently

| Aspect | SaaS PM Approach | Consulting PM Approach |
|--------|-----------------|----------------------|
| **Data sources** | Product analytics, user interviews, support tickets, NPS surveys | Stakeholder interviews, process documentation, org charts |
| **Persona depth** | Behavior, feelings, journey, jobs-to-be-done | Organizational role, authority, RACI |
| **Process focus** | User flows within the product | Business processes across the organization |
| **Success metrics** | Adoption, retention, NRR, NPS | Cycle time, error rate, cost per transaction |
| **Competitive context** | Other products and workarounds | Other consulting firms' transformation designs |
| **Handoff target** | PRD (pm-prd-generator) | TOM (tom-architect) |

---

## SaaS Discovery Anti-Patterns

| Anti-Pattern | Risk | Mitigation |
|-------------|------|------------|
| **Building for the loudest customer** | Skews product toward one use case | Validate with data across segments |
| **Feature-request driven discovery** | Collects solutions, not problems | Ask "what are you trying to accomplish?" not "what do you want us to build?" |
| **Ignoring non-users** | Misses why people do not adopt | Study churn reasons and trial abandonment |
| **Over-indexing on power users** | Neglects the majority experience | Segment analysis by usage level |
| **No quantitative validation** | Discovery is anecdotal | Pair qualitative interviews with product analytics |
