# Prompt Hardening Patterns

Composable patterns that harden any prompt against drift, hallucination, vagueness, and structural collapse. Apply these as layers on top of any technique — they are independent, stackable, and order-agnostic.

Each pattern is a small, focused unit (UNIX philosophy: do one thing well). The agent auto-selects which patterns to apply based on signal detection. Users can also request specific patterns by name.

---

## Pattern 1: The Anchor

**What it does**: Locks the AI onto a specific output format before it processes anything else.

**When to apply**: Every prompt that needs structured output. The anchor prevents the AI from drifting into narrative when you need a list, or a list when you need a table.

**Signal**: Task requires specific output structure (table, list, JSON, sections, numbered steps).

**Implementation**: Start the prompt with a single sentence defining the exact output format.

```
Respond only with a numbered list. No preamble. No explanation after the list.
```

**Why it works**: The AI processes the format constraint first, anchoring all subsequent reasoning to that structure. Without an anchor, the AI defaults to whatever format its training distribution favors.

---

## Pattern 2: The Constraint Stack

**What it does**: Moves constraints immediately after the core ask, before context — reversing the common (and less effective) pattern of ask → context → constraints.

**When to apply**: Any prompt with multiple constraints. Especially critical when constraints are non-negotiable (compliance, word limits, format rules).

**Signal**: 2+ hard constraints detected during context gathering.

**Implementation**: Structure as Ask → Constraints → Context.

```
Write a security audit report.
Constraints: Maximum 2 pages. Must reference NIST 800-53. No recommendations — findings only.
Context: The client runs a healthcare SaaS platform on AWS with 50K users...
```

**Why it works**: Constraints placed after context are treated as afterthoughts. Constraints placed immediately after the ask become load-bearing walls the AI builds around.

---

## Pattern 3: The Persona Boundary

**What it does**: Adds a hard behavioral boundary to the role assignment, not just a title.

**When to apply**: Any prompt with a role/persona. Without a boundary, the AI performs the role loosely — with one, it performs it precisely.

**Signal**: Task requires domain expertise, factual accuracy, or specific behavioral constraints.

**Implementation**: Role + explicit boundary condition.

```
You are a senior data scientist. You do not speculate. If data is missing, you say so explicitly.
```

```
You are a legal analyst specializing in GDPR. You distinguish between settled law and areas of active interpretation. You never present interpretations as settled law.
```

**Why it works**: The boundary activates the persona. Without it, "You are a senior data scientist" is just a label. With it, the AI has a concrete behavioral rule to enforce.

---

## Pattern 4: The Failure Injection

**What it does**: Shows the AI an example of the wrong answer before asking for the right one.

**When to apply**: When you've previously received generic, surface-level, or off-target outputs. When the task has a known failure mode.

**Signal**: Task is prone to generic outputs, boilerplate, or surface-level analysis. User has described what they don't want.

**Implementation**: Provide a negative example before the task.

```
Here is the kind of response I do NOT want:
"AI is transforming industries and creating new opportunities for growth and innovation."

That is too generic. I need specific mechanisms, named technologies, quantified impacts, and cited sources.

Now write: [actual task]
```

**Why it works**: Negative examples outperform positive examples at reducing generic output. The AI calibrates by avoidance — it sees the failure mode and steers away from it.

---

## Pattern 5: The Confidence Gate

**What it does**: Instructs the AI to exclude any claim it cannot support with specific reasoning.

**When to apply**: Any factual, research, or analytical task where hallucination risk is non-trivial.

**Signal**: Task involves facts, data, analysis, recommendations, or claims about the real world.

**Implementation**: Add a single constraint line.

```
Do not include any claim you cannot support with specific reasoning.
```

**Why it works**: The AI stops padding answers with plausible-sounding filler. Output length drops. Output accuracy climbs. The gate forces the AI to self-audit each claim before including it.

---

## Pattern 6: The Step Separator

**What it does**: Converts multi-step tasks from bullet lists into hard stops with explicit checkpoints.

**When to apply**: Multi-step workflows, sequential analysis, any task where step order matters and steps build on each other.

**Signal**: Task has 3+ sequential steps where output quality depends on completing each step fully before proceeding.

**Implementation**: Write steps as hard stops, not bullets.

```
Complete step 1. Stop. Wait for my confirmation. Then proceed to step 2.
```

Or for single-pass execution:

```
Complete step 1 fully before beginning step 2. Show your output for step 1 before proceeding.
```

**Why it works**: Agents that run all steps without stopping drift 60% more than agents that checkpoint. Hard stops force the AI to commit to each step's output before building on it.

---

## Pattern 7: The Compression Command

**What it does**: Compresses verbose AI output into decision-relevant information only.

**When to apply**: After any long AI output, or proactively when you need concise output from a complex task.

**Signal**: Task involves synthesis, summarization, executive communication, or decision support.

**Implementation**: Add as a post-processing instruction or as a primary constraint.

```
Compress the above into the 5 sentences that contain the most decision-relevant information.
```

Or proactively:

```
Your output must contain only decision-relevant information. No background context, no caveats, no hedging. Maximum 5 sentences.
```

**Why it works**: You get signal without noise. This pattern is particularly powerful for processing large volumes of information — research papers, logs, reports.

---

## Pattern 8: The Assumption Audit

**What it does**: Forces the AI to list every assumption it is making before beginning the analysis.

**When to apply**: Before any strategic, analytical, or planning task. Especially valuable when the problem space is ambiguous or the user hasn't provided complete context.

**Signal**: Task involves strategy, planning, analysis, recommendations, or any domain where hidden assumptions can invalidate conclusions.

**Implementation**: Add before the task instruction.

```
List every assumption you are making before you begin.
```

**Why it works**: The AI surfaces hidden reasoning that would otherwise be buried inside confident-sounding answers. You can then challenge or correct assumptions before the AI builds an entire analysis on a faulty foundation.

---

## Pattern 9: The Reframe Test

**What it does**: After receiving an AI recommendation, instructs the AI to argue the opposite position with equal conviction.

**When to apply**: After any recommendation, analysis, or position statement. Use this to stress-test whether the AI's analysis has substance or is just pattern-matching to the most likely answer.

**Signal**: Task involves recommendations, strategic decisions, technology choices, or any conclusion that should survive adversarial scrutiny.

**Implementation**: Run as a follow-up instruction.

```
Now argue the opposite position with equal conviction.
```

Or embed proactively:

```
After presenting your recommendation, argue the strongest case against it. If both arguments are equally compelling, flag the decision as unresolved.
```

**Why it works**: If the AI can argue both sides with equal strength, the original recommendation lacked substance. The reframe test is the fastest way to find weak analysis.

---

## Pattern 10: The Specificity Ladder

**What it does**: Forces every claim to become 3x more specific than the AI's first instinct.

**When to apply**: When outputs feel generic, vague, or could apply to any situation. When you need actionable specificity.

**Signal**: Task requires actionable outputs, implementation details, or specific recommendations rather than general advice.

**Implementation**: Add as a constraint.

```
Make every claim 3x more specific than your first instinct.
```

**Calibration examples**:
- Generic: "Improve your marketing."
- Specific: "Run a 3-email sequence targeting users who clicked but did not purchase in the last 14 days, with subject lines under 40 characters, sent Tuesday/Thursday at 10am EST."

- Generic: "Use a microservices architecture."
- Specific: "Extract the payment processing domain into a separate service behind a gRPC API, deployed as an AKS pod with a 200ms P99 latency SLA, using the Saga pattern for distributed transactions with the order service."

**Why it works**: The AI's training distribution favors safe, general statements. The specificity ladder overrides this default, forcing concrete, actionable output.

---

## Auto-Application Rules

The prompt-forge agent applies hardening patterns automatically based on detected signals. Here is the default application matrix:

| Task Signal | Auto-Applied Patterns |
|-------------|----------------------|
| Structured output needed | Anchor |
| 2+ hard constraints | Constraint Stack |
| Role/persona assigned | Persona Boundary |
| Factual/research task | Confidence Gate |
| 3+ sequential steps | Step Separator |
| Analytical/strategic task | Assumption Audit |
| Recommendation output | Reframe Test (optional — suggest to user) |
| Generic-prone task | Specificity Ladder, Failure Injection |
| Decision support | Compression Command |
| All prompts | Anchor (always — output format is always relevant) |

## Hardening Cap

**Maximum 4 hardening patterns per prompt** (plus Anchor, which is structural and does not count toward the cap). Over-hardening bloats prompts and creates conflicting instructions.

When more than 4 patterns trigger, prioritize by task relevance:

1. **Structural patterns first**: Constraint Stack, Step Separator (these shape the prompt's skeleton)
2. **Quality gates second**: Confidence Gate, Assumption Audit, Persona Boundary (these prevent bad output)
3. **Calibration third**: Specificity Ladder, Compression Command, Failure Injection (these tune output quality)
4. **Verification last**: Reframe Test (this is post-output — suggest rather than embed if at cap)

If the cap forces a trade-off, tell the user which patterns were dropped and why:

> "I applied **Constraint Stack**, **Persona Boundary**, **Confidence Gate**, and **Assumption Audit**. I skipped Specificity Ladder (your constraints are already specific enough) and Reframe Test (I can run it as a follow-up instead). Want me to add either back?"

## Composition Rules

Patterns compose freely within the cap. Common stacks:

- **Research stack**: Anchor + Confidence Gate + Assumption Audit + Compression Command
- **Strategy stack**: Persona Boundary + Assumption Audit + Reframe Test + Specificity Ladder
- **Execution stack**: Anchor + Constraint Stack + Step Separator + Specificity Ladder
- **Analysis stack**: Persona Boundary + Confidence Gate + Failure Injection + Reframe Test

When stacking, embed patterns in this order within the prompt:
1. Anchor (output format — always first)
2. Persona Boundary (role + boundary)
3. Constraint Stack (ask → constraints → context)
4. Failure Injection (negative examples)
5. Confidence Gate / Assumption Audit (quality gates)
6. Step Separator (execution structure)
7. Specificity Ladder / Compression Command (output calibration)
8. Reframe Test (post-output verification)
