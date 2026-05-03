---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 2400
keywords: [d365-fo, finance-operations, erp, finance, scm, hr, x++, modules, procure-to-pay, order-to-cash, record-to-report]
version: "1.0"
last_updated: "2026-03-23"
---

# D365 Finance & Operations Mapping — Processes to Modules

## Overview

Maps Finance, Supply Chain Management, and Human Resources L1 processes to their corresponding D365 F&O modules. For each process area: the primary module, out-of-box (OOB) capabilities, common X++ customizations, and integration points.

---

## Finance L1 Processes

### Record to Report (R2R)

| Component | Detail |
|---|---|
| **D365 Modules** | General Ledger, Fixed Assets, Budgeting, Financial Reporting |
| **OOB Capabilities** | Chart of accounts, journal posting, financial dimensions, currency revaluation, consolidation, budget control, financial statements (Management Reporter / Financial Reporting) |
| **Common X++ Customizations** | Custom posting profiles, automated journal generation via batch, intercompany elimination rules, custom financial dimension validation, period-close automation extensions |
| **Integration Points** | Sub-ledger integration (AR/AP/Inventory auto-post to GL), bank statement import (Electronic Reporting), tax engine integration (Vertex, Avalara), consolidation from external entities via Data Management Framework (DMF) |
| **Copilot Features** | Collections coordinator copilot, cash flow forecasting AI |

### Procure to Pay (P2P)

| Component | Detail |
|---|---|
| **D365 Modules** | Procurement and Sourcing, Accounts Payable |
| **OOB Capabilities** | Purchase requisitions, purchase orders, vendor collaboration portal, three-way matching (PO/receipt/invoice), vendor invoice automation, payment proposals, vendor rebates, procurement categories |
| **Common X++ Customizations** | Custom approval workflows, automated matching tolerance rules, vendor onboarding extensions, custom scoring models for vendor evaluation, budget check overrides |
| **Integration Points** | Vendor portal (Power Pages or D365 portal), invoice capture (AI Builder), bank payment files (ISO 20022 via Electronic Reporting), punchout catalogs (cXML), e-invoicing (Electronic Invoicing add-in) |
| **Copilot Features** | Invoice matching anomaly detection, spend analytics AI |

### Order to Cash (O2C)

| Component | Detail |
|---|---|
| **D365 Modules** | Sales and Marketing, Accounts Receivable, Credit and Collections |
| **OOB Capabilities** | Sales quotations, sales orders, delivery scheduling, invoicing, free text invoices, customer payment journals, credit management, collection letters, interest notes, revenue recognition |
| **Common X++ Customizations** | Custom pricing engines, commission calculation extensions, automated credit limit checks, custom revenue recognition schedules, intercompany O2C chain modifications |
| **Integration Points** | CRM integration (D365 Sales dual-write), EDI (purchase order acknowledgment, ASN), payment gateways, e-invoicing, customer portal (Power Pages) |
| **Copilot Features** | Collections coordinator copilot, customer payment predictions |

### Treasury & Cash Management

| Component | Detail |
|---|---|
| **D365 Modules** | Cash and Bank Management, Cash Flow Forecasting |
| **OOB Capabilities** | Bank accounts, bank reconciliation (advanced), cash flow forecasting, letters of credit, letters of guarantee, postdated checks, centralized payments |
| **Common X++ Customizations** | Custom bank reconciliation matching rules, cash position reporting extensions, multi-bank connectivity modules, treasury dashboard data providers |
| **Integration Points** | Bank connectivity (SWIFT, host-to-host), cash flow forecasting AI (Azure ML), bank statement import (BAI2, MT940, CAMT.053), payment hub integration |
| **Copilot Features** | Cash flow forecasting with AI predictions |

---

## Supply Chain Management L1 Processes

### Plan to Produce

| Component | Detail |
|---|---|
| **D365 Modules** | Master Planning (Planning Optimization), Production Control, Product Information Management |
| **OOB Capabilities** | MRP/MPS, Planning Optimization (cloud-based), production orders (discrete, process, lean/kanban), BOM management, route management, shop floor execution, batch orders, co-products/by-products |
| **Common X++ Customizations** | Custom planning fence logic, production scheduling extensions, quality check integration at route operations, custom BOM explosion rules, shop floor device extensions |
| **Integration Points** | IoT integration (Azure IoT Hub for machine data), MES integration, demand forecasting (Azure ML), D365 Supply Chain Insights, Sensor Data Intelligence add-in |
| **Copilot Features** | Demand planning copilot, supply chain disruption alerts |

### Source to Contract

| Component | Detail |
|---|---|
| **D365 Modules** | Procurement and Sourcing, Vendor Management |
| **OOB Capabilities** | RFQ management, vendor evaluation, purchase agreements (blanket orders), vendor categories, approved vendor lists, vendor collaboration, procurement catalogs, sealed bidding |
| **Common X++ Customizations** | Custom vendor scorecards, contract compliance monitoring, automated rebate calculation extensions, category-based approval routing |
| **Integration Points** | Supplier portals (vendor collaboration or Power Pages), contract management (SharePoint or third-party CLM), Ariba/Coupa connectivity via integration middleware |

### Warehouse to Deliver

| Component | Detail |
|---|---|
| **D365 Modules** | Warehouse Management (WMS Advanced), Transportation Management |
| **OOB Capabilities** | Wave processing, location directives, work templates, mobile device flows (Warehouse Management mobile app), load planning, rate shopping, freight reconciliation, containerization, cross-docking |
| **Common X++ Customizations** | Custom wave templates, mobile device menu extensions, custom label printing logic, integration with warehouse automation (pick-to-light, ASRS), custom freight rate engines |
| **Integration Points** | Warehouse automation systems (material handling APIs), carrier APIs, GPS/fleet tracking, Advanced Shipping Notice (EDI 856), Warehouse Management mobile app customization |

### Inventory Management

| Component | Detail |
|---|---|
| **D365 Modules** | Inventory Management, Quality Management, Inventory Visibility |
| **OOB Capabilities** | Inventory transactions, batch/serial tracking, inventory aging, counting journals, quarantine management, quality orders, quality associations, inventory visibility service (real-time ATP) |
| **Common X++ Customizations** | Custom inventory dimensions, batch attribute extensions, quality test type additions, custom reservation logic, inventory valuation report extensions |
| **Integration Points** | Inventory Visibility add-in (real-time cross-channel ATP), IoT for temperature/condition monitoring, barcode/RFID integration via mobile app |

---

## Human Resources L1 Processes

### Hire to Retire

| Component | Detail |
|---|---|
| **D365 Modules** | Personnel Management, Recruitment (or LinkedIn Talent Hub) |
| **OOB Capabilities** | Worker records, position management, employment history, personnel actions, recruitment projects, applicant tracking, onboarding checklists, offboarding tasks |
| **Common X++ Customizations** | Custom personnel action types, onboarding workflow extensions, integration with background check providers, custom position hierarchy logic |
| **Integration Points** | LinkedIn Talent Solutions, background check APIs, payroll systems (Ceridian, ADP via Dayforce connector), identity provisioning (Entra ID lifecycle workflows) |

### Compensate

| Component | Detail |
|---|---|
| **D365 Modules** | Compensation Management, Benefits Management |
| **OOB Capabilities** | Fixed/variable compensation plans, compensation grids, benefit eligibility, open enrollment, life events, benefit plans (medical, dental, vision, retirement), flex credits |
| **Common X++ Customizations** | Custom compensation calculation rules, benefit plan eligibility overrides, integration with benefits carriers, custom variable compensation formulas |
| **Integration Points** | Payroll integration (Ceridian Dayforce connector), benefits carrier feeds (EDI 834), compensation benchmarking data imports |

### Develop

| Component | Detail |
|---|---|
| **D365 Modules** | Performance Management, Learning (coming), Skills and Competencies |
| **OOB Capabilities** | Performance journals, performance reviews, goal management, skill gap analysis, course management, certificates tracking |
| **Common X++ Customizations** | Custom review templates, competency framework extensions, training compliance automation |
| **Integration Points** | Viva Learning, LinkedIn Learning, LMS integration (Cornerstone, SAP SuccessFactors Learning), Power BI people analytics |

### Time & Attendance

| Component | Detail |
|---|---|
| **D365 Modules** | Time and Attendance, Project Time Entry |
| **OOB Capabilities** | Time registration, absence management, flex time, overtime calculation, time profiles, calculation parameters, project timesheet entry |
| **Common X++ Customizations** | Custom time calculation rules, shift pattern extensions, integration with physical time clocks, custom absence type workflows |
| **Integration Points** | Time clock hardware (badge readers), mobile time entry (Power Apps or D365 mobile), payroll export, project accounting integration |

---

## Cross-Cutting Considerations

| Aspect | Guidance |
|---|---|
| **Dual-Write** | Synchronize D365 F&O with Dataverse for CRM integration; use virtual entities for read scenarios, dual-write for bidirectional sync |
| **Data Management Framework** | Use DMF (data entities + data projects) for bulk data import/export and migration |
| **Electronic Reporting** | Use ER for configurable document formats (financial statements, regulatory reports, payment files) |
| **Feature Management** | Enable new features via Feature Management workspace; plan feature adoption per release wave |
| **X++ Best Practices** | Prefer chain of command (CoC) over overlayering; use extension-based customization; follow ISV-like development patterns for upgrade resilience |
