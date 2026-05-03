# Star Levels 9 through 11: Aspirational / Magical

These levels are NOT design targets. They are thought exercises used during review to expand the possibility space, then work backward to find the feasible sweet spot at stars 6-8. If a PRD's anchor features aim at these levels without grounding, the Feasibility score should reflect that.

---

## Star 9: Feels Like Magic

**Core principle**: The product delivers results so accurate, timely, and personalized that it feels like it can read the user's mind. The underlying technology is invisible; the experience is indistinguishable from having a brilliant assistant who knows everything about you.

### Description

At star 9, the product operates with such precision that users stop thinking about how it works and start trusting it implicitly. Predictions are eerily accurate. Recommendations are exactly right. The system seems to understand intent, not just input.

The emotional response is wonder and deep trust: "How did it know?" followed by "I don't question it anymore."

### SaaS Product Example

A sales intelligence platform that tells a rep: "Do not send the proposal to Acme Corp today. Their CFO was just replaced (source: LinkedIn update 3 hours ago), their Q3 earnings missed by 12% (source: SEC filing), and similar companies in this situation delay purchasing decisions by 45 days on average. Instead, send a congratulatory note to the new CFO and schedule a re-engagement for Q1." The rep did not ask for any of this. The system synthesized signals across multiple data sources, applied pattern recognition from thousands of similar deals, and produced advice that a senior sales strategist would give.

### Consulting Engagement Example

A transformation advisory engagement where the consultant appears to predict every stakeholder objection before it is raised, because the firm's knowledge base contains pattern-matched data from 200 similar engagements. The client feels like the consultant has done this exact project before, even though every engagement is unique.

### What a PRD Looks Like at This Level

Requirements describe AI/ML capabilities that synthesize data across multiple domains, predict user behavior with high accuracy, and act autonomously on the user's behalf. The PRD specifies personalization so deep that each user effectively has a bespoke product.

### Role in Review

When reviewing a PRD, ask: "What would star 9 look like for this feature?" Use the answer to challenge whether the PRD's current ambition (likely star 5-6) could feasibly move one level higher. Star 9 is the provocative question, not the target.

---

## Star 10: 10x Workflow Transformation

**Core principle**: The product does not just improve the specific task -- it transforms the entire workflow that the task lives within. The impact radiates outward from the feature to reshape how the user's team, department, or organization operates.

### Description

At star 10, the product's impact extends far beyond its immediate function. It creates a cascade effect where improving one task fundamentally changes the workflow around it. Adjacent processes are simplified, eliminated, or reimagined because the product has changed what is possible.

The emotional response is paradigm shift: "This didn't just change how I do X -- it changed how my whole team works."

### SaaS Product Example

A document collaboration platform that does not just make editing faster but eliminates the entire review-approve-distribute cycle. Documents are always live, always current, always accessible. The concept of "document versions" disappears. Meetings that existed solely to review document status are eliminated. The approval workflow collapses because stakeholders can see changes in real time and comment asynchronously. The product did not optimize the workflow; it dissolved it.

### Consulting Engagement Example

An operating model redesign that does not just streamline the finance close process but eliminates the concept of a "close period" entirely by implementing continuous accounting. Month-end close, which consumed 10 business days and 40 people, becomes a button click that produces auditable financials at any moment. The transformation is not about doing the close faster -- it is about making the close a non-event.

### What a PRD Looks Like at This Level

Requirements describe capabilities that would require fundamental changes to organizational structure, role definitions, or business processes beyond the product's immediate scope. The PRD implicitly assumes a level of organizational readiness and change management that is rarely present.

### Role in Review

Star 10 thinking reveals whether the PRD is thinking big enough about the problem space. Ask: "If this feature worked perfectly, what else would change?" If the answer is "nothing else changes," the feature may be too narrowly scoped. If the answer reveals a cascade of improvements, the PRD may benefit from acknowledging that broader vision even if v1 is more modest.

---

## Star 11: The Problem Ceases to Exist

**Core principle**: The product is so effective that the problem it was designed to solve no longer exists. The need for the product itself disappears because the underlying condition has been resolved.

### Description

At star 11, the product achieves the ultimate outcome: the user no longer needs it. The problem has been permanently resolved, prevented, or restructured out of existence. This is the theoretical endpoint of any solution -- so effective it is self-eliminating.

The emotional response is liberation: "I used to worry about this. Now I don't even think about it."

### SaaS Product Example

A cybersecurity platform whose endpoint is not "detect and respond to threats faster" but "threats cannot reach the organization." Not better antivirus -- an architecture where malware has no attack surface. The security team does not monitor alerts because there are no alerts. The problem (security threats reaching the organization) has ceased to exist within this architecture.

### Consulting Engagement Example

A supply chain optimization engagement whose endpoint is not "optimize inventory levels" but "inventory as a concept is unnecessary." Real-time demand sensing, distributed manufacturing, and on-demand production eliminate the need to hold inventory. The client does not manage inventory better -- they do not have inventory.

### What a PRD Looks Like at This Level

This is almost never what a PRD describes, and that is correct. Star 11 is a philosophical exercise. However, the question "What would it mean for this problem to not exist?" often reveals that the PRD is solving a symptom rather than a root cause. That insight can push the PRD from star 5 to star 7.

### Role in Review

Star 11 is the ultimate "challenge the default" question. Ask: "Why does this problem exist in the first place? What would need to change for it to not exist?" The answer rarely produces a feasible feature, but it often reveals:

- The PRD is solving a downstream symptom when the root cause is addressable
- An entire feature category could be replaced by eliminating the condition that necessitates it
- The product's long-term vision should point toward problem elimination, even if v1 addresses symptoms

---

## Using Stars 9-11 in Review

### The Backward Design Exercise

For each anchor feature in the PRD:

1. **Describe the star 11 version**: What would it mean for this problem to not exist?
2. **Describe the star 10 version**: What if this feature transformed the entire workflow?
3. **Describe the star 9 version**: What if this feature felt like magic?
4. **Now ask**: Which elements of stars 9-11 could be partially achieved at star 7-8?

This exercise typically surfaces 2-3 concrete improvements that push the feature from "functional" to "differentiated" without requiring magical technology.

### Warning Signs in PRDs

If a PRD's features genuinely sit at stars 9-11 without qualification:
- **Flag Feasibility concerns**: The technology or organizational change required may not exist
- **Check for hand-waving**: Phrases like "AI will automatically..." or "the system intelligently..." without specifying how are star 9-11 aspirations disguised as requirements
- **Verify grounding**: Is there a credible technical approach, or is this speculative?
- **Score Feasibility accordingly**: A beautiful vision with no path to implementation is not a PRD -- it is a wish list

### The Grounding Test

For any feature that appears to target star 9-11, apply the grounding test:

1. Can you describe the specific algorithm, data source, or mechanism that enables this?
2. Does similar capability exist in any product today, even in a different domain?
3. Can the team build a meaningful v1 of this in the stated timeline?
4. What is the degraded experience if the ambitious version fails? Is it still star 5+?

If the answer to all four questions is "no," the feature needs to be brought back to earth. If the answer to 2-3 is "yes," the ambition may be justified.
