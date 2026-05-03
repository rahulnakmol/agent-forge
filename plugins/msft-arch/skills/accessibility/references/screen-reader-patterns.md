# Screen Reader Patterns

Test with keyboard only first, then screen reader. NVDA on Windows, VoiceOver on macOS. Automated tools cannot detect missing context, confusing narratives, or poor focus management in dynamic UIs. Manual testing is non-negotiable.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Robust section, Operable section).

## Tooling Coverage

| Pair | Use for |
|---|---|
| NVDA + Firefox | WCAG compliance baseline. Free, widely used, generates the most reliable reports. |
| Narrator + Edge | Microsoft platform parity (Windows, Office desktop, Teams desktop). Default for Microsoft customers. |
| VoiceOver + Safari | macOS and iOS coverage. Required for any cross-platform claim. |
| TalkBack + Chrome (Android) | Mobile coverage where mobile is in scope. |
| JAWS + Chrome / Edge | Enterprise customers often standardise on JAWS. Test if contractually required. |

Pick at least one Windows pair and one Apple pair per release.

## NVDA Workflow (Windows)

1. Install NVDA (free at nvaccess.org). Use a virtual machine if installing on a primary device feels intrusive.
2. Toggle NVDA with Ctrl+Alt+N. Use Insert (or Caps Lock) as the NVDA modifier key.
3. Common keys for testing:
   - `H` / `Shift+H`: next / previous heading
   - `K` / `Shift+K`: next / previous link
   - `F` / `Shift+F`: next / previous form field
   - `D` / `Shift+D`: next / previous landmark
   - `Insert+F7`: open Elements List (a directory of headings, links, landmarks, form fields)
   - `Insert+Down Arrow`: read from current position
4. Test charter: heading structure (one H1 per page, descending H2-H6), landmark coverage (`<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>` or ARIA roles), form labels, validation messages, live region announcements, route changes (SPA), modal open / close.

## VoiceOver Workflow (macOS)

1. Toggle VoiceOver with Cmd+F5. Use VO modifier (Ctrl+Option) for navigation.
2. Common keys:
   - `VO+Right Arrow` / `VO+Left Arrow`: next / previous element
   - `VO+Cmd+H`: next heading
   - `VO+Cmd+L`: next link
   - `VO+U`: open the Rotor (directory of headings, landmarks, links, form fields)
   - `VO+A`: read from current position
3. Test on Safari first; Chrome and Firefox have known VoiceOver gaps.

## Accessible Names

Every interactive control needs a clear, machine-readable name.

| Source | Example |
|---|---|
| Visible text content | `<button>Save</button>` (preferred) |
| `<label for>` / `<label>` wrapping the input | `<label for="email">Email</label><input id="email">` |
| `aria-label` | `<button aria-label="Close dialog">x</button>` (use only when no visible text) |
| `aria-labelledby` | Reference an existing element ID containing the label |
| `<title>` inside SVG | `<svg><title>Chart of monthly revenue</title>...</svg>` |

Avoid: `placeholder` as the only label (vanishes on input), `title` attribute as the only label (mouse-only on most screen readers).

## Roles and States

The role tells the screen reader what kind of widget this is. The state tells what the widget is currently doing.

- Use **native HTML** first: `<button>`, `<a href>`, `<input type="checkbox">`, `<select>`. Native elements come with the correct role + state + keyboard wired up.
- When a custom widget is unavoidable, use ARIA roles and properties from the W3C ARIA Authoring Practices Guide. Match the keyboard pattern exactly.
- Common states: `aria-expanded` (true / false) for disclosures and menus, `aria-checked` for custom checkboxes, `aria-pressed` for toggle buttons, `aria-current="page"` for the active nav item, `aria-selected` inside listbox / tab patterns.

## Live Regions

Live regions announce dynamic content changes (toasts, status, validation, tab switches, background refresh). Without a live region, screen reader users miss the change entirely.

```html
<div role="status" aria-live="polite" aria-atomic="true">
  Item added to cart
</div>
```

- **`aria-live="polite"`** for non-urgent notifications, status updates, form save confirmations. The screen reader finishes its current utterance, then announces.
- **`aria-live="assertive"`** for critical, time-sensitive errors only. Interrupts the screen reader. Reserve for genuine emergencies. Frequent assertive updates are disruptive.
- **`role="status"`** is equivalent to `aria-live="polite"` plus `aria-atomic="true"`. **`role="alert"`** is equivalent to `aria-live="assertive"` plus `aria-atomic="true"`.
- **`aria-atomic="true"`** announces the entire region content on change, not just the diff. Set this for short status messages.
- The live region must exist in the DOM **before** the content changes. Inserting a populated live region at the same time as the change is a common bug: NVDA misses it.

## Power Apps Live Regions

In Power Apps canvas, a Label control becomes a live region by setting its `Live` property:

| `Live` value | Behaviour |
|---|---|
| Off | Not a live region. Screen readers do not announce changes. |
| Polite | Screen reader announces after finishing its current utterance. Use for non-critical status. |
| Assertive | Screen reader interrupts to announce. Use sparingly, for critical events only. |

Best practices (from Microsoft Learn):

- Always set `Visible` to true. Some screen readers do not detect regions that toggle visibility.
- Do not change `Live` at runtime. Some screen readers do not detect the toggle.
- Position the live region in a logical location; users may navigate to it directly with the screen reader.
- To repeat the same message, set `Text` to empty string then back to the message; the value must change to trigger an announcement.

## Blazor Live Regions

Use a standard ARIA live region in Razor markup:

```razor
<div role="status" aria-live="polite" aria-atomic="true">
  @StatusMessage
</div>
```

For toast / notification components, render the live region container at app shell level and update its content via a state container. Do not toggle the container `display` between `none` and `block` on each toast: render the container always, and update only the inner text.

## SPA Route Change Announcements

Single-page apps do not trigger a page-load event, so screen readers do not announce navigation. The fix:

1. Move keyboard focus to the new page `<h1>`, which the screen reader will read.
2. Or, write the new page title into a polite live region.

Blazor pattern (JS interop helper):

```javascript
window.moveFocusToMain = () => {
  const target = document.querySelector('main h1') || document.querySelector('main');
  if (target) {
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus();
  }
};
```

Call from `OnAfterRenderAsync` after navigation:

```csharp
await JS.InvokeVoidAsync("moveFocusToMain");
```

## Landmark Roles

Landmark roles let screen reader users jump between page regions with a single key.

- `<header>` (or `role="banner"`): once per page, top of page.
- `<nav>` (or `role="navigation"`): named via `aria-label` if more than one nav.
- `<main>` (or `role="main"`): once per page, primary content.
- `<aside>` (or `role="complementary"`): supplementary content.
- `<footer>` (or `role="contentinfo"`): once per page, bottom.
- `<section>` with `aria-labelledby` (or `role="region"`): generic named region for major content blocks.

Power Pages and Blazor templates should use the HTML landmark elements directly. ARIA `role` attributes are a fallback for older markup.

## Test Charter

For every release-critical surface, run a screen reader pass with these prompts:

1. Open the page from a fresh tab. What does the screen reader announce on load? Title, heading, landmark.
2. Navigate by heading (`H` in NVDA). Are all sections reachable? Is the structure logical (one H1, descending levels)?
3. Navigate by landmark (`D` in NVDA). Are all major regions present?
4. Navigate by form field. Is every input labelled? Are validation messages associated and read?
5. Trigger a dynamic event (toast, validation, search). Does the live region announce?
6. Navigate to a new route (SPA). Is the new page announced?
7. Open and close a modal. Does focus move correctly? Is the modal announced?
