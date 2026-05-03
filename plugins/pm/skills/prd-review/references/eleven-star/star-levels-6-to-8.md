# Star Levels 6 through 8: THE SWEET SPOT

This is the most important reference file in the review framework. Stars 6-8 represent the differentiation zone -- the range where products stop being "good enough" and start being "the reason customers choose you." The reviewer's primary job is to identify where a PRD's anchor features can feasibly reach this zone.

---

## Star 6: Anticipates User Needs

**Core principle**: The product does not wait for the user to ask. It proactively surfaces what the user needs next, before they realize they need it.

### Description

At star 6, the experience shifts from reactive to proactive. The user no longer drives every interaction; the product begins to meet them halfway. The feature demonstrates understanding of the user's context, workflow, and likely next action.

The emotional response is surprise followed by appreciation: "I was just about to do that" or "I didn't know I needed that, but it's exactly right."

### Detailed Criteria

- **Contextual awareness**: The feature uses available information (user history, current state, time, role) to anticipate needs
- **Proactive suggestions**: The system offers next steps, related items, or completions without being asked
- **Reduced cognitive load**: The user makes fewer decisions because the product pre-selects reasonable defaults based on context
- **Graceful degradation**: When the anticipation is wrong, dismissing the suggestion is effortless (not intrusive or patronizing)

### SaaS Product Example

A project management tool that, when a user marks a task as blocked, automatically surfaces:
- The dependency chain showing what is blocking this task
- The team member responsible for the blocking task
- A pre-drafted message to that team member asking for an update
- Similar past blockers and how they were resolved

The user did not search for any of this. The system recognized the pattern and assembled the relevant context.

### Consulting Engagement Example

A strategy document that does not just recommend "implement a data governance framework" but anticipates the client's next questions:
- Which teams will be impacted and what their likely resistance points are
- What quick wins can demonstrate value in the first 30 days
- Which existing processes can be repurposed rather than replaced
- What the typical failure modes are for this type of initiative and how to avoid them

### What Makes a PRD Aim for Star 6

- User stories include context about what the user was doing before and will do after
- Requirements specify intelligent defaults, not just empty forms
- The PRD describes what the system proactively surfaces, not just what it does when asked
- Edge cases are handled with helpful suggestions, not error messages
- The feature considers the user's workflow holistically, not in isolation

### Specific Review Questions

1. Does this feature wait for user input, or does it offer something proactively?
2. What information does the system have that it could use to anticipate the user's next need?
3. Are defaults based on context (smart) or arbitrary (static)?
4. When the user encounters a problem, does the system help them solve it or just report it?
5. Does the feature connect to adjacent workflows, or does it exist in isolation?

### Common Patterns at Star 6

- Auto-populating forms based on prior entries or context
- "You might also need..." suggestions at decision points
- Automatic escalation or notification when conditions are met
- Pre-computed answers to likely follow-up questions
- Progressive disclosure that surfaces complexity only when the user needs it

---

## Star 7: Creates Wow Moments

**Core principle**: The experience is so good that users spontaneously tell others about it. The product creates moments of genuine delight that become part of how users describe the product.

### Description

At star 7, the product crosses from "useful" to "remarkable" in the original sense -- worth remarking on. Users do not just appreciate the feature; they share it. They show it to colleagues. They mention it in reviews. The feature becomes a story.

The emotional response is delight and advocacy: "You have to see this" or "I can't believe it does this."

### Detailed Criteria

- **Unexpected value**: The feature delivers more than the user expected, in a way that feels generous rather than overwhelming
- **Emotional resonance**: The interaction creates a positive emotional response, not just task completion
- **Shareability**: The moment is concrete enough that users can describe it to others in one sentence
- **Consistency**: The wow moment is reproducible, not a one-time trick
- **Craft**: The detail and polish signal that someone cared deeply about this specific interaction

### SaaS Product Example

An analytics dashboard that, instead of showing a flat table of metrics, surfaces an insight: "Your conversion rate dropped 23% last Tuesday. This correlates with a 4-second increase in page load time after the 2pm deployment. Here's the commit." The user did not ask for root cause analysis. The system connected data across domains (analytics, infrastructure, version control) to tell a story.

Users do not say "our analytics tool shows metrics." They say "our analytics tool told us exactly which commit broke our conversion rate."

### Consulting Engagement Example

A process optimization deliverable that includes a "day in the life" video walkthrough showing a real employee (anonymized) performing the current process with a voice-over highlighting the 47 minutes of waste per day, then showing the redesigned process completing the same work in 12 minutes. The emotional impact of seeing the difference -- rather than reading about it in a table -- creates a wow moment that gets shared across the executive team.

### What Makes a PRD Aim for Star 7

- The PRD identifies specific moments in the user journey where the product can exceed expectations
- Requirements describe the user's emotional response, not just the functional outcome
- At least one feature is designed to be "the story" -- the thing users would describe at dinner
- Cross-domain data integration is specified (connecting information from multiple sources to create novel insights)
- The PRD includes examples of what the user sees/experiences, not just system behavior

### Specific Review Questions

1. If a user described this product to a friend, which feature would they mention first? Is that feature in the PRD?
2. Does any feature create a moment where the user learns something they did not know?
3. Is there a feature that connects information from separate domains to produce a novel insight?
4. Does the PRD describe any interaction where the user's response would be emotional (delight, surprise, relief) rather than merely functional (task complete)?
5. Could a user describe the best feature in one sentence? If not, the wow moment may be too abstract.

### Common Patterns at Star 7

- Cross-domain insight synthesis (connecting data the user would not connect themselves)
- "How did it know that?" moments driven by intelligent pattern recognition
- Time savings so dramatic they change the user's relationship with the task
- Visual or interactive experiences that make complex information intuitive
- Personalization that feels like the product was built specifically for this user

---

## Star 8: Fundamentally Changes How Users Think

**Core principle**: The product does not just solve the problem better -- it reframes the problem entirely. After using it, users cannot go back to the old way because the old way now feels broken.

### Description

At star 8, the product achieves something rare: it changes the user's mental model. The user does not just prefer this product; they cannot imagine working without it. The old approach -- which seemed perfectly fine before -- now feels primitive, tedious, or fundamentally limited.

The emotional response is revelation and permanent shift: "I can never go back to the old way" or "This made me realize we were thinking about this all wrong."

### Detailed Criteria

- **Mental model shift**: The feature introduces a new way of thinking about the problem that makes the old way feel inadequate
- **Irreversibility**: Once users experience this level, returning to the previous approach feels like a downgrade, not just a preference
- **Category redefinition**: The feature changes what users expect from this category of product
- **Emergent capability**: Users discover they can do things they could not do before -- not just do old things faster
- **Ecosystem effect**: The change in thinking spreads to adjacent workflows and tools

### SaaS Product Example

Slack did not just make team messaging faster than email. It changed how teams think about communication. After Slack, email feels like shouting into a void -- no threads, no presence indicators, no integrations, no searchable history by topic. Teams that adopted Slack did not "prefer" it to email for internal communication; they found email fundamentally inadequate for collaboration. The mental model shifted from "send messages to people" to "communicate in context."

Another example: Figma did not just make design collaboration easier. It eliminated the concept of "design file versions." After Figma, sending a Sketch file as an email attachment feels absurd. The mental model shifted from "files that designers own" to "living designs that teams share."

### Consulting Engagement Example

A digital transformation engagement that does not just implement new technology but fundamentally restructures how the client thinks about their business processes. Instead of "automate the existing approval workflow," the engagement reveals that the approval workflow exists because of a trust deficit that can be addressed with real-time visibility. Remove the trust deficit, and the approval steps become unnecessary. The client's mental model shifts from "how do we make approvals faster?" to "why do we need approvals at all?"

### What Makes a PRD Aim for Star 8

- The PRD challenges a fundamental assumption about how the problem domain works
- At least one feature enables something that was previously impossible, not just inconvenient
- The problem statement reframes the conventional understanding of the problem
- Requirements describe new capabilities (things users could not do before) rather than improvements to existing capabilities (things users can do faster)
- The PRD articulates a vision of the world after the product exists, and that world is meaningfully different from the current state

### Specific Review Questions

1. Does the PRD challenge any assumption that the industry takes for granted?
2. Is there a feature that enables a genuinely new capability (not just a faster version of an existing one)?
3. After using this product, would the user find competing products feel fundamentally broken?
4. Does the PRD describe a world-after that is qualitatively different from the world-before?
5. Can you identify the mental model shift? What did users believe before, and what will they believe after?

### Common Patterns at Star 8

- Eliminating steps that were previously considered necessary (not automating them -- removing them)
- Real-time collaboration replacing asynchronous file exchange
- Continuous insight replacing periodic reporting
- Contextual intelligence replacing manual configuration
- Unified views replacing tool-switching across multiple systems
- Self-service replacing gatekept processes

---

## Sweet Spot Strategy

Not every feature in a PRD should aim for star 8. The sweet spot strategy is:

1. **Identify 1-2 anchor features** that define the product's identity. These must reach 7-8 stars.
2. **Ensure table-stakes features** are at 5 stars (solid, polished, competitive). Stars 4 or below in table stakes is a quality defect.
3. **Push supporting features** to star 6 where feasible. Proactive behavior and intelligent defaults should be the norm, not the exception.
4. **Use star 9-11 thinking** to inspire the anchor features. Ask "what would 10 stars look like?" then work backward to find the feasible version at 7-8.

### Feature Portfolio Balance

| Feature Type | Target Star | Percentage of PRD |
|-------------|-------------|-------------------|
| Table stakes | 5 | 40-50% |
| Enhanced | 6 | 20-30% |
| Anchor / Differentiator | 7-8 | 15-25% |
| Aspirational (design exercise) | 9-11 | 0% (used to inspire, not to ship) |

A PRD where every feature aims for 7-8 stars is as problematic as one where every feature sits at 5. The first is infeasible; the second is undifferentiated. The reviewer's job is to ensure the right features get the right level of ambition.
