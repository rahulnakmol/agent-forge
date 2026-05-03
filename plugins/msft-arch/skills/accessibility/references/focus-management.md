# Focus Management

Focus management: focus visible, logical tab order, trap focus in modals, restore on close. The keyboard user must always know where focus is and be able to move it predictably.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Operable section, Focus Visible, Focus Appearance).

## Focus Visible (WCAG 2.2 AA)

The focus indicator must be visible whenever a control has keyboard focus. Specifically:

- Contrast >= 3:1 against adjacent colors.
- Encloses an area at least 2 CSS pixels around the perimeter of the component (Focus Appearance, WCAG 2.2 AA).
- Does not get hidden by sticky headers, overlays, or other content.

The most common defect: `outline: none` in CSS without a custom replacement. The browser default outline meets the minimum bar; removing it without a replacement is a release blocker.

```css
/* Bad: focus removed entirely. */
button:focus { outline: none; }

/* Good: custom focus that meets contrast and area. */
button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

Use `:focus-visible` (not `:focus`) for the visual indicator on mouse-and-keyboard inputs. `:focus-visible` activates only when the browser detects a keyboard interaction, so mouse users do not see the indicator on click. `:focus` still applies for programmatic checks.

## Logical Tab Order

Source order is the default tab order. The visual order should match the source order. If they diverge:

- Reorder the source. Do not patch with positive `tabindex`.
- For Power Apps, reorder via the controls tree or via Container repositioning.

Verification: Tab through the surface from top to bottom. Focus should follow a predictable pattern: top-to-bottom, left-to-right (or right-to-left for RTL languages).

## Modal Focus Trap

When a modal opens, focus must be trapped inside until it closes. Steps:

1. **Save the trigger**. Capture a reference to the element that opened the modal.
2. **Move focus into the modal**. Best target: the modal's primary action, or the modal container itself if it has `role="dialog"` and a labelled `aria-labelledby`.
3. **Trap Tab and Shift+Tab**. Tab from the last interactive element wraps to the first. Shift+Tab from the first wraps to the last. Implement either by listening for keydown and adjusting focus, or by using the HTML `<dialog>` element with `showModal()`, which traps natively.
4. **Escape closes**. Pressing Escape dismisses the modal.
5. **Restore focus on close**. Move focus back to the element that opened the modal. If that element is gone (e.g., it was inside a removed list item), move focus to a sensible nearby target.

```javascript
// Generic trap helper.
function trapFocus(modalElement) {
  const focusable = modalElement.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  modalElement.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
}
```

Native `<dialog>` (HTML5) handles the trap and the inert background automatically. Prefer it where browser support allows.

## Focus Restoration

Common scenarios:

- **Modal close**: focus returns to the trigger button.
- **Item deleted from a list**: focus moves to the next item, or the previous if there is no next, or to a parent landmark if the list is now empty.
- **Wizard step advance**: focus moves to the heading of the new step (or to the first interactive control of the new step).
- **Toast appears and auto-dismisses**: focus does not move (toasts must not steal focus). The live region announces the toast.

## Initial Focus on Page Load

For traditional page loads, the browser handles focus (top of document). For SPA route changes, focus does not move automatically. Implement a route-change focus handler:

```javascript
// Move focus to the page heading after navigation.
window.moveFocusToMain = () => {
  const target = document.querySelector('main h1') || document.querySelector('main');
  if (!target) return;
  if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
  target.focus();
};
```

In Blazor, call from `OnAfterRenderAsync` after navigation:

```csharp
protected override async Task OnAfterRenderAsync(bool firstRender)
{
    if (firstRender || _routeChanged)
    {
        await JS.InvokeVoidAsync("moveFocusToMain");
        _routeChanged = false;
    }
}
```

For Power Apps screens, the screen name is announced automatically by the platform. Do not call `SetFocus` immediately on screen load: it cancels the screen-name announcement. Either let the platform announce the screen name, then move focus on user action; or create a visible heading Label as a live region and use it to announce the new screen.

## Skip Links

The first focusable element on every page should be a "Skip to main content" link. It can be visually hidden until focused.

```html
<a href="#main" class="skip-link">Skip to main content</a>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  position: fixed;
  left: 1rem;
  top: 1rem;
  z-index: 9999;
  padding: 0.5rem 1rem;
  background: var(--color-surface);
  color: var(--color-text);
}
```

Target: a `<main>` element with `tabindex="-1"`, or the page H1 with `tabindex="-1"`.

## Focus Inside Composite Widgets

Composite widgets (menu, tab list, tree, grid, listbox, combobox) use the **roving tabindex** pattern: only one descendant has `tabindex="0"` at a time; the others have `tabindex="-1"`. Arrow keys move focus inside the widget; Tab leaves the widget.

The pattern keeps the widget a single tab stop in the broader page tab order, which matches user expectation. Reference the W3C ARIA Authoring Practices Guide for each widget pattern.

## Power Apps Focus

- `SetFocus(Control.Name)`: programmatic focus. Use for: opening a modal-like Container, advancing a wizard step, returning focus after a dismiss.
- `OnVisible` of a Screen: do not call `SetFocus` here; it cancels the screen-name announcement.
- After a "modal" Container appears: call `SetFocus` on the first interactive control inside.
- After it dismisses: call `SetFocus` on the trigger control if it is still on screen.
- Focus visible: classic controls expose `FocusedBorderColor` and `FocusedBorderThickness`. Verify both meet contrast and visibility requirements.

## Blazor Focus

- `ElementReference` plus `FocusAsync()`: the standard pattern. Capture a reference with `@ref`, then call `await elementRef.FocusAsync()`.
- `AuthorizeView`: when the authorisation state changes, the rendered tree changes. If the previously focused element disappears, set focus to a stable landmark.
- `EditForm`: on `OnInvalidSubmit`, move focus to the first invalid field (or to the validation summary). Do not leave focus on the submit button silently.

## Validation

1. Tab through the entire surface keyboard-only. Confirm focus is visible at every step. Confirm tab order matches visual order.
2. Open every modal, popover, menu. Confirm trap behaviour, Escape closes, focus restores.
3. Trigger every dynamic action (toast, validation, route change). Confirm focus moves where it should and does not move where it should not.
4. Forced Colors mode (Windows): confirm the focus indicator is still visible. Use `outline: 2px solid CanvasText` as a fallback if the custom indicator vanishes.
5. Code search for `outline: none` and `outline: 0`. Every match needs a paired custom focus style or a justification.
