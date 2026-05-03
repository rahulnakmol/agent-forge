# Pattern Library: Complete AI Writing Tell Taxonomy

30+ patterns organised by level (document, paragraph, sentence) and category. Each pattern includes: what to detect, why it matters, and how to rewrite. Based on Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup) plus 2025-2026 stylometric and linguistic research.

---

## Document-Level Patterns

### D1. Structural Predictability
**Detect:** Introduction → Context → Analysis → Conclusion, every time. Sections arrive in the same order regardless of content. No genuine digressions, callbacks, or structural surprises.

**Why it matters:** Human writers organise by what the content demands. AI organises by template. Stylometric analysis (UCC, 2025) confirmed that structural uniformity is a primary fingerprint.

**Rewrite:** Let the content dictate structure. Start with the most compelling point, not the chronological beginning. Allow a section that circles back to an earlier idea. Break the expected order when it serves clarity.

### D2. Paragraph Symmetry
**Detect:** Paragraphs cluster around the same length (typically 3-5 sentences, 60-100 words each). No short punchy paragraphs. No long developed ones. Everything is medium.

**Why it matters:** Human writing has natural asymmetry. A two-sentence paragraph followed by a ten-sentence paragraph is normal. Uniform paragraph length is a burstiness failure.

**Rewrite:** Deliberately vary paragraph lengths. Allow a one-sentence paragraph for emphasis. Allow a long paragraph when the argument demands development.

### D3. The Zoom-Out Reflex
**Detect:** Opening paragraphs that compulsively contextualise: "In a world where..." "In today's rapidly evolving..." "As technology continues to transform..." The text starts at 30,000 feet before descending to the actual topic.

**Why it matters:** Human writers usually start with the specific and zoom out only when context is needed. AI starts broad because it's hedging — the statistical middle is always safer.

**Rewrite:** Start specific. Start with the point, the anecdote, the concrete detail. Contextualise only when the reader needs it, not as a preamble.

### D4. Formulaic Challenges-and-Prospects Sections
**Detect:** "Despite its [positive quality], [subject] faces several challenges..." followed by "Despite these challenges, [optimistic conclusion]." Nearly always near the end.

**Why it matters:** This is pure template. Real analysis integrates challenges throughout rather than quarantining them into a formulaic section.

**Rewrite:** Integrate challenges where they naturally arise. If a challenge relates to a specific point, discuss it there. Drop the formulaic "despite these challenges" redemption arc.

---

## Paragraph-Level Patterns

### P1. Cadence Uniformity (Low Burstiness)
**Detect:** Sentences cluster around 18-22 words. Uniform Subject-Verb-Object structure. The rhythm is metronomic — no short punches, no long flowing sentences, everything is medium.

**Why it matters:** This is the single most reliable discriminator in 2025-era detection. Human "burstiness" (mixing short and long sentences naturally) is extremely difficult for AI to replicate consistently. Perplexity and burstiness analysis remain central to AI detection.

**Rewrite by voice:**
- `OX`: Elegant variation — a short declarative followed by a longer sentence with subordinate clauses. The occasional fragment.
- `SF`: Punchy-then-long — a headline sentence ("Here's the thing.") followed by developed reasoning.
- `AB`: Steady with sharp punctuation — generally even rhythm but allow a short sentence to land when emphasis demands it.
- `ST`: Architectural complexity — longer sentences that reward attention, punctuated by devastating short ones. Semicolons used with genuine purpose.

### P2. Semantic Front-Loading
**Detect:** Every paragraph leads with its conclusion, then elaborates predictably. The structure is always: claim → evidence → implication. No paragraphs that build toward a realisation.

**Why it matters:** Human writers sometimes lead with the conclusion, sometimes build toward it, sometimes discover it mid-paragraph. AI always front-loads because it's generating token by token.

**Rewrite:** Vary paragraph architecture. Sometimes lead with a question. Sometimes build through evidence toward a conclusion. Sometimes start with an observation and let the implication emerge.

### P3. Transitional Scaffolding
**Detect:** Mechanical deployment of: "That said," "To be sure," "What's more," "Moreover," "Furthermore," "Additionally," "In contrast," "On the other hand." These appear at paragraph beginnings with algorithmic regularity.

**Why it matters:** Human writers use transitions less frequently and more organically. The connection between paragraphs is usually implicit in the content, not announced by a transition word.

**Rewrite:** Remove most transitional phrases. Let the logic of the argument provide the connection. When a transition is genuinely needed, vary the construction — or use a full sentence that bridges ideas rather than a stock phrase.

### P4. Emotional Flattening
**Detect:** Reactions are uniformly mild: "interesting," "notable," "concerning," "impressive," "significant." No genuine surprise, discomfort, delight, frustration, or ambivalence.

**Why it matters:** Real humans have specific emotional responses. "This is terrifying" or "I keep coming back to this" or "honestly, I'm not sure what to make of it" — these signal a person behind the words.

**Rewrite by voice:**
- `OX`: Understated but precise emotional register. "Rather unsettling" carries more weight than "concerning."
- `SF`: Direct and occasionally blunt. "This is a problem" rather than "this presents challenges."
- `AB`: Genuine warmth or honest scepticism. "I'm not entirely convinced" rather than "some may disagree."
- `ST`: Rich emotional texture through language. Allow wonder, allow indignation, allow the eloquent admission of uncertainty.

### P5. Epistemic Cowardice
**Detect:** "Some argue that..." "Others contend..." "Various experts have suggested..." "There is debate about..." — the text never takes a position. It presents "both sides" without committing to anything.

**Why it matters:** Human writers (especially good ones) take positions. They may acknowledge counterarguments, but they don't hide behind permanent neutrality.

**Rewrite:** Take a position where appropriate. Acknowledge the counterargument, then explain why the position holds. "Some argue X, and they have a point about Y, but the evidence for Z is stronger because..."

---

## Sentence-Level Patterns

### S1. Significance Inflation
**Words to detect:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, marking/shaping the, represents a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Rewrite:** State what actually happened. Replace claims of importance with evidence of importance.

### S2. AI Vocabulary Cluster
**High-frequency words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant, nuanced, multifaceted, realm, paradigm, synergy

**Rewrite:** Use plain equivalents. "Important" not "crucial." "Show" not "showcase." "Complex" not "intricate." Or better yet, be specific about what makes something important or complex.

### S3. Copula Avoidance
**Words to detect:** serves as, stands as, marks, represents [a], boasts, features, offers [a], functions as

**Rewrite:** Use "is," "are," "has," "was." "The gallery is an exhibition space" not "The gallery serves as an exhibition space."

### S4. Superficial -ing Analyses
**Words to detect:** highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, showcasing

**Rewrite:** Cut the -ing phrase entirely. If the information is important, give it its own sentence. If it isn't, cut it.

### S5. Promotional Language
**Words to detect:** boasts a, vibrant, rich (figurative), profound, enhancing its, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning, cutting-edge, state-of-the-art, world-class

**Rewrite:** Replace with specific descriptive language. Not "a stunning vista" but "the valley drops 800 metres to the river below."

### S6. Vague Attributions / Weasel Words
**Words to detect:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources, according to multiple studies, research suggests

**Rewrite:** Name the source. "A 2024 McKinsey report found..." If you don't have a specific source, acknowledge it: "I haven't seen definitive data on this, but..."

### S7. Negative Parallelisms
**Detect:** "Not only...but..." "It's not just about..., it's..." "It's not merely X, it's Y."

**Rewrite:** State the positive directly. "The beat adds to the aggressive tone" rather than "It's not just about the beat; it's about the aggression."

### S8. Rule of Three Overuse
**Detect:** Ideas forced into groups of three. "Innovation, inspiration, and industry insights." "Streamlining processes, enhancing collaboration, and fostering alignment."

**Rewrite:** Use the number of items the content actually requires. Two is fine. Four is fine. The number three is not inherently superior.

### S9. Elegant Variation (Synonym Cycling)
**Detect:** "The protagonist... The main character... The central figure... The hero..." — excessive synonym substitution to avoid repetition.

**Rewrite:** Repeat the same word if that's clearest. Humans repeat words. Algorithms cycle synonyms.

### S10. False Ranges
**Detect:** "From X to Y" constructions where X and Y aren't on a meaningful scale. "From the Big Bang to the cosmic web, from star formation to dark matter."

**Rewrite:** List items directly without pretending they form a spectrum.

### S11. Em Dash Overuse
**Detect:** More than one em dash per 200 words, or em dashes used where commas or full stops would be more natural.

**Rewrite:** Replace most em dashes with commas, full stops, or parentheses. Reserve em dashes for genuine asides — one per piece at most, two if the piece is long.

### S12. Overuse of Boldface
**Detect:** Mechanical bolding of key terms, especially in lists. **Term:** followed by explanation.

**Rewrite:** Remove most bolding. If emphasis is needed, let sentence structure and word choice carry it.

### S13. Inline-Header Vertical Lists
**Detect:** Lists where each item starts with a bolded header followed by a colon and explanation.

**Rewrite:** Convert to prose. "The update improves three things: the interface, load times, and encryption."

### S14. Communication Artefacts
**Detect:** "I hope this helps!" "Of course!" "Certainly!" "Great question!" "Would you like me to..." "Let me know if..."

**Rewrite:** Remove entirely. These are chatbot artefacts, not content.

### S15. Sycophantic Tone
**Detect:** "You're absolutely right!" "That's an excellent point!" "What a great question!"

**Rewrite:** Engage with the substance rather than praising the question.

### S16. Filler Phrases
**Common fillers:** "In order to" → "To." "Due to the fact that" → "Because." "At this point in time" → "Now." "It is important to note that" → (cut entirely). "Has the ability to" → "Can."

### S17. Excessive Hedging
**Detect:** "It could potentially possibly be argued that..." Multiple qualifiers stacked.

**Rewrite:** One qualifier maximum. "The policy may affect outcomes."

### S18. Generic Positive Conclusions
**Detect:** "The future looks bright." "Exciting times lie ahead." "A major step in the right direction."

**Rewrite:** End with a specific fact, action, or honest assessment. Not optimism for its own sake.

### S19. Knowledge-Cutoff Disclaimers
**Detect:** "As of [date]," "While specific details are limited..." "Based on available information..."

**Rewrite:** Remove entirely. If information is uncertain, say what you do know and acknowledge the gap specifically.

### S20. Synthetic Specificity
**Detect:** Fake-precise details that sound authoritative but add nothing. "A 2019 study" without naming the study. "Research from leading universities" without naming them. Percentages without sources.

**Rewrite:** Either provide the real source or acknowledge that you're speaking generally. "Several studies have explored this, though I don't have a specific citation to hand" is more honest than a fabricated reference.

### S21. Pronoun Avoidance
**Detect:** AI avoids "I" and "we" even when first-person is natural. Everything is written in impersonal third person when the context calls for a human perspective.

**Rewrite by voice:**
- `OX`: Use "one" occasionally, but also "I" when genuine perspective is offered.
- `SF`: "I" freely. "We" for shared experience. Direct and personal.
- `AB`: "We" as default collaborative pronoun. "I" when personal perspective adds value.
- `ST`: "One" for generalisation, "I" for conviction, "we" for shared intellectual journey.

### S22. Title Case in Headings
**Detect:** All Main Words Capitalised In Every Heading.

**Rewrite:** Use sentence case: "Strategic negotiations and global partnerships."

### S23. Curly Quotation Marks
**Detect:** "Curly quotes" instead of "straight quotes."

**Rewrite:** Use straight quotes consistently.

---

## New Patterns (2025-2026 Research)

### N1. Model Fingerprint Clustering
**What it is:** Each AI model (GPT-4, Claude, Llama) produces text that clusters into identifiable stylometric groups. Even when prompted to vary, the output stays within a detectable cluster. (UCC stylometric study, 2025)

**Implication:** Simply prompting an AI to "write differently" is insufficient. The transformation must actively break the model's native clustering patterns — which is why voice profiles and burstiness engineering matter more than surface-level word substitution.

### N2. VERMILLION Markers
**What they are:** The VERMILLION heuristic framework (Research Leap, 2025) identifies AI tendencies to: generalise audiences without specifying actors, and produce "echoed sentence structures" where multiple paragraphs exhibit uniform clause length and mirror grammatical rhythm.

**Rewrite:** Name specific actors. Vary clause length within and across paragraphs. Break mirrored grammatical structures.

### N3. Low Perplexity Patterns
**What it is:** AI text uses statistically "safe" word choices, resulting in low perplexity (high predictability). Human text features more unexpected word choices — the surprising adjective, the uncommon verb, the phrase that's distinctly personal.

**Rewrite:** Choose the less obvious word when it's more precise. "The proposal landed with a thud" rather than "The proposal was not well received." Voice profiles guide which unexpected choices are appropriate for each register.
