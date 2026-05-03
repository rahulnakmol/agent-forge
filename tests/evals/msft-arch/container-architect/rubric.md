Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Platform Selection Rationale** — Applies the correct Container Apps vs AKS decision rule: Container Apps first for stateless/event-driven/DAPR workloads; AKS only when custom node pools, GPU, advanced network policies, or multi-cluster federation are needed. Score 5 if decision is well-reasoned and follows the codified preference; 1 if AKS is recommended without clear justification over Container Apps.

2. **DAPR Architecture Correctness** — Recommends appropriate DAPR building blocks for the scenario: service invocation, state management (Cosmos DB/Redis), pub/sub (Service Bus/Event Hubs), and Key Vault secret store. Does not recommend direct SDK dependencies when DAPR building blocks suffice. Score 5 if DAPR components are correctly selected and configured; 1 if direct SDK coupling is recommended instead.

3. **GitOps with Flux** — Recommends Flux-based GitOps for delivery with no manual kubectl in production. Covers repository structure, promotion gates, and drift detection. Score 5 if GitOps principles are correctly applied with Flux; 1 if direct kubectl apply is recommended.

4. **Container Security Defaults** — Addresses all required security defaults: non-root containers, read-only filesystem, network policies, workload identity (not service principal secrets), image scanning. Score 5 if security is comprehensively addressed with specific controls; 1 if security is superficial or omitted.

5. **WAF Validation Coverage** — Produces or references a WAF validation covering all 5 pillars: reliability (PDBs, health probes, multi-AZ), security (pod security, workload identity), cost (KEDA scale-to-zero, spot pools), operational excellence (GitOps, structured logging), performance (HPA/KEDA, resource limits). Score 5 if all pillars are addressed with specific checks; 1 if WAF is skipped.
