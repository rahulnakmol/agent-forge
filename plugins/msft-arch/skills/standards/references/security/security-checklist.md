---
category: security
loading_priority: 1
tokens_estimate: 500
keywords: [security, STRIDE, authentication, authorization, encryption, OWASP]
---

# Security Review Checklist

Every architecture design MUST pass this security gate. No exceptions.

## Security Items

- [ ] **Threat model**: STRIDE analysis completed for all external-facing components
- [ ] **Authentication**: Entra ID / managed identity / mTLS; no custom auth schemes
- [ ] **Authorization**: RBAC or ABAC with least privilege; no admin-by-default
- [ ] **Zero Trust**: Every service-to-service call authenticated and authorized
- [ ] **Input validation**: All external inputs validated at boundary (Zod, FluentValidation, Pydantic)
- [ ] **No secrets in code**: Key Vault for all secrets, managed identity for service auth
- [ ] **Encryption**: TLS 1.3 in transit, AES-256 at rest, Key Vault for keys
- [ ] **Network isolation**: Private endpoints for data stores, no public access in production
- [ ] **Dependency security**: Scanning configured, lockfiles pinned, patching cadence defined
- [ ] **Audit logging**: All security-relevant actions logged with structured context
- [ ] **Container security**: Non-root users, read-only filesystems, image scanning
- [ ] **OWASP Top 10**: Every web-facing component addresses all 10 categories

> For comprehensive security framework: Read `security-by-design.md` in this directory.
