---
category: templates
loading_priority: 3
tokens_estimate: 3200
keywords:
  - workbook template
  - XLSX
  - Excel
  - capability register
  - maturity assessment
  - KPI tracker
  - technology mapping
  - RACI matrix
  - AI augmentation
  - spreadsheet
  - data validation
  - conditional formatting
version: "1.0"
last_updated: "2026-03-23"
---

# TOM Workbook Template: 6-Sheet XLSX Specification

Standard workbook template for Target Operating Model data capture, analysis, and tracking. This specification defines the structure, columns, data types, validation rules, and conditional formatting for each sheet.

---

## Invocation Pattern

To generate the workbook using the xlsx skill:

```
Use the ms-xlsx skill to create a TOM workbook following the template in
references/templates/tom-workbook-template.md. Domain: {domain}. Scope: {L1 processes in scope}.
```

---

## Sheet 1: Capability Register

**Purpose**: Complete inventory of all processes (L1 through L4) with metadata, ownership, and scope classification.

| Column | Header | Data Type | Validation | Width |
|--------|--------|-----------|------------|-------|
| A | Domain | Text | Dropdown: Finance, HR, Procurement, SCM, Cyber, Sustainability | 15 |
| B | L1 Process | Text | Dropdown per domain (from process taxonomies) | 25 |
| C | L2 Process Area | Text | Dropdown per L1 | 25 |
| D | L3 Process | Text | Free text | 30 |
| E | L4 Activity | Text | Free text | 35 |
| F | Process Owner | Text | Free text | 20 |
| G | In Scope | Text | Dropdown: Yes, No, Partial | 10 |
| H | Automation Classification | Text | Dropdown: Manual, Assisted, Semi-Automated, Fully Automated, AI-Augmented | 18 |
| I | Primary System | Text | Dropdown: D365 F&O, D365 SCM, D365 HR, Power Platform, Azure, Fabric, Third-Party, Manual | 18 |
| J | D365 Module/Transaction | Text | Free text | 25 |
| K | Volume (per month) | Number | Integer >= 0 | 12 |
| L | Avg Processing Time (min) | Number | Decimal >= 0 | 12 |
| M | Notes | Text | Free text | 40 |

**Conditional formatting**:
- Column G: "Yes" = green fill, "No" = red fill, "Partial" = amber fill
- Column H: "Fully Automated" / "AI-Augmented" = green fill, "Manual" = red fill

**Filters**: Enable auto-filter on all columns. Default grouping by L1 → L2 → L3.

---

## Sheet 2: Maturity Assessment

**Purpose**: Current-state and target-state maturity scores per L2 process across all four dimensions.

| Column | Header | Data Type | Validation | Width |
|--------|--------|-----------|------------|-------|
| A | Domain | Text | Dropdown: Finance, HR, Procurement, SCM, Cyber, Sustainability | 15 |
| B | L1 Process | Text | Dropdown per domain | 25 |
| C | L2 Process Area | Text | Dropdown per L1 | 25 |
| D | Current: People | Integer | 1-5 | 12 |
| E | Current: Process | Integer | 1-5 | 12 |
| F | Current: Technology | Integer | 1-5 | 12 |
| G | Current: Data | Integer | 1-5 | 12 |
| H | Current: Overall | Formula | `=D*0.25 + E*0.30 + F*0.25 + G*0.20` | 12 |
| I | Target: People | Integer | 1-5 | 12 |
| J | Target: Process | Integer | 1-5 | 12 |
| K | Target: Technology | Integer | 1-5 | 12 |
| L | Target: Data | Integer | 1-5 | 12 |
| M | Target: Overall | Formula | `=I*0.25 + J*0.30 + K*0.25 + L*0.20` | 12 |
| N | Gap: Overall | Formula | `=M - H` | 10 |
| O | Priority | Text | Dropdown: Quick Win, Strategic, Fill-in, Deprioritize | 15 |
| P | Key Finding | Text | Free text | 40 |

**Conditional formatting**:
- Columns D–G, I–L: Color scale 1=red, 2=orange, 3=yellow, 4=light green, 5=dark green
- Column N (Gap): 0=white, 1=light yellow, 2=orange, 3+=red
- Column O: Quick Win=green, Strategic=blue, Fill-in=gray, Deprioritize=light gray

---

## Sheet 3: KPI Tracker

**Purpose**: KPI definitions, current performance, benchmarks, and targets per L2 process.

| Column | Header | Data Type | Validation | Width |
|--------|--------|-----------|------------|-------|
| A | Domain | Text | Dropdown | 15 |
| B | L1 Process | Text | Dropdown per domain | 25 |
| C | L2 Process Area | Text | Dropdown per L1 | 25 |
| D | KPI Name | Text | Free text | 30 |
| E | KPI Definition | Text | Free text | 40 |
| F | Unit of Measure | Text | Dropdown: %, Days, Count, Currency, Ratio, Hours | 12 |
| G | Measurement Frequency | Text | Dropdown: Daily, Weekly, Monthly, Quarterly, Annual | 12 |
| H | Current Value | Number | Decimal | 12 |
| I | Industry Benchmark (Median) | Number | Decimal | 15 |
| J | Industry Benchmark (Top Quartile) | Number | Decimal | 15 |
| K | Target Value | Number | Decimal | 12 |
| L | KPI Owner | Text | Free text | 20 |
| M | Data Source | Text | Free text | 25 |
| N | Dashboard | Text | Dropdown: Executive, Operational, Both, N/A | 12 |
| O | Status | Text | Dropdown: On Track, At Risk, Off Track, Not Measured | 12 |

**Conditional formatting**:
- Column O: On Track=green, At Risk=amber, Off Track=red, Not Measured=gray
- Column H vs I: If Current Value >= Benchmark Median, green fill on H; else red fill

---

## Sheet 4: Technology Mapping

**Purpose**: Process-to-technology mapping showing which platform supports each L2/L3 process.

| Column | Header | Data Type | Validation | Width |
|--------|--------|-----------|------------|-------|
| A | Domain | Text | Dropdown | 15 |
| B | L2 Process Area | Text | Dropdown | 25 |
| C | L3 Process | Text | Free text | 30 |
| D | Primary Platform | Text | Dropdown: D365 F&O, D365 SCM, D365 HR, D365 CE, Power Apps, Power Automate, Azure, Fabric, M365, Third-Party | 18 |
| E | D365 Module | Text | Free text | 20 |
| F | Specific Feature/Transaction | Text | Free text | 30 |
| G | Integration Required | Text | Dropdown: Yes, No | 10 |
| H | Integration Type | Text | Dropdown: API, Dataverse, Dual-Write, Batch, Event-Based, File, N/A | 15 |
| I | Integration Target | Text | Free text | 25 |
| J | Customization Required | Text | Dropdown: None, Configuration, Extension, ISV, Custom Development | 18 |
| K | Customization Description | Text | Free text | 35 |
| L | Fit Assessment | Text | Dropdown: Full Fit, Partial Fit, Gap, Not Assessed | 15 |
| M | Gap Description | Text | Free text | 35 |

**Conditional formatting**:
- Column L: Full Fit=green, Partial Fit=amber, Gap=red, Not Assessed=gray
- Column J: None/Configuration=green, Extension=yellow, ISV/Custom Development=red

---

## Sheet 5: RACI Matrix

**Purpose**: Responsibility assignment matrix mapping roles to L3 processes.

| Column | Header | Data Type | Validation | Width |
|--------|--------|-----------|------------|-------|
| A | Domain | Text | Dropdown | 15 |
| B | L2 Process Area | Text | Dropdown | 25 |
| C | L3 Process | Text | Free text | 30 |
| D–Z | {Role Names} | Text | Dropdown: R, A, C, I, blank | 5 each |

**Column D onward**: Each column represents a role. Role names are populated in the header row based on the domain's role catalog (from Section 2.2). Typical roles for Finance: CFO, Controller, GL Accountant, AP Clerk, AR Analyst, Tax Manager, Treasury Analyst, Financial Analyst, etc.

**Validation rules**:
- Each row must have exactly one "A" (Accountable)
- Each row must have at least one "R" (Responsible)
- No role should be both "R" and "A" for the same process (SoD check)

**Conditional formatting**:
- R = green fill, A = red fill, C = blue fill, I = light gray fill
- Flag rows with no "A" or no "R" in red border
- Flag cells where same role has both R and A with warning icon

---

## Sheet 6: AI Augmentation

**Purpose**: AI opportunity assessment and roadmap per L3 process.

| Column | Header | Data Type | Validation | Width |
|--------|--------|-----------|------------|-------|
| A | Domain | Text | Dropdown | 15 |
| B | L2 Process Area | Text | Dropdown | 25 |
| C | L3 Process | Text | Free text | 30 |
| D | AI Opportunity | Text | Dropdown: None, Low, Medium, High | 10 |
| E | AI Type | Text | Dropdown: Copilot, Custom Agent, RPA, ML Model, GenAI, Computer Vision, NLP, N/A | 15 |
| F | Microsoft Technology | Text | Dropdown: M365 Copilot, Copilot Studio, Power Automate, Azure AI, Azure ML, AI Builder, Custom, N/A | 18 |
| G | Use Case Description | Text | Free text | 40 |
| H | Current Automation % | Number | 0–100, integer | 12 |
| I | Target Automation % | Number | 0–100, integer | 12 |
| J | Adoption Phase | Text | Dropdown: Assist, Augment, Automate, Autonomous | 12 |
| K | Implementation Wave | Text | Dropdown: Wave 1 (0-6m), Wave 2 (6-12m), Wave 3 (12-18m), Wave 4 (18-24m), Backlog | 15 |
| L | Estimated Effort (days) | Number | Integer >= 0 | 12 |
| M | Estimated Annual Savings | Number | Currency >= 0 | 15 |
| N | Human-in-the-Loop Required | Text | Dropdown: Yes, No | 10 |
| O | Risk Level | Text | Dropdown: Low, Medium, High | 10 |
| P | Notes | Text | Free text | 35 |

**Conditional formatting**:
- Column D: High=green, Medium=yellow, Low=light gray, None=white
- Column J: Assist=light blue, Augment=blue, Automate=dark blue, Autonomous=purple
- Column O: Low=green, Medium=amber, High=red
- Columns H–I: Color scale from red (0%) to green (100%)

---

## Workbook-Level Settings

| Setting | Value |
|---------|-------|
| Default font | Segoe UI, 10pt |
| Header font | Segoe UI Semibold, 11pt |
| Header fill | #1a73e8 (blue), white text |
| Freeze panes | Row 1 (headers) frozen on all sheets |
| Auto-filter | Enabled on all sheets |
| Print area | Fit to 1 page wide, multiple pages long |
| Named ranges | Define named ranges for all dropdown lists |
| Protection | Lock header rows and formula cells; allow data entry in input cells |
