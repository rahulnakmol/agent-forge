---
category: security
loading_priority: 1
keywords:
  - security
  - zero-trust
  - secure-by-design
  - OWASP
  - threat-modeling
  - encryption
  - authentication
  - authorization
applies_to:
  - agent
  - odin
  - spec
version: "1.0"
last_updated: "2026-03-21"
---

# Security-by-Design Reference

> This is the canonical security framework referenced by ALL three skills
> (agent, odin, spec). Every design produced must be
> **secure by design**, **secure at code**, and **secure at execution**.
> No design passes validation without satisfying the controls in this document.

---

## 1. Security-by-Design Principles

These principles are non-negotiable. They apply to every architecture, every
component, and every line of specification produced by any skill.

| # | Principle | Rule |
|---|-----------|------|
| 1 | **Zero Trust** | Never trust, always verify. Every request, internal or external, is authenticated and authorized before processing. Network location alone never grants trust. |
| 2 | **Least Privilege** | Grant the minimum permissions necessary for a task. No admin-by-default. Permissions are time-boxed (JIT access) where supported. |
| 3 | **Defense in Depth** | Multiple overlapping security layers protect every asset. Failure of one layer does not expose the system. |
| 4 | **Secure Defaults** | Encryption is on by default. Authentication is required by default. Logging is on by default. Public access is off by default. |
| 5 | **Fail Secure** | When a component fails, it fails to a secure state: deny access, reject the request, close the connection. Never fail open. |
| 6 | **Separation of Concerns** | Security logic (authn, authz, validation) is isolated from business logic. Security cross-cuts via middleware, policies, and decorators, not inline checks scattered through code. |
| 7 | **Input Validation** | All external input is validated, sanitized, and typed before processing. Validation occurs at the trust boundary, not deep inside the stack. |
| 8 | **Audit Everything** | Every security-relevant action is logged with actor, action, resource, timestamp, and outcome. Logs are immutable, centralized, and retained per compliance policy. |

**Application rule**: When reviewing any design, if a principle above is
violated, the design MUST be revised before approval. There are no exceptions.

---

## 2. Secure at Design

### 2.1 Threat Modeling (STRIDE)

For every design, identify threats using the STRIDE model. Each threat category
must have explicit mitigations documented in the design artifact.

| Threat | Question | Required Mitigation |
|--------|----------|---------------------|
| **S: Spoofing** | Can an attacker impersonate a user or service? | Strong authentication: Entra ID for users, managed identity for services, mTLS for service-to-service where managed identity is unavailable. |
| **T: Tampering** | Can data be modified in transit or at rest? | TLS 1.3 for all transit. Encryption at rest (AES-256). Integrity checks (checksums, HMAC) for critical data flows. |
| **R: Repudiation** | Can a user deny performing an action? | Immutable audit logs with signed tokens. Non-repudiation via Azure Monitor + Log Analytics with tamper-proof storage. |
| **I: Information Disclosure** | Can sensitive data be exposed? | Data classification labels on all stores. Encryption. DLP policies. Column-level and row-level security. No secrets in logs. |
| **D: Denial of Service** | Can the system be overwhelmed? | Rate limiting (APIM, middleware). WAF rules. Autoscaling with upper bounds. Circuit breakers. Azure DDoS Protection Standard. |
| **E: Elevation of Privilege** | Can a user gain unauthorized access? | RBAC with least privilege. Input validation to prevent injection. Separation of admin and user planes. Regular access reviews. |

**Mandatory output**: Every HLD and LLD must include a STRIDE table for each
public-facing component and each trust boundary crossing.

### 2.2 Data Classification

Every data element in the design must be classified. The classification drives
encryption, access control, and retention decisions.

| Classification | Access | Encryption at Rest | Additional Controls |
|---------------|--------|-------------------|---------------------|
| **Public** | No restrictions | Platform default | None |
| **Internal** | Organization-only (Entra ID authenticated) | Platform default | Access logging |
| **Confidential** | Role-based access (named roles only) | AES-256, service-managed keys | Audit logging, DLP policies, no export without approval |
| **Highly Confidential** | Named-individual access with MFA | AES-256, customer-managed keys (CMK) via Key Vault HSM | Full audit trail, data masking in non-prod, geo-fencing, HSM-backed keys |

**Mandatory output**: Every data store in the design must have a classification
label. Unclassified data stores are a validation failure.

### 2.3 Authentication Architecture per Stack

| Stack | User Authentication | Service Authentication | External User Authentication |
|-------|--------------------|-----------------------|------------------------------|
| **Stack A** (Power Platform) | Entra ID + Dataverse security roles | Managed identity, service principals with certificate auth | Entra ID B2B (guest accounts) |
| **Stack B** (Azure PaaS) | Entra ID + Azure RBAC | Managed identities (system-assigned preferred) | Azure AD B2C with custom policies |
| **Stack C** (Containers / AKS) | Entra ID + K8s RBAC (Azure AD integration) | Workload identity (federated credentials), mTLS via service mesh | Azure AD B2C or OIDC provider via ingress |
| **Stack D** (D365) | Entra ID + D365 security roles + business units | Managed identity, S2S application users | Entra ID B2C with Power Pages portal authentication |

**Rule**: Service-to-service communication MUST use managed identity or workload
identity. Shared secrets and connection strings with passwords are prohibited in
production.

### 2.4 Authorization Patterns

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| **RBAC** (Role-Based Access Control) | Default for most scenarios. Users map to roles, roles map to permissions. | Entra ID app roles, Azure RBAC, D365 security roles, Dataverse roles |
| **ABAC** (Attribute-Based Access Control) | When role alone is insufficient: decisions depend on data residency, tenant, department, or time of day. | Azure AD conditional access, custom policy engines, Dataverse row-level security with business units |
| **Policy-as-Code** | Infrastructure and platform guardrails enforced automatically. | Azure Policy (deny/audit/modify), OPA/Gatekeeper for AKS, Dataverse column security profiles |
| **API Authorization** | Every API endpoint must enforce authorization. | OAuth 2.0 scopes with incremental consent, Azure APIM policies for JWT validation, custom middleware for fine-grained claims checks |

**Rule**: Authorization checks MUST occur at the API/service boundary. Client-
side-only authorization is never acceptable.

### 2.5 Network Security

- **Virtual Network isolation**: All backend and data-tier resources reside in
  VNets with NSGs restricting traffic to required ports and sources only.
- **Private endpoints**: All PaaS services (Storage, SQL, Cosmos DB, Key Vault,
  Service Bus, Event Hub) use private endpoints in production. Public endpoints
  are disabled.
- **WAF**: Azure Front Door or Application Gateway with WAF v2 (OWASP 3.2
  ruleset) protects all public-facing HTTP endpoints.
- **Network segmentation**: Separate subnets for frontend, backend, and data
  tiers. NSGs enforce inter-subnet traffic rules. ASGs simplify rule management.
- **DNS**: Azure Private DNS Zones for internal name resolution. No public DNS
  records for internal-only services.
- **Egress control**: Azure Firewall or NAT Gateway with UDRs for controlled
  egress. No direct internet access from backend or data subnets.

---

## 3. Secure at Code

### 3.1 Input Validation

- ALL external inputs are validated against typed schemas at the trust boundary.
- Client-side validation is for UX only. Never rely on it for security.
- Parameterized queries always. String concatenation for SQL is a blocking defect.
- File uploads: validate MIME type (magic bytes, not extension), enforce size
  limits, scan for malware (Azure Defender for Storage or ClamAV sidecar).
- URL inputs: allowlist permitted domains, validate redirect targets against a
  known-safe list to prevent open redirect attacks.

### 3.2 Secrets Management

- **NO secrets in code, config files, or environment variables.** This is
  enforced via pre-commit hooks and CI/CD secret scanning.
- All secrets, keys, and certificates reside in **Azure Key Vault**.
- Service-to-service authentication uses **managed identities** (zero secrets).
- Key rotation policy: automated rotation where supported. Manual rotation
  cadence: 90 days maximum.
- Secret scanning tools run in every CI/CD pipeline: GitHub Advanced Security
  (push protection), Credential Scanner, or equivalent.
- If a secret is detected in source control, it is rotated immediately and the
  commit history is cleaned.

### 3.3 Dependency Security

- Automated dependency scanning is mandatory: Dependabot (GitHub), Snyk, or
  OWASP Dependency-Check.
- Dependency versions are pinned via lockfiles: `package-lock.json`,
  `requirements.txt` with hashes, `Directory.Packages.props` for .NET.
- Vulnerability patching cadence:
  - **Critical** (CVSS >= 9.0): patched within **24 hours**
  - **High** (CVSS 7.0–8.9): patched within **7 days**
  - **Medium** (CVSS 4.0–6.9): patched within **30 days**
  - **Low** (CVSS < 4.0): patched in next scheduled release
- Container images are scanned on build (Trivy, Azure Defender for Containers)
  and rejected if critical vulnerabilities are found.
- Supply chain security: use signed packages, generate SBOM (CycloneDX or SPDX
  format), verify provenance with SLSA framework where available.

### 3.4 Secure Coding Patterns

**C#: Result type with explicit error handling**:

```csharp
// GOOD: Explicit result type, no hidden exceptions, no null returns
public static Result<User, AuthError> Authenticate(Credentials credentials)
    => ValidateCredentials(credentials)
        .Bind(creds => VerifyPassword(creds))
        .Bind(user => CheckAccountLocked(user))
        .Bind(user => GenerateToken(user));

// BAD: Exception swallowing with null return; hides failures
public User Authenticate(string username, string password) {
    try { ... } catch (Exception ex) { return null; } // NEVER DO THIS
}
```

**TypeScript: Zod schema validation at boundary**:

```typescript
// GOOD: Typed schema validation at API boundary
const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s]+$/),
  role: z.enum(["user", "admin", "viewer"]),
});

// Validate at boundary, propagate typed result
const result = CreateUserSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json(formatZodError(result.error));
}
const validatedUser = result.data; // Fully typed from here
```

**Python: Pydantic model with strict validation**:

```python
# GOOD: Immutable, validated, typed at the boundary
class CreateUser(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z\s]+$")
    role: Literal["user", "admin", "viewer"]

    model_config = ConfigDict(frozen=True)  # Immutable after creation
```

### 3.5 OWASP Top 10 Checklist

Every design MUST address all ten categories. This table maps each category to
required controls.

| # | Category | Required Controls |
|---|----------|-------------------|
| 1 | **Broken Access Control** | RBAC/ABAC at every API. Authorization checks at service boundary. Deny by default. |
| 2 | **Cryptographic Failures** | TLS 1.3 in transit. AES-256 at rest. Key Vault for key management. No custom crypto. |
| 3 | **Injection** | Parameterized queries. ORM usage. Input validation at boundary. CSP headers for XSS. |
| 4 | **Insecure Design** | Threat modeling (STRIDE). Abuse cases in requirements. Security as a first-class requirement, not an afterthought. |
| 5 | **Security Misconfiguration** | IaC validation (tflint, checkov). Azure Policy guardrails. CIS benchmarks applied. No default credentials. |
| 6 | **Vulnerable Components** | Dependency scanning. Automated patching. SBOM generation. Container image scanning. |
| 7 | **Authentication Failures** | Entra ID (no custom auth). MFA enforced. Token validation (issuer, audience, expiry). Secure session management. |
| 8 | **Data Integrity Failures** | Signed CI/CD artifacts. Integrity checks on deployments. No unsigned code in production. Pipeline protection rules. |
| 9 | **Logging Failures** | Structured logging (JSON). Audit trails for all auth events. SIEM integration (Sentinel). No secrets in logs. |
| 10 | **SSRF** | URL validation with allowlists. Network isolation (private endpoints). Deny outbound by default from application subnets. |

---

## 4. Secure at Execution

### 4.1 Runtime Protection

- **Azure Defender for Cloud**: enabled for all subscriptions. Provides threat detection
  across VMs, containers, storage, SQL, Key Vault, DNS, and App Service.
- **Microsoft Sentinel**: SIEM + SOAR for security operations. Connected to all
  Azure diagnostic logs, Entra ID sign-in logs, and application audit logs.
- **Container hardening** (AKS):
  - Non-root user (`runAsNonRoot: true`, `runAsUser: 1000`)
  - Read-only root filesystem (`readOnlyRootFilesystem: true`)
  - No privilege escalation (`allowPrivilegeEscalation: false`)
  - Dropped capabilities (`drop: ["ALL"]`)
  - Pod Security Standards enforced at namespace level (restricted profile)
- **API protection**: Rate limiting via APIM policies (per-subscription, per-IP).
  Throttling with retry-after headers. KEDA-based autoscaling for burst handling.
- **DDoS protection**: Azure DDoS Protection Standard enabled on VNets hosting
  public-facing resources.

### 4.2 Encryption

| Scope | Standard | Implementation |
|-------|----------|----------------|
| **In transit** | TLS 1.3 minimum | Enforced via Azure Front Door, App Gateway, and service configuration. TLS 1.0/1.1 disabled globally. |
| **At rest** | AES-256 | Azure SSE for Storage, TDE for SQL/Cosmos DB, platform encryption for all other services. |
| **In use** | Confidential computing | Azure Confidential VMs or enclaves for Highly Confidential workloads requiring processing-time protection. |
| **Key management** | Azure Key Vault (FIPS 140-2 Level 2; HSM for Level 3) | Service-managed keys for Confidential and below. Customer-managed keys (CMK) mandatory for Highly Confidential. |
| **Certificates** | Key Vault certificates | Auto-renewal enabled. Minimum RSA-2048 or P-256 EC. Wildcard certs prohibited in production. |

### 4.3 Monitoring and Incident Response

- **Security logging**: All resources emit diagnostic logs to Azure Monitor and
  Log Analytics workspace. Retention: minimum 90 days hot, 1 year cold.
- **Alert rules** (mandatory):
  - Failed authentication attempts (threshold: 10 in 5 minutes)
  - Privilege escalation events (any role assignment change)
  - Data exfiltration patterns (bulk download, unusual egress)
  - Key Vault access anomalies (unexpected principal, unusual operation)
  - Resource configuration changes (policy non-compliance)
- **Automated response**: Sentinel playbooks (Logic Apps) for:
  - Blocking IP addresses after brute-force detection
  - Disabling compromised service principals
  - Notifying SOC team via Teams/email
  - Isolating compromised VMs from the network
- **Incident response lifecycle**:
  1. **Detect**: Sentinel alert or Defender for Cloud finding
  2. **Triage**: Severity classification (P1–P4), assign responder
  3. **Contain**: Isolate affected resources, revoke compromised credentials
  4. **Eradicate**: Remove threat actor artifacts, patch vulnerability
  5. **Recover**: Restore from known-good state, validate integrity
  6. **Review**: Post-incident review within 48 hours, update runbooks
- **Penetration testing**: Scheduled quarterly for internet-facing components.
  Annual full-scope assessment for the entire platform.

### 4.4 Compliance Controls

- **Azure Policy**: Enforced via Terraform. Policies include:
  - Deny public blob access on storage accounts
  - Require HTTPS on all web apps and APIs
  - Enforce minimum TLS version 1.2 (target 1.3)
  - Require resource tags (environment, owner, data-classification, cost-center)
  - Deny creation of resources outside approved regions
- **Microsoft Purview**: Data governance, classification scanning, and data
  lineage for all data stores containing Confidential or Highly Confidential data.
- **Compliance Manager**: Regulatory alignment dashboards for SOC 2, ISO 27001,
  HIPAA, GDPR, and PCI-DSS. Control mapping to Azure services documented.
- **Data residency**: Azure regions selected per customer requirements. Geo-
  redundancy configured only within approved geographies. Cross-region replication
  policies documented in the design.
- **Data retention and deletion**: Retention policies defined per data
  classification. Automated deletion via lifecycle management policies.
  Right-to-erasure (GDPR Art. 17) workflows for PII.

### 4.5 Infrastructure Security (Terraform)

```hcl
# Secure defaults for storage: every storage account must follow this pattern
resource "azurerm_storage_account" "main" {
  name                          = "stexample"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  account_tier                  = "Standard"
  account_replication_type      = "GRS"
  min_tls_version               = "TLS1_2"
  https_traffic_only_enabled    = true
  public_network_access_enabled = false
  shared_access_key_enabled     = false  # Use Entra ID auth only

  blob_properties {
    delete_retention_policy {
      days = 30
    }
    container_delete_retention_policy {
      days = 30
    }
  }

  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices"]
    ip_rules       = []  # No public IPs; access via private endpoint only
  }
}

# Private endpoint: required for all PaaS services in production
resource "azurerm_private_endpoint" "storage" {
  name                = "pe-stexample"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "psc-stexample"
    private_connection_resource_id = azurerm_storage_account.main.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}
```

---

## 5. Security Validation Checklist

This is the master checklist that ALL skills (agent, odin,
spec) MUST execute when validating a design. A design is not approved until
every applicable item is checked.

### Design-Time Security

- [ ] Threat model (STRIDE) completed for all public-facing components and trust boundary crossings
- [ ] Data classification applied to ALL data stores and data flows
- [ ] Authentication architecture defined: Entra ID for users, managed identity for services
- [ ] Authorization model defined: RBAC/ABAC with least privilege, deny by default
- [ ] Network security: private endpoints for all PaaS services, no public access to data stores
- [ ] Encryption: TLS 1.3 in transit, AES-256 at rest, Key Vault for all key management
- [ ] API security: OAuth 2.0 scopes, rate limiting, input validation at API boundary
- [ ] No shared secrets or password-based service accounts in the design

### Code-Time Security

- [ ] Input validation at every external boundary (Zod, FluentValidation, Pydantic)
- [ ] No secrets in code, config, or environment variables; Key Vault and managed identity only
- [ ] Parameterized queries for all database access; no string concatenation
- [ ] Dependency scanning configured in CI/CD pipeline with blocking on critical vulnerabilities
- [ ] Container images scanned and signed before deployment to any environment
- [ ] OWASP Top 10 addressed for every web-facing and API component
- [ ] Pre-commit hooks for secret detection enabled in all repositories
- [ ] SBOM generated and stored for every release artifact

### Execution-Time Security

- [ ] Azure Defender for Cloud enabled on all subscriptions
- [ ] Security logging flowing to centralized SIEM (Microsoft Sentinel)
- [ ] DDoS protection enabled for all public-facing endpoints
- [ ] Runtime containers: non-root, read-only filesystem, dropped capabilities, security contexts
- [ ] Certificate auto-renewal configured in Key Vault
- [ ] Incident response runbook documented and tested
- [ ] Rate limiting and throttling configured on all public APIs
- [ ] Automated alerting for failed auth, privilege changes, and anomalous data access

### Compliance

- [ ] Regulatory requirements (SOC 2, ISO 27001, HIPAA, GDPR, PCI-DSS) mapped to specific controls
- [ ] Azure Policy guardrails enforced via Terraform; no manual policy exceptions
- [ ] Data residency constraints satisfied; resources deployed only in approved regions
- [ ] Audit logging meets regulatory retention requirements (minimum 90 days hot, 1 year archive)
- [ ] Data retention and deletion policies defined and automated per classification
- [ ] Penetration testing schedule established (quarterly for public-facing, annual full-scope)

---

## Cross-Skill Usage

| Skill | How This Reference Is Used |
|-------|---------------------------|
| **agent** | Validates that HLD and LLD artifacts satisfy all Design-Time and Compliance checklist items. Embeds STRIDE tables in design documents. |
| **odin** | Reviews architecture decisions against security principles. Flags violations of Zero Trust, Least Privilege, and Secure Defaults during design reviews. |
| **spec** | Generates specification documents that include security requirements derived from this reference. Ensures every API spec includes authentication, authorization, input validation, and rate limiting sections. |

**Enforcement**: If a design artifact is missing any required security control
from this document, the validating skill MUST reject the artifact and provide
specific remediation guidance referencing the applicable section of this file.
