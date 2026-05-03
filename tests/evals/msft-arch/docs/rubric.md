Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Document Type Selection** — Selects the correct document type (HLD, LLD, tech-design spec, or live architecture diagram) based on the request. HLD for leadership/overview, LLD for implementation-ready detail, design.md for feature specs, live diagram from resource group. Score 5 if the correct document type is produced with appropriate sections; 1 if wrong document type is produced.

2. **Section Completeness** — Produces all required sections for the selected document type. HLD: Executive Summary through Appendices (11 sections). LLD: Component Specs through Monitoring (8 sections). design.md: Overview through Test Strategy. Score 5 if all required sections are present and populated; 1 if major sections are missing.

3. **Diagram Quality** — Produces Mermaid diagrams with labeled arrows showing action AND data, error paths shown with dashed lines, async operations labeled, and real technology names (not generic placeholders). C4 diagrams follow the C4 model conventions. Score 5 if diagrams are complete and correctly styled; 1 if diagrams are missing or generic.

4. **Audience Calibration** — Adapts content depth and vocabulary to the stated audience. Executive/leadership docs avoid implementation detail. Developer docs include code-level specifics, API contracts, and data models. Score 5 if content is well-calibrated to the audience; 1 if audience needs are ignored.

5. **Handoff Structure** — Produces a handoff block to the next skill (validate) with artifacts produced and open questions. Documentation is traceable to the architecture decisions that drove it. Score 5 if handoff is complete and content is traceable; 1 if handoff is missing or traceability is absent.
