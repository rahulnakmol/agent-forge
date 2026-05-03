# Hyperscale vs Premium (Business Critical) vs General Purpose

**Applies to**: Azure SQL Database, single database and elastic pool, vCore purchasing model. The DTU "Premium" tier maps to vCore Business Critical for the purposes of this guide.

> Codified opinion: Hyperscale > Premium for >1TB workloads needing fast restore.

## When to choose each tier

| Tier | Choose when | Avoid when |
|---|---|---|
| General Purpose | OLTP, <1 TB, predictable load, dev or low-tier prod, cost is the driving constraint, RPO of minutes is acceptable | Sub-millisecond IO required; in-memory OLTP needed; >1 TB projected within the next 18 months |
| Business Critical | Mission-critical OLTP, in-memory OLTP, sub-ms IO, local SSD, AG-style HA inside the tier, read-scale-out via the BC built-in replica | Data size approaches 4 TB ceiling; restore RTO of hours is unacceptable; cost ceiling is tight relative to projected size |
| Hyperscale | >1 TB or fast restore matters; up to 128 TB ceiling; read-scale-out via up to four HA secondaries plus named replicas; serverless-on-Hyperscale for variable load; geo-replication via active geo-replication and failover groups | Need DTU purchasing model; need legacy log shipping pattern; workload requires features explicitly not supported in Hyperscale (verify with `microsoft_docs_search` for current limitations) |
| Managed Instance (GP / BC) | Lift-and-shift from on-prem SQL needing Agent, CLR, cross-DB queries, Service Broker, linked servers | Greenfield cloud-native workload (use Azure SQL Database) |
| SQL on Azure VM | BYOL, full surface area, AGs you own end-to-end, OS-level customization | Operational overhead of patching and HA is not justified by a control requirement |

## Storage architecture: why Hyperscale restores fast

Hyperscale separates the relational engine (compute nodes) from durable storage (page servers + log service + Azure Storage). Backups are file-snapshot based and are nearly instantaneous regardless of database size: the log service ships log records to page servers, and snapshots are taken at the storage layer. Restore is also snapshot-based, so restore RTO is bounded by snapshot copy and metadata operations, not by the volume of data.

In Business Critical and General Purpose, backup and restore work on the file-based model familiar from SQL Server: full + differential + log, restored sequentially. Restore RTO grows with database size. For a 5 TB database, expect hours on Business Critical and minutes on Hyperscale.

This is the single biggest reason Hyperscale wins above ~1 TB: when something goes wrong (bad deploy, accidental DELETE, ransomware), restore is the recovery path, and restore time is the actual RTO.

## Read-scale-out

| Tier | Read replicas | How to use |
|---|---|---|
| General Purpose | None natively (geo-replica only) | App reads hit the primary |
| Business Critical | 1 always-on readable secondary | `ApplicationIntent=ReadOnly` connection string + read-only routing |
| Hyperscale | Up to 4 HA secondaries + named replicas (compute-isolated) for OLTP read-scale-out | `ApplicationIntent=ReadOnly` with named replicas for HTAP-style read offload |

Read-only routing is preferred over app-side splitting in every case. The gateway routes ReadOnly intent to the configured replica; the app holds one connection string. App-side splitting only makes sense if you need geo-secondary reads in a different region for residency reasons.

## Cost crossover (rule of thumb, verify with current pricing)

For a steady-state workload of size S:

- S < 500 GB and predictable load: General Purpose is cheapest.
- 500 GB to ~1 TB and mission-critical: Business Critical is usually right.
- 1 TB to 4 TB and the BC compute SKU is sufficient: Business Critical, but reconsider if restore RTO matters more than cost.
- > 1 TB with fast restore as a hard NFR, OR > 4 TB at all: Hyperscale.

Hyperscale charges separately for storage (per GB-month allocated) and compute. Serverless-on-Hyperscale autopauses compute for variable load. For long stretches of low activity, the storage-only floor on Hyperscale can beat a fixed Business Critical SKU. Run the FinOps math with `/finops-architect` rather than guessing.

## Tradeoffs to call out in the ADR

- Hyperscale uses Full recovery model only: simple and bulk-logged are not available. Bulk loads use the Hyperscale log architecture's higher ingest ceiling (~150 MiB/s per current Microsoft docs: verify with `microsoft_docs_search`).
- Hyperscale geo-replicas have separate storage from the primary, which adds cost; this is the price of regional isolation and is correct.
- Converting an existing Azure SQL Database to Hyperscale is supported; converting back from Hyperscale is not. Treat the move as one-way.
- Convert-to-Hyperscale with geo-replicas is a more recent capability: confirm GA status with `microsoft_docs_search` before quoting a migration path.
- DC-series hardware (required for Intel SGX enclaves with Always Encrypted) is not available with serverless and not in every region. If SGX attestation is a hard requirement, design for fixed compute and verify regional availability.

## Decision flow

1. Is this lift-and-shift from on-prem with Agent / CLR / cross-DB / Service Broker? Yes: Managed Instance. Else continue.
2. Is the data size today or in 18 months > 4 TB, or is restore RTO < 1 hour required at any size > 1 TB? Yes: Hyperscale. Else continue.
3. Does the workload need in-memory OLTP, sub-ms IO, or local-SSD latency floor? Yes: Business Critical. Else continue.
4. Predictable load, < 1 TB, RPO of minutes acceptable? General Purpose.

Always verify current limits and feature availability with Microsoft Learn MCP before locking the choice. Hyperscale capabilities and ledger features evolve frequently.
