# .NET MAUI MVVM with CommunityToolkit.Mvvm

**Applies to**: .NET MAUI 9 (`net9.0-*` TFMs). CommunityToolkit.Mvvm 8.x.

---

## Package Reference

```xml
<PackageReference Include="CommunityToolkit.Mvvm" Version="8.*" />
```

Use Central Package Management (`Directory.Packages.props`) to pin the version across all projects.

## View Model Base

All view models derive from `ObservableObject` (provided by CommunityToolkit.Mvvm). Never implement `INotifyPropertyChanged` manually.

```csharp
namespace MyApp.ViewModels;

public partial class OrderListViewModel : ObservableObject
{
    [ObservableProperty]
    private ObservableCollection<OrderSummary> orders = [];

    [ObservableProperty]
    private bool isLoading;

    [RelayCommand]
    private async Task LoadOrdersAsync(CancellationToken ct)
    {
        IsLoading = true;
        try
        {
            Orders = new ObservableCollection<OrderSummary>(
                await _orderService.GetOrdersAsync(ct));
        }
        finally
        {
            IsLoading = false;
        }
    }
}
```

`[ObservableProperty]` source-generates:
- The public property (`Orders`, `IsLoading`)
- `OnOrdersChanged` / `OnIsLoadingChanged` partial methods (override for side effects)
- Proper `PropertyChanged` notification

`[RelayCommand]` source-generates an `IAsyncRelayCommand` property (`LoadOrdersCommand`). CancellationToken injection is automatic when the method accepts `CancellationToken`.

## Source Generation: partial class Requirement

View model classes MUST be declared `partial`. The source generator adds the other half.

```csharp
// Correct
public partial class ProductViewModel : ObservableObject { }

// Wrong: source generation will not work
public class ProductViewModel : ObservableObject { }
```

## DI Registration in MauiProgram.cs

```csharp
builder.Services.AddTransient<OrderListViewModel>();
builder.Services.AddTransient<OrderListPage>();
builder.Services.AddSingleton<IOrderService, OrderService>();
```

Register pages and view models together. Inject view models into pages via constructor injection.

```csharp
public partial class OrderListPage : ContentPage
{
    public OrderListPage(OrderListViewModel vm)
    {
        InitializeComponent();
        BindingContext = vm;
    }
}
```

Never use `BindingContext = new SomeViewModel()` in code-behind. Always inject.

## Commands: Async vs Sync

Prefer `[RelayCommand]` on async methods. The generated `AsyncRelayCommand` handles:
- Execution state tracking (`IsRunning`)
- Automatic `CanExecute` suppression while running (prevents double-tap)
- CancellationToken propagation

```csharp
[RelayCommand(CanExecute = nameof(CanSubmit))]
private async Task SubmitOrderAsync(CancellationToken ct) { ... }

private bool CanSubmit => !IsLoading && SelectedItems.Count > 0;
```

Call `SubmitOrderCommand.NotifyCanExecuteChanged()` when `CanSubmit` dependencies change.

## OnPropertyChanged Interception

To run side effects when a property changes, override the generated partial method:

```csharp
partial void OnIsLoadingChanged(bool value)
{
    // e.g., update a status bar or trigger analytics
}
```

## ObservableValidator for Form Input

For forms with validation, derive from `ObservableValidator` instead of `ObservableObject`:

```csharp
public partial class LoginViewModel : ObservableValidator
{
    [ObservableProperty]
    [Required]
    [EmailAddress]
    private string email = string.Empty;

    [RelayCommand]
    private async Task LoginAsync(CancellationToken ct)
    {
        ValidateAllProperties();
        if (HasErrors) return;
        // proceed
    }
}
```

`[Required]`, `[EmailAddress]`, and other `System.ComponentModel.DataAnnotations` attributes are recognised by `ObservableValidator`.

## Messenger for Cross-VM Communication

Use `WeakReferenceMessenger` for decoupled communication between view models. Never reference one view model from another directly.

```csharp
// Sender
WeakReferenceMessenger.Default.Send(new OrderPlacedMessage(orderId));

// Recipient: implement IRecipient<T> and register in constructor
public partial class OrderBadgeViewModel : ObservableObject, IRecipient<OrderPlacedMessage>
{
    public OrderBadgeViewModel()
    {
        WeakReferenceMessenger.Default.Register(this);
    }

    public void Receive(OrderPlacedMessage message)
    {
        BadgeCount++;
    }
}
```

## What NOT to Do

| Anti-pattern | Correct Alternative |
|---|---|
| `public class VM : ObservableObject` (not partial) | `public partial class VM : ObservableObject` |
| `new Command(() => { })` in new code | `[RelayCommand]` |
| Manual `SetProperty(ref _field, value)` | `[ObservableProperty]` |
| `DependencyService.Get<T>()` | Constructor injection via MAUI DI |
| ViewModel resolving another ViewModel directly | `WeakReferenceMessenger` |

## References

- CommunityToolkit.Mvvm docs: `microsoft_docs_search "CommunityToolkit MVVM ObservableObject source generation"`
- eShop MAUI reference app: `microsoft_docs_search "eShop MAUI enterprise app patterns"`
