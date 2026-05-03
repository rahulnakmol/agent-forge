---
category: methodology
loading_priority: 2
tokens_estimate: 3400
keywords:
  - process decomposition
  - L1 L2 L3 L4
  - value chain
  - process hierarchy
  - MECE
  - process taxonomy
  - Record to Report
  - Order to Cash
  - Hire to Retire
  - Procure to Pay
  - process ownership
  - automation potential
  - activity task
version: "1.0"
last_updated: "2026-03-23"
---

# Process Decomposition Methodology

The L1 to L4 process decomposition is the backbone of the Target Operating Model. It provides a structured, hierarchical breakdown of all business processes from strategic value chains down to individual tasks.

---

## The Four Levels

### L1 — Value Chain / End-to-End Process

The highest level of process abstraction. L1 processes represent complete value chains that span multiple functional areas and deliver a defined business outcome.

**Characteristics**:
- Cross-functional (spans multiple departments)
- Outcome-oriented (named as "verb-to-verb" or "trigger-to-outcome")
- Typically 5–12 L1 processes per domain
- Owned by a Global Process Owner (GPO)
- Stable over time — rarely changes unless strategy changes

**Naming convention**: `[Trigger] to [Outcome]` — e.g., "Record to Report", "Order to Cash", "Hire to Retire"

### L2 — Major Process Area

The decomposition of an L1 process into its major functional components. L2 processes represent distinct process areas that can be independently managed and measured.

**Characteristics**:
- Functional grouping within the value chain
- Typically 3–8 L2 processes per L1
- Each L2 has a clear process area owner
- Maturity is assessed at the L2 level
- Service delivery decisions are made at L2 (insource/outsource)

**Naming convention**: Noun-based — e.g., "General Ledger", "Accounts Payable", "Fixed Assets"

### L3 — Process

The decomposition of an L2 area into specific, executable processes. L3 is the primary design level — where process flows are documented, roles are assigned, and KPIs are defined.

**Characteristics**:
- Specific, measurable, and documentable
- Typically 3–10 L3 processes per L2
- Each L3 has a defined process flow (swimlane diagram)
- KPIs and SLAs are defined at L3
- Controls and compliance requirements map to L3

**Naming convention**: Verb + noun phrase — e.g., "Journal Entry Processing", "Period Close", "Invoice Matching"

### L4 — Activity / Task

The most granular level — individual steps within a process. L4 activities are the building blocks used for automation assessment, effort estimation, and detailed design.

**Characteristics**:
- Discrete, actionable steps
- Typically 3–15 L4 activities per L3
- Each L4 is assigned to a specific role
- Automation potential is assessed at L4
- System transactions map to L4 (e.g., specific D365 transactions)

**Naming convention**: Verb + object — e.g., "Post journal entry", "Review and approve", "Run validation report"

---

## Decomposition Rules

### Rule 1: MECE (Mutually Exclusive, Collectively Exhaustive)

At each level, the child processes must:
- **Not overlap** (mutually exclusive) — no activity belongs to two processes
- **Cover everything** (collectively exhaustive) — no gaps in coverage

Test: If you remove a child process, is there work that is no longer accounted for? If yes, the decomposition is not exhaustive. If two children seem to cover the same work, the decomposition is not exclusive.

### Rule 2: Ownership Clarity

Every process at every level must have a single, clearly identified owner:
- L1: Global Process Owner (GPO)
- L2: Process Area Owner
- L3: Process Owner
- L4: Role assignment (who performs the task)

### Rule 3: Measurability at L3

Every L3 process must be measurable with at least one KPI. If a process cannot be measured, it is either too granular (should be L4) or too vague (needs further decomposition).

### Rule 4: Automation Potential at L4

Every L4 activity must be assessed for automation potential using this classification:

| Classification | Description | Technology |
|---------------|-------------|------------|
| **Manual** | Requires human judgment, no automation possible | N/A |
| **Assisted** | Human performs with system assistance | D365 workflows, guided tasks |
| **Semi-automated** | System performs with human review/approval | Power Automate + approval flows |
| **Fully automated** | System performs without human intervention | RPA, scheduled jobs, AI agents |
| **AI-augmented** | AI performs with human oversight | Copilot, custom AI agents |

### Rule 5: Consistent Granularity

Within the same parent, all children should be at approximately the same level of granularity. Avoid mixing a 5-minute task with a 2-day process at the same level.

---

## Cross-Domain L1 Process Examples

### Finance

| L1 Process | Description | Key L2 Areas |
|-----------|-------------|-------------|
| Record to Report (R2R) | Financial recording through reporting | General Ledger, Fixed Assets, Intercompany, Close & Consolidation, Financial Reporting |
| Order to Cash (O2C) | Customer order through cash collection | Customer Master, Sales Order, Billing, Accounts Receivable, Credit Management, Collections |
| Procure to Pay (P2P) | Requisition through vendor payment | Purchase Requisition, Purchase Order, Goods Receipt, Invoice Processing, Payment Processing |
| Treasury & Cash Management | Cash positioning through investment | Cash Positioning, Bank Reconciliation, Cash Forecasting, Investments, Debt Management |
| Tax Management | Tax calculation through compliance | Tax Determination, Tax Reporting, Transfer Pricing, Tax Audit, Indirect Tax |
| Financial Planning & Analysis | Budgeting through forecasting | Budgeting, Forecasting, Variance Analysis, Management Reporting, Cost Allocation |

### HR

| L1 Process | Description | Key L2 Areas |
|-----------|-------------|-------------|
| Hire to Retire (H2R) | Recruitment through separation | Recruitment, Onboarding, Employee Records, Offboarding, Alumni Management |
| Talent to Performance (T2P) | Goal setting through performance review | Goal Management, Performance Reviews, 360 Feedback, Talent Calibration, Succession Planning |
| Learn to Grow (L2G) | Training needs through career development | Training Needs Analysis, Learning Design, Learning Delivery, Certification, Career Pathing |
| Compensate to Reward (C2R) | Compensation design through payroll | Compensation Design, Benefits Administration, Payroll Processing, Incentive Management |
| Plan to Workforce (P2W) | Workforce planning through deployment | Workforce Planning, Position Management, Org Design, Contingent Labor, Mobility |

### Procurement

| L1 Process | Description | Key L2 Areas |
|-----------|-------------|-------------|
| Source to Contract (S2C) | Category strategy through contract execution | Category Management, Supplier Sourcing, RFx Management, Contract Negotiation, Contract Management |
| Procure to Pay (P2P) | Requisition through payment | Requisition, Sourcing, Purchase Order, Goods Receipt, Invoice Processing, Payment |
| Supplier Management | Onboarding through performance | Supplier Onboarding, Supplier Master, Supplier Performance, Supplier Risk, Supplier Development |
| Procurement Analytics | Spend analysis through optimization | Spend Analysis, Savings Tracking, Compliance Monitoring, Market Intelligence |

### Supply Chain Management (SCM)

| L1 Process | Description | Key L2 Areas |
|-----------|-------------|-------------|
| Plan to Produce (P2P) | Demand planning through production | Demand Planning, Supply Planning, Production Planning, MRP, Capacity Planning |
| Order to Deliver (O2D) | Order receipt through delivery | Order Management, Inventory Management, Warehouse Operations, Transportation, Last Mile |
| Design to Operate (D2O) | Product design through lifecycle | Product Design, BOM Management, Engineering Change, PLM, Quality Management |
| Return to Resolve (R2R) | Return initiation through resolution | Return Authorization, Inspection, Disposition, Refund/Replacement, Root Cause Analysis |

### Cyber Security

| L1 Process | Description | Key L2 Areas |
|-----------|-------------|-------------|
| Identify | Asset and risk identification | Asset Management, Risk Assessment, Threat Intelligence, Vulnerability Management |
| Protect | Preventive security controls | Access Control, Data Security, Network Security, Endpoint Protection, Security Awareness |
| Detect | Threat detection and monitoring | Security Monitoring, Anomaly Detection, Event Correlation, Threat Hunting |
| Respond | Incident response and containment | Incident Response, Forensics, Communication, Containment, Eradication |
| Recover | Recovery and lessons learned | Recovery Planning, Business Continuity, Restoration, Lessons Learned, Improvement |

### Sustainability

| L1 Process | Description | Key L2 Areas |
|-----------|-------------|-------------|
| Measure | Data collection and carbon accounting | Scope 1/2/3 Data Collection, Carbon Accounting, Environmental Metrics, Social Metrics |
| Report | Regulatory and voluntary reporting | CSRD Reporting, GRI Reporting, CDP Disclosure, Internal Reporting, Assurance |
| Reduce | Emission and waste reduction | Energy Efficiency, Waste Reduction, Supply Chain Decarbonization, Circular Economy |
| Offset | Carbon offset and credit management | Offset Strategy, Credit Procurement, Registry Management, Verification |
| Govern | ESG governance and compliance | ESG Governance, Materiality Assessment, Stakeholder Engagement, Policy Management |

---

## Decomposition Example: Finance — Record to Report

```
L1: Record to Report
├── L2: General Ledger
│   ├── L3: Journal Entry Processing
│   │   ├── L4: Create journal entry
│   │   ├── L4: Validate journal entry (automated)
│   │   ├── L4: Review and approve journal entry
│   │   ├── L4: Post journal entry
│   │   └── L4: Run posting validation report
│   ├── L3: Chart of Accounts Management
│   │   ├── L4: Request new account
│   │   ├── L4: Validate against CoA structure
│   │   ├── L4: Approve new account
│   │   └── L4: Create account in D365
│   └── L3: Intercompany Accounting
│       ├── L4: Generate intercompany transactions
│       ├── L4: Match intercompany balances
│       ├── L4: Investigate and resolve differences
│       └── L4: Post intercompany eliminations
├── L2: Fixed Assets
│   ├── L3: Asset Acquisition
│   ├── L3: Asset Depreciation
│   ├── L3: Asset Transfer & Disposal
│   └── L3: Asset Revaluation
├── L2: Close & Consolidation
│   ├── L3: Period Close
│   ├── L3: Currency Revaluation
│   ├── L3: Consolidation
│   └── L3: Financial Statement Preparation
└── L2: Financial Reporting
    ├── L3: Management Reporting
    ├── L3: Statutory Reporting
    └── L3: Regulatory Reporting
```

---

## Practical Guidelines

1. **Start with L1/L2 from the reference taxonomy** — do not reinvent; customize from the domain-specific references in `domains/{domain}/1.1-process-taxonomies.md`
2. **Validate L3 with process owners** — the process owner should recognize and agree with the L3 decomposition
3. **Detail L4 only where needed** — full L4 decomposition is required for processes targeted for automation or significant redesign; other processes can remain at L3
4. **Map to systems at L4** — every L4 activity should reference a specific system transaction or manual step
5. **Flag automation candidates** — mark L4 activities with their automation classification to feed into the AI augmentation overlay (Section 4.1)
