---
category: "capability-mapping"
loading_priority: 3
tokens_estimate: 1600
keywords: [fabric, power-bi, analytics, data-engineering, data-warehouse, lakehouse, real-time, kql, mdm, purview, onelake, mirroring, databricks]
version: "1.0"
last_updated: "2026-03-23"
---

# Fabric & Analytics Mapping — KPIs, Reporting & Data Management

## Overview

Maps TOM Data & Analytics layer requirements to Microsoft Fabric workloads and Power BI capabilities. Covers the full analytics spectrum from data ingestion through to executive dashboards.

---

## KPI Dashboards — Power BI with DirectLake

| TOM Requirement | Fabric/Power BI Solution | Implementation Pattern |
|---|---|---|
| Executive scorecard | Power BI report over Fabric Lakehouse (DirectLake) | Lakehouse stores curated KPI tables; DirectLake semantic model for sub-second query; Power BI dashboard with RLS per business unit |
| Department KPI tracking | Power BI app workspace per domain | Finance, HR, SCM, Procurement each get dedicated workspace; shared certified datasets; composite models for cross-domain |
| Real-time KPI monitoring | Power BI + Fabric Real-Time Intelligence | KQL database for streaming data; Real-Time Dashboard for live metrics; alerts via Data Activator |
| Self-service exploration | Power BI Desktop + shared semantic models | Business analysts connect to published semantic models; create personal reports; promote to certified via governance flow |
| Mobile dashboards | Power BI Mobile app | Optimized mobile layouts; push notifications on data-driven alerts |

---

## Operational Reporting — Paginated Reports

| TOM Requirement | Solution | Implementation Pattern |
|---|---|---|
| Financial statements | Power BI Paginated Reports | Pixel-perfect multi-page reports; parameter-driven (entity, period, currency); export to PDF/Excel |
| Regulatory reports | Paginated Reports + D365 Electronic Reporting | ER for D365-native regulatory formats; Paginated Reports for custom regulatory submissions |
| Invoice / statement printing | Paginated Reports | Mail-merge style document generation; scheduled delivery via subscriptions |
| Operational lists | Paginated Reports or Power BI tables | Paginated for print-ready; Power BI for interactive filtering |
| Report subscriptions | Power BI subscriptions + Power Automate | Scheduled email delivery; Power Automate for conditional distribution (e.g., send only if KPI breached) |

---

## Data Warehousing — Fabric Data Warehouse

| TOM Requirement | Fabric Solution | Implementation Pattern |
|---|---|---|
| Enterprise data warehouse | Fabric Data Warehouse (T-SQL) | Star/snowflake schema; T-SQL for transformations; cross-database queries within Fabric |
| Domain data marts | Fabric Lakehouse per domain | Finance lakehouse, HR lakehouse, SCM lakehouse; Delta tables; Spark notebooks for transformation |
| Semantic layer | Fabric Semantic Models (formerly Power BI datasets) | Centralized business logic (measures, hierarchies, relationships); DirectLake for performance |
| Historical data archive | Fabric Lakehouse (cold tier) | OneLake shortcut to ADLS for cold storage; lifecycle policies for cost optimization |

---

## Data Engineering — Fabric Spark & Databricks

| TOM Requirement | Primary Solution | Alternative | When to Choose |
|---|---|---|---|
| ETL/ELT pipelines | Fabric Data Factory (pipelines + dataflows) | Azure Data Factory | Fabric DF for OneLake-native; ADF for Azure-native or hybrid scenarios |
| Complex transformations | Fabric Spark Notebooks (PySpark/Spark SQL) | Azure Databricks | Fabric Spark for unified platform; Databricks for advanced ML, Delta Live Tables, Unity Catalog |
| Data quality | Fabric Spark + Great Expectations / dbt | Databricks with dbt | Fabric for integrated experience; Databricks for mature data engineering teams |
| Medallion architecture | Fabric Lakehouse (Bronze → Silver → Gold) | Databricks Lakehouse | Bronze: raw ingestion; Silver: cleansed/conformed; Gold: business-ready aggregates |
| Streaming ETL | Fabric Spark Structured Streaming | Databricks Structured Streaming | Real-time data transformation from Event Hub / Kafka into lakehouse |

### Medallion Architecture in Fabric

```
Bronze (Raw)          Silver (Cleansed)       Gold (Business-Ready)
─────────────         ─────────────────       ────────────────────
D365 F&O mirror  ──→  Conformed entities  ──→  Finance KPI aggregates
D365 CE mirror   ──→  Unified customer    ──→  Sales performance cubes
External files   ──→  Validated records   ──→  Operational dashboards
IoT streams      ──→  Enriched events     ──→  Real-time analytics
```

---

## Master Data Management — OneLake & Purview

| TOM Requirement | Solution | Implementation Pattern |
|---|---|---|
| Passive MDM (virtual) | Fabric OneLake + Shortcuts | OneLake as single copy of truth; shortcuts to source systems; no data movement |
| Active MDM | Profisee on Azure (or Informatica) | Golden record management; match/merge/survivorship; stewardship workflows; publish to D365 via integration |
| Data catalog | Microsoft Purview Data Catalog | Discover, classify, and tag data assets across D365, Fabric, Azure, on-premises |
| Data lineage | Purview + Fabric lineage | End-to-end lineage from source (D365) through transformation (Fabric) to consumption (Power BI) |
| Data classification | Purview sensitivity labels | Auto-classify PII, financial data, health data; propagate labels to Power BI |
| Data quality monitoring | Purview Data Quality (preview) | Data quality rules, profiling, scorecards across OneLake and external sources |

---

## Real-Time Analytics — Fabric Real-Time Intelligence

| TOM Requirement | Solution | Implementation Pattern |
|---|---|---|
| Streaming ingestion | Eventstream (from Event Hub, Kafka, custom sources) | Low-latency ingestion into KQL database; no-code stream processing |
| Real-time querying | KQL Database | Kusto Query Language for time-series, anomaly detection, pattern analysis |
| Real-time dashboards | Real-Time Dashboard | Auto-refresh dashboards on KQL data; tile-based with parameters |
| Alerting | Data Activator (Reflex) | Trigger actions (Power Automate, email, Teams) when data conditions are met |
| IoT analytics | Eventstream + KQL | Device telemetry ingestion, time-series analysis, anomaly detection |

---

## Data Ingestion — Fabric Data Factory & Mirroring

| TOM Source | Ingestion Method | Latency | Notes |
|---|---|---|---|
| D365 Finance & Operations | Fabric Mirroring | Near-real-time (minutes) | Preferred method; incremental sync of F&O tables to OneLake Delta tables |
| D365 Customer Engagement | Fabric Link for Dataverse | Near-real-time (minutes) | Syncs Dataverse tables to OneLake; replaces Synapse Link |
| Azure SQL / SQL Server | Fabric Mirroring | Near-real-time (minutes) | CDC-based incremental replication |
| On-premises databases | Fabric Data Factory + on-prem gateway | Scheduled (minutes-hours) | Gateway for secure on-prem connectivity |
| Files (CSV, Parquet, JSON) | Fabric Data Factory / OneLake shortcuts | Scheduled or on-arrival | Shortcuts for no-copy access; pipelines for transformation |
| External APIs | Fabric Data Factory (REST connector) | Scheduled | Parameterized API calls with pagination |
| Streaming sources | Eventstream (Event Hub, Kafka) | Real-time (seconds) | For IoT, clickstream, transaction streams |

---

## TOM Data & Analytics Layer — Reference Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Consumption Layer                         │
│  Power BI Dashboards │ Paginated Reports │ Excel │ Copilot      │
├─────────────────────────────────────────────────────────────────┤
│                      Semantic Model Layer                        │
│         DirectLake Models │ Composite Models │ XMLA             │
├─────────────────────────────────────────────────────────────────┤
│                        Gold (Business-Ready)                     │
│     Fabric DW (T-SQL) │ Lakehouse (Delta) │ KQL Database        │
├─────────────────────────────────────────────────────────────────┤
│                      Silver (Cleansed/Conformed)                 │
│              Fabric Spark Notebooks │ Dataflows Gen2             │
├─────────────────────────────────────────────────────────────────┤
│                        Bronze (Raw Ingestion)                    │
│  Mirroring │ Fabric Link │ Data Factory │ Eventstream │ Shortcut│
├─────────────────────────────────────────────────────────────────┤
│                         OneLake (Storage)                        │
│                    Delta/Parquet │ Governance (Purview)          │
├─────────────────────────────────────────────────────────────────┤
│                          Source Systems                           │
│  D365 F&O │ D365 CE │ Azure SQL │ APIs │ Files │ IoT Streams   │
└─────────────────────────────────────────────────────────────────┘
```

### Governance Considerations

| Aspect | Recommendation |
|---|---|
| Workspace strategy | One workspace per domain per environment (e.g., Finance-Prod, Finance-Dev) |
| Capacity management | Fabric capacity per environment tier (F64 prod, F32 non-prod); auto-scale for burst |
| Access control | Workspace roles (Admin, Member, Contributor, Viewer) + item-level permissions + RLS in semantic models |
| Lineage & impact analysis | Purview integration for end-to-end lineage; impact analysis before schema changes |
| Cost optimization | Monitor CU consumption; pause/resume capacity for non-prod; use OneLake shortcuts to avoid data duplication |
