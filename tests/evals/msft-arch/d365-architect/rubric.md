Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Standard over Custom Principle** — Correctly applies the "standard over custom" D365 principle: maximizes OOB functionality, uses extension model (plugins/X++) rather than base code modification, evaluates AppSource ISV solutions before custom development. Score 5 if standard-first approach is consistently applied; 1 if custom development is recommended without exhausting standard options.

2. **Fit-Gap Classification Accuracy** — Correctly classifies requirements into Fit (OOB), Gap (customization needed), Workaround (modified business process), or Out of Scope. Does not recommend customization for requirements that can be met with configuration. Score 5 if classification is accurate and complete; 1 if most gaps are incorrectly classified.

3. **Integration Pattern Selection** — Selects the appropriate integration pattern: dual-write for real-time bidirectional CE/F&O sync, virtual entities for read-only external data, Dataverse APIs for third-party integration. Does not recommend custom middleware when native patterns suffice. Score 5 if pattern selection matches the integration scenario; 1 if inappropriate integration approach is recommended.

4. **Security Model Design** — Designs the Dataverse security model correctly: business units, security roles, teams, and field-level security layered appropriately. Does not conflate row-level and field-level security. Score 5 if the security model correctly implements the stated requirements; 1 if fundamental security model mistakes are made.

5. **WAF and Success by Design Alignment** — References D365 WAF pillars (reliability, security, cost, operational excellence, performance) and Success by Design phases where appropriate. Addresses API limits, batch processing, and async plugin patterns for performance. Score 5 if operational and WAF guidance is comprehensive; 1 if design is incomplete on operational concerns.
