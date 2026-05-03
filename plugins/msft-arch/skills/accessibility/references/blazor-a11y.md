# Blazor Accessibility

Blazor: use semantic HTML. AuthorizeView and components must not break tab order. Blazor renders HTML, so standard accessibility rules apply, with two extras: SPA route announcements and `EditForm` validation association.

Canonical checklist: `standards/references/quality/accessibility-wcag.md` (Blazor section).

## Semantic HTML First

Razor markup is HTML. Author with native semantic elements: `<button>`, `<a href>`, `<input>`, `<label>`, `<nav>`, `<main>`, `<header>`, `<footer>`. The same rules in `references/aria-when-and-how.md` apply: native HTML beats ARIA in nearly every case.

Common Blazor anti-patterns to avoid:

- `<div @onclick="Handler">`. No keyboard, no focus, no role. Replace with `<button type="button" @onclick="Handler">`.
- `<a @onclick="Handler">` without `href`. Not in tab order, no Enter activation. Replace with `<button>` for actions, `<a href>` for navigation (`NavLink` for client-side routing).
- Wrapping a button in a label without `for` association. Validation message will not link to the input.

## Route Change Focus

Blazor SPA navigation does not trigger a page-load event. Screen readers do not announce. Fix: move keyboard focus to the new page heading after navigation.

JS interop helper (in `wwwroot/js/a11y.js` or inline):

```javascript
window.moveFocusToMain = () => {
  const target = document.querySelector('main h1') || document.querySelector('main');
  if (!target) return;
  if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
  target.focus();
};
```

Call from a layout component on navigation:

```csharp
@inject NavigationManager Navigation
@inject IJSRuntime JS
@implements IDisposable

@code {
    protected override void OnInitialized()
    {
        Navigation.LocationChanged += OnLocationChanged;
    }

    private async void OnLocationChanged(object? sender, LocationChangedEventArgs e)
    {
        await JS.InvokeVoidAsync("moveFocusToMain");
    }

    public void Dispose() => Navigation.LocationChanged -= OnLocationChanged;
}
```

Each page should expose exactly one `<h1>` with the page title. The focus handler moves focus to that `<h1>`, the screen reader announces it, and the user knows the page changed.

## EditForm and Validation Association

Blazor `EditForm` plus `DataAnnotationsValidator` plus `ValidationMessage` is the standard pattern. By default, the `ValidationMessage` is **not** auto-associated with the input. Screen readers announce the field but not the validation message that appears below it.

The fix: add `aria-describedby` linking the input to the validation message span.

```razor
<EditForm Model="Model" OnValidSubmit="HandleSubmit">
    <DataAnnotationsValidator />

    <div>
        <label for="email">Email</label>
        <InputText id="email" @bind-Value="Model!.Email"
                   aria-describedby="email-error"
                   aria-invalid="@_emailInvalid" />
        <ValidationMessage For="() => Model!.Email" id="email-error" />
    </div>

    <button type="submit">Save</button>
</EditForm>
```

For a complete pattern: pair `aria-invalid` with the field invalid state, and put the `ValidationMessage` inside (or adjacent to) the labelled control.

On `OnInvalidSubmit`, move focus to the first invalid field to reduce time-to-fix. Use an `ElementReference` and `FocusAsync`.

```csharp
private ElementReference _firstInvalidField;

private async Task OnInvalidSubmit(EditContext editContext)
{
    var firstInvalid = editContext.GetValidationMessages().FirstOrDefault();
    // Move focus by selector or via tracked element references.
    await _firstInvalidField.FocusAsync();
}
```

## AuthorizeView and Tab Order

`AuthorizeView` conditionally renders content based on the authentication state. When the user is not authorised, the children are not rendered, so they cannot trap focus. Risks:

- **Layout shift**: when the auth state resolves, content appears or disappears, shifting focus context. Render a consistent layout shell with `Authorizing` and `NotAuthorized` placeholders so the tab order remains predictable across states.
- **Stale focus**: if focus was inside a region that just disappeared, focus falls back to `<body>`. Move focus to a stable landmark when this happens.

```razor
<AuthorizeView>
    <Authorized>
        <button @onclick="Save">Save</button>
    </Authorized>
    <NotAuthorized>
        <a href="/login">Sign in to save</a>
    </NotAuthorized>
    <Authorizing>
        <span aria-live="polite">Checking access...</span>
    </Authorizing>
</AuthorizeView>
```

The `Authorizing` placeholder includes a polite live region so screen reader users know the state is loading.

## Live Regions in Razor

Render the live region container at the layout level so it persists across pages. Update the inner text via a state container. Do not toggle the container display between none and block on each notification: render the container always, update only the text.

```razor
@inject IStatusService Status

<div role="status" aria-live="polite" aria-atomic="true" class="sr-only">
    @Status.CurrentMessage
</div>
```

The `.sr-only` CSS class makes the region visually hidden but accessible to screen readers:

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Component Library Patterns

For reusable Blazor components: expose accessibility-relevant attributes as parameters so consumers can label per usage.

```razor
@code {
    [Parameter] public string AriaLabel { get; set; } = string.Empty;
    [Parameter] public string AriaDescribedBy { get; set; } = string.Empty;
}

<button aria-label="@AriaLabel" aria-describedby="@AriaDescribedBy" @onclick="Handler">
    @ChildContent
</button>
```

Do not bake a static `aria-label` into a reusable component. Different consumers need different labels.

## Component Frameworks

If using Fluent UI Blazor, MudBlazor, or Radzen, verify the components produce correct ARIA before assuming. Run Accessibility Insights against the rendered output. Report regressions to the component library upstream and document workarounds locally.

## Server vs WebAssembly

Functional differences are small for accessibility:

- **Blazor Server**: SignalR-driven UI updates run server-side. Network latency can delay live-region announcements; consider local `aria-busy` to indicate loading.
- **Blazor WebAssembly**: full client-side. JS interop is synchronous from the WASM perspective; live-region updates are immediate.
- **Static SSR (Blazor Web App static rendering)**: client-side validation requires an active SignalR circuit. Forms in static SSR components validate on server submission. Plan validation messages to render in the post-submit response.

## Pre-Merge Checklist (Blazor)

- [ ] Native semantic HTML for every interactive element (`<button>`, `<a href>`, `<label>`, `<input>`).
- [ ] Route-change focus handler wired to `NavigationManager.LocationChanged`.
- [ ] Each page has exactly one `<h1>` with a meaningful title.
- [ ] `EditForm` validation messages associated with their inputs via `aria-describedby`.
- [ ] `aria-invalid` paired with the invalid field state.
- [ ] On `OnInvalidSubmit`, focus moves to the first invalid field.
- [ ] `AuthorizeView` renders an `Authorizing` placeholder with a live region; `NotAuthorized` content is in a stable layout position.
- [ ] Live region container rendered at the layout level; updates via state, not display toggle.
- [ ] Reusable components expose `AriaLabel` and related parameters.
- [ ] `axe-core` (or Accessibility Insights) clean on a representative page set.

## Validation Workflow

1. Run `axe-core` (Playwright integration) in CI against every page template.
2. Manual keyboard pass on representative pages: navigate, fill a form with errors, open a modal, sign out and back in (AuthorizeView state change).
3. Screen reader pass with NVDA + Firefox: heading structure, landmark coverage, route-change announcements, validation message association.
4. Forced Colors mode: focus indicators visible, borders on inputs and buttons present.
