---
category: methodology
loading_priority: 2
tokens_estimate: 2800
keywords:
  - maturity model
  - maturity assessment
  - maturity levels
  - gap analysis
  - current state
  - target state
  - process maturity
  - people maturity
  - technology maturity
  - data maturity
  - heatmap
  - scoring methodology
  - continuous improvement
  - AI augmented
version: "1.0"
last_updated: "2026-03-23"
---

# Maturity Framework

A 5-level maturity model for assessing current-state capabilities and defining target-state ambitions across the Target Operating Model.

---

## The 5 Maturity Levels

### Level 1: Initial

**Characteristics**: Ad-hoc, reactive, person-dependent. Processes exist but are informal, undocumented, and inconsistently executed. Outcomes depend on individual heroics rather than organizational capability.

| Dimension | Indicators |
|-----------|-----------|
| **People** | Tribal knowledge, no formal training, key-person dependencies |
| **Process** | Undocumented, inconsistent execution, no standard procedures |
| **Technology** | Spreadsheets, email, manual workarounds, shadow IT |
| **Data** | Siloed, inconsistent definitions, no master data governance |

**Typical state**: Legacy ERP with heavy customization, manual reconciliations, no analytics beyond basic reporting.

### Level 2: Managed

**Characteristics**: Basic processes defined, some standardization. Work is repeatable within teams but not yet consistent across the organization. Management has visibility into operations but limited control.

| Dimension | Indicators |
|-----------|-----------|
| **People** | Defined roles, basic training programs, some cross-training |
| **Process** | Documented procedures, basic workflows, some standardization |
| **Technology** | Core ERP implemented, basic automation (macros, simple workflows) |
| **Data** | Departmental reporting, some shared definitions, basic data quality |

**Typical state**: ERP implemented with standard configuration, basic Power Automate flows, departmental Power BI reports.

### Level 3: Defined

**Characteristics**: Standardized, documented, measured. Processes are consistent across the organization, performance is tracked, and governance is in place. This is the minimum target for most transformation programs.

| Dimension | Indicators |
|-----------|-----------|
| **People** | Competency frameworks, structured training, performance metrics |
| **Process** | End-to-end process ownership (GPOs), SLAs, exception management |
| **Technology** | Integrated platform (D365 + Power Platform), workflow automation |
| **Data** | Enterprise reporting, MDM in place, data stewardship roles defined |

**Typical state**: D365 F&O live with integrated Power Platform, GBS established, enterprise Power BI dashboards, formal change management.

### Level 4: Quantified

**Characteristics**: Data-driven, predictive, automated. Processes are optimized using analytics, automation handles routine work, and decisions are informed by real-time data. Performance is benchmarked against industry peers.

| Dimension | Indicators |
|-----------|-----------|
| **People** | Data-literate workforce, AI-augmented decision-making, self-service analytics |
| **Process** | Automated exception handling, predictive process monitoring, touchless processing |
| **Technology** | AI/ML integrated (Copilot, custom models), advanced RPA, real-time integration |
| **Data** | Predictive analytics, real-time dashboards, data quality automation, Fabric lakehouse |

**Typical state**: D365 with Copilot, advanced Power Automate orchestrations, Fabric-based analytics, 70%+ touchless processing rates.

### Level 5: Optimized

**Characteristics**: Continuous improvement, AI-augmented, autonomous. The organization continuously adapts its operating model using AI-driven insights. Processes self-optimize, exceptions are handled autonomously, and human intervention is reserved for strategic decisions.

| Dimension | Indicators |
|-----------|-----------|
| **People** | Strategic focus, AI collaboration, continuous learning culture |
| **Process** | Self-optimizing workflows, autonomous exception resolution, zero-touch processing |
| **Technology** | Autonomous AI agents, digital twins, self-healing integrations |
| **Data** | Real-time prescriptive analytics, automated data governance, AI-driven data quality |

**Typical state**: Autonomous finance operations, AI agents handling end-to-end processes, digital twins for supply chain, prescriptive analytics driving strategy.

---

## Assessment Dimensions

Every maturity assessment evaluates four dimensions at each process level:

| Dimension | Weight | Assessment Focus |
|-----------|--------|-----------------|
| **People** | 25% | Skills, roles, culture, change readiness |
| **Process** | 30% | Standardization, documentation, efficiency, compliance |
| **Technology** | 25% | Platform capability, automation, integration, AI adoption |
| **Data** | 20% | Quality, governance, analytics maturity, MDM coverage |

Weights can be adjusted based on organizational priorities (e.g., a technology-led transformation may weight Technology at 35%).

---

## Scoring Methodology

### Per-Process Scoring

Each L2 process is scored across all four dimensions:

```
Process Score = (People_Score x 0.25) + (Process_Score x 0.30) +
                (Technology_Score x 0.25) + (Data_Score x 0.20)
```

Scores are integers from 1 to 5, corresponding to the maturity levels.

### Domain-Level Aggregation

Domain maturity is the weighted average of all L2 process scores within the domain:

```
Domain Score = SUM(Process_Score_i x Volume_Weight_i) / SUM(Volume_Weight_i)
```

Volume weights reflect the relative business importance and transaction volume of each process.

### Enterprise-Level Aggregation

Enterprise maturity is the weighted average of all domain scores:

```
Enterprise Score = SUM(Domain_Score_j x Strategic_Weight_j) / SUM(Strategic_Weight_j)
```

---

## Gap Analysis Approach

### Step 1: Assess Current State

Conduct workshops with process owners and subject matter experts to score each L2 process across all four dimensions. Use evidence-based scoring: documented processes, system screenshots, KPI reports, audit findings.

### Step 2: Define Target State

Work with leadership to define target maturity levels per L2 process, informed by:
- Strategic objectives ("We want to be best-in-class in Record to Report")
- Industry benchmarks (APQC, Hackett peer comparisons)
- Business case constraints (budget, timeline, change capacity)
- Regulatory requirements (minimum maturity for compliance)

### Step 3: Calculate Gaps

```
Gap = Target_Score - Current_Score
```

Classify gaps:
| Gap Size | Priority | Typical Effort |
|----------|----------|---------------|
| 0 | No gap: maintain | Sustain current performance |
| 1 | Low priority | Incremental improvement, 3–6 months |
| 2 | Medium priority | Significant improvement, 6–12 months |
| 3+ | High priority | Transformational change, 12–24 months |

### Step 4: Prioritize Actions

Use a 2x2 matrix: **Impact** (strategic value of closing the gap) vs **Effort** (cost and complexity):
- High Impact / Low Effort = Quick Wins (do first)
- High Impact / High Effort = Strategic Initiatives (plan carefully)
- Low Impact / Low Effort = Fill-ins (do when convenient)
- Low Impact / High Effort = Deprioritize (do last or not at all)

---

## Maturity Heatmap Visualization

The maturity heatmap is a color-coded matrix showing current and target maturity across all L2 processes and all four dimensions:

```
Rows:    L2 processes (grouped by domain)
Columns: People | Process | Technology | Data | Overall
Colors:  Level 1 = Red | Level 2 = Orange | Level 3 = Yellow | Level 4 = Light Green | Level 5 = Dark Green
Markers: Current state = filled cell | Target state = border/outline
```

This visualization is typically generated as a Power BI dashboard or included in the TOM deck (see `templates/tom-deck-template.md`, Slide 6).

---

## Common Maturity Patterns

| Pattern | Description | Typical Action |
|---------|-------------|---------------|
| **Technology ahead of process** | Systems upgraded but processes unchanged | Focus on process redesign and adoption |
| **Process ahead of technology** | Processes designed but system gaps | Prioritize technology implementation |
| **Data lagging** | Strong processes and tech, poor data | Invest in MDM and data governance |
| **People lagging** | Good systems and processes, low adoption | Focus on change management and training |
| **Uneven across domains** | Finance at Level 4, HR at Level 1 | Balanced investment across domains |
