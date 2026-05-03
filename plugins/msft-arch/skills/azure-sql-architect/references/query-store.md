# Query Store

**Applies to**: Azure SQL Database (all tiers), Azure SQL Managed Instance, Azure SQL Edge.

> Codified opinion: Query Store enabled on every production DB. Analyze top regressions weekly.

Query Store is the audit trail for query plans and runtime stats. It is on by default in Azure SQL Database, but the defaults are not always right for production. Tune the settings, then build the weekly regression workflow on top.

## Enabling and configuring

Enable Query Store and set the operation mode to read-write:

```sql
ALTER DATABASE CURRENT SET QUERY_STORE = ON;

ALTER DATABASE CURRENT SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,
    QUERY_CAPTURE_MODE = AUTO,
    SIZE_BASED_CLEANUP_MODE = AUTO,
    MAX_STORAGE_SIZE_MB = 2048,
    INTERVAL_LENGTH_MINUTES = 15,
    STALE_QUERY_THRESHOLD_DAYS = 30
);
```

Settings that matter:

- `OPERATION_MODE = READ_WRITE`: capture is on. `READ_ONLY` happens automatically when storage fills, which silently blinds you. Alert on it.
- `QUERY_CAPTURE_MODE = AUTO`: filters out trivial queries; for high-volume workloads `CUSTOM` lets you tune thresholds further.
- `MAX_STORAGE_SIZE_MB`: size for retention. 2 GB is a starting point; busy workloads need more. If Query Store flips to READ_ONLY, raise this.
- `INTERVAL_LENGTH_MINUTES`: aggregation bucket. 15 is fine for most; 5 for high-frequency tuning windows.
- `STALE_QUERY_THRESHOLD_DAYS = 30`: long enough to compare across a full deployment cycle.

## Top-regression workflow (weekly)

Every Monday: pull the top regressions, decide on each.

```sql
-- Regressions in the last 7 days vs prior baseline
SELECT TOP 25
    qsq.query_id,
    qsqt.query_sql_text,
    qsp.plan_id,
    rs.avg_duration / 1000.0 AS avg_duration_ms,
    rs.count_executions,
    rs.last_execution_time
FROM sys.query_store_query qsq
JOIN sys.query_store_query_text qsqt
    ON qsq.query_text_id = qsqt.query_text_id
JOIN sys.query_store_plan qsp
    ON qsq.query_id = qsp.query_id
JOIN sys.query_store_runtime_stats rs
    ON qsp.plan_id = rs.plan_id
WHERE rs.last_execution_time > DATEADD(day, -7, SYSUTCDATETIME())
ORDER BY rs.avg_duration DESC;
```

For each regression:

1. Compare plans: `sys.query_store_plan` entries for the same `query_id`. If a previously-fast plan exists, that is the candidate to force.
2. Identify the cause: stats out of date, parameter sniffing, missing index, schema change, AAD outage spike. Do not skip this step. Forcing a plan without understanding why the regression happened defers the problem.
3. Force the better plan only as a stopgap:

```sql
EXEC sp_query_store_force_plan @query_id = 42, @plan_id = 17;
```

4. Log the forced plan in an ADR-style note in the repo (date, query_id, plan_id, reason, follow-up issue link). The next engineer needs to see why this exists.
5. File a follow-up: index, query rewrite, statistics update, or schema change. Plan forcing is not a fix.

## Unforce when the underlying issue is resolved

```sql
EXEC sp_query_store_unforce_plan @query_id = 42, @plan_id = 17;
```

A graveyard of forced plans is a maintenance hazard. Audit them quarterly and unforce the ones whose root cause was fixed.

## Alerts to wire up

- Query Store flipped to READ_ONLY mode (storage full): high-priority alert.
- Top regression count above a threshold week-over-week: medium-priority alert into the team channel.
- Plan forcing failures (`sys.query_store_plan_forcing_locations`): low-priority but log for review.

## Built-in views worth knowing

- `sys.query_store_query`, `sys.query_store_query_text`, `sys.query_store_plan`: the catalog.
- `sys.query_store_runtime_stats` and `sys.query_store_runtime_stats_interval`: bucketed runtime numbers.
- `sys.query_store_wait_stats`: wait categories per query (Azure SQL DB and MI).
- The Azure portal Query Performance Insight surfaces these for casual review; for the weekly workflow, hit the DMVs directly so your queries are versioned in the repo.

## Don'ts

- Do not turn Query Store off to "save space". Raise `MAX_STORAGE_SIZE_MB` instead.
- Do not force plans without recording why. A forced plan with no rationale is technical debt with high blast radius.
- Do not rely on Query Store alone for app-tier latency: pair with App Insights / Log Analytics so you see the end-to-end picture (`/observability-architect`).

Verify current Query Store DMVs and any new capture modes with `microsoft_docs_search` before quoting capabilities to the customer; the surface evolves.
