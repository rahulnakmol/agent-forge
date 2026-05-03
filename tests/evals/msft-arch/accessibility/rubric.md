Score the output 1-5 on each criterion. Return the AVERAGE.

1. **WCAG Accuracy** — Recommendations correctly reference WCAG 2.2 AA standards, cite correct success criteria, and apply correct contrast ratios (4.5:1 normal, 3:1 large text). Score 5 if all references are accurate; 1 if standards are misquoted or wrong.

2. **Platform Specificity** — Guidance is specific to the platform in context (Power Apps, Blazor, HTML). Uses correct property names (AccessibleLabel, AcceptsFocus for Power Apps; JS interop for Blazor route focus). Score 5 if highly specific; 1 if generic/platform-agnostic only.

3. **Actionability** — Provides concrete, implementable steps rather than vague advice. A developer can act on the guidance without further research. Score 5 if immediately actionable; 1 if only high-level description.

4. **Native HTML First** — Recommends native HTML elements over ARIA where applicable. Does not suggest div+role workarounds when a semantic element exists. Score 5 if native-first principle is applied; 1 if ARIA overuse is recommended.

5. **Testing Guidance** — Includes how to verify the fix (screen reader + browser pairing, Accessibility Insights, axe-core). Score 5 if testing approach is specified; 1 if no verification guidance given.
