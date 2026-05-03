# Power Apps Accessibility

Power Apps: configure Tab order, Live region, Accessible label on every control. Default control names ("TextInput3") fail screen reader users. Canvas apps render as a custom canvas (not semantic HTML), so the accessibility tree depends entirely on platform property configuration.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Power Apps Canvas + Model-driven sections).

## Per-Control Property Checklist

Every control in a canvas app needs three core properties configured:

| Property | Purpose | Acceptable values |
|---|---|---|
| `AccessibleLabel` | Screen-reader name | A short human label. Empty string hides Image / Icon / Shape from screen readers (decorative). |
| `AcceptsFocus` (modern) or `TabIndex` (classic) | Keyboard reachability | Modern: `true` for interactive, `false` for decorative. Classic: `0` for interactive, `-1` for decorative. Never > 0. |
| `Live` (Label only) | Live region for announcements | `Off`, `Polite`, or `Assertive`. |
| `Role` (Label only) | Heading semantics | `Default`, `Heading1` ... `Heading4`. Exactly one `Heading1` per screen. |

Verify property semantics current via `microsoft_docs_search` query "Power Apps AccessibleLabel TabIndex AcceptsFocus Live Role" before authoring; the property surface evolves between modern and classic generations.

## App-Level Settings

- **Simplified tab index**: enable in App settings -> Accessibility. With this on, navigation order follows source order plus container grouping; positive `TabIndex` values are ignored. Without it, legacy positive-tabindex behaviour kicks in and breaks screen reader narration. Default: enable.
- **Accessibility Checker**: built into Power Apps Studio. Run before every release. The Checker flags missing `AccessibleLabel`, default screen names, positive `TabIndex`, missing state indication, and Pen control without input alternative. Fix every Tip and Issue before sign-off.

## Canvas App Patterns

### Screen Naming

The first thing a screen reader announces on screen load is the screen name. Default screen names ("Screen1") fail this announcement.

- Rename every screen in the controls tree or properties panel.
- For dynamic screen titles, place a visible Label as the page heading and configure `Role = Heading1` plus `Live = Polite`.
- Do not call `SetFocus` in `OnVisible` immediately: it cancels the screen-name announcement. Let the platform announce, then move focus on the next user action.

### Logical Control Order

Power Apps splits two distinct ordering concerns:

1. **Visual order** plus **screen-reader reading order**: follows control source order. Reorder via the controls tree.
2. **Keyboard tab order**: follows source order plus container grouping when Simplified tab index is enabled.

Containers, Form Cards, and Galleries auto-group children: Tab cycles inside the group, then moves to the next sibling. This is the recommended pattern for grouping logically related controls.

To reorder without using positive `TabIndex`: place the to-be-first control in a Container positioned earlier in source order. Both screen reader and keyboard now see it first.

### Live Regions for Dynamic Updates

Only a Label control can be a live region. Configure:

- `Live = Polite` for non-critical status (form save, item added, tab switched).
- `Live = Assertive` for critical errors only.
- `Visible = true` always. Toggling visibility breaks live-region detection.
- Do not change `Live` at runtime.
- Position the live region in a logical screen location; users may navigate to it manually.

To repeat the same message: clear `Text` to empty string, then set the message again. The value must change to trigger an announcement.

### Color and Contrast on Canvas

Canvas does not inherit Windows Forced Colors. If the user has high-contrast mode on at the OS level, the canvas does not respond. Custom canvas surfaces must meet WCAG AA on their own:

- 4.5:1 for normal text against background.
- 3:1 for large text and non-text components.
- Use Microsoft palette tokens where possible. For custom palettes, validate every foreground / background pair with Accessibility Insights or Colour Contrast Analyser.
- Focus indicator: classic controls expose `FocusedBorderColor` and `FocusedBorderThickness`. Verify both meet 3:1 contrast and at least 2 CSS pixels thickness.

### Pen Input

When a screen contains a Pen control, the in-platform Accessibility Checker flags a Tip to add an alternative input method. Add a Text input control next to the Pen control. Some users cannot use a pen and need to type a signature.

### Modal-Like Containers

Canvas does not have a true modal element. To approximate:

1. Place a Container that covers the screen with a semi-transparent backdrop.
2. Put the modal content in a child Container.
3. On open: `SetFocus(FirstControlInside)`.
4. On close: `SetFocus(TriggerControl)`.
5. Add a Close button that handles Escape via the screen `OnKeyPress` (modern controls) or via a dedicated keyboard shortcut control.
6. Hide the rest of the screen from focus via setting `AcceptsFocus = false` on background controls while the modal is open.

This is awkward by HTML standards, but it is the workable pattern within canvas. Document as a known limitation if a modal must be richly interactive.

## Model-Driven App Patterns

Model-driven apps render standard HTML and inherit most accessibility behaviour from the platform. Areas that still require care:

### Custom PCF Controls

Custom Power Apps Component Framework controls render real HTML. The author owns the accessibility:

- Implement keyboard interaction matching the W3C ARIA APG pattern for the widget type (button, listbox, grid, etc.).
- Provide an accessible name via `aria-label`, `aria-labelledby`, or visible text.
- Honour the host theme; do not bake colors that do not respect Forced Colors.
- Test with Accessibility Insights for Web. Custom PCFs are the most common source of model-driven a11y regressions.

### Custom Subgrids

Subgrids that present tabular data must follow the ARIA grid pattern: `role="grid"`, row and cell roles, arrow-key navigation between cells, Home / End for row, Ctrl+Home / Ctrl+End for the grid as a whole. Reference the W3C ARIA Authoring Practices Guide grid pattern.

### Lookup and Option-Set Comboboxes

Lookups and option sets render as custom comboboxes. The platform implements the ARIA combobox pattern but occasionally regresses. Test:

- Tab to the field. Screen reader announces the field as a combobox with current value.
- Down arrow opens the list; Up / Down navigates options.
- Enter selects; Escape closes without selection.
- Filtered search announces the result count via a live region.

If a regression appears, file with Microsoft via the Power Apps Ideas portal and document a workaround in the design.

## Power Pages Patterns

Power Pages renders standard HTML through Liquid templates. Accessibility is largely a function of template authorship plus any custom JS widgets.

- Use HTML5 landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` directly in Liquid templates.
- Form fields: associate `<label for>` with `<input id>`. Add `aria-describedby` linking validation messages.
- Custom JS widgets (carousels, accordions, modals): implement focus management and ARIA states per `references/focus-management.md` and `references/aria-when-and-how.md`.
- Run Accessibility Insights for Web (FastPass) against every page template. Use Assessment mode quarterly for full WCAG 2.2 AA compliance.

## Validation

1. Run the in-platform Accessibility Checker on every canvas screen. Resolve every Issue and Tip.
2. Tab through the running app keyboard-only. Confirm reach, focus visibility, no traps.
3. Screen-reader pass: Narrator + Edge for canvas (Microsoft platform parity); NVDA + Firefox for Power Pages (WCAG baseline); VoiceOver + Safari for cross-platform claim.
4. For model-driven: Accessibility Insights FastPass on every form, view, and dashboard. Assessment mode before release.
5. For custom PCF: Accessibility Insights, plus manual screen reader. Custom PCFs are the highest-risk surface.

## Known Limitations

Achieving full WCAG 2.2 AA compliance in legacy canvas apps is genuinely difficult. The platform's rendering engine limits what authors can control. When limitations block compliance:

- Document the limitation explicitly in the design.
- Provide an accessible alternative (model-driven app surface, or a web interface backed by the same Dataverse data).
- File the gap with Microsoft via the Power Apps Ideas portal.
- Plan migration to modern controls where they exist; Microsoft is closing legacy gaps on the modern control track.
