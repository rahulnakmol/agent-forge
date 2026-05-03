---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 2600
keywords: [ai-capabilities, workday, illuminate, skills-intelligence, document-intelligence, predictive, anomaly-detection]
version: "1.0"
last_updated: "2026-03-28"
---

# Workday AI Capabilities — TOM Process Categories to Workday AI Features

## Overview

Workday's AI strategy is centered on Workday Illuminate, an embedded ML and GenAI platform trained on the largest unified dataset of HR and financial data. Key capabilities include Skills Intelligence, Document Intelligence, Anomaly Detection, and Ask Workday (natural language interface). This reference maps Workday AI capabilities to TOM process categories.

---

## Workday Illuminate — ML Platform

Illuminate is Workday's AI/ML engine embedded across all products, trained on anonymized data from 65M+ workers and trillions of transactions across the Workday customer base.

| Capability | Description | Where Applied |
|---|---|---|
| Predictive Models | ML models trained on Workday data to forecast outcomes | Retention, performance, forecasting, planning |
| Generative AI | LLM-powered content generation and summarization | Job descriptions, performance reviews, contract summaries |
| Recommendations | AI-driven suggestions based on user context | Learning, career paths, suppliers, journal corrections |
| Classification | Automated categorization of data | Expense categories, skills, job families, spend |
| Natural Language Processing | Text analysis for sentiment and entity extraction | Employee feedback (Peakon), document processing |

---

## Ask Workday — Natural Language Interface

| Capability | Description | Example Use Cases |
|---|---|---|
| Conversational Queries | Ask questions in natural language about Workday data | "What is my PTO balance?", "Show me my team's headcount by location" |
| Task Execution | Complete Workday tasks via natural language | "Submit my timesheet", "Request time off next Friday" |
| Summarization | Summarize complex Workday data | "Summarize this candidate's application", "Give me a performance review summary" |
| Guided Navigation | Direct users to relevant Workday pages | "Take me to my benefits enrollment", "Open the compensation review" |
| Manager Insights | Surface team-level insights proactively | "Which team members have overdue goals?", "Show attrition risk on my team" |

---

## Skills Intelligence

| Feature | Description | TOM Process Category |
|---|---|---|
| Skills Ontology | AI-curated taxonomy of 55,000+ skills with synonym mapping | Hire-to-Retire |
| Skills Inference | Automatically infer worker skills from job history, learning, and projects | Hire-to-Retire |
| Skills Gap Analysis | Identify skill gaps at org, team, and individual level | Hire-to-Retire |
| Talent Marketplace | AI-matched internal gigs, projects, and mentoring opportunities | Hire-to-Retire |
| Career Hub | AI-recommended career paths based on skills, interests, and adjacencies | Hire-to-Retire |
| Skills-Based Recruiting | Match candidates to roles based on skills rather than credentials | Hire-to-Retire |
| Workforce Composition | Model workforce by skills to inform strategic planning | Hire-to-Retire |

---

## Predictive Capabilities

| Prediction | Module | TOM Process Category | Description |
|---|---|---|---|
| Retention Risk (Flight Risk) | HCM Talent | Hire-to-Retire | Predict which employees are likely to leave within 12 months |
| Time-to-Fill | Recruiting | Hire-to-Retire | Predict how long a requisition will take to fill |
| Candidate Fit | Recruiting | Hire-to-Retire | Score candidates based on likelihood of success in role |
| Performance Prediction | Talent Management | Hire-to-Retire | Predict future performance based on leading indicators |
| Cash Flow Forecasting | Financial Management | Treasury | ML-based cash position predictions |
| Revenue Forecasting | Adaptive Planning | Record-to-Report | Predictive revenue modeling using historical patterns |
| Expense Prediction | Adaptive Planning | Record-to-Report | Forecast expense trends for budget planning |

---

## Anomaly Detection

| Detection Type | Module | TOM Process Category | Description |
|---|---|---|---|
| Journal Entry Anomalies | Financial Management | Record-to-Report | Flag unusual journal entries by amount, account, or timing |
| Expense Anomalies | Expenses | Procure-to-Pay | Detect policy violations, duplicates, and suspicious patterns |
| Payroll Anomalies | Payroll | Hire-to-Retire | Identify unusual payroll calculations before processing |
| Time Entry Anomalies | Time Tracking | Hire-to-Retire | Flag unusual time entry patterns (overtime spikes, scheduling conflicts) |
| Transaction Anomalies | Financial Management | Record-to-Report | Detect unusual AP/AR transaction patterns |

---

## Document Intelligence

| Capability | Module | TOM Process Category | Description |
|---|---|---|---|
| Invoice Processing | Financial Management (AP) | Procure-to-Pay | AI-powered invoice field extraction and matching |
| Receipt Processing | Expenses | Procure-to-Pay | Automated receipt scanning and expense line creation |
| Contract Analysis | Procurement | Procure-to-Pay | Extract key terms, dates, and obligations from contracts |
| Resume Parsing | Recruiting | Hire-to-Retire | Extract skills, experience, and qualifications from resumes |
| Benefits Document Processing | Benefits | Hire-to-Retire | Process life event documentation and carrier forms |

---

## AI-Powered Recommendations

| Recommendation Type | Module | Description |
|---|---|---|
| Learning Recommendations | Learning | Suggest courses based on role, skills gaps, and career goals |
| Career Path Recommendations | Career Hub | Suggest next roles based on skills adjacencies and interests |
| Mentor Matching | Talent Marketplace | Match mentors and mentees based on skills and goals |
| Supplier Recommendations | Procurement | Suggest preferred suppliers based on category and history |
| Journal Corrections | Financial Management | Suggest corrections for anomalous journal entries |
| Compensation Recommendations | Compensation | Benchmark-driven pay recommendations for merit cycles |

---

## Process Automation Candidates (AI-Augmented)

| Process | Automation Type | AI Enhancement | Expected Impact |
|---|---|---|---|
| Invoice processing (AP) | Document Intelligence + BPF | OCR extraction, auto-matching, anomaly flagging | 70-80% touchless processing |
| Expense reporting | Mobile + AI | Receipt OCR, auto-categorization, policy check | 85% automated submission |
| Employee onboarding | Orchestrations + Ask Workday | AI-guided task completion, document processing | 50% reduction in onboarding time |
| Performance reviews | Generative AI | AI-drafted review summaries, calibration insights | 40% less manager time on reviews |
| Recruiting | Skills Intelligence | Skills-based matching, time-to-fill prediction | 30% reduction in time-to-hire |
| Workforce planning | Predictive + Adaptive | Skills gap forecasting, scenario modeling | 25% improvement in plan accuracy |
| Financial close | Anomaly detection + BPF | Auto-reconciliation, anomaly flagging, close task automation | 30% reduction in close cycle |
| Payroll processing | Anomaly detection | Pre-processing validation, anomaly alerts | 90%+ payroll accuracy on first run |

---

## AI Capability-to-TOM Process Category Mapping

| TOM Process Category | Workday AI Capabilities | Maturity |
|---|---|---|
| Hire-to-Retire | Skills Intelligence, retention prediction, candidate fit, career recommendations, resume parsing | High |
| Record-to-Report | Journal anomaly detection, cash flow prediction, revenue forecasting, close automation | Medium-High |
| Procure-to-Pay | Document Intelligence (invoices, receipts), expense anomaly detection, supplier recommendations | Medium-High |
| Workforce Planning | Skills gap analysis, workforce composition modeling, headcount prediction, adaptive planning AI | High |
| Compensation & Benefits | Compensation recommendations, benchmarking AI, benefits document processing | Medium-High |
| Learning & Development | Learning recommendations, skills inference, career path suggestions | High |
| Employee Experience | Ask Workday (NL interface), Peakon sentiment analysis, proactive manager insights | High |
| Treasury & Cash Mgmt | Cash flow forecasting, transaction anomaly detection | Medium |
| Payroll | Payroll anomaly detection, pre-processing validation | Medium |

---

## Licensing & AI Considerations

| Aspect | Detail |
|---|---|
| Illuminate (base ML) | Included with Workday HCM and Financial Management subscriptions |
| Ask Workday (GenAI) | Included in HCM and Financials (rolling availability) |
| Skills Cloud | Included with Workday HCM |
| Talent Marketplace | Add-on to HCM |
| Document Intelligence | Add-on to Financial Management |
| Prism Analytics (for AI insights) | Add-on for multi-source AI analytics |
| Peakon Employee Voice | Add-on for employee engagement and sentiment AI |
| Data privacy | Workday AI trained on anonymized, aggregated data; customer data never shared across tenants |
| Foundation models | Workday partners with leading LLM providers; models fine-tuned on Workday domain data |
| Responsible AI | Workday Responsible AI framework: fairness, transparency, accountability, privacy |
