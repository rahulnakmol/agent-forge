# NuGet and Dependency Hygiene

A clean dependency graph is a security and maintainability asset. Unmanaged NuGet references accumulate version drift, known vulnerabilities, and transitive surprises. Establish the discipline at project creation; retrofitting is expensive.

## Central Package Management (CPM)

Central Package Management moves all version declarations into a single `Directory.Packages.props` file at the solution root. Individual `.csproj` files reference packages without versions. Benefits: one file to audit, one PR to upgrade across all projects, and automatic duplicate-version detection.

```xml
<!-- Directory.Packages.props: solution root -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <!-- Core framework -->
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="9.0.4" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore.SqlServer" Version="9.0.4" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore.Design" Version="9.0.4" />

    <!-- ASP.NET Core -->
    <PackageVersion Include="Microsoft.AspNetCore.OpenApi" Version="9.0.4" />

    <!-- Testing -->
    <PackageVersion Include="xunit" Version="2.9.0" />
    <PackageVersion Include="xunit.runner.visualstudio" Version="2.8.2" />
    <PackageVersion Include="FluentAssertions" Version="6.12.1" />
    <PackageVersion Include="Verify.Xunit" Version="25.0.0" />
    <PackageVersion Include="NSubstitute" Version="5.1.0" />
    <PackageVersion Include="Testcontainers.PostgreSql" Version="3.10.0" />

    <!-- Resilience / error handling -->
    <PackageVersion Include="FluentResults" Version="3.16.0" />
    <PackageVersion Include="OneOf" Version="3.0.271" />
  </ItemGroup>
</Project>
```

Project files reference packages without versions:

```xml
<!-- src/Orders.Api/Orders.Api.csproj -->
<ItemGroup>
  <PackageReference Include="Microsoft.AspNetCore.OpenApi" />
  <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" />
  <PackageReference Include="FluentResults" />
</ItemGroup>
```

NuGet emits `NU1507` if any project sets a version that conflicts with `Directory.Packages.props`. Treat this as a build error.

## Lock Files

Lock files (`packages.lock.json`) pin the exact resolved package graph (including transitive dependencies) and prevent silent upgrades during restore. Commit the lock file to source control.

Enable in `Directory.Build.props`:

```xml
<!-- Directory.Build.props: solution root -->
<Project>
  <PropertyGroup>
    <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
    <!-- In CI, fail if the lock file is out of sync -->
    <RestoreLockedMode Condition="'$(CI)' == 'true'">true</RestoreLockedMode>
  </PropertyGroup>
</Project>
```

In CI, `RestoreLockedMode=true` causes restore to fail if the lock file does not match the current package graph, catching unintentional dependency changes before they reach production.

## Vulnerability Scanning

NuGet 6.8+ (.NET 8 SDK) performs automated vulnerability scanning during `dotnet restore`. Vulnerabilities are reported as warnings by default. Treat `High` and `Critical` severity findings as build errors:

```xml
<!-- Directory.Build.props -->
<PropertyGroup>
  <NuGetAudit>true</NuGetAudit>
  <NuGetAuditMode>all</NuGetAuditMode>      <!-- include transitive deps -->
  <NuGetAuditLevel>high</NuGetAuditLevel>   <!-- warn on high and critical -->
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>
```

For periodic scanning outside the build pipeline:

```bash
dotnet list package --vulnerable --include-transitive
```

When a vulnerability is found in a transitive dependency where you don't control the version, use CPM's transitive pinning to override it:

```xml
<!-- Directory.Packages.props: pin vulnerable transitive dep -->
<ItemGroup>
  <PackageVersion Include="System.Text.Json" Version="9.0.4" />
</ItemGroup>
```

## Source Link

Source Link enables stepping into NuGet package source code in the debugger. It does not affect your distributable; it embeds a pointer to the source repository in the PDB. Enable for all packages you publish internally:

```xml
<!-- In every publishable .csproj -->
<PropertyGroup>
  <PublishRepositoryUrl>true</PublishRepositoryUrl>
  <EmbedUntrackedSources>true</EmbedUntrackedSources>
  <IncludeSymbols>true</IncludeSymbols>
  <SymbolPackageFormat>snupkg</SymbolPackageFormat>
</PropertyGroup>

<ItemGroup>
  <PackageReference Include="Microsoft.SourceLink.GitHub" Version="8.0.0" PrivateAssets="All" />
</ItemGroup>
```

For internally hosted packages (Azure Artifacts), use `Microsoft.SourceLink.AzureDevOpsServer` instead.

## Package Source Mapping

When using both nuget.org and a private feed (e.g., Azure Artifacts), package source mapping prevents dependency confusion attacks. It declares which feed each package prefix restores from:

```xml
<!-- nuget.config -->
<configuration>
  <packageSources>
    <clear />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
    <add key="contoso-internal" value="https://pkgs.dev.azure.com/contoso/_packaging/internal/nuget/v3/index.json" />
  </packageSources>
  <packageSourceMapping>
    <packageSource key="contoso-internal">
      <package pattern="Contoso.*" />
    </packageSource>
    <packageSource key="nuget.org">
      <package pattern="*" />
    </packageSource>
  </packageSourceMapping>
</configuration>
```

This ensures `Contoso.*` packages only ever restore from the internal feed, preventing a public nuget.org package with the same name from being substituted.

## Trimming Unused Dependencies

Dependencies accumulate over time. Periodically audit with:

```bash
# List all packages and find ones with no direct usage
dotnet list package

# Identify outdated packages (review before updating; don't auto-update blindly)
dotnet list package --outdated
```

For large solutions, `dotnet-outdated` (global tool) produces a consolidated upgrade report:

```bash
dotnet tool install --global dotnet-outdated-tool
dotnet outdated --include-auto-references
```

Before upgrading a major version, verify the package changelog and check for breaking changes against the project's usage. Apply CPM-level upgrades one dependency at a time with a focused PR so a regression is easy to bisect.

## Signed Packages

For regulated environments or supply chain hardening requirements, configure NuGet to require repository-signed packages:

```xml
<!-- nuget.config -->
<configuration>
  <trustedSigners>
    <repository name="nuget.org" serviceIndex="https://api.nuget.org/v3/index.json">
      <certificate fingerprint="0E5F38F57DC1BCC806D8494F4F90FBBA..." hashAlgorithm="SHA256" allowUntrustedRoot="false" />
    </repository>
  </trustedSigners>
  <config>
    <add key="signatureValidationMode" value="require" />
  </config>
</configuration>
```

Most public nuget.org packages are repository-signed. Internal packages should be author-signed using a code signing certificate managed via Key Vault, not a self-signed cert stored in a secret.
