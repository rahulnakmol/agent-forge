---
category: artifacts
loading_priority: 2
tokens_estimate: 1800
keywords:
  - effort estimation
  - story points
  - workbook
  - xlsx
  - MOSCOW
  - fit gap
  - complexity
  - capability
  - sizing
version: "1.0"
last_updated: "2026-03-21"
---

# Effort Estimation Workbook Specification

This document defines the complete specification for the Effort Estimation Excel workbook. The workbook is generated during Phase 2 (Analysis) and provides a story-point-based effort breakdown organized by capability, priority, fit-gap analysis, and complexity.

## Sheet 1: "Effort Detail"

### Column Specifications

#### Column A: Sl No. (width: 8)
- Auto-increment integer starting at 1.
- Number format: integer, no decimals.

#### Column B: Epic/Module/Work stream (width: 35)
- Hierarchical grouping label for the body of work.
- Examples: "Customer Service AI", "Data Migration", "Identity & Access", "Integration Layer", "Reporting & Analytics".
- Used for grouping and subtotals.

#### Column C: RFR Reference (width: 20)
- Requirement ID linking back to the Requirements for Response document.
- Format: `REQ-[XX]-[NNN]` where XX is a two-letter category code and NNN is sequential.
- Category codes: FR (Functional), NF (Non-Functional), IN (Integration), DA (Data), SE (Security).
- Examples: `REQ-FR-001`, `REQ-NF-012`, `REQ-IN-003`.

#### Column D: Requirements/User Stories/Task Description (width: 60, wrap text enabled)
- Detailed description of the requirement, user story, or task.
- For user stories, use the format: "As a [role], I want to [action], so that [benefit]."
- For tasks, use a concise imperative statement.

#### Column E: Capability (width: 25)
- Data validation dropdown with the following values:
  - Azure
  - Power Platform
  - Data & AI
  - Integration
  - Software Engineering
  - Testing
  - D365 CE+PP
  - D365 F&O
  - Databricks

#### Column F: MOSCOW (width: 12)
- Data validation dropdown:
  - **MH**: Must Have
  - **SH**: Should Have
  - **CH**: Could Have
  - **WH**: Won't Have (this time)

**Color coding:**
| Priority | Background Color  |
| -------- | ----------------- |
| MH       | Red (#FF0000)     |
| SH       | Orange (#FFA500)  |
| CH       | Yellow (#FFFF00)  |
| WH       | Gray (#BFBFBF)    |

#### Column G: Fit Gap (width: 18)
- Data validation dropdown:
  - **OOB**: Out of the Box (no customization needed)
  - **Config**: Configuration only (settings, toggles, parameters)
  - **Customization**: Custom development required
  - **Third Party**: External vendor or third-party solution

#### Column H: Complexity (width: 15)
- Data validation dropdown:
  - V.Simple
  - Simple
  - Medium
  - Complex
  - V.Complex

**Story point mapping:**
| Complexity | Story Points |
| ---------- | ------------ |
| V.Simple   | 1            |
| Simple     | 2            |
| Medium     | 3            |
| Complex    | 5            |
| V.Complex  | 8            |

#### Column I: Volume/No of Units (width: 18)
- Numeric value representing the story point measure for the item.
- Derived from Complexity mapping multiplied by count of units where applicable.
- Number format: integer, no decimals.

### Sheet 1 Formatting

- **Header row:** Bold, dark blue background (#003366), white text (#FFFFFF), freeze pane on row 1.
- **Alternating row colors:** Odd rows white (#FFFFFF), even rows light gray (#F2F2F2).
- **Wrap text:** Enabled on Column D.
- **Auto-filter:** Enabled on all columns.
- **Conditional formatting:** Applied to Column F (MOSCOW) with the color coding above.
- **Number format:** Column A and Column I as integer.
- **Subtotals:** Group by Column B (Epic/Module) with SUM on Column I.

---

## Sheet 2: "Summary"

A pivot-style summary sheet providing aggregated views of the effort data.

### Section 1: Total Story Points by Capability (rows 2-12)
| Capability             | Total Story Points |
| ---------------------- | ------------------ |
| Azure                  | =SUMIFS(...)       |
| Power Platform         | =SUMIFS(...)       |
| Data & AI              | =SUMIFS(...)       |
| Integration            | =SUMIFS(...)       |
| Software Engineering   | =SUMIFS(...)       |
| Testing                | =SUMIFS(...)       |
| D365 CE+PP             | =SUMIFS(...)       |
| D365 F&O               | =SUMIFS(...)       |
| Databricks             | =SUMIFS(...)       |
| **Grand Total**        | =SUM(...)          |

### Section 2: Total Story Points by MOSCOW Priority (rows 14-19)
| Priority   | Total Story Points | Percentage |
| ---------- | ------------------ | ---------- |
| MH         | =SUMIFS(...)       | =.../Total |
| SH         | =SUMIFS(...)       | =.../Total |
| CH         | =SUMIFS(...)       | =.../Total |
| WH         | =SUMIFS(...)       | =.../Total |

### Section 3: Count by Fit-Gap Category (rows 21-26)
| Fit Gap       | Count          |
| ------------- | -------------- |
| OOB           | =COUNTIFS(...) |
| Config        | =COUNTIFS(...) |
| Customization | =COUNTIFS(...) |
| Third Party   | =COUNTIFS(...) |

### Section 4: Count by Complexity Level (rows 28-34)
| Complexity | Count          |
| ---------- | -------------- |
| V.Simple   | =COUNTIFS(...) |
| Simple     | =COUNTIFS(...) |
| Medium     | =COUNTIFS(...) |
| Complex    | =COUNTIFS(...) |
| V.Complex  | =COUNTIFS(...) |

### Charts
- **Pie chart:** Capability distribution of total story points. Positioned at cell D2, size 400x300px.
- **Bar chart:** MOSCOW priority breakdown. Positioned at cell D18, size 400x300px.

---

## Example Data Rows (Sheet 1)

| Sl No. | Epic/Module          | RFR Reference | Requirements/User Stories/Task Description                                                    | Capability         | MOSCOW | Fit Gap       | Complexity | Volume |
| ------ | -------------------- | ------------- | --------------------------------------------------------------------------------------------- | ------------------ | ------ | ------------- | ---------- | ------ |
| 1      | Customer Service AI  | REQ-FR-001    | As a service agent, I want AI-suggested responses so that I can resolve tickets faster         | Data & AI          | MH     | Customization | Complex    | 5      |
| 2      | Customer Service AI  | REQ-FR-002    | Implement knowledge base ingestion pipeline for RAG pattern                                    | Azure              | MH     | Customization | V.Complex  | 8      |
| 3      | Identity & Access    | REQ-SE-001    | Configure Conditional Access policies for zero-trust authentication                            | Azure              | MH     | Config        | Medium     | 3      |
| 4      | Data Migration       | REQ-DA-001    | Migrate 2.5M customer records from on-prem SQL to Dataverse                                   | D365 CE+PP         | MH     | Customization | Complex    | 5      |
| 5      | Integration Layer    | REQ-IN-001    | As a system admin, I want real-time sync between D365 and legacy ERP so that data is consistent | Integration        | SH     | Customization | V.Complex  | 8      |
| 6      | Reporting            | REQ-FR-010    | Build Power BI dashboard for call center KPIs and agent performance                            | Power Platform     | CH     | Config        | Simple     | 2      |

---

## xlsx Skill Invocation Pattern

```
Invoke the xlsx skill to create an Excel workbook with:
- Sheet 1 name: "Effort Detail"
  - Columns: [A: "Sl No." (8), B: "Epic/Module/Work stream" (35), C: "RFR Reference" (20),
    D: "Requirements/User Stories/Task Description" (60, wrap), E: "Capability" (25),
    F: "MOSCOW" (12), G: "Fit Gap" (18), H: "Complexity" (15), I: "Volume/No of Units" (18)]
  - Data validation on E: ["Azure", "Power Platform", "Data & AI", "Integration",
    "Software Engineering", "Testing", "D365 CE+PP", "D365 F&O", "Databricks"]
  - Data validation on F: ["MH", "SH", "CH", "WH"]
  - Data validation on G: ["OOB", "Config", "Customization", "Third Party"]
  - Data validation on H: ["V.Simple", "Simple", "Medium", "Complex", "V.Complex"]
  - Conditional formatting on F: MH=Red, SH=Orange, CH=Yellow, WH=Gray
  - Header formatting: bold, #003366 background, white text
  - Freeze top row, auto-filter enabled
- Sheet 2 name: "Summary"
  - SUMIFS tables by Capability, MOSCOW, Fit-Gap, Complexity
  - Pie chart for Capability distribution
  - Bar chart for MOSCOW breakdown
- Data: [provide rows]
```
