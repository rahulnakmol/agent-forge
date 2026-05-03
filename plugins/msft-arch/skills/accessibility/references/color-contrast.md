# Color and Contrast

Color contrast >= 4.5:1 for normal text, 3:1 for large. Verify with Accessibility Insights. Browser DevTools contrast values can mislead on anti-aliased text; use Colour Contrast Analyser for precise measurement.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Perceivable section).

## Required Ratios (WCAG 2.2 AA)

| Element | Ratio | Notes |
|---|---|---|
| Normal text | 4.5:1 | < 18pt regular or < 14pt bold against the background |
| Large text | 3:1 | >= 18pt regular or >= 14pt bold |
| Non-text UI components | 3:1 | Input borders, focus indicators, icon-only buttons, chart data colors |
| Focus indicator (WCAG 2.2 AA Focus Appearance) | 3:1 | Against adjacent colors, perimeter at least 2 CSS pixels |
| Decorative graphics | None | No requirement; mark with `alt=""` and skip |

AAA targets (7:1 normal text, 4.5:1 large text) are aspirational. Pursue only when contractually required.

## Color Cannot Be the Only Channel

If red means error, the error must also have an icon, text, or pattern. If green means success, pair with text and an icon. Color-blind users (about 8 percent of men, 0.5 percent of women in Western populations) cannot distinguish red and green reliably. The same applies to charts: use shape, pattern, or label, not color alone.

## Tooling

| Tool | Best for | Notes |
|---|---|---|
| Accessibility Insights for Web (FastPass) | Automated contrast scan across all visible text | Browser extension, free; integrates with Chrome and Edge. |
| axe DevTools | CI integration via `axe-core` (Jest, Playwright) | Same engine as Accessibility Insights for the contrast check. |
| Colour Contrast Analyser (CCA, TPGi) | Spot checks, custom theme validation, anti-aliased text | Desktop app; eyedropper picker. The most accurate option for designer workflows. |
| Chrome DevTools / Edge DevTools contrast | Quick designer feedback | Can over-report passes on anti-aliased text near borders. Re-verify with CCA before sign-off. |
| Stark (Figma plugin) | Design-time validation | Useful before tokens are even committed. |

## Microsoft Palette Compliance Matrix

When working with Microsoft tokenised palettes, the approved foreground / background pairs are pre-validated. Stick to them. The most common compliant pairings:

| Foreground token | Background token | Use case | Approx ratio |
|---|---|---|---|
| `colorNeutralForeground1` | `colorNeutralBackground1` | Default text on default surface | >= 7:1 |
| `colorNeutralForeground2` | `colorNeutralBackground1` | Secondary text on default surface | >= 4.5:1 |
| `colorNeutralForeground3` | `colorNeutralBackground1` | Disabled / hint text on default surface | borderline; verify per theme |
| `colorBrandForeground1` | `colorNeutralBackground1` | Brand emphasis text on default surface | >= 4.5:1 |
| `colorNeutralForegroundOnBrand` | `colorBrandBackground` | Text on brand-colored surface | >= 4.5:1 |

Custom palettes need manual validation. Run every foreground / background pair you intend to ship through Accessibility Insights or CCA. Document the approved pairs in a design-system token sheet so engineers cannot accidentally invert them.

## Power Apps Themes

Default Power Apps themes are designed to meet WCAG AA. Customisation is where most issues appear:

- Canvas does not inherit Windows / browser high-contrast themes. If the user has a forced color scheme, the canvas does not respond. Custom canvas surfaces must meet AA on their own.
- Custom theme color tokens: validate every visible foreground / background pair before committing. The Power Apps Accessibility Checker flags the most obvious failures but not all.
- Modern controls expose theme tokens; stick to the platform tokens rather than literal hex values where possible.

## Blazor and Custom CSS

- Token your colors. Hex values scattered across components are impossible to audit. CSS custom properties (`--color-text-primary`) give you a single point of validation.
- Verify dark mode separately. Light-mode pass does not imply dark-mode pass; they are independent variants.
- Hover and focus states change the visible color. Verify the hover and focus states meet contrast against the underlying surface.
- For data-visualisation: use `aria-label` to convey the value, do not rely on the color alone for chart series.

## Forced Colors and High Contrast

Windows users can enable Forced Colors mode (formerly High Contrast). The OS overrides authored colors with a small system palette. Test every user-facing surface with Forced Colors on:

- Use CSS system colors (`Canvas`, `CanvasText`, `LinkText`, `ButtonText`, `Highlight`) where appropriate.
- Do not use `background-image` for critical UI affordances; Forced Colors hides background images by default.
- Borders on inputs and buttons must be present (not transparent), or they vanish in Forced Colors.

CSS opt-in:

```css
@media (forced-colors: active) {
  .my-button {
    border: 1px solid CanvasText;
  }
}
```

## Verification Workflow

1. Designer authors with token references; never literal hex.
2. Designer runs Stark (or equivalent) on every Figma frame. Fix at design time.
3. Engineer implements with the token system. No hard-coded colors except in the token file.
4. CI runs `axe-core` (or Accessibility Insights) over the rendered components. Contrast violations break the build.
5. Tester runs CCA on a representative sample (top 10 page templates) before release. Spot-checks anti-aliased text.
6. Tester verifies Forced Colors mode on Windows for the same sample.

A contrast failure at any stage is a release blocker.
