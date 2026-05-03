---
name: humanize
description: >
  This skill should be used when the user asks to "humanize" text, "make this sound human",
  "rewrite in OX/SF/AB/ST voice", "remove AI patterns", "make this less AI", "edit for voice",
  "write like a human", or needs any text transformed to sound authentically human-written.
  Also triggers when generating new content with a voice shortcode (OX, SF, AB, ST) or when
  the user's personal preferences reference the humanize skill. Covers AI pattern detection,
  regional voice calibration, burstiness engineering, and multi-pass verification.
license: Complete terms in LICENSE.txt
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanize: Writing Transformation System

Transform AI-generated or AI-sounding text into genuinely human prose — or generate new content that reads as unmistakably human from the first word. This is not a pattern-removal checklist. It is a four-phase transformation system that detects, calibrates, transforms, and verifies.

The test: if someone reads the output and thinks "an AI wrote this," the skill has failed.

## Voice Shortcodes

Four regional English voices, each grounded in its origin and proud of it. Default is `OX` unless another is specified.

| Code | Voice | One-line |
|------|-------|----------|
| `OX` | Oxford English | Senior diplomat at Chatham House — quiet authority, educated warmth |
| `SF` | American English | Foggy Bottom meets Sand Hill Road — strategic gravitas, builder velocity |
| `AB` | Canadian English | Albertan prairie directness — no-nonsense warmth, global polish |
| `ST` | Indian English | Tharoorian eloquence calibrated for boardroom clarity — erudite yet precise |

When the user specifies a shortcode, load `references/voice-profiles.md` for the full voice specification. When no shortcode is given, apply `OX` as default.

## The Four Phases

### Phase 1: Detect

Scan the input for AI patterns across three levels. Consult `references/pattern-library.md` for the full taxonomy.

**Document level** — structural predictability, paragraph symmetry, formulaic section ordering, absence of genuine digressions or callbacks.

**Paragraph level** — cadence uniformity (sentences clustering around 18-22 words), semantic front-loading, the zoom-out reflex, transitional scaffolding.

**Sentence level** — the original tells: significance inflation, promotional language, -ing analyses, vague attributions, em dash overuse, rule of three, AI vocabulary words, negative parallelisms, sycophantic tone, filler phrases, excessive hedging, copula avoidance.

**Quick-reference — the 10 highest-signal patterns:**

1. **Significance inflation** — "pivotal moment," "enduring testament," "evolving landscape"
2. **AI vocabulary cluster** — additionally, crucial, delve, enhance, foster, garner, intricate, landscape, pivotal, showcase, tapestry, testament, underscore, vibrant
3. **Cadence uniformity** — every sentence roughly the same length and structure
4. **Copula avoidance** — "serves as," "stands as," "functions as" instead of "is"
5. **Superficial -ing phrases** — "highlighting," "underscoring," "reflecting," "symbolizing"
6. **Promotional language** — "groundbreaking," "nestled," "vibrant," "breathtaking," "renowned"
7. **Transitional scaffolding** — mechanical "That said," "To be sure," "What's more"
8. **Epistemic cowardice** — "some argue," "others contend" without taking a position
9. **Emotional flattening** — everything is "interesting" or "notable" but never genuinely felt
10. **Communication artefacts** — "Great question!", "I hope this helps!", "Let me know if..."

### Phase 2: Calibrate

Determine the target voice and register. This phase shapes everything that follows.

**If a shortcode is specified:** Load the corresponding profile from `references/voice-profiles.md`. Apply its full specification — spelling conventions, sentence architecture, rhetorical style, signature moves, and explicit avoidances.

**If no shortcode is specified:** Apply `OX` as default.

**Calibration checklist:**
- What is the output genre? (article, email, report, presentation, social post)
- What formality level does the voice profile call for?
- What spelling convention? (OX/ST: British; SF: American; AB: Canadian)
- What sentence architecture? (OX: elegant variation; SF: punchy-then-long; AB: steady with sharp punctuation; ST: architectural complexity with devastating one-liners)
- What rhetorical style? (OX: understatement; SF: direct thesis; AB: collaborative; ST: classical allusion)

### Phase 3: Transform

This is where the work happens. Two sub-phases, always in this order.

**3a. Subtract — Remove AI patterns**
Strip every identified AI pattern. Replace with constructions appropriate to the target voice. Do not simply delete — rewrite the surrounding context so the removal is seamless.

Key rewrites by voice:
- `OX`: Replace promotional language with measured assessment. Replace vague attributions with specific sources or honest acknowledgement of uncertainty.
- `SF`: Replace hedging with direct statements. Replace -ing phrases with active constructions. Cut filler ruthlessly.
- `AB`: Replace significance inflation with practical framing. Replace emotional flattening with genuine, understated reaction.
- `ST`: Replace simplistic constructions with architecturally richer sentences. Replace vague attributions with precise sourcing or eloquent acknowledgement of the unknown.

**3b. Add — Inject human qualities**
Removing AI patterns is necessary but insufficient. Actively inject the characteristics that make writing unmistakably human. Consult `references/advanced-techniques.md` for the full methodology.

**Burstiness** — Vary sentence length deliberately. Short sentences. Then longer ones that take their time, building through clauses, pausing where emphasis demands it, resuming with fresh energy. The target voice profile specifies the burstiness pattern.

**Structural asymmetry** — Break predictable structures. Not every paragraph should be the same length. Not every section should follow the same arc. Allow a short paragraph after a long one. Allow a digression that earns its place.

**Epistemic honesty** — Take positions. Acknowledge genuine uncertainty without hiding behind weasel words. "I don't know" is more human than "various experts have suggested."

**Specificity over abstraction** — Replace vague claims with concrete details. Not "a recent study" but the actual study, or honest acknowledgement that you're speaking from general knowledge.

**Genuine emotional texture** — Not "this is interesting" but what specifically is interesting about it and why it matters. Allow mixed feelings. Allow surprise. Allow the admission that something is complicated.

**Natural imperfections** — Thoughts that build rather than arrive fully formed. The slight digression. Starting with conjunctions when it feels right. Ending sentences with prepositions where they naturally belong. Occasional fragments for emphasis.

### Phase 4: Verify

Multi-pass verification. The depth depends on the operational tier.

**Tier selection:**
- **Quick Pass** (emails, messages, short pieces under 300 words): Single rewrite, spot-check the top 5 patterns, no formal audit loop.
- **Standard** (articles, reports, general content): Full pattern scan, voice calibration, single audit pass using the 7-axis check below.
- **Deep Humanise** (thought leadership, published work, high-stakes content): Full pattern scan, voice calibration, structural humanisation, multi-pass verification. Consult `references/verification-prompts.md`.

**The 7-axis audit** (Standard and Deep tiers):
1. **Cadence** — Do sentence lengths genuinely vary, or do they cluster?
2. **Lexical diversity** — Is the vocabulary natural and varied, or does it cycle through synonyms?
3. **Structural predictability** — Could someone guess the next paragraph's structure?
4. **Emotional authenticity** — Do reactions feel genuine or performative?
5. **Voice consistency** — Does the output match the target voice profile throughout?
6. **Specificity** — Are claims grounded in concrete detail or floating in abstraction?
7. **The read-aloud test** — Does it sound natural when read aloud, or does it sound "written by committee"?

For Standard tier: Run the 7-axis check internally, fix any failures, present the final version.

For Deep tier: Run the 7-axis check, present draft with brief self-assessment, then run a second pass asking "What still sounds AI-generated and why?" Fix remaining issues. Present final version.

## Output Format

**Quick Pass:** Present the rewritten text directly.

**Standard:**
1. Rewritten text
2. Brief summary of changes (3-5 lines maximum)

**Deep Humanise:**
1. Draft rewrite
2. 7-axis audit results (brief bullets)
3. Self-assessment: "What still sounds AI-generated?"
4. Final rewrite after second pass
5. Summary of changes

## Critical Rules

- Never use: "delve into," "it's worth noting that," "in today's fast-paced world," "the landscape of," "at the end of the day," "a testament to"
- Never produce inline-header vertical lists (bolded term followed by colon) unless the user explicitly requests bullet points
- Never use emojis unless the user explicitly requests them
- Never use title case in headings unless the style guide demands it
- Favour prose over lists. Write in paragraphs. Use natural inline enumeration ("three factors matter here: x, y, and z") rather than bullet points
- Preserve the user's core meaning. Humanisation changes how something is said, not what is said
- When generating new content (not editing existing text), apply the full four-phase process: detect patterns in your own draft, calibrate to the target voice, transform, and verify

## Reference Files

- **`references/pattern-library.md`** — Complete 30+ pattern taxonomy with examples and rewrites
- **`references/voice-profiles.md`** — Full specifications for all four voice profiles (OX, SF, AB, ST)
- **`references/verification-prompts.md`** — Multi-dimensional audit system with specific prompts per axis
- **`references/advanced-techniques.md`** — Structural humanisation, burstiness engineering, document-level transformation
