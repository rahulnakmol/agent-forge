# OWASP Top 10: Azure Control Mapping

OWASP Top 10 mapped at design time for any web-facing workload, not just at pen-test time. Complete this table before the first sprint of a web workload. For each risk: identify whether the Azure platform, application code, or both are responsible for the control. Document accepted risks with an ADR reference.

## Mapping Table

| # | OWASP Risk | Azure Platform Control | Application Code Control | Test Signal |
|---|---|---|---|---|
| **A01** | Broken Access Control | RBAC + Entra ID Conditional Access; Azure API Management subscription keys + JWT validation policy; private endpoints restrict network access | `[Authorize]` with policy-based auth; resource-based authorization (`IAuthorizationHandler`); enforce object-level ownership checks. Never trust client-supplied resource IDs. | Burp Suite / OWASP ZAP: attempt IDOR with another user's resource IDs |
| **A02** | Cryptographic Failures | Key Vault for all secrets/keys/certs; TLS 1.2+ enforced at App Service / APIM / Front Door; Azure Storage server-side encryption (SSE) on by default; CMK optional for regulated workloads | Never store passwords in plain text; use `PasswordHasher<T>` (ASP.NET Identity) or Argon2id for password hashing; no MD5/SHA1 for security-sensitive hashing; no custom crypto | Check TLS configuration with `testssl.sh`; verify no secrets in app settings (Key Vault references confirmed) |
| **A03** | Injection (SQL, LDAP, OS command) | Defender for SQL detects SQL injection attack patterns and alerts in Defender for Cloud | Parameterised queries / ORMs (EF Core). Never use string concatenation in SQL. Validate + sanitise all external inputs; use `Regex.IsMatch` with allowlist patterns, not blocklists. | SQLMap scan; manual test with `' OR 1=1--` patterns in all input fields |
| **A04** | Insecure Design | Threat model (STRIDE-A) completed at design time; architecture review gates before first deploy; private endpoints + NSG deny-by-default topology | Apply defence in depth in code: validate at API layer + domain layer; don't rely on a single security control; reject unexpected input shapes (discriminated unions / sealed classes) | Architecture review sign-off; STRIDE-A worksheet completed (`standards/references/security/stride-a-worksheet.md`) |
| **A05** | Security Misconfiguration | Defender for Cloud secure score ≥ 80%; MCSB regulatory compliance dashboard; Azure Policy `deny` for non-compliant resource configurations (e.g., storage public access, SQL without TLS); no development ports open in production NSGs | No stack traces exposed in production HTTP responses; `app.UseExceptionHandler` not `app.UseDeveloperExceptionPage` in production; CORS policy allowlist not `*`; disable unnecessary features (directory browsing, debug endpoints) | Defender for Cloud recommendations exported; Nessus / Qualys scan for open ports |
| **A06** | Vulnerable and Outdated Components | Defender for Containers agentless vuln scan (images); Defender for Servers vuln assessment (VMs); Dependabot / MSDO dependency scan in CI pipeline | Block High/Critical CVEs from merging without exception ADR; pin base images to specific digest not `latest`; review Dependabot PRs within SLA (Critical: 24h, High: 7 days) | CI dependency review action fails on High/Critical; Trivy scan in Dockerfile build step |
| **A07** | Identification and Authentication Failures | Entra ID + Conditional Access (MFA required, sign-in risk policy); APIM OAuth 2.0 validation policy; account lockout at identity provider level | Use ASP.NET Core Identity or MSAL. Never implement auth from scratch. Enforce PKCE for public clients; validate `aud`, `iss`, `exp` claims on every JWT; short-lived access tokens (≤ 1 hour) + refresh token rotation. | Attempt authentication bypass; verify token validation rejects expired / wrong-audience tokens |
| **A08** | Software and Data Integrity Failures | Signed container images (cosign); SBOM generated in CI (syft / CycloneDX); SLSA provenance attestation for release builds; branch protection + signed commits on all repos | Validate NuGet package integrity via `dotnet nuget verify`; do not deserialise untrusted data with `BinaryFormatter` or `JavaScriptSerializer`; use `System.Text.Json` with strict options | Verify cosign signature in CD before deployment; check SBOM for unexpected transitive dependencies |
| **A09** | Security Logging and Monitoring Failures | Azure Monitor diagnostic logs on all resources; Log Analytics workspace with ≥ 90 days retention; Defender for Cloud alert notifications to security email; Sentinel (orientation: see `sentinel-overview.md`) | Log authentication events, authorisation failures, and data access to structured logs; include `correlationId` + `userId` (pseudonymised) in every log record; do not log secret values or PII raw | Simulate auth failure. Verify alert fires within 5 minutes; check log schema includes required fields. |
| **A10** | Server-Side Request Forgery (SSRF) | Private endpoints + no public access on internal services removes reachable targets; Azure Firewall egress rules restrict outbound URLs | Validate all user-supplied URLs against an allowlist of expected destinations before making outbound requests; never pass raw user input as a URL to `HttpClient`; use `Uri.IsWellFormedUriString` + scheme + host validation | Supply `http://169.254.169.254/metadata` (IMDS endpoint) as a user-supplied URL and confirm request is rejected |

## How to Use This Table

1. At design time, before sprint 1 of any web workload, fill in a copy of this table for the specific workload.
2. For each risk, assign an owner: platform team (Azure controls) or application team (code controls).
3. Mark each control as: **Implemented** / **Planned (sprint X)** / **Accepted risk (ADR-NNN)**.
4. Include the completed table in the security design artefact handoff to `validate`.
5. During pen-test or security review, use the "Test Signal" column to verify controls are functioning. Do not wait for the pen-tester to define what to test.

## Container-Specific Additions

Container image scanning sits at A06 (Vulnerable Components) but warrants its own pipeline step:

```yaml
# .github/workflows/build.yml: Trivy container scan
- name: Scan container image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}
    format: sarif
    output: trivy-results.sarif
    severity: HIGH,CRITICAL
    exit-code: '1'   # Fail build on High/Critical findings

- name: Upload Trivy results to GitHub Security
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: trivy-results.sarif
```

Block merges with High/Critical CVEs without an exception ADR. Exceptions must include: CVE ID, CVSS score, affected component, compensating control, and remediation target date.
