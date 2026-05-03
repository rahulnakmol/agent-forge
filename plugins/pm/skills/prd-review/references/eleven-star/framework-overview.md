# The 11-Star Experience Framework

## Origin

In 2014, Brian Chesky, co-founder and CEO of Airbnb, described a mental exercise he used to design exceptional guest experiences. The premise was simple: instead of rating experiences on the typical 1-5 star hotel scale, extend the scale to 11 stars and ask "what would each level look like?"

Chesky originally applied this to the Airbnb guest arrival experience:

- **1 star**: You show up and nobody is home. The door is locked.
- **5 stars**: You arrive, the host greets you, the place is clean, everything works as described.
- **7 stars**: The host picks you up from the airport in a luxury car with a personalized welcome package.
- **10 stars**: A private jet picks you up, and Elon Musk gives you a tour of SpaceX on the way.
- **11 stars**: You arrive and the experience is so transformative that it fundamentally changes your life.

The exercise was never about literally delivering 10 or 11 stars. The purpose was to expand the possibility space, then work backward to find the "sweet spot" -- the highest feasible level of experience that creates genuine differentiation.

## Core Concept

Rate any experience on a 1-11 scale, where:

- **1-3**: The experience is broken, hostile, or requires painful workarounds. Users suffer through it because they have no alternative.
- **4-5**: The experience meets expectations. It works. It is functional. It is what every competitor also delivers. Users are satisfied but not loyal.
- **6-8**: The experience exceeds expectations in ways that create emotional resonance. Users notice the difference, feel valued, and tell others. This is the **sweet spot** -- ambitious enough to differentiate, feasible enough to build.
- **9-11**: The experience is magical, transformative, or eliminates the problem entirely. These levels are aspirational thought exercises, not design targets.

## Application to PRD Review

While Chesky developed this framework for hospitality experiences, it applies directly to product requirements:

**A PRD is a blueprint for an experience.** Every feature, every user story, every acceptance criterion describes a moment in the user's journey. The 11-star framework provides a lens to evaluate whether those moments aim high enough.

### The Problem with Most PRDs

Most PRDs aim for 5 stars. They describe features that:
- Work correctly
- Meet the documented requirements
- Match what competitors offer
- Pass QA validation

This is necessary but insufficient. A 5-star PRD produces a 5-star product -- functional, forgettable, and vulnerable to any competitor who aims higher.

### The Goal of 11-Star PRD Review

The reviewer's job is to:

1. **Map each feature to its current star level** -- Where on the spectrum does this requirement sit?
2. **Identify the ceiling** -- What would one star higher look like for this feature?
3. **Find the sweet spot** -- Which features should be pushed to 7-8 stars, and which are fine at 5?
4. **Challenge the defaults** -- Where has the PRD accepted "this is how it's done" without questioning whether there is a better way?

### The Spectrum Applied to Product Requirements

| Star Level | Requirement Characteristic | User Emotional Response |
|------------|---------------------------|------------------------|
| 1 | Feature missing entirely | Frustration, abandonment |
| 2 | Feature exists but is punishing to use | Anger, complaint |
| 3 | Feature works with significant friction | Resignation, workarounds |
| 4 | Feature meets minimum expectations | Neutral, expected |
| 5 | Feature works well, matches competitors | Satisfaction, no loyalty |
| 6 | Feature anticipates what user needs next | Surprise, appreciation |
| 7 | Feature creates a moment user talks about | Delight, advocacy |
| 8 | Feature changes how user thinks about the problem | Revelation, loyalty |
| 9 | Feature feels like it reads the user's mind | Wonder, trust |
| 10 | Feature transforms the entire workflow | Paradigm shift |
| 11 | The problem the feature solves ceases to exist | Liberation |

## Key Insight

**Most PRDs cluster at stars 4-5 because that is where specifications live.** Specifications describe what the system should do. They do not describe what the user should feel, discover, or become capable of. The 11-star framework forces the reviewer to look beyond functional correctness and ask: "Is this PRD designing an experience, or just documenting a system?"

The sweet spot is 7-8 stars: ambitious enough to differentiate the product in the market, feasible enough to build within real constraints of timeline, budget, and technology. Not every feature needs to be at 7-8 -- but the anchor features (the 1-2 features that define the product's identity) absolutely should be.

## Framework Limitations

The 11-star framework is a qualitative diagnostic tool, not a measurement instrument. It cannot be averaged or aggregated meaningfully. A product with ten 5-star features and one 8-star feature may be more compelling than a product with eleven 6-star features. The framework identifies where to concentrate ambition, not how to distribute it evenly.

Use it alongside -- never instead of -- the quantitative scoring rubric.
