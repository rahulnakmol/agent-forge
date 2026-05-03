---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 2800
keywords: [ai-capabilities, sap, joule, business-ai, btp-ai, process-automation, generative-ai]
version: "1.0"
last_updated: "2026-03-28"
---

# SAP AI Capabilities — TOM Process Categories to SAP AI Features

## Overview

SAP's AI strategy is built around Business AI embedded natively into SAP applications and Joule as the generative AI copilot across the SAP ecosystem. SAP BTP provides foundational AI services for custom AI development. This reference maps SAP AI capabilities to TOM process categories.

---

## Joule AI Copilot — Four Capability Types

| Capability Type | Description | Example Use Cases |
|---|---|---|
| Transactional | Execute business transactions via natural language | Create purchase orders, post journal entries, approve requests, submit time sheets |
| Navigational | Guide users to the right app or screen | "Take me to supplier invoices", "Open my team's leave calendar" |
| Informational | Retrieve and summarize business data | "Show my open invoices over $10K", "Summarize this employee's performance history" |
| Analytical | Perform analysis and generate insights | "Why did procurement costs increase last quarter?", "Compare revenue across regions" |

### Joule Availability by Application

| Application | Joule Capabilities | Status |
|---|---|---|
| S/4HANA Cloud | Transaction execution, data retrieval, guided navigation | GA (growing scenario coverage) |
| SuccessFactors | Job description generation, candidate summaries, performance insights | GA |
| SAP Ariba | Sourcing event creation, supplier risk summaries | GA |
| SAP Build Code | Code generation (ABAP, CAP, JavaScript), test generation, documentation | GA |
| SAP Analytics Cloud | Natural language querying, story generation, insight explanations | GA |
| SAP Integration Suite | Integration flow generation from natural language descriptions | GA |

---

## Embedded Business AI Scenarios

### Finance

| AI Scenario | Module | TOM Process Category | Description |
|---|---|---|---|
| Intelligent Accruals | S/4HANA Finance | Record-to-Report | Automated accrual estimation using historical patterns |
| Cash Flow Prediction | S/4HANA Cash Management | Treasury | ML-based cash position forecasting |
| Invoice Matching | S/4HANA AP | Procure-to-Pay | Three-way match automation with exception handling |
| Credit Risk Scoring | S/4HANA AR | Order-to-Cash | ML-driven customer credit risk assessment |
| Anomaly Detection (GL) | S/4HANA Finance | Record-to-Report | Detect unusual journal entries and posting patterns |

### Supply Chain & Manufacturing

| AI Scenario | Module | TOM Process Category | Description |
|---|---|---|---|
| Demand Sensing | S/4HANA SCM | Plan-to-Produce | Short-term demand forecasting using external signals |
| Predictive MRP | S/4HANA PP | Plan-to-Produce | ML-enhanced material requirements planning |
| Quality Prediction | S/4HANA QM | Plan-to-Produce | Predict quality issues before they occur |
| Delivery Performance | S/4HANA SD | Order-to-Cash | Predict on-time delivery probability |
| Supplier Risk Scoring | SAP Ariba | Procure-to-Pay | AI-driven supplier risk assessment with external data |

### Human Capital Management

| AI Scenario | Module | TOM Process Category | Description |
|---|---|---|---|
| Job Description Generator | SuccessFactors Recruiting | Hire-to-Retire | AI-generated inclusive job descriptions |
| Candidate Ranking | SuccessFactors Recruiting | Hire-to-Retire | ML-based candidate-to-role matching |
| Skills Inference | SuccessFactors | Hire-to-Retire | Infer employee skills from role history and learning |
| Retention Risk | SuccessFactors | Hire-to-Retire | Predict employee flight risk |
| Learning Recommendations | SuccessFactors Learning | Hire-to-Retire | Personalized learning path suggestions |
| Compensation Insights | SuccessFactors Compensation | Hire-to-Retire | Market benchmarking and pay equity analysis |

### Procurement

| AI Scenario | Module | TOM Process Category | Description |
|---|---|---|---|
| Guided Buying | SAP Ariba Buying | Procure-to-Pay | AI-guided catalog search and supplier recommendations |
| Spend Classification | SAP Ariba Spend Analysis | Procure-to-Pay | Automated spend categorization using ML |
| Contract Intelligence | SAP Ariba Contracts | Procure-to-Pay | AI-assisted contract clause extraction and risk flagging |
| Supplier Discovery | SAP Business Network | Procure-to-Pay | AI-recommended suppliers based on requirements |

---

## SAP Build Code AI (Developer AI)

| Capability | Description |
|---|---|
| Code generation | Generate ABAP, CAP (Node.js/Java), and UI5 code from natural language |
| Unit test generation | Auto-generate unit tests for existing code |
| Code explanation | Explain legacy ABAP code and suggest modernization |
| Data model generation | Create CDS data models from business descriptions |
| Documentation | Auto-generate technical documentation from code |
| Bug detection | Identify potential issues and suggest fixes |

---

## SAP BTP AI Services

| Service | Capability | Use Case |
|---|---|---|
| SAP AI Core | Model training, serving, and lifecycle management | Custom ML models, foundation model access (GPT, Google) |
| SAP AI Launchpad | ML operations dashboard | Monitor and manage AI scenarios across BTP |
| Document Information Extraction | Extract fields from business documents | Invoice processing, delivery notes, customs declarations |
| Data Attribute Recommendation | Predict master data attributes | Auto-classify materials, auto-assign GL accounts |
| Business Entity Recognition | Extract business entities from unstructured text | Identify company names, addresses, amounts in emails |
| Personalized Recommendation | Content-based and collaborative filtering | Product recommendations, learning content suggestions |

---

## Process Automation Candidates (AI-Augmented)

| Process | Automation Type | AI Enhancement | Expected Impact |
|---|---|---|---|
| Invoice processing (AP) | End-to-end automation | Document extraction + matching + posting | 80-90% touchless processing |
| Employee onboarding | Workflow automation | Joule-guided task completion, document generation | 60% time reduction |
| Purchase requisition | Guided workflow | Guided buying, auto-sourcing, approval prediction | 70% cycle time reduction |
| Financial close | Task orchestration | Anomaly detection, auto-reconciliation, accrual prediction | 30-40% close time reduction |
| Expense management | Mobile automation | Receipt OCR, policy compliance check, auto-approval | 85% touchless processing |
| Service ticket routing | Intelligent routing | NLP classification, sentiment analysis, auto-assignment | 50% faster resolution |
| Demand planning | Predictive automation | Demand sensing, external signal integration | 20-30% forecast accuracy improvement |
| Talent acquisition | Workflow + AI | Job description generation, candidate ranking, interview scheduling | 40% time-to-hire reduction |

---

## AI Capability-to-TOM Process Category Mapping

| TOM Process Category | SAP AI Capabilities | Maturity |
|---|---|---|
| Record-to-Report | Intelligent accruals, anomaly detection, Joule GL queries | High |
| Order-to-Cash | Credit scoring, delivery prediction, Joule order management | High |
| Procure-to-Pay | Invoice automation, guided buying, spend classification, supplier risk | High |
| Plan-to-Produce | Demand sensing, predictive MRP, quality prediction | Medium-High |
| Hire-to-Retire | Skills inference, retention risk, job description AI, candidate ranking | High |
| Treasury & Cash Mgmt | Cash flow prediction, bank statement matching | Medium |
| Asset Management | Predictive maintenance (via SAP APM), anomaly detection | Medium |
| Customer Service | Joule-assisted case handling, sentiment analysis, knowledge search | Medium |
| IT Operations | SAP Cloud ALM AI-assisted operations, anomaly detection | Medium |

## Licensing & AI Considerations

| Aspect | Detail |
|---|---|
| Joule access | Included with S/4HANA Cloud, SuccessFactors, and Ariba subscriptions |
| Business AI scenarios | Included with application licenses (130+ scenarios) |
| SAP AI Core (BTP) | Consumption-based pricing on BTP (AI units) |
| Data residency | SAP AI processes data within SAP's trust boundary; no customer data used for model training |
| Foundation models | SAP partners with multiple LLM providers (OpenAI, Google, Anthropic) accessed via AI Core |
| Responsible AI | SAP AI Ethics policy, bias testing, transparency reporting |
