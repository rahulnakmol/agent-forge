---
category: coding-stack
loading_priority: 1
tokens_estimate: 4500
keywords:
  - technology stack
  - coding standards
  - .NET
  - TypeScript
  - TanStack
  - Python
  - Go
  - Terraform
  - Kubernetes
  - PostgreSQL
  - Azure SQL
  - SQLite
  - DuckDB
  - Power BI
  - Databricks
  - Microsoft Fabric
  - Azure Data Platform
  - data platform
  - functional programming
  - domain-driven design
  - preferred stack
  - implementation guidance
  - managed instance
  - database as a service
version: "2.0"
last_updated: "2026-03-22"
---

# Preferred Pro Coding Stack

## Overview

When generating tech-design-first specs (design.md) or providing implementation guidance, Odin uses this preferred technology stack. These are priorities: the skill recommends these first but adapts to client requirements.

The stack is organized into four tiers: **Application**, **Data**, **Infrastructure**, and **Cross-Cutting**.

---

## Application Tier

### 1. .NET with C# (LTS Versions Only)

- **Use for**: Enterprise APIs, microservices, backend services, Azure Functions, D365 F&O plugins (X++/C#), D365 CE plugins (C#)
- **Target**: .NET 8 LTS (or latest LTS at time of design)
- **Patterns**: Minimal APIs, Clean Architecture, CQRS with MediatR, Vertical Slice Architecture
- **Functional paradigm**: Prefer immutable records, pattern matching, discriminated unions (OneOf), Result<T> pattern over exceptions
- **DDD**: Rich domain models, value objects as records, domain events via MediatR
- **Testing**: xUnit, FluentAssertions, NSubstitute, Testcontainers for integration tests, Verify for snapshot tests
- **Key packages**: MediatR, FluentValidation, Mapster, Polly (resilience), Serilog, Entity Framework Core
- **When to use Go instead**: Pure system tooling with no business domain logic, extreme concurrency requirements, infrastructure agents

### 2. TypeScript with Bun

- **Use for**: Agent development, serverless functions, CLI tools, scripting, automation, edge functions
- **Runtime**: Bun (preferred for speed + built-in bundler/test runner) or Node.js LTS (fallback for enterprise compatibility)
- **Patterns**: Functional core / imperative shell, Effect-TS for complex workflows, Zod for validation
- **Agent development**: Anthropic SDK, Azure OpenAI SDK, LangChain.js, Semantic Kernel JS, Vercel AI SDK
- **Key packages**: Zod, Effect, ts-pattern (pattern matching), neverthrow (Result type), drizzle-orm
- **When NOT to use**: Heavy compute workloads (use .NET or Go), ML pipelines (use Python)

### 3. TanStack for All Frontend UI Development

- **Framework**: React (primary) or Solid (secondary)
- **Core libraries** (use ALL of these as a cohesive stack):
  - **TanStack Router**: Type-safe routing with URL-based state management, file-based routes, search params serialization
  - **TanStack Query**: Server state management, caching, deduplication, optimistic updates, infinite scroll
  - **TanStack Table**: Headless data grids with sorting, filtering, grouping, pagination, column resizing, virtual scrolling
  - **TanStack Form**: Type-safe form state with validation, field arrays, async validation, form-level errors
  - **TanStack Virtual**: Virtualization for large lists and grids (60 FPS at 100K+ rows)
  - **TanStack Store**: Framework-agnostic reactive state for cross-component state
  - **TanStack Start** (RC): Full-stack React framework with SSR, streaming, server functions
- **UI approach**: Motion-driven UI, agentic experience design (conversational + visual), progressive disclosure, skeleton loading
- **Styling**: Tailwind CSS v4 with CSS custom properties for design tokens
- **Animation**: Framer Motion (React) or Motion One for scroll-driven, layout, and shared-element animations
- **Build**: Vite with Bun as package manager and test runner
- **Testing**: Vitest (unit), Testing Library (component), Playwright (E2E)
- **Agentic UI patterns**: Streaming responses, tool-call visualization, artifact rendering, chat + canvas layouts

### 4. Python with Type Safety and Performance

- **Use for**: Data engineering, analytics, ML pipelines, data science, Databricks notebooks, Fabric notebooks
- **Python version**: 3.12+ (latest stable)
- **Type safety**: Strict mypy, Pydantic v2 for runtime validation, beartype for runtime type checking
- **Performance**: Polars (preferred over pandas; 10-100x faster), asyncio, uvloop, multiprocessing
- **Data engineering**: Polars, DuckDB, Apache Arrow, Delta Lake (delta-rs), PySpark (Databricks/Fabric)
- **ML/AI**: scikit-learn, PyTorch, Hugging Face Transformers, MLflow
- **API**: FastAPI with Pydantic models (when Python API is needed; prefer .NET for enterprise APIs)
- **Testing**: pytest, hypothesis (property-based testing), Great Expectations (data quality)
- **Key packages**: Polars, Pydantic, FastAPI, DuckDB, httpx, delta-rs

### 5. Go for System Programming

- **Use for**: High-performance system tools, network services, infrastructure agents, CLI tools, Kubernetes operators
- **Patterns**: Interface-driven design, error handling with explicit returns, goroutines + channels for concurrency
- **Key libraries**: cobra (CLI), viper (config), zerolog (logging), testify (testing), chi (HTTP router)
- **Build**: Standard Go toolchain, ko for container images, goreleaser for releases
- **When to use over .NET**: Infrastructure tooling, Kubernetes operators/controllers, tools that must compile to a single static binary

### 6. X++ for Dynamics 365 F&O

- **Use for**: D365 Finance & Operations customization and extension ONLY
- **IDE**: Visual Studio with Dynamics 365 development tools
- **Extension model**: Chain of Command (`[ExtensionOf]`); never overlayer
- **Key patterns**: Data entities (OData), business events, SysOperation framework, Electronic Reporting
- **Build/deploy**: Azure DevOps → CI/CD → LCS (Lifecycle Services) → environments
- **Testing**: SysTest framework, RSAT (Regression Suite Automation Tool)
- **Reference**: `references/technology/dynamics-specifics.md` for full X++ guidance

---

## Data Tier

### 7. Database Strategy (OLTP)

The database choice depends on the stack, workload type, and deployment model:

| Database | Type | Use When | Stack Alignment |
|----------|------|----------|-----------------|
| **Azure SQL Database** | PaaS (DBaaS) | Enterprise OLTP, D365 integration, SQL Server compatibility | Stack A, B, D |
| **Azure SQL Managed Instance** | PaaS (near-IaaS) | SQL Server migration, cross-database queries, CLR, linked servers, SQL Agent | Stack B, D (legacy migration) |
| **PostgreSQL (Azure)** | PaaS or AKS | Open-source OLTP, pgvector for AI embeddings, PostGIS for geo, jsonb for semi-structured | Stack B, C |
| **SQLite** | Embedded | Simple bespoke apps, local-first, edge/mobile, prototyping, single-user tools | Stack A, B (simple apps) |
| **Cosmos DB** | PaaS (NoSQL) | Global distribution, multi-model (doc/graph/key-value), sub-10ms latency | Stack B, C |
| **Dataverse** | SaaS (Power Platform) | D365 CE data, Power Platform apps, low-code data layer | Stack A, D |

**Azure SQL Database (DBaaS)**: the default for enterprise OLTP on Azure:
- Elastic pools for multi-tenant cost optimization
- Geo-replication and auto-failover groups for DR
- Serverless tier for intermittent workloads (auto-pause, auto-scale)
- Hyperscale tier for databases up to 100 TB
- Transparent data encryption (TDE), Always Encrypted for sensitive columns
- Azure Defender for SQL (threat detection, vulnerability assessment)
- T-SQL compatibility: near-100% with SQL Server on-premises

**Azure SQL Managed Instance**: when you need full SQL Server engine compatibility:
- Cross-database queries and distributed transactions
- SQL Server Agent for job scheduling
- CLR integration for custom .NET functions in-database
- Service Broker for async messaging
- Linked servers for hybrid connectivity to on-premises
- Migration path: Azure Database Migration Service (DMS) for online migration from SQL Server
- **Use for**: Lift-and-shift SQL Server migrations, apps that use SQL Server-specific features not in Azure SQL DB

**PostgreSQL on Azure**:
- Azure Database for PostgreSQL Flexible Server (preferred PaaS)
- PostgreSQL on AKS (when full control needed, or operator pattern with CloudNativePG)
- Extensions: pgvector (AI embeddings), PostGIS (geospatial), pg_cron (scheduling), TimescaleDB (time-series)
- Connection: PgBouncer for connection pooling (built into Azure Flexible Server)

**SQLite**: for simple, bespoke, single-user applications:
- Embedded in-process database, zero configuration, zero server
- Use for: CLI tools, mobile/desktop apps, prototyping, test harnesses, configuration stores
- Libraries: better-sqlite3 (TypeScript/Bun), Microsoft.Data.Sqlite (.NET), sqlite3 (Python)
- **When NOT to use**: Multi-user concurrent write workloads, distributed systems, anything needing network access
- Turso/libSQL for edge-distributed SQLite (when needed)

**ORM / Data Access**:
- **C#**: Entity Framework Core (migrations, LINQ, change tracking) or Dapper (raw SQL performance)
- **TypeScript**: Drizzle ORM (type-safe, SQL-like) or Prisma (schema-first, migrations)
- **Python**: SQLAlchemy (ORM + Core), or raw SQL with asyncpg/psycopg3
- **Go**: sqlc (compile SQL to type-safe Go) or GORM

### 8. Database Strategy (OLAP / Analytics)

| Database | Type | Use When |
|----------|------|----------|
| **DuckDB** | Embedded columnar | Local analytics, data transformation, ad-hoc queries, in-process OLAP |
| **Fabric Data Warehouse** | SaaS (T-SQL) | Enterprise analytics, cross-system reporting, Power BI DirectLake |
| **Databricks SQL Warehouse** | PaaS | Advanced analytics, Photon engine, Unity Catalog governed queries |
| **Azure Synapse Serverless** | PaaS | Ad-hoc queries over Parquet/Delta in ADLS (pay-per-query) |

**DuckDB**: the default for local/embedded analytical queries:
- Embedded columnar database, SQL interface, zero dependencies
- Reads Parquet, CSV, JSON, Delta Lake directly (no ETL needed)
- In-process: runs inside Python, TypeScript, .NET, Go, or CLI
- Use for: data transformation in CI/CD, local development analytics, testing data pipelines, ad-hoc exploration
- Integration: Python (polars + duckdb), TypeScript (duckdb-wasm for browser analytics), .NET (DuckDB.NET)
- **Scales to**: ~100 GB single-node (beyond that → Fabric or Databricks)

### 9. Azure Data Platform: Microsoft Fabric

**Use for**: ALL enterprise data engineering, data migration, data transformation, data analytics, OLAP on the Microsoft SaaS stack

Microsoft Fabric is the unified analytics platform. Use as the default data platform when:
- Organization is Power BI-centric or D365-centric
- Need unified governance (Purview built-in)
- Citizen data engineers alongside pro data engineers
- Cross-system analytics (D365 + external + operational data)

**Fabric workloads**:
- **Data Factory**: 200+ connectors, Power Query, pipeline orchestration (ETL/ELT)
- **Data Engineering**: Spark notebooks (PySpark, Spark SQL, Scala, R), Lakehouse (Delta tables + files)
- **Data Warehouse**: T-SQL analytics, serverless compute, Delta Lake native storage
- **Data Science**: MLflow, Microsoft Foundry, experiment tracking, model deployment
- **Real-Time Intelligence**: KQL databases, Event Streams, Data Activator alerts
- **Power BI**: DirectLake (query Delta tables directly), semantic models, DAX
- **OneLake**: Centralized logical data lake (ADLS Gen2), shortcuts to external storage, zero-copy access
- **Mirroring**: Near-real-time replication from Azure SQL, Cosmos DB, Databricks, D365 F&O, Snowflake

**Patterns**: Lakehouse architecture, Medallion (Bronze → Silver → Gold), Delta Lake format everywhere

### 10. Azure Data Platform: Databricks

**Use for**: Advanced data engineering, complex ML pipelines, multi-cloud data strategy

Use Databricks when:
- Advanced ML (custom models, GPU training, LLM fine-tuning)
- Heavy Spark engineering with custom runtimes
- Multi-cloud portability (same platform on Azure, AWS, GCP)
- Organization already standardized on Databricks

**Key capabilities**: Unity Catalog governance, Delta Lake, MLflow, Photon SQL engine, Auto Loader, Workflows, Lakeflow Declarative Pipelines

**Fabric + Databricks together** (common in large enterprises):
- Databricks for data engineering + ML
- Fabric for self-service analytics + Power BI
- Data flows between them via OneLake shortcuts (both use Delta Lake format)

### 11. Power BI for All Visualizations

- **Use for**: ALL dashboard, reporting, and visualization needs
- **Power BI MCP Servers** for AI-assisted development:
  - **Modeling MCP** (https://github.com/microsoft/powerbi-modeling-mcp): Create/modify semantic models
  - **Remote MCP**: Natural language DAX queries, schema-aware query generation
- **Connection modes**:
  - **DirectLake** (Fabric): Fastest; queries Delta tables directly, no import or DirectQuery
  - **DirectQuery** (Azure SQL, Databricks SQL): Real-time, no data movement
  - **Import**: Scheduled refresh, best for complex transformations
- **Patterns**: Star schema modeling, DAX measures, row-level security (RLS), object-level security (OLS)
- **Embedded**: Power BI Embedded for custom apps (React/TanStack SDK)
- **Governance**: Endorsed datasets, data lineage, sensitivity labels, deployment pipelines
- **Paginated reports**: For formal/regulatory/printed reports with exact layout control

---

## Infrastructure Tier

### 12. Terraform for All Infrastructure as Code

- **Use for**: ALL Azure workload deployments, packaging, infrastructure provisioning
- **Provider**: azurerm (Azure), azuread (Entra ID), databricks (Databricks workspaces)
- **Patterns**: Module composition, remote state in Azure Storage, workspace-per-environment
- **Structure**: `modules/` (reusable) + `environments/` (dev/staging/prod) + `shared/` (networking, identity)
- **Alternatives acknowledged**: Bicep (Azure-native, simpler but less portable, no multi-cloud)
- **Testing**: Terratest, terraform validate, tflint, checkov (security scanning), OPA/Rego for policy
- **CI/CD**: GitHub Actions or Azure DevOps with plan → approve → apply workflow

### 13. Kubernetes Native for Services

- **Platform**: AKS (Azure Kubernetes Service), always preferred
- **Manifests**: Kustomize for environment overlays, Helm for third-party charts
- **GitOps**: Flux v2 (preferred) or ArgoCD
- **Service mesh**: Istio (when needed for mTLS, traffic management, observability)
- **Observability**: Prometheus + Grafana (metrics), Jaeger/Tempo (tracing), Fluent Bit → Azure Monitor (logs)
- **Scaling**: KEDA for event-driven autoscaling, HPA for CPU/memory, VPA for right-sizing
- **Security**: Pod security standards, workload identity (no service account keys), Key Vault CSI driver
- **Alternative**: Azure Container Apps (when full K8s is overkill; simpler serverless containers with DAPR built-in)

### 14. UNIX/Linux Native Solutions

- **Shell**: Bash/Zsh scripts for automation, GNU coreutils, jq for JSON, yq for YAML
- **Container base**: Alpine Linux (minimal, security) or Ubuntu LTS (full-featured, dev)
- **Principles**: Everything is a file, pipe composition, small sharp tools, 12-factor app methodology
- **Scheduling**: Cron, systemd timers; Azure Container Apps jobs for cloud scheduling
- **Tooling**: curl, httpie, ripgrep, fd, bat, fzf (modern UNIX replacements)

---

## Cross-Cutting Concerns

### Functional Programming Paradigm

Across ALL languages, prefer:

- **Immutable data**: records, readonly, const, frozen dataclasses
- **Pure functions**: Business logic as pure functions; side effects at boundaries only
- **Pattern matching**: Over if/else chains (C# switch expressions, ts-pattern, Python match)
- **Result/Either types**: Over exceptions for expected failures (OneOf in C#, neverthrow in TS, Result in Rust/Go)
- **Composition over inheritance**: Compose small functions, not deep class hierarchies
- **Algebraic data types**: Discriminated unions (C#), tagged unions (TS), sealed classes (Kotlin)
- **Higher-order functions**: map, filter, reduce; avoid imperative loops for data transformation

### Domain-Driven Design Priorities

- **Bounded contexts**: Aligned to team/domain boundaries, own their data and schema
- **Rich domain models**: Behavior + data together (not anemic models)
- **Value objects**: Domain primitives as value types (Email, Money, OrderId, Quantity)
- **Domain events**: Cross-context communication (publish/subscribe, event sourcing)
- **Anti-corruption layers**: At context boundaries; translate external models to internal
- **Repository pattern**: Aggregate persistence, never expose ORM outside domain
- **Specification pattern**: Composable query predicates for complex filters

---

## Stack Selection Matrix

| Use Case | Primary | Secondary | Database |
|----------|---------|-----------|----------|
| Enterprise API | .NET C# | Go | Azure SQL / PostgreSQL |
| Frontend UI | TanStack + React | TanStack + Solid | (none) |
| Agent / Copilot | TypeScript + Bun | Python | SQLite (local state) |
| D365 F&O Extension | X++ (Visual Studio) | .NET C# (plugins) | F&O SQL (managed) |
| D365 CE Plugin | .NET C# | (none) | Dataverse |
| Data Pipeline | Python + Polars | PySpark (Databricks/Fabric) | DuckDB (local) / Fabric Warehouse |
| ML / AI | Python + PyTorch | Databricks ML | Databricks / Fabric |
| System Tool / CLI | Go | .NET (global tool) | SQLite |
| Simple Bespoke App | TypeScript + Bun | .NET | SQLite |
| IaC | Terraform | Bicep (Azure-only) | (none) |
| Container Platform | AKS + Flux | Container Apps | (none) |
| OLTP (enterprise) | (none) | (none) | Azure SQL (DBaaS) / SQL MI |
| OLTP (open-source) | (none) | (none) | PostgreSQL (Flexible Server / AKS) |
| OLTP (simple/local) | (none) | (none) | SQLite |
| OLAP (local) | (none) | (none) | DuckDB |
| OLAP (enterprise) | (none) | (none) | Fabric Warehouse / Databricks SQL |
| Data Platform (SaaS) | Microsoft Fabric | (none) | OneLake + Delta Lake |
| Data Platform (PaaS) | Azure Databricks | Fabric | Unity Catalog + Delta Lake |
| Data Migration | Fabric Data Factory | Databricks Auto Loader | (none) |
| Visualization | Power BI | TanStack Table (custom) | (none) |

---

## AWS-to-Azure Conversion

This stack can convert any AWS-specific design to Azure-native. → Read `references/coding-stack/aws-to-azure.md` for the full 60+ service mapping.
