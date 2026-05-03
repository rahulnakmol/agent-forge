# Voice Profiles & Humanize Integration

## Voice Profile Options

Present these options when the task produces an artifact (DOCX, XLSX, PPTX, or MD):

### OX — Oxford Academic
- **Character**: Measured, precise, authoritative, evidence-based
- **Sentence style**: Longer sentences with subordinate clauses, formal transitions, hedged claims
- **Vocabulary**: Academic register, Latinate word choices, domain-specific terminology
- **Best for**: Formal reports, research papers, technical documentation, white papers, policy documents
- **Example tone**: "The evidence suggests that, while significant progress has been made in automated testing frameworks, the challenge of maintaining comprehensive coverage in rapidly evolving codebases remains substantively unaddressed."

### SF — San Francisco Tech
- **Character**: Direct, energetic, conversational, optimistic
- **Sentence style**: Short punchy sentences mixed with longer explanatory ones, contractions, rhetorical questions
- **Vocabulary**: Tech-forward language, startup vernacular, occasional colloquialisms
- **Best for**: Blog posts, product documentation, startup communications, developer guides, README files
- **Example tone**: "Here's the thing about microservices: they're not a silver bullet. But when you've got 12 teams shipping independently? They're a game-changer. Let me show you why."

### AB — Australian Business
- **Character**: Warm, pragmatic, clear, no-nonsense
- **Sentence style**: Medium-length sentences, active voice, practical framing, occasional dry humor
- **Vocabulary**: Plain business English, concrete language, minimal jargon
- **Best for**: Business communications, proposals, internal memos, client-facing reports, project updates
- **Example tone**: "The migration is tracking well against plan. We've hit two of the three milestones ahead of schedule, and the remaining database cutover is set for next Thursday. No major risks to flag — the team's across it."

### ST — Southern Storyteller
- **Character**: Engaging, warm, narrative-driven, relatable
- **Sentence style**: Varied rhythm with storytelling cadence, anecdotes, vivid metaphors
- **Vocabulary**: Accessible language, conversational warmth, illustrative examples
- **Best for**: Presentations, case studies, thought leadership, newsletters, keynote content
- **Example tone**: "When we started this project, nobody thought we'd be here twelve months later with a platform serving half a million users. But that's exactly what happened — and the story of how we got here has a few lessons worth sharing."

### Custom Voice
If the user describes a voice that doesn't match the four profiles above, acknowledge it and calibrate:
> "Got it — I'll calibrate the voice to match: [user's description]. The generated prompt will include specific voice instructions so the output matches your preference."

## Humanize Skill Integration Rules

When the generated prompt involves an artifact, include this instruction block in the final prompt:

### For Word Documents (DOCX)
```
IMPORTANT: After drafting the content, invoke the `humanize` skill with voice profile [PROFILE]. Then invoke the `docx` skill to produce the final Word document. The humanize pass must happen BEFORE document formatting — apply voice calibration to the raw content first, then format.
```

### For Spreadsheets (XLSX)
```
IMPORTANT: For any narrative content in this spreadsheet (headers, descriptions, commentary cells, summary sheets), invoke the `humanize` skill with voice profile [PROFILE] to ensure natural language. Then invoke the `xlsx` skill to produce the final spreadsheet.
```

### For Presentations (PPTX)
```
IMPORTANT: After writing slide content, invoke the `humanize` skill with voice profile [PROFILE] to ensure all slide text, speaker notes, and narrative content sounds authentically human. Then invoke the `pptx` skill to produce the final presentation.
```

### For Markdown (MD)
```
IMPORTANT: After drafting the content, invoke the `humanize` skill with voice profile [PROFILE] to ensure the writing sounds authentically human. Apply burstiness engineering, remove AI patterns (filler phrases, hedge stacking, formulaic transitions), and calibrate to the specified regional voice.
```

## Voice-Technique Pairing Recommendations

| Voice Profile | Pairs Well With | Reason |
|--------------|-----------------|--------|
| OX | Knowledge Generation | Academic depth benefits from explicit knowledge scaffolding |
| SF | Zero-Shot | Direct instructions match the direct voice |
| AB | Meta Prompting | Pragmatic approach benefits from strategy-first thinking |
| ST | Prompt Chaining | Narrative arc benefits from phased development |
