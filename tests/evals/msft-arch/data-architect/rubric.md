Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Medallion Architecture Correctness** — Recommends bronze/silver/gold medallion structure for data organization. Bronze is raw ingestion, silver is cleansed/conformed, gold is business-ready aggregates. Never recommends exposing raw data directly to consumers. Score 5 if medallion layers are correctly designed and applied; 1 if raw data is exposed or layers are incorrectly structured.

2. **Platform Selection Rationale** — Applies correct platform selection: Microsoft Fabric for unified analytics and Microsoft-standardizing orgs; Azure Databricks for advanced ML/AI, Unity Catalog, or multi-cloud; DuckDB for embedded/local analytics. Score 5 if platform selection is well-reasoned against the stated requirements; 1 if platform is recommended without justification.

3. **DirectLake over Import Principle** — For Fabric scenarios, recommends DirectLake mode for Power BI semantic models (zero-copy analytics from lakehouse) rather than Import or DirectQuery. Score 5 if DirectLake is correctly recommended with explanation of the zero-copy benefit; 1 if Import or DirectQuery is recommended without clear justification.

4. **Data Governance Design** — Addresses Purview integration for classification, lineage, and access control. Covers sensitivity labels, row-level security, and object-level security. Recommends governing before loading production data. Score 5 if governance is comprehensive and integrated from the start; 1 if governance is omitted or treated as an afterthought.

5. **Incremental Pipeline Design** — Designs pipelines for incremental processing with retry/error handling, not full refresh by default. Addresses partitioning strategy, Delta Lake versioning for reliability, and capacity sizing. Score 5 if pipeline design is operationally sound; 1 if full refresh is recommended without justification or pipeline resilience is ignored.
