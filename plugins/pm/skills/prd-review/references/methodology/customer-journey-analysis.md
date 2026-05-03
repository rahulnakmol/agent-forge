# Customer Journey Analysis

## Purpose

Customer journey analysis traces how a user moves through the product experience described in the PRD. It reveals gaps (journey stages with no features), over-indexing (too many features concentrated in one stage), and narrative breaks (discontinuities between stages). The analysis feeds into the Story Quality and Completeness dimensions of the scoring rubric.

---

## Journey Stages

### Stage 1: Awareness

**Definition**: The user discovers that the product exists and understands what problem it solves.

**PRD features to look for**:
- Onboarding messaging, landing page content, value proposition
- How the product describes itself to a first-time visitor
- Marketing hooks, positioning statements

**Common gap**: PRDs often assume users already know about the product. If the PRD describes features but not how users discover them, Awareness is a gap.

**Review question**: "How does a user who has never heard of this product learn what it does and why they should care?"

### Stage 2: Consideration

**Definition**: The user evaluates the product against alternatives and decides whether to try it.

**PRD features to look for**:
- Free trial, freemium model, demo capabilities
- Comparison features, import from competitors
- Social proof integration (testimonials, case studies, usage stats)
- Pricing transparency, feature comparison matrices

**Common gap**: PRDs frequently skip from "product exists" to "user is onboarded" without addressing why the user chose this product over alternatives.

**Review question**: "What does the PRD offer that would make a user choose this product over doing nothing or using a competitor?"

### Stage 3: Activation

**Definition**: The user achieves first value -- the moment they experience the core benefit for the first time.

**PRD features to look for**:
- Onboarding flow, setup wizard, guided first-use
- Time-to-value optimization (how quickly does the user see the benefit?)
- Quick-start templates, sample data, interactive tutorials
- First success milestone and celebration

**Common gap**: PRDs often describe the full feature set without addressing how a new user reaches their first success. Powerful features behind complex setup flows create an activation gap.

**Review question**: "How many steps and how much time does it take for a new user to experience the core value proposition?"

### Stage 4: Retention

**Definition**: The user returns to the product repeatedly and integrates it into their workflow.

**PRD features to look for**:
- Notifications, reminders, digests that pull users back
- Habit loops (trigger -> action -> reward -> investment)
- Progressive feature disclosure (new capabilities unlocked with use)
- Data accumulation that makes the product more valuable over time
- Integration with daily tools (email, Slack, calendar)

**Common gap**: PRDs may design a great first experience but not address what brings users back on day 7, day 30, or day 90.

**Review question**: "Why would the user open this product tomorrow? Next week? Next month?"

### Stage 5: Expansion

**Definition**: The user discovers additional value beyond the initial use case.

**PRD features to look for**:
- Advanced features, power-user capabilities
- Team collaboration features, sharing and permissions
- Integrations with adjacent tools in the user's workflow
- Cross-selling or upselling pathways
- Customization and personalization options

**Common gap**: PRDs that serve one use case well but do not grow with the user's needs. The product becomes a point solution rather than a platform.

**Review question**: "What does the user do after they have mastered the core features? Does the product grow with them?"

### Stage 6: Advocacy

**Definition**: The user recommends the product to others, becoming a growth engine.

**PRD features to look for**:
- Referral mechanisms, invite flows
- Shareable outputs (reports, dashboards, exports that carry the brand)
- Community features, user forums, knowledge sharing
- "Wow moments" designed to be story-worthy (star 7 features)
- Multi-user collaboration that naturally introduces new users

**Common gap**: This is the most commonly missing stage in PRDs. Products that rely entirely on marketing for growth miss the opportunity to design virality into the product itself.

**Review question**: "If a user loves this product, what mechanism exists for them to bring others in? What would they say when describing it?"

---

## Analysis Process

### Step 1: Build the Journey Map

Create a matrix with journey stages as columns and PRD features as rows. Place each feature in the stage(s) where it primarily contributes.

| Feature | Awareness | Consideration | Activation | Retention | Expansion | Advocacy |
|---------|-----------|---------------|------------|-----------|-----------|----------|
| Feature A | | | X | | | |
| Feature B | | | | X | X | |
| Feature C | | | X | X | | |
| ... | | | | | | |

### Step 2: Count and Assess

For each stage:
- Count features mapped to that stage
- Assess whether those features adequately serve the stage's purpose
- Identify empty columns (gaps) and overloaded columns (over-indexing)

### Step 3: Trace the Flow

Read the journey left to right. For each transition between stages, ask:
- Is the transition smooth or abrupt?
- Does the PRD describe what triggers the user's progression?
- Are there features that bridge between stages?

### Step 4: Identify Transition Triggers

For each stage transition, identify what causes the user to move forward:

| Transition | Trigger | PRD Coverage |
|-----------|---------|-------------|
| Awareness -> Consideration | User recognizes the problem + discovers solution | ? |
| Consideration -> Activation | User decides to try the product | ? |
| Activation -> Retention | User achieves first value and sees ongoing benefit | ? |
| Retention -> Expansion | User's needs grow or they discover new capabilities | ? |
| Expansion -> Advocacy | User is delighted enough to recommend | ? |

Uncovered transitions are narrative gaps in the PRD.

---

## Common Anti-Patterns

### The Activation Cliff

The PRD describes powerful features that require significant setup, configuration, or learning before the user sees value. There is a "cliff" between signing up and experiencing the benefit. Users who fall off this cliff never reach the features the PRD spent the most effort describing.

**Recommendation**: The PRD should include a fast-path to first value (guided tour, sample data, template) that demonstrates the core benefit within 5 minutes.

### The Retention Desert

The PRD covers initial use extensively but has no features for ongoing engagement. There is nothing that brings the user back, nothing that accumulates value, and nothing that deepens the relationship.

**Recommendation**: Identify at least one engagement loop (notification, digest, progressive reward) that creates a reason to return.

### The Expansion Void

The product serves one use case perfectly but provides no growth path. Users hit a ceiling and eventually look for a more comprehensive solution.

**Recommendation**: The PRD should include at least a "future considerations" section that outlines how the product evolves beyond the initial scope.

### The Advocacy Absence

The product creates no mechanism for organic growth. Every new user must be acquired through marketing spend.

**Recommendation**: Identify at least one feature that produces shareable outputs or enables collaborative use that naturally introduces new users.

---

## Connecting to the 11-Star Framework

Journey analysis and star-level analysis complement each other:

- **Star level** answers "How good is each feature?"
- **Journey analysis** answers "Are the right features present for a complete experience?"

A product with all star-7 features but no Activation stage will fail. A product with complete journey coverage but all star-4 features will be mediocre. The review should assess both dimensions.

The anchor features (star 7-8) should typically live in the Activation or Retention stages -- the moments where the user experiences the core value proposition. Table-stakes features (star 5) can cover Awareness, Consideration, and Expansion. Advocacy features should aim for star 7 because they need to create moments worth sharing.
