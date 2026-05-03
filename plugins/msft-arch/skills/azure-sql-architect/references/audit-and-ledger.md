# Audit and Ledger

**Applies to**: Azure SQL Database, Azure SQL Managed Instance, SQL Server 2022+ (ledger).

> Codified opinion: Audit + Ledger for regulated workloads.

Two distinct controls for two distinct questions. Audit answers "what happened on this database": who connected, what they ran, what schema changed. Ledger answers "is the data in this table the same data we wrote": tamper-evidence on the row level, cryptographically verifiable.

Use both for HIPAA, PCI, SOX, FedRAMP, and most "regulated" workloads. Use audit alone for general-purpose production logging; reach for ledger when integrity-of-record is the regulatory ask.

## Auditing

### Destinations

| Destination | When |
|---|---|
| Log Analytics workspace | Default. Enables KQL queries, alerts, and integration with Sentinel via `/security-architect`. Pair with App Insights data for end-to-end traces. |
| Storage account (Blob) | Long-term retention beyond Log Analytics retention; immutable container policies for tamper-evidence on the audit log itself. |
| Event Hubs | Stream to a third-party SIEM. Pairs cleanly with Sentinel ingestion if the SIEM is Sentinel-adjacent. |

Multi-destination is supported and is the right answer for regulated workloads: Log Analytics for query speed, Storage for retention, optionally Event Hubs for SIEM streaming.

### Configuration baseline (Azure SQL Database)

Enable server-level audit (covers all databases) plus database-level audit overrides only when a specific database needs different policy.

```sql
-- Database-level audit specification (run on user database)
CREATE DATABASE AUDIT SPECIFICATION AuditPII
FOR SERVER AUDIT [Default]
ADD (SELECT, INSERT, UPDATE, DELETE ON SCHEMA::pii BY public),
ADD (SCHEMA_OBJECT_CHANGE_GROUP),
ADD (DATABASE_PRINCIPAL_CHANGE_GROUP)
WITH (STATE = ON);
```

What to capture at minimum:

- All DDL on production schemas (`SCHEMA_OBJECT_CHANGE_GROUP`).
- All login events (`SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP`, `FAILED_DATABASE_AUTHENTICATION_GROUP`).
- Permission changes (`DATABASE_PERMISSION_CHANGE_GROUP`, `DATABASE_PRINCIPAL_CHANGE_GROUP`).
- Selects on tables containing PII or PHI.

Avoid capturing every SELECT on every table: cost balloons and signal-to-noise drops. Scope audit to PII-containing schemas.

### Retention

Log Analytics: align with your regulatory retention floor (1 year is common; 7 years for SOX). Storage: lifecycle policy moves blobs to Cool then Archive tiers based on age; immutability policy locks the retention window.

Hand off to `/finops-architect` for cost validation: long retention in Log Analytics is expensive; tiered Storage is the cost lever.

## Ledger

Ledger provides cryptographic tamper-evidence at the row level using a Merkle-tree of SHA-256 hashes, with periodic database digests stored outside the database in tamper-proof storage.

### Two ledger table modes

| Mode | When |
|---|---|
| Updatable ledger tables | System-of-record patterns where rows do change (customer records, orders, positions). Each update writes a history row; the ledger view joins current and history. |
| Append-only ledger tables | Insert-only patterns: SIEM events, immutable audit trails, financial transactions, blockchain mirroring. UPDATE and DELETE blocked at the API level. |

Ledger database (whole-database ledger) is the right default for regulated workloads where every table must be tamper-evident: every table created in a ledger database is an updatable ledger table by default unless created with `APPEND_ONLY = ON`.

```sql
-- Updatable ledger table
CREATE TABLE Customers (
    CustomerId      uniqueidentifier NOT NULL,
    Email           nvarchar(256) NOT NULL,
    -- ...
)
WITH (
    SYSTEM_VERSIONING = ON,
    LEDGER = ON
);

-- Append-only ledger table for an immutable audit feed
CREATE TABLE AuditEvents (
    EventId         bigint IDENTITY(1,1) NOT NULL,
    OccurredAt      datetime2 NOT NULL,
    Payload         nvarchar(max) NOT NULL
)
WITH (LEDGER = ON (APPEND_ONLY = ON));
```

### Database digests

The hash chain culminates in a database digest. Configure automatic digest storage to a tamper-proof destination:

| Digest destination | When |
|---|---|
| Azure Blob Storage with immutability policy (time-based retention, allow protected append blob writes) | Default. Lock the policy after creation; do not use LRS-only accounts for digest containers (per current Microsoft docs). |
| Azure Confidential Ledger | Strongest tamper-evidence on the digest itself; appropriate when the regulatory regime demands provable digest integrity (verify current capabilities with `microsoft_docs_search`). |

Manual digest storage is supported but is operationally fragile. Prefer automatic.

### Verification cadence

Verification recomputes hashes and compares to the stored digests. Schedule it: weekly is a reasonable floor for production, daily for high-sensitivity workloads.

```sql
EXEC sys.sp_verify_database_ledger
    @digest_locations = N'[{"path":"https://<account>.blob.core.windows.net/sqldbledgerdigests","object_type":"AzureBlobStorage"}]';
```

Wire the verification call into a scheduled job (Azure Automation, Logic App on a timer, or a runbook) and route failures to the security on-call channel.

### Ledger limitations to surface in the ADR

- Existing non-ledger tables cannot be converted in place; data must be migrated.
- A ledger table cannot be reverted to a non-ledger table; this is by design.
- TRUNCATE TABLE not supported; aging-out append-only ledger data is constrained.
- In-memory tables, sparse column sets, FileTable, graph table, full-text indexes, transactional replication, database mirroring: not supported on ledger tables. SWITCH IN/OUT not supported (rules out date-partitioned sliding window archival on a ledger table).
- A transaction can update up to 200 ledger tables (current cap; verify with `microsoft_docs_search`).
- Azure Synapse Link is supported on the ledger table itself, not on the history table.

These limitations push some workloads toward audit-only. Apply ledger to the tables where integrity-of-record is the regulatory ask, not blanket-on across the database.

## Decision summary

- General production: Audit on (Log Analytics + Storage). No ledger.
- Regulated workload, system-of-record table: Audit + updatable ledger table on the system-of-record table; verify digests weekly.
- Regulated workload, immutable event stream: Audit + append-only ledger table; verify digests daily; route digests to immutable Blob with locked policy or Confidential Ledger.
- Regulated workload, every table is integrity-sensitive: ledger database with audit.

Hand off SIEM integration and Defender for SQL configuration to `/security-architect`.
