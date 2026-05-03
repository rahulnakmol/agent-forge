Score the output 1-5 on each criterion. Return the AVERAGE.

1. **OIDC over Secrets** — Recommends Workload Identity Federation (OIDC) for Azure authentication in pipelines, never PAT tokens or client secrets for Azure resource access. Score 5 if OIDC is correctly recommended; 1 if long-lived secrets are suggested.

2. **GitOps Principles** — For AKS/Container Apps scenarios, recommends GitOps (Flux or ArgoCD) where pipeline commits to config repo and cluster reconciles. Does not suggest direct kubectl apply in pipelines. Score 5 if GitOps principles are correctly applied; 1 if direct kubectl apply is recommended.

3. **Deployment Strategy Correctness** — Selects the right strategy: ring deployments for stateless services, blue-green for stateful. Includes health gates between ring stages. Score 5 if strategy is appropriate with gates; 1 if strategy is mismatched to the scenario.

4. **Tool Selection Alignment** — Recommends GitHub Actions for OSS/GitHub-hosted orgs, Azure DevOps for enterprise. Terraform plan via tfcmt/Atlantis, not manual. Dependabot grouped by ecosystem, auto-merge for minor/patch only. Score 5 if all tool selections follow the codified opinions; 1 if opposing approaches are recommended.

5. **Security and Compliance** — Addresses pipeline security: scoped federated credentials, no secrets in PR branches, environment protection rules, apply only post-merge. Score 5 if security is comprehensively addressed; 1 if security aspects are ignored.
