---
category: quality
loading_priority: 2
tokens_estimate: 9600
keywords: [quality-standards, deliverable-quality, review-criteria, architecture-quality]
---

# Quality Standards and Review Guidelines

## Overview

This document establishes comprehensive quality standards for all enterprise architecture deliverables produced through the architecture skills suite. These standards ensure consistency, accuracy, and value delivery across all phases of the Solution Accelerator Methodology (SAM) framework. All deliverables must meet these quality gates before presentation to stakeholders.

## Quality Gates

Quality gates are mandatory checkpoints that must be passed before proceeding to the next phase of the engagement. Each gate includes specific criteria, required artifacts, and sign-off requirements.

### Vision Phase Exit Criteria

**Business Alignment**
- Problem statement clearly articulated and validated by business stakeholders
- Business objectives quantified with measurable success metrics
- Stakeholder analysis complete with roles and influence mapped
- Executive sponsor identified and committed
- Budget range established and approved for next phase

**Technical Readiness**
- Current state architecture documented at appropriate level of detail
- Technical constraints and dependencies identified
- Integration requirements catalogued
- Data architecture considerations outlined
- Security and compliance requirements captured

**Deliverable Quality**
- Vision document reviewed and approved by steering committee
- Presentation materials refined based on stakeholder feedback
- Business case developed with ROI projections
- Risk register initiated with mitigation strategies
- Project charter drafted with scope boundaries

**Go/No-Go Decision Factors**
- Executive sponsorship confirmed (MANDATORY)
- Budget availability validated (MANDATORY)
- Resource commitment secured (MANDATORY)
- Strategic alignment verified (HIGH)
- Technical feasibility validated (HIGH)
- Risk profile acceptable (MEDIUM)

### Validate Phase Exit Criteria

**Architecture Quality**
- Solution architecture aligns with Microsoft Well-Architected Framework
- All five pillars addressed (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency)
- Architecture Decision Records (ADRs) documented for key decisions
- Reference architectures from Azure/Power Platform Architecture Center incorporated
- Integration patterns validated against enterprise standards

**Technical Validation**
- Proof of concept successfully demonstrates critical functionality
- Performance testing validates scalability requirements
- Security assessment completed with no critical findings unresolved
- Data migration strategy proven feasible
- Integration approach validated with actual endpoints

**Business Case Refinement**
- Cost estimates refined to +/- 15% accuracy
- ROI calculations validated with finance team
- Implementation timeline detailed to phase/sprint level
- Resource requirements specified (FTEs, skills, third-party)
- Change management impact assessed

**Deliverable Quality**
- Architecture diagrams follow Microsoft Visio/Draw.io standards
- Technical specifications complete and reviewed
- Proof of concept documentation includes code samples and test results
- Risk register updated with detailed mitigation plans
- Steering committee approval documented

**Go/No-Go Decision Factors**
- POC demonstrates technical viability (MANDATORY)
- Costs within approved budget range (MANDATORY)
- Security risks mitigated to acceptable levels (MANDATORY)
- Implementation timeline realistic (HIGH)
- Resource availability confirmed (HIGH)
- Stakeholder alignment maintained (MEDIUM)

### Construct Phase Exit Criteria

**Development Quality**
- Code reviews completed for all custom development
- Unit test coverage meets minimum thresholds (80% for critical components)
- Security scanning completed with no high-severity vulnerabilities
- Performance testing validates SLA requirements
- Integration testing successful across all systems
- User acceptance testing passed with sign-off

**Documentation Completeness**
- Technical documentation complete and accessible
- User documentation drafted and reviewed
- Administrator guides created with runbooks
- API documentation generated (if applicable)
- Architecture diagrams updated to reflect as-built state
- Change logs and release notes prepared

**Operational Readiness**
- Support team trained and runbooks validated
- Monitoring and alerting configured
- Backup and disaster recovery tested
- Service level objectives (SLOs) defined and baselined
- Incident response procedures documented
- Knowledge transfer sessions completed

**Deliverable Quality**
- Solution builds successfully in all environments
- Deployment automation tested and validated
- Configuration management documented
- Security controls implemented and verified
- Compliance requirements met with evidence

**Go/No-Go Decision Factors**
- All test cases passed (MANDATORY)
- No critical or high-severity bugs open (MANDATORY)
- Security assessment approved (MANDATORY)
- Performance SLAs met in testing (HIGH)
- Documentation complete (HIGH)
- Training completed (MEDIUM)

### Deploy Phase Exit Criteria

**Deployment Execution**
- Production deployment successful with no rollback
- Post-deployment validation tests passed
- Performance monitoring showing expected metrics
- User access provisioned and tested
- Data migration validated for completeness and accuracy
- Integrations functioning in production environment

**User Adoption**
- End user training completed with attendance tracked
- Super users/champions identified and trained
- Help desk prepared with knowledge base and escalation procedures
- User feedback collected and addressed
- Early adoption metrics meeting targets

**Business Value**
- Key performance indicators (KPIs) baselined
- Initial business metrics showing positive trends
- Stakeholder satisfaction surveyed
- Value realization tracking initiated
- Success stories documented

**Deliverable Quality**
- Final architecture documentation updated
- Deployment runbook validated
- Production support handoff completed
- Lessons learned session conducted and documented
- Project closure report approved

**Go/No-Go Decision Factors**
- Production deployment stable (MANDATORY)
- Critical business processes functioning (MANDATORY)
- User access working correctly (MANDATORY)
- Performance acceptable (HIGH)
- No critical incidents in first 48 hours (HIGH)
- Training completion rate >80% (MEDIUM)

### Evolve Phase Exit Criteria

**Continuous Improvement**
- Monthly operational review meetings established
- Performance metrics trending positively
- User adoption increasing or stable at target levels
- Technical debt being actively managed
- Enhancement requests prioritized and roadmapped

**Value Realization**
- ROI targets being met or on track
- Business KPIs showing improvement
- User satisfaction scores meeting targets
- Cost optimization opportunities identified and implemented
- Innovation pipeline established for future capabilities

**Sustainability**
- Knowledge transfer completed to operational teams
- Documentation kept current with changes
- Compliance attestations maintained
- Security patching processes operating
- Disaster recovery tested quarterly

## Review Checklists

### Architecture Review Checklist

This checklist ensures architecture designs align with Microsoft Well-Architected Framework principles and enterprise standards.

**Reliability Assessment**
- [ ] Target SLA defined and achievable (99.9%, 99.95%, 99.99%)
- [ ] Single points of failure identified and mitigated
- [ ] Fault tolerance mechanisms implemented (retry logic, circuit breakers)
- [ ] Backup and restore strategy defined with RPO/RTO
- [ ] Disaster recovery plan documented and tested
- [ ] High availability configuration appropriate for SLA
- [ ] Regional redundancy considered for critical workloads
- [ ] Health monitoring and alerting configured
- [ ] Chaos engineering approach defined for resilience testing

**Security Assessment**
- [ ] Zero Trust principles applied (verify explicitly, least privilege, assume breach)
- [ ] Identity and access management strategy defined (Azure AD, RBAC)
- [ ] Data protection mechanisms implemented (encryption at rest and in transit)
- [ ] Network security controls in place (NSGs, firewalls, private endpoints)
- [ ] Threat detection and response capabilities configured (Defender, Sentinel)
- [ ] Vulnerability management process established
- [ ] Security baseline compliance validated (CIS benchmarks)
- [ ] Privileged access management implemented (PIM)
- [ ] Security incident response plan documented
- [ ] Regular security assessments scheduled

**Cost Optimization Assessment**
- [ ] Azure Pricing Calculator estimates documented
- [ ] Right-sizing analysis completed for all resources
- [ ] Reserved instances evaluated for predictable workloads
- [ ] Spot/Burstable VMs considered for appropriate workloads
- [ ] Auto-scaling configured to match demand
- [ ] Unused resources identified and eliminated
- [ ] Cost monitoring and alerting configured (budgets, anomaly detection)
- [ ] FinOps practices established for ongoing optimization
- [ ] Licensing optimization analyzed (Hybrid Benefit, dev/test pricing)
- [ ] Showback/chargeback model defined for cost allocation

**Operational Excellence Assessment**
- [ ] Infrastructure as Code (IaC) implemented (ARM, Bicep, Terraform)
- [ ] CI/CD pipelines automated (Azure DevOps, GitHub Actions)
- [ ] Monitoring strategy comprehensive (Azure Monitor, Application Insights)
- [ ] Logging centralized and retained per compliance requirements
- [ ] Runbooks documented for common operational tasks
- [ ] Deployment rings/stages defined for safe rollout
- [ ] Configuration management strategy defined
- [ ] Change management process integrated
- [ ] Performance baselines established
- [ ] Operational reviews scheduled and tracked

**Performance Efficiency Assessment**
- [ ] Performance requirements quantified (response time, throughput, concurrency)
- [ ] Load testing completed with expected peak loads
- [ ] Bottlenecks identified and mitigated
- [ ] Caching strategy implemented (Redis, CDN, Application Gateway)
- [ ] Database optimization applied (indexing, partitioning, read replicas)
- [ ] Compute sizing appropriate for workload characteristics
- [ ] Network latency minimized (proximity placement, ExpressRoute)
- [ ] Asynchronous processing patterns used where appropriate
- [ ] Content delivery optimized (CDN, compression, minification)
- [ ] Performance monitoring and continuous tuning planned

**Architecture Decision Records (ADRs)**
- [ ] All significant architecture decisions documented
- [ ] Decision context, options considered, and rationale captured
- [ ] Trade-offs and consequences articulated
- [ ] ADRs reviewed and approved by architecture board
- [ ] ADRs accessible to project team and stakeholders

### Design Review Checklist

**Security Design Review**
- [ ] Authentication mechanism appropriate (OAuth 2.0, SAML, certificate-based)
- [ ] Authorization model aligns with least privilege principle
- [ ] Sensitive data classified and protected appropriately
- [ ] API security implemented (API Management, rate limiting, throttling)
- [ ] Secrets management solution configured (Key Vault)
- [ ] Input validation and sanitization implemented
- [ ] Cross-site scripting (XSS) and injection attack prevention
- [ ] Security headers configured (HSTS, CSP, X-Frame-Options)
- [ ] Dependency scanning for vulnerable packages
- [ ] Security testing integrated in CI/CD pipeline

**Scalability Design Review**
- [ ] Horizontal scaling strategy defined
- [ ] Stateless application design where possible
- [ ] Database scalability approach validated (sharding, read replicas, Cosmos DB)
- [ ] Asynchronous processing patterns implemented (queues, event grid)
- [ ] Rate limiting and throttling configured
- [ ] CDN and caching layers appropriately utilized
- [ ] Microservices boundaries well-defined (if applicable)
- [ ] Load balancing configured correctly
- [ ] Session management in distributed environment
- [ ] Data consistency approach defined (eventual vs strong)

**Maintainability Design Review**
- [ ] Code structure modular and organized
- [ ] Naming conventions consistent and meaningful
- [ ] Comments and documentation adequate
- [ ] Technical debt identified and tracked
- [ ] Design patterns appropriately applied
- [ ] Dependency injection and loose coupling utilized
- [ ] Configuration externalized from code
- [ ] Logging levels and messages informative
- [ ] Error handling comprehensive
- [ ] Unit tests provide adequate coverage

**Integration Design Review**
- [ ] Integration patterns appropriate (synchronous vs asynchronous)
- [ ] API versioning strategy defined
- [ ] Error handling and retry logic implemented
- [ ] Idempotency ensured for critical operations
- [ ] Message schemas documented
- [ ] Integration testing approach defined
- [ ] Dependency management across systems
- [ ] Data transformation logic validated
- [ ] Integration monitoring and alerting configured
- [ ] Partner SLAs and dependencies documented

### Code Review Standards (If Applicable)

**Code Quality**
- [ ] Code follows language-specific style guides (C#, JavaScript, Python)
- [ ] No code smells (duplicated code, long methods, large classes)
- [ ] SOLID principles applied in object-oriented code
- [ ] Functions/methods have single responsibility
- [ ] Magic numbers replaced with named constants
- [ ] Code complexity within acceptable limits (cyclomatic complexity <10)
- [ ] Commented code removed (use version control history instead)
- [ ] TODO comments tracked in backlog items

**Testing**
- [ ] Unit tests cover critical business logic (minimum 80% coverage)
- [ ] Test names clearly describe scenarios
- [ ] Tests are independent and can run in any order
- [ ] Mock objects used appropriately
- [ ] Edge cases and error conditions tested
- [ ] Integration tests validate end-to-end scenarios
- [ ] Performance tests baseline critical paths
- [ ] Test data managed appropriately (not production data)

**Security**
- [ ] No hardcoded credentials or secrets
- [ ] SQL injection prevention (parameterized queries, ORM)
- [ ] XSS prevention (output encoding, CSP)
- [ ] CSRF protection implemented
- [ ] File upload validation and sanitization
- [ ] Authentication and authorization enforced
- [ ] Sensitive data not logged
- [ ] Dependencies up-to-date with security patches

### Documentation Review Checklist

**Technical Documentation**
- [ ] Architecture diagrams accurate and current
- [ ] Component interactions clearly illustrated
- [ ] Data flows documented with security boundaries
- [ ] API documentation complete (endpoints, parameters, responses)
- [ ] Configuration documentation includes all settings
- [ ] Deployment documentation includes prerequisites and steps
- [ ] Troubleshooting guide covers common issues
- [ ] Glossary defines technical terms and acronyms

**User Documentation**
- [ ] User guides appropriate for target audience skill level
- [ ] Screenshots and visuals enhance understanding
- [ ] Step-by-step instructions clear and concise
- [ ] Common tasks and workflows documented
- [ ] FAQs address anticipated questions
- [ ] Navigation instructions for complex interfaces
- [ ] Video tutorials for complex processes (if applicable)
- [ ] Accessibility considerations documented

**Administrator Documentation**
- [ ] Installation and configuration guides complete
- [ ] Security hardening procedures documented
- [ ] Backup and restore procedures tested and documented
- [ ] Monitoring and alerting configuration documented
- [ ] Incident response runbooks available
- [ ] Performance tuning guidelines provided
- [ ] Capacity planning guidance included
- [ ] Update and patching procedures documented

### Deliverable Quality Checklist

**Presentation Materials**
- [ ] Executive summary on first slide with key messages
- [ ] Slide titles are assertions, not topics
- [ ] Visuals support narrative (not decorative)
- [ ] Data visualizations accurately represent data
- [ ] Consistent formatting (fonts, colors, layout)
- [ ] No spelling or grammatical errors
- [ ] Slide count appropriate for time allocated
- [ ] Appendix includes supporting detail
- [ ] Branded appropriately (if client-facing)
- [ ] Accessible to screen readers and color-blind viewers

**Written Reports**
- [ ] Executive summary provides standalone overview
- [ ] Table of contents includes page numbers
- [ ] Headings use consistent hierarchy
- [ ] Tables and figures numbered and captioned
- [ ] Cross-references accurate and functional
- [ ] Citations and references complete
- [ ] Consistent terminology throughout
- [ ] Page numbers on all pages
- [ ] Headers/footers include document control information
- [ ] Appendices organized logically

**Excel Workbooks**
- [ ] Worksheets named descriptively
- [ ] Input cells clearly distinguished from calculations
- [ ] Formulas use cell references, not hardcoded values
- [ ] Complex formulas include comments explaining logic
- [ ] Data validation applied to input cells
- [ ] Conditional formatting enhances readability
- [ ] Charts have descriptive titles and axis labels
- [ ] Print settings configured appropriately
- [ ] Workbook protected where appropriate
- [ ] Macro-enabled workbooks only when necessary

## Content Standards

### Document Formatting and Structure

**Hierarchy and Organization**
- Level 1 Heading: Document title or major section (24pt bold)
- Level 2 Heading: Primary sections (18pt bold)
- Level 3 Heading: Subsections (14pt bold)
- Level 4 Heading: Minor subsections (12pt bold italic)
- Body text: 11-12pt regular
- Maximum heading depth: 4 levels for readability

**Typography**
- Font family: Calibri, Segoe UI, or Arial for body text
- Monospace font: Consolas or Courier New for code samples
- Line spacing: 1.15-1.5 for body text
- Paragraph spacing: 6-12pt after paragraphs
- Margins: 1 inch all sides (or 0.75 inch for dense content)

**Lists and Tables**
- Bullet lists for unordered items (use consistent bullet style)
- Numbered lists for sequential steps or priorities
- Tables include headers with bold formatting
- Alternate row shading for readability (10% gray)
- Table borders: minimal (header border and bottom border only)
- Tables fit within page width without horizontal scrolling

### Writing Style and Tone

**Clarity Principles**
- Use active voice: "The architect designs..." not "The design is done by..."
- Write concisely: eliminate unnecessary words
- Use simple language: prefer "use" over "utilize"
- Define acronyms on first use: Azure Active Directory (Azure AD)
- Avoid jargon unless audience-appropriate

**Professional Tone**
- Objective and factual, not promotional
- Confident but not arrogant: "This approach provides..." not "This is the only way..."
- Inclusive language: avoid "he/she", use "they" or rewrite
- Positive framing: "Opportunities for improvement" vs "Problems"
- Respectful of alternatives: acknowledge trade-offs

**Actionable Content**
- Recommendations clear and specific
- Next steps explicitly stated
- Responsibilities assigned
- Timelines included where relevant
- Success criteria defined

### Visual Standards

**Diagram Standards**
- Use Microsoft official icons (Azure Architecture Icons, Microsoft 365 Icons)
- Consistent color scheme across all diagrams
- Azure services: blue shades
- Microsoft 365: orange/red shades
- Third-party: gray shades
- Data flows: arrows with labels
- Security boundaries: red dashed lines
- Network boundaries: blue dashed lines
- Labels readable at 100% zoom
- Legend included when symbols need explanation

**Chart Standards**
- Chart titles descriptive and informative
- Axes labeled with units
- Legends positioned consistently (right or bottom)
- Color palette accessible (color-blind safe)
- Data labels on bars/columns when space permits
- Gridlines minimal (major only, light gray)
- 3D effects avoided (distort perception)
- Source attribution when data from external source

**Screenshot Standards**
- Crop to relevant area (exclude unnecessary UI)
- Highlight important elements (red box or arrow)
- Resolution sufficient for readability (minimum 1280px width)
- Annotations use consistent color (red for actions, yellow for information)
- Sequential screenshots numbered (Step 1, Step 2...)
- Sensitive information redacted

### Branding Compliance

**Microsoft Branding (If Applicable)**
- Use Microsoft logo per brand guidelines
- Color palette: Microsoft Blue (#0078D4), Microsoft Gray (#505050)
- Respect trademark usage (Azure®, Microsoft 365®)
- Partner logo placement per co-branding guidelines

**Document Metadata**
- Author information complete
- Creation date and version number
- Document classification (Public, Internal, Confidential)
- Copyright notice if applicable
- Change log for version tracking

### Version Control and Change Tracking

**File Naming Conventions**
- Format: `[Project]_[DocumentType]_v[Major].[Minor]_[YYYYMMDD].ext`
- Example: `ContosoRetail_Architecture_v1.2_20250109.docx`
- Avoid special characters except underscore and hyphen
- Use consistent capitalization

**Version Numbering**
- Major version (1.0, 2.0): Significant changes, requires review
- Minor version (1.1, 1.2): Updates and refinements
- Version 0.x indicates draft status
- Version 1.0 indicates first approved release

**Change Tracking**
- Change log table includes: Date, Version, Author, Description
- Track changes feature used during review cycles
- Final versions have all changes accepted
- Comments addressed or resolved before approval

## Technical Accuracy

### Architecture Pattern Validation

**Reference Architectures**
- Compare design against Azure Architecture Center patterns
- Validate against industry standard patterns (CQRS, Event Sourcing, Microservices)
- Ensure appropriate pattern selection for requirements
- Document deviations from standard patterns with rationale
- Cross-reference Microsoft documentation for recommended approaches

**Anti-Pattern Detection**
- Identify and eliminate known anti-patterns
- Database as integration pattern (avoid tight coupling)
- God objects or classes (violates single responsibility)
- Tight coupling between components
- Hard-coded configuration values
- Ignoring cloud-native capabilities (not leveraging PaaS)

### Microsoft Technology Verification

**Version Accuracy**
- Verify current versions of all Microsoft products referenced
- Check end-of-support dates for products (don't recommend EOL products)
- Validate licensing requirements are current
- Confirm feature availability in specified tiers/SKUs
- Reference official Microsoft documentation URLs

**Feature Validation**
- Test features mentioned in documentation
- Verify feature availability in target regions
- Confirm preview vs GA status
- Validate prerequisites and dependencies
- Check compliance certifications for services used

### Performance and Scalability Validation

**Performance Metrics**
- Response time targets achievable and tested
- Throughput requirements validated with load testing
- Concurrency levels proven in test environment
- Network latency measured and within acceptable range
- Database query performance optimized

**Scalability Verification**
- Horizontal scaling tested to target levels
- Auto-scaling configurations validated
- Resource limits understood (quota, throttling)
- Bottlenecks identified and mitigation plans documented
- Cost implications of scaling calculated

### Security Best Practice Compliance

**Security Controls Verification**
- All OWASP Top 10 vulnerabilities addressed
- Zero Trust principles applied across architecture
- Least privilege access implemented
- Defense in depth layered security
- Encryption in transit and at rest
- Security monitoring and alerting configured
- Incident response procedures documented
- Compliance frameworks mapped (ISO 27001, SOC 2, HIPAA)

### Cost Optimization Verification

**Cost Estimation Accuracy**
- Azure Pricing Calculator used for estimates
- All services included in cost model
- Regional pricing differences accounted for
- Licensing costs included (not just consumption)
- Support costs factored in
- Contingency buffer appropriate (typically 10-20%)

**Cost Optimization Opportunities**
- Reserved instances evaluated for predictable workloads
- Right-sizing analysis completed
- Auto-shutdown policies for non-production
- Storage tiering optimized
- Network egress costs minimized
- Monitoring and unused resource cleanup automated

### Reference URL Accuracy

**Link Validation**
- All URLs tested and accessible
- Links point to current content (not deprecated pages)
- Deep links functional (not broken by site reorganization)
- Prefer learn.microsoft.com over older docs.microsoft.com
- Include access date for time-sensitive content
- Use short links or hyperlinked text (not raw URLs in body text)

## Business Alignment

### Business Case Validation

**ROI Calculation Accuracy**
- All cost components included (licensing, implementation, training, ongoing)
- Benefit quantification realistic and defensible
- Timeframe appropriate (typically 3-5 years)
- Discount rate applied per finance team guidance
- Sensitivity analysis shows range of outcomes
- Payback period calculated
- Net present value (NPV) positive

**Assumptions Documentation**
- All assumptions explicitly stated
- Assumptions validated with stakeholders
- Dependencies on other initiatives identified
- External factors considered (market conditions, regulatory)

### Risk Assessment Completeness

**Risk Identification**
- Technical risks comprehensively identified
- Business risks considered (adoption, change management)
- Organizational risks assessed (skills, resources)
- External risks evaluated (vendor, regulatory)
- Risk register includes likelihood and impact ratings
- Risks prioritized by severity (Likelihood × Impact)

**Mitigation Strategies**
- Each high and critical risk has mitigation plan
- Contingency plans for top risks documented
- Risk owners assigned
- Risk monitoring approach defined
- Residual risk after mitigation assessed

### Stakeholder Alignment Verification

**Stakeholder Engagement**
- All key stakeholders identified and engaged
- Stakeholder concerns addressed in documentation
- Trade-off decisions socialized and approved
- Regular status communication maintained
- Feedback incorporated into deliverables

**Sign-off Process**
- Approvers clearly identified
- Approval criteria documented
- Sign-off obtained before phase gates
- Approvals documented and archived
- Change control process for post-approval changes

### Value Realization Planning

**KPI Definition**
- Key performance indicators specific and measurable
- Baseline metrics established
- Target values realistic and time-bound
- Measurement methodology defined
- Accountability for tracking assigned

**Benefits Tracking**
- Benefits realization timeline created
- Quick wins identified and prioritized
- Long-term value drivers mapped
- Measurement cadence established (monthly, quarterly)
- Course correction triggers defined

## Document Quality

### Executive Readability

**Executive Summary Standards**
- Length: 1-2 pages maximum
- Front-loaded: key message in first paragraph
- Structured: Problem → Solution → Value → Next Steps
- Quantified: Specific numbers, percentages, timelines
- Standalone: Can be read without full document
- Visual: Include 1-2 key graphics if helpful

**Clarity for Non-Technical Audiences**
- Technical jargon minimized or explained
- Analogies used to explain complex concepts
- Focus on business outcomes, not technical features
- Implications and consequences clearly stated
- Risks and mitigation strategies understandable

### Technical Depth Appropriate to Audience

**Audience-Specific Content**
- Executive audience: Strategic, high-level, ROI-focused
- Business audience: Functional capabilities, user experience, change impact
- Technical audience: Architecture details, implementation approach, integration
- Use appendices for detailed technical content
- Layered information: summary → detail approach

### Actionable Recommendations

**Recommendation Quality**
- Specific: Exactly what should be done
- Measurable: How success will be evaluated
- Achievable: Within organization's capabilities
- Relevant: Aligned with business objectives
- Time-bound: When it should be completed
- Prioritized: Critical, high, medium, low

**Decision Support**
- Options presented with pros/cons
- Trade-offs explicitly articulated
- Criteria for decision-making provided
- Recommended option clearly identified with rationale

### Clear Next Steps

**Action Plan Elements**
- Tasks listed in priority or dependency order
- Owners assigned to each action
- Timelines realistic and achievable
- Dependencies noted
- Success criteria defined
- Review/checkpoint dates scheduled

### Complete Artifact Delivery

**Deliverable Checklist**
- All committed deliverables completed
- File formats appropriate for consumption (PDF for distribution, DOCX/PPTX/XLSX for editing)
- Files named per convention
- Files stored in agreed location (/mnt/user-data/outputs/)
- Access permissions configured correctly
- Delivery notification sent to stakeholders
- Handoff meeting scheduled if appropriate

## Skills Implementation Validation

### Skills-First Approach Verification

This section ensures enterprise architects leverage Claude Code skills for document creation, following the skills-first principle.

**Mandatory Skills Usage**
- [ ] PowerPoint presentations created using `pptx` skill, NOT manual tool calls
- [ ] Word documents created using `docx` skill, NOT manual tool calls
- [ ] Excel workbooks created using `xlsx` skill, NOT manual tool calls
- [ ] PDF generation using `pdf` skill when conversion needed
- [ ] Skills invoked properly (e.g., `command: "pptx"` via Skill tool)

**Skills Invocation Checklist**
- [ ] Skill invoked before attempting manual file creation
- [ ] Skill parameters passed correctly per skill documentation
- [ ] Skill output validated before proceeding
- [ ] Multiple skills coordinated when deliverable requires multiple file types
- [ ] Error handling implemented if skill invocation fails

### Template Compliance Checked

**Template Validation**
- [ ] Correct template selected for deliverable type (SAM phase, document type)
- [ ] Template structure preserved (sections, formatting, placeholders)
- [ ] All template sections completed (no "TBD" or "[Content Here]" placeholders)
- [ ] Custom sections added where needed with justification
- [ ] Template version current (check `/references/templates/` for latest)

**Template Customization**
- [ ] Branding updated per client requirements
- [ ] Metadata updated (date, version, author, project)
- [ ] Headers/footers customized appropriately
- [ ] Table of contents updated if structure changed
- [ ] Change log updated with customization notes

### Output Quality Standards Met

**File Quality Verification**
- [ ] Files open correctly in target applications (Microsoft Office, Adobe Reader)
- [ ] No corruption or rendering errors
- [ ] Fonts embedded or standard (Calibri, Arial)
- [ ] Images display correctly (not broken links)
- [ ] Hyperlinks functional
- [ ] File size reasonable (<20MB for typical documents)
- [ ] Accessibility features enabled (alt text, heading structure)

**Content Quality Verification**
- [ ] All content accurate and validated
- [ ] Spelling and grammar checked
- [ ] Formatting consistent throughout
- [ ] Charts and diagrams render clearly
- [ ] Tables format correctly across pages
- [ ] No track changes or comments in final version
- [ ] Metadata sanitized (author, company info appropriate)

### File Locations Correct

**Output Directory Standards**
- [ ] All client deliverables saved to `/mnt/user-data/outputs/`
- [ ] Subdirectories organized by project and phase
- [ ] Internal working files in appropriate skill directories
- [ ] Naming convention followed: `[Project]_[Type]_v[Version]_[Date]`
- [ ] No duplicate or conflicting file names

**Directory Structure Example**
```
/mnt/user-data/outputs/
├── ContosoRetail/
│   ├── Phase1_Vision/
│   │   ├── ContosoRetail_VisionPresentation_v1.0_20250109.pptx
│   │   ├── ContosoRetail_BusinessCase_v1.0_20250109.xlsx
│   │   └── ContosoRetail_VisionDocument_v1.0_20250109.pdf
│   ├── Phase2_Validate/
│   │   ├── ContosoRetail_ArchitectureDesign_v1.2_20250115.docx
│   │   └── ContosoRetail_TechnicalSpecs_v1.1_20250115.pdf
```

### User Access Links Provided

**Link Generation**
- [ ] Direct links to output files provided in final response
- [ ] Links tested and accessible
- [ ] Links formatted as `/mnt/user-data/outputs/[path/to/file]`
- [ ] File description included with each link
- [ ] Instructions for accessing files provided if needed

**Delivery Confirmation Template**
```markdown
## Deliverables Created

The following files have been created and are ready for review:

1. **Vision Presentation**: `/mnt/user-data/outputs/ContosoRetail/Phase1_Vision/ContosoRetail_VisionPresentation_v1.0_20250109.pptx`
   - 25-slide executive presentation covering problem statement, solution approach, and business case

2. **Business Case Workbook**: `/mnt/user-data/outputs/ContosoRetail/Phase1_Vision/ContosoRetail_BusinessCase_v1.0_20250109.xlsx`
   - ROI analysis, cost-benefit model, and implementation timeline

3. **Vision Document (PDF)**: `/mnt/user-data/outputs/ContosoRetail/Phase1_Vision/ContosoRetail_VisionDocument_v1.0_20250109.pdf`
   - Comprehensive vision document suitable for distribution to stakeholders
```

## Quality Assessment Scoring Rubrics

### Architecture Quality Rubric

Each criterion scored 1-5:
- **5 - Exceptional**: Exceeds standards, industry-leading approach
- **4 - Strong**: Meets all standards, best practices applied
- **3 - Adequate**: Meets minimum standards, some improvements possible
- **2 - Needs Improvement**: Below standards, significant gaps
- **1 - Unacceptable**: Does not meet standards, requires rework

**Scoring Criteria**
- Well-Architected Framework alignment (20%)
- Security best practices (20%)
- Scalability and performance (15%)
- Cost optimization (15%)
- Operational excellence (15%)
- Documentation quality (15%)

**Minimum Passing Score**: 3.5 average across all criteria

### Document Quality Rubric

**Content Quality (40%)**
- Accuracy and technical correctness
- Completeness of information
- Relevance to audience
- Logical flow and organization

**Presentation Quality (30%)**
- Professional formatting
- Visual effectiveness
- Readability and clarity
- Brand compliance

**Actionability (30%)**
- Clear recommendations
- Specific next steps
- Measurable outcomes
- Stakeholder alignment

**Minimum Passing Score**: 4.0 average (Strong)

## Defect Severity Classifications

### Critical (P1)
- **Impact**: Blocks progress, major inaccuracy, security vulnerability
- **Examples**: Incorrect architecture violates security policy, cost estimate off by >50%, missing mandatory sections
- **SLA**: Remediate within 24 hours
- **Escalation**: Immediate notification to engagement lead

### High (P2)
- **Impact**: Significant issue, workaround available
- **Examples**: Broken references, missing ADR for key decision, incomplete test coverage
- **SLA**: Remediate within 3 business days
- **Escalation**: Notify engagement lead within 24 hours

### Medium (P3)
- **Impact**: Moderate issue, doesn't block progress
- **Examples**: Formatting inconsistency, minor technical inaccuracy, missing non-critical documentation
- **SLA**: Remediate within 1 week
- **Escalation**: Track in backlog, address before phase gate

### Low (P4)
- **Impact**: Minor issue, cosmetic or enhancement
- **Examples**: Typos, style guide deviations, suggestions for improvement
- **SLA**: Remediate as capacity allows
- **Escalation**: Track in backlog, address opportunistically

## Remediation Workflows

### Defect Remediation Process

1. **Detection**: Reviewer identifies defect during quality review
2. **Classification**: Assign severity (P1-P4) and category
3. **Assignment**: Route to responsible team member
4. **Remediation**: Fix defect and update documentation
5. **Verification**: Reviewer validates fix
6. **Closure**: Mark defect as resolved in tracking system

### Review Feedback Loop

**Review Cycle**
1. Author submits deliverable for review
2. Reviewer conducts assessment within 2 business days
3. Feedback provided with specific, actionable comments
4. Author remediates issues
5. Revised deliverable re-submitted
6. Reviewer verifies remediation
7. Deliverable approved or cycle repeats (maximum 3 iterations)

**Escalation Path**
- Iteration 3+: Escalate to technical lead for guidance
- Repeated quality issues: Additional training or support
- Systemic problems: Process improvement review

## Continuous Improvement Processes

### Lessons Learned Capture

**Post-Engagement Retrospective**
- Conduct within 2 weeks of engagement completion
- Include all team members
- Structured format: What went well, what didn't, what to change
- Document in lessons learned repository
- Share insights with broader team

**Continuous Improvement Actions**
- Identify top 3 improvement opportunities
- Assign owners and target completion dates
- Track progress in monthly quality reviews
- Update standards and templates based on learnings
- Celebrate improvements and share successes

### Quality Metrics Tracking

**Key Quality Indicators**
- Defect density (defects per deliverable)
- Rework rate (percentage requiring revision)
- Review cycle time (time from submission to approval)
- Customer satisfaction scores
- On-time delivery percentage

**Monthly Quality Dashboard**
- Track trends over time
- Identify improvement opportunities
- Recognize high-quality work
- Address systemic issues
- Report to leadership

## Conclusion

These quality standards ensure that all enterprise architecture deliverables meet the high bar expected by clients and stakeholders. Consistent application of these standards, combined with continuous improvement based on feedback and lessons learned, drives excellence in enterprise architecture practice. All architects must internalize these standards and apply them rigorously to every engagement.
