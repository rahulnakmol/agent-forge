# Failover Groups and Geo-Replication

**Applies to**: Azure SQL Database (single database and elastic pool), Azure SQL Managed Instance (instance failover groups), SQL Server on Azure VM (Always On AGs).

> Codified opinion: Failover groups for cross-region. Auto-failover only after sufficient soak time in test.

Failover groups are the right abstraction for cross-region disaster recovery on Azure SQL Database and Managed Instance. They wrap active geo-replication with managed listener endpoints (`<group>.database.windows.net` for read-write, `<group>.secondary.database.windows.net` for read-only) so the app does not pin a region and a failover does not require app config changes.

## Pair design

| Source region | Pair to | Why |
|---|---|---|
| East US | West US 3 | Microsoft-paired regions; lowest replication latency for the pair |
| West Europe | North Europe | Same |
| Southeast Asia | East Asia | Same |
| Other | Use Microsoft's documented region pair | Pairing reduces blast radius from regional planned maintenance |

Verify current paired regions with `microsoft_docs_search` before committing; the pairing list is updated periodically and a few regions have non-obvious pairs.

## Auto-failover policy

Two modes:

- Automatic: Azure SQL initiates failover after a grace period (default 1 hour) when the primary is unreachable.
- Manual: failover only via explicit command (CLI, PowerShell, T-SQL, REST).

Default to manual until the soak test passes. The soak protocol:

1. Stand up failover groups in non-prod, with the same listener-endpoint usage as prod.
2. Run failover drills monthly: trigger manual failover, verify app reconnects via the listener within the connection-resilience window, verify read-only replica still serves reports.
3. Inject partial-failure modes: latency spikes, intermittent DNS, blocked outbound from the primary region. Confirm the app does not flap.
4. Only after a successful drill streak (at least 3 months of clean monthly drills, no app-side regressions) flip to automatic in non-prod first, then prod.
5. Revisit the auto policy after every major app deploy that touches connection management.

The grace period is the lever. Shorter grace = faster RTO, more flap risk; longer grace = slower RTO, more stable. 1 hour is a reasonable production default; 15 minutes is aggressive and should be paired with a circuit-breaker pattern app-side (`connection-resilience.md`).

## Listener endpoint discipline

The whole point of failover groups is that the app uses the listener endpoint, not a region-specific server name. Enforce in code review:

- Connection strings reference `<group>.database.windows.net` (read-write) and `<group>.secondary.database.windows.net` (read-only).
- No region pinning in app config, no environment-specific server names, no fallback logic that bypasses the listener.

For read-only routing on top of a failover group (Hyperscale or Business Critical secondary, plus the geo-secondary): set `ApplicationIntent=ReadOnly` on the connection string targeting the read-write listener; the gateway routes to the appropriate replica.

## RTO and RPO

Document the targets per environment in the ADR:

- Failover group RPO: typically seconds (asynchronous replication). Specific RPO depends on workload; verify the current SLA via `microsoft_docs_search`.
- Failover group RTO: minutes for managed failover. Faster on Hyperscale; SLA varies by tier.
- Acceptable data loss on unplanned failover: state explicitly. Customers will assume zero unless told otherwise.

## Managed Instance failover groups

Instance failover groups replicate every database in the instance as one unit. Useful for lift-and-shift workloads with cross-database queries that would break if databases failed over independently.

Caveats:

- The secondary instance is a full instance with its own cost, even when not serving traffic.
- Failover times tend to be longer than single-database failover groups; verify with current docs.
- Some MI features (Service Broker, distributed transactions across linked servers) need explicit configuration on both the primary and secondary.

## Always On AGs on SQL VM (IaaS)

When the workload runs on SQL on Azure VM (BYOL or feature requirements that need full SQL Server surface), failover groups do not apply: build Always On AGs with Windows Server Failover Cluster (WSFC) or distributed AGs.

Patterns:

- Synchronous AG within an Availability Zone for sub-second RPO and HA.
- Asynchronous AG to a different region for DR.
- Listener: an Azure Internal Load Balancer in front of the AG nodes; app connects to the listener, not individual nodes.
- Quorum: cloud witness backed by Azure Storage account (cheap, recommended) or a third file-share witness.
- Patching: rolling, secondary first, with manual failover during a maintenance window.

This is more operational overhead than the PaaS path. Use only when SQL VM is required (license cost, full surface area, OS-level customization). For greenfield, the Azure SQL Database Hyperscale or Business Critical path with a failover group is the right answer.

## Pre-cutover checklist

- [ ] Pair regions selected from Microsoft's paired regions list
- [ ] Replication latency baselined under peak load
- [ ] Listener endpoints used in app config (no region pinning)
- [ ] Failover policy: manual until soak test passes
- [ ] Monthly failover drill scheduled and runbook documented
- [ ] Connection resilience pattern in place app-side (`connection-resilience.md`)
- [ ] RPO and RTO documented per environment
- [ ] Identity: server-level firewall, Private Endpoint, and Entra-only authentication apply on both primary and secondary (`/identity-architect`, `/security-architect`)
- [ ] Audit and ledger configurations replicated to the secondary (verify per-database; some settings are server-level)
