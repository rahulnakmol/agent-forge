Score the output 1-5 on each criterion. Return the AVERAGE.

1. **One PRD Per Epic Rule** — Produces one PRD per epic, not a monolithic document combining multiple epics. Each PRD is a self-contained file with all 12 required sections (11 for Mode A, 12 for Mode B which adds TOM Alignment). Epics are never combined into a single document. Score 5 if one-PRD-per-epic is enforced with all required sections; 1 if multiple epics are combined or required sections are missing.

2. **Named Persona in Every Story** — Every user story names a specific persona from Section 2 (e.g., "As a support agent", "As a finance manager"). "As a user" is never acceptable. Stories with generic "user" persona are flagged as non-compliant. Score 5 if all stories reference named personas from the PRD's persona section; 1 if "As a user" stories are accepted.

3. **Acceptance Criteria Coverage** — Every story has 3-8 acceptance criteria in Given-When-Then format with at least: one happy path AC, one boundary AC, and one error/negative AC. Stories with only happy path criteria are non-compliant. Score 5 if all three AC types (happy, boundary, error) are present for every story; 1 if only happy path ACs are included.

4. **Priority Distribution Enforcement** — Applies MH/SH/CH distribution rules: at least 60% Must Have, no more than 20% Could Have. Pushes back when all stories are marked Must Have, requiring re-prioritization. Lists MH stories first, then SH, then CH. Does not accept 100% Must Have without challenge. Score 5 if priority distribution is enforced with pushback on all-MH lists; 1 if all stories are accepted as Must Have without challenge.

5. **Success Metrics Quality** — Section 7 has at least 3 success metrics, each with baseline, target, measurement method, and frequency. Includes at minimum 1 leading metric and 1 lagging metric. Metrics are tied to business outcomes, not just activity counts. Score 5 if all metrics have baseline/target/method/frequency with leading+lagging balance; 1 if metrics lack baselines and targets or are activity counts only.
