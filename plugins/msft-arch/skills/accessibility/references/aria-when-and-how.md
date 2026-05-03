# ARIA: When and How

ARIA roles only when native HTML does not have a semantic equivalent. Most a11y failures come from over-applying ARIA. Incorrect ARIA is worse than no ARIA: it generates false positives in automated tools while confusing screen reader users.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Robust section).

## The Five Rules of ARIA (W3C)

The W3C summarises ARIA usage in five rules. Internalise them before adding a single `role` attribute.

1. **If you can use a native HTML element with the semantics and behaviour you need, do so.** A `<button>` already has `role="button"`, keyboard activation (Enter, Space), focus, disabled state, and label association.
2. **Do not change native semantics unless you really have to.** `<h1 role="button">` is wrong; use a `<button>` inside the `<h1>`, or rethink the design.
3. **All interactive ARIA controls must be keyboard accessible.** If you build a custom widget with `role="button"`, you also have to wire `tabindex="0"`, Enter, Space, and the visible focus indicator.
4. **Do not use `role="presentation"` or `aria-hidden="true"` on a focusable element.** This hides it from screen readers while leaving it tabbable, which is the worst possible state.
5. **All interactive elements must have an accessible name.** Visible text, `<label>`, `aria-label`, or `aria-labelledby`. Unnamed buttons are unusable.

## Native HTML Beats ARIA: The Common Failures

| Bad pattern | Why it fails | Replace with |
|---|---|---|
| `<div onclick="...">` | No keyboard, no focus, no role | `<button type="button" onclick="...">` |
| `<a onclick="...">` (no `href`) | No keyboard activation, not in tab order | `<button>` if it triggers an action; `<a href>` if it navigates |
| `<span role="link">` | No keyboard, no focus, no real navigation | `<a href>` |
| `<div role="checkbox" tabindex="0">` plus custom keyboard | Ten lines of code that `<input type="checkbox">` already provides | `<input type="checkbox">` with `<label>` |
| `<div role="dialog">` without focus management | No keyboard trap, no Escape, no focus return | `<dialog>` element with HTML showModal API, or full ARIA dialog pattern with focus management |
| `<img alt="logo">` for an icon button | Alt is not the name of an action | `<button><img alt="" ...>Save</button>` or `<button aria-label="Save">` with hidden visual |

## When ARIA Is the Right Tool

- **Live regions**: announce dynamic changes. There is no native HTML equivalent. Use `aria-live`, `role="status"`, `role="alert"`. See `references/screen-reader-patterns.md`.
- **Custom composite widgets**: tab list, tree, grid, listbox, combobox. Native HTML has `<select>` for the simplest cases; complex pickers and command palettes need full ARIA composite patterns. Match the W3C ARIA Authoring Practices Guide pattern exactly: roles, states, keyboard contract.
- **Relationships**: `aria-describedby`, `aria-labelledby`, `aria-controls`, `aria-owns` to link elements that are not in a parent-child DOM relationship. Example: a validation message below a form field linked via `aria-describedby`.
- **States that HTML cannot express**: `aria-expanded` (true / false) on a disclosure button, `aria-pressed` on a toggle button, `aria-current="page"` on the active nav item, `aria-busy="true"` on a section that is loading.
- **Landmarks for older markup**: `role="navigation"`, `role="main"`, `role="banner"`, `role="contentinfo"`. Modern HTML5 elements (`<nav>`, `<main>`, `<header>`, `<footer>`) implicitly carry these roles; ARIA roles are a fallback for legacy markup.

## State Attributes That Solve Real Problems

| Attribute | When to use |
|---|---|
| `aria-expanded` | Disclosure pattern: button toggles a panel. Set to true / false on the trigger. |
| `aria-pressed` | Toggle button: distinct from a checkbox. Set true / false on the button. |
| `aria-checked` | Custom checkbox or radio. Required if not using `<input>`. |
| `aria-selected` | Active item in tabs, listbox, treeview. |
| `aria-current` | Active item in a set: `page`, `step`, `location`, `date`, `time`, `true`. |
| `aria-disabled` | Non-interactive but still in tab order (read-only state). Prefer the HTML `disabled` attribute on form controls. |
| `aria-invalid` | Form field has failed validation. Set on the input, paired with `aria-describedby` to the error message. |
| `aria-required` | Form field is required. Visible asterisks plus `aria-required="true"`. Or use HTML `required` attribute. |
| `aria-busy` | Region is updating. Helps screen readers wait until updates settle. |
| `aria-haspopup` | Trigger opens a menu, listbox, tree, grid, or dialog. Set the value to the popup type. |
| `aria-controls` | Trigger is associated with another element it controls (the popup, panel, tab panel). |

## Common Over-Application Failures

- **Adding `role="button"` to a `<button>`**. Redundant. Some validators flag it as an error.
- **`aria-label` on a `<button>` that already has visible text**. The aria-label overrides the visible text; if they differ, the screen reader reads the aria-label, not what the user sees. Confusing.
- **`role="presentation"` on an `<img>` that conveys information**. Hides it from assistive tech. Use `alt=""` for decorative; for informative images, write meaningful alt text.
- **`aria-hidden="true"` on a focusable element**. The element disappears from the screen reader but remains tabbable. Tabbing onto an invisible element is the worst possible UX.
- **`aria-live="assertive"` on toasts, status, frequent updates**. Constantly interrupts the screen reader. Use `polite` unless the message is genuinely critical.
- **`tabindex="0"` on every clickable `<div>`**. Wrong fix. Replace the `<div>` with a `<button>`.

## ARIA in Power Platform

- **Power Apps canvas**: ARIA is exposed through specific control properties (`AccessibleLabel` for the name, `Live` for live regions, `Role` on Label for headings). You do not author raw ARIA. Configure the platform properties.
- **Power Apps model-driven, custom PCF controls**: PCF controls render real HTML, so ARIA applies normally. Custom subgrids need `role="grid"` plus the W3C grid keyboard pattern.
- **Power Pages**: standard HTML and Liquid templates. Use HTML5 landmarks first, ARIA only for custom widgets.

## ARIA in Blazor

Razor markup is HTML, so all ARIA rules apply. Common Blazor-specific gotchas:

- `EditForm` with `ValidationMessage`: the validation message is not auto-associated with the input. Add `aria-describedby` linking the input to the validation message span.
- Custom Blazor components: expose ARIA attributes as parameters so consumers can label them per usage. Do not bake a static `aria-label` into a reusable component.
- Conditional rendering with `@if`: when an element appears, it joins the live document. If it should announce, wrap it in a `role="status"` or `aria-live` region.

## Validation

1. Run Accessibility Insights or `axe-core`. ARIA reference errors (`aria-labelledby` pointing to a missing ID) and role / required attribute mismatches will surface.
2. Manual screen reader test. Listen for: every interactive control announces a name and a role; states change announce ("expanded", "selected", "pressed").
3. Code review: any new `role`, `aria-*`, or `tabindex` attribute is a smell. Justify in the PR description. Most justified additions are removable by switching to native HTML.
