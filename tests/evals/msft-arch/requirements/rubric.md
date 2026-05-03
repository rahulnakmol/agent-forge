Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Structured Questioning Approach** — Uses batched questions (2-3 at a time) across all functional requirement areas (business process, integration, data, security, performance, UX, reporting). Does not ask all questions at once. Score 5 if questioning is systematic and batched; 1 if all questions are asked in one dump or critical categories are skipped.

2. **NFR Specificity** — Converts vague NFRs into measurable targets: availability (99.9%/99.95%), response time in ms, concurrent users, RTO/RPO in hours, data classification levels. Challenges vague terms like "fast" or "scalable". Score 5 if NFRs are specific and measurable; 1 if vague NFRs are accepted without probing for specifics.

3. **Fit-Gap Classification Accuracy** — Correctly classifies each requirement as OOB, Config, Customization, or Third Party. Does not recommend custom development for requirements achievable via configuration. Score 5 if classification is accurate for all requirements; 1 if requirements are systematically misclassified.

4. **MOSCOW Prioritization Quality** — Applies MOSCOW prioritization with clear criteria. Pushes back when all requirements are labeled Must Have. Achieves a reasonable distribution: at least 60% MH is acceptable, but pure 100% MH is rejected and re-prioritized. Score 5 if MOSCOW is applied correctly with pushback on all-Must-Have lists; 1 if all requirements are accepted as Must Have without challenge.

5. **Requirements Register Completeness** — Produces a requirements register with all required columns: ID, Requirement, Category, MOSCOW, Fit-Gap, Capability, NFR Target, Notes. Followed by a handoff block with item counts and context for specialist skills. Score 5 if register is complete and well-structured; 1 if register is incomplete or missing required columns.
