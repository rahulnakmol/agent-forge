---
category: template
template_type: validate
loading_priority: 2
tokens_estimate: 455
dependencies: [phases/phase-validate]
keywords: [validate-phase-templates, hypothesis-test-plan, mvp-definition, pilot-plan, validation-report, pivot-persevere-decision]
version: 1.0
last_updated: 2025-11-09
---

# Validate Phase Templates

## Overview

The Validate phase tests hypotheses, validates assumptions, and proves value through MVPs and pilots before full-scale implementation. This guide provides templates for key Validate phase deliverables that minimize risk and maximize learning.

**Skills-First Reminder**: Before creating any Validate phase document, ALWAYS check for available skills:
- **docx skill** → Hypothesis test plans, validation reports, lessons learned, refined requirements
- **pptx skill** → Pivot/persevere recommendations, stakeholder updates, demo presentations
- **xlsx skill** → Test metrics, user feedback analysis, cost tracking, success criteria scoring
- **pdf skill** → Formal validation reports, executive summaries, decision memos

## Hypothesis Testing Framework Template

### When to Use
Use hypothesis testing to validate critical assumptions before committing to full-scale implementation. Essential for:
- Unproven technology approaches
- New business models or processes
- User experience innovations
- Integration patterns
- Performance assumptions

### Template Structure

#### Hypothesis Test Plan (use **docx skill**)

```markdown
# Hypothesis Test Plan: [Initiative/Feature Name]

## Executive Summary
- What we're testing and why
- Key hypotheses
- Test approach and timeline
- Success criteria
- Resource requirements

## 1. Hypotheses to Test

### Hypothesis 1: [Primary Hypothesis]
**Statement**: We believe that [specific assumption] will result in [expected outcome] for [target users].

**Why This Matters**:
- Business impact if true
- Risk if assumption is false
- Dependencies on this hypothesis

**Success Criteria**:
- Metric 1: [Quantitative measure] achieves [target]
- Metric 2: [Qualitative measure] shows [evidence]
- Metric 3: [User behavior] demonstrates [outcome]

**Falsification Criteria** (when to pivot):
- Less than [X]% of users adopt feature
- Performance worse than [Y] seconds
- Negative feedback from more than [Z]% of participants

### Hypothesis 2: [Secondary Hypothesis]
[Repeat structure above]

### Hypothesis 3: [Technical Hypothesis]
**Example**: "We believe that Azure OpenAI + Dataverse integration can respond to user queries in under 2 seconds with 90% accuracy."

## 2. Test Design

### Scope of MVP
**In Scope**:
- Core features to test hypotheses
- Minimum viable integration points
- Essential user workflows
- Basic analytics and monitoring

**Out of Scope** (for later phases):
- Advanced features
- Full enterprise integration
- Production-scale performance
- Complete UI polish

### Test Environment
- Platform: [Azure/Power Platform/Dynamics/M365]
- User group: [Specific cohort, size, characteristics]
- Duration: [Time period]
- Geographic scope: [Location]

### Data Collection Methods
1. **Quantitative Metrics** (use **xlsx skill**):
   - Usage analytics (adoption, engagement, retention)
   - Performance metrics (response times, throughput)
   - Business outcomes (efficiency gains, cost reduction)

2. **Qualitative Feedback**:
   - User interviews (structured questions)
   - Observational studies (user behavior)
   - Feedback surveys (satisfaction, usability)

3. **Technical Validation**:
   - Performance benchmarks
   - Integration reliability
   - Scalability tests

## 3. Test Execution Plan

### Phase 1: Setup (Week 1-2)
- Environment provisioning
- Test data preparation
- User recruitment and onboarding
- Baseline measurement

### Phase 2: Execution (Week 3-6)
- MVP deployment
- User onboarding and training
- Continuous monitoring
- Weekly feedback sessions

### Phase 3: Analysis (Week 7-8)
- Data analysis and synthesis
- Hypothesis validation/invalidation
- Lessons learned documentation
- Recommendations formulation

### Roles & Responsibilities
| Role | Responsibility | Time Commitment |
|------|----------------|-----------------|
| Product Owner | Define success criteria, make pivot/persevere decisions | 20% |
| Solution Architect | Design MVP, technical validation | 50% |
| Test Users | Participate in pilot, provide feedback | Varies |
| Data Analyst | Measure and analyze results | 30% |
| Delivery Lead | Coordinate execution, manage timeline | 40% |

## 4. Success Criteria & Decision Framework

### Quantitative Targets (use **xlsx skill** for tracking)
| Metric | Baseline | Target | Stretch Goal | Measured How |
|--------|----------|--------|--------------|--------------|
| User adoption | 0% | 60% | 80% | Usage analytics |
| Task completion time | 30 min | 10 min | 5 min | Time tracking |
| User satisfaction | N/A | 4.0/5.0 | 4.5/5.0 | Survey |
| System response time | N/A | <2 sec | <1 sec | Performance monitoring |
| Error rate | N/A | <5% | <2% | Error logs |

### Decision Matrix
| Outcome | Criteria Met | Decision |
|---------|--------------|----------|
| **Strong Success** | All targets exceeded | Persevere → accelerate to Construct |
| **Success** | 80%+ targets met | Persevere → proceed to Construct with minor adjustments |
| **Partial Success** | 50-79% targets met | Pivot → refine approach and re-test |
| **Failure** | <50% targets met | Pivot significantly OR stop |

## 5. Risk Management

### Key Risks
| Risk | Impact | Likelihood | Mitigation | Contingency |
|------|--------|------------|------------|-------------|
| Low user participation | High | Medium | Early engagement, incentives | Expand user pool |
| Technical issues block testing | High | Medium | Thorough pre-testing, backup env | Manual workarounds |
| Inconclusive results | Medium | Medium | Clear metrics upfront, sufficient sample size | Extend test period |

## 6. Deliverables

- ☐ Hypothesis test plan (this document) → **docx skill**
- ☐ MVP implementation (configured environment)
- ☐ Test data and scripts
- ☐ User guide and training materials → **docx skill** or **pptx skill**
- ☐ Validation report → **docx/pdf skill**
- ☐ Pivot/persevere recommendation → **pptx skill**
- ☐ Lessons learned → **docx skill**
```

## Validation Report Template

### When to Use
Use the validation report to document test results, analyze findings, and make data-driven recommendations. Required for:
- Executive decision-making
- Investment approval for Construct phase
- Lessons learned capture
- Risk mitigation planning

### Template Structure (use **docx skill** or **pdf skill**)

```markdown
# Validation Report: [Initiative Name]

## Executive Summary
- Hypotheses tested
- Key findings (validated/invalidated)
- Recommendation (Pivot/Persevere)
- Confidence level in recommendation
- Next steps

## 1. Test Overview

### Hypotheses
| Hypothesis | Result | Confidence | Impact |
|------------|--------|------------|--------|
| H1: Users will adopt new workflow | ✅ VALIDATED | High | High |
| H2: Response time <2 sec achievable | ✅ VALIDATED | Medium | High |
| H3: 50% reduction in manual effort | ❌ INVALIDATED | High | Medium |

### Test Execution Summary
- Duration: [Start date] to [End date]
- Participants: [N users from X business unit]
- Environment: [Platform/tools used]
- Data collected: [Volume and types]

## 2. Detailed Findings

### Hypothesis 1: User Adoption
**Expected**: 60% of invited users actively use new workflow

**Actual Results** (use **xlsx skill** for charts):
- 72% of users completed onboarding
- 65% used system at least 3x per week
- 48% became daily active users
- NPS score: 42 (favorable)

**Analysis**:
- ✅ Exceeded target for active usage
- Strong initial adoption with gradual increase
- Power users emerged (15% driving 60% of usage)

**Evidence**:
- Usage analytics dashboard (Appendix A)
- User interview quotes (Appendix B)
- Adoption curve chart (see below)

**Key Learnings**:
- Users valued [specific feature] most highly
- Onboarding was critical to success
- Integration with existing tools drove adoption

### Hypothesis 2: Technical Performance
**Expected**: System responds to queries in under 2 seconds

**Actual Results**:
- Average response time: 1.7 seconds (✅ Met target)
- 95th percentile: 3.2 seconds (❌ Missed stretch goal)
- Peak load performance degraded to 4.5 seconds

**Analysis**:
- Performance acceptable for current user load
- Scaling concerns identified for 10x user base
- Azure OpenAI throttling observed during peaks

**Recommendations**:
- Implement caching for common queries
- Add request queuing for peak loads
- Consider Premium tier for production

### Hypothesis 3: Efficiency Gains
**Expected**: 50% reduction in task completion time

**Actual Results**:
- Average reduction: 35% (❌ Below target)
- Variation by user type: 20% (novice) to 55% (expert)
- Initial learning curve added 2 hours per user

**Analysis**:
- Benefit realization lower than expected initially
- Expert users achieved target gains
- Training investment required upfront

**Pivot Consideration**:
- Adjust success criteria to 35% or
- Enhance automation features or
- Improve user onboarding/training

## 3. User Feedback Analysis

### Quantitative Feedback (use **xlsx skill**)
| Question | Avg Score | Target | Result |
|----------|-----------|--------|--------|
| Overall satisfaction | 4.2/5.0 | 4.0 | ✅ |
| Ease of use | 3.8/5.0 | 4.0 | ⚠️ |
| Would recommend to colleague | 4.5/5.0 | 4.0 | ✅ |

### Qualitative Themes
**Positive Feedback**:
- "Saves me hours every week on reporting"
- "Love the AI-powered suggestions"
- "Much easier than the old system"

**Constructive Feedback**:
- "Needs better mobile experience"
- "Search functionality could be smarter"
- "Would like more customization options"

**Feature Requests** (prioritized by demand):
1. Mobile app (requested by 80% of users)
2. Bulk operations (45%)
3. Advanced filtering (40%)

## 4. Technical Learnings

### What Worked Well
- Power Platform + Dataverse integration performed reliably
- Azure OpenAI provided high-quality responses
- Model orchestration pattern proved flexible

### Challenges Encountered
- Initial latency higher than expected (resolved via caching)
- Dataverse connection throttling under load
- User authentication UX needed refinement

### Architecture Refinements
[Reference mermaid-diagram-patterns.md for before/after diagrams]
- Added Redis cache layer
- Implemented asynchronous processing for heavy queries
- Optimized Dataverse queries with selective field retrieval

## 5. Business Impact Assessment

### Realized Benefits (use **xlsx skill**)
- Time savings: 140 hours per month across pilot group
- Cost avoidance: $12,000 (annualized based on pilot)
- User satisfaction improvement: +25 points NPS

### Projected Benefits at Scale
- Annual time savings: 8,400 hours (500 users)
- Annual cost savings: $420,000
- Improved customer response time: 30% reduction

### ROI Calculation
- MVP investment: $85,000
- Projected annual benefit (scaled): $420,000
- Payback period: 2.4 months
- 3-year ROI: 1,380%

## 6. Risks & Mitigations

### Risks Identified During Validation
| Risk | Severity | Mitigation for Construct Phase |
|------|----------|--------------------------------|
| User adoption plateau | Medium | Enhanced change management, executive sponsorship |
| Performance at scale | High | Load testing, infrastructure scaling plan |
| Integration complexity | Medium | Phased rollout, thorough testing |

## 7. Recommendations

### Primary Recommendation: **PERSEVERE** ✅

**Rationale**:
- 2 of 3 core hypotheses validated
- Strong user adoption and satisfaction
- Clear path to address identified gaps
- Business case remains compelling

**Confidence Level**: High (85%)

### Conditions for Success in Construct Phase
1. **Must Have**:
   - Address performance scaling (caching, infrastructure)
   - Enhance user training program
   - Implement top 3 feature requests

2. **Should Have**:
   - Improve mobile experience
   - Add advanced customization
   - Create user community/champions program

3. **Nice to Have**:
   - AI model fine-tuning for domain-specific accuracy
   - Advanced analytics and reporting

### Refined Requirements for Construct
Based on validation learnings, update requirements:
- [List specific requirement changes]
- [Adjust technical architecture]
- [Revise success criteria]

## 8. Next Steps

### Immediate Actions (Week 1-2)
- [ ] Present findings to steering committee → **pptx skill**
- [ ] Secure approval for Construct phase
- [ ] Refine architecture based on learnings
- [ ] Update project plan and budget

### Construct Phase Preparation (Week 3-4)
- [ ] Finalize requirements document → **docx skill**
- [ ] Establish production environment
- [ ] Recruit and onboard delivery team
- [ ] Create detailed sprint plan

### Success Criteria for Construct
- Deliver full-featured solution within [X] months
- Achieve [Y]% user adoption across full user base
- Realize [Z]% of projected business benefits

## Appendices

### Appendix A: Detailed Metrics (use **xlsx skill**)
- Raw data exports
- Statistical analysis
- Trend charts and visualizations

### Appendix B: User Feedback
- Interview transcripts (summarized)
- Survey responses (anonymized)
- Observational study notes

### Appendix C: Technical Documentation
- Architecture diagrams → **mermaid-diagram-patterns.md**
- Performance benchmarks
- Integration test results
```

## MVP Scoping Template

### When to Use
Use MVP scoping to define the minimum feature set required to test hypotheses while minimizing development effort.

### Template Structure (use **docx skill**)

```markdown
# MVP Scope Definition: [Feature/Initiative]

## MVP Purpose
**Goal**: Test the hypothesis that [specific assumption] by delivering [minimal capability] to [target users].

**Success Metric**: [Quantifiable measure]

## Feature Prioritization: MoSCoW

### Must Have (Core MVP)
Features absolutely required to test hypotheses:
- ☑ User authentication (Azure AD SSO)
- ☑ Core workflow: Submit → Review → Approve
- ☑ Basic dashboard (status visibility)
- ☑ Email notifications
- ☑ Mobile-responsive UI

### Should Have (Enhance value)
Features that significantly improve UX but not critical for validation:
- ☐ Bulk operations
- ☐ Advanced search
- ☐ Customizable views
- ☐ Export to Excel

### Could Have (Nice to have)
Features that add value but can wait for later:
- ☐ Mobile native app
- ☐ Offline capability
- ☐ Advanced analytics
- ☐ Custom branding

### Won't Have (Explicitly descoped)
Features intentionally excluded from MVP:
- ✗ Multi-language support
- ✗ Complex approval workflows
- ✗ Integration with legacy System X
- ✗ Audit trail and compliance features

## Technical Scope

### In Scope
- Power Apps canvas app (single screen)
- Dataverse (3 tables, basic relationships)
- Power Automate (2 simple flows)
- Azure OpenAI (text generation API)

### Out of Scope (for production)
- High availability/disaster recovery
- Performance optimization
- Enterprise-scale security
- Production support processes

## Acceptance Criteria

### Functional Criteria
- [ ] User can complete end-to-end workflow in <5 clicks
- [ ] System responds to queries within 3 seconds
- [ ] 95% uptime during test period
- [ ] Zero data loss or corruption

### Non-Functional Criteria
- [ ] Deployable in <1 day
- [ ] Trainable in <30 minutes
- [ ] Usable without documentation for core tasks
- [ ] Supportable by existing team

## Estimated Effort
- Development: [X] days
- Testing: [Y] days
- Deployment: [Z] days
- **Total**: [T] days (vs [F] days for full solution)
```

## Lessons Learned Template

### When to Use
Capture lessons learned at the end of every Validate phase to improve future delivery.

### Template Structure (use **docx skill**)

```markdown
# Lessons Learned: [Initiative] Validate Phase

## Executive Summary
- Top 3 things that went well
- Top 3 things to improve
- Key recommendations for Construct phase

## What Went Well (Keep Doing)

### 1. [Success Area]
**What happened**: [Description]
**Why it worked**: [Root cause analysis]
**How to replicate**: [Actionable guidance]
**Responsible**: [Team/person]

### 2. Hypothesis-Driven Testing
**What happened**: Structured hypothesis framework prevented scope creep
**Why it worked**: Clear success criteria enabled objective decisions
**How to replicate**: Use hypothesis test plan template for all future MVPs
**Responsible**: Product Owner + Solution Architect

## What Didn't Go Well (Improve)

### 1. [Challenge Area]
**What happened**: [Description]
**Why it occurred**: [Root cause analysis]
**Impact**: [Consequences]
**How to prevent**: [Specific recommendations]
**Responsible**: [Team/person]

### 2. User Onboarding
**What happened**: First-week adoption was only 35%, well below 60% target
**Why it occurred**: Training was optional, not integrated into workflow
**Impact**: Extended validation period by 2 weeks
**How to prevent**: Mandatory hands-on workshop, in-app guidance, buddy system
**Responsible**: Change Management Lead

## Recommendations for Construct Phase

### Process Improvements
1. Start architecture refinement during validation (don't wait)
2. Involve production support team earlier
3. Allocate 20% buffer for unexpected learnings

### Technical Improvements
1. Invest in automated testing from day 1
2. Implement feature flags for gradual rollout
3. Establish performance baselines early

### Team & Collaboration
1. Weekly demo cadence worked well → continue
2. Add dedicated UX resource for polish
3. Increase stakeholder communication frequency

## Metrics for Continuous Improvement

| Metric | Validate Phase | Target for Construct |
|--------|----------------|----------------------|
| Hypothesis validation accuracy | 67% (2 of 3) | 80%+ |
| Time to first user feedback | 3 weeks | 1 week |
| MVP deployment time | 4 weeks | 2 weeks |
| User satisfaction (NPS) | 42 | 60+ |
```

## Best Practices for Validate Phase Templates

### 1. Hypothesis-Driven Approach
- Define clear, testable hypotheses upfront
- Establish quantitative success criteria
- Design minimum tests to validate/invalidate
- Accept failures as valuable learning

### 2. Fail Fast, Learn Fast
- Time-box validation activities (typically 4-8 weeks)
- Make pivot/persevere decisions based on data, not opinions
- Don't gold-plate MVPs
- Capture learnings in real-time

### 3. User-Centric Validation
- Test with real users, not proxies
- Observe actual behavior, not stated preferences
- Iterate based on feedback
- Build user champions early

### 4. Leverage All Available Skills
Before creating documents:
- **docx skill**: Plans, reports, requirements
- **pptx skill**: Decision presentations, demos
- **xlsx skill**: Metrics tracking, analysis
- **pdf skill**: Formal deliverables

### 5. Technical Rigor
- Test at realistic scale
- Validate integration points
- Measure performance objectively
- Document architecture learnings (use **mermaid-diagram-patterns.md**)

## Common Pitfalls to Avoid

1. **Building too much**: MVP scope creep defeats the purpose
2. **Testing too little**: Insufficient data leads to uninformed decisions
3. **Ignoring negative results**: Failed hypotheses are valuable learnings
4. **Skipping documentation**: Capture lessons while fresh
5. **Not involving users early**: Testing in isolation misses reality
6. **Analysis paralysis**: Don't over-analyze, make decision and move forward

## Related References

- **phase-validate.md**: Detailed guidance on Validate phase approach
- **vision-phase-templates.md**: Link to business case and hypotheses from Vision
- **mermaid-diagram-patterns.md**: Architecture diagrams for before/after, sequence flows
- **technical-documentation-templates.md**: For documenting MVP architecture
- **presentation-templates.md**: For pivot/persevere decision presentations
