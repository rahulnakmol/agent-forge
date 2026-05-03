# Problem Framing Techniques

## Purpose

Problem framing ensures the team solves the right problem before designing solutions. A well-framed problem reduces rework, aligns stakeholders, and produces sharper requirements. This reference covers four proven techniques and guidance on distinguishing root causes from symptoms.

---

## Technique 1: Five Whys

A root cause analysis method that drills through layers of symptoms to reach the underlying cause.

### How to Apply

1. State the problem as observed
2. Ask "Why does this happen?" -- answer concisely
3. Take the answer and ask "Why?" again
4. Repeat until you reach a cause that, if resolved, would prevent the problem
5. Typically requires 3-5 iterations (not always exactly 5)

### Example (SaaS Context)

| # | Question | Answer |
|---|----------|--------|
| 1 | Why are users abandoning the onboarding flow? | They get stuck on the integration step |
| 2 | Why do they get stuck on integration? | The API key setup instructions are unclear |
| 3 | Why are the instructions unclear? | They reference a deprecated admin panel |
| 4 | Why do they reference a deprecated panel? | Documentation was not updated after the Q3 platform migration |
| 5 | **Root cause** | No documentation update process tied to platform releases |

### Example (Consulting Context)

| # | Question | Answer |
|---|----------|--------|
| 1 | Why is invoice processing taking 15 days? | Invoices queue for manager approval |
| 2 | Why do they queue? | Managers batch approvals weekly |
| 3 | Why weekly batching? | The approval system requires VPN access only available on office desktops |
| 4 | Why VPN-only? | The ERP was never configured for mobile/web access |
| 5 | **Root cause** | Technology constraint forces inefficient approval behavior |

### When to Use
- Problem seems straightforward but keeps recurring
- Team disagrees on what the "real" problem is
- Quick analysis needed before deeper investigation

---

## Technique 2: Fishbone / Ishikawa Diagram

A structured cause-and-effect analysis that categorizes potential root causes into standard categories.

### Standard Categories

| Category | What to Examine | SaaS Examples | Consulting Examples |
|----------|----------------|---------------|-------------------|
| **People** | Skills, training, staffing, motivation | Developer experience gaps | Process owner unclear |
| **Process** | Workflow, procedures, handoffs | No QA gate before release | Manual data re-entry between systems |
| **Technology** | Systems, tools, infrastructure | Legacy API rate limits | ERP not integrated with CRM |
| **Data** | Quality, availability, timeliness | Incomplete user analytics | Inconsistent master data across regions |
| **Environment** | Market, regulatory, organizational culture | Competitive pressure to ship fast | Siloed departments resist sharing |
| **Management** | Priorities, resources, decision-making | Unclear product strategy | No executive sponsor for change |

### How to Apply

1. Write the problem statement at the "head" of the fish
2. Draw main bones for each category
3. Brainstorm potential causes within each category
4. Identify which causes have the strongest evidence
5. Prioritize the top 2-3 causes for further investigation

### When to Use
- Problem has multiple potential causes across different areas
- Team needs a structured brainstorming framework
- Root cause is not obvious from Five Whys alone

---

## Technique 3: Jobs-to-be-Done (JTBD)

Frames the problem from the user's perspective: what "job" is the user trying to accomplish, and what barriers prevent successful completion?

### JTBD Statement Formula

**When** [situation], **I want to** [motivation], **so I can** [expected outcome].

### Three Dimensions of a Job

| Dimension | Question | Example |
|-----------|----------|---------|
| **Functional** | What does the user need to accomplish? | "Process expense reports within 2 business days" |
| **Emotional** | How does the user want to feel? | "Confident that I won't make errors that trigger audit flags" |
| **Social** | How does the user want to be perceived? | "Seen as efficient and responsive by the team" |

### Job Map (8 Steps)

| Step | Description | Discovery Questions |
|------|-------------|-------------------|
| 1. **Define** | How does the user define what needs to be done? | "How do you decide what to work on first?" |
| 2. **Locate** | How does the user find the inputs needed? | "Where do you get the information you need?" |
| 3. **Prepare** | How does the user set up for the task? | "What do you have to do before you can start?" |
| 4. **Confirm** | How does the user verify readiness? | "How do you know you have everything you need?" |
| 5. **Execute** | How does the user perform the core task? | "Walk me through the steps you take" |
| 6. **Monitor** | How does the user track progress? | "How do you know if things are going well?" |
| 7. **Modify** | How does the user handle exceptions? | "What do you do when something goes wrong?" |
| 8. **Conclude** | How does the user finish and hand off? | "How do you know you are done?" |

### When to Use
- Mode A (SaaS) -- primary technique for understanding user needs
- When the team is solution-first and needs to refocus on user outcomes
- When existing feature requests lack clear "why" context

---

## Technique 4: Problem Statement Canvas

A structured template that forces precision in problem definition.

### Canvas Fields

```markdown
## Problem Statement Canvas

**Problem**: [One sentence describing the problem]

**Who is affected**: [Specific personas, not "everyone"]

**Impact**: [Quantified: cost, time, error rate, churn, revenue loss]

**Current behavior**: [How people cope today -- workarounds, manual processes]

**Desired outcome**: [What success looks like, measurably]

**Constraints**: [What limits the solution space]

**Scope boundary**: [Explicitly what is IN and OUT of scope]

**Evidence**: [Data, user quotes, metrics that prove this is real]
```

### Quality Checklist for Problem Statements

A good problem statement:
- [ ] Describes the problem, not a solution
- [ ] Names specific affected personas
- [ ] Quantifies impact with real data
- [ ] Is falsifiable (you could discover it is not actually a problem)
- [ ] Is scoped narrowly enough to be actionable
- [ ] Does not contain "we need to build..." or "we should implement..."

---

## Distinguishing Root Causes from Symptoms

### Symptom vs Root Cause Test

Ask: "If I fix this, does the problem go away permanently?"
- **Yes** -> Root cause (or close to it)
- **No, something else would still cause the same problem** -> Symptom

### Common Patterns

| Symptom (What You See) | Root Cause (What Actually Drives It) |
|------------------------|--------------------------------------|
| High customer churn | Unclear value proposition / poor onboarding |
| Slow process cycle time | Manual handoffs due to system gaps |
| Frequent data errors | No validation at point of entry |
| Stakeholder misalignment | No shared definition of success |
| Scope creep | Problem was never clearly defined |
| Low user adoption | Tool does not fit user workflow |

---

## Dependency Mapping Across Personas

When multiple personas are affected, map how their problems interconnect.

### Dependency Map Structure

1. List each persona's primary pain point
2. Draw arrows showing causal relationships between pain points
3. Identify which pain point, if resolved, would cascade relief to others
4. Prioritize the upstream cause

### Example

```
[Sales Rep: "I can't get accurate quotes"]
    |
    v  (depends on)
[Product Manager: "Pricing rules are not codified"]
    |
    v  (depends on)
[Finance: "We change pricing quarterly but don't update the system"]
    |
    v  (root)
[No process for propagating pricing changes to downstream systems]
```

The root cause is a process gap in Finance, but the visible symptom appears in Sales. Fixing Sales tooling alone would not resolve the problem.
