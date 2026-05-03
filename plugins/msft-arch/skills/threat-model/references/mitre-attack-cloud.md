# MITRE ATT&CK Cloud: Curated Technique Reference

MITRE ATT&CK for Cloud (Enterprise matrix, cloud sub-techniques) is the primary threat library for Azure infrastructure, API, and data-platform workloads. Use this reference to enumerate relevant techniques during the threat-modeling session. For AI/ML-specific threats, use `references/mitre-atlas-ai.md` instead.

Microsoft Defender for Cloud maps its recommendations and alerts to the MITRE ATT&CK matrix. Sentinel advanced hunting queries are structured around MITRE tactic categories. This alignment means every technique enumerated here has a corresponding detection or prevention control in the Azure security stack.

Reference: https://attack.mitre.org/matrices/enterprise/cloud/

---

## Tactic Coverage Matrix

| Tactic | ID | Techniques covered in this file |
|---|---|---|
| Initial Access | TA0001 | T1190, T1078, T1078.004 |
| Execution | TA0002 | T1651, T1059.009 |
| Persistence | TA0003 | T1098, T1098.001, T1136.003 |
| Privilege Escalation | TA0004 | T1548.005, T1078.004 |
| Defense Evasion | TA0005 | T1562.008, T1078.004 |
| Credential Access | TA0006 | T1552.001, T1552.004, T1528 |
| Discovery | TA0007 | T1580, T1538 |
| Lateral Movement | TA0008 | T1021.007 |
| Collection | TA0009 | T1530, T1213.003 |
| Exfiltration | TA0010 | T1537, T1567 |
| Impact | TA0040 | T1485, T1490, T1496 |

---

## Technique Detail: Initial Access

### T1190: Exploit Public-Facing Application

**Description:** Attacker exploits a vulnerability (injection flaw, authentication bypass, deserialization) in an internet-facing application to gain initial access to the cloud environment.

**Azure attack scenario:** A web application deployed on App Service has an unpatched dependency (Log4Shell-class CVE). An attacker exploits the vulnerability remotely, gains code execution in the App Service worker process, and uses the instance's Managed Identity token (retrieved from the IMDS endpoint) to authenticate to the Azure management plane.

**Detection signals:**
- Defender for App Service: "Anomalous code execution" alert
- Dependency scanner (Trivy, Defender for Containers): CVE detected in deployed image
- App Insights: unexpected exception patterns or HTTP 500 spike

**Mitigations:**
- Dependency scanning in CI (block High/Critical CVEs from merging without exception ADR)
- Azure WAF (Front Door / Application Gateway) in Prevention mode with OWASP 3.2 ruleset
- SBOM (syft, CycloneDX) in CI: know every dependency version deployed
- Managed Identity scope: minimum required RBAC; even if code execution is achieved, the blast radius is bounded by the identity's role

---

### T1078: Valid Accounts

**Description:** Attacker uses legitimate credentials, obtained via phishing, credential stuffing, password spray, or insider threat, to authenticate as a valid user or service principal.

**Azure attack scenario:** An attacker conducts a password-spray attack against an organisation's Entra ID tenant using a list of common passwords. A service account with a weak password, exempted from MFA due to a legacy integration exemption, is compromised. The account has Contributor access at the subscription scope.

**Detection signals:**
- Entra ID Identity Protection: "Password spray attack" risk event
- Microsoft Sentinel: UEBA anomalous sign-in (unusual location, unusual volume)
- Defender XDR: Fusion alert correlating failed logins + resource manager activity

**Mitigations:**
- MFA enforced via Conditional Access for all user accounts; no MFA exemptions without ADR
- Entra ID Smart Lockout + Password Protection (ban common passwords, custom banned list)
- PIM for privileged roles; no permanent Contributor / Owner assignments
- Workload Identity Federation for service-to-service (no password at all)

---

### T1078.004: Valid Accounts (Cloud Accounts)

**Description:** Attacker specifically targets cloud-native accounts (Entra ID users, service principals, Managed Identities) as opposed to on-premises accounts.

**Azure attack scenario:** A service principal client secret is committed to a public GitHub repository. An attacker scans the repository via GitHub Advanced Security or a third-party secret scanning tool, extracts the secret, and authenticates to the Azure management plane using the service principal identity, which has been assigned Owner at the resource group scope.

**Detection signals:**
- GitHub Advanced Security: secret scanning alert (push protection)
- Azure Activity Log: authentication from unexpected IP, unexpected geographic region
- Entra ID: service principal sign-in anomaly (Identity Protection)

**Mitigations:**
- Workload Identity Federation (eliminates the client secret entirely; highest priority mitigation)
- GitHub push protection + secret scanning enabled on all repos
- Secret rotation: any secret detected in a repository must be rotated immediately; assume it is compromised
- RBAC scope: service principal assignments should be at resource group or resource scope, never subscription or management group scope

---

## Technique Detail: Persistence

### T1098.001: Account Manipulation, Additional Cloud Credentials

**Description:** Attacker who has compromised a cloud account adds a new credential (service principal secret, certificate, SSH key, RBAC role assignment) to maintain persistent access even if the original credential is rotated.

**Azure attack scenario:** An attacker who has gained access to the Azure management plane via a compromised service principal adds a new client secret to a second, higher-privilege service principal. The new credential provides persistence independent of the original compromise.

**Detection signals:**
- Microsoft Sentinel: UEBA "Anomalous privilege granted" (Entra audit log, `Add app role assignment to service principal`)
- Azure Activity Log: `microsoft.authorization/roleassignments/write` events
- Entra ID audit log: credential addition events on service principals

**Mitigations:**
- Entra ID audit log alert on credential additions to service principals
- Periodic access review (Entra ID Access Reviews): detect stale or unexpected credentials
- Prefer Managed Identity over service principals (no credentials to add)
- PIM access reviews for role assignments: detect unexpected RBAC changes

---

### T1136.003: Create Account (Cloud Account)

**Description:** Attacker creates a new cloud account (Entra ID user, guest account, service principal, Managed Identity) to establish persistence in the environment.

**Azure attack scenario:** An attacker with sufficient Entra ID permissions creates a new service principal with a federated credential pointing to an attacker-controlled identity provider. The new service principal is assigned a role that provides ongoing access, and the federated credential means there is no client secret to expire.

**Detection signals:**
- Entra ID audit log: `Add service principal` events outside approved provisioning workflows
- Azure Activity Log: new RBAC role assignments to newly created identities
- Microsoft Sentinel: correlation between account creation and subsequent resource access

**Mitigations:**
- Conditional Access: restrict service principal creation to designated admin roles
- Alert on new service principal creation events in non-standard hours or by non-standard identities
- Regular audit of all service principals: purpose, owner, expiry (quarterly at minimum)

---

## Technique Detail: Credential Access

### T1552.001: Unsecured Credentials (Credentials in Files)

**Description:** Attacker searches for credentials stored in configuration files, scripts, IaC templates, environment variable files, or source control history.

**Azure attack scenario:** A developer stores a storage account connection string in `appsettings.Development.json` and accidentally commits it to a shared repository. The connection string grants full read/write access to the storage account. An attacker discovers the credential in the repository history (even after the file is removed; Git history preserves it).

**Detection signals:**
- GitHub Advanced Security / ADO Credential Scanner: inline secret detection
- Defender for Cloud: "Sensitive data exposed in source code" recommendation

**Mitigations:**
- Key Vault reference syntax for all secrets in App Service / Container Apps / AKS
- GitHub push protection enabled; Dependabot security updates on all repos
- `git secrets` or `trufflehog` in pre-commit hooks
- Immediately rotate any credential detected in source control; do not rely on history rewriting

---

### T1528: Steal Application Access Token

**Description:** Attacker steals an OAuth access token or Managed Identity token to authenticate as the application without knowing the underlying credential.

**Azure attack scenario:** An attacker achieves code execution on a compute resource (App Service, VM, container) and calls the Azure Instance Metadata Service (IMDS) at `http://169.254.169.254/metadata/identity/oauth2/token` to retrieve a Managed Identity access token. The token is valid for one hour and can be used to authenticate to any Azure resource the identity is authorised to access.

**Detection signals:**
- IMDS call patterns: Defender for Cloud / Defender for Servers monitors for IMDS access from unexpected processes
- Defender for Resource Manager: authentication from an unusual geographic location using an access token

**Mitigations:**
- Managed Identity RBAC scope: the identity should only have access to the specific resources it needs. Even if the token is stolen, the blast radius is bounded.
- Conditional Access: enforce location and device compliance conditions even for non-interactive (application) authentication where supported
- Network isolation: limit compute resource outbound access to approved endpoints (prevents exfiltrating the token via outbound HTTP)

---

## Technique Detail: Collection

### T1530: Data from Cloud Storage

**Description:** Attacker accesses and extracts sensitive data from cloud storage objects (Azure Blob Storage, Azure Data Lake Storage, Azure Files) using valid credentials or misconfigured access policies.

**Azure attack scenario:** A storage account with `AllowBlobPublicAccess = true` and a container set to `Blob` public access level exposes a container of customer records. An attacker enumerates the container URL (guessable via predictable naming conventions) and downloads all files without authentication.

**Detection signals:**
- Defender for Storage: "Anonymous access to Azure Blob" alert
- Defender for Storage: mass download / unusual data volume alert
- Azure Monitor: anomalous access patterns (time of day, geographic region, volume)

**Mitigations:**
- Azure Policy (deny effect): `Deny-PublicBlobAccess` on all storage accounts
- Managed Identity + RBAC (Storage Blob Data Reader) for all legitimate access; no SAS tokens for inter-service access
- Defender for Storage enabled on all production storage accounts (GA, includes malware scanning on upload)
- Private endpoint for all production storage accounts; disable public access after confirming private endpoint health

---

### T1213.003: Data from Information Repositories (Code Repositories)

**Description:** Attacker accesses code repositories (GitHub, Azure DevOps) to steal credentials, proprietary code, or internal documentation.

**Azure attack scenario:** A GitHub Actions workflow secret (a service principal client secret used for deployment) is printed to the workflow log by a dependency or debug step. An attacker with read access to the repository reads the log and extracts the secret.

**Detection signals:**
- GitHub Advanced Security: secret scanning of workflow logs
- Entra ID: service principal authentication from unexpected IP / geography

**Mitigations:**
- Never `echo` or `print` secrets in pipeline steps; use masked variables
- Scope GitHub Actions OIDC (Workload Identity Federation) to the specific repository and branch; no client secrets in pipeline
- Restrict repository access to the minimum team; enforce 2FA for all contributors
- GitHub secret scanning + push protection on all repositories (no opt-out)

---

## Technique Detail: Exfiltration

### T1537: Transfer Data to Cloud Account

**Description:** Attacker exfiltrates data by moving it to an attacker-controlled cloud storage account in a different tenancy, bypassing network egress controls.

**Azure attack scenario:** An attacker with access to Azure Storage (via compromised Managed Identity token) uses the `azcopy sync` command to replicate a production blob container to a storage account in a separate Azure tenant under their control. This bypasses on-premises egress monitoring because the traffic is Azure-to-Azure.

**Detection signals:**
- Defender for Storage: cross-tenant copy operations
- Azure Monitor: large data volume outbound from storage (even within Azure)
- Microsoft Sentinel: `azcopy` or `az storage copy` executed from an unexpected resource

**Mitigations:**
- Enable Defender for Storage (includes anomalous cross-tenant copy detection)
- Storage account firewall: restrict access to approved VNet subnets only; block public endpoints
- Azure Policy: prevent storage accounts from allowing external replication unless explicitly authorised

---

## Technique Detail: Impact

### T1485: Data Destruction

**Description:** Attacker destroys data or system resources to deny availability or cover tracks.

**Azure attack scenario:** A ransomware operator who has compromised an Azure subscription uses the Azure management plane API to delete all blob containers and Cosmos DB databases in the subscription. Soft-delete is not enabled on the storage accounts, so the data is irrecoverable.

**Detection signals:**
- Azure Activity Log: bulk `delete` operations on storage accounts, databases, Key Vaults
- Defender for Resource Manager: suspicious bulk delete operations alert
- Microsoft Sentinel: analytics rule detecting mass deletion events

**Mitigations:**
- Soft-delete enabled on all storage accounts (minimum 30 days for production)
- Cosmos DB continuous backup + point-in-time restore enabled
- Azure Backup for VMs, SQL databases
- Resource locks (`ReadOnly` or `Delete` lock) on production resource groups. Removing the lock before deleting resources creates an additional audit event.
- PIM for all identities with delete permissions; no permanent delete access

---

### T1496: Resource Hijacking

**Description:** Attacker uses compromised cloud resources for cryptomining, DDoS amplification, or other resource-intensive workloads, generating large unexpected charges.

**Azure attack scenario:** An attacker compromises an App Service Managed Identity with Contributor permissions. They provision a fleet of GPU VMs in the subscription to run cryptocurrency mining workloads, generating tens of thousands of dollars in charges before the subscription owner notices.

**Detection signals:**
- Defender for Cloud: "Suspicious cryptocurrency mining activity" alert
- Azure Cost Management: unusual spend spike (cost anomaly detection)
- Azure Monitor: unexpected VM provisioning events outside approved resource groups

**Mitigations:**
- Azure Policy: restrict allowed VM SKUs to approved list; restrict allowed regions; prohibit GPU SKUs if not required
- Resource group locks on subscription-level resources
- Azure Cost Management alerts: alert on 20%+ daily spend deviation
- Managed Identity scope: Contributor at subscription scope should never be granted to non-administrative identities

---

## Technique Prioritisation by Azure Architecture Type

| Architecture type | Top 3 techniques to prioritise |
|---|---|
| Multi-tenant SaaS (App Service + Cosmos DB + Entra ID) | T1078.004 (cloud account takeover), T1530 (cross-tenant data access), T1098.001 (persistence via credential addition) |
| Data platform (Azure Data Lake + Synapse + ADF) | T1530 (data from cloud storage), T1537 (exfiltration to attacker cloud), T1552.001 (credentials in ADF linked service configs) |
| AI agent (Azure OpenAI + Cosmos DB + Managed Identity) | T1528 (IMDS token theft), T1530 (data collection via agent), T1490 (inhibit system recovery; agent corrupts state) |
| Container platform (AKS + ACR + private endpoints) | T1190 (exploit container vulnerability), T1136.003 (create service account in cluster), T1562.008 (disable audit logging) |
| CI/CD pipeline (GitHub Actions + Azure DevOps) | T1552.004 (credentials in pipeline), T1213.003 (data from code repos), T1098.001 (add persistent credentials) |

For AI/ML-specific techniques beyond T1528, use `references/mitre-atlas-ai.md`.
