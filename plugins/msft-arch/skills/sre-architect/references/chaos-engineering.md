# Chaos Engineering Reference

**Used by**: `sre-architect` Step 5  
**Tool**: Azure Chaos Studio (API version `2025-01-01`, latest stable)  
**Verify**: `microsoft_docs_search "Azure Chaos Studio fault library"` before finalizing experiment designs. Fault capabilities expand quarterly.

---

## Principle

Chaos engineering in production (with safety controls) over only in staging. Staging environments diverge from production in load profile, data shape, connection counts, and dependency topology. A chaos experiment that passes in staging can still fail in production for reasons staging cannot simulate.

Safety controls make production chaos safe:
1. Abort conditions tied to Azure Monitor alerts.
2. Experiments run during low-traffic windows (not business-critical hours).
3. Blast radius limited to a single AZ, a single instance, or a single dependency at a time.
4. Every experiment is preceded by a verified steady-state.

---

## Chaos Experiment Structure

Azure Chaos Studio experiments follow a hierarchy:

```
Experiment
  Step 1 (sequential with Step 2)
    Branch A (parallel with Branch B within the step)
      Action 1: fault injection
      Action 2: delay
    Branch B
      Action 1: start load test
  Step 2
    Branch A
      Action 1: second fault (after Step 1 completes)
```

Use multiple branches within a step to run concurrent faults (e.g., inject network latency on the API service while simultaneously loading the database).

---

## Fault Types

### Service-Direct Faults

Run against Azure resources via Azure Resource Manager. No agent required.

| Resource type | ARM type | Available faults |
|---|---|---|
| App Service | `Microsoft.Web/sites` | Stop App Service |
| AKS | `Microsoft.ContainerService/managedClusters` | Chaos Mesh: DNS, HTTP, IO, Kernel, Network, Pod, Stress, Time |
| Cosmos DB | `Microsoft.DocumentDB/databaseAccounts` | Cosmos DB Failover |
| Event Hubs | `Microsoft.EventHub/namespaces` | Change Event Hub State |
| Service Bus | `Microsoft.ServiceBus/namespaces` | Change Queue/Topic/Subscription State |
| Azure Cache for Redis | `Microsoft.Cache/redis` | Reboot |
| Key Vault | `Microsoft.KeyVault/vaults` | Deny Access, Disable Certificate, Increment Certificate Version, Update Certificate Policy |
| NSG | `Microsoft.Network/networkSecurityGroups` | NSG Security Rule |
| Virtual Machine (service-direct) | `Microsoft.Compute/virtualMachines` | VM Redeploy, VM Shutdown |
| Virtual Machine Scale Set | `Microsoft.Compute/virtualMachineScaleSets` | VMSS Shutdown, VMSS Shutdown 2.0 (by AZ) |
| Autoscale Settings | `Microsoft.Insights/autoscaleSettings` | Disable Autoscale |

### Agent-Based Faults

Require the Chaos Agent VM extension installed on the target VM or VMSS. Agent authenticates via user-assigned Managed Identity.

| Fault | OS | Scenario |
|---|---|---|
| CPU Pressure | Windows, Linux | Compute saturation |
| Physical Memory Pressure | Windows, Linux | Memory exhaustion |
| Virtual Memory Pressure | Windows | Paging pressure |
| Kill Process | Windows, Linux | Dependency process failure |
| Stop Service | Windows, Linux | Service disruption |
| Network Disconnect | Windows, Linux (outbound) | Network isolation |
| Network Latency | Windows, Linux (outbound) | Latency injection |
| Network Packet Loss | Windows, Linux (outbound) | Reliability under loss |
| Network Isolation | Windows, Linux (outbound) | Full partition |
| DNS Failure | Windows | DNS resolution failure |
| DiskIO Pressure | Windows, Linux | Disk I/O saturation |
| Linux Arbitrary Stress-ng | Linux | General system stress |
| Time Change | Windows | Clock skew scenarios |

### Orchestration Actions

| Action | Purpose |
|---|---|
| Start/Stop Azure Load Testing | Combine load test with fault injection |
| Delay | Time-gate steps within an experiment |

---

## Regional Availability

Chaos Studio is a regional service. Experiment creation and resource targeting are available in different region sets.

**Regions supporting both experiment creation and resource targeting (as of 2026):**
East US, East US 2, West Central US, West US, North Central US, Central US, UK South, Southeast Asia, Japan East, West Europe, Sweden Central, Brazil South, Australia East.

**Regions supporting resource targeting only** (cross-region targeting: experiment in one region, target in another):
South Central US, West US 2, West US 3, Canada Central, UAE North, East Asia, North Europe, Germany West Central, France Central, Italy North.

Always verify current availability: `microsoft_docs_search "Azure Chaos Studio regional availability"`.

---

## Experiment Design Process

### 1. Define the Steady-State Hypothesis

Before injecting any fault, define measurable conditions that confirm the system is healthy. Express as KQL queries or Azure Monitor metric conditions.

Example:
```
Steady state: orders-api availability SLI > 99.9% over the last 5 minutes
              p99 request latency < 500ms
              Message queue depth < 100
```

Verify steady state is met before starting the experiment. Abort the experiment if the steady state is already violated before injection.

### 2. Define the Abort Condition

Every experiment must have an automatic abort condition: an Azure Monitor alert or metric that stops the experiment if the blast radius exceeds expectation.

Configure in the experiment as a stop signal (Azure Monitor alert integration in Chaos Studio) or as an Azure Monitor action group that calls the Chaos Studio REST API to cancel the running experiment.

Example abort conditions:
- Fast-burn alert fires for the SLO under test.
- Error rate exceeds 1% for 5 consecutive minutes.
- Any downstream dependency alerts.

### 3. Scope the Blast Radius

Start narrow. First run: single instance or single zone. Subsequent runs: increase scope only after the system demonstrates the expected behavior at smaller scope.

| Run | Scope | Goal |
|---|---|---|
| 1 | 1 pod / 1 VM instance | Confirm circuit breaker trips correctly |
| 2 | 1 Availability Zone | Confirm AZ failover works end-to-end |
| 3 | Single region | Confirm cross-region failover (if applicable) |

### 4. Run the Experiment

Execute during a defined low-traffic window. Have the Operations Lead monitoring the SLO dashboard and ready to manually abort if the abort condition is not triggering automatically.

### 5. Record Results

For each experiment, record:
- Did steady state hold during and after the fault?
- Did the abort condition work as designed?
- What unexpected behaviors were observed?
- What action items arose?

Log results in `docs/sre/chaos-log.md`.

---

## Chaos Experiment Backlog Template

Store in `docs/sre/chaos-backlog.md`. Prioritize by SLO impact (experiments that cover the highest-value SLO first).

| Priority | Hypothesis | Fault type | Target resource | Abort condition | Status |
|---|---|---|---|---|---|
| P1 | API availability SLO holds during single-AZ VMSS loss | VMSS Shutdown 2.0 (1 AZ) | orders-api VMSS | Error rate > 1% for 5 min | Not started |
| P1 | Cosmos DB failover completes within RPO | Cosmos DB Failover | orders-db account | App error rate > 2% | Not started |
| P2 | Circuit breaker trips correctly on downstream App Service stop | Stop App Service | payments-api | SLO fast-burn alert fires | Not started |
| P2 | Redis cache miss handled gracefully | Redis Reboot | app-cache | Error rate > 0.5% for 3 min | Not started |
| P3 | Service Bus queue disruption handled with backlog drain | Change Queue State | orders-bus | Message lag > 10,000 | Not started |
| P3 | Key Vault access denied, retry succeeds | Key Vault Deny Access | app-keyvault | App errors > 1% | Not started |

---

## IaC: Terraform Chaos Experiment

Use the AzAPI Terraform provider for Chaos Studio resources (AzureRM provider coverage is limited).

```hcl
// Chaos Studio target (service-direct VM)
resource "azapi_resource" "chaos_target_vm" {
  type      = "Microsoft.Compute/virtualMachines/providers/targets@2025-01-01"
  // or equivalently: Microsoft.Chaos/targets@2025-01-01 as child of the VM
  name      = "Microsoft-VirtualMachine"
  parent_id = var.vm_resource_id
  body = {}
}

// Chaos Studio experiment
resource "azapi_resource" "chaos_experiment_az_loss" {
  type      = "Microsoft.Chaos/experiments@2025-01-01"
  name      = "exp-az-loss-orders-api"
  location  = var.location
  parent_id = var.resource_group_id

  body = {
    identity = {
      type = "SystemAssigned"
    }
    properties = {
      steps = [
        {
          name = "AZ-Loss"
          branches = [
            {
              name = "Shutdown-AZ1"
              actions = [
                {
                  type = "continuous"
                  name = "urn:csci:microsoft:virtualMachineScaleSet:shutdown/2.0"
                  parameters = [
                    { key = "abruptShutdown", value = "false" },
                    { key = "zones", value = "[\"1\"]" }
                  ]
                  duration    = "PT5M"
                  selectorId  = "vmss-selector"
                }
              ]
            }
          ]
        }
      ]
      selectors = [
        {
          type = "List"
          id   = "vmss-selector"
          targets = [
            {
              type = "ChaosTarget"
              id   = azapi_resource.chaos_target_vmss.id
            }
          ]
        }
      ]
    }
  }
}
```

Never create chaos experiments manually in production. All experiments in source control and applied via CI/CD.

---

## Safety Checklist Before Running Any Experiment

- [ ] Steady-state hypothesis documented and currently verified.
- [ ] Abort condition configured and tested.
- [ ] Low-traffic window confirmed (no business-critical events in the next 2 hours).
- [ ] Operations Lead actively monitoring the SLO dashboard.
- [ ] On-call engineer aware and ready.
- [ ] Rollback plan documented (what to do if the experiment cannot be automatically aborted).
- [ ] Stakeholders notified (for P1 hypothesis experiments in production).
