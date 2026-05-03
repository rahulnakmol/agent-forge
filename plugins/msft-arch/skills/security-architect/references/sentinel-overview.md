# Microsoft Sentinel: Orientation

This file is intentionally high-level. Deep Sentinel content (analytics rules, hunting queries, SOAR playbooks, connector configuration, KQL alert logic) lives in the `defender-sentinel` skill (Phase 4). Read that skill when the engagement explicitly requires SOC-tier Sentinel deployment.

## What Is Microsoft Sentinel?

Microsoft Sentinel is a cloud-native SIEM (Security Information and Event Management) and SOAR (Security Orchestration, Automation, and Response) platform built on Azure. It ingests security signals from across the environment, correlates them into incidents, and provides investigation and response tooling for security operations teams.

Sentinel sits on top of a Log Analytics workspace. All data (whether from Microsoft services, third-party connectors, or custom log sources) lands in Log Analytics and is queryable with KQL.

## When Sentinel Fits

Sentinel is a SOC-tier investment. It is appropriate when:

- The organisation has a dedicated security operations team or managed SOC provider that will actively triage incidents
- The workload handles regulated data (PII, PHI, payment card data) or has a compliance requirement for continuous security monitoring
- The threat surface justifies the operational overhead: multi-cloud, hybrid, or large number of internet-facing services
- The engagement produces a measurable volume of security signals that exceed what Defender for Cloud alerts alone can manage

Sentinel is **not** a substitute for Defender for Cloud. Defender for Cloud produces posture findings and workload alerts; Sentinel correlates those alerts with signals from identity, network, endpoints, and third-party sources into higher-fidelity incidents.

For workloads that do not yet have a SOC, start with Defender for Cloud alerts routed to the security team's email and an Azure DevOps work item workflow. Add Sentinel when the team is ready to actively use it.

## Core Concepts (Orientation Only)

| Concept | Brief description |
|---|---|
| **Workspace** | Sentinel is enabled on a Log Analytics workspace. One workspace per tenant is typical for smaller organisations; separate workspaces per environment for regulated multi-tenant scenarios. |
| **Data connectors** | Pre-built connectors for Microsoft 365, Entra ID, Defender for Cloud, Azure activity logs, AWS CloudTrail, and 150+ third-party sources. Each connector streams data into the workspace. |
| **Analytics rules** | KQL queries that run on a schedule and create incidents when conditions match. Microsoft provides a community rule library; custom rules are authored in the `defender-sentinel` skill. |
| **Incidents** | Correlated alert groups that form an actionable security event. Assigned to SOC analysts for investigation. |
| **Playbooks** | Logic Apps triggered by incident events for automated response (e.g., block an IP in NSG, disable a user account, post to Teams channel). |
| **Hunting** | Ad-hoc KQL queries for proactive threat investigation. Not covered here; see `defender-sentinel`. |
| **Workbooks** | Dashboard visualisations on top of workspace data. Microsoft provides workbook templates per connector. |

## Data Connectors: Common Starting Set

For most Azure-centric workloads, enable these connectors first:

1. **Microsoft Defender for Cloud**: streams Defender alerts into Sentinel incidents
2. **Microsoft Entra ID**: sign-in logs, audit logs (requires Entra ID P1/P2)
3. **Azure Activity**: subscription management operations, resource changes
4. **Azure Firewall**: network flow logs, threat intelligence matches
5. **Microsoft 365 Defender**: (if M365 in scope) unified XDR signal from Defender for Endpoint, Office, Identity

Each connector adds data volume to the Log Analytics workspace and increases Sentinel ingestion cost. Size the workspace commitment tier against expected GB/day before enabling all connectors simultaneously.

## Cost Orientation

Sentinel pricing: ingestion charged per GB/day. Log Analytics retention charged after 90 days (default free tier). Commitment tiers (100 GB/day, 200 GB/day, etc.) provide significant discounts over PAYG for large workloads.

Use the **Sentinel Cost Estimation Workbook** (available in the Sentinel workbook gallery) to estimate ingestion volume before going live. Defender for Cloud continuous export to Log Analytics contributes to ingestion; account for it in the estimate.

## Handoff Pointer

For any engagement that proceeds to SOC-level Sentinel deployment, invoke `/defender-sentinel` (Phase 4). That skill owns: analytics rule authoring, MITRE ATT&CK coverage mapping, custom workbook design, SOAR playbook implementation, and incident response workflow design.
