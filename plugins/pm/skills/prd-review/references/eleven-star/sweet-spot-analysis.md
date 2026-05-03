# Sweet Spot Analysis Methodology

## Purpose

The sweet spot analysis is a 5-step methodology for locating where a PRD's features should sit on the 11-star spectrum. The goal is not to maximize the star level -- it is to find the highest feasible level that creates genuine differentiation without sacrificing deliverability.

---

## Step 1: Define the 1-Star Experience

**Question**: What is broken today? What does the user suffer through?

Map the current state -- the pain that motivates the PRD's existence. Be specific about:

- What task is the user trying to accomplish?
- What tools or processes do they use today?
- Where does the experience break down?
- What workarounds have users developed?
- How much time, effort, or money does the broken experience cost?

**Output**: A concrete description of the worst version of this experience. This anchors the bottom of the spectrum.

**Example**: "Today, a sales manager spends 4 hours every Monday manually compiling pipeline data from 6 different spreadsheets, cross-referencing Salesforce records, and formatting a slide deck for the weekly forecast meeting. Data is always 3-5 days stale. Errors are found in the meeting. The deck is outdated before it is presented."

---

## Step 2: Define the 5-Star Experience

**Question**: What does "meets spec" look like? What would a competent competitor ship?

Describe the functional, polished, fully-working version of the solution. This is what the PRD should deliver at minimum. It includes:

- All stated requirements met
- Clean, professional UX
- Reliable performance
- Correct data
- Standard integrations
- No significant friction

**Output**: A description of the experience that would earn a "satisfactory" rating from users and stakeholders. No complaints, no praise.

**Example**: "An automated dashboard pulls pipeline data from Salesforce in real time. The sales manager opens the dashboard, sees current pipeline by stage, rep, and region. A PDF export generates the weekly deck automatically. Data is always current. The Monday meeting starts with accurate numbers."

---

## Step 3: Define the 11-Star Experience

**Question**: What would the impossible, magical version look like? What if there were no constraints?

Remove all constraints -- budget, technology, physics, organizational politics -- and describe the ultimate version. This is a creative exercise, not a requirements exercise. Be outrageous.

**Output**: A provocative description that stretches imagination. It will not be built as described, but it reveals the direction of maximum value.

**Example**: "The sales manager never attends a forecast meeting because there is nothing to discuss. The system has already predicted which deals will close this quarter with 99% accuracy, automatically adjusted resource allocation, alerted reps to at-risk deals 3 weeks before they stalled, and sent the board an updated forecast in real time. The concept of a weekly pipeline review meeting does not exist because every stakeholder has continuous, real-time clarity. The sales manager spends Mondays coaching reps on the 3 deals the system flagged as saveable, with a recommended playbook for each."

---

## Step 4: Work Backward from 11 to Find 7-8

**Question**: What elements of the 11-star vision could be partially achieved with current technology and resources?

This is the critical analytical step. Take the 11-star description and decompose it into elements:

1. List every capability described in the 11-star version
2. For each capability, ask: "Is a meaningful version of this feasible within constraints?"
3. Grade feasibility: **Now** (existing technology), **Near** (12-18 months), **Far** (3-5 years), **Impossible** (requires breakthrough)
4. The "Now" and "Near" capabilities that are NOT in the current PRD are the sweet spot opportunities

**Decomposition example**:

| 11-Star Element | Feasible Version | Feasibility | In Current PRD? |
|----------------|-----------------|-------------|-----------------|
| 99% deal prediction | Win probability model based on historical patterns (70-80% accuracy) | Near | No |
| Auto-adjust resource allocation | Surface recommended actions, human approves | Now | No |
| Alert reps to at-risk deals 3 weeks early | Flag deals with declining engagement signals | Now | Partially |
| Recommended playbook per deal | Template playbooks matched by deal characteristics | Now | No |
| Eliminate forecast meeting entirely | Async forecast updates with exception-only meetings | Now | No |
| Real-time board forecast | Auto-updated executive dashboard | Now | Yes |

**Output**: A list of feasible enhancements that would push the PRD from star 5 to star 7-8. These become the improvement suggestions in the review report.

---

## Step 5: Map PRD Requirements to the Spectrum

**Question**: Where does each existing PRD feature sit on the 1-11 spectrum?

Take every feature or user story in the PRD and assign it a star level based on the framework definitions. Use this mapping to:

1. **Identify the average star level**: Is the PRD clustering at 4-5 (common) or spread across levels?
2. **Identify anchor features**: Which 1-2 features are meant to differentiate? Are they at 7-8?
3. **Identify underperformers**: Are any features below star 4? These are quality defects.
4. **Identify over-ambition**: Are any features at 9-11 without feasibility grounding?

**Output**: A feature-by-star mapping table and a portfolio assessment.

---

## Decision Framework

After completing all 5 steps, apply the following decision logic:

### If most features are at Stars 4-5

**Diagnosis**: The PRD is functional but undifferentiated. It will produce a competent product that competes on price, not experience.

**Recommendation**: Push 2-3 anchor features to star 7-8 using the sweet spot opportunities identified in Step 4. Keep table-stakes features at star 5.

### If most features are at Stars 6-7

**Diagnosis**: The PRD is ambitious and well-positioned. Focus the review on ensuring feasibility and identifying the 1-2 features that could reach star 8.

**Recommendation**: Validate that the ambitious features have credible technical approaches. Ensure table-stakes features have not been neglected.

### If most features are at Stars 9-10

**Diagnosis**: The PRD needs grounding. The vision is inspiring but may not be deliverable. There is a high risk of scope creep, delayed delivery, and stakeholder disappointment.

**Recommendation**: Apply the grounding test to every star 9-10 feature. Work backward to find the star 7-8 version that captures 80% of the value with 20% of the complexity. Flag Feasibility concerns in the scoring rubric.

### If features are spread across Stars 2-9

**Diagnosis**: The PRD is inconsistent. Some features have been deeply considered while others have been neglected. This usually indicates uneven stakeholder input or rushed authoring.

**Recommendation**: Bring the low-star features up to 5 (quality baseline) and calibrate the high-star features for feasibility. The spread itself is a concern worth flagging.

### If the PRD has no feature above Star 5

**Diagnosis**: The PRD may be technically excellent but strategically insufficient. It describes a product that will work but will not win.

**Recommendation**: This is the most important review finding. Explicitly identify the anchor features and conduct the 11-star backward design exercise (Steps 3-4) for each. Include specific sweet spot opportunities in the improvement suggestions.

---

## Common Pitfalls

1. **Averaging star levels**: Do not average. A product with one 8-star feature and nine 5-star features is stronger than ten 6-star features. Focus on the anchor.
2. **Pushing everything higher**: Not every feature needs to be ambitious. Table stakes should be solid (5 stars), not innovative.
3. **Confusing polish with ambition**: A beautifully designed 5-star feature is still 5 stars. Polish is about execution quality; star level is about experience ambition.
4. **Ignoring constraints**: The sweet spot must be feasible. An unfeasible star 8 is worse than a solid star 6.
5. **Forgetting the user**: Star levels are about the user's experience, not the team's technical achievement. A technically impressive feature that users do not notice is not an 8.
