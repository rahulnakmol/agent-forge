# Star Levels 1 through 5: Broken to Baseline

These levels represent the spectrum from completely broken to functional parity with competitors. Most PRDs that need review are somewhere in this range.

---

## Star 1: Broken / Missing

**Description**: The experience does not exist or is fundamentally broken. The user cannot accomplish their goal at all. There is no feature, no workaround, nothing.

**SaaS product example**: A project management tool with no way to assign tasks to team members. Users must communicate assignments through a separate channel (email, Slack) and manually track who is doing what.

**Consulting engagement example**: A client requests a data migration strategy. The deliverable contains a project timeline but no actual migration approach, tooling recommendations, or risk assessment. The core need is unaddressed.

**What a PRD looks like at this level**: A critical user need is not mentioned anywhere in the PRD. The user story is absent. The feature gap is invisible because nobody thought to include it.

**How to identify during review**:
- Trace the customer journey end to end. Are there stages with no features mapped?
- Ask: "What does the user do when they need X?" If the answer is "nothing" or "use a different product," this is a 1-star gap.
- Look for implicit assumptions that a capability exists when it does not.

---

## Star 2: Exists but Frustrating

**Description**: The feature exists in some form, but using it is actively painful. The experience is hostile -- confusing UI, excessive steps, misleading feedback, or error-prone flows. Users complete the task but resent the product for making it hard.

**SaaS product example**: An expense reporting tool where uploading a receipt requires 7 clicks, choosing from 40 uncategorized expense types, and manually entering every field even when the receipt image contains the data. Submitting produces no confirmation, and errors surface only after the manager rejects the report days later.

**Consulting engagement example**: A requirements document exists but is written in dense technical jargon with no glossary, contradicts itself across sections, and provides no context for why decisions were made. Stakeholders can technically read it, but extracting actionable information requires significant effort.

**What a PRD looks like at this level**: The feature is described, but the user flow involves excessive friction. No thought has been given to error states, edge cases, or the emotional experience of using the feature. Requirements are technically complete but practically hostile.

**How to identify during review**:
- Count the steps in any described user flow. More than 3 steps for a routine action is a warning sign.
- Look for missing error handling, undo/redo capabilities, or confirmation feedback.
- Check if the PRD describes what the system does but not what the user experiences.

---

## Star 3: Works but Clunky

**Description**: The feature functions and users can accomplish their goal, but the experience requires workarounds, mental models that do not match reality, or tolerance for rough edges. Users develop coping strategies rather than enjoying the product.

**SaaS product example**: A CRM that lets you search contacts but only by exact name match. Partial matches, fuzzy search, or search by company/role do not work. Users learn to keep a separate spreadsheet of contacts they reference frequently because the in-app search is unreliable.

**Consulting engagement example**: A process design document describes the target state accurately but provides no transition plan. The client understands where they need to be but has no guidance on how to get there. They must fill in the gap themselves.

**What a PRD looks like at this level**: Requirements are present and technically correct, but they describe the minimum viable implementation. User stories lack acceptance criteria for edge cases. Non-functional requirements (performance, accessibility, error recovery) are absent or vague.

**How to identify during review**:
- Look for user stories without acceptance criteria.
- Check if non-functional requirements are addressed (performance targets, accessibility standards, error handling).
- Ask: "What happens when things go wrong?" If the PRD does not answer, it is designing for the happy path only.
- Identify features that work in isolation but create friction when combined.

---

## Star 4: Meets Minimum Expectations

**Description**: The feature works correctly and meets the basic expectations a user would have. There are no significant pain points, but there is also nothing memorable. This is the "it does what it says on the tin" level.

**SaaS product example**: A calendar application that lets you create events, set reminders, invite attendees, and view by day/week/month. Everything works. Nothing surprises. It is functionally equivalent to a dozen other calendar apps.

**Consulting engagement example**: A strategy document that accurately describes the current state, identifies gaps, and recommends solutions. The analysis is sound, the recommendations are reasonable, and the format is professional. The client receives exactly what they expected and nothing more.

**What a PRD looks like at this level**: All standard sections are present (problem statement, user stories, acceptance criteria, technical considerations). Requirements are clear and testable. The PRD would pass a completeness checklist. However, every feature described could have been written for any competitor's product. There is no unique angle.

**How to identify during review**:
- Apply the "logo swap" test: Could you replace the product name with a competitor's and the PRD would still make sense? If yes, it is a 4-star PRD.
- Check if user stories describe generic roles ("As a user") rather than specific personas with real context.
- Look for features that solve the stated problem but do not consider adjacent problems.

---

## Star 5: Works Well / Competitive Parity

**Description**: The feature is polished, well-executed, and matches the best available alternatives. Users are satisfied. The experience is smooth, professional, and reliable. This is where most successful products live -- and where most PRDs aim.

**SaaS product example**: A project management tool with kanban boards, list views, timeline/Gantt views, assignees, due dates, labels, filters, integrations with Slack and GitHub, and a mobile app. It works as well as Asana, Monday, or Linear. Users choose it based on price or ecosystem, not because the experience is fundamentally different.

**Consulting engagement example**: A transformation roadmap with phased milestones, resource estimates, risk register, RACI matrix, and governance framework. It follows industry best practices, references recognized frameworks (TOGAF, ITIL, SAFe), and presents a credible execution plan. The client is confident in the approach.

**What a PRD looks like at this level**: Comprehensive, well-structured, and professionally written. User stories have detailed acceptance criteria. Technical architecture is considered. Success metrics are defined. Dependencies and risks are documented. This is a solid PRD that would earn approval in most organizations.

**How to identify during review**:
- The PRD checks every box on a standard quality checklist.
- Features described are familiar -- they exist in competing products.
- The PRD prioritizes correctness and completeness over innovation.
- Success metrics focus on adoption and satisfaction rather than transformation.
- There is no section that makes you think "I have never seen this before."

---

## Summary: Stars 1-5

| Star | Label | Core Issue | Review Action |
|------|-------|-----------|---------------|
| 1 | Broken/missing | User need unaddressed | Flag as P0 gap in review |
| 2 | Hostile | Feature exists but punishes users | Flag as P0, recommend UX overhaul |
| 3 | Clunky | Works with workarounds | Flag as P1, identify specific friction points |
| 4 | Meets minimum | Functional but undifferentiated | Note as baseline, push for star 6+ on anchor features |
| 5 | Parity | Polished but not distinctive | Acceptable for table-stakes features, insufficient for anchor features |

Stars 1-3 represent quality defects that must be fixed. Stars 4-5 represent adequacy that should be questioned for the product's anchor features. The review should identify which features are table stakes (fine at 5 stars) and which are anchor features (must reach 6-8 stars for product differentiation).
