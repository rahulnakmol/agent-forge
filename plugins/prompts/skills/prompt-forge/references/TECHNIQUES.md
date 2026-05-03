# Prompt Engineering Techniques — Full Reference

Techniques are organized into three tiers based on reasoning complexity. The agent selects techniques based on signal detection (see SIGNAL-ROUTER.md), not user self-assessment.

**Tier 1 — Direct**: Single-pass, no explicit reasoning structure needed.
**Tier 2 — Reasoning**: Explicit reasoning steps that improve accuracy on complex tasks.
**Tier 3 — Agentic**: Multi-turn, tool-using, or self-correcting patterns for autonomous work.

---

# Tier 1: Direct Techniques

## Technique 1: Zero-Shot Prompting

**When to use**: The task is straightforward, well-defined, and doesn't require examples to illustrate the expected output. The user has provided clear enough context that a direct instruction will suffice.

**How it works**: A single, clear instruction with all necessary context embedded directly. No examples needed.

**Best for**: Simple queries, standard document formats, well-understood coding tasks, factual research.

**Prompt pattern**:
```
[Role/Context] + [Clear instruction] + [Constraints] + [Output format]
```

**Example**:
```
You are a senior technical writer. Write a 500-word overview of Kubernetes pod autoscaling for a developer audience. Use clear language, include one concrete example, and end with three best practices. Format as Markdown with H2 headings.
```

---

## Technique 2: Few-Shot Prompting

**When to use**: The desired output has a specific style, format, or pattern that is best communicated through examples. The user has (or can provide) 2-5 examples of what good output looks like.

**How it works**: Provide 2-5 examples of input-output pairs before the actual task, so the model learns the pattern.

**Best for**: Consistent formatting tasks, style-matching, classification, data transformation, any task where "show don't tell" is more efficient.

**If selecting this technique**, ask:
> "To get the best results, I'd like to include a few examples in the prompt. Can you share 2-3 examples of what good output looks like for this task? Or should I generate representative examples based on what you've described?"

**If the user asks you to generate examples**: Create 2-3 representative input-output pairs that match the task's domain, format, and complexity. Make them realistic but clearly illustrative — each example should demonstrate a different aspect of the expected output pattern (e.g., one short input, one complex input, one edge case). Present the generated examples to the user for approval before embedding them in the final prompt.

**Prompt pattern**:
```
[Role/Context]

Example 1:
Input: [sample input]
Output: [sample output]

Example 2:
Input: [sample input]
Output: [sample output]

Example 3:
Input: [sample input]
Output: [sample output]

Now complete this task:
Input: [actual input]
Output:
```

**Example**:
```
You are a changelog writer. Convert commit messages into user-friendly changelog entries.

Example 1:
Input: fix(auth): resolve token refresh race condition in concurrent sessions
Output: Fixed an issue where users could be unexpectedly logged out during heavy usage.

Example 2:
Input: feat(dashboard): add real-time notification bell with unread count badge
Output: Added a notification bell to the dashboard that shows your unread notification count in real time.

Now convert this:
Input: refactor(api): migrate REST endpoints to use new validation middleware
Output:
```

---

# Tier 2: Reasoning Techniques

## Technique 3: Meta Prompting

**When to use**: The task is complex, ambiguous, or requires the AI to reason about HOW to approach the problem before executing. The user wants the AI to first plan its approach, then execute.

**How it works**: The prompt instructs the AI to first analyze the task, develop a strategy, and then execute that strategy. Essentially, the AI writes its own sub-prompts.

**Best for**: Complex research, multi-faceted analysis, architectural decisions, tasks where the approach itself is uncertain.

**Prompt pattern**:
```
[Role/Context]

Before executing, first analyze this task and outline your approach:
1. What are the key dimensions to consider?
2. What information do you need to gather or generate?
3. What structure will best serve the audience?
4. What are the potential pitfalls?

Then execute your plan step by step, showing your reasoning.

Task: [Task description]

Quality criteria: [Success measures]
```

**Example**:
```
You are a solutions architect evaluating cloud migration strategies.

Before making recommendations, first:
1. Identify the key decision factors for this specific workload
2. Map the current architecture's dependencies and constraints
3. Evaluate at least 3 migration approaches against these factors
4. Assess risks and mitigation strategies for each

Then present your analysis and recommendation.

Task: The client runs a monolithic Java ERP system on-premises with 500 concurrent users, a 2TB Oracle database, and strict compliance requirements (SOX, GDPR). They want to move to Azure within 18 months.

Quality criteria: Recommendation must address cost, risk, timeline, and compliance. Include a phased migration roadmap.
```

---

## Technique 4: Knowledge Generation Prompting

**When to use**: The task requires the AI to first generate or surface relevant knowledge before using that knowledge to complete the task. Useful when the answer depends on synthesizing multiple pieces of information.

**How it works**: Two-stage prompt — first generate relevant facts, frameworks, or background knowledge, then use that generated knowledge to produce the final output.

**Best for**: Expert analysis, technical deep-dives, comparative studies, tasks requiring domain expertise, informed recommendations.

**Prompt pattern**:
```
[Role/Context]

Stage 1 — Knowledge Generation:
First, generate the key facts, frameworks, and principles relevant to [topic]. Consider:
- [Dimension 1]
- [Dimension 2]
- [Dimension 3]

Stage 2 — Application:
Now, using the knowledge you've generated above, [actual task instruction].

Output format: [Specification]
```

**Example**:
```
You are a cybersecurity consultant.

Stage 1 — Knowledge Generation:
First, generate the key facts and frameworks relevant to zero-trust architecture in healthcare settings. Consider:
- HIPAA and HITECH compliance requirements
- Common threat vectors in healthcare IT
- Zero-trust maturity models (CISA, Forrester, NIST 800-207)
- Network segmentation patterns for medical devices

Stage 2 — Application:
Using this knowledge, write a 3-page executive briefing recommending a zero-trust adoption roadmap for a 500-bed hospital system currently using perimeter-based security. Include a 12-month phased approach with quick wins in the first quarter.

Output format: Executive briefing with sections: Current Risk Landscape, Recommended Approach, Phased Roadmap, Budget Estimates, Quick Wins.
```

---

## Technique 5: Chain-of-Thought (CoT)

**When to use**: The task requires multi-step reasoning — math, logic, causal analysis, debugging, or any problem where the answer depends on intermediate steps. The AI needs to "show its work" to reach an accurate conclusion.

**How it works**: Instruct the AI to reason step-by-step before producing a final answer. This can be zero-shot ("Let's think step by step") or few-shot (provide examples with explicit reasoning chains).

**Best for**: Mathematical reasoning, logical deduction, causal analysis, debugging, multi-constraint optimization, decision trees.

**Prompt pattern (zero-shot CoT)**:
```
[Role/Context]

[Task description]

Let's think through this step by step before reaching a conclusion.
```

**Prompt pattern (few-shot CoT)**:
```
[Role/Context]

Example:
Q: [Sample problem]
A: Let's think step by step.
Step 1: [reasoning]
Step 2: [reasoning]
Step 3: [reasoning]
Therefore: [answer]

Now solve:
Q: [Actual problem]
A: Let's think step by step.
```

**Example**:
```
You are a systems architect evaluating database choices.

Our application processes 10,000 transactions/second with complex joins across 5 tables, requires ACID compliance, and must support real-time analytics on the same dataset. We currently use PostgreSQL 14 and are considering adding a read replica vs. migrating to CockroachDB.

Let's think through this step by step, evaluating each option against our specific requirements before making a recommendation.
```

---

## Technique 6: Self-Consistency

**When to use**: The task has a deterministic correct answer but the AI might reach it inconsistently. You want higher confidence by generating multiple reasoning paths and selecting the most consistent conclusion.

**How it works**: Instruct the AI to approach the problem from multiple independent angles, then identify where the conclusions converge. This is essentially "take the majority vote across reasoning paths."

**Best for**: Complex analysis with a definitive answer, risk assessment, technical evaluation, any task where you want to reduce variance in the output.

**Prompt pattern**:
```
[Role/Context]

[Task description]

Approach this problem from 3 independent angles:

Approach 1: [Frame/perspective A]
Approach 2: [Frame/perspective B]
Approach 3: [Frame/perspective C]

For each approach, reason through to a conclusion independently.

Then: Compare your conclusions. Where do they converge? Where do they diverge? Present the conclusion supported by the most approaches, and flag any divergences as areas of uncertainty.
```

**Example**:
```
You are a security consultant assessing whether a proposed API design is safe for production.

Approach this from 3 independent angles:
1. Attack surface analysis (STRIDE model)
2. Data flow analysis (trace every piece of user input)
3. Compliance lens (OWASP Top 10 checklist)

For each, reason through to a security verdict independently. Then compare: where do all three agree there's a risk? Those are your high-confidence findings.
```

---

## Technique 7: Tree of Thought (ToT)

**When to use**: The task requires exploring multiple solution paths where early decisions constrain later options. Problems where backtracking might be necessary — strategic planning, architectural design, creative problem solving.

**How it works**: The AI generates multiple candidate approaches, evaluates each partially, prunes unpromising branches, and continues developing the most promising paths. Think chess: consider several opening moves, evaluate the board position after each, pursue the strongest line.

**Best for**: Strategic planning, architectural decisions with trade-offs, creative problem solving, optimization problems, game-like decision trees.

**Prompt pattern**:
```
[Role/Context]

[Problem description]

Explore this problem using a tree of thought approach:

Step 1 — Generate 3 distinct approaches to this problem.
Step 2 — For each approach, reason forward 2-3 steps. What does the solution look like if you continue down this path?
Step 3 — Evaluate each path: feasibility, risk, quality of outcome.
Step 4 — Select the strongest path and develop it fully. Explain why the alternatives were weaker.
```

**Example**:
```
You are an engineering manager redesigning the deployment pipeline for a monorepo with 12 services.

Current pain: deployments take 45 minutes, any failure blocks all services, rollbacks require manual intervention.

Explore 3 distinct approaches:
1. Parallel independent pipelines per service
2. Dependency-aware orchestrated pipeline
3. Trunk-based with feature flags and progressive rollout

For each, reason forward: what does the pipeline look like? What breaks? What's the operational burden? Then select and develop the strongest option fully.
```

---

## Technique 8: Directional Stimulus

**When to use**: You know the direction you want the output to go but don't want to over-constrain it. You want to nudge the AI toward a specific angle, style, or conclusion without dictating the answer.

**How it works**: Provide hints, cues, or directional signals that guide the AI's generation without prescribing the exact output. Like giving a writer a theme rather than an outline.

**Best for**: Creative tasks with a desired direction, analysis where you want a specific lens applied, content generation with tone/angle guidance, brainstorming with focus.

**Prompt pattern**:
```
[Role/Context]

[Task description]

Direction: [Hint, cue, or guiding signal]
Consider especially: [Specific angle or emphasis]
The output should lean toward: [Quality or characteristic]
```

**Example**:
```
You are a product strategist writing a competitive analysis of Notion vs. Obsidian.

Direction: The audience is a CTO evaluating which tool to standardize for a 200-person engineering org.
Consider especially: the total cost of ownership including migration, training, and plugin maintenance.
The output should lean toward: practical decision criteria rather than feature comparison.
```

---

# Tier 3: Agentic Techniques

## Technique 9: ReAct (Reasoning + Acting)

**When to use**: The task requires the AI to interleave reasoning with actions — looking things up, checking facts, using tools, or gathering information before continuing analysis. The AI can't answer from knowledge alone; it needs to act in the world.

**How it works**: The prompt instructs the AI to alternate between Thought (reasoning about what to do next), Action (performing an operation — search, read, calculate), and Observation (processing the result). This loop continues until the task is complete.

**Best for**: Research tasks requiring verification, code debugging with codebase exploration, fact-checking, tasks requiring tool use, information gathering with synthesis.

**Prompt pattern**:
```
[Role/Context]

[Task description]

Work through this using a Thought → Action → Observation loop:

Thought: [What do I need to figure out? What's my current understanding?]
Action: [What do I need to do? Search, read, calculate, verify?]
Observation: [What did I learn from that action?]

Repeat until you have enough information to produce the final output.

Then synthesize your observations into: [Final deliverable]
```

**Example**:
```
You are a tech lead investigating a production performance regression.

The P99 latency for the /api/orders endpoint jumped from 120ms to 800ms after last Thursday's deployment.

Work through this systematically:
Thought: What could cause a 6x latency increase? What changed in Thursday's deployment?
Action: Review the deployment diff, check database query plans, examine connection pool metrics.
Observation: [Process what you find]

Continue until you can identify the root cause and propose a fix. Present your findings as: Root Cause → Evidence → Fix → Verification Plan.
```

---

## Technique 10: Prompt Chaining

**When to use**: The task is too complex for a single prompt. It has distinct phases where the output of one phase feeds into the next. The user wants a multi-step workflow.

**How it works**: Break the task into a sequence of linked prompts, where each prompt's output becomes the input for the next. The final generated prompt will instruct the agent to work through these phases sequentially.

**Best for**: End-to-end workflows, document pipelines (research → outline → draft → review), multi-artifact tasks, complex code features with dependencies.

**Prompt pattern**:
```
This task requires a multi-step approach. Execute each step sequentially, using the output of each step as input for the next.

--- Step 1: [Phase name] ---
[First prompt instruction]
Produce: [Intermediate deliverable description]

--- Step 2: [Phase name] ---
Using the output from Step 1, [second prompt instruction]
Produce: [Intermediate deliverable description]

--- Step 3: [Phase name] ---
Using the output from Step 2, [third prompt instruction]
Produce: [Final deliverable description]

Quality gate: After each step, verify [criteria] before proceeding.
```

**Example**:
```
This task requires a multi-step approach. Execute each step sequentially.

--- Step 1: Research ---
Research the top 5 CRM platforms for mid-market B2B SaaS companies (50-500 employees). For each, identify: pricing model, key features, integration ecosystem, and known limitations. Produce a structured comparison table.

--- Step 2: Analysis ---
Using the comparison from Step 1, analyze which platforms best fit a company with these requirements: HubSpot Marketing Hub integration, Salesforce migration path, under $100/user/month, strong API for custom integrations. Produce a ranked shortlist of 3 with pros/cons.

--- Step 3: Recommendation ---
Using the analysis from Step 2, write a 1-page executive recommendation memo addressed to the VP of Sales. Include the top pick, runner-up, migration considerations, and estimated timeline. Produce the final memo.

Quality gate: After each step, verify completeness before proceeding.
```

---

## Technique Selection Matrix

| Signal | Reasoning Needed? | Examples Available? | Multi-Phase? | Technique |
|--------|-------------------|--------------------|--------------|-----------------------|
| Simple, clear task | No | No | No | **Zero-Shot** |
| Pattern/style matching | No | Yes (2-5) | No | **Few-Shot** |
| Ambiguous, needs strategy | Yes (approach) | No | No | **Meta** |
| Domain knowledge required | Yes (knowledge) | No | No | **Knowledge Generation** |
| Multi-step reasoning | Yes (steps) | No | No | **Chain-of-Thought** |
| High-stakes, need confidence | Yes (multiple paths) | No | No | **Self-Consistency** |
| Branching decisions/trade-offs | Yes (exploration) | No | No | **Tree of Thought** |
| Direction known, not outcome | No | No | No | **Directional Stimulus** |
| Requires tool use/verification | Yes (interleaved) | No | No | **ReAct** |
| Multi-step workflow | N/A | N/A | Yes | **Prompt Chaining** |

See [SIGNAL-ROUTER.md](SIGNAL-ROUTER.md) for the full signal-based auto-selection logic.

## Combining Techniques

Techniques compose. Common combinations:

**Tier 1 + Tier 1**:
- **Few-Shot + Directional Stimulus**: Show examples, nudge toward a specific angle

**Tier 1 + Tier 2**:
- **Few-Shot + Chain-of-Thought**: Examples with explicit reasoning chains
- **Knowledge Generation + Chain-of-Thought**: Generate knowledge, then reason through it step by step

**Tier 2 + Tier 2**:
- **Meta + Self-Consistency**: Plan the approach, then verify from multiple angles
- **Chain-of-Thought + Tree of Thought**: Reason step-by-step within each branch of exploration

**Tier 2 + Tier 3**:
- **Chain-of-Thought + ReAct**: Reason, act, observe — with explicit reasoning at each step

**Tier 3 + Tier 1**:
- **Prompt Chaining + Zero-Shot**: Simple steps sequenced into a pipeline
- **Prompt Chaining + Few-Shot**: Complex workflow where each step needs examples

**Cross-tier stack** (for maximum-complexity tasks):
- **Meta + Knowledge Generation + Chain-of-Thought + Prompt Chaining**: Analyze approach → generate knowledge → reason step-by-step → execute in phases

When combining, explain to the user why and how the techniques complement each other. Prefer the simplest technique that achieves the goal — don't over-engineer the prompt.
