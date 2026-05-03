Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Defender Plan Completeness** — Correctly maps all resource types to their required Defender plans. Production minimum: Foundational CSPM (free, all subscriptions), Defender CSPM (paid, production), Servers P2 (VMs), Storage, Key Vault, Resource Manager, App Service, Containers (AKS/ACR), SQL. Score 5 if plan matrix is complete and correct; 1 if major plans are missing or incorrectly assigned.

2. **Sentinel Workspace Topology Decision** — Correctly selects single vs hub-and-spoke topology based on tenancy, data residency, and billing requirements. Hub-and-spoke for multi-tenant/MSSP/EU residency; single workspace for single tenant with no residency constraints. Score 5 if topology decision matches requirements with clear rationale; 1 if topology is inappropriate or undecided.

3. **Analytics Rules MITRE Mapping** — Requires MITRE ATT&CK tactic and technique mapping on every analytics rule. Correctly prioritizes OOTB Content Hub solutions before custom rules. Addresses NRT rules only for single-event high-priority detections. Score 5 if MITRE mapping is required and correct; 1 if MITRE mapping is omitted.

4. **SOAR Playbook Design** — Correctly decouples automation rule (trigger) from Logic Apps playbook (response). Stores playbook ARM templates in Git. Does not hard-wire playbooks to individual analytics rules. Score 5 if SOAR architecture follows the decoupled pattern with IaC; 1 if playbooks are hard-wired or not version-controlled.

5. **Ingestion Cost Management** — Addresses log volume estimation before enabling connectors. Routes low-value high-volume logs to Basic Logs tier or separate workspace. Sets commitment tier appropriately. Score 5 if cost governance is addressed with specific recommendations; 1 if cost considerations are ignored.
