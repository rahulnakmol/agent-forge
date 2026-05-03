# Building Approach Guide

## What is a Building Approach?

Your building approach is the documented set of practices, standards, and rituals that define how your team turns ideas into shipped product. It is not a process document -- it is a philosophy of craft that answers: "What does it mean to build well here?"

## Methodology

Choose your core methodology and document why it fits your team:

**Scrum**: Fixed-length sprints, ceremonies (standup, planning, retro, review), defined roles (PO, SM). Best for: teams that need predictable delivery cadence and clear accountability.

**Kanban**: Continuous flow, WIP limits, pull-based. Best for: teams with unpredictable work (support, ops), or teams that find sprint boundaries artificial.

**Shape Up** (Basecamp): 6-week cycles, shaped pitches, cool-down periods, small teams with autonomy. Best for: teams that want to eliminate estimation and give teams real ownership of scope.

**Custom hybrid**: Most mature teams evolve a hybrid. Document what you took from each methodology and why. Be specific -- "we do Scrum but without story points" is not a methodology; explain what replaced points and why.

### What Ceremonies Matter?

List only the ceremonies you actually practice and find valuable. Kill the rest.

| Ceremony | Frequency | Purpose | Who attends |
|----------|-----------|---------|-------------|
| {name} | {cadence} | {why it exists} | {roles} |

If a ceremony does not have a clear purpose and regular attendees who find it valuable, eliminate it.

## Quality Bar

Define what "done" means for your team:

**Testing standards**: What never ships without tests? Unit? Integration? E2E? Define the bar, not the aspiration.

**Code review standards**: Who reviews? How many approvals? What are reviewers looking for beyond correctness (readability, architecture, naming)?

**Accessibility bar**: WCAG level (A, AA, AAA)? Which guidelines are hard requirements vs. aspirations? Do you test with screen readers?

**Performance bar**: Load time budgets? Bundle size limits? API response time SLAs?

Be honest about your actual bar, not your aspirational one. A documented bar of "all PRs need one approval and unit tests for business logic" that you actually enforce is worth more than "100% coverage and three approvals" that you routinely skip.

## Craft Standards

Craft is what separates "it works" from "it works beautifully."

**Friction logging** (Stripe practice): Before every major launch, team members use the product end-to-end and log every point of friction, confusion, or annoyance -- no matter how small. These logs are triaged and the worst friction points are fixed before launch.

**Dogfooding**: Does your team use your own product daily? How formally? Some teams mandate it; others rely on voluntary use. Document your stance and how feedback flows from dogfooding into the backlog.

**Design review**: Is design review a blocking gate or an advisory input? Who has final say when design and engineering disagree on implementation fidelity? Document the escalation path.

**Copy review**: Who writes user-facing copy? Who reviews it? Is there a voice and tone guide? Inconsistent copy is a surprisingly common source of product friction.

## Release Philosophy

**Continuous deployment**: Every merged PR goes to production. Best for: mature CI/CD, strong test coverage, feature flag infrastructure. Risk: requires high discipline.

**Release trains**: Scheduled releases (weekly, biweekly). Best for: teams that need coordination across multiple services or external stakeholders. Risk: becomes a bottleneck.

**Feature flags**: Decouple deployment from release. Ship code dark, enable for internal users, then percentage rollout, then GA. This is increasingly the industry standard for non-trivial features.

**Canary releases**: Route a small percentage of traffic to the new version, monitor for errors, then roll forward. Best for: backend services, infrastructure changes.

Document your approach and the decision tree for when to use flags vs. direct deployment vs. staged rollout.

## Tech Debt Stance

Every team accumulates tech debt. The question is how you manage it:

- **Percentage allocation**: Reserve a fixed percentage (commonly 15-20%) of each cycle for debt reduction
- **Dedicated sprints**: Full cycles devoted to debt, usually quarterly
- **Continuous refactoring**: Refactor as you go -- every PR should leave the code better than it found it (Boy Scout Rule)
- **Debt budget**: Treat tech debt like financial debt -- track it, set a maximum acceptable level, pay it down deliberately

Document which approach you use and how you decide what debt to pay down first.

## Documentation Culture

What gets documented and what does not:

- **Architecture decisions**: ADRs (Architecture Decision Records)? Where do they live?
- **API contracts**: OpenAPI specs? Generated from code or hand-written?
- **Runbooks**: For on-call and incident response?
- **Product decisions**: PRDs? RFCs? Where is the canonical record of why a decision was made?

The test: when a new engineer joins, can they understand why things are the way they are without asking five people? If not, your documentation culture has gaps.

## Reference: Spotify's Think-Build-Ship-Tweak

Spotify's model provides a useful mental framework for the building cycle:

- **Think**: Understand the problem. Research, define, shape.
- **Build**: Create the solution. Design, code, test.
- **Ship**: Get it to customers. Deploy, enable, announce.
- **Tweak**: Learn and improve. Monitor, iterate, polish.

Most teams over-invest in Build and under-invest in Think and Tweak. Document where your team tends to under-invest and how you compensate.
