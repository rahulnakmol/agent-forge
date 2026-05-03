Score the output 1-5 on each criterion. Return the AVERAGE.

1. **App Type Selection Rationale** — Applies the correct selection: Canvas Apps for task-specific/mobile-first/custom UX; Model-driven Apps for data-rich/relationship-heavy/process-centric scenarios. Documents selection rationale against the stated requirements. Score 5 if selection matches requirements with clear rationale; 1 if wrong app type is recommended for the scenario.

2. **Delegation over Collections** — Always recommends Dataverse delegation for data filtering rather than loading records into Collections. Collections are only for data that cannot be delegated. Score 5 if delegation is correctly recommended as the solution for large data scenarios; 1 if collections with in-memory filtering are recommended for large datasets.

3. **Security Layers Design** — Designs the correct Dataverse security model: business units, security roles, teams, and column-level security layered appropriately. Does not use only row-level security when field-level security is also required. Score 5 if all required security layers are designed correctly; 1 if security model is incomplete for the stated requirements.

4. **Solution-Aware Architecture** — Every customization in a managed solution with no unmanaged changes in production. Designs environment strategy (dev/test/UAT/prod) with ALM pipeline for promotion. Recommends Power Platform Pipelines or Azure Pipelines for deployment automation. Score 5 if solution architecture and ALM pipeline are correctly designed; 1 if unmanaged production customizations are accepted.

5. **DLP Policy Governance** — Designs DLP policies with correct connector classification: Business (approved), Non-Business (blocked from mixing with Business), Blocked (never allowed). Covers CoE toolkit for governance monitoring. Score 5 if DLP classification is accurate and governance model is comprehensive; 1 if DLP classifications are incorrect or governance is omitted.
