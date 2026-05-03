---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 1900
keywords: [d365-ce, customer-engagement, crm, sales, customer-service, field-service, project-operations, customer-insights, dataverse]
version: "1.0"
last_updated: "2026-03-23"
---

# D365 Customer Engagement Mapping — Processes to Modules

## Overview

Maps customer-facing TOM processes to D365 Customer Engagement modules. For each process area: the primary D365 CE module, core Dataverse entities, Power Platform extension patterns, and copilot features.

---

## Lead to Opportunity — D365 Sales

| Component | Detail |
|---|---|
| **D365 Module** | D365 Sales (Enterprise or Premium) |
| **Core Dataverse Entities** | Lead, Contact, Account, Opportunity, Quote, Order, Invoice, Product, Price List, Competitor |
| **OOB Capabilities** | Lead scoring, lead qualification, opportunity pipeline, sales forecasting, product catalog, discount management, quote generation, sales accelerator (sequences), relationship intelligence, conversation intelligence |
| **Power Platform Extensions** | Canvas apps for mobile seller experience; Power Automate for lead assignment and follow-up reminders; Power BI embedded for territory analytics; Copilot Studio for sales FAQ bot |
| **Copilot Features** | Email drafting with context, opportunity summarization, meeting preparation briefs, lead prioritization, CRM record updates from natural language |
| **Integration Points** | LinkedIn Sales Navigator (embedded profiles, InMail), Outlook/Teams integration (server-side sync), ERP integration via dual-write (quotes to sales orders), marketing automation (D365 Customer Insights - Journeys) |

## Case Management — D365 Customer Service

| Component | Detail |
|---|---|
| **D365 Module** | D365 Customer Service (Enterprise or Premium) |
| **Core Dataverse Entities** | Case (Incident), Knowledge Article, Entitlement, SLA, Queue, Activity (Email, Phone Call, Task), Customer Voice Survey |
| **OOB Capabilities** | Unified routing (intelligent work distribution), omnichannel engagement (chat, voice, SMS, social, email), knowledge base with AI search, SLA tracking with entitlements, agent desktop (Customer Service workspace), sentiment analysis, conversation summarization |
| **Power Platform Extensions** | Power Automate for escalation workflows and SLA breach notifications; Power Pages for customer self-service portal; Copilot Studio for customer-facing virtual agent; AI Builder for case classification |
| **Copilot Features** | Case summarization, suggested responses from knowledge base, email drafting, conversation wrap-up, real-time sentiment tracking, knowledge article generation from resolved cases |
| **Integration Points** | Telephony (Azure Communication Services or partner CTI), social channels (Facebook, WhatsApp, LINE, WeChat), IoT alerts (Azure IoT Hub), ERP (case-to-RMA or case-to-credit memo via integration) |

## Field Operations — D365 Field Service

| Component | Detail |
|---|---|
| **D365 Module** | D365 Field Service |
| **Core Dataverse Entities** | Work Order, Booking, Resource, Service Account, Asset (Customer Asset), Agreement, Incident Type, Inventory Adjustment, Purchase Order |
| **OOB Capabilities** | Work order lifecycle management, Resource Scheduling Optimization (RSO), schedule board, mobile technician app (model-driven), preventive maintenance agreements, IoT alert-to-work-order, inventory management (truck stock), inspections |
| **Power Platform Extensions** | Power Automate for work order status notifications and SLA escalations; canvas apps for custom inspection forms; Power BI for field service KPIs (first-time fix rate, mean time to repair); Copilot Studio for technician knowledge assistant |
| **Copilot Features** | Work order recaps, scheduling assistance, parts identification from photos, knowledge retrieval for repair procedures |
| **Integration Points** | IoT Hub (predictive maintenance triggers), ERP (inventory replenishment, purchase orders), GIS/mapping (Bing Maps, Azure Maps), asset management systems, Mixed Reality (Dynamics 365 Guides, Remote Assist) |

## Project Delivery — D365 Project Operations

| Component | Detail |
|---|---|
| **D365 Module** | D365 Project Operations (Lite, Resource/Non-stocked, or Stocked/Production) |
| **Core Dataverse Entities** | Project, Project Task, Resource Requirement, Booking, Time Entry, Expense Entry, Project Contract, Project Invoice, Estimate |
| **OOB Capabilities** | Project planning (WBS, Gantt), resource management (skills-based matching, availability), time and expense entry, project billing (fixed price, T&M, milestone), revenue recognition, project accounting (F&O integration for stocked mode), project cost tracking |
| **Power Platform Extensions** | Power Automate for time/expense approval workflows; canvas apps for simplified mobile time entry; Power BI for project profitability dashboards and resource utilization; Copilot Studio for project status inquiries |
| **Copilot Features** | Project status summaries, resource availability insights, risk identification from project telemetry |
| **Integration Points** | D365 Finance (project accounting, revenue recognition for stocked/production mode), Microsoft Project for the Web (scheduling engine), Teams (project collaboration channels), Azure DevOps (agile project delivery tracking) |

## Customer Insights — D365 Customer Insights

| Component | Detail |
|---|---|
| **D365 Module** | D365 Customer Insights — Data (CDP) + Journeys (marketing automation) |
| **Core Dataverse Entities** | Unified Customer Profile, Segment, Measure, Prediction, Journey, Email Template, Event, Marketing Form, Lead Scoring Model |
| **OOB Capabilities** | **Data**: Data unification (map, match, merge from multiple sources), AI predictions (churn, CLV, sentiment), segment builder, measures and KPIs, enrichment (brand affinity, interests) | **Journeys**: Real-time journey orchestration, trigger-based journeys, email/SMS/push channels, A/B testing, consent management, event management |
| **Power Platform Extensions** | Power Automate for journey trigger actions (create case, assign task); Power BI for marketing analytics; Copilot Studio for conversational lead capture; Power Pages for event registration |
| **Copilot Features** | Natural language segment creation, journey design assistance, content rewrite suggestions, campaign performance insights |
| **Integration Points** | Data sources (D365 Sales/Service, Azure Data Lake, third-party via connectors), Fabric (export unified profiles to lakehouse), advertising platforms (Google Ads, Facebook Ads audience sync), analytics (Power BI, Fabric) |

---

## Cross-Cutting D365 CE Architecture

### Dataverse Platform Capabilities

| Capability | Description |
|---|---|
| **Security model** | Business units, security roles, field-level security, hierarchy security, teams (owner, access, Entra ID group) |
| **Extensibility** | Plugins (C#), custom workflow activities, Power Automate (cloud flows as replacement for classic workflows), custom APIs, PCF controls |
| **Data integration** | Dataverse connectors (900+), virtual tables (OData, SQL, external), dual-write (F&O sync), Fabric link (Dataverse to OneLake) |
| **ALM** | Solutions (managed/unmanaged), environment strategy (dev/test/UAT/prod), Azure DevOps or GitHub pipelines, Power Platform CLI (pac) |

### D365 CE Environment Strategy

| Environment | Purpose | Data |
|---|---|---|
| Development | Feature development, customization | Synthetic or minimal |
| Test / QA | Integration testing, UAT | Anonymized production copy |
| Pre-production | Final validation, performance testing | Production copy |
| Production | Live business operations | Live data |
| Sandbox | POC, experimentation, training | Synthetic |

### Licensing Considerations

| App | Key License | Add-ons |
|---|---|---|
| D365 Sales | Enterprise or Premium | Sales Insights, Viva Sales |
| D365 Customer Service | Enterprise or Premium | Digital Messaging, Voice Channel |
| D365 Field Service | Per user | Remote Assist, Guides |
| D365 Project Operations | Per user | Deployment mode determines F&O integration |
| Customer Insights - Data | Per tenant (profile capacity) | Enrichments, predictions |
| Customer Insights - Journeys | Per tenant (interaction capacity) | SMS, push, custom channels |
