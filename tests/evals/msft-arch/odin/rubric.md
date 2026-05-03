Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Plan Mode Discipline** — Enters plan mode before producing any design. Uses structured analysis before jumping to recommendations. No design recommendations without upfront context analysis. Score 5 if the response demonstrates structured analysis and planning before recommendations; 1 if recommendations are made immediately without structured thinking.

2. **DDD and Bounded Context Application** — Decomposes systems into bounded contexts with clear ownership and explicit contracts between contexts. Identifies coupling points and domain boundaries. Score 5 if bounded contexts are correctly identified with clear boundaries; 1 if service decomposition ignores domain boundaries.

3. **Functional Programming Principles** — Prefers pure functions, immutability, and functional composition for business logic. Uses Result types over exceptions. Identifies where functional paradigm improves the design. Score 5 if functional principles are applied to the design recommendations; 1 if OOP anti-patterns like mutable shared state are recommended.

4. **Trade-off Explicitness** — Every recommendation includes explicit rationale tied to a design principle. Trade-offs are stated, not hand-waved. Failure modes and scalability cliffs are identified. Score 5 if trade-offs are explicit with rationale; 1 if recommendations are made without justification.

5. **Validated Design Output** — Produces output in the Odin format: Context/Assessment/Recommendations/Proposed Architecture/Implementation Plan/ADR Candidates. Every component has a single responsibility. Mid-level developer could implement from the output. Score 5 if output follows the structured format and is implementable; 1 if output is a loose collection of suggestions without structure.
