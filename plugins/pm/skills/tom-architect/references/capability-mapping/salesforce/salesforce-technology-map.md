---
category: "capability-mapping"
loading_priority: 1
tokens_estimate: 3400
keywords: [technology-map, salesforce, tom-layers, capability-mapping, sales-cloud, service-cloud, marketing-cloud, mulesoft, tableau, platform]
version: "1.0"
last_updated: "2026-03-28"
---

# Salesforce Technology Map — TOM Capabilities to Salesforce Stack

## Overview

This master mapping connects each TOM design layer to the recommended Salesforce technology. Salesforce is predominantly a CRM and customer engagement platform; this map covers its full ecosystem including MuleSoft for integration and Tableau for analytics.

---

## Layer 1: Processes

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Process automation | Salesforce Flow (Record-Triggered, Screen, Autolaunched) | Apex Triggers (complex logic) | Flow for declarative automation; Apex for code-based complex scenarios |
| Process mining | Salesforce does not offer native process mining | Partner: Celonis, SAP Signavio | Integrate via MuleSoft or APIs |
| Business rules | Salesforce Flow (Decision Elements, Formulas) | Validation Rules, Apex | Flow for orchestrated decisions; Validation Rules for field-level enforcement |
| Workflow orchestration | Salesforce Flow Orchestrator | MuleSoft Composer | Flow Orchestrator for multi-step, multi-user processes; MuleSoft for cross-system |
| Document processing | Salesforce does not offer native document AI | Partner: DocuSign, Adobe, OmniStudio | OmniStudio for guided document generation |
| RPA | MuleSoft RPA | Third-party (UiPath, Automation Anywhere) | MuleSoft RPA for Salesforce-adjacent automation |

## Layer 2: Organization

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Org structure management | Salesforce Roles & Territories | External HR system integration | Roles for data access hierarchy; Territories for sales alignment |
| Role management | Salesforce Profiles, Permission Sets, Permission Set Groups | Salesforce Shield (Event Monitoring) | Permission Sets for modular RBAC; Groups for scalable assignment |
| Workforce planning | Not native to Salesforce | Integrate with Workday / SuccessFactors | Salesforce focuses on customer-facing roles, not full workforce |
| Skills & competency | Salesforce Trailhead (employee learning) | Partner LMS integration | Trailhead for Salesforce skills; LMS for broader competency |
| Collaboration | Slack (Salesforce-owned) | Chatter (in-app collaboration) | Slack for real-time team collaboration; Chatter for record-level discussion |
| Identity governance | Salesforce Shield + Identity Connect | SSO (SAML/OIDC), MFA | Shield for advanced security monitoring; Identity Connect for AD sync |

## Layer 3: Service

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Service desk | Service Cloud (Cases, Omni-Channel) | Einstein Service Agent (AI) | Service Cloud for full case lifecycle; Einstein Agent for AI deflection |
| ITSM | Not native (CRM-focused) | ServiceNow integration via MuleSoft | Salesforce is not an ITSM platform; integrate with ITSM tools |
| SLA management | Service Cloud (Entitlements, Milestones) | Omni-Channel SLA tracking | Entitlements define SLAs; Milestones track compliance |
| Knowledge management | Service Cloud Knowledge | Einstein Search, Lightning Knowledge | Knowledge for structured articles; Einstein for AI-powered search |
| Self-service portal | Experience Cloud (Customer Community) | Einstein Bots, Salesforce Help Center | Experience Cloud for branded portals; Bots for conversational self-service |
| Service analytics | CRM Analytics (formerly Tableau CRM) | Service Cloud Einstein Analytics | Embedded dashboards in Service Cloud; CRM Analytics for advanced |

## Layer 4: Technology

### CRM & Customer Engagement

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| Lead Management | Sales Cloud | Leads, Web-to-Lead, Lead Assignment | Lead capture, scoring, qualification, conversion |
| Opportunity Management | Sales Cloud | Opportunities, Products, Price Books | Pipeline management, stage tracking, forecasting |
| Account & Contact Mgmt | Sales Cloud | Accounts, Contacts, Person Accounts | 360-degree customer view with hierarchy support |
| Sales Forecasting | Sales Cloud | Forecasting, Pipeline Inspection | Collaborative forecasting with AI-enhanced predictions |
| CPQ | Salesforce CPQ (Revenue Cloud) | Products, Quotes, Contracts, Billing | Configure-price-quote with subscription billing |
| Case Management | Service Cloud | Cases, Queues, Assignment Rules, Macros | Omnichannel case routing and resolution |
| Knowledge Base | Service Cloud | Knowledge Articles, Categories, Data Categories | Internal and external knowledge with article versioning |
| Omnichannel Service | Service Cloud | Omni-Channel, Chat, Messaging, Voice | Unified agent console across phone, chat, email, social, messaging |
| Field Service | Salesforce Field Service | Work Orders, Scheduling, Mobile App | Dispatch optimization, mobile workforce, asset management |
| Marketing Journeys | Marketing Cloud Engagement | Journey Builder, Email Studio, Mobile Studio | Multi-channel customer journey orchestration |
| Personalization | Marketing Cloud Personalization | Web, Email, App personalization | Real-time interaction management and recommendations |
| Data Cloud (CDP) | Salesforce Data Cloud | Unified Profiles, Segmentation, Activation | Customer data platform for unified identity resolution |
| B2B Commerce | Commerce Cloud | Storefronts, Catalogs, Pricing, Order Mgmt | Headless commerce for B2B buyer experiences |
| B2C Commerce | Commerce Cloud | Storefronts, Promotions, Search, Einstein Recommendations | Digital storefronts with AI-driven product recommendations |
| Order Management | Salesforce Order Management | Order Lifecycle, Fulfillment, Returns | Distributed order management with inventory visibility |

### Platform & Development

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Declarative development | Salesforce Flow, Lightning App Builder | No-code/low-code app building and automation |
| Pro-code development | Apex, Lightning Web Components (LWC) | Server-side (Apex) and client-side (LWC) custom development |
| External portals | Experience Cloud | Branded communities, portals, and sites for customers and partners |
| AppExchange | Salesforce AppExchange | 7000+ partner applications and components |
| Mobile | Salesforce Mobile App | Native mobile access to all Salesforce data and customizations |

### Integration & Analytics

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Integration platform | MuleSoft Anypoint Platform | API-led connectivity, 400+ prebuilt connectors, API lifecycle management |
| API management | MuleSoft API Manager | API gateway, policies, analytics, developer portal |
| Event-driven architecture | Platform Events + Change Data Capture | Platform Events for pub-sub; CDC for data change notifications |
| Enterprise analytics | Tableau | Visual analytics, dashboards, data prep, governed self-service |
| Embedded analytics | CRM Analytics (Tableau CRM) | AI-powered analytics embedded in Salesforce UI |
| Data visualization | Tableau | Industry-leading visualization with natural language queries |

## Layer 5: Data & Analytics

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Customer analytics | CRM Analytics | Tableau | CRM Analytics for in-platform; Tableau for enterprise-wide |
| KPI dashboards | Tableau, CRM Analytics | Salesforce Reports & Dashboards | Tableau for advanced; native Reports for operational |
| Customer 360 | Salesforce Data Cloud | MuleSoft data integration | Data Cloud for unified customer profiles from all sources |
| Predictive analytics | Einstein Discovery | Tableau (Einstein) | Einstein Discovery for no-code predictions in Salesforce |
| Data integration | MuleSoft Anypoint | Salesforce Connect (OData) | MuleSoft for enterprise; Salesforce Connect for virtual objects |
| Data governance | Salesforce Shield (Field Audit Trail) | Data Cloud governance features | Shield for audit and encryption; Data Cloud for data lineage |
| Real-time data | Data Cloud (Streaming Data) | Platform Events, CDC | Data Cloud for real-time unification; Events for app-level streaming |
| Master data | Salesforce Data Cloud | MuleSoft + MDM partner | Data Cloud for customer MDM; MuleSoft for cross-system MDM |

## Layer 6: Governance

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Access governance | Salesforce Shield (Event Monitoring) | Health Check, Permission Set analysis | Shield for monitoring access patterns; Health Check for baseline security |
| Data protection | Salesforce Shield (Platform Encryption) | Data Mask (sandbox) | Shield for encryption at rest; Data Mask for non-prod environments |
| Compliance management | Salesforce Shield (Field Audit Trail) | Financial Services Cloud Compliance | 10-year audit trail for regulated fields |
| Security monitoring | Salesforce Shield (Event Monitoring + Threat Detection) | Login Forensics | Real-time threat detection and event-level monitoring |
| Privacy management | Salesforce Privacy Center | Data Cloud consent management | Privacy Center for GDPR/CCPA; Data Cloud for consent-based activation |
| Audit & logging | Salesforce Setup Audit Trail + Shield Event Monitoring | Debug Logs (development) | Setup Audit Trail for config changes; Event Monitoring for user activity |

---

## Salesforce Ignite Methodology

| Phase | Key Activities | Salesforce Tools |
|---|---|---|
| Align | Business alignment, stakeholder mapping, vision | Salesforce Advisory Services |
| Discover | Current state analysis, process mapping, requirements | Salesforce Business Analyst tools, Data Cloud assessment |
| Design | Solution architecture, data model, integration design | Salesforce Architect resources, MuleSoft C4E |
| Build | Configuration, development, integration, data migration | Salesforce DevOps Center, Scratch Orgs, MuleSoft |
| Validate | Testing (unit, integration, UAT, performance) | Salesforce Test frameworks, CumulusCI |
| Deploy | Release management, cutover, go-live | Salesforce DevOps Center, Change Sets, Managed Packages |
| Evolve | Adoption tracking, continuous improvement, new releases | Salesforce Optimizer, In-App Guidance, Trailhead |

## Integration Patterns

| Pattern | Salesforce Technology | Use Case |
|---|---|---|
| API-based (sync) | MuleSoft Anypoint + Salesforce REST/SOAP APIs | Real-time data sync between Salesforce and external systems |
| Event-driven (async) | Platform Events + MuleSoft | Pub-sub event notifications (e.g., Opportunity closed-won) |
| Change Data Capture | Salesforce CDC + MuleSoft | React to record changes in near-real-time |
| File-based (batch) | Data Loader, Bulk API, MuleSoft Batch | Large-volume data loads and migrations |
| Virtual integration | Salesforce Connect (External Objects) | Real-time access to external data without replication |
| Prebuilt connectors | MuleSoft Anypoint Exchange | 400+ prebuilt connectors for common systems (SAP, Workday, etc.) |

## Licensing & Editions

| Edition | Scope | Typical Use Case |
|---|---|---|
| Sales Cloud (Enterprise/Unlimited) | Per-user/month | Full CRM for sales teams; Unlimited adds Premier Support |
| Service Cloud (Enterprise/Unlimited) | Per-user/month | Omnichannel service; Unlimited adds 24/7 support |
| Marketing Cloud Engagement | Contact-based pricing | Email, journey, and mobile marketing automation |
| Marketing Cloud Account Engagement (Pardot) | Per-user pricing | B2B marketing automation and lead nurturing |
| Data Cloud | Per-profile pricing | CDP for unified customer data, segmentation, activation |
| Commerce Cloud | GMV-based or per-order | B2B and B2C digital commerce |
| MuleSoft | vCore-based (Anypoint) | Integration platform, API management |
| Tableau | Per-user (Creator/Explorer/Viewer) | Enterprise analytics and visualization |
| Salesforce Shield | Add-on to any edition | Platform encryption, event monitoring, field audit trail |

## Decision Matrix Summary

| Decision Factor | Recommended Approach |
|---|---|
| Customer-facing sales process | Sales Cloud with Einstein AI |
| Customer service and support | Service Cloud with Omni-Channel and Knowledge |
| Marketing automation (B2B) | Marketing Cloud Account Engagement (Pardot) |
| Marketing automation (B2C) | Marketing Cloud Engagement (Journey Builder) |
| Customer data unification | Data Cloud for unified profiles and segmentation |
| Enterprise integration | MuleSoft Anypoint Platform (API-led connectivity) |
| Enterprise analytics | Tableau for governed self-service analytics |
| Custom applications on platform | Lightning App Builder (low-code) or Apex/LWC (pro-code) |
| External-facing portals | Experience Cloud (communities) |
| Field workforce management | Salesforce Field Service |
