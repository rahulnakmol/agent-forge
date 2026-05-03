Score the output 1-5 on each criterion. Return the AVERAGE.

1. **MAUI over Xamarin.Forms** — Recommends .NET MAUI (net9.0 TFMs) as the replacement for Xamarin.Forms. Xamarin.Forms is end-of-life; all new and migrated mobile work targets net9.0-android, net9.0-ios, etc. Score 5 if MAUI is correctly recommended with TFM specifications; 1 if Xamarin.Forms or Xamarin.iOS/Android is recommended for new work.

2. **CommunityToolkit.Mvvm Adoption** — Recommends CommunityToolkit.Mvvm with [ObservableProperty] and [RelayCommand] source generation. Never recommends rolling a custom ObservableObject or using manual INotifyPropertyChanged. Score 5 if CommunityToolkit.Mvvm patterns are correctly applied; 1 if manual boilerplate MVVM is recommended.

3. **Shell Navigation over NavigationPage** — Recommends Shell navigation for new MAUI apps with AppShell.xaml, URL-based routing, and Routing.RegisterRoute. NavigationPage only for compatibility with existing codebases. Score 5 if Shell navigation is correctly recommended; 1 if NavigationPage is recommended for new apps without justification.

4. **Offline-First SQLite Design** — For offline scenarios, recommends sqlite-net-pcl for local storage with a defined sync service and conflict resolution strategy. Treats cloud as the cache, not the source-of-truth. Score 5 if offline-first architecture is correctly designed with sync strategy; 1 if direct API calls are recommended without offline capability.

5. **Azure Notification Hubs for Push** — Recommends Azure Notification Hubs for single-SDK multi-platform push notifications (APNs + FCM v1 + WNS) rather than per-platform direct integration. Score 5 if Azure Notification Hubs is recommended with backend registration design; 1 if per-platform direct push integration is recommended.
