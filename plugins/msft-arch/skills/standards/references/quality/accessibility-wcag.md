# Accessibility: WCAG 2.2 AA Checklist

**Standard**: WCAG 2.2, Level AA (required baseline for all Microsoft-platform applications per Microsoft Accessibility Standard and EU EN 301 549).

This checklist applies the standard to the Microsoft platform stack: Power Apps, Power Pages, Blazor, Office Add-ins, and Teams apps. Each section identifies platform-specific gotchas and recommended tooling.

---

## WCAG 2.2 AA: Core Principle Checklist

### 1. Perceivable

**Color contrast**
- Normal text (< 18pt or < 14pt bold): minimum 4.5:1 contrast ratio against background.
- Large text (≥ 18pt or ≥ 14pt bold): minimum 3:1.
- Non-text UI components (icons, input borders, chart data): minimum 3:1.
- Do not use color as the only means of conveying information (e.g., red = error must also have an icon or text).

**Text alternatives**
- Every `<img>` must have a meaningful `alt` attribute. Decorative images use `alt=""`.
- SVG icons used as controls must have `aria-label` or `<title>` inside the SVG.
- Complex images (charts, diagrams) need a text alternative that conveys the same information.

**Captions and transcripts**: Pre-recorded video requires synchronized captions. Live audio/video requires real-time captions. Audio-only content requires a transcript.

**Resize and reflow**
- Content must remain readable at 400% zoom without horizontal scrolling (except for content requiring 2D layout such as maps).
- Text spacing: content must not lose functionality when line height is set to 1.5×, letter spacing to 0.12em, word spacing to 0.16em.

---

### 2. Operable

**Keyboard navigation**
- Every interactive element must be reachable and operable via keyboard alone (Tab, Shift+Tab, Enter, Space, Arrow keys).
- No keyboard traps: pressing Tab (or Escape for modals) must always allow focus to escape.
- Skip navigation link: provide a "Skip to main content" link as the first focusable element on each page.

**Focus visible (WCAG 2.2 new)**
- Focus indicator must be visible, with at least 3:1 contrast against adjacent colors and a minimum bounding area of the component perimeter × 2px.
- Do not use `outline: none` in CSS without providing an equivalent custom focus indicator.

**Pointer gestures**
- Functionality that uses multipoint gestures (pinch, swipe) must also be achievable via single pointer or keyboard.
- Drag-and-drop: provide an alternative action (cut/paste, button-triggered move) for users who cannot drag.

**Target size (WCAG 2.2 new, AA)**
- Interactive targets must be at least 24×24 CSS pixels, with spacing such that the total target area is at least 24×24px.
- Exception: inline links in text, or where target size is constrained by the surrounding content.

**Timing**
- If a session timeout will cause data loss, warn the user at least 20 seconds before it occurs and provide a way to extend.
- Moving, blinking, or auto-updating content must be pausable.

---

### 3. Understandable

**Language**
- Declare `lang` attribute on the `<html>` element.
- Declare `lang` attribute on any passage in a different language.

**Consistent navigation**
- Navigation components that appear on multiple pages must appear in the same relative order.
- Components with the same function must have consistent labels.

**Error identification**
- Form errors must be: (a) identified in text, (b) described in text (not just color), (c) associated with the specific field via `aria-describedby` or adjacent label.
- Provide suggestions for correction where possible ("Enter a date in the format DD/MM/YYYY").

**Authentication (WCAG 2.2 new)**
- Do not require cognitive function tests (puzzles, transcribing images) as the only authentication method. Allow copy-paste in authentication fields. Provide a second factor option that does not require memorization.

---

### 4. Robust

- Use semantic HTML or ARIA correctly. Do not use `<div>` as a button without `role="button"`, `tabindex="0"`, and keyboard event handlers.
- Every ARIA attribute must reference an existing, valid element.
- Custom widgets must implement the correct ARIA role and keyboard interaction pattern from the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/).

---

## Platform-Specific Guidance

### Power Apps: Canvas Apps

Canvas controls do not generate semantic HTML; the accessibility tree depends entirely on `AccessibleLabel` properties. Every control must have `AccessibleLabel` set. Default names ("TextInput3") are not accessible. Screen reader reading order follows z-order, not visual order; use the Reorder pane.

**Checklist**: `AccessibleLabel` on all controls; `TabIndex` in logical order; contrast validated (canvas does not inherit high-contrast themes); test with Narrator + Edge and VoiceOver + Safari.

### Power Apps: Model-Driven Apps

Model-driven apps render standard HTML and are generally more accessible out-of-the-box. Custom PCF controls must implement `IInputControl.getAccessibilityLevel()` and follow ARIA patterns. Custom subgrids need ARIA grid/treegrid patterns. Test lookup and option set fields with a screen reader; they use custom combobox patterns that occasionally regress.

### Power Pages

Power Pages generates standard HTML. Run Accessibility Insights for Web against every page template. Use semantic HTML in Liquid templates (`<nav>`, `<main>`, `<aside>` with labels). Associate form field labels via `for`/`id` or `aria-labelledby`. Custom JS widgets must manage focus on modal open/close.

### Blazor (Server and WebAssembly)

Blazor renders HTML. Standard HTML accessibility rules apply with two extra considerations:

- **Route changes**: SPA navigation does not trigger a page load announcement. After navigation, move focus to `<h1>` via JS interop (`await JS.InvokeVoidAsync("moveFocusToMain")`).
- **Validation errors**: Blazor `EditForm` does not auto-associate `ValidationMessage` with the input. Add `aria-describedby` linking the field to its validation message span.
- **`aria-live` regions**: Use `aria-live="polite"` for notifications and status; `aria-live="assertive"` only for critical, time-sensitive errors.

### Office Add-ins

Office Add-ins run inside an iframe within the Office host. Keyboard focus must not escape the task pane. Use Fluent UI React components; they implement the correct ARIA patterns for the Office context. Note: the host does not forward all keyboard events into the add-in; test Alt+F4, Escape, and Tab explicitly in desktop Win32 Office with Narrator and in Office for the web with NVDA + Firefox.

### Teams Apps (Tabs, Bots, Meeting Extensions)

Teams wraps your app in an iframe. The `@microsoft/teams-js` SDK handles focus integration. Do not conflict with Teams keyboard shortcuts (F6 focus cycling). Test focus management on meeting extension panel open/close. Bot messages must use accessible Adaptive Cards; include the `speak` property for screen reader narration.

---

## Remediation Playbook

1. **Automated scan**: Run Accessibility Insights for Web (Fast Pass mode) or `axe-core` in CI. Catches ~30% of issues: missing alt text, low contrast, missing labels, keyboard traps.

2. **Manual keyboard test**: Tab through every interactive element without a mouse. Verify reach, operability, visible focus, and modal focus trapping (Tab cycles inside, Escape closes).

3. **Screen reader test**: Minimum coverage: Narrator + Edge (Windows/Teams/Office), NVDA + Firefox (WCAG compliance standard), VoiceOver + Safari (macOS/iOS). Test headings, landmarks, form labels, live regions, and route-change announcements.

4. **Contrast check**: Use Colour Contrast Analyser (desktop tool) for accurate measurement. Browser DevTools contrast values can be incorrect for anti-aliased text.

5. **Report and track**: Log every finding with: WCAG criterion (e.g., "1.4.3 Contrast Minimum"), affected component, severity (Critical/High/Medium/Low), and acceptance criteria for the fix.

---

## Tools Summary

| Tool | Type | Primary Use |
|---|---|---|
| Accessibility Insights for Web | Browser extension | Fast automated scan + guided manual testing |
| axe DevTools | Browser extension + CI library | Automated scan, integrates with Jest/Playwright |
| Colour Contrast Analyser | Desktop app | Precise contrast measurement including custom themes |
| Narrator | Built-in (Windows) | Windows screen reader testing |
| NVDA | Free desktop app (Windows) | Most common Windows screen reader for WCAG testing |
| VoiceOver | Built-in (macOS/iOS) | macOS and iOS screen reader testing |
| TalkBack | Built-in (Android) | Android screen reader testing |
| Power Apps Accessibility Checker | In-platform | Canvas app `AccessibleLabel` and focus order validation |

---

## Trade-offs and Exceptions

- **Automated testing covers ~30% of issues**: Automated tools cannot detect missing context, confusing screen-reader narratives, or poor focus management in dynamic UIs. Manual testing with a screen reader is non-negotiable.
- **AA vs AAA**: WCAG 2.2 AAA is aspirational and not a contractual or regulatory requirement in most jurisdictions. Focus on AA. Adopt AAA criteria (e.g., 7:1 contrast, no timing at all) only where explicit stakeholder requirements exist.
- **Legacy Power Apps canvas apps**: Achieving full WCAG 2.2 AA compliance in canvas apps is genuinely difficult. The platform's rendering engine limits what authors can control. Document known limitations, provide accessible alternatives (model-driven app or web interface), and raise issues with Microsoft via the Power Apps Ideas portal.
- **Custom ARIA patterns**: Do not invent ARIA patterns. Use only the patterns defined in the ARIA Authoring Practices Guide. Incorrect ARIA is worse than no ARIA; it generates false positives in automated tools while confusing screen reader users.
- **Performance vs accessibility**: `aria-live="assertive"` interrupts the screen reader immediately and can be disruptive for frequent updates. Reserve it for critical errors. Use `aria-live="polite"` for notifications, toast messages, and status updates.
