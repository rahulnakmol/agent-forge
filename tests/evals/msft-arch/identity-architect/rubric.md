Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Managed Identity over Service Principal** — Recommends System-assigned Managed Identity for single-service:identity bindings and User-assigned MI for shared/pre-created identities. Never recommends service principal with client secret when the compute runs on Azure. Documents any SP recommendation in an ADR with justification. Score 5 if MI is correctly recommended; 1 if SP with secret is recommended for Azure-hosted compute.

2. **Workload Identity Federation** — Recommends Workload Identity Federation (OIDC) for GitHub Actions, AKS pods, and any outside-Azure caller with OIDC support. Never recommends long-lived service principal secrets in pipelines. Score 5 if WIF is correctly recommended with federated credential configuration; 1 if long-lived secrets are recommended for pipelines.

3. **Conditional Access Baseline** — Applies the non-negotiable CA baseline: block legacy auth, MFA for all admins, device compliance for sensitive resources, sign-in risk policies. Deploys in report-only mode before enforcement. Excludes break-glass accounts. Score 5 if baseline is comprehensive and follows report-only-first approach; 1 if legacy auth is not blocked or MFA for admins is omitted.

4. **External ID over B2C** — For new CIAM (customer-facing) scenarios, recommends Entra External ID over Azure AD B2C. B2C only for existing legacy migration or proven External ID gap. Notes that B2C is no longer available for new customers. Score 5 if External ID is recommended for greenfield CIAM; 1 if B2C is recommended for new customer scenarios.

5. **PIM for Privileged Access** — Requires PIM (Privileged Identity Management) for any role above Reader on production. No standing Owner/Contributor on production subscriptions. Just-in-time elevation with approval workflow and time-bounded activation. Score 5 if PIM is correctly specified with approval workflow; 1 if permanent privileged access is recommended.
