# Windows Container Fallback

**Applies to**: .NET Framework 4.x applications where full migration to .NET 8/9 is not viable within the next 12-18 months.

**Principle**: Windows Container as last resort when full migration is not viable for the next 12-18 months.

---

## When to Use Windows Containers

Windows Containers are a deferral strategy, not a destination. Use them when:

- The full migration effort exceeds 12-18 months and the customer needs infrastructure modernisation (containerisation, AKS hosting, CI/CD pipelines) to proceed now.
- The legacy codebase has hard OS dependencies (`System.Drawing` GDI+, COM interop, Registry access, custom native DLLs) that prevent running on Linux.
- An existing WCF server-side implementation is too risky to migrate before a hard compliance or infra deadline.
- A Windows Licensing or ISV dependency prevents the Linux container path.

Do NOT use Windows Containers as a long-term strategy. Set an explicit migration exit date (max 18 months from container deployment) and track it as a migration backlog item in the project plan.

---

## Container Image Selection

| .NET Framework version | Container image | Base OS |
|---|---|---|
| 4.8 (recommended) | `mcr.microsoft.com/dotnet/framework/aspnet:4.8` | Windows Server Core |
| 4.7.x | `mcr.microsoft.com/dotnet/framework/aspnet:4.7.2` | Windows Server Core |
| 4.6.x | `mcr.microsoft.com/dotnet/framework/aspnet:4.6.2` | Windows Server Core |

.NET 8/9 target (preferred, when migration complete):
```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
# Linux-based, much smaller, faster start
```

---

## Minimal Dockerfile for .NET Framework 4.8 ASP.NET App

```dockerfile
# Build stage (requires Windows build agent)
FROM mcr.microsoft.com/dotnet/framework/sdk:4.8 AS build
WORKDIR /src
COPY . .
RUN msbuild /p:Configuration=Release /p:DeployOnBuild=true \
    /p:WebPublishMethod=FileSystem /p:PublishUrl=C:\out

# Runtime stage
FROM mcr.microsoft.com/dotnet/framework/aspnet:4.8 AS runtime
WORKDIR /inetpub/wwwroot
COPY --from=build C:\out .
```

---

## Hosting Windows Containers

### AKS (Windows node pools)

AKS supports Windows node pools alongside Linux node pools. Windows Containers run on `Windows Server 2022` nodes.

Key constraints:
- Windows node pools cannot use Linux-only add-ons (e.g., some CNI plugins, certain storage drivers).
- Windows container images are substantially larger (multiple GB vs. hundreds of MB for Linux .NET images). This increases pull times and storage costs.
- Autoscale is supported but node provisioning for Windows nodes is slower.

```yaml
# Add Windows node pool to existing AKS cluster (Azure CLI)
az aks nodepool add \
  --resource-group rg-myapp \
  --cluster-name aks-myapp \
  --name win22 \
  --os-type Windows \
  --os-sku Windows2022 \
  --node-count 2 \
  --node-vm-size Standard_D4s_v3
```

### App Service (Windows Containers)

App Service supports Windows Container deployments via App Service Plan (P2v3+). Simpler than AKS for monolithic apps but lacks Kubernetes orchestration.

```azurecli
az appservice plan create \
  --name plan-myapp \
  --resource-group rg-myapp \
  --sku P2V3 \
  --hyper-v
```

### Azure Container Instances (ACI)

For batch or short-lived workloads, ACI supports Windows Containers without cluster management overhead.

---

## Group Managed Service Accounts (gMSA)

Windows Containers cannot be domain-joined. For Active Directory authentication (e.g., Integrated Windows Authentication to SQL Server), use Group Managed Service Accounts (gMSA):

1. Create a gMSA in Active Directory.
2. Create a credential spec JSON using `CredentialSpec` PowerShell module.
3. Reference the credential spec in the pod spec (AKS) or container spec.

```yaml
# AKS pod spec with gMSA credential spec
securityContext:
  windowsOptions:
    gmsaCredentialSpecName: my-gmsa-credspec
```

This allows IIS and SQL Server integrated authentication without domain-joining the container.

---

## Cost and Operational Implications

| Factor | Windows Container | Linux Container (.NET 8/9) |
|---|---|---|
| Image size | 3-8 GB (Windows Server Core) | 200-400 MB (Alpine/Debian) |
| Start time | 30-90 seconds (IIS warm-up) | 2-10 seconds (Kestrel) |
| Node cost | Windows Server licensing included in Azure VM pricing | Linux VMs are cheaper |
| Patch cadence | Monthly Windows patch cycle required | Smaller attack surface, faster patches |
| AKS scaling speed | Slower (larger image, slower node provision) | Fast |

These costs justify the migration exit date. Capture the cost delta in the FinOps brief and use it to drive migration prioritisation.

---

## Migration Exit Criteria

Define these before deploying Windows Containers:

1. Exit date: maximum 18 months from first Windows Container deployment.
2. Migration milestone tracked in project backlog (link to migration phase plan).
3. Monthly review of migration progress vs. exit date.
4. Container image cost tracked in FinOps dashboard (see `/finops-architect`).

---

## References

- Windows Containers on AKS: https://learn.microsoft.com/azure/aks/windows-container-cli
- Containerising existing .NET Framework apps: https://learn.microsoft.com/virtualization/windowscontainers/quick-start/lift-shift-to-containers
- Docker image selection for .NET Framework: https://learn.microsoft.com/dotnet/architecture/microservices/net-core-net-framework-containers/net-container-os-targets
- gMSA for Windows Containers on AKS: https://learn.microsoft.com/azure/aks/use-group-managed-service-accounts
