# Signal Router — Intelligent Technique & Pattern Selection

The signal router replaces the static technique selection matrix with context-aware auto-selection. Instead of asking the user "which technique do you want?", the agent detects signals from the user's input, context, and task category, then selects the optimal technique and hardening patterns automatically.

UNIX philosophy: the router is a pipe — raw signals in, technique + pattern selection out.

---

## How Signal Detection Works

### Phase 1: Extract Signals

From the user's input and gathered context, detect the presence of these signals:

| Signal | How to Detect |
|--------|---------------|
| `structured-output` | User mentions table, list, JSON, CSV, sections, headings, numbered items |
| `has-examples` | User provides or offers to provide input-output examples |
| `ambiguous-scope` | User says "it depends", "not sure exactly", "maybe", or describes competing requirements |
| `needs-reasoning` | Task involves math, logic, causality, debugging, "why does X happen" |
| `needs-exploration` | Task involves trade-offs, "what are my options", architectural decisions with branching paths |
| `needs-verification` | Task involves facts, real-world data, "is this correct", "verify this" |
| `needs-tool-use` | Task requires reading files, searching codebases, calling APIs, looking things up |
| `domain-knowledge` | Task requires specialized expertise — medical, legal, financial, technical depth |
| `multi-step` | Task has distinct phases: research → analyze → produce, or any A → B → C pipeline |
| `high-stakes` | User mentions production, compliance, audit, client-facing, board-level, legal |
| `generic-prone` | Task topic is well-trodden (marketing strategy, best practices, industry trends) |
| `has-constraints` | User specifies word limits, format rules, compliance requirements, deadlines |
| `direction-known` | User knows the angle/conclusion but wants the AI to develop it with evidence |
| `sequential-steps` | Task has 3+ ordered steps where output of step N feeds into step N+1 |
| `recommendation` | Task ends with a recommendation, decision, or choice between options |
| `strategic` | Task involves planning, strategy, roadmap, prioritization |

### Phase 2: Route to Technique

Apply the first matching rule (priority order):

```
IF needs-tool-use AND needs-verification → ReAct
IF multi-step AND sequential-steps      → Prompt Chaining
IF needs-exploration AND high-stakes     → Tree of Thought
IF needs-reasoning AND high-stakes       → Self-Consistency (CoT from 3 angles)
IF needs-reasoning                       → Chain-of-Thought
IF ambiguous-scope                       → Meta Prompting
IF domain-knowledge                      → Knowledge Generation
IF has-examples                          → Few-Shot
IF direction-known                       → Directional Stimulus
ELSE                                     → Zero-Shot
```

### Phase 3: Auto-Apply Hardening Patterns

Based on detected signals, layer hardening patterns (see HARDENING-PATTERNS.md):

```
ALWAYS apply                             → Anchor (output format)
IF has-constraints (2+)                  → Constraint Stack
IF domain-knowledge OR high-stakes       → Persona Boundary
IF generic-prone                         → Failure Injection + Specificity Ladder
IF needs-verification OR domain-knowledge → Confidence Gate
IF sequential-steps (3+)                 → Step Separator
IF strategic OR recommendation           → Assumption Audit
IF recommendation                        → Reframe Test (suggest, don't force)
IF high-stakes                           → Compression Command (for exec summary)
```

---

## Signal Detection Examples

### Example 1: Simple question
**Input**: "What's the difference between gRPC and REST?"
**Signals**: `needs-reasoning` (comparison)
**Technique**: Chain-of-Thought (reason through the comparison dimensions)
**Hardening**: Anchor (table format), Confidence Gate

### Example 2: Complex architecture task
**Input**: "Design a real-time notification system for our e-commerce platform. We have 500K DAU, need sub-second delivery, must work across web and mobile, and needs to handle flash sale events with 10x traffic spikes."
**Signals**: `needs-exploration`, `high-stakes`, `has-constraints`, `domain-knowledge`, `multi-step`
**Technique**: Tree of Thought (explore architectural options) + Prompt Chaining (multi-phase)
**Hardening**: Anchor, Constraint Stack, Persona Boundary, Assumption Audit, Step Separator

### Example 3: Code debugging
**Input**: "Our API response times spiked after deploying the new caching layer. Help me figure out why."
**Signals**: `needs-reasoning`, `needs-tool-use`, `needs-verification`
**Technique**: ReAct (interleave reasoning with investigation)
**Hardening**: Persona Boundary, Confidence Gate, Step Separator

### Example 4: Blog post
**Input**: "Write a blog post about why we chose Rust for our data pipeline. The angle: we tried Python first and hit performance walls."
**Signals**: `direction-known`, `has-constraints` (angle specified)
**Technique**: Directional Stimulus
**Hardening**: Anchor, Specificity Ladder

### Example 5: Research brief
**Input**: "I need a competitive analysis of the top 5 project management tools for a 200-person engineering org."
**Signals**: `domain-knowledge`, `recommendation`, `structured-output`, `generic-prone`
**Technique**: Knowledge Generation (generate knowledge about each tool) + Chain-of-Thought (reason through comparison)
**Hardening**: Anchor (comparison table), Confidence Gate, Specificity Ladder, Failure Injection, Assumption Audit

---

## Presenting the Selection

After auto-selecting, explain the choice concisely:

> "Based on your task, I'm using **[technique]** because [one-sentence reason]. I'm also applying **[patterns]** to [one-sentence benefit]. Does this approach sound right?"

The user can override:
- "Use few-shot instead" → Switch technique
- "Skip the reframe test" → Remove pattern
- "Add failure injection" → Add pattern
- "Just zero-shot, keep it simple" → Strip to minimal

---

## Escalation Rules

If signal detection is ambiguous (multiple techniques could apply equally well):

1. **Prefer the simpler technique** — Zero-Shot > Few-Shot > CoT > Meta > ToT
2. **Ask one clarifying question** — "This could be handled as a step-by-step analysis (Chain-of-Thought) or by exploring multiple approaches (Tree of Thought). Do you want depth on one path or a comparison of options?"
3. **Never block** — if in doubt, default to Chain-of-Thought with Confidence Gate. It's the safest general-purpose reasoning technique.
