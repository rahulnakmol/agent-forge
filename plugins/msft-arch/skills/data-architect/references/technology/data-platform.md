---
category: technology
loading_priority: 2
tokens_estimate: 4500
keywords:
  - databricks
  - fabric
  - microsoft-fabric
  - data-engineering
  - data-migration
  - data-transformation
  - data-analytics
  - olap
  - lakehouse
  - onelake
  - delta-lake
  - data-factory
  - synapse
  - etl
  - elt
  - data-visualization
version: "1.0"
last_updated: "2026-03-22"
---

# Data Platform: Databricks vs Microsoft Fabric

## Overview

When the solution requires data engineering, data migration, data transformation, data visualization, or data analytics on the Microsoft stack, choose between Azure Databricks and Microsoft Fabric. Both platforms use Delta Lake as the open storage format, enabling data interoperability between them.

## Data Platform Decision

| Capability | Azure Databricks | Microsoft Fabric |
|-----------|-----------------|-----------------|
| **Type** | PaaS on Azure (IaaS-like control) | SaaS (fully managed) |
| **Engine** | Apache Spark (managed) | Multiple engines (Spark, SQL, KQL) |
| **Storage** | Delta Lake on ADLS Gen2 | OneLake (built on ADLS Gen2) |
| **Governance** | Unity Catalog | Microsoft Purview (built-in) |
| **Data Integration** | Partner ETL or custom Spark | Data Factory (200+ connectors, Power Query) |
| **ML/AI** | MLflow, Hugging Face, custom models | Fabric Data Science, Microsoft Foundry |
| **Real-time** | Structured Streaming | Real-Time Intelligence (KQL, Event Streams) |
| **SQL Analytics** | SQL Warehouses (Photon engine) | Synapse Data Warehouse (T-SQL) |
| **BI** | Connects to Power BI | Power BI native (built-in) |
| **Pricing** | DBU-based (pay per compute) | Capacity Units (CU, reserved) |
| **Identity** | Entra ID + Unity Catalog ACLs | Entra ID + Fabric RBAC |
| **Best For** | Advanced ML, multi-cloud, heavy Spark, custom runtimes | Unified analytics SaaS, Power BI-centric, citizen data engineers |

### Decision Tree

- If your organization is Power BI-centric and wants a unified SaaS analytics platform → **Microsoft Fabric**
- If you need advanced ML pipelines, custom Spark runtimes, multi-cloud portability → **Azure Databricks**
- If you need both (common in large enterprises) → **Databricks for ML + engineering, Fabric for BI + self-service**
- Both use Delta Lake format → data can flow between them via OneLake shortcuts

---

## Microsoft Fabric Deep Dive

Fabric is a SaaS analytics platform unifying data engineering, data science, real-time analytics, and business intelligence into a single product with shared governance and a single data lake (OneLake).

### Data Factory (ETL/ELT)

- 200+ native connectors (on-prem + cloud)
- Power Query for no-code transformations
- Dataflow Gen2 for complex pipelines
- Orchestration with pipelines (schedule, trigger, dependency)
- Copy activity for bulk data movement
- Incremental refresh and change data capture support

### Data Engineering (Apache Spark)

- Notebooks (PySpark, Spark SQL, Scala, R)
- Lakehouse architecture (Delta tables + files in OneLake)
- Lakeflow Spark Declarative Pipelines for managed ETL
- Auto Loader for incremental ingestion from cloud storage
- Environment management (libraries, compute config)
- V-Order optimization for read performance on Delta tables

### Data Warehouse (T-SQL)

- Serverless SQL compute (auto-scale)
- Delta Lake native storage (open format)
- Cross-database queries across lakehouses and warehouses
- T-SQL compatibility for existing SQL skills
- Separate compute from storage (independent scaling)
- Clone tables for zero-copy testing and development

### Data Science

- MLflow integration (experiment tracking, model registry)
- Microsoft Foundry integration (pre-built models)
- Python, R, Spark ML
- Model deployment and batch scoring
- Integration with Azure Machine Learning
- Semantic Link for bridging Power BI semantic models with notebooks

### Real-Time Intelligence

- KQL (Kusto Query Language) databases
- Event Streams (Azure Event Hubs, IoT Hub, CDC sources)
- Real-time dashboards with auto-refresh
- Data Activator (event-driven actions/alerts)
- Reflexes for triggering actions on data conditions

### Power BI (Native in Fabric)

- DirectLake mode (query Delta tables directly, no import needed)
- Semantic models over OneLake data
- DAX measures, row-level security
- Power BI MCP integration for AI-assisted development
- Paginated reports, embedded analytics
- Composite models combining DirectLake with DirectQuery

### OneLake

- Single logical data lake per tenant (like OneDrive for data)
- Built on ADLS Gen2
- Shortcuts to external storage (Azure, AWS S3, GCP): no data movement
- Delta Lake format (open, columnar, versioned)
- Zero-copy access across all Fabric workloads
- Automatic governance via Microsoft Purview
- Unified namespace across all Fabric items

### Mirroring

- Continuously replicate external databases into OneLake
- Supported sources: Azure SQL, Azure Cosmos DB, Snowflake, Azure Databricks, Fabric SQL
- Near-real-time replication, no ETL pipelines needed
- Enables analytics over operational data without impacting source systems
- Change data capture (CDC) based: only changes are replicated

---

## Azure Databricks Deep Dive

Databricks on Azure provides a unified analytics platform built on Apache Spark, optimized for large-scale data engineering, machine learning, and SQL analytics.

### Lakehouse Architecture

- Delta Lake: ACID transactions, time travel, schema enforcement, Z-ordering
- Unity Catalog: centralized governance (data, AI, analytics)
- Data stored in ADLS Gen2 (customer-managed)
- Medallion architecture: Bronze (raw) → Silver (cleaned) → Gold (business-ready)

### Data Engineering

- Apache Spark (auto-tuned, managed clusters)
- Notebooks (Python, Scala, SQL, R)
- Workflows: job orchestration with dependencies, retries, alerts
- Lakeflow Declarative Pipelines: define pipelines declaratively, Databricks manages execution
- Auto Loader: incremental file ingestion from cloud storage
- Delta Live Tables: streaming + batch ETL with quality expectations
- Structured Streaming for real-time data processing

### SQL Analytics

- SQL Warehouses: serverless or classic compute for BI queries
- Photon engine: C++ native vectorized execution (10-100x faster)
- JDBC/ODBC connectivity for BI tools
- Power BI integration (DirectQuery to Databricks SQL)
- Query Federation: query external databases without data movement

### Machine Learning and AI

- MLflow: experiment tracking, model registry, deployment
- Feature Store: centralized feature management
- AutoML: automated model training and selection
- GPU clusters for deep learning (PyTorch, TensorFlow, Hugging Face)
- Model serving: real-time and batch inference endpoints
- LLM fine-tuning with DBRX, Llama, Mistral
- Vector Search for RAG applications

### Governance (Unity Catalog)

- Centralized metastore across workspaces
- Table, column, and row-level security
- Data lineage tracking
- Audit logging
- Delta Sharing: secure data sharing across organizations
- AI model governance alongside data governance

### Integration with Azure

- Azure Key Vault for secrets
- Entra ID for authentication
- VNet injection for network isolation
- Private Link endpoints
- Azure Monitor integration
- Event Hubs / IoT Hub for streaming
- OneLake shortcuts for Fabric interoperability

---

## Data Platform Architecture Patterns per Stack

### Stack A (Power Platform + Data)

- Fabric for analytics over Dataverse data
- OneLake shortcuts to Dataverse
- Power BI DirectLake for real-time dashboards
- Data Factory for external data ingestion into Fabric

### Stack B (Azure PaaS + Data)

- Fabric for self-service analytics, Power BI
- Databricks for advanced data engineering and ML
- Azure SQL / Cosmos DB for transactional data
- DuckDB for local analytical queries
- Data Factory (Fabric) or Azure Data Factory for ETL

### Stack C (Containers + Data)

- Databricks on Azure for data pipelines (Spark, Delta Lake)
- PostgreSQL on AKS for transactional data
- DuckDB embedded in containers for analytical queries
- Fabric for enterprise BI and self-service
- Streaming: Event Hubs → Databricks Structured Streaming or Fabric Real-Time Intelligence

### Stack D (D365 + Data)

- Fabric Mirroring to replicate D365 data to OneLake (no ETL)
- Azure Synapse Link for Dataverse → OneLake
- Fabric Data Warehouse for cross-system analytics
- Power BI DirectLake over D365 + operational data
- Databricks for advanced analytics over D365 data exports

---

## Data Migration Patterns

Common patterns for moving data to the Microsoft data platform:

- **Lift and shift**: Bulk copy from on-prem to ADLS Gen2/OneLake using Data Factory. Minimal transformation. Fast migration timeline.
- **Incremental migration**: Auto Loader / CDC for ongoing sync during migration. Enables parallel running of old and new systems.
- **ETL modernization**: Replace SSIS with Fabric Data Factory or Databricks Workflows. Migrate package logic to notebooks or dataflows.
- **Database migration**: Azure Database Migration Service → Azure SQL, then Fabric Mirroring for analytics. Minimal downtime with online migration mode.
- **Data warehouse migration**: Redshift/Snowflake → Fabric Data Warehouse or Databricks SQL. Use migration assistants for SQL translation.
- **Medallion pattern adoption**: Organize migrated data into Bronze (raw landing), Silver (cleaned/conformed), Gold (business-ready aggregates).

---

## Data Visualization Stack

Power BI is THE visualization platform for the Microsoft data stack. Integration paths depend on the data platform:

- **Fabric DirectLake**: Query Delta tables directly from OneLake (fastest, no import or query translation needed)
- **Databricks SQL Warehouse**: DirectQuery from Power BI to Databricks SQL endpoints
- **Import mode**: Schedule refreshes from any source (simplest, but data is not real-time)
- **Power BI Embedded**: Custom apps with TanStack React frontend using Power BI JavaScript SDK
- **Power BI MCP Server**:
  - Modeling MCP (https://github.com/microsoft/powerbi-modeling-mcp): AI-assisted semantic model creation
  - Remote MCP: Natural language DAX queries
- **Paginated reports**: Formal/regulatory reporting with precise formatting and print layout
- **Real-time dashboards (Fabric)**: Auto-refresh dashboards over streaming data in Real-Time Intelligence

---

## Effort Estimation Capability Values

When using this data platform, add these Capability values to the Effort Estimation workbook:

- **Databricks**: Databricks notebooks, Spark jobs, Unity Catalog setup, Delta Lake tables, Workflows orchestration
- **Fabric**: Fabric lakehouses, Data Factory pipelines, warehouses, semantic models, Mirroring configuration
- **Data & AI**: ML models, AI services, data science notebooks, feature engineering, model serving

---

## When to Load This Reference

Load this reference when:
- Designing data engineering or analytics solutions
- Evaluating Databricks vs Fabric for a project
- Planning data migration to the Microsoft stack
- Architecting lakehouse or data warehouse solutions
- Integrating Power BI with data platforms
- Keywords: "Databricks", "Fabric", "data engineering", "data migration", "data analytics", "lakehouse", "OneLake", "Delta Lake", "ETL", "data visualization"

## Related References

- `/references/coding-stack/preferred-stack.md` - Preferred technology stack including data tools
- `/references/technology/dynamics-specifics.md` - Dynamics 365 data integration patterns
- `/references/stack-selection/stack-overview.md` - Stack selection and combination rules
- `/references/stack-selection/stack-d-dynamics.md` - Stack D data analytics patterns
