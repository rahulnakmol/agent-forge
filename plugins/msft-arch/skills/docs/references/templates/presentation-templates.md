---
category: template
template_type: presentation
loading_priority: 2
tokens_estimate: 438
dependencies: [phases/phase-vision, phases/phase-validate, phases/phase-deploy]
keywords: [presentation-templates, executive-briefing, technical-presentation, stakeholder-communication, slide-deck, visual-communication]
version: 1.0
last_updated: 2025-11-09
---

# Presentation Templates

## Overview

Enterprise architects create presentations for diverse audiences - from technical deep-dives to executive briefings. This guide provides templates for common presentation scenarios optimized for Microsoft ecosystem solutions.

**Skills-First Reminder**: Before creating ANY presentation, ALWAYS check for the **pptx skill**:
- **pptx skill** → All presentations (executive briefings, architecture reviews, roadmaps, demos)
- **docx skill** → Speaker notes, detailed handouts, follow-up documentation
- **xlsx skill** → Data for charts, financial models, metrics dashboards
- **pdf skill** → Final read-only versions for distribution

## Executive Briefing Template

### When to Use
Use executive briefings for C-level stakeholders who need strategic context and business outcomes, not technical details. Typical scenarios:
- Vision phase kickoff or approval
- Major investment decisions
- Steering committee updates
- Board presentations

### Template Structure (use **pptx skill**)

```
Slide 1: Title Slide
├── Initiative name
├── Presenter name & title
├── Date
└── Audience (e.g., "Executive Steering Committee")

Slide 2: Executive Summary (Single Slide)
├── Business context (1-2 sentences)
├── Proposed solution (2-3 bullets)
├── Investment required ($X over Y years)
├── Expected returns (ROI, payback period)
└── Decision required (Go/No-Go, funding approval, etc.)

Slide 3: Strategic Context
├── Market/competitive pressures
├── Customer expectations
├── Regulatory requirements
└── Alignment to corporate strategy

Slide 4: The Challenge
├── Current state pain points (3-4 bullets)
├── Quantified impact (costs, inefficiencies)
├── Risk of inaction
└── Visual: Before-state diagram (use mermaid-diagram-patterns.md)

Slide 5: The Solution (High-Level)
├── Vision statement
├── Key capabilities delivered (3-5 bullets)
├── Technology approach (platform-level only)
└── Visual: After-state diagram (use mermaid-diagram-patterns.md)

Slide 6: Business Benefits
├── Revenue growth opportunities
├── Cost reduction/avoidance
├── Risk mitigation
├── Competitive advantage
└── Chart: 5-year benefit realization (use xlsx skill)

Slide 7: Investment & Timeline
├── Total investment by category
├── Phased approach (high-level roadmap)
├── Resource requirements
└── Visual: Gantt chart (use mermaid-diagram-patterns.md)

Slide 8: Financial Summary
├── NPV, IRR, Payback period
├── Benefit-to-cost ratio
├── Sensitivity analysis summary
└── Chart: Investment vs. returns over time (use xlsx skill)

Slide 9: Risk Management
├── Top 3-5 risks
├── Mitigation strategies
├── Contingency plans
└── Overall risk rating (Low/Medium/High)

Slide 10: Implementation Approach
├── Delivery methodology (e.g., 5-phase approach)
├── Governance model
├── Change management strategy
└── Success criteria

Slide 11: Recommendation & Next Steps
├── Clear recommendation (Go/No-Go)
├── Conditions for success
├── Immediate actions required
├── Decision timeline
└── Call to action

Slide 12: Appendix Title (if needed)
└── "Additional Details Available"
```

### Content Guidelines

**Visual Hierarchy**:
- Title: 1-5 words maximum
- Body: 3-5 bullets per slide
- Each bullet: 1 line maximum (use sub-bullets sparingly)

**The 6-Second Rule**:
Each slide should convey its core message in 6 seconds of viewing.

**Data Visualization** (use **xlsx skill** for charts):
- Prefer charts over tables
- Use consistent color scheme (align with brand)
- Annotate key insights directly on charts
- Limit to 1-2 visualizations per slide

**Diagrams** (use **mermaid-diagram-patterns.md**):
- Use C4 Context diagrams for architecture overview
- Use Before/After comparisons for transformation
- Keep diagrams simple - hide complexity

## Architecture Review Presentation Template

### When to Use
Use architecture reviews for technical audiences (architects, engineers, technical leads) who need to understand design decisions, patterns, and implementation details. Common scenarios:
- Design approval gates
- Technical steering committee
- Peer review sessions
- Knowledge transfer

### Template Structure (use **pptx skill**)

```
Slide 1: Title Slide
├── Solution/System name
├── Architect name
├── Review date & version
└── Audience

Slide 2: Agenda
├── Context & Requirements
├── Architecture Overview
├── Design Decisions
├── Quality Attributes
├── Risks & Open Items
└── Q&A

Slide 3: Business Context
├── Business problem being solved
├── Key stakeholders
├── Success criteria
└── Constraints (budget, timeline, technology)

Slide 4: Requirements Summary
├── Functional requirements (top 5-7)
├── Non-functional requirements (performance, scalability, security)
├── Integration requirements
└── Compliance/regulatory requirements

Slide 5: Architecture Principles
├── Cloud-first (Azure landing zones)
├── API-driven integration
├── Zero Trust security
├── Observability by design
└── Cost optimization

Slide 6: C4 Context Diagram
├── System in context
├── Users and external systems
├── Key interactions
└── Diagram from mermaid-diagram-patterns.md (C4 Context)

Slide 7: C4 Container Diagram
├── High-level technology choices
├── Key containers (apps, databases, services)
├── Communication patterns
└── Diagram from mermaid-diagram-patterns.md (C4 Container)

Slide 8: Component View (for critical containers)
├── Internal structure of key container
├── Component responsibilities
├── Dependencies
└── Diagram from mermaid-diagram-patterns.md (C4 Component)

Slide 9: Deployment Architecture
├── Azure subscription/resource group structure
├── Networking topology
├── High availability setup
├── Disaster recovery approach
└── Diagram from mermaid-diagram-patterns.md (Deployment)

Slide 10: Integration Architecture
├── Integration patterns used
├── API strategy (REST, GraphQL, webhooks)
├── Event-driven flows (if applicable)
├── Data synchronization approach
└── Sequence diagram (use mermaid-diagram-patterns.md)

Slide 11: Data Architecture
├── Data storage strategy (Dataverse, SQL, Cosmos DB, etc.)
├── Data model overview
├── Data residency & sovereignty
├── Backup and retention
└── ER diagram (use mermaid-diagram-patterns.md)

Slide 12-16: Well-Architected Framework Assessment
Each slide covers one WAF pillar:

Slide 12: Reliability
├── Availability targets (SLA/SLO)
├── Redundancy & failover
├── Backup & DR strategy
└── Assessment: ✅ Met / ⚠️ Partial / ❌ Gap

Slide 13: Security
├── Zero Trust implementation
├── Identity & access management
├── Data protection (encryption at rest/in transit)
├── Compliance & auditing
└── Assessment: ✅ Met / ⚠️ Partial / ❌ Gap

Slide 14: Cost Optimization
├── Pricing tier selections
├── Reserved instances / savings plans
├── Auto-scaling strategy
├── FinOps practices
└── Monthly run-rate estimate

Slide 15: Operational Excellence
├── Monitoring & alerting
├── CI/CD pipeline
├── Infrastructure as Code
├── Support model
└── Runbook reference

Slide 16: Performance Efficiency
├── Performance targets
├── Scalability approach
├── Load testing results/plans
└── Optimization strategy

Slide 17-20: Architecture Decision Records (Top 4)
For each key decision:
├── Decision: [Technology/pattern choice]
├── Context: [Why decision was needed]
├── Alternatives considered
├── Rationale: [Why this choice]
└── Consequences: [Trade-offs]

Example:
Decision: Azure OpenAI vs. Azure ML custom model
Context: Need NLP capabilities for user query understanding
Alternatives: Azure ML, 3rd party API, open-source
Rationale: Faster time-to-market, enterprise-ready, strong accuracy
Consequences: Cost higher, vendor dependency, regional availability

Slide 21: Risks & Mitigations
├── Technical risks (performance, integration, etc.)
├── Delivery risks (skills, timeline, dependencies)
├── Operational risks (support, adoption, maintenance)
└── Risk mitigation strategies

Slide 22: Open Items & Decisions Needed
├── Unresolved design questions
├── Dependencies on other teams
├── Decisions required from this review
└── Follow-up actions & owners

Slide 23: Implementation Roadmap
├── Phasing strategy (if applicable)
├── Key milestones
├── Dependencies
└── Go-live timeline

Slide 24: Success Criteria
├── Functional acceptance criteria
├── Performance benchmarks
├── Security/compliance validation
└── Business outcome metrics

Slide 25: Q&A / Discussion
└── Open floor for questions
```

### Content Guidelines

**Technical Depth**:
Balance detail with clarity. Assume audience is technical but may not know your domain deeply.

**Diagrams Are Critical** (use **mermaid-diagram-patterns.md**):
- C4 diagrams for architecture views
- Sequence diagrams for complex interactions
- State diagrams for workflows
- ER diagrams for data models

**ADR Integration**:
Link to full ADR documents (use **architecture-decision-records.md** template).

**Live Demo** (when appropriate):
- Include backup slides in appendix
- Have environment ready to show
- Prepare 3-5 minute walkthrough

## Roadmap Presentation Template

### When to Use
Use roadmap presentations to communicate phased delivery plans, dependencies, and timelines. Essential for:
- Program kickoffs
- Quarterly planning reviews
- Stakeholder alignment
- Vendor/partner coordination

### Template Structure (use **pptx skill**)

```
Slide 1: Title Slide
Slide 2: Vision & Goals
├── North star vision
├── Strategic objectives
├── Success metrics
└── Timeline overview (e.g., "24-month transformation")

Slide 3: Roadmap Principles
├── Value-driven prioritization
├── Risk mitigation through phasing
├── Dependencies & sequencing
└── Flexibility for learning

Slide 4: Phasing Strategy
├── Phase 1: Foundation (Months 1-6)
├── Phase 2: Core Capabilities (Months 7-12)
├── Phase 3: Advanced Features (Months 13-18)
├── Phase 4: Scale & Optimize (Months 19-24)
└── Visual: High-level timeline (use mermaid-diagram-patterns.md Gantt)

Slides 5-8: Phase Details (one per phase)
For each phase:
├── Objectives
├── Key deliverables (epics/features)
├── Success criteria
├── Dependencies (internal & external)
├── Resource requirements
├── Risks
└── Estimated cost & timeline

Slide 9: Capability Delivery Timeline
├── Visual: Swim-lane diagram showing capability rollout
├── Color-coded by business area or technology stack
└── Milestones marked

Slide 10: Dependencies & Critical Path
├── Inter-phase dependencies
├── External dependencies (vendors, partners, other programs)
├── Critical path items
└── Risk mitigation for dependencies

Slide 11: Resource Plan
├── Team structure by phase
├── External partner engagement
├── Skills development plan
└── Resource onboarding timeline

Slide 12: Investment Profile
├── Budget by phase
├── CAPEX vs. OPEX breakdown
├── Funding milestones/gates
└── Chart: Spend curve over time (use xlsx skill)

Slide 13: Benefit Realization
├── When benefits start accruing
├── Cumulative benefit over time
├── Link to business case
└── Chart: Benefits vs. investment (use xlsx skill)

Slide 14: Governance & Checkpoints
├── Decision gates between phases
├── Steering committee cadence
├── Success criteria for phase progression
└── Pivot points (when to reassess)

Slide 15: Next Steps
├── Immediate actions (next 30 days)
├── Approvals needed
├── Kick-off timeline
└── Communication plan
```

## Demonstration / Walkthrough Presentation Template

### When to Use
Use demo presentations to showcase working solutions, MVPs, or proofs of concept. Ideal for:
- Validate phase results
- Sprint reviews
- User acceptance testing
- Sales/marketing demonstrations

### Template Structure (use **pptx skill**)

```
Slide 1: Title Slide
├── Solution name
├── Demo date
├── Presenter
└── Audience

Slide 2: What You'll See Today
├── Demo objectives
├── Scenario being demonstrated
├── Key features highlighted
├── What's out of scope (for this demo)
└── Duration: [X] minutes

Slide 3: Business Scenario
├── User persona
├── Business problem
├── Current state (pain)
└── Desired outcome

Slide 4: Solution Overview
├── High-level architecture (simple C4 Context)
├── Technology stack
├── Key capabilities
└── Integration points

Slides 5-10: Demo Script (Screenshots + Annotations)
For each key workflow:
├── Step-by-step screenshots with annotations
├── Callouts highlighting key features
├── Expected outcomes at each step
└── Connection to business value

Note: These are BACKUP slides. Live demo is preferred, but screenshots ensure message lands if demo fails.

Slide 11: Technical Highlights
├── Architecture pattern used
├── Performance achieved
├── Integration points demonstrated
├── Security features shown
└── Platform capabilities leveraged

Slide 12: User Feedback (if Validate phase)
├── Quotes from pilot users
├── NPS or satisfaction scores
├── Feature requests captured
└── Adoption metrics

Slide 13: What's Next
├── Roadmap for additional features
├── Production deployment plan
├── Scaling considerations
└── Timeline to general availability

Slide 14: Q&A
└── Open floor for questions
```

### Demo Best Practices

**Preparation**:
- Test demo environment 30 minutes before
- Have backup environment ready
- Practice walkthrough 3+ times
- Prepare for common failure modes

**Execution**:
- Tell a story, not just feature tour
- Connect each feature to business value
- Keep pace brisk (respect audience time)
- Pause for questions at logical breaks

**Fallback Plan**:
- Screenshots pre-loaded as backup slides
- Video recording of demo as alternative
- Be ready to pivot to discussion if tech fails

## Technical Deep-Dive Template

### When to Use
Use technical deep-dives for specialized audiences who need implementation-level details. Scenarios:
- Developer onboarding
- DevOps setup reviews
- Security assessments
- Troubleshooting sessions

### Template Structure (use **pptx skill**)

```
Slide 1: Title Slide
Slide 2: Scope of Deep-Dive
├── Component/area being covered
├── Audience assumptions (knowledge level)
├── Duration
└── Related documentation links

Slides 3-N: Technical Content
Structure varies by topic, but typically includes:
├── Architecture diagrams (detailed C4 Component views)
├── Code snippets (key algorithms, configurations)
├── Sequence diagrams (use mermaid-diagram-patterns.md)
├── State diagrams (use mermaid-diagram-patterns.md)
├── Configuration examples
├── Performance benchmarks
├── Deployment procedures
└── Troubleshooting guides

Final Slide: References & Resources
├── Documentation links
├── Code repositories
├── Support contacts
└── Related deep-dives
```

## Best Practices for All Presentations

### 1. Know Your Audience
- **Executives**: Business outcomes, investment, timeline, risk
- **Technical**: Design decisions, patterns, trade-offs, implementation
- **Business stakeholders**: Capabilities, user experience, benefits, change impact
- **Mixed audience**: Layer detail (summary upfront, detail in appendix)

### 2. Skills-First Approach
Always check for **pptx skill** before creating any presentation. The skill may:
- Provide templates aligned with corporate branding
- Offer advanced formatting and layout options
- Include best practices for visual design
- Support collaboration features

### 3. Visual Communication
- Use **mermaid-diagram-patterns.md** extensively for technical diagrams
- Use **xlsx skill** for data charts and financial models
- One message per slide
- Minimize text, maximize visuals
- Consistent color scheme and fonts

### 4. Storytelling Structure
All presentations should follow a narrative arc:
1. **Setup**: Context, problem, stakes
2. **Conflict**: Challenges, constraints, risks
3. **Resolution**: Solution, approach, benefits
4. **Call to Action**: Decision, next steps, timeline

### 5. Appendix Strategy
Keep main deck to 15-20 slides max. Use appendix for:
- Detailed analysis
- Backup data
- Alternative scenarios
- Technical deep-dives
- Frequently asked questions

### 6. Rehearsal & Refinement
- Practice full presentation at least twice
- Time yourself (aim for 2 minutes per slide)
- Anticipate questions and prepare answers
- Get peer review before high-stakes presentations

## Common Pitfalls to Avoid

1. **Too much text**: If you can read it, you're not listening to me
2. **Death by bullet points**: Use visuals, diagrams, charts instead
3. **Inconsistent messaging**: Align with business case and strategy documents
4. **Wrong level of detail**: Match depth to audience (executives ≠ developers)
5. **No call to action**: Always end with clear next steps and decisions needed
6. **Forgetting skills check**: Always verify **pptx skill** availability first
7. **Poor diagram quality**: Use **mermaid-diagram-patterns.md** for consistency
8. **Ignoring brand guidelines**: Check for user-uploaded skills with templates

## Presentation Checklist

Before Finalizing ANY Presentation:
- [ ] Checked for **pptx skill** availability
- [ ] Verified audience and adjusted depth appropriately
- [ ] Used diagrams from **mermaid-diagram-patterns.md** where applicable
- [ ] Included data charts from **xlsx skill** where needed
- [ ] Clear call to action on final slide
- [ ] Appendix with supporting details
- [ ] Rehearsed at least twice
- [ ] Spell-checked and grammar-checked
- [ ] Aligned with brand guidelines (if available)
- [ ] PDF version created for distribution (use **pdf skill**)

## Related References

- **mermaid-diagram-patterns.md**: Comprehensive diagram library (C4, sequence, state, ER, Gantt)
- **vision-phase-templates.md**: Business case and TOM content for executive briefings
- **validate-phase-templates.md**: MVP demo and validation report content
- **architecture-decision-records.md**: ADR content for architecture reviews
- **business-case-templates.md**: Financial analysis for investment slides
