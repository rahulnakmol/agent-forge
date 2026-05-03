# Threat Library by Domain

This file provides a per-domain threat library matrix that maps architecture domains to their highest-priority threat techniques, applicable libraries (MITRE ATT&CK Cloud, MITRE ATLAS), OWASP coverage, and canonical mitigations. Use this as a quick-start enumeration guide at the beginning of a threat modeling session to ensure no major threat category is missed for the architecture in scope.

---

## How to Use This Matrix

1. Identify the primary architecture domain(s) from the discovery brief.
2. Look up the domain row to get the starting set of threat techniques.
3. Supplement with technique details from `references/mitre-attack-cloud.md` (cloud techniques) or `references/mitre-atlas-ai.md` (AI/ML techniques).
4. Apply the STRIDE-A worksheet from `standards/references/security/stride-a-worksheet.md` to each trust boundary identified in the C4 Level 2 diagram.
5. For AI domains, run the OWASP ASI Top-10 checklist from `references/owasp-asi-top10.md`.

---

## Domain 1: Web Application (App Service + Entra ID + Azure SQL)

**Typical stack:** ASP.NET Core / Node.js on App Service; Entra ID for authentication; Azure SQL Database for OLTP; APIM or Front Door as API gateway; Key Vault for secrets.

### Top STRIDE-A Threats

| STRIDE-A Category | Highest-risk threat | Primary control |
|---|---|---|
| S: Spoofing | Credential stuffing against Entra ID login | Conditional Access + MFA; Smart Lockout; Entra ID Identity Protection |
| T: Tampering | SQL injection via unsanitised user input | Parameterised queries in EF Core; WAF OWASP 3.2 SQL injection rules |
| R: Repudiation | User denies posting a harmful comment or initiating a transaction | Immutable application log with user ID, timestamp, and request payload hash; Entra ID audit log |
| I: Info Disclosure | API returning PII in excess of what the caller is authorised to see | Response shaping middleware; `[JsonIgnore]` on sensitive fields; APIM response transformation |
| D: DoS | L7 application-layer DoS via expensive query patterns | APIM rate limiting per subscription; EF Core query cost limits; Front Door WAF in Prevention mode |
| E: Elevation | IDOR: authenticated user accesses another user's resources by guessing IDs | Resource-based authorization on every data access method; no sequential / guessable IDs in public APIs (use UUIDs) |
| A: Abuse | N/A (no AI components); mark A column N/A and revisit when AI is introduced | N/A |

### MITRE ATT&CK Cloud Techniques (High Priority)

| Technique ID | Technique | Priority |
|---|---|---|
| T1190 | Exploit Public-Facing Application | Critical: first entry point |
| T1078 | Valid Accounts (credential attack on Entra ID) | Critical |
| T1552.001 | Credentials in Files (connection strings committed to repo) | High |
| T1530 | Data from Cloud Storage (misconfigured blob container) | High |
| T1098.001 | Additional Cloud Credentials (persistence after initial compromise) | High |
| T1562.008 | Disable or Modify Cloud Logs (disable diagnostic settings) | Medium |

### OWASP Top-10 Priority Items (Traditional Web)

OWASP 2021 items relevant to this domain, in priority order:
1. A01 Broken Access Control: IDOR, missing function-level authorization
2. A02 Cryptographic Failures: PII in cleartext, weak TLS configuration
3. A03 Injection: SQL, NoSQL, LDAP injection via user input
4. A07 Identification and Authentication Failures: brute force, session fixation
5. A08 Software and Data Integrity Failures: dependency vulnerabilities, SBOM gaps

---

## Domain 2: API Platform (APIM + Azure Functions + Cosmos DB)

**Typical stack:** Azure API Management as gateway; Azure Functions (consumption or premium) as backend compute; Cosmos DB (NoSQL API) for document storage; Managed Identity for service-to-service auth; Event Grid or Service Bus for async messaging.

### Top STRIDE-A Threats

| STRIDE-A Category | Highest-risk threat | Primary control |
|---|---|---|
| S: Spoofing | API key theft (shared API key embedded in client-side application) | Entra ID JWT validation per API product; deprecate shared API keys for authenticated workloads |
| T: Tampering | Malformed message payloads in Event Grid / Service Bus causing unexpected Function behaviour | Schema validation on message receipt; dead-letter queue with max-delivery-count ≤ 10 |
| R: Repudiation | Asynchronous event processing leaves no correlation between the API call and the downstream Function execution | Distributed trace ID propagated through Event Grid metadata; App Insights correlation |
| I: Info Disclosure | Cosmos DB query returning all partition documents when tenant filter is missing | Tenant-scoped partition key in every Cosmos DB query; cross-partition query disabled in production |
| D: DoS | Unbounded Function invocation via malformed Event Grid events | Event Grid subscription filter rules; Function dead-letter and retry policy; APIM webhook validation (event delivery token check) |
| E: Elevation | Function Managed Identity assigned Cosmos DB Contributor (account-level) instead of Data Contributor (data-level) | Cosmos DB Built-in Data Contributor role at the specific database scope; deny-assignment policy |
| A: Abuse | N/A unless Functions invoke AI endpoints; add A category when AI is introduced | N/A |

### MITRE ATT&CK Cloud Techniques (High Priority)

| Technique ID | Technique | Priority |
|---|---|---|
| T1528 | Steal Application Access Token (IMDS token from Function environment) | Critical |
| T1530 | Data from Cloud Storage / Cosmos DB (cross-tenant data access) | Critical |
| T1552.004 | Credentials in Cloud Instance Metadata (pipeline secrets exposed) | High |
| T1190 | Exploit Public-Facing Application (APIM endpoint vulnerability) | High |
| T1496 | Resource Hijacking (Managed Identity used to provision compute) | Medium |

---

## Domain 3: AI Agent (Azure OpenAI + Cosmos DB + Managed Identity + APIM)

**Typical stack:** Azure OpenAI Service (GPT-4o or GPT-4.1 deployment); APIM as gateway with rate-limiting and JWT validation; Cosmos DB as conversation history / RAG corpus store; Managed Identity for all Azure service access; Azure AI Content Safety for input/output moderation; Azure AI Foundry for agent lifecycle management.

### Top STRIDE-A Threats

All seven STRIDE-A categories are relevant. The Abuse (A) category dominates for this domain.

| STRIDE-A Category | Highest-risk threat | Primary control |
|---|---|---|
| S: Spoofing | Attacker impersonates a trusted agent identity in a multi-agent pipeline | Microsoft Entra Agent ID; Conditional Access for agents; authenticated inter-agent calls |
| T: Tampering | RAG corpus poisoned with adversarial content that shifts agent behaviour | Data provenance tracking; content sanitisation pipeline before corpus ingestion; Defender for AI model scanning |
| R: Repudiation | Agent takes an action (send email, call API) with no per-turn tool-call audit log | Tool-call audit log: tool name, arguments, result, timestamp, user identity, correlation ID; Foundry Agent Control Plane |
| I: Info Disclosure | Agent retrieves cross-tenant documents in a multi-tenant RAG deployment | Retrieval-time tenant-scoped filtering; Managed Identity RBAC scoped per tenant |
| D: DoS | Wallet attack: prompt injection causes agent to loop, exhausting Azure OpenAI TPM | Per-user TPM budget in APIM; session maximum tool call count; alert at 80% TPM |
| E: Elevation | Agent's tool list includes admin-scope operations; prompt injection causes admin action | Least-privilege tool list; human approval for any destructive or write operation |
| A: Abuse | Indirect prompt injection via document retrieval causes agent to exfiltrate data | Azure AI Content Safety Prompt Shields; Foundry Spotlighting; output schema validation before tool execution |

### OWASP ASI Top-10 Priority Items (AI Agents)

Apply the full ASI Top-10 checklist from `references/owasp-asi-top10.md`. Highest-priority for a standard RAG agent architecture:

1. **ASI-01** Prompt Injection (indirect; via retrieved documents)
2. **ASI-02** Excessive Agency (over-privileged tool list)
3. **ASI-06** Sensitive Data Exposure (cross-tenant retrieval)
4. **ASI-09** Resource Governance (wallet attacks, TPM exhaustion)
5. **ASI-07** Insufficient Audit (no per-turn tool-call log)

### MITRE ATLAS Techniques (High Priority)

| ATLAS Technique | Technique | Priority |
|---|---|---|
| AML.T0051 | LLM Prompt Injection (direct + indirect / AML.T0051.001) | Critical |
| AML.T0057 | LLM Data Leakage (cross-tenant context leak) | Critical |
| AML.T0040 | ML Model Inference API Access (API key theft, unprotected endpoint) | High |
| AML.T0029 | Denial of ML Service (wallet attack, TPM exhaustion) | High |
| AML.T0020 | Poison Training Data (RAG corpus poisoning) | High |
| AML.T0056 | Exfiltration via ML Inference API (model extracting proprietary data) | Medium |

### MITRE ATT&CK Cloud Techniques (AI Infrastructure)

| Technique ID | Technique | Priority |
|---|---|---|
| T1528 | Steal Application Access Token (IMDS token from agent compute) | Critical |
| T1530 | Data from Cloud Storage (agent reads beyond authorised scope) | High |
| T1098.001 | Additional Cloud Credentials (attacker adds credentials to agent identity) | High |

---

## Domain 4: Data Platform (Azure Data Factory + Azure Data Lake + Synapse / Fabric)

**Typical stack:** Azure Data Factory for ingestion and orchestration; Azure Data Lake Storage Gen2 as the raw and curated data store; Azure Synapse Analytics or Microsoft Fabric for transformation and analytical queries; Purview for data governance and lineage; Managed Identity for all service-to-service authentication.

### Top STRIDE-A Threats

| STRIDE-A Category | Highest-risk threat | Primary control |
|---|---|---|
| S: Spoofing | ADF linked service using stored credentials (username + password) instead of Managed Identity | Convert all ADF linked services to Managed Identity; block legacy credential stores in ADF via Azure Policy |
| T: Tampering | ADF pipeline modified by a developer with Contributor access on the Data Factory, introducing a malicious data transformation | RBAC: ADF Contributor role limited to data engineering team; pipeline changes via PR-gated CI/CD (no direct portal edits to production) |
| R: Repudiation | ADF pipeline failure deletes intermediate data; no audit trail of what data was deleted and by which pipeline run | Diagnostic logs on all ADF activities forwarded to Log Analytics; immutable pipeline run history |
| I: Info Disclosure | ADLS Gen2 container set to allow public access due to misconfiguration; raw PII data is publicly readable | Azure Policy deny on `AllowBlobPublicAccess`; Hierarchical Namespace ACLs scoped per service identity; Defender for Storage |
| D: DoS | A misconfigured Spark job in Synapse consumes all available compute units, blocking other pipeline runs | Resource pool limits in Synapse; pipeline priority tiers; alert on 80% compute utilisation |
| E: Elevation | ADF Managed Identity assigned Storage Blob Data Contributor at storage account scope; attacker who compromises ADF can read/write any container | Scope ADF Managed Identity to the specific containers it needs; deny at account scope using RBAC conditions |
| A: Abuse | N/A unless ML models are trained or served from this platform; add A when AI is in scope | N/A |

### MITRE ATT&CK Cloud Techniques (High Priority)

| Technique ID | Technique | Priority |
|---|---|---|
| T1530 | Data from Cloud Storage (ADLS Gen2 misconfiguration or credential theft) | Critical |
| T1537 | Transfer Data to Cloud Account (exfiltration via ADF copy to attacker-controlled storage) | Critical |
| T1552.001 | Credentials in Files (ADF linked service credentials in pipeline JSON) | High |
| T1485 | Data Destruction (ADF pipeline deleting curated data layer) | High |
| T1190 | Exploit Public-Facing Application (Synapse Studio public endpoint) | Medium |

---

## Domain 5: Mobile Application (MAUI / React Native + Entra ID B2C + Azure API Backend)

**Typical stack:** .NET MAUI or React Native mobile app; Azure AD B2C for consumer identity (PKCE flow); App Service or APIM + Functions as backend; Azure Blob Storage for user-generated content uploads; Notification Hubs for push notifications.

### Top STRIDE-A Threats

| STRIDE-A Category | Highest-risk threat | Primary control |
|---|---|---|
| S: Spoofing | OAuth PKCE flow downgraded to implicit flow by a malicious redirect_uri | Enforce PKCE in B2C custom policy; reject implicit flow tokens in MSAL configuration; validate redirect_uri against approved list |
| T: Tampering | Man-in-the-middle on mobile device (user installs rogue CA cert); API traffic intercepted | Certificate pinning for critical API endpoints; TLS 1.3 minimum; detect certificate anomalies via network monitoring |
| R: Repudiation | User denies making a purchase or submitting content; no server-side audit log of the action tied to the B2C user identity | Server-side audit log per API action: B2C `oid` claim (immutable user ID), action, timestamp, request correlation ID; signed audit receipts for financial transactions |
| I: Info Disclosure | Mobile app bundles API URL and B2C client ID in compiled binary; reverse-engineered and used to craft malicious API calls | Client IDs are not secrets. The backend must validate the JWT issued by B2C and enforce per-user access control; do not trust on client ID alone. |
| D: DoS | Push notification flooding via compromised device token; Notification Hubs quota exhausted | Per-device notification rate limit; validate device token ownership before sending; Defender for App Service: anomalous notification patterns |
| E: Elevation | B2C custom claims allow a user to claim `admin: true` by manipulating a custom attribute | Never trust client-supplied claims for authorization decisions; re-validate roles against the server-side identity store on every request |
| A: Abuse | On-device AI model (e.g., Core ML / ONNX) manipulated via adversarial image input to misclassify content | Input validation before on-device inference; confidence threshold gates: low-confidence outputs go to server-side validation; do not make irreversible decisions based solely on on-device ML output |

### MITRE ATT&CK Mobile / Cloud Techniques

| Technique ID | Technique | Priority |
|---|---|---|
| T1528 | Steal Application Access Token (B2C access token exfiltrated from device storage) | Critical |
| T1078 | Valid Accounts (credential stuffing against B2C sign-in endpoint) | High |
| T1190 | Exploit Public-Facing Application (APIM backend API vulnerability) | High |
| T1552.001 | Credentials in Files (connection strings in mobile app bundle; not applicable to B2C PKCE, but relevant for third-party SDKs) | Medium |

---

## Cross-Domain Threat Patterns

Some threats apply across all domains and should be enumerated regardless of the specific architecture:

| Threat | Applies to | STRIDE-A | MITRE Technique |
|---|---|---|---|
| Secrets in CI/CD pipeline variables | All domains | T: Tampering, S: Spoofing | T1552.004 |
| Dependency vulnerability (unpatched CVE in deployed artifact) | All domains | T: Tampering, D: DoS | T1190 |
| Diagnostic setting disabled or removed | All domains | R: Repudiation | T1562.008 |
| RBAC over-assignment (Contributor at subscription scope) | All domains | E: Elevation | T1078.004, T1548.005 |
| Resource group lacking delete lock | All domains (production) | D: DoS (data destruction risk) | T1485 |
| No soft-delete on Key Vault / Storage | All domains (production) | D: DoS (ransomware risk) | T1485, T1490 |

---

## Threat Library Selection Flowchart

```text
Architecture in scope
        |
        +-- Contains AI agent, LLM, ML model, or RAG pipeline?
        |       |
        |       +-- YES: Use MITRE ATLAS as primary, ATT&CK Cloud as supplement
        |       |         Run OWASP ASI Top-10 checklist (references/owasp-asi-top10.md)
        |       |
        |       +-- NO: Use MITRE ATT&CK Cloud as primary
        |                 Run OWASP Top-10 for traditional web workloads (per security-architect)
        |
        +-- Contains personal data (PII, PHI, financial)?
        |       |
        |       +-- YES: Compute blast-radius table (references/blast-radius-modeling.md)
        |       |         Consider LINDDUN supplement for special-category data
        |       |
        |       +-- NO: Standard STRIDE-A only
        |
        +-- Spans multiple regulatory regimes (GDPR + HIPAA, etc.)?
                |
                +-- YES: Check Defender for Cloud Regulatory Compliance for each regime
                          Verify current framework availability via microsoft_docs_search
```
