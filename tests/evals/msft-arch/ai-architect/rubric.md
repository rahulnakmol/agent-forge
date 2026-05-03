Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Foundry-First Approach** — Recommends Microsoft Foundry as the unified AI platform. Uses correct current terminology (Foundry Agents, Foundry IQ, azure-ai-projects SDK). Does not recommend outdated patterns (Assistants API v0.5, separate Hub resources). Score 5 if Foundry-aligned; 1 if recommends outdated or non-Foundry approach.

2. **Pattern Selection Rationale** — Selects the appropriate architectural pattern (RAG, multi-agent, copilot orchestrator, model router) with clear rationale tied to the use case. Score 5 if pattern is well-justified and fits the scenario; 1 if arbitrary or mismatched.

3. **Guardrails Coverage** — Addresses responsible AI: content safety filtering, prompt injection protection, PII handling, hallucination mitigation. Score 5 if all four guardrail categories are addressed; 1 if guardrails are omitted.

4. **WAF Alignment** — Validates against Azure Well-Architected Framework pillars (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) for AI workloads. Score 5 if WAF is systematically applied; 1 if not mentioned.

5. **Specificity and Completeness** — Provides specific service names, SDK choices, and configuration guidance rather than vague recommendations. A team can start implementing from the output. Score 5 if highly specific; 1 if only generic advice.
