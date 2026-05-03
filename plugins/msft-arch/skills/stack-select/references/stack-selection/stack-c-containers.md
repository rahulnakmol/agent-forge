---
category: stack-selection
loading_priority: 4
tokens_estimate: 2400
keywords:
  - containers
  - kubernetes
  - AKS
  - container apps
  - DAPR
  - GitOps
  - Flux
  - ArgoCD
  - Helm
  - service mesh
  - KEDA
  - CNAB
  - container registry
  - microservices
version: "1.0"
last_updated: "2026-03-21"
---

# Stack C: Containers

Stack C extends Stack B by adding container orchestration for workloads that require polyglot runtimes, fine-grained resource control, sidecar patterns, or massive horizontal scale. Power Platform and Azure PaaS remain integral; containers handle the workloads that PaaS services cannot serve efficiently.

Stack C is the most operationally complex stack. Only adopt it when the decision criteria below are clearly met. Unnecessary container adoption increases cost, staffing requirements, and operational risk.

## Azure Kubernetes Service (AKS)

AKS is the fully managed Kubernetes offering on Azure. It handles control plane management, node provisioning, and platform upgrades while giving full access to the Kubernetes API.

### Cluster Architecture

**System node pools:** Dedicated to Kubernetes system components (CoreDNS, metrics-server, kube-proxy). Use a minimum of 3 nodes across availability zones for production. Taint system nodes to prevent application workloads from scheduling on them.

**User node pools:** Host application workloads. Create separate node pools for different workload profiles:
- General-purpose pool (D-series VMs): Standard web APIs, background workers.
- Memory-optimized pool (E-series VMs): In-memory caches, data processing.
- GPU pool (NC-series VMs): Machine learning inference, video processing.
- Spot pool (discounted, preemptible VMs): Batch processing, non-critical background tasks. Savings of 60-90% but VMs can be evicted with 30-second notice.

**Availability zones:** Spread nodes across three availability zones for 99.99% SLA (vs 99.95% for single-zone). Zone-redundant deployments protect against datacenter-level failures. Persistent volumes must use ZRS (Zone-Redundant Storage) for cross-zone pod rescheduling.

### Networking

**Azure CNI:** Assigns Azure VNet IP addresses directly to pods. Pods are first-class VNet citizens with full connectivity to other Azure resources. Use Azure CNI for production clusters that need: direct pod-to-PaaS connectivity, network policy enforcement, Windows node pools.

**Azure CNI Overlay:** Assigns pod IPs from a private CIDR overlay network, conserving VNet address space. Use when VNet IP exhaustion is a concern (large clusters with many pods per node).

**Network policies:** Enforce pod-to-pod traffic rules using Kubernetes NetworkPolicy resources. Choose between Azure Network Policy (Azure-native, basic) and Calico Network Policy (richer features, broader community). Default-deny all traffic, then explicitly allow required flows.

**Ingress controllers:**
- *NGINX Ingress Controller:* Community standard. TLS termination, path-based routing, rate limiting, basic WAF-like features. Deploy via Helm chart with internal or external load balancer.
- *Application Gateway Ingress Controller (AGIC):* Uses Azure Application Gateway as the ingress. Provides WAF v2, SSL offload, cookie-based affinity, and Azure Monitor integration. Preferred when WAF requirements exist or when leveraging existing Application Gateway infrastructure.

### Service Mesh

Service mesh adds observability, security, and traffic management between services without application code changes.

**Istio:** The most feature-rich service mesh. Provides: mTLS between all services (zero-trust networking), traffic splitting (canary deployments), circuit breakers, retry policies, distributed tracing (Jaeger/Zipkin), and Kiali dashboard for service graph visualization. Overhead: 10-15% CPU and memory per pod for the Envoy sidecar proxy.

**Linkerd:** Lightweight alternative to Istio. Lower resource overhead (~5% per pod), simpler configuration, Rust-based data plane. Provides: mTLS, traffic splitting, retries, observability. Choose Linkerd when mTLS and observability are the primary needs without requiring Istio's full feature set.

**Open Service Mesh (OSM):** Microsoft-contributed CNCF project. Lightweight, SMI-compatible. Suitable for simpler scenarios but less mature than Istio or Linkerd. Consider for Microsoft-aligned shops that want vendor alignment.

### Security

**Pod security:** Use Pod Security Standards (Restricted, Baseline, Privileged) enforced through Pod Security Admission. Restricted profile: no root containers, no privilege escalation, read-only root filesystem, non-root UID. Apply Restricted to all namespaces; grant exceptions explicitly.

**Workload identity:** Replace pod-managed identity with workload identity federation. Pods authenticate to Azure services using Kubernetes service accounts federated with Entra ID managed identities. No secrets stored in pods. This is the recommended pattern for all pod-to-Azure-service authentication.

**Azure Key Vault CSI Driver:** Mount Key Vault secrets as files in pod volumes. Secrets rotate automatically without pod restarts when using the rotation feature. Use for: database connection strings, API keys, TLS certificates. Avoid Kubernetes Secrets for sensitive values; they are base64-encoded, not encrypted at rest by default.

**Image security:** Enable Microsoft Defender for Containers for vulnerability scanning of container images in ACR. Enforce image signing with Notary/cosign. Use admission controllers (OPA Gatekeeper, Kyverno) to block deployment of unsigned or vulnerable images.

### Scaling

**Horizontal Pod Autoscaler (HPA):** Scale pod replicas based on CPU, memory, or custom metrics. Configure target utilization (e.g., CPU 60%) with min/max replica bounds. HPA evaluates every 15 seconds by default.

**Vertical Pod Autoscaler (VPA):** Adjusts pod CPU and memory requests based on observed usage. Use VPA in recommendation mode first to understand actual resource needs, then switch to auto mode for non-critical workloads. Do not use VPA and HPA on the same metric simultaneously.

**KEDA (Kubernetes Event-Driven Autoscaling):** Scale pods based on external event sources: Service Bus queue depth, Kafka lag, Cosmos DB change feed, HTTP request rate, custom Prometheus metrics. KEDA enables scale-to-zero for event-driven workloads, which is not possible with HPA alone. Use KEDA for: queue workers, event processors, batch handlers.

**Cluster Autoscaler:** Automatically adds or removes nodes based on pending pods that cannot be scheduled (scale-up) or underutilized nodes (scale-down). Configure scale-down delay (default 10 minutes) and minimum/maximum node count per node pool. Cluster autoscaler works alongside HPA: HPA adds pods, cluster autoscaler adds nodes to accommodate them.

### Monitoring

**Container Insights:** Azure Monitor for Containers. Collects container logs, performance metrics (CPU, memory, network), and Kubernetes events. Queries via Log Analytics using KQL. Pre-built dashboards show cluster, node, and pod-level health.

**Prometheus and Grafana:** Azure Managed Prometheus collects metrics from pods exposing `/metrics` endpoints. Azure Managed Grafana provides dashboards. Use Prometheus for application-level metrics (request latency, error rate, queue depth). The managed offerings reduce operational burden compared to self-hosted Prometheus/Grafana.

**Alerting:** Configure alerts on: node CPU > 80%, pod restart count > 3 in 10 minutes, container memory working set > 90% of limit, DaemonSet pods not running on all nodes, persistent volume usage > 85%.

## Azure Container Apps

Container Apps provides a serverless container hosting platform built on Kubernetes (KEDA, Envoy, DAPR) without exposing Kubernetes complexity.

### When to Use Container Apps vs AKS

| Scenario | Container Apps | AKS |
|---|---|---|
| Simple HTTP APIs and microservices | Preferred. Simpler setup, built-in scaling. | Overkill for simple scenarios. |
| Event-driven background workers | Preferred. Built-in KEDA scaling, scale-to-zero. | Use if already running AKS cluster. |
| Need for sidecar patterns, service mesh | Limited. DAPR provides some capabilities. | Required for full service mesh (Istio/Linkerd). |
| Fine-grained resource control | Not available. Platform manages infrastructure. | Full control over node types, resource quotas. |
| GPU workloads | Not supported. | Required for GPU workloads. |
| Windows containers | Not supported. | Supported via Windows node pools. |
| Team Kubernetes expertise | Low/None. Container Apps abstracts K8s. | Required. Team must operate K8s clusters. |
| Cost at low scale | Lower. Pay for actual vCPU/memory consumption. | Higher. Pay for node VMs regardless of utilization. |
| Cost at high scale | Higher per unit. Consumption pricing adds up. | Lower per unit. VM-based pricing more efficient. |

### DAPR Integration

DAPR (Distributed Application Runtime) is built into Container Apps and provides building blocks for microservices:

- **Service invocation:** Call other services by name with automatic service discovery, mTLS, retries, and observability. No need to manage DNS or service URLs.
- **State management:** Pluggable state stores (Cosmos DB, Redis, Azure SQL) with consistent API. Application code uses DAPR SDK/HTTP API; state store is configured per environment.
- **Pub/sub:** Publish and subscribe to messages using pluggable brokers (Service Bus, Event Hubs, Redis Streams). Application code is broker-agnostic; swapping message brokers requires only configuration change.
- **Bindings:** Input and output bindings connect to external systems (blob storage, SMTP, Twilio, Cron) without SDK dependencies. Input bindings trigger the app; output bindings send data.

### Revisions and Traffic Splitting

Container Apps supports multiple active revisions for blue-green and canary deployments. Route a percentage of traffic to a new revision (e.g., 10% to v2, 90% to v1) and gradually increase. Revisions that receive 0% traffic scale to zero automatically.

### Scale Rules

Configure scale rules based on: HTTP concurrent requests, KEDA scalers (queue length, CPU, custom metrics), TCP connections. Set minimum replicas to 0 for scale-to-zero (cold start applies) or 1+ for always-warm.

## Cloud-Native Application Bundles (CNAB)

CNAB is a packaging format for distributing multi-service cloud applications as a single installable unit.

### Porter

Porter is the primary CNAB tool. It packages a multi-service application (AKS manifests, Helm charts, Azure resource templates, configuration) into a single bundle that can be installed, upgraded, and uninstalled as an atomic unit.

**Use cases:**
- Distributing a reference architecture (AKS cluster + database + monitoring + application) as a single installable package.
- Creating repeatable environment provisioning for complex Stack C deployments.
- ISV distribution of cloud-native applications to customer Azure subscriptions.

**Bundle contents:** Dockerfile (invocation image), porter.yaml (manifest), mixins (Helm, Terraform, Azure CLI, Kubernetes), parameter and credential definitions.

### Distributing Bundled Applications

Store CNAB bundles in OCI-compliant registries (ACR supports CNAB artifacts). Distribute bundles to teams or customers via ACR with RBAC controls. Version bundles semantically; reference specific versions in deployment pipelines.

## GitOps Deployment Patterns

GitOps uses Git as the single source of truth for declarative infrastructure and application deployments. Changes are applied by an operator running in the cluster that continuously reconciles cluster state with the Git repository.

### Flux v2

Flux v2 is the CNCF GitOps operator recommended for AKS.

**GitRepository:** Points Flux to a Git repository containing Kubernetes manifests. Flux polls the repository (configurable interval, default 1 minute) and detects changes.

**Kustomization:** Applies Kustomize overlays from the Git repository. Use for environment-specific configuration (dev/staging/prod overlays on a shared base). Kustomization resources define dependencies, health checks, and pruning policies.

**HelmRelease:** Manages Helm chart deployments declaratively. Flux installs, upgrades, and rolls back Helm releases based on the HelmRelease resource definition in Git. Combines with HelmRepository sources pointing to Helm chart registries.

**Multi-tenancy:** Use Flux with namespace-scoped tenants. Each team gets a namespace with its own GitRepository, Kustomization, and RBAC. Platform team manages cluster-wide resources through a separate Flux configuration.

### ArgoCD

ArgoCD is an alternative GitOps operator with a richer UI and broader ecosystem.

**Application CRD:** Define an ArgoCD Application that points to a Git repo path and target cluster/namespace. ArgoCD continuously compares the desired state (Git) with the live state (cluster) and shows drift.

**Sync policies:** Auto-sync applies changes automatically when Git changes. Manual sync requires operator approval. Self-heal reverts manual cluster changes to match Git. Prune deletes resources removed from Git.

**Rollback:** ArgoCD maintains a history of deployed revisions. One-click rollback to any previous revision through the UI or CLI. Rollback reapplies the previous Git commit's manifests.

**Choosing Flux vs ArgoCD:**
- Flux: Lighter weight, better multi-tenancy, native AKS extension support, declarative-only (no UI required).
- ArgoCD: Richer UI for visualization, application-of-apps pattern for large deployments, broader plugin ecosystem.
- Both are CNCF graduated projects and production-ready.

## Container vs PaaS Decision Criteria

Use this checklist to determine whether a workload belongs in containers (Stack C) or PaaS (Stack B):

**Choose containers when:**
- Workload requires a runtime not supported by Azure Functions or App Service (e.g., Rust, Elixir, custom-compiled binaries).
- Application architecture uses sidecar patterns (logging agents, auth proxies, protocol adapters) that require multi-container pods.
- Team needs fine-grained resource allocation (specific CPU/memory limits per service, resource quotas per namespace).
- Application consists of 10+ microservices that benefit from service mesh capabilities (mTLS, traffic management, circuit breaking).
- Workload needs GPU compute (ML inference, video transcoding).
- Organization has platform engineering capability to operate Kubernetes clusters.

**Choose PaaS when:**
- Workload is a stateless HTTP API or event-driven function (Azure Functions handles this simpler and cheaper).
- Team lacks Kubernetes expertise and the learning curve is not justified by the workload requirements.
- Application has fewer than 5 services; the overhead of container orchestration exceeds the architectural benefit.
- Cold start latency is acceptable (Functions consumption plan) or addressable with premium plan.
- Budget constraints favor consumption-based pricing over dedicated VM node pools.

**Choose Container Apps when:**
- Need container packaging (custom runtime, dependency isolation) but not full Kubernetes control.
- Event-driven scaling with scale-to-zero is important for cost management.
- DAPR building blocks address the microservice communication patterns needed.
- Team wants container benefits without Kubernetes operations burden.

**Default rule:** Start with Functions/App Service. Move to Container Apps if you need container packaging. Move to AKS only if you need full Kubernetes capabilities. Never start with AKS unless the requirements clearly demand it.

## Container Registry

**Azure Container Registry (ACR):** Managed Docker registry on Azure. Tiers: Basic ($5/month, 10GB), Standard ($20/month, 100GB), Premium ($50/month, 500GB, geo-replication, private link).

**Image scanning:** Microsoft Defender for Containers scans images pushed to ACR for OS and language-level vulnerabilities. Integrate scanning into CI/CD pipelines with a quality gate: block deployment of images with Critical or High severity vulnerabilities.

**Helm chart repository:** ACR supports OCI artifact storage, including Helm charts. Push Helm charts to ACR alongside container images. Reference ACR as a Helm repository in Flux HelmRepository resources or ArgoCD Application manifests.

**Image lifecycle:** Enable retention policies to automatically delete untagged manifests after N days (default: disabled). Tag images with Git commit SHA for traceability. Use semantic version tags (v1.2.3) for release images. Never use the `latest` tag in production manifests.

## DevOps for Container Workloads

### GitHub Actions

Build container images in GitHub Actions workflows:
1. Checkout code.
2. Build Docker image with build args for environment-specific configuration.
3. Scan image with Trivy or Microsoft Defender.
4. Push to ACR using `azure/docker-login` action.
5. Update GitOps repository with new image tag (for Flux/ArgoCD to detect and deploy).

### Azure DevOps Pipelines

Equivalent pipeline structure:
1. Build stage: Docker build, test, scan.
2. Push stage: Push to ACR with image tag.
3. Deploy stage (if not using GitOps): Helm upgrade or kubectl apply with the new image tag.
4. For GitOps: Pipeline updates the manifest repository; Flux/ArgoCD handles deployment.

### Pipeline Best Practices

- Use multi-stage Dockerfiles to minimize image size (build stage with SDK, runtime stage with minimal base image).
- Cache Docker layers in CI to reduce build times (use `docker/build-push-action` with cache-from/cache-to).
- Run security scanning before pushing to registry. Fail the pipeline on Critical vulnerabilities.
- Sign images with cosign in the pipeline. Verify signatures in admission controllers.
- Separate CI (build and push) from CD (deploy). CI produces an artifact (image); CD consumes it. This enables deploying the same image to multiple environments.
