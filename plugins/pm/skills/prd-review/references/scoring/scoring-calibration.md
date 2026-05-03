# Scoring Calibration Examples

## Purpose

Calibration examples ensure scoring is reproducible and consistent. Each example shows a PRD excerpt, its scores across all 7 dimensions, and annotations explaining the rationale. Use these examples to anchor your scoring before evaluating a new PRD.

---

## Example 1: Weak PRD (Overall Score: 3.2/10)

### PRD Excerpt

> **Product**: Employee Expense Reporting Tool
>
> **Problem**: Employees need to submit expenses.
>
> **Features**:
> - Users can submit expenses
> - Managers can approve expenses
> - System generates reports
> - Integration with accounting software
>
> **User Story**: As a user, I want to submit my expenses so that I can get reimbursed.
>
> **Success Metrics**: Track number of expenses submitted.

### Scores and Annotations

| Dimension | Score | Annotation |
|-----------|-------|------------|
| Completeness | 2/10 | Problem statement is one sentence with no context (why is this needed? what is broken today?). Features are bullet points with no detail. No acceptance criteria, no technical considerations, no constraints, no timeline, no edge cases. Missing: error handling, expense categories, receipt upload, currency handling, policy compliance, mobile support. |
| Clarity | 3/10 | "Submit expenses" -- how? What fields? What formats? "Generates reports" -- what reports? For whom? What data? "Integration with accounting software" -- which software? What data flows? Every requirement is ambiguous. |
| Feasibility | 5/10 | Paradoxically, a vague PRD is "feasible" because it commits to nothing. But this is false feasibility -- the moment implementation begins, every decision will surface as a question. Score reflects that nothing described is impossible, but nothing is specified enough to build. |
| Ambition | 1/10 | Every feature described exists in every expense tool since 2005. No proactive features, no intelligence, no contextual awareness. This is star 4 at best for every feature. No evidence of aspirational thinking. |
| Differentiation | 1/10 | Zero differentiation. This describes the generic category, not a specific product. A user would choose this only if it were free. |
| Metric Alignment | 2/10 | "Track number of expenses submitted" is a vanity metric. It does not measure whether the tool is successful (fast reimbursement? policy compliance? reduced manual processing?). No targets, no baselines, no timeline. |
| Story Quality | 2/10 | No narrative. No user context. No before/after. The single user story is the most generic possible formulation. You cannot picture the user, their pain, or their journey. |

**Overall**: (2 x 0.15) + (3 x 0.15) + (5 x 0.15) + (1 x 0.15) + (1 x 0.15) + (2 x 0.10) + (2 x 0.15) = 0.30 + 0.45 + 0.75 + 0.15 + 0.15 + 0.20 + 0.30 = **2.3/10**

**Grade**: F (Reject)

**Key takeaway**: This PRD describes a category of software, not a product. It needs a fundamental rewrite starting with user research and problem definition.

---

## Example 2: Solid PRD (Overall Score: 7.1/10)

### PRD Excerpt

> **Product**: SmartExpense -- AI-Assisted Expense Reporting
>
> **Problem Statement**: Finance teams at mid-market companies (200-2000 employees) spend an average of 18 minutes per expense report on manual data entry, categorization, and policy compliance checks. Employees submit expenses an average of 11 days after the expense occurs, leading to inaccurate cash flow forecasting. 34% of first submissions are rejected for policy violations, creating rework cycles averaging 3 back-and-forth exchanges.
>
> **Target User**: Sarah, a regional sales manager who travels 3 weeks per month. She accumulates 15-20 expenses per week across meals, transport, lodging, and client entertainment. She currently saves receipts in a folder on her phone and batch-submits on Sunday evenings, often miscategorizing expenses because she cannot remember the context from 2 weeks ago.
>
> **Key Features**:
>
> 1. **Receipt Capture** (Star 5): Photograph receipt, OCR extracts merchant, amount, date, and category. User confirms or corrects. Supports 12 currencies with real-time conversion.
>    - AC: OCR accuracy > 95% for printed receipts in supported languages (EN, FR, DE, ES, JP)
>    - AC: Currency conversion uses daily rates from European Central Bank API
>    - AC: Processing completes in < 3 seconds on 4G connection
>
> 2. **Smart Categorization** (Star 6): System suggests expense category based on merchant, amount, time of day, and user history. Learns from corrections.
>    - AC: First suggestion is correct > 80% of the time after 10 submitted expenses
>    - AC: Category suggestions appear within 1 second of receipt capture
>    - AC: User can override with single tap; override trains the model
>
> 3. **Policy Pre-Check** (Star 7): Before submission, the system validates all expenses against company policy and highlights violations with plain-language explanations and suggested fixes. "Your dinner at Le Bernardin ($312) exceeds the $150 meal limit for domestic travel. Options: Split across 2 meals, reclassify as client entertainment (requires client name), or submit with justification note."
>    - AC: 100% of policy rules are encoded and checked pre-submission
>    - AC: Violation explanations are in plain language (no policy code references)
>    - AC: Each violation includes at least one actionable resolution
>
> **Success Metrics**:
> - Time to submit: Reduce from 18 min to < 5 min per report (baseline from current analytics)
> - First-submission approval rate: Increase from 66% to > 90%
> - Submission latency: Reduce from 11 days to < 3 days post-expense
> - User satisfaction: > 4.2/5.0 on monthly pulse survey

### Scores and Annotations

| Dimension | Score | Annotation |
|-----------|-------|------------|
| Completeness | 7/10 | Problem statement is data-driven and specific. Features have detailed acceptance criteria. Success metrics have baselines and targets. Missing: technical architecture, dependencies (OCR provider, policy engine), rollout plan, edge cases for international scenarios, accessibility requirements. |
| Clarity | 8/10 | Requirements are specific and testable. Performance targets are quantified. Acceptance criteria use measurable thresholds. The policy pre-check feature includes a concrete example of the user experience. Minor gap: no glossary for domain terms, some assumption about "supported languages" without listing all. |
| Feasibility | 7/10 | OCR at 95% accuracy is achievable with modern APIs. Smart categorization with 80% accuracy after 10 samples is ambitious but supported by existing ML approaches. Policy pre-check is technically straightforward. Timeline and resource plan not included -- feasibility assessment is based on feature complexity alone. |
| Ambition | 7/10 | Receipt capture is table stakes (star 5) -- appropriate. Smart categorization at star 6 shows proactive behavior. Policy pre-check at star 7 is genuinely differentiating -- users would tell colleagues about a tool that explains policy violations in plain language and suggests fixes. Good sweet-spot targeting. |
| Differentiation | 7/10 | Policy pre-check with plain-language explanations and actionable fixes is a genuine differentiator. Most expense tools flag violations; few explain them helpfully. Smart categorization is increasingly common but the learning-from-corrections aspect adds stickiness. Positioning against specific competitors would strengthen this. |
| Metric Alignment | 8/10 | Strong metrics with baselines, targets, and clear measurement methodology. Metrics connect to real business outcomes (time savings, reduced rework, cash flow accuracy). Missing: leading indicators for adoption, guardrail metrics (e.g., false positive rate on policy checks). |
| Story Quality | 7/10 | Sarah as a specific user with a specific workflow is compelling. The before/after is implicit but clear. The policy pre-check example brings the feature to life. Missing: the full user journey from download to weekly habit. Features are well-described individually but the narrative connecting them could be stronger. |

**Overall**: (7 x 0.15) + (8 x 0.15) + (7 x 0.15) + (7 x 0.15) + (7 x 0.15) + (8 x 0.10) + (7 x 0.15) = 1.05 + 1.20 + 1.05 + 1.05 + 1.05 + 0.80 + 1.05 = **7.25/10**

**Grade**: C+ / B (Minor Revision)

**Key takeaway**: This is a solid PRD with clear thinking and good ambition targeting. Improvements needed in technical architecture, rollout planning, and connecting features into a complete user journey narrative.

---

## Example 3: Exceptional PRD (Overall Score: 9.2/10)

### PRD Excerpt

> **Product**: SmartExpense v2 -- Expense Intelligence Platform
>
> **Problem Statement**: [Same as Example 2, plus:] Beyond the immediate pain of expense reporting, finance teams lack real-time visibility into travel spend patterns, cannot proactively enforce budgets (only reactively reject violations), and have no mechanism to surface cost-saving opportunities. The expense report is treated as a compliance artifact rather than a strategic data source.
>
> **Vision**: Expense reporting should not exist as a distinct task. Expenses should capture themselves at the moment of transaction, categorize themselves correctly, comply with policy by default, and generate strategic insights automatically. The 18-minute expense report should become a 0-minute non-event, and the data it produces should make the organization smarter about how it spends.
>
> **Target Users**: [Sarah from Example 2, plus David -- a finance controller who spends 3 days per month reviewing expense reports, and Lisa -- a CFO who gets a quarterly spend analysis that is always 6 weeks stale.]
>
> **Anchor Feature -- Proactive Budget Intelligence** (Star 8):
> Instead of flagging policy violations after they occur, the system prevents them. When Sarah books a hotel in Chicago, SmartExpense detects the booking (via email integration or corporate card transaction), checks the Chicago per-diem rate, and sends a push notification: "Your hotel rate ($289/night) is 15% above the Chicago average for your dates. Here are 3 policy-compliant alternatives within 0.5 miles of your meeting location, saving $47/night." If Sarah proceeds with the original booking, the system pre-attaches the justification context (meeting location, availability of alternatives, price differential) so the approval is automatic.
>
> This reframes expense management from "submit and get rejected" to "decide and get guided." The mental model shifts from compliance-after-the-fact to intelligence-before-the-decision. After using this, returning to traditional expense reporting feels like filing paperwork after the work is already done.
>
> - AC: Real-time transaction detection within 30 seconds of corporate card charge or booking email
> - AC: Alternative suggestions include only options within policy, within 1 mile of meeting location, with availability confirmed
> - AC: Pre-attached justification reduces approval time from 48 hours average to < 2 hours
> - AC: Users who receive proactive suggestions make policy-compliant choices 85%+ of the time (vs 66% baseline)
> - Degraded experience: If real-time detection fails, fall back to receipt-capture flow (star 5 baseline)
>
> **Success Metrics**:
> - Input metric: % of expenses captured at point of transaction (target: 70% within 6 months)
> - Process metric: Time from expense to approval (target: < 4 hours, baseline: 14 days)
> - Output metric: Policy compliance rate (target: > 95%, baseline: 66%)
> - Business metric: Travel spend reduction through proactive suggestions (target: 8-12% annually)
> - Guardrail metric: User satisfaction must not drop below 4.0 during compliance increase (prevent "nanny state" perception)
> - Experimentation: A/B test proactive suggestions vs control group for 90 days to validate spend reduction claim

### Scores and Annotations

| Dimension | Score | Annotation |
|-----------|-------|------------|
| Completeness | 9/10 | Problem statement addresses multiple stakeholders and escalates from tactical (expense reporting) to strategic (spend intelligence). Features include acceptance criteria, degraded experience, and experimentation plan. Multiple personas with distinct needs. Only gap: security and data privacy considerations for email/card integration not detailed in this excerpt. |
| Clarity | 9/10 | Every requirement is testable with specific thresholds. The anchor feature is described with a concrete scenario that leaves no ambiguity about the intended experience. Degraded experience is specified. Acceptance criteria distinguish between happy path and fallback. |
| Feasibility | 8/10 | Corporate card transaction detection is proven technology. Email parsing for booking confirmation is established. Alternative hotel suggestions require API integration (Booking.com, hotel chains) -- feasible but complex. The 30-second detection window is ambitious; acknowledged implicitly by including fallback. Meeting location inference requires calendar integration. Scores 8 because the approach is credible with known trade-offs. |
| Ambition | 10/10 | The anchor feature reframes the problem from compliance to intelligence. This is genuine star 8 thinking: after using proactive budget guidance, traditional expense reporting feels broken. The vision of "0-minute expense reports" shows clear 11-star backward design. The distinction between star 5 baseline and star 8 anchor is deliberate and well-calibrated. |
| Differentiation | 9/10 | No major expense tool offers proactive, pre-decision budget intelligence with real-time alternatives. The shift from post-hoc compliance to pre-decision guidance is a category-level differentiator. The data advantage compounds (more usage = better suggestions = more savings). Only gap: defensibility against well-resourced competitors who could replicate. |
| Metric Alignment | 10/10 | Exemplary metric hierarchy: input -> process -> output -> business. Guardrail metric prevents over-optimization. Experimentation plan validates the core value hypothesis. Baselines and targets for every metric. The metrics themselves tell a story about the product's theory of change. |
| Story Quality | 9/10 | The Chicago hotel scenario is vivid and immediately understandable. Multiple personas show the product's impact across roles. The before/after is explicit and compelling ("submit and get rejected" vs "decide and get guided"). The vision statement is specific, not generic. The narrative connects tactical features to strategic outcomes. |

**Overall**: (9 x 0.15) + (9 x 0.15) + (8 x 0.15) + (10 x 0.15) + (9 x 0.15) + (10 x 0.10) + (9 x 0.15) = 1.35 + 1.35 + 1.20 + 1.50 + 1.35 + 1.00 + 1.35 = **9.1/10**

**Grade**: A+ (Exemplary)

**Key takeaway**: This PRD demonstrates every principle of the review framework. It shows clear 11-star backward design (the 0-minute vision), targets the sweet spot (star 8 anchor with star 5 fallback), uses specific personas and scenarios, and backs ambition with feasible approaches and measurable metrics.

---

## Using Calibration Examples During Review

Before scoring a new PRD:

1. Reread the 3.2/10 example to anchor your sense of "weak"
2. Reread the 7.1/10 example to anchor your sense of "solid"
3. Reread the 9.2/10 example to anchor your sense of "exceptional"
4. Score the new PRD relative to these anchors

**Common calibration errors**:
- **Generosity bias**: Scoring 7/10 as "default good." A 7 means the PRD is genuinely strong with specific evidence. Compare to the 7.1 example.
- **Ambition conflation**: Scoring Ambition high because the PRD mentions AI. Ambition requires evidence of 11-star thinking, not buzzword inclusion.
- **Completeness inflation**: Scoring Completeness high because the document is long. Length is not completeness. Check for depth, not pages.
- **Clarity/Feasibility confusion**: A clear requirement can be infeasible, and a feasible feature can be poorly specified. Score independently.
