---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 2800
keywords: [ai-capabilities, oracle, fusion-ai, oci-ai, agentic-workflows, ai-agent-studio, embedded-ml]
version: "1.0"
last_updated: "2026-03-28"
---

# Oracle AI Capabilities — TOM Process Categories to Oracle AI Features

## Overview

Oracle embeds AI natively across its Fusion Cloud Applications with 100+ AI use cases and 50+ agentic workflows. Oracle Cloud Infrastructure (OCI) provides foundational AI services for custom development. This reference maps Oracle AI capabilities to TOM process categories.

---

## Oracle AI for Fusion Applications — 100+ AI Use Cases

### Finance AI

| AI Use Case | Module | TOM Process Category | Description |
|---|---|---|---|
| Intelligent Document Recognition | Fusion AP | Procure-to-Pay | Automated invoice capture and field extraction |
| Supplier Recommendation | Fusion Procurement | Procure-to-Pay | AI-suggested suppliers based on requisition content |
| Dynamic Discounting | Fusion AP | Procure-to-Pay | ML-optimized early payment discount offers |
| Cash Forecasting | Fusion Cash Management | Treasury | Predictive cash position using historical patterns and AR/AP data |
| Anomalous Transaction Detection | Fusion GL | Record-to-Report | Flag unusual journal entries and transaction patterns |
| Automated Account Reconciliation | Fusion GL | Record-to-Report | ML-assisted matching for reconciliation |
| Revenue Estimation | Fusion Revenue Management | Order-to-Cash | AI-driven standalone selling price estimation |
| Expense Violation Detection | Fusion Expenses | Procure-to-Pay | Detect policy violations and duplicate expense claims |

### HCM AI

| AI Use Case | Module | TOM Process Category | Description |
|---|---|---|---|
| Best Candidate Recommendation | HCM Recruiting | Hire-to-Retire | ML-ranked candidate shortlists based on job requirements |
| Internal Mobility Recommendations | HCM Career Development | Hire-to-Retire | AI-suggested internal roles based on skills and aspirations |
| Attrition Prediction | HCM Workforce | Hire-to-Retire | Predict which employees are at risk of leaving |
| Compensation Recommendations | HCM Compensation | Hire-to-Retire | Market-aligned pay recommendations with equity analysis |
| Skills Advisor | HCM Talent Profile | Hire-to-Retire | AI-inferred skills from job history, project experience |
| Absence Duration Prediction | HCM Absence Management | Hire-to-Retire | Predict expected absence duration for workforce planning |
| Learning Content Recommendations | HCM Learning | Hire-to-Retire | Personalized learning suggestions based on role and skills |

### Supply Chain AI

| AI Use Case | Module | TOM Process Category | Description |
|---|---|---|---|
| Demand Forecasting | SCM Planning | Plan-to-Produce | ML-enhanced demand forecasts with external signals |
| Lead Time Variability | SCM Procurement | Procure-to-Pay | Predict supplier lead time deviations |
| Quality Inspection Prediction | SCM Manufacturing | Plan-to-Produce | Predict inspection pass/fail likelihood |
| Order Promising Optimization | SCM Order Management | Order-to-Cash | AI-optimized ATP across distribution network |
| Backlog Management | SCM Order Management | Order-to-Cash | Prioritize orders based on predicted fulfillment success |

### CX AI

| AI Use Case | Module | TOM Process Category | Description |
|---|---|---|---|
| Lead Scoring | CX Sales | Lead-to-Cash | AI-ranked leads based on conversion probability |
| Opportunity Win Probability | CX Sales | Lead-to-Cash | Predictive deal scoring for pipeline management |
| Next Best Action (Sales) | CX Sales | Lead-to-Cash | AI-recommended sales actions and follow-ups |
| Intelligent Service Routing | CX Service | Customer Service | ML-based case assignment to best-fit agent |
| Answer Recommendations | CX Service | Customer Service | Suggest knowledge articles for service agents |
| Customer Sentiment Analysis | CX Service | Customer Service | NLP-based sentiment detection in service interactions |

---

## Agentic Workflows (50+ Scenarios)

Oracle's agentic AI workflows autonomously execute multi-step business processes with human-in-the-loop oversight.

| Agent Category | Example Workflows | TOM Process Category |
|---|---|---|
| Finance Agents | Automated invoice processing, journal anomaly resolution, intercompany reconciliation | Record-to-Report, Procure-to-Pay |
| Procurement Agents | Requisition-to-PO automation, supplier onboarding, contract renewal | Procure-to-Pay |
| HR Agents | Onboarding orchestration, benefits enrollment assistance, exit processing | Hire-to-Retire |
| Sales Agents | Lead qualification and routing, quote generation, renewal management | Lead-to-Cash |
| Service Agents | Case triage and resolution, escalation management, proactive outreach | Customer Service |
| Supply Chain Agents | Exception-based replenishment, shipment tracking escalation, demand adjustment | Plan-to-Produce |

---

## Oracle AI Agent Studio

| Capability | Description |
|---|---|
| Agent Builder | Low-code builder for custom agentic workflows within Fusion applications |
| Pre-built Agent Templates | 50+ templates covering finance, HR, SCM, CX processes |
| Guardrails & Governance | Policy-based controls for agent autonomy levels (fully automated to human-approved) |
| Multi-step Reasoning | Agents chain multiple Fusion API calls to complete complex tasks |
| Audit Trail | Full logging of agent decisions, actions, and human overrides |
| Cross-Application | Agents can orchestrate across ERP, HCM, SCM, and CX modules |

---

## OCI AI Services

| Service | Capability | Use Case |
|---|---|---|
| OCI Vision | Image classification, object detection, document analysis | Product image categorization, defect detection, document digitization |
| OCI Language | Sentiment analysis, key phrase extraction, text classification, NER | Customer feedback analysis, contract clause extraction |
| OCI Speech | Speech-to-text, real-time transcription | Call center transcription, meeting notes, voice commands |
| OCI Anomaly Detection | Multivariate anomaly detection | Equipment failure prediction, financial fraud detection |
| OCI Generative AI | LLM hosting (Cohere, Meta Llama), fine-tuning, RAG | Custom GenAI applications, document summarization, chatbots |
| OCI Data Science | ML model training, AutoML, model deployment | Custom predictive models, feature engineering, MLOps |
| OCI Digital Assistant | Conversational AI, multi-channel bots | Customer self-service, employee HR assistant |

---

## Embedded ML in Fusion Applications

| ML Capability | Where Embedded | Description |
|---|---|---|
| Adaptive Intelligent Apps | All Fusion modules | ML models trained on customer data, improving over time |
| Smart Lists | Fusion UI | AI-prioritized work lists based on predicted impact |
| Predictive Planning | EPM Cloud | ML-driven forecasting within financial planning |
| Anomaly Alerts | Fusion ERP, HCM | Proactive alerts on statistical anomalies in transactions |
| Natural Language Queries | Oracle Analytics Cloud | Ask questions in plain English across any dataset |
| Auto-Insights | Oracle Analytics Cloud | Automatically surface significant patterns and outliers |

---

## AI Capability-to-TOM Process Category Mapping

| TOM Process Category | Oracle AI Capabilities | Maturity |
|---|---|---|
| Record-to-Report | Anomaly detection, auto-reconciliation, intelligent close tasks, agentic journal processing | High |
| Order-to-Cash | Revenue estimation, order promising AI, credit scoring, delivery prediction | High |
| Procure-to-Pay | Intelligent document recognition, supplier recommendation, dynamic discounting, spend AI | High |
| Plan-to-Produce | Demand forecasting, lead time prediction, quality inspection AI, replenishment agents | High |
| Hire-to-Retire | Candidate ranking, skills advisor, attrition prediction, compensation AI, onboarding agents | High |
| Treasury & Cash Mgmt | Cash forecasting, payment anomaly detection | Medium-High |
| Lead-to-Cash | Lead scoring, win probability, next best action, renewal agents | High |
| Customer Service | Intelligent routing, answer recommendations, sentiment analysis, service agents | High |
| IT Operations | OCI Cloud Guard AI, anomaly detection, auto-remediation | Medium |
| Financial Planning | EPM Predictive Planning, scenario analysis, narrative generation | High |

---

## Licensing & AI Considerations

| Aspect | Detail |
|---|---|
| Embedded Fusion AI | Included with Fusion Cloud application subscriptions |
| AI Agent Studio | Included with Fusion Cloud (GA 2025+) |
| OCI AI Services | Consumption-based pricing (per API call / per hour) |
| OCI Generative AI | Token-based pricing for hosted LLMs |
| Data privacy | Customer data isolated; AI models trained per-tenant; no cross-tenant data sharing |
| Foundation models | Oracle partners with Cohere, Meta (Llama), and offers custom model hosting |
| Responsible AI | Oracle Responsible AI principles: fairness, accountability, transparency, privacy |
