Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Service Selection Rationale** — Selects Azure services appropriate to the workload (correct compute: App Service vs Functions vs Container Apps vs AKS; correct data: SQL vs Cosmos DB vs Table). Provides clear rationale for each choice. Score 5 if all selections are well-justified; 1 if arbitrary or mismatched.

2. **WAF Validation** — Addresses Azure Well-Architected Framework pillars: Reliability (availability zones, health probes, retry), Performance Efficiency (caching, CDN, async), and flags Security/Cost/Ops for horizontals. Score 5 if WAF is systematically covered; 1 if WAF is absent.

3. **Networking and Security Defaults** — Recommends Private Endpoints, Managed Identity, and appropriate networking patterns (hub-spoke, WAF). Does not leave public endpoints without justification. Score 5 if security defaults are applied; 1 if basic security practices are omitted.

4. **C4 Diagram or Architecture Description** — Produces a structured description of the architecture with clear service boundaries and data flows (ideally as C4 Context and Container views or Mermaid diagrams). Score 5 if architecture is clearly visualized; 1 if only prose with no structure.

5. **Horizontal Handoff** — Identifies cross-cutting concerns (identity, security, IaC, observability, FinOps) and signals handoff to appropriate horizontal skills rather than trying to cover everything. Score 5 if handoffs are clear; 1 if no handoff or everything is addressed inline.
