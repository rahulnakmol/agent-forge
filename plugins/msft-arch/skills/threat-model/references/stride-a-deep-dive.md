# STRIDE-A Deep Dive

STRIDE-A extends Microsoft's classic STRIDE threat model with an Abuse (A) category that captures AI-specific attack vectors. This file provides technique-level guidance for applying each category and a worked example against a concrete Azure architecture. The canonical worksheet template and severity guide live in `standards/references/security/stride-a-worksheet.md`. Read that file before running a session; do not reproduce it here.

---

## Category-by-Category Technique Guide

### S: Spoofing

Spoofing attacks impersonate a legitimate identity: a user, a service, or a system component. The violated security property is Authentication.

**Common Azure attack vectors:**

- **Credential theft via phishing or adversarial credential reuse**: attacker obtains an Entra ID user's credentials and authenticates to the management plane or application.
- **Service principal secret exfiltration**: a CI/CD pipeline secret or app registration client secret exposed in a repository is used to authenticate as the service principal with its full set of RBAC permissions.
- **Shared Access Signature (SAS) token leakage**: a time-limited SAS URI embedded in a log file or URL parameter is used to authenticate to Azure Blob Storage without an identity token.
- **Token replay**: a JWT access token captured in transit (insufficient TLS, debug logging) is replayed within its validity window.
- **Managed Identity impersonation**: an attacker who has obtained code execution on a compute resource can call the Instance Metadata Service (IMDS) endpoint to retrieve a Managed Identity token for any resource the identity is authorized to access.

**Primary mitigations:**

| Attack vector | Azure control | Code / config control |
|---|---|---|
| Credential theft | Entra ID Conditional Access + MFA; PIM for privileged roles | N/A (platform control) |
| Service principal secret | GitHub / ADO secret scanning + push protection; Key Vault reference syntax in all app configs | Rotate secrets on detection; prefer Workload Identity Federation (no secret) |
| SAS token leakage | Managed Identity + RBAC instead of SAS wherever supported; SAS token scope: minimum permissions, short TTL | Avoid logging SAS URIs; use User Delegation SAS (Entra-backed) |
| Token replay | Short-lived access tokens (1-hour default); enforce TLS 1.2+ everywhere | Validate `aud`, `iss`, `nbf`, `exp` claims in JWT middleware |
| IMDS token abuse | Restrict Managed Identity to narrowest RBAC scope; prefer User-Assigned MI per workload | Monitor IMDS call patterns via Defender for Cloud |

**Detection signals:** Entra ID sign-in risk alerts (impossible travel, anonymous IP); Defender for Cloud "Suspicious authentication activity" alerts; Key Vault access anomalies via Defender for Key Vault.

---

### T: Tampering

Tampering attacks modify data in transit or at rest without authorization. The violated security property is Integrity.

**Common Azure attack vectors:**

- **Connection string injection**: an inline connection string in application settings is overwritten by an attacker who has gained access to the App Service configuration plane.
- **Man-in-the-middle on internal traffic**: service-to-service calls within a VNet that do not enforce TLS are intercepted and the payload modified.
- **Storage account key compromise**: a leaked storage account key is used to overwrite or corrupt blobs.
- **Database record tampering**: an application with overly broad SQL permissions (db_owner instead of a custom role) allows an attacker who has compromised the app identity to issue arbitrary UPDATE/DELETE statements.
- **Configuration drift**: an IaC-managed resource is manually modified outside the Terraform state, introducing a misconfiguration that weakens security controls (e.g., disabling private endpoint enforcement).

**Primary mitigations:**

| Attack vector | Azure control | Code / config control |
|---|---|---|
| Connection string injection | Key Vault reference syntax in all App Service / Container Apps config; managed HSM for secrets requiring FIPS 140-2 L3 | Never store secrets in appsettings.json or environment variables inline |
| MitM on internal calls | Enforce TLS 1.2+ on all service-to-service; Private Endpoints eliminate public routing | Certificate pinning for high-value service calls; mutual TLS where supported |
| Storage key compromise | Managed Identity + RBAC (Storage Blob Data Contributor); disable shared key access after confirmed healthy | Use `DefaultAzureCredential`; never pass storage keys in code |
| Database tampering | Least-privilege SQL login per workload; db_datareader / db_datawriter custom roles | Parameterized queries only; no dynamic SQL construction |
| Configuration drift | Terraform + AVM; enforce deny-assignment or policy to block manual changes to security-critical resources | Lock production resource groups; run `terraform plan` in PR pipelines |

**Detection signals:** Azure Policy compliance reports for configuration drift; Defender for Storage anomalous write alerts; Diagnostic logs on App Service configuration changes (Azure Activity Log).

---

### R: Repudiation

Repudiation threats arise when a user or service can deny performing an action because no immutable audit trail exists. The violated security property is Non-repudiation.

**Common Azure attack vectors:**

- **Audit log deletion**: an identity with Log Analytics Contributor or Contributor at workspace scope can delete log tables, erasing evidence of malicious activity.
- **Diagnostic setting removal**: a Contributor can remove diagnostic settings from a resource, cutting off the log pipeline before an attack reaches the SIEM.
- **Shared account actions**: multiple people sharing a single service account or app registration mean individual actions cannot be attributed.
- **Log forwarding gap**: logs are written to a storage account but not forwarded to Log Analytics; the storage account retention period expires before an investigation begins.

**Primary mitigations:**

| Attack vector | Azure control | Code / config control |
|---|---|---|
| Audit log deletion | Log Analytics workspace with immutable data retention (table-level locks); Microsoft Sentinel ingests to a separate immutable tier | Never grant Log Analytics Contributor to application identities |
| Diagnostic setting removal | Azure Policy to enforce diagnostic settings (deny effect); alert on activity log events for `microsoft.insights/diagnosticsettings/delete` | Codify all diagnostic settings in Terraform; detect drift via policy |
| Shared accounts | Managed Identity per workload (inherently attributed); PIM for human admins (individual Entra accounts only) | Prohibit service account credentials shared across workloads |
| Log forwarding gap | Log Analytics retention ≥ 90 days for standard; WORM storage (immutable blob policy) for regulated retention requirements | Set retention policy in Terraform; alert if diagnostic setting health check fails |

**Detection signals:** Azure Activity Log: changes to diagnostic settings; Microsoft Sentinel analytics rule for log gap detection; Defender for Cloud recommendation "Diagnostic logs should be enabled."

---

### I: Information Disclosure

Information disclosure threats expose sensitive data to unauthorized parties. The violated security property is Confidentiality.

**Common Azure attack vectors:**

- **Overly broad API response**: an API endpoint returns all fields of a database entity, including fields the requesting caller is not authorized to see (PII, internal IDs, hashed credentials).
- **Public blob container**: a Storage account with `AllowBlobPublicAccess = true` exposes files intended to be private.
- **Exception details in HTTP responses**: unhandled exceptions propagate stack traces, connection strings, or internal paths to the client.
- **Log-level PII exposure**: structured logging includes user-identifiable fields (email, phone, SSN) at DEBUG level that flow into Log Analytics and are visible to anyone with Log Analytics Reader.
- **Cross-tenant data leakage**: in a multi-tenant SaaS, a missing `tenantId` filter in a LINQ query returns records belonging to another tenant.

**Primary mitigations:**

| Attack vector | Azure control | Code / config control |
|---|---|---|
| Overly broad API response | APIM policies for response-body transformation; API response shaping | Apply `[JsonIgnore]` / field-level projection; never return `SELECT *` mapped to DTOs without explicit field selection |
| Public blob container | Azure Policy (deny) for `AllowBlobPublicAccess`; Defender for Storage anomalous access alerts | Disable public access at storage account level; use SAS or MI for legitimate external access |
| Exception details | App Insights: exceptions forwarded to telemetry, not client | Global exception handler returns RFC 7807 `ProblemDetails`; no stack traces; log internally |
| Log-level PII | Log Analytics workspace RBAC; scrub or hash PII before logging | Use structured logging with explicit field allow-lists; never log raw request bodies |
| Cross-tenant leakage | N/A (application logic) | Resource-based authorization in every data access path; integrate `tenantId` claim into every query predicate; test with multi-tenant integration tests |

**Detection signals:** Defender for Storage: anomalous access, mass download; Defender for SQL: unusual query patterns; App Insights: exception rate spikes.

---

### D: Denial of Service

DoS threats make the system unavailable to legitimate users. The violated security property is Availability.

**Common Azure attack vectors:**

- **Volumetric DDoS**: high-volume traffic floods public endpoints, exhausting bandwidth or compute capacity.
- **Application-layer (L7) DoS**: low-and-slow HTTP requests or expensive query patterns (e.g., unbounded joins, deeply nested GraphQL) exhaust application threads or database connections.
- **Token flood**: an unauthenticated or cheaply authenticated endpoint is hammered to exhaust downstream token budgets (Azure OpenAI TPM limits, APIM quotas).
- **Queue poisoning**: malformed messages injected into a Service Bus or Event Hub queue cause repeated processing failures, blocking the queue and starving legitimate consumers.
- **Certificate expiry**: an expired TLS certificate causes all callers to fail connection, producing an availability outage without any attacker action.

**Primary mitigations:**

| Attack vector | Azure control | Code / config control |
|---|---|---|
| Volumetric DDoS | Azure DDoS Protection Standard on the hub VNet; Front Door WAF (OWASP 3.2) for global HTTP; Application Gateway WAF for regional | N/A (platform control) |
| L7 DoS | APIM rate-limiting policies (per IP, per subscription, per product); App Service auto-scale rules | Pagination on all list endpoints; query cost limits; connection pool max-size configuration |
| Token flood | APIM rate limiting on AI endpoints; Azure OpenAI token-per-minute (TPM) limits per deployment | Authenticate every AI-endpoint caller; log per-user token consumption |
| Queue poisoning | Service Bus dead-letter queue with max-delivery-count ≤ 10; alert on dead-letter queue depth | Validate message schema before processing; poison-message handler with backoff |
| Certificate expiry | Key Vault certificate auto-renewal (DigiCert / Let's Encrypt); Defender for App Service: dangling DNS / cert alerts | Monitor certificate expiry in pipeline; alert at 30 days and 7 days before expiry |

**Detection signals:** Azure Monitor: App Service HTTP 5xx spike; APIM: request rate alerts; DDoS Protection: mitigation active notifications; Application Gateway: blocked request rate.

---

### E: Elevation of Privilege

Elevation threats allow a low-privilege actor to gain higher-privilege access than intended. The violated security property is Authorization.

**Common Azure attack vectors:**

- **IDOR (Insecure Direct Object Reference)**: a user passes another user's resource ID (e.g., `/api/orders/12345`) in an API call; the application checks authentication but not authorization (whether the caller owns order 12345).
- **RBAC role over-assignment**: a workload identity is assigned Contributor or Owner at subscription scope rather than the minimum required role at the minimum required scope.
- **PIM bypass**: a privileged role is permanently assigned to a user account instead of activated on-demand via PIM, extending the blast radius of account compromise.
- **Broken function-level access control**: an administrative API endpoint is only hidden from the UI but not guarded by a server-side authorization check.
- **JWT claim manipulation**: a JWT that is not cryptographically validated server-side allows an attacker to modify the `roles` or `scp` claim to claim permissions they were not granted.

**Primary mitigations:**

| Attack vector | Azure control | Code / config control |
|---|---|---|
| IDOR | N/A (application logic) | Resource-based authorization on every endpoint (`IAuthorizationHandler` in ASP.NET Core); never trust caller-supplied resource IDs without ownership verification |
| RBAC over-assignment | Azure Policy (deny) for Owner / Contributor assignment at subscription scope for non-admin identities; use built-in least-privilege roles | Document every RBAC assignment in Terraform with a justification comment |
| PIM bypass | Require PIM activation for all privileged Entra ID roles; no permanent GA/Owner assignments except break-glass | Automate PIM assignment review quarterly via Access Reviews |
| Function-level access | APIM subscription key + policy-based auth per API product | Enforce authorization at the method level, not just the controller level; integration tests with denied callers |
| JWT manipulation | Entra ID token validation (app validates signature, issuer, audience, expiry) | Use `Microsoft.Identity.Web` token validation middleware; never accept unsigned JWTs for authorization decisions |

**Detection signals:** Entra ID: sign-in events with unexpected roles; Defender for Cloud: over-privileged identity recommendations; Azure Activity Log: RBAC assignment changes.

---

### A: Abuse (AI Extension)

Abuse threats arise specifically from incorporating language models, embedding models, or autonomous AI agents into a system. These do not map cleanly to classic STRIDE categories because the attack surface is the model's behavior, not only the data or transport layer. See the full Abuse threat patterns in `standards/references/security/stride-a-worksheet.md`.

**Primary sub-categories:**

| Sub-category | Threat | Violated property |
|---|---|---|
| Prompt injection (direct) | Attacker types instructions into the chat UI to override the system prompt | Trustworthiness / Integrity |
| Prompt injection (indirect) | Attacker plants instructions in a document, email, or database record that the agent retrieves and executes | Trustworthiness / Integrity |
| Model exfiltration / inversion | Attacker reconstructs training data, system prompts, or proprietary fine-tuning content through repeated queries | Confidentiality |
| Jailbreaks | Adversarial prompt patterns bypass content safety policy | Trustworthiness |
| Training-data poisoning | User-submitted content shifts model behavior in a RAG corpus or fine-tuning dataset | Integrity / Trustworthiness |
| Agent tool misuse | Agent is manipulated to invoke tools (delete, send email, post HTTP) outside its intended operational scope | Availability / Integrity |
| Wallet attacks | Prompt injection causes the agent to make excessive API calls, exhausting token budgets or triggering large cloud charges | Availability |

**Primary mitigations:**

| Sub-category | Azure / platform control | Code / architecture control |
|---|---|---|
| Prompt injection (direct + indirect) | Azure AI Content Safety prompt shields (GA); Foundry spotlighting (2025 GA) for real-time injection detection | Structurally separate system prompt from user content (different message roles); output schema validation |
| Model exfiltration | APIM rate limiting per user; Defender for AI threat detection (GA: activity monitoring, prompt evidence) | Never include PII or proprietary secrets in system prompts; monitor for patterned queries |
| Jailbreaks | Azure OpenAI built-in safety system; Content Safety moderation layer | Log all model I/O; alert on content policy violations; treat as security incident |
| Training-data poisoning | Defender for AI: supply chain risk detection; data provenance tracking | Validate and sanitize all content before RAG ingestion; monitor output drift metrics |
| Agent tool misuse | Microsoft Entra Agent ID: Conditional Access for agents; tool-scoping via agent policy (Foundry / Copilot Studio) | Apply least-privilege tool lists; require human approval for high-impact tool actions |
| Wallet attacks | Azure OpenAI TPM / RPM limits per deployment; APIM cost-guard policies | Per-user token budget enforcement; alert on anomalous token consumption |

**Detection signals:** Defender for AI Services (GA): jailbreak detection, data leakage, credential theft alerts; Defender XDR: AI incident correlation; Foundry continuous evaluation and monitoring; Microsoft Entra Agent ID: agent risk management (preview).

---

## Worked Example: App Service + Cosmos DB + Entra ID Authentication

### Architecture

```text
Internet
  |
Azure Front Door + WAF (OWASP 3.2, Prevention mode)
  |
App Service (ASP.NET Core, Managed Identity: SystemAssigned)
  |--- Entra ID (user authentication via MSAL, JWT validation via Microsoft.Identity.Web)
  |--- Azure Cosmos DB (NoSQL API; RBAC: Cosmos DB Built-in Data Contributor scoped to the account)
  |--- Azure Key Vault (Key Vault Secrets User; connection strings for legacy dependencies)
  |--- Azure OpenAI Service (Cognitive Services OpenAI User; chat completions endpoint)
  |
Log Analytics Workspace + App Insights
```

Trust boundaries: Internet → Front Door, Front Door → App Service, App Service → Cosmos DB, App Service → Azure OpenAI, App Service → Key Vault.

### STRIDE-A Assessment (selected rows)

| Asset / Data Flow | Category | Threat | Existing Control | Mitigation Required | Severity |
|---|---|---|---|---|---|
| Entra ID JWT → App Service | **S** Spoofing | Attacker forges or replays an Entra ID JWT to authenticate as a legitimate user | `Microsoft.Identity.Web` validates signature, audience, issuer, expiry | Enforce token binding; short access token lifetime (≤ 1 hour); Conditional Access: compliant device + MFA | High |
| App Service → Cosmos DB | **T** Tampering | App identity assigned write access to the entire Cosmos DB account; a compromised app can overwrite any document | Managed Identity (no shared key) | Scope RBAC to the specific database and container; use custom role with `dataActions` limited to required paths | High |
| App Service → Log Analytics | **R** Repudiation | Diagnostic logs not flowing; attacker disables diagnostic setting post-compromise | Diagnostic setting configured in Terraform | Azure Policy (deny) for diagnostic setting deletion; immutable table retention on Log Analytics workspace | Critical |
| Cosmos DB | **I** Info Disclosure | Application returns full Cosmos DB document (including internal fields and other-tenant data) in API response | Entra ID authentication enforced on API | Apply tenant-scoped LINQ queries on every data access method; explicit DTO projection (no `Select * from c`); response-body transformation in APIM | Critical |
| Front Door | **D** DoS | Volumetric DDoS on the public Front Door endpoint exhausts origin capacity | Front Door WAF in Detection mode | Promote WAF to Prevention mode after 2-week false-positive review; enable DDoS Protection Standard; APIM rate-limit per subscription | High |
| Cosmos DB RBAC assignment | **E** Elevation | App Service identity assigned Cosmos DB Contributor (manages account settings) instead of Data Contributor (data only) | Managed Identity (no password) | Re-scope assignment to `Cosmos DB Built-in Data Contributor` at the specific account/database scope; deny-assignment policy for Contributor on data plane | High |
| Azure OpenAI chat endpoint | **A** Abuse | Indirect prompt injection: user uploads a PDF containing adversarial instructions; the app summarizes the PDF using Azure OpenAI, and the injected instructions override the system prompt | Azure OpenAI content filter (default) | Enable Azure AI Content Safety prompt shields; structurally separate retrieved content from system prompt using distinct `role: user` messages; validate structured output schema before acting on response | Critical |
| Azure OpenAI chat endpoint | **A** Abuse | Wallet attack: unauthenticated callers enumerate the Azure OpenAI endpoint directly (URL discovered in client-side JavaScript) and exhaust the TPM deployment limit | APIM subscription key on the API surface | Enforce APIM policy: validate Entra ID JWT before forwarding to Azure OpenAI; per-user TPM budget enforcement; alert at 80% TPM consumption | High |

### Attack Tree: Indirect Prompt Injection → PII Exfiltration

```text
Goal: Extract PII records from Cosmos DB via manipulated AI agent response
|
+-- Sub-goal: Inject adversarial instruction into the AI agent's context
|   |
|   +-- Attack: Embed instruction in a user-uploaded document
|   |   [Feasibility: High; app accepts PDF/DOCX uploads]
|   |   [Existing control: None on document content]
|   |   [Residual risk: Critical]
|   |
|   +-- Attack: Embed instruction in a database record the agent queries
|       [Feasibility: Medium; requires prior write access to the record]
|       [Existing control: Tenant-scoped writes]
|       [Residual risk: High]
|
+-- Sub-goal: Cause agent to issue unauthorized Cosmos DB query
|   [Feasibility: High if injection succeeds; agent has Cosmos DB read access]
|   [Existing control: Tool-scoping not yet implemented]
|   [Residual risk: Critical]
|
+-- Sub-goal: Exfiltrate query result to attacker-controlled endpoint
    [Feasibility: Medium; agent must have outbound HTTP tool or email tool]
    [Existing control: Agent outbound restricted to approved tool list (PARTIAL)]
    [Residual risk: High]
```

**Mitigations targeting the attack tree root:**
1. Structurally isolate retrieved document content from system-prompt channel (breaks Sub-goal 1, Attack 1).
2. Apply Azure AI Content Safety prompt shields at the API layer (detects and blocks Sub-goal 1 at the platform boundary).
3. Scope agent tool list to read-only Cosmos DB queries against the authenticated user's own tenant (severs Sub-goal 2 for cross-tenant exfiltration).
4. Require human confirmation for any agent action that produces outbound HTTP calls (blocks Sub-goal 3).

### Mitigation Backlog (severity-ordered)

| Mitigation | STRIDE-A category | Severity | Owner | Sprint |
|---|---|---|---|---|
| Enable Azure AI Content Safety prompt shields on Azure OpenAI endpoint | A | Critical | AI/Platform team | Current |
| Immutable Log Analytics retention + Azure Policy deny for diagnostic setting deletion | R | Critical | Ops/Infra team | Current |
| Tenant-scoped LINQ queries on every Cosmos DB data access; explicit DTO projection | I | Critical | API team | Current |
| Promote Front Door WAF to Prevention mode + DDoS Protection Standard | D | High | Infra team | Current |
| Re-scope Cosmos DB RBAC from Contributor to Data Contributor | E | High | Infra team | Current |
| APIM per-user JWT validation + TPM budget policy for Azure OpenAI | A | High | Platform/API team | Current |
| Agent tool-scoping: read-only Cosmos DB; human approval for outbound HTTP | A | High | AI team | Sprint + 1 |
| Cosmos DB tenant-scope validation integration tests | I | High | API team | Sprint + 1 |
| Short access token lifetime enforcement via Conditional Access | S | High | Identity team | Sprint + 1 |
| Output schema validation for all Azure OpenAI responses before acting | A | Medium | AI team | 30 days |

---

## Incremental Maintenance Protocol

A threat model is never done. The following ADR and architecture-change events trigger a delta review, not a full restart, of the relevant STRIDE-A rows:

| Trigger event | Delta review scope |
|---|---|
| New external-facing API endpoint added | S (authentication), I (response shaping), D (rate limiting) rows for the new endpoint |
| AI agent added or agent tool list expanded | Full A (Abuse) section; update attack tree for any new tool that provides data write or outbound HTTP |
| New data store or data classification change | I (Info Disclosure), T (Tampering) rows for the new store; update blast-radius table |
| New trust boundary (VNet peering, service endpoint, private endpoint added) | Full STRIDE-A row for the new data flow across the boundary |
| Regulatory scope change (HIPAA added, GDPR SCCs updated) | Blast-radius table recalculation; LINDDUN supplement if special-category data newly in scope |
| New Entra ID role assignment or Managed Identity scope change | E (Elevation) rows; RBAC minimisation check |
| Dependency version update introducing known CVE | T (Tampering) and D (DoS) rows if the CVE is in a network-facing or data-processing dependency |
