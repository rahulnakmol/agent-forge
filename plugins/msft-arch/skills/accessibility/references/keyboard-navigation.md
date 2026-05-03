# Keyboard Navigation

Every interactive element must be reachable and operable from the keyboard alone. This is the most common automated-test pass / manual-test fail pattern: a `<div>` with a click handler scans clean and breaks every keyboard user.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Operable section).

## Core Contract

Every interactive control honours this contract:

- **Reach**: Tab moves forward, Shift+Tab moves back. Every interactive control is in the tab order in DOM order or in a deliberately defined logical order.
- **Operate**: Enter activates buttons and links. Space activates buttons and toggles checkboxes. Arrow keys navigate within composite widgets (radio groups, listbox, menubar, tree, grid).
- **Escape**: Pressing Escape closes any popup, dialog, or menu. No keyboard traps outside modals.
- **Visible focus**: The focus indicator is visible at >= 3:1 contrast against adjacent colors and covers a perimeter at least 2 CSS pixels around the component (WCAG 2.2 AA Focus Appearance).

## Tab Order Rules

- **Source order is the default**. The tab order matches the visual order. If the visual order requires reordering, change the source order, not `tabindex`.
- **Avoid positive `tabindex`** (`tabindex="1"`, `tabindex="2"`, ...). Positive values bypass DOM order and are nearly impossible to maintain. The W3C ARIA APG and Microsoft Power Apps docs both flag positive values as discouraged.
- **`tabindex="0"`** adds a non-interactive element to the tab order. Use only when implementing a custom widget that needs keyboard focus, never on something that should be a `<button>`.
- **`tabindex="-1"`** removes an element from sequential navigation but allows programmatic focus. Use for items inside a roving-tabindex composite widget.

## Skip Links

Every page with site-level navigation needs a "Skip to main content" link as the first focusable element. The link can be visually hidden until focused. The target must be a `<main>` element or a heading with `tabindex="-1"`.

```html
<a href="#main" class="skip-link">Skip to main content</a>
...
<main id="main" tabindex="-1">...</main>
```

The skip link CSS pattern: position absolute off-screen, on `:focus` reposition to top-left.

## Modifier Keys and Shortcuts

- Reserve native browser and OS shortcuts. Do not override Ctrl+F, Ctrl+S, Tab, F6, or platform shortcuts.
- For application shortcuts (Ctrl+K command palette, "/" focus search), provide a way to view, remap, or disable them (WCAG 2.1.4 Character Key Shortcuts).
- For Teams apps: F6 cycles between Teams regions. Do not override.
- For Office add-ins: test Alt+F4, Escape, and Tab inside desktop Win32 Office. The host does not forward all keyboard events.

## Composite Widgets

Composite widgets (menus, listboxes, grids, trees) follow the **roving tabindex** pattern: only one descendant has `tabindex="0"` at a time; others have `tabindex="-1"`. Arrow keys move focus within the widget, Tab leaves the widget. Reference: W3C ARIA APG patterns.

| Widget | Inside-widget keys |
|---|---|
| Listbox | Up / Down to move, Home / End to jump |
| Menu | Up / Down to move, Right / Left to open / close submenus, Escape to close |
| Tabs | Left / Right to move between tabs, Home / End to jump |
| Tree | Up / Down to move, Right / Left to expand / collapse |
| Grid | Arrow keys to move cells, Home / End for row, Ctrl+Home / Ctrl+End for grid |
| Radiogroup | Up / Down or Left / Right to move (selection follows focus) |

## Modal Focus Trap

When a dialog opens:

1. Move focus into the dialog (typically to the first interactive element, or to the dialog itself if it has `role="dialog"` and `aria-labelledby`).
2. Trap Tab and Shift+Tab inside the dialog. Tab from the last element wraps to the first; Shift+Tab from the first wraps to the last.
3. Escape closes the dialog.
4. On close, restore focus to the element that opened the dialog.

Reference: `references/focus-management.md` for implementation patterns.

## Power Apps Tab Order

Power Apps splits keyboard navigation across two property names depending on the control generation:

- **Modern controls** (Button, Text input modern, Combo box modern): use `AcceptsFocus` (true / false). Set true for interactive, false for decorative.
- **Classic controls** (Label, Image, Icon, Shape, classic Button): use `TabIndex`. Set 0 for interactive, -1 for decorative. Do not use values greater than 0.
- **Simplified tab index** app setting: enable. With this on, navigation order follows control source order plus container grouping. Without it, the legacy positive-tabindex behaviour kicks in and breaks screen readers.
- **Containers, Form Cards, Galleries** group their children automatically. Tab inside the group, then move to the next sibling.
- **Custom tab sequence**: use a Container positioned at the desired Y to reorder. Avoid positive `TabIndex` values.

Verify via `microsoft_docs_search` query "Power Apps AccessibleLabel TabIndex AcceptsFocus" before authoring: the property names changed between control generations and the docs are authoritative.

## Blazor Tab Order

- DOM order drives tab order. Source order in the `.razor` file controls the experience.
- `AuthorizeView` conditionally renders content. When the user is not authorised, the children do not exist in the DOM, so they cannot trap focus, but the order of authorised vs unauthorised regions must remain coherent (do not interleave).
- Components that conditionally render with `@if` produce gaps. Verify the focus order across the toggle states.
- Avoid `@onclick` on a non-interactive element such as `<div>` or `<span>`. Use `<button>` or `<a>` with the correct semantics.

## Validation Workflow

1. Unplug the mouse or use a keyboard-only test mode (in Chrome / Edge: simulate via DevTools Emulation).
2. Tab through the entire surface. Note: any focus jumps that contradict visual order, any control that cannot be reached, any control that does not show a visible focus indicator.
3. Test every interactive control with the expected key (Enter, Space, Arrow keys for composite widgets).
4. Open every dialog, menu, popover. Verify trap and restoration.
5. Try Escape on every layered surface.

If the surface fails any step, the build fails. Keyboard accessibility is a P0 release blocker.
