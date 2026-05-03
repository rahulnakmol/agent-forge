Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Terraform over Bicep Preference** — Recommends Terraform for greenfield work with no org-mandated tooling constraints. Bicep only when org policy mandates Microsoft-only tooling. Provides clear rationale. Score 5 if Terraform is correctly recommended or Bicep is recommended only with a clear mandate; 1 if Bicep is recommended without a mandate or Terraform is dismissed.

2. **AVM Modules First** — Recommends Azure Verified Modules (AVM) from the Terraform registry for all AVM-covered resources. Custom modules only when an AVM gap is real and documented in an ADR. Score 5 if AVM modules are correctly identified and referenced; 1 if custom modules are recommended for resources that have AVM equivalents.

3. **Remote State with Locking** — Requires Azure Storage blob container for remote state with blob lease locking and RBAC (not access keys). Never local state in production. Directory-per-environment layout over workspace multiplexing. Score 5 if remote state design is correct and complete; 1 if local state or workspace multiplexing is recommended for production.

4. **PR-Gated Apply Workflow** — Requires the workflow: lint + checkov + conftest → terraform plan → plan review comment → human approval → CI/CD apply only. No local applies to shared environments. Nightly drift detection. Score 5 if the PR-gated workflow is correctly specified; 1 if local applies or auto-approve is recommended.

5. **Policy-as-Code Three-Layer Stack** — Implements the three-layer policy stack: tflint (provider-specific lint), checkov (CIS benchmarks), and OPA/Conftest (org-wide rules). All three gates must pass before the plan is posted. Score 5 if all three layers are present and correctly described; 1 if only one or two layers are covered.
