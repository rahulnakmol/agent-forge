Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Correct Artifact Type** — Identifies and generates the right artifact type(s) for the request (ADR, Effort, RAID, Solution Design, Test Strategy). Uses correct ADR reference numbering format (MS-[TECH]-[PLATFORM]-[PROJECT]-XXX). Score 5 if artifact type and format are correct; 1 if wrong type or missing format.

2. **Field Completeness** — Populates all required columns for the artifact type (e.g., ADR: Context, Decision, Consequence, Status; Effort: Capability, MOSCOW, Fit-Gap, Complexity). Score 5 if all required fields are populated; 1 if major fields are missing.

3. **Content Quality** — Entries are specific to the project context, not generic placeholders. ADR decisions include rationale; RAID items have mitigations; effort items have realistic complexity. Score 5 if highly contextual; 1 if all generic filler.

4. **Review Checkpoint Offer** — Offers a review checkpoint before generating the workbook artifact. Score 5 if checkpoint is offered; 1 if skipped entirely.

5. **Handoff Clarity** — Concludes with a clear handoff noting what was produced and what the next step is (e.g., use ADR references in HLD/LLD via docs skill). Score 5 if handoff is structured; 1 if no handoff or next steps.
