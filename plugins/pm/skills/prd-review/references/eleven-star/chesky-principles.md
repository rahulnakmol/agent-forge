# Brian Chesky's 5 Principles as Review Lenses

Each of Chesky's core principles becomes a lens through which to evaluate PRD quality. During the qualitative assessment phase, apply each lens to the PRD and note where the document excels or falls short.

---

## Principle 1: Customer Obsession

**Chesky's formulation**: "Build for the person, not the persona."

### The Lens

A PRD should describe real human beings with real problems, emotions, and contexts -- not abstract user types defined by demographics and job titles. "Enterprise admin" is a persona. "Sarah, who manages 200 user accounts and dreads the quarterly access review because it takes 3 full days of mind-numbing checkbox clicking" is a person.

### Review Questions

1. **Does the PRD describe real human needs or abstract system requirements?**
   - Weak: "The system shall support role-based access control."
   - Strong: "When a team lead onboards a new hire, they need to grant the right permissions in under 2 minutes without understanding the full RBAC model."

2. **Can you picture the user's face when they use this feature?**
   - If the user story is so generic that it could apply to any product, it lacks customer obsession.

3. **Does the PRD reference actual user research, interviews, or observed behavior?**
   - Claims about user needs should be grounded in evidence, not assumptions.

4. **Are edge cases described with empathy?**
   - Weak: "System displays error message when input is invalid."
   - Strong: "When a user enters a date in the wrong format, the system suggests the correct format and preserves their input so they only need to adjust, not re-enter."

5. **Does the PRD acknowledge the user's emotional state during key interactions?**
   - Some interactions happen during stressful moments (error recovery, deadline pressure, public presentations). The PRD should acknowledge and design for that context.

### Red Flags

- User stories that begin with "As a user" instead of a specific role with specific context
- No mention of user research, interviews, or behavioral observation
- Requirements written entirely in system language ("the system shall") with no user language ("the user can")
- Missing error states, edge cases, or recovery flows
- No distinction between novice and expert user needs

---

## Principle 2: Do Things That Don't Scale

**Chesky's formulation**: "Focus on delighting a few users deeply before trying to serve many users adequately."

### The Lens

Many PRDs optimize for scale prematurely. They specify features that serve millions of users adequately rather than features that would make the first 100 users ecstatic. A PRD that prioritizes scalable mediocrity over focused excellence is unlikely to produce a differentiated product.

### Review Questions

1. **Is the PRD optimizing for the first 100 users or the first 100,000?**
   - Early-stage products should obsess over a narrow audience. If the PRD tries to serve everyone, it may delight no one.

2. **Are there features that would be amazing for a specific segment but are absent because they "don't scale"?**
   - The most powerful product insights come from doing things that do not scale, then finding the scalable version later.

3. **Does the PRD include any concierge-level features?**
   - Personalized onboarding, hand-crafted templates for specific industries, curated content for specific roles -- these signal customer obsession over operational efficiency.

4. **Is the MVP defined by what users love or by what the team can ship quickly?**
   - An MVP should be the minimum product that users would be upset to lose, not the minimum the team can build.

5. **Does the PRD sacrifice depth for breadth?**
   - A product that does 3 things brilliantly beats one that does 30 things adequately.

### Red Flags

- Feature lists that are wide and shallow (many features, none deeply specified)
- Scalability requirements in the first version that constrain the experience
- No mention of pilot users, early adopters, or focus segments
- Requirements that explicitly avoid personalization because "it doesn't scale"
- MVP defined by effort reduction rather than user value maximization

---

## Principle 3: Design the 11-Star, Then Work Backward

**Chesky's formulation**: "Start with impossible perfection, then find the feasible sweet spot."

### The Lens

The best PRDs show evidence of aspirational thinking that has been grounded. You can tell because the features feel both ambitious and achievable -- they push boundaries without breaking constraints. This only happens when the author first imagined the impossible version, then worked backward to find the feasible sweet spot.

### Review Questions

1. **Does the PRD include a vision statement that stretches beyond the feature list?**
   - A PRD with only requirements and no vision likely started at star 5 and never looked higher.

2. **Can you identify the "worked backward" features?**
   - Features that feel both surprising and achievable are usually the product of backward design. Features that feel either obvious or impossible are not.

3. **Is there a long-term vision alongside the short-term scope?**
   - Even if v1 is modest, the PRD should articulate where the product is heading. This context helps reviewers assess whether v1 is a stepping stone to star 8 or a dead end at star 5.

4. **Does the PRD explain why certain ambitious features were descoped?**
   - A PRD that says "we considered X but descoped it to Y because Z" shows evidence of backward design. A PRD that never mentions X may not have considered it.

5. **Are there "future consideration" sections that reveal aspirational thinking?**
   - Not everything belongs in v1, but the PRD should show awareness of what star 9-11 would look like.

### Red Flags

- No vision statement or future roadmap context
- All features feel "safe" and predictable
- No mention of descoped ideas or future phases
- The PRD reads like a specification, not a strategy document
- No evidence that alternatives were considered

---

## Principle 4: Storytelling

**Chesky's formulation**: "Requirements should tell a story. If you can't narrate the user's journey, the requirements are incomplete."

### The Lens

A PRD is not a database of features. It is a narrative about how a person's life or work changes because this product exists. The best PRDs can be read as a story: there is a protagonist (the user), a conflict (the problem), a journey (the features), and a resolution (the outcome). If the PRD cannot be narrated, the user journey has gaps.

### Review Questions

1. **Can you read the PRD end to end and follow the user's journey?**
   - If the PRD is a disconnected list of features, the story is missing. Features should flow logically from one to the next.

2. **Is there a clear before/after narrative?**
   - The PRD should paint a picture of the user's world before the product and after. The contrast should be compelling.

3. **Do user stories connect to each other?**
   - Isolated user stories suggest fragmented thinking. The best PRDs link stories into journeys.

4. **Can you explain why each feature matters in plain language?**
   - If a feature requires technical context to understand its value, the story is missing.

5. **Does the PRD have a narrative arc?**
   - Problem -> Discovery -> First value -> Deepening engagement -> Mastery. The best PRDs mirror the user's journey from awareness to advocacy.

### Red Flags

- Features listed in no particular order (no narrative flow)
- User stories that cannot be linked into a coherent journey
- No before/after comparison
- Technical requirements with no user context
- Requirements that make sense individually but not collectively

---

## Principle 5: Challenge the Default

**Chesky's formulation**: "Every time someone says 'this is how it's done,' that is a signal to question why."

### The Lens

Most PRDs inherit assumptions from the industry, the organization, or the existing product. These defaults are rarely examined. The challenge-the-default lens asks: "What is this PRD assuming must be true?" and then tests each assumption.

### Review Questions

1. **What does this PRD assume about the user's workflow that might not be true?**
   - Example: "Users will configure settings before first use." Why? What if the product configured itself?

2. **What industry conventions does this PRD follow without questioning?**
   - Example: "The dashboard displays charts and graphs." Why charts? What if the insight were a sentence?

3. **Are there features that exist because "every competitor has them"?**
   - Feature parity is star 5 thinking. The question is: "Why does every competitor have this? Is it because users need it, or because nobody questioned it?"

4. **Does the PRD introduce any new interaction patterns?**
   - If every interaction follows established UI conventions, the product is inheriting, not innovating.

5. **What would a first-principles redesign look like?**
   - Strip away everything inherited and ask: "If we were solving this problem for the first time today, with today's technology, what would we build?"

### Red Flags

- Every feature has a direct competitor equivalent
- No novel interaction patterns or workflows
- The PRD reads like a competitor feature comparison matrix
- Requirements reference "industry standard" or "best practice" without questioning applicability
- No features that make the reviewer think "I have not seen this before"

---

## Applying the Lenses

During Phase 2 (Assess), apply each principle as a pass through the PRD:

1. **First pass (Customer Obsession)**: Read for the human. Are real people visible in this document?
2. **Second pass (Don't Scale)**: Read for depth over breadth. Where has the PRD chosen breadth at the expense of depth?
3. **Third pass (11-Star Backward)**: Read for ambition. Where is the PRD aiming, and is it high enough?
4. **Fourth pass (Storytelling)**: Read for narrative. Can you follow the user's journey from problem to resolution?
5. **Fifth pass (Challenge Default)**: Read for assumptions. What is the PRD taking for granted?

Document findings from each pass. These feed directly into the qualitative assessment section of the review report.
