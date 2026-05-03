# .NET MAUI App Store Deployment

**Applies to**: .NET MAUI 9. `dotnet publish` workflows for iOS App Store, Google Play, and Microsoft Store.

---

## Principle: dotnet publish as the Single Deployment Verb

All platform packages are produced with `dotnet publish`. No platform-specific GUI wizards in CI. Signing credentials are loaded from Azure Key Vault or encrypted CI secrets, not committed to the repository.

## Platform Artefacts

| Platform | Artefact | Command |
|----------|----------|---------|
| iOS (App Store) | `.ipa` | `dotnet publish -f net9.0-ios -c Release` |
| Android (Play Store) | `.aab` | `dotnet publish -f net9.0-android -c Release -p:AndroidPackageFormat=aab` |
| Android (Ad-hoc/enterprise) | `.apk` | `dotnet publish -f net9.0-android -c Release -p:AndroidPackageFormat=apk` |
| Windows (Store) | `.msix` | `dotnet publish -f net9.0-windows10.0.19041.0 -c Release` |
| macOS (App Store) | `.pkg` | `dotnet publish -f net9.0-maccatalyst -c Release` |

## Project File: TFMs and Signing Properties

```xml
<PropertyGroup>
  <TargetFrameworks>net9.0-android;net9.0-ios;net9.0-maccatalyst;net9.0-windows10.0.19041.0</TargetFrameworks>
  <OutputType>Exe</OutputType>
  <ApplicationId>com.mycompany.myapp</ApplicationId>
  <ApplicationVersion>1</ApplicationVersion>
  <ApplicationDisplayVersion>1.0.0</ApplicationDisplayVersion>
</PropertyGroup>

<!-- iOS signing: set in CI via environment variable or MSBuild property -->
<PropertyGroup Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'ios'">
  <CodesignKey>$(IOS_CODESIGN_KEY)</CodesignKey>
  <CodesignProvision>$(IOS_PROVISION_PROFILE)</CodesignProvision>
</PropertyGroup>

<!-- Android signing -->
<PropertyGroup Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'android'">
  <AndroidKeyStore>true</AndroidKeyStore>
  <AndroidSigningKeyStore>$(ANDROID_KEYSTORE_PATH)</AndroidSigningKeyStore>
  <AndroidSigningKeyAlias>$(ANDROID_KEY_ALIAS)</AndroidSigningKeyAlias>
  <AndroidSigningKeyPass>$(ANDROID_KEY_PASS)</AndroidSigningKeyPass>
  <AndroidSigningStorePass>$(ANDROID_STORE_PASS)</AndroidSigningStorePass>
</PropertyGroup>
```

Never commit keystore files or `.p12` certificates to source control.

## Azure Key Vault Code Signing (Preferred for CI)

Azure Key Vault Code Signing replaces local certificate management:

1. Import the distribution certificate (`.p12`) into Key Vault as a certificate object.
2. Grant the CI service principal `Key Vault Certificate User` role.
3. Use the `AzureSignTool` or `Sign CLI` action in CI to sign the package after `dotnet publish`.

```yaml
# GitHub Actions step (after dotnet publish)
- name: Sign iOS IPA with Key Vault
  run: |
    dotnet tool install -g AzureSignTool
    AzureSignTool sign \
      --azure-key-vault-url ${{ secrets.KV_URL }} \
      --azure-key-vault-client-id ${{ secrets.KV_CLIENT_ID }} \
      --azure-key-vault-client-secret ${{ secrets.KV_CLIENT_SECRET }} \
      --azure-key-vault-certificate ${{ secrets.KV_CERT_NAME }} \
      --timestamp-rfc3161 http://timestamp.digicert.com \
      bin/Release/net9.0-ios/publish/*.ipa
```

For Android `.aab`, use `jarsigner` with a keystore loaded from Key Vault secrets.
For Windows `.msix`, use `SignTool` with the Key Vault certificate.

## GitHub Actions Matrix: Multi-Platform Build

```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - platform: android
            os: ubuntu-latest
            tfm: net9.0-android
          - platform: ios
            os: macos-latest
            tfm: net9.0-ios
          - platform: maccatalyst
            os: macos-latest
            tfm: net9.0-maccatalyst
          - platform: windows
            os: windows-latest
            tfm: net9.0-windows10.0.19041.0
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - name: Install .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.x'

      - name: Install MAUI workload
        run: dotnet workload install maui

      - name: Restore
        run: dotnet restore MyApp/MyApp.csproj

      - name: Publish
        run: dotnet publish MyApp/MyApp.csproj -f ${{ matrix.tfm }} -c Release
```

iOS and macOS runners require Xcode 16+ (Xcode 16 required for .NET MAUI 9 / iOS 18 SDK support).

## iOS-Specific Requirements

- Apple Developer account (Individual or Organisation; Enterprise for in-house distribution).
- Distribution provisioning profile and distribution certificate installed on the Mac runner or loaded from CI secrets.
- `Privacy manifest` file (`PrivacyInfo.xcprivacy`) in `Platforms/iOS/` declaring data collection and required-reason API usage. Missing manifest causes App Store rejection.
- Minimum deployment target: iOS 12.2 (set `<SupportedOSPlatformVersion>12.2</SupportedOSPlatformVersion>` in `.csproj`).

## Android-Specific Requirements

- Google Play Developer account.
- Signed `.aab` with a keystore. Google Play App Signing is strongly recommended: upload the `.aab` signed with an upload key; Google re-signs with the distribution key.
- `targetSdkVersion` must match the current Play Store requirement (Android 14 / API 34 as of 2024). Set in `Platforms/Android/AndroidManifest.xml`.
- Native AOT (opt-in) reduces `.aab` size and startup time but requires zero trimmer warnings.

## Windows-Specific Requirements

- Windows App SDK (WinUI 3) package identity configured in `Package.appxmanifest`.
- Code-signed `.msix` for sideload distribution; Windows Store handles signing for Store-distributed apps.
- Package Identity Name must match the Store reservation.

## Native AOT (iOS and Mac Catalyst)

Enable for production builds to reduce package size (up to 2.5x) and startup time (up to 2x):

```xml
<PropertyGroup Condition="'$(Configuration)' == 'Release' And
    ($([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'ios' Or
     $([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'maccatalyst')">
  <PublishAot>true</PublishAot>
  <TrimMode>Full</TrimMode>
</PropertyGroup>
```

Prerequisite: all assemblies and third-party packages must be fully trim-compatible. Run `dotnet publish` with `-p:TreatWarningsAsErrors=true` to surface trimmer warnings in CI before enabling AOT.

## References

- iOS deployment: `microsoft_docs_search ".NET MAUI publish iOS App Store distribution dotnet publish"`
- Android deployment: `microsoft_docs_search ".NET MAUI publish Android Google Play AAB dotnet publish"`
- Native AOT: `microsoft_docs_search ".NET MAUI Native AOT deployment iOS Mac Catalyst"`
- Key Vault Code Signing: `microsoft_docs_search "Azure Key Vault code signing CI pipeline AzureSignTool"`
