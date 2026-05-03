# Qualitative Rubric: 11-Star Assessment Methodology

## Purpose

The qualitative rubric guides how to perform the 11-star experience mapping for a PRD. It provides structured questions, a customer journey tracing methodology, and a delight moment identification process. This assessment feeds into the Ambition, Differentiation, and Story Quality dimensions of the quantitative rubric.

---

## Per-Feature 5-Question Assessment

For every feature or user story in the PRD, answer these 5 questions:

### Question 1: What star level is this feature targeting?

Map the feature to the 11-star spectrum using the detailed level descriptions in `references/eleven-star/star-levels-*.md`. Consider:

- What does the user experience? (Not what the system does.)
- Is the feature reactive (responds to user input) or proactive (anticipates needs)?
- Is the feature familiar (exists in competitors) or novel (introduces something new)?
- Does the feature create an emotional response beyond task completion?

**Assignment guide**:
- If the feature is present in every major competitor and implemented similarly: Star 5
- If the feature adds contextual intelligence or proactive behavior: Star 6
- If the feature creates a moment users would share with colleagues: Star 7
- If the feature reframes how users think about the problem: Star 8

### Question 2: What would one star higher look like?

Describe concretely what the feature would need to deliver to move up one level. This is not hypothetical -- it should be a specific, describable enhancement.

**Example**:
- Current (Star 5): "Users can search for contacts by name, company, or role."
- One star higher (Star 6): "The system proactively surfaces contacts relevant to the user's current task -- e.g., when drafting a proposal for Acme Corp, contacts at Acme with decision-making authority appear automatically."

### Question 3: Is the next star feasible within constraints?

Evaluate whether the one-star-higher version is achievable given:

- Available technology and data sources
- Timeline and budget constraints
- Team capability and organizational readiness
- Dependency on external systems or partners

**Grade**: Feasible now / Feasible with moderate effort / Feasible in future version / Not feasible

### Question 4: What is the user's emotional response at this level?

Identify the emotion the user would feel when interacting with this feature at its current star level:

| Star Range | Typical Emotions |
|-----------|-----------------|
| 1-2 | Frustration, anger, helplessness |
| 3 | Resignation, tolerance, mild annoyance |
| 4 | Neutrality, expectation met |
| 5 | Satisfaction, competence confirmed |
| 6 | Pleasant surprise, appreciation |
| 7 | Delight, eagerness to share |
| 8 | Revelation, "aha" moment, loyalty |
| 9-11 | Wonder, trust, liberation |

If the PRD does not address the user's emotional experience, note this as a Story Quality gap.

### Question 5: Does this differentiate from competitors?

Assess whether the feature, at its current star level, creates competitive differentiation:

- **No differentiation (Star 4-5)**: Feature exists in competitors with similar implementation
- **Mild differentiation (Star 6)**: Feature exists in competitors but this implementation adds contextual intelligence
- **Strong differentiation (Star 7)**: Feature creates a distinct experience not available elsewhere
- **Category-defining differentiation (Star 8)**: Feature redefines what users expect from this product category

---

## Customer Journey Tracing Methodology

### Step 1: Identify the Journey Stages

Map the PRD's features to the standard customer journey stages:

| Stage | Description | Key Question |
|-------|-------------|-------------|
| **Awareness** | User discovers the product exists | How does the user first learn about the product? |
| **Consideration** | User evaluates the product against alternatives | What makes the user choose this over competitors? |
| **Activation** | User achieves first value | How quickly does the user experience the core benefit? |
| **Retention** | User returns and deepens usage | What brings the user back repeatedly? |
| **Expansion** | User discovers additional value | How does the product grow with the user's needs? |
| **Advocacy** | User recommends to others | What would the user tell a colleague about this product? |

### Step 2: Map Features to Stages

Create a matrix showing which PRD features map to which journey stages. A single feature may span multiple stages.

### Step 3: Identify Gaps

Look for journey stages with no features mapped. Common gaps:

- **Activation gap**: The PRD describes powerful features but no onboarding or first-use experience. Users may never reach the value.
- **Retention gap**: The PRD focuses on acquisition features but has no engagement loops, notifications, or progressive value.
- **Advocacy gap**: No features designed to be shareable, remarkable, or worth discussing.

### Step 4: Identify Over-Indexing

Look for journey stages with disproportionate feature density:

- **Over-indexing on Activation**: Many first-use features but no depth. Users arrive but do not stay.
- **Over-indexing on Expansion**: Advanced features without a strong core. Power users are served but new users are lost.
- **Over-indexing on Retention**: Engagement mechanics without genuine value. Users return but do not deepen.

### Step 5: Assess Journey Coherence

Read the features in journey order (Awareness through Advocacy). Does the sequence tell a coherent story? Can you narrate the user's progression from first encounter to loyal advocate?

If the journey has gaps, discontinuities, or illogical transitions, note these as Story Quality issues in the review.

---

## Delight Moment Identification

Delight moments are specific interactions where the user's experience exceeds their expectations. They are the building blocks of star 6-8 features.

### Characteristics of Delight Moments

1. **Unexpected**: The user did not anticipate the product would do this
2. **Valuable**: The unexpected behavior saves time, prevents error, or reveals insight
3. **Personal**: The behavior feels tailored to this user's specific context
4. **Effortless**: The delight arrives without the user doing extra work
5. **Memorable**: The user remembers and can describe the moment later

### How to Find Delight Moments in a PRD

1. **Search for proactive features**: Features that act without user prompting are candidates for delight
2. **Look for cross-domain connections**: Features that combine data from multiple sources to produce novel insights
3. **Identify friction-removal features**: Features that eliminate steps users expect to have to perform
4. **Find personalization features**: Features that adapt to the individual user's patterns or preferences
5. **Check for surprise features**: Features that deliver more than the stated requirement

### How to Identify Missing Delight Moments

For each journey stage, ask: "What could the product do here that would make the user smile?" If the PRD has no answer for any stage, there is a delight deficit.

Common opportunities for delight:
- **First use**: Intelligent defaults that make setup feel effortless
- **Error recovery**: Helpful guidance that turns a mistake into a learning moment
- **Milestone achievement**: Recognition when the user accomplishes something significant
- **Repeated use**: The product gets better over time as it learns the user's patterns
- **Collaboration moments**: Features that make users look good to their colleagues

---

## Synthesizing Qualitative Findings

After completing the per-feature assessment, journey trace, and delight moment identification, synthesize findings into:

1. **Star-level spectrum map**: A visual showing where each feature sits on the 1-11 scale
2. **Journey gap analysis**: Stages with insufficient feature coverage
3. **Delight inventory**: Existing and missing delight moments
4. **Ambition assessment**: Whether anchor features are at the sweet spot (7-8 stars)
5. **Chesky principle evaluation**: How well the PRD performs against each of the 5 lenses

These feed into the qualitative assessment section of the review report template.
