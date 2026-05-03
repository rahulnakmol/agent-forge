# Partitioning Strategies

**Applies to**: Azure SQL Database, Azure SQL Managed Instance, Azure SQL Edge, SQL Server on Azure VM.

> Codified opinion: Partition by date (most common) or tenant (multi-tenant). Never by random hash.

Two partition strategies are correct for ~95% of OLTP and audit workloads on Azure SQL: date-based sliding window for time-series and audit data, and tenant-id partitioning for multi-tenant SaaS. A third strategy (hash partitioning on a synthetic key) is almost always wrong and is called out below.

## Date partitioning (sliding window)

Use for: audit logs, telemetry, orders, events, ledgers, transactional history that ages out.

The pattern:

1. Choose granularity matching the archival cadence: monthly is the default, daily for very high-volume workloads, yearly for low-volume long-retention data.
2. Pre-create future partitions: always at least 3 ahead of "now" so an automated job that fails does not break inserts.
3. Pre-create empty staging tables matching the partition schema for switch-out.
4. On the rolling cadence: switch out the oldest partition into a staging table, archive it (Blob Storage cool tier, Parquet, or a Fabric / Databricks lakehouse via `/data-architect`), then drop the staging table and merge the empty boundary.

Example skeleton (T-SQL):

```sql
-- Partition function: monthly boundaries
CREATE PARTITION FUNCTION pf_orders_monthly (datetime2)
AS RANGE RIGHT FOR VALUES
    ('2026-01-01', '2026-02-01', '2026-03-01', '2026-04-01');

CREATE PARTITION SCHEME ps_orders_monthly
AS PARTITION pf_orders_monthly ALL TO ([PRIMARY]);

CREATE TABLE Orders (
    OrderId        bigint NOT NULL,
    PlacedAt       datetime2 NOT NULL,
    CustomerId     uniqueidentifier NOT NULL,
    -- ...
    CONSTRAINT PK_Orders PRIMARY KEY CLUSTERED (PlacedAt, OrderId)
) ON ps_orders_monthly (PlacedAt);
```

The clustering key leads with the partition column (`PlacedAt`). This is what enables partition elimination on date-range queries: the optimizer reads only the partitions overlapping the WHERE clause.

Switch out an aged partition:

```sql
-- Staging table on the same filegroup as the partition being switched out
CREATE TABLE Orders_2026_01 (...) ON [PRIMARY];

ALTER TABLE Orders SWITCH PARTITION 1 TO Orders_2026_01;

-- Archive Orders_2026_01 (BCP / Polybase / Data Factory), then DROP it.
```

Switch in a fresh empty partition by merging the next future boundary:

```sql
ALTER PARTITION SCHEME ps_orders_monthly NEXT USED [PRIMARY];
ALTER PARTITION FUNCTION pf_orders_monthly() SPLIT RANGE ('2026-05-01');
```

## Tenant partitioning (multi-tenant SaaS)

Use for: hard-tenanted SaaS where a noisy or large tenant must not block others, where per-tenant residency may matter later, or where tenant offboarding must be a switch-out and drop.

The pattern:

1. Tenant id is the partition key. Boundaries are explicit ranges or hash buckets you control (not random hash, see below).
2. Clustered index leads with `TenantId`: every multi-tenant query is naturally tenant-scoped, and partition elimination cuts IO accordingly.
3. Onboarding a large tenant: split a partition to give them their own partition (or filegroup, on IaaS).
4. Offboarding a tenant: switch out their partition, archive, drop.

Trade-off: partition count cap. Azure SQL allows 15,000 partitions per object: plenty for most SaaS, but plan for it. If you have 50,000 small tenants, group them by hashed range (deterministic, controlled) into a smaller number of partitions: still not random, still aligned to the data lifecycle.

## Why never random hash

A random hash partition key (uniqueidentifier without sequencing, MD5 of a tenant id, modulo of a surrogate key) gives you uniform distribution and nothing else. You lose:

- Sliding-window archival: you cannot switch out a partition that aligns to a date or tenant boundary.
- Partition elimination: queries that filter on date or tenant cannot eliminate partitions because the data is uniformly spread.
- Tenant isolation: a single tenant's data is scattered across every partition, so per-tenant offboarding becomes a DELETE rather than a SWITCH OUT.

If the goal is hot-spot avoidance on a sequential PK, the right answer is a clustered key on (PartitionColumn, SequentialId) plus appropriate indexes, not random hashing.

## Index alignment

All nonclustered indexes on a partitioned table should be partition-aligned (on the same partition scheme) unless there is a specific reason not to. Aligned indexes allow SWITCH operations to succeed; non-aligned indexes block SWITCH and force you to drop and rebuild the index around every archival cycle.

```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId
ON Orders (CustomerId)
ON ps_orders_monthly (PlacedAt);  -- aligned
```

## Operational guardrails

- Always pre-create at least 3 future partitions. The job that creates the next partition will eventually fail; the buffer prevents an outage.
- Run the sliding-window job in a maintenance window with a clear runbook.
- Verify partition counts and sizes weekly: `sys.dm_db_partition_stats`. Drift indicates the boundary maintenance has fallen behind.
- Document the partition strategy in an ADR. Partitioning choices outlive the engineer who made them.

For data-lifecycle hand-off into a lakehouse or Fabric warehouse, switch out into a staging table, then export to Parquet via `/data-architect`. Do not stream rows out of the live partition.
