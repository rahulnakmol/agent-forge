---
category: template
template_type: vision
loading_priority: 2
tokens_estimate: 377
dependencies: [phases/phase-vision]
keywords: [vision-phase-templates, target-operating-model, functional-tom, technical-tom, gap-analysis, roadmap, stakeholder-alignment]
version: 1.0
last_updated: 2025-11-09
---

# Vision Phase Templates

## Overview

The Vision phase establishes strategic direction, aligns stakeholders, and creates the business case for transformation. This guide provides templates for the key deliverables required during Vision phase engagements.

**Skills-First Reminder**: Before creating any Vision phase document, ALWAYS check for available skills:
- **docx skill** → TOM documentation, gap analysis, maturity assessments, ADRs
- **pptx skill** → Vision strategy presentations, roadmap decks, executive briefings
- **xlsx skill** → Business case financials, cost models, benefit quantification, maturity scoring
- **pdf skill** → Formal reports, executive summaries, final deliverables

## Target Operating Model (TOM) Template

### When to Use
Use the TOM template when defining the aspirational future state for an organization's technology, processes, and people. TOMs are essential for:
- Major digital transformation initiatives
- Cloud migration programs
- Post-merger technology integration
- Platform modernization efforts

### Template Structure

#### 1. Executive Summary
- Strategic context and business drivers
- Vision statement (2-3 sentences)
- Expected outcomes and success metrics
- Investment overview (high-level)
- Timeline and phasing approach

#### 2. Current State Assessment
- Technology landscape (systems, platforms, integrations)
- Process maturity and efficiency
- Organizational structure and capabilities
- Pain points and constraints
- Technical debt inventory

#### 3. Future State Vision

**Functional TOM** (use **docx skill**):
```
Business Capabilities
├── Customer Experience
│   ├── Omnichannel engagement
│   ├── Self-service portals
│   └── Personalization engine
├── Operations
│   ├── Process automation
│   ├── Workflow orchestration
│   └── Knowledge management
└── Analytics & Insights
    ├── Real-time dashboards
    ├── Predictive analytics
    └── AI-powered recommendations
```

**Technical TOM** (use **docx skill** + **mermaid-diagram-patterns.md**):
- Reference architecture (C4 Context/Container diagrams)
- Platform components and services
- Integration patterns and data flows
- Security and identity architecture
- Deployment topology

#### 4. Gap Analysis
- Capability gaps (current vs. target)
- Technology gaps (platforms, services, tools)
- Skills and organizational gaps
- Process and governance gaps

Use **mermaid-diagram-patterns.md** for Before/After comparison diagrams.

#### 5. Transformation Roadmap
- Phasing strategy (waves/releases)
- Dependencies and prerequisites
- Risk mitigation approach
- Change management plan

Use Gantt charts from **mermaid-diagram-patterns.md** for timeline visualization.

### Example TOM Document Outline

```markdown
# Target Operating Model: [Organization] Digital Transformation

## 1. Executive Summary
- Business context
- Strategic vision
- Expected outcomes
- Investment summary

## 2. Current State Analysis
### 2.1 Technology Landscape
- Applications inventory
- Infrastructure overview
- Integration architecture
- Data architecture

### 2.2 Business Capabilities
- Capability maturity assessment
- Process efficiency metrics
- Customer satisfaction scores

### 2.3 Organizational Readiness
- Skills inventory
- Change capacity
- Governance maturity

## 3. Target Operating Model
### 3.1 Functional TOM
- Business capability model
- Process design (future state)
- Operating model principles

### 3.2 Technical TOM
- Reference architecture
- Platform strategy
- Integration patterns
- Data strategy
- Security architecture

### 3.3 Organization & Governance
- Target org structure
- Roles and responsibilities
- Governance model
- Decision rights

## 4. Gap Analysis & Transformation Path
### 4.1 Capability Gaps
- High-priority gaps
- Dependencies
- Remediation approach

### 4.2 Technology Gaps
- Platform selection
- Migration strategy
- Build vs. buy decisions

### 4.3 Organizational Gaps
- Skills development plan
- Hiring strategy
- Change management approach

## 5. Roadmap & Phasing
### 5.1 Transformation Waves
- Wave 1: Foundation (Months 1-6)
- Wave 2: Core capabilities (Months 7-12)
- Wave 3: Advanced features (Months 13-18)

### 5.2 Dependencies
- Critical path items
- External dependencies
- Risk mitigation

## 6. Success Metrics & KPIs
- Business outcomes
- Technical metrics
- User adoption indicators
```

## Gap Analysis Template

### When to Use
Use gap analysis to quantify the delta between current and target states. Essential for:
- Business case development
- Roadmap prioritization
- Resource planning
- Risk assessment

### Template Structure

Create using **docx skill** with diagrams from **mermaid-diagram-patterns.md** (Before/After section).

#### Gap Analysis Document Outline

```markdown
# Gap Analysis: [Initiative Name]

## Executive Summary
- Scope of analysis
- Key findings
- Recommended actions
- Investment implications

## 1. Capability Gap Analysis

### Business Capabilities
| Capability | Current Maturity | Target Maturity | Gap | Priority | Effort |
|------------|------------------|-----------------|-----|----------|--------|
| Customer 360 | Level 2 (Managed) | Level 4 (Optimizing) | 2 levels | High | 12 months |
| Process Automation | Level 1 (Initial) | Level 4 (Optimizing) | 3 levels | High | 18 months |
| Data Analytics | Level 2 (Managed) | Level 5 (Innovating) | 3 levels | Medium | 24 months |

### Technology Capabilities
| Area | Current State | Target State | Gap Description | Remediation |
|------|---------------|--------------|-----------------|-------------|
| Cloud Platform | On-premises only | Azure hybrid | No cloud presence | 6-month migration |
| Integration | Point-to-point | API-first | 50+ integrations to refactor | 12-month program |
| Security | Perimeter-based | Zero Trust | Identity modernization needed | 9-month initiative |

## 2. As-Is vs. To-Be Architecture

### Current Architecture Limitations
- [Diagram using mermaid-diagram-patterns.md]
- Scalability constraints
- Integration complexity
- Maintenance burden

### Target Architecture Benefits
- [Diagram using mermaid-diagram-patterns.md]
- Cloud-native scalability
- API-driven integration
- Reduced technical debt

## 3. Organizational Gaps

### Skills & Competencies
| Required Skill | Current Level | Target Level | Gap | Plan |
|----------------|---------------|--------------|-----|------|
| Azure architecture | 2 people | 8 people | 6 FTE | Hire + train |
| Power Platform development | 5 people | 15 people | 10 FTE | Upskill existing |
| DevOps practices | Limited | Enterprise-wide | Broad gap | Training program |

### Process Maturity
- Current: Ad-hoc project delivery
- Target: Standardized, automated delivery
- Gap: Lack of templates, automation, governance

## 4. Prioritized Remediation Plan

### Critical Path Items (Must Have)
1. Cloud platform establishment (Months 1-3)
2. Identity and access management (Months 2-4)
3. Core integration platform (Months 3-6)

### High Priority (Should Have)
4. Data platform modernization (Months 4-9)
5. Application migration wave 1 (Months 6-12)
6. Security controls implementation (Months 4-10)

### Future Enhancements (Nice to Have)
7. Advanced analytics capabilities (Months 12-18)
8. AI/ML platform (Months 15-24)

## 5. Investment Summary
- Gap remediation costs by category
- Resource requirements (FTE)
- Timeline and phasing
- Risk-adjusted budget
```

## Business Case Template

### When to Use
Use the business case template to justify investment in transformation initiatives. Required for:
- Executive approval
- Budget allocation
- Program prioritization
- Stakeholder alignment

### Template Structure

Use **xlsx skill** for financial models and **docx skill** for narrative.

#### Business Case Document Outline

```markdown
# Business Case: [Initiative Name]

## Executive Summary
- Strategic alignment
- Investment required
- Expected returns
- Recommendation

## 1. Strategic Context

### Business Drivers
- Market pressures
- Competitive landscape
- Customer expectations
- Regulatory requirements

### Strategic Objectives
- Objective 1: [Description + success metric]
- Objective 2: [Description + success metric]
- Objective 3: [Description + success metric]

### Alignment to Corporate Strategy
- How initiative supports strategic goals
- Contribution to competitive advantage
- Risk of not proceeding

## 2. Solution Overview

### Proposed Solution
- High-level description
- Key capabilities delivered
- Technology platforms
- Implementation approach

### Alternatives Considered
| Option | Pros | Cons | Cost | Decision |
|--------|------|------|------|----------|
| Option 1: Full transformation | Complete modernization | High cost, high risk | $5M | **RECOMMENDED** |
| Option 2: Incremental | Lower risk | Slower value realization | $3M | Not selected |
| Option 3: Status quo | No investment | Competitive disadvantage | $0 | Not viable |

## 3. Financial Analysis

### Investment Required (use **xlsx skill**)
- Initial capital expenditure
- Recurring operational costs
- Resource costs (internal + external)
- Training and change management
- Contingency

### Benefits & Returns (use **xlsx skill**)

**Quantified Benefits** (5-year view):
- Revenue growth: $X from new capabilities
- Cost reduction: $Y from automation
- Cost avoidance: $Z from modernization
- Productivity gains: $W from process improvement

**Qualitative Benefits**:
- Improved customer satisfaction
- Enhanced employee experience
- Reduced risk and compliance burden
- Increased agility and innovation capacity

### Financial Metrics (use **xlsx skill**)
- NPV (Net Present Value)
- IRR (Internal Rate of Return)
- Payback period
- ROI % over 5 years
- Break-even analysis

## 4. Risk Analysis

### Key Risks
| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| Executive sponsorship lost | High | Medium | Strong governance, regular communication | Program Sponsor |
| Skills shortage | Medium | High | Training program, external partners | HR + IT |
| Integration complexity | High | Medium | Phased approach, proof of concept | Solution Architect |

### Sensitivity Analysis (use **xlsx skill**)
- Impact of 20% cost overrun
- Impact of 6-month delay
- Impact of 30% lower adoption
- Best/worst/likely scenarios

## 5. Implementation Roadmap

### Phasing Strategy
- Phase 1: Foundation (Q1-Q2)
- Phase 2: Core delivery (Q3-Q4)
- Phase 3: Scale and optimize (Year 2)

### Resource Requirements
- Program team structure
- External partner engagement
- Business stakeholder commitment

### Success Metrics
- Financial KPIs
- Operational KPIs
- User adoption metrics
- Technical quality indicators

## 6. Recommendation

Clear recommendation with:
- Investment ask
- Expected timeline
- Key dependencies
- Decision criteria
- Next steps
```

## Maturity Assessment Template

### When to Use
Use maturity assessments to baseline capabilities and measure progress. Common frameworks:
- CMMI (Capability Maturity Model Integration)
- Custom capability models
- Technology-specific maturity scales

### Template Structure (use **xlsx skill** for scoring, **docx skill** for report)

```markdown
# Maturity Assessment: [Domain/Capability]

## Assessment Framework

### Maturity Levels
1. **Initial**: Ad-hoc, reactive, unpredictable
2. **Managed**: Planned, tracked, repeatable
3. **Defined**: Standardized, documented, proactive
4. **Quantitatively Managed**: Measured, controlled, predictable
5. **Optimizing**: Continuous improvement, innovative

## Assessment Results

### Capability Scorecard (use **xlsx skill**)

| Capability Area | Current Level | Evidence | Target Level | Gap | Priority |
|-----------------|---------------|----------|--------------|-----|----------|
| Cloud Architecture | 2 | Some cloud use, no standards | 4 | 2 | High |
| Data Management | 1 | Siloed, inconsistent | 4 | 3 | High |
| DevOps | 2 | Manual deployments | 4 | 2 | Medium |
| Security | 3 | Policies defined | 4 | 1 | Medium |

### Domain Deep-Dive

#### Cloud Architecture (Example)
**Current State (Level 2 - Managed)**:
- Some workloads in Azure
- No formal cloud adoption framework
- Inconsistent governance
- Limited automation

**Target State (Level 4 - Quantitatively Managed)**:
- Cloud-first strategy
- CAF-aligned landing zones
- Automated compliance monitoring
- FinOps practices implemented

**Gap Remediation**:
1. Establish cloud governance framework
2. Deploy standardized landing zones
3. Implement policy-as-code
4. Enable cost optimization

## Recommendations

### Quick Wins (0-3 months)
- Low-hanging fruit
- High impact, low effort

### Strategic Investments (6-18 months)
- Transformational changes
- Require significant investment

### Long-term Vision (18+ months)
- Aspirational capabilities
- Continuous improvement focus
```

## Best Practices for Vision Phase Templates

### 1. Always Start with Skills Check
Before creating any document, verify which skills are available:
```bash
# Check for document creation skills
ls /path/to/skills/
# Look for: pptx, docx, xlsx, pdf skills
```

### 2. Use Consistent Formatting
- Professional, executive-ready appearance
- Clear hierarchy and navigation
- Visual elements (diagrams, charts)
- Brand alignment when available

### 3. Leverage Mermaid Diagrams
Reference **mermaid-diagram-patterns.md** for:
- Before/After comparisons (gap analysis)
- C4 diagrams (TOM architecture)
- Gantt charts (roadmaps)
- Context maps (DDD bounded contexts)

### 4. Quantify Everything
Use **xlsx skill** for:
- Maturity scoring models
- Financial analysis
- Benefit quantification
- Risk-adjusted calculations

### 5. Tell a Compelling Story
Structure documents to:
- Start with business context
- Build the case for change
- Paint vision of future state
- Provide clear path forward
- End with specific asks/recommendations

## Common Pitfalls to Avoid

1. **Creating documents without checking skills**: Always verify which skills are available first
2. **Technology-first thinking**: Start with business outcomes, not technology features
3. **Unrealistic timelines**: Account for organizational change capacity
4. **Vague benefits**: Quantify and validate all claimed benefits
5. **Ignoring constraints**: Address budget, skills, and political realities
6. **Missing stakeholder alignment**: Ensure executive sponsorship before proceeding

## Related References

- **phase-vision.md**: Detailed guidance on Vision phase approach
- **mermaid-diagram-patterns.md**: Diagram templates for TOM, gap analysis, roadmaps
- **business-case-templates.md**: Detailed financial analysis templates
- **domain-driven-design.md**: Context mapping for functional TOM
- **core-platforms.md**: Platform-specific TOM considerations
