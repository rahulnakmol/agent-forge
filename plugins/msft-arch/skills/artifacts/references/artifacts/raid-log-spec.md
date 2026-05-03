---
category: artifacts
loading_priority: 2
tokens_estimate: 1200
keywords:
  - RAID log
  - risk
  - assumption
  - issue
  - dependency
  - workbook
  - xlsx
  - mitigation
  - project tracking
version: "1.0"
last_updated: "2026-03-21"
---

# RAID Log Workbook Specification

This document defines the complete specification for the RAID (Risks, Assumptions, Issues, Dependencies) Log Excel workbook. The RAID Log is a continuous artifact maintained across all engagement phases, capturing and tracking items that may impact project success.

## Sheet: "RAID Log"

### Column Specifications

#### Column A: RAID Name (width: 30)
- Descriptive identifier for the RAID item.
- Use a concise phrase that conveys the nature and subject of the item.
- Examples: "Data Migration Complexity Risk", "Azure Region Availability Assumption", "Legacy API Deprecation Issue", "D365 Licensing Dependency".

#### Column B: Type (width: 15)
- Data validation dropdown:
  - **Risk**: Potential event that could negatively impact the project
  - **Assumption**: Condition believed to be true but not yet confirmed
  - **Issue**: Current problem that is actively affecting the project
  - **Dependency**: External factor or deliverable the project relies upon

**Color coding:**
| Type       | Background Color   |
| ---------- | ------------------ |
| Risk       | Red (#FF0000)      |
| Assumption | Blue (#4472C4)     |
| Issue      | Orange (#FFA500)   |
| Dependency | Purple (#7030A0)   |

#### Column C: Description (width: 60, wrap text enabled)
- Detailed explanation of the RAID item.
- Provide enough context for someone unfamiliar with the project to understand the item.
- Use complete sentences; 2-4 sentences recommended.

#### Column D: Mitigation (width: 50, wrap text enabled)
- Action plan to address the RAID item.
- For Risks: preventive and contingency actions.
- For Assumptions: validation steps and fallback plans.
- For Issues: resolution steps and timeline.
- For Dependencies: tracking mechanism and escalation path.

#### Column E: Owner (width: 25)
- Person or role responsible for managing the item.
- Use role titles when specific names are not yet assigned.
- Examples: "Solution Architect", "Project Manager", "Security Lead", "Client IT Director".

#### Column F: Referenced ADR (width: 30)
- Cross-reference to the ADR Ref No from the ADR Workbook.
- Format: `MS-[TECH]-[PLATFORM]-[PROJECT]-XXX` (matches ADR Ref No format).
- Leave blank if the RAID item is not linked to a specific ADR.

### Optional Additional Columns

#### Column G: Priority (width: 12)
- Data validation dropdown: **High** | **Medium** | **Low**
- Color coding: High=Red (#FF0000), Medium=Yellow (#FFFF00), Low=Green (#00B050)

#### Column H: Status (width: 15)
- Data validation dropdown:
  - **Open**: Item is active and unresolved
  - **In Progress**: Mitigation actions are underway
  - **Mitigated**: Risk reduced to acceptable level or assumption validated
  - **Closed**: Item fully resolved
  - **Accepted**: Item acknowledged and accepted without further action

#### Column I: Due Date (width: 15)
- Date format: YYYY-MM-DD
- Target date for mitigation or resolution.

### Formatting Rules

- **Header row:** Bold, dark blue background (#003366), white text (#FFFFFF), freeze pane on row 1.
- **Alternating row colors:** Odd rows white (#FFFFFF), even rows light gray (#F2F2F2).
- **Conditional formatting:** Applied to Column B (Type) with the color coding defined above.
- **Wrap text:** Enabled on Columns C and D.
- **Auto-filter:** Enabled on all columns (A through I).
- **Font:** Calibri 10pt for data rows, Calibri 11pt bold for headers.
- **Border:** Thin border on all cells.

### Example Data Rows

| RAID Name                              | Type       | Description                                                                                                              | Mitigation                                                                                                        | Owner              | Referenced ADR                  | Priority | Status      | Due Date   |
| -------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------- | -------- | ----------- | ---------- |
| Data Migration Complexity Risk         | Risk       | Migration of 2.5M customer records from on-prem SQL to Dataverse may exceed estimated timeline due to data quality issues. | Conduct data profiling in Sprint 1. Establish data cleansing pipeline. Add 20% buffer to migration estimate.       | Solution Architect | MS-DATA-AZURE-CALLCENTER-003   | High     | Open        | 2026-04-15 |
| Azure OpenAI Regional Availability     | Assumption | GPT-4o model is assumed to be available in EU West region with sufficient quota for production workloads.                  | Validate quota availability with Microsoft account team by end of discovery phase. Identify fallback to EU North.  | Cloud Architect    | MS-AI-AZURE-CALLCENTER-001     | High     | In Progress | 2026-04-01 |
| Legacy ERP API Deprecation             | Issue      | The legacy ERP vendor has announced deprecation of the SOAP API in Q4 2026, earlier than the planned migration cutover.    | Accelerate integration layer development. Negotiate extended support window with vendor. Prepare REST adapter.     | Integration Lead   | MS-INT-D365-CALLCENTER-004     | High     | Open        | 2026-05-01 |
| D365 CE Licensing Procurement          | Dependency | Project timeline depends on client procuring 500 D365 CE licenses before UAT phase begins.                               | Provide license requirements document by Sprint 2. Set up weekly procurement tracking with client IT.              | Project Manager    |                                 | Medium   | Open        | 2026-06-01 |
| MFA Rollout User Readiness             | Risk       | End users may resist MFA enforcement, leading to increased help desk tickets and productivity loss during rollout.         | Plan phased MFA rollout with pilot group. Prepare user communication and training materials. Staff help desk surge. | Security Lead      | MS-SEC-ENTRA-CALLCENTER-002    | Medium   | Open        | 2026-05-15 |

### xlsx Skill Invocation Pattern

```
Invoke the xlsx skill to create an Excel workbook with:
- Sheet name: "RAID Log"
- Columns:
  - A: "RAID Name" (width: 30)
  - B: "Type" (width: 15)
  - C: "Description" (width: 60, wrap text)
  - D: "Mitigation" (width: 50, wrap text)
  - E: "Owner" (width: 25)
  - F: "Referenced ADR" (width: 30)
  - G: "Priority" (width: 12)
  - H: "Status" (width: 15)
  - I: "Due Date" (width: 15)
- Data validation on B: ["Risk", "Assumption", "Issue", "Dependency"]
- Data validation on G: ["High", "Medium", "Low"]
- Data validation on H: ["Open", "In Progress", "Mitigated", "Closed", "Accepted"]
- Conditional formatting on B: Risk=Red, Assumption=Blue, Issue=Orange, Dependency=Purple
- Header formatting: bold, #003366 background, white text
- Freeze top row, auto-filter enabled
- Data: [provide rows]
```
