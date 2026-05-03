# Verification Prompts: Multi-Dimensional Audit System

Use these prompts during Phase 4 (Verify) to systematically interrogate the output across seven axes. Each axis has a detection prompt, failure indicators, and fix guidance.

---

## How to Use

**Standard tier:** Run all 7 axes as an internal check. Fix failures silently. Present the final version with a brief summary of changes.

**Deep Humanise tier:** Run all 7 axes. Present the draft with a brief audit summary. Then run the meta-prompt ("What still sounds AI-generated?"), fix remaining issues, and present the final version.

---

## Axis 1: Cadence

**Detection prompt:** "Measure the sentence lengths in this passage. Do they genuinely vary, or do they cluster within a narrow range?"

**Failure indicators:**
- More than 60% of sentences fall between 15-25 words
- No sentences under 8 words
- No sentences over 30 words
- Three or more consecutive sentences of similar length

**Fix guidance:** Introduce deliberate variation. Break a medium sentence into a short one and a long one. Combine two medium sentences into one flowing sentence. Add a fragment for emphasis. The target burstiness pattern is specified in the active voice profile.

---

## Axis 2: Lexical Diversity

**Detection prompt:** "Are there words or phrases that repeat more than expected? Is vocabulary cycling through synonyms rather than using natural repetition?"

**Failure indicators:**
- The same transition word appears more than twice (e.g., "However" used three times)
- Synonym cycling: the same concept described with three different words in three consecutive sentences
- AI vocabulary cluster words present (check against the S2 pattern list)
- Absence of any unexpected or distinctly personal word choices

**Fix guidance:** Allow natural repetition of key terms (humans repeat words). Replace AI vocabulary with plain or voice-specific alternatives. Introduce at least one unexpected word choice per 200 words — the surprising verb, the telling adjective, the phrase that belongs to a person rather than an algorithm.

---

## Axis 3: Structural Predictability

**Detection prompt:** "Could someone guess the structure of the next paragraph from reading the previous ones? Does every paragraph follow the same internal pattern?"

**Failure indicators:**
- Every paragraph follows claim → evidence → implication
- Paragraphs are within 20% of each other in length
- Sections follow the expected template order (intro → context → analysis → conclusion)
- No digressions, callbacks, or structural surprises

**Fix guidance:** Vary paragraph architecture. Start one paragraph with a question. Let another build toward its conclusion rather than stating it first. Insert a short paragraph after a long one. Allow a genuine digression that earns its place. If the piece follows a predictable section order, break it — start with the most compelling point, not the chronological beginning.

---

## Axis 4: Emotional Authenticity

**Detection prompt:** "Do the emotional reactions in this text feel genuine, or do they feel performed? Would a real person use these exact words to express these feelings?"

**Failure indicators:**
- Reactions limited to: "interesting," "notable," "concerning," "impressive," "significant"
- Emotional statements that could apply to any topic ("this raises important questions")
- Absence of mixed feelings, genuine surprise, or honest uncertainty
- Emotions stated rather than demonstrated

**Fix guidance by voice:**
- `OX`: Understate with precision. "Rather unsettling" or "one can't help but notice." The emotion is real but the expression is measured.
- `SF`: Be direct. "This is broken" or "I keep coming back to this." Don't soften what doesn't need softening.
- `AB`: Be genuine and warm. "That's honestly harder than it sounds" or "I'm not sure we've got this right yet."
- `ST`: Be rich. "There is something quietly devastating about..." or "The irony is not lost, though it is seldom acknowledged." Emotion as analytical instrument.

---

## Axis 5: Voice Consistency

**Detection prompt:** "Does this output consistently match the target voice profile throughout, or does it drift between voices?"

**Failure indicators:**
- Spelling inconsistencies (mixing British and American)
- Sentence architecture shifts (starting with OX elegance, drifting to SF punchiness)
- Rhetorical style changes mid-piece
- Signature moves from the wrong voice appearing
- Tone shifts unexplained by content (becoming suddenly formal or informal without reason)

**Fix guidance:** Identify drift points and rewrite to match the target voice. Common drift patterns: reverting to AI-default neutral voice in the middle of a piece, losing voice-specific rhythm in technical sections, dropping regional character when discussing abstract topics. Technical content especially needs voice-profile attention — it's where most drift occurs.

---

## Axis 6: Specificity

**Detection prompt:** "Are claims grounded in concrete detail, or floating in abstraction? Where specific examples are given, are they real or synthetic?"

**Failure indicators:**
- Claims of importance without evidence ("this is crucial")
- Statistics without sources ("studies show that 70%...")
- Named examples that sound plausible but may be fabricated
- Abstractions where specifics would serve: "various stakeholders" instead of naming who
- "Recent research" without identifying the research

**Fix guidance:** Replace every abstract claim with a specific one. If a specific source isn't available, acknowledge it honestly: "I don't have a definitive number, but..." or "The commonly cited figure is X, though its provenance is debatable." Specificity is not the same as citing sources — it's about being concrete. "The team of twelve in the Manchester office" is more specific than "cross-functional stakeholders."

---

## Axis 7: The Read-Aloud Test

**Detection prompt:** "Read this text aloud (mentally). Does it sound like a person talking, or does it sound like text that was assembled?"

**Failure indicators:**
- Phrases that no human would say in conversation
- Rhythm that feels mechanical when vocalised
- Transitions that feel bolted on rather than flowing naturally
- Sentences that sound fine in print but awkward when spoken
- The overall impression is "written by committee" rather than "written by a person"

**Fix guidance:** Rewrite any sentence that fails the read-aloud test. The voice profiles provide the target speaking rhythm. OX should sound like an educated person in conversation — formal but not stiff. SF should sound like someone making a case in a meeting. AB should sound like someone explaining over coffee. ST should sound like someone commanding a room — oratorical but never pompous.

---

## Meta-Prompt (Deep Humanise Only)

After fixing all 7-axis failures, run this final check:

**"What makes the text below so obviously AI-generated? Identify specific remaining tells — not general categories but particular phrases, structural choices, or rhythm patterns that betray machine authorship."**

Answer in 3-5 brief, specific bullets. Then fix each identified issue. Present the final version.

---

## Quick-Reference Audit Matrix

| Axis | Quick Pass | Standard | Deep Humanise |
|------|-----------|----------|---------------|
| Cadence | Spot-check | Full check | Full check + fix |
| Lexical Diversity | Skip | Full check | Full check + fix |
| Structural Predictability | Skip | Full check | Full check + fix |
| Emotional Authenticity | Spot-check | Full check | Full check + fix |
| Voice Consistency | Spot-check | Full check | Full check + fix |
| Specificity | Skip | Full check | Full check + fix |
| Read-Aloud Test | Skip | Internal | Full check + fix |
| Meta-Prompt | Skip | Skip | Run + fix |
