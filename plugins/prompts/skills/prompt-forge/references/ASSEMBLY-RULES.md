# Prompt Assembly & Delivery — Full Reference

## Assembly Process

Follow these 13 composable layers to assemble the final prompt. Each layer is independent — include only layers that apply. Order matters: the prompt reads top-to-bottom in this sequence.

### Layer 1: Anchor (Output Format)
**Always include.** Define the exact output format before anything else. This locks the AI onto a structure before processing content.

```
Respond with [format]. No preamble. No explanation after the [format].
```

### Layer 2: Persona + Boundary
**Include when**: Persona Boundary hardening pattern is applied, or task requires domain expertise.

```
You are a [specific role] with [experience/expertise]. [Hard behavioral boundary — what you do NOT do].
```

### Layer 3: Objective
One clear sentence describing what needs to be produced. Avoid ambiguity.

```
[Clear instruction producing deliverable type] that [key requirement].
```

### Layer 4: Constraints (Before Context)
**Include when**: Constraint Stack hardening pattern is applied, or 2+ hard constraints exist. Place constraints BEFORE context — they are load-bearing, not afterthoughts.

```
Constraints:
- [Hard limit 1]
- [Hard limit 2]
- [Hard limit 3]
```

### Layer 5: Context
Background information, domain context, existing content references. This comes AFTER constraints when the Constraint Stack pattern is applied.

### Layer 6: Failure Guard
**Include when**: Failure Injection hardening pattern is applied. Show the wrong answer to avoid.

```
Here is the kind of response I do NOT want: [negative example]
[Explanation of why it fails]
```

### Layer 7: Technique Structure
Apply the selected prompt technique's pattern (see TECHNIQUES.md):
- **Tier 1**: Zero-Shot (direct instruction), Few-Shot (examples → task), Directional Stimulus (hints + cues)
- **Tier 2**: Meta (analyze → plan → execute), Knowledge Generation (generate → apply), Chain-of-Thought (step-by-step), Self-Consistency (3 angles → converge), Tree of Thought (explore → evaluate → select)
- **Tier 3**: ReAct (thought → action → observation loop), Prompt Chaining (sequential linked steps)

### Layer 8: Quality Gates
**Include when**: Confidence Gate and/or Assumption Audit hardening patterns are applied.

```
Do not include any claim you cannot support with specific reasoning.
List every assumption you are making before you begin.
```

### Layer 9: Step Control
**Include when**: Step Separator hardening pattern is applied. Converts bullet-list steps into hard stops.

```
Complete step 1 fully before beginning step 2. Show your output for each step before proceeding.
```

### Layer 10: Output Calibration
**Include when**: Specificity Ladder and/or Compression Command hardening patterns are applied.

```
Make every claim 3x more specific than your first instinct.
Compress the output to the N sentences that contain the most decision-relevant information.
```

### Layer 11: Artifact Instructions (if applicable)
When the output is a DOCX, XLSX, PPTX, or MD file:
- Include the humanize skill invocation with voice profile (see VOICE-PROFILES.md)
- Reference the appropriate document skill
- Specify the order: content first, humanize second, format third

### Layer 12: Verification Criteria
How to know the output is complete and correct:
- Checklist of required elements
- Quality benchmarks
- Audience-appropriateness check

### Layer 13: Reframe (Post-Output)
**Include when**: Reframe Test hardening pattern is applied. Always place last.

```
After presenting your recommendation, argue the strongest case against it. If both arguments are equally compelling, flag the decision as unresolved.
```

## Output Envelope

Wrap the assembled prompt in this structure when presenting to the user:

```markdown
## Forged Prompt

---

**Technique**: [Selected technique name]
**Hardening**: [Applied patterns, comma-separated, or "Anchor only" for minimal]
**Task Category**: [Category from Phase 1]
**Voice Profile**: [Selected profile, or "N/A" for non-artifacts]
**Complexity**: [Light / Standard / Deep]

---

[The comprehensive prompt text, ready to be used directly]

---

**Usage Notes**:
- [Platform recommendation: Claude Chat, Claude Code, etc.]
- [Suggested model: Opus for complex tasks, Sonnet for standard tasks]
- [If prompt chaining: sequence of execution steps]
- [Any caveats or customization points]
```

## Delivery Checklist

Before presenting the prompt, verify:

- [ ] Prompt is self-contained (runnable without additional context)
- [ ] Success criteria are included (how to know output is correct)
- [ ] Output format is specified (what the deliverable looks like)
- [ ] Correct technique pattern is applied
- [ ] Humanize skill + voice profile included (if artifact)
- [ ] Prompt is specific enough for consistent results
- [ ] No unnecessary padding or filler instructions
- [ ] Constraints from user dialogue are all represented

## Final Interaction

After presenting the prompt, ask:

> "Here's your generated prompt. Would you like me to:
> 1. **Execute it now** — I'll run this prompt immediately and produce the output
> 2. **Refine it** — Tell me what to adjust and I'll regenerate
> 3. **Save it** — I'll save this prompt as a file for later use
>
> What would you prefer?"

Handle each option:
- **Execute**: Take the generated prompt text and execute it directly in the current session as if the user had typed it. If the prompt references skills (humanize, docx, xlsx, pptx), invoke those skills as part of execution. For Prompt Chaining, execute each step sequentially and show intermediate outputs.
- **Refine**: Ask what to change via AskUserQuestion, update the relevant phase inputs, reassemble the prompt, and present the updated version. Repeat until the user is satisfied.
- **Save**: Write the prompt (including the output envelope with technique, category, voice profile, and usage notes) to a `.md` file in the current working directory. Suggest a filename like `prompt-forge-[task-summary].md`.
