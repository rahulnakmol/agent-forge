# Defender for Cloud Baseline

## Subscription Onboarding

Every Azure subscription must have Defender for Cloud enabled before any workload is deployed. Foundational CSPM is free and auto-enables when you connect a subscription; it provides the Microsoft Cloud Security Benchmark (MCSB) assessment, secure score, and basic recommendations at no cost.

### Onboarding checklist

```bash
# Verify Defender for Cloud is active on a subscription
az security auto-provisioning-setting show --name mma
az security pricing list --output table

# Enable Defender CSPM (paid plan) - requires Subscription Owner
az security pricing create --name CloudPosture --tier Standard

# Enable Defender for Servers Plan 2 on a subscription
az security pricing create --name VirtualMachines --tier Standard --subplan P2

# Enable Defender for Containers
az security pricing create --name Containers --tier Standard

# Enable Defender for Storage (malware scanning on-upload)
az security pricing create --name StorageAccounts --tier Standard
```

Auto-provisioning agents (MMA / AMA) must be enabled for Defender for Servers to function. Use AMA (Azure Monitor Agent) for all new deployments. MMA is deprecated.

## Plans by Resource Type

| Resource type | Free (Foundational CSPM) | Standard (paid plan) | Plan name in API |
|---|---|---|---|
| All resources | MCSB posture recommendations, secure score | N/A | `CloudPosture` (CSPM) |
| VMs / VMSS / Arc | Basic OS recommendations | P1: MDE integration, adaptive app controls. P2: adds file integrity monitoring, JIT VM access, agentless vuln scan | `VirtualMachines` |
| AKS / containers | Basic image vulnerability (registry) | Runtime threat detection, env hardening, agentless container posture | `Containers` |
| App Service | N/A | Threat detection, dangling DNS, unusual process invocation | `AppServices` |
| Azure SQL | N/A | SQL anomaly detection, SQL injection alerts | `SqlServers`, `SqlServerVirtualMachines` |
| PostgreSQL / MySQL Flexible | N/A | Anomalous access pattern alerts | `OpenSourceRelationalDatabases` |
| Storage accounts | N/A | Malware scanning on-upload (up to 50 GB/blob), anomalous access alerts | `StorageAccounts` |
| Key Vault | N/A | Unusual access pattern alerts, high-volume operation alerts | `KeyVaults` |
| DNS | N/A | Exfiltration, tunneling, malicious domain resolution detection | `Dns` |
| ARM (management layer) | N/A | Suspicious management operations, cryptomining alerts | `Arm` |

**Rule of thumb**: Enable all standard plans for production subscriptions. Use Foundational CSPM only for dev/sandbox. The cost calculator in the Azure portal (`portal.azure.com > Defender for Cloud > Cost Calculator`) estimates monthly spend before enabling.

## Secure Score Targets

| Environment | Minimum acceptable score | Target score |
|---|---|---|
| Dev / sandbox | ≥ 60% | ≥ 70% |
| Staging / pre-prod | ≥ 70% | ≥ 80% |
| Production | ≥ 80% | ≥ 90% |

Secure score is calculated against MCSB controls weighted by criticality. Prioritise "Quick fixes" (single-click remediations) first to gain score efficiently. Bulk remediation via Azure Policy is available for findings affecting multiple resources.

## MCSB Regulatory Compliance Dashboard

The Regulatory Compliance dashboard maps MCSB controls to external frameworks automatically. Enable it on day 1.

Frameworks available out-of-box (no custom policy needed):
- **Microsoft Cloud Security Benchmark v1** (always enabled; MCSB is the default assessment)
- **NIST SP 800-53 Rev 5**
- **CIS Azure Foundations Benchmark**
- **ISO 27001:2013**
- **PCI-DSS v4**
- **SOC 2 Type 2**

For regulated workloads (healthcare, finance, government), add the relevant framework to the compliance dashboard and track against it from sprint 1. Do not wait for audit time.

MCSB v2 is currently in preview (12 domains, expanded AI Security domain). Monitor progress at `learn.microsoft.com/security/benchmark/azure/introduction`. Adopt v2 controls as preview guidance; maintain v1 for compliance reporting until v2 reaches GA.

## Continuous Export + Alerting

Export Defender findings to Log Analytics for long-term retention and SIEM correlation:

```bash
# Configure continuous export to Log Analytics workspace
az security auto-provisioning-setting update --name mma --auto-provision On

# Export security recommendations and alerts to Log Analytics
az security setting update --name MCAS --enabled true
```

Set email notifications for high-severity alerts to the security distribution list. Configure workflow automation to create Azure DevOps work items for Critical findings (secure score impact > 10 points).
