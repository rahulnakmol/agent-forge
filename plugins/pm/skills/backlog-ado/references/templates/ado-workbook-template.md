# ADO Excel Workbook Template Specification

## Overview

The PM Backlog Generator produces an Excel workbook (.xlsx) for Azure DevOps
backlog import and project documentation. The workbook contains five sheets,
each serving a specific purpose.

---

## Sheet 1: Backlog Items

### Purpose
Contains all work items in a flat table format suitable for CSV export and ADO
import. This is the primary data sheet.

### Columns

| Column             | Width | Data Type | Format / Validation                      |
|--------------------|-------|-----------|------------------------------------------|
| Work Item Type     | 25    | Text      | Dropdown: Epic, Feature, User Story,     |
|                    |       |           | Technical User Story, Risk, Impediment,  |
|                    |       |           | Continuous Improvement Item              |
| ID                 | 10    | Number    | Auto-generated sequential (1, 2, 3...)   |
| Title              | 60    | Text      | Max 255 characters                       |
| State              | 12    | Text      | Always "New" for generated items         |
| Area               | 30    | Text      | Format: Project\Team                     |
| Iteration          | 30    | Text      | Format: Project\Release                  |
| Description        | 80    | Text      | HTML content (see formatting rules)      |
| Acceptance Criteria| 80    | Text      | HTML content (User Story/Tech Story only)|
| Priority           | 10    | Number    | Dropdown: 1, 2, 3                        |
| Risk               | 10    | Text      | Dropdown: 1-High, 2-Medium, 3-Low       |
| Story Points       | 12    | Number    | Dropdown: 1, 2, 3, 5, 8, 13, 21         |
| Effort             | 10    | Number    | Numeric (Feature only)                   |
| Business Value     | 14    | Number    | Range: 1-100 (Feature only)              |
| Time Criticality   | 14    | Number    | Range: 1-100 (Feature only)              |
| Parent ID          | 12    | Number    | References ID column of parent item      |
| Tags               | 40    | Text      | Semicolon-separated                      |

### Column Formatting Rules

- **Header row**: Bold, frozen, background color #4472C4 (blue), white text.
- **Work Item Type column**: Color-coded by type:
  - Epic: #7C3AED (purple)
  - Feature: #2563EB (blue)
  - User Story: #059669 (green)
  - Technical User Story: #D97706 (amber)
  - Risk: #DC2626 (red)
  - Impediment: #E11D48 (pink)
  - CI Item: #8B5CF6 (light purple)
- **Priority column**: Conditional formatting:
  - 1: Red background
  - 2: Yellow background
  - 3: Green background
- **Story Points column**: Right-aligned, number format.

### Data Validation Rules

- Work Item Type: List validation from allowed values.
- Priority: List validation (1, 2, 3).
- Story Points: List validation (1, 2, 3, 5, 8, 13, 21).
- Risk: List validation (1-High, 2-Medium, 3-Low).
- Business Value: Whole number between 1 and 100.
- Time Criticality: Whole number between 1 and 100.
- Parent ID: Whole number, must reference an existing ID in the sheet.

### Row Ordering

Items are ordered hierarchically:
1. Epic rows first (sorted by priority, then title).
2. Under each Epic: its child Features (sorted by priority, then title).
3. Under each Feature: its child Stories (sorted by type then priority).
4. Risks grouped after their parent.
5. Impediments at the end.
6. CI Items at the very end.

---

## Sheet 2: Hierarchy Map

### Purpose
Visual tree representation of the backlog hierarchy. This sheet is read-only
documentation, not for import.

### Layout

| Column A (Epic)              | Column B (Feature)               | Column C (Story)                         | Column D (Type) |
|-----------------------------|---------------------------------|------------------------------------------|-----------------|
| Customer Onboarding         |                                 |                                          | Epic            |
|                             | Self-Service Registration       |                                          | Feature         |
|                             |                                 | Register with email                      | User Story      |
|                             |                                 | Set up OAuth2 provider                   | Tech Story      |
|                             |                                 | Register with social login               | User Story      |
|                             | Profile Management              |                                          | Feature         |
|                             |                                 | Update profile information               | User Story      |
|                             |                                 | Upload profile photo                     | User Story      |
| Payment Processing          |                                 |                                          | Epic            |
|                             | Checkout Flow                   |                                          | Feature         |
|                             |                                 | Complete purchase with credit card       | User Story      |

### Formatting

- **Column A (Epic)**: Bold, font size 14, purple background (#7C3AED).
- **Column B (Feature)**: Bold, font size 12, blue background (#2563EB).
- **Column C (Story)**: Normal, font size 11, green or amber background based on type.
- **Column D (Type)**: Italic, font size 10.
- Indentation visually represents hierarchy depth.
- Empty cells indicate the item belongs to the parent in the column to the left.
- Group rows by Epic with collapsible sections (Excel grouping).

---

## Sheet 3: Risk Register

### Purpose
Dedicated risk tracking with all risk-specific fields. Provides a consolidated
view of all project risks.

### Columns

| Column          | Width | Data Type | Format / Validation                        |
|-----------------|-------|-----------|--------------------------------------------|
| Risk ID         | 10    | Text      | Format: R-001, R-002, etc.                 |
| Title           | 50    | Text      | Concise risk statement                     |
| Description     | 80    | Text      | Detailed risk description                  |
| Business Impact | 60    | Text      | Impact if risk materializes                |
| Likelihood      | 12    | Number    | Dropdown: 1 (Very Likely) to 5 (Very Unlikely) |
| Impact          | 10    | Text      | Dropdown: A (Severe) to E (Negligible)     |
| Risk Assessment | 14    | Number    | Formula: derived from Likelihood x Impact   |
| Mitigation Plan | 80    | Text      | Steps to mitigate                          |
| Owner           | 20    | Text      | Person responsible (blank by default)       |
| Status          | 15    | Text      | Dropdown: Open, Mitigating, Accepted, Closed|
| Parent Item     | 40    | Text      | Title of related Epic or Feature           |

### Conditional Formatting

- **Risk Assessment**:
  - 1 (High): Red background, white text
  - 2 (Medium High): Orange background
  - 3 (Medium): Yellow background
  - 4 (Medium Low): Light green background
  - 5 (Low): Green background
- **Status**:
  - Open: Red text
  - Mitigating: Orange text
  - Accepted: Blue text
  - Closed: Green text

### Risk Assessment Formula Reference

| Likelihood \ Impact | A     | B     | C     | D     | E     |
|---------------------|-------|-------|-------|-------|-------|
| 1 (Very Likely)     | 1     | 1     | 2     | 3     | 4     |
| 2 (Likely)          | 1     | 2     | 3     | 4     | 5     |
| 3 (Possible)        | 2     | 3     | 3     | 4     | 5     |
| 4 (Unlikely)        | 3     | 3     | 4     | 5     | 5     |
| 5 (Very Unlikely)   | 3     | 4     | 5     | 5     | 5     |

---

## Sheet 4: Impediments

### Purpose
Track all identified impediments with resolution plans and status.

### Columns

| Column          | Width | Data Type | Format / Validation                        |
|-----------------|-------|-----------|--------------------------------------------|
| ID              | 10    | Text      | Format: IMP-001, IMP-002, etc.             |
| Title           | 50    | Text      | Concise impediment description             |
| Description     | 80    | Text      | Detailed impediment description            |
| Resolution      | 80    | Text      | Proposed or actual resolution steps        |
| Priority        | 10    | Number    | Dropdown: 1, 2, 3                          |
| Owner           | 20    | Text      | Person responsible (blank by default)       |
| Status          | 15    | Text      | Dropdown: Open, In Progress, Resolved      |
| Blocked Items   | 40    | Text      | List of stories/features affected          |
| Date Identified | 15    | Date      | Auto-populated with generation date        |
| Target Date     | 15    | Date      | Expected resolution date (blank by default)|

### Conditional Formatting

- **Priority**:
  - 1: Red background
  - 2: Yellow background
  - 3: Green background
- **Status**:
  - Open: Red text
  - In Progress: Orange text
  - Resolved: Green text

---

## Sheet 5: CI Items

### Purpose
Track continuous improvement opportunities identified during backlog generation.

### Columns

| Column           | Width | Data Type | Format / Validation                       |
|------------------|-------|-----------|--------------------------------------------|
| ID               | 10    | Text      | Format: CI-001, CI-002, etc.               |
| Title            | 50    | Text      | Improvement opportunity description        |
| Description      | 80    | Text      | What needs to improve and why              |
| Expected Benefit | 60    | Text      | Measurable benefit of the improvement      |
| Priority         | 10    | Number    | Dropdown: 1, 2, 3                          |
| Owner            | 20    | Text      | Person responsible (blank by default)       |
| Category         | 20    | Text      | Dropdown: Process, Tooling, Documentation, |
|                  |       |           | Testing, Communication, Other              |
| Status           | 15    | Text      | Dropdown: Proposed, Approved, In Progress, |
|                  |       |           | Completed                                  |

### Conditional Formatting

- **Priority**: Same as Impediments sheet.
- **Category**: Color-coded by category type.

---

## Workbook-Level Settings

### General

- **File name**: `backlog-{prd-name}-ado-workbook.xlsx`
- **Default font**: Calibri, size 11
- **Sheet tab colors**:
  - Backlog Items: Blue (#2563EB)
  - Hierarchy Map: Purple (#7C3AED)
  - Risk Register: Red (#DC2626)
  - Impediments: Orange (#D97706)
  - CI Items: Green (#059669)

### Summary Row

Each data sheet includes a summary row at the bottom (separated by a blank row):

- **Backlog Items**: Total count by work item type, total story points.
- **Risk Register**: Count by risk assessment level, count by status.
- **Impediments**: Count by priority, count by status.
- **CI Items**: Count by category, count by status.

### Print Settings

- Landscape orientation for all sheets.
- Fit to 1 page wide (allow multiple pages tall).
- Repeat header row on each printed page.
- Include sheet name and page number in footer.
