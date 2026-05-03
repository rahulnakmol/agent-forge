# Dashboards and Alerting Design

Two visualisation tools serve different audiences. Azure Workbooks own operational + application dashboards (KQL-backed, co-located with Log Analytics). Azure Managed Grafana owns infrastructure and Prometheus dashboards. Never use the Azure portal "Dashboards" blade as the primary operational surface; it lacks drill-down and is hard to version-control.

## Azure Workbooks

Workbooks are parameterised, interactive reports backed by KQL queries against Log Analytics + App Insights. Deploy via ARM/Bicep/Terraform from a versioned JSON template; never build Workbooks manually in the portal for shared operational use.

### Workbook structure per operational domain

Each domain gets one Workbook with a consistent tab structure:

```text
[Overview]     SLO status, top errors, request volume (last 24h)
[Availability] Availability rate over time; top failing operations; geographic distribution
[Performance]  p50/p95/p99 latency; slow dependency calls; top slow endpoints
[Errors]       Exception rate; top exception types; structured log errors with property drill-down
[Traces]       Distributed trace lookup by correlation ID; waterfall view
[Capacity]     Request volume trends; dependency call trends; ingestion volume
```

### Workbook template pattern (Bicep excerpt)

```bicep
resource workbook 'Microsoft.Insights/workbooks@2022-04-01' = {
  name: guid('order-service-operations')
  location: location
  kind: 'shared'
  properties: {
    displayName: 'Order Service - Operations'
    category: 'workbook'
    sourceId: appInsights.id
    serializedData: loadTextContent('workbooks/order-service-ops.workbook.json')
  }
}
```

The `serializedData` is the exported JSON from the Workbook editor. Check it into source control and deploy via CI/CD; this makes Workbook changes reviewable and rollback-capable.

### Key Workbook parameters

Always include these time-range parameters at the top of every Workbook:

```json
{
  "parameters": [
    {
      "id": "time-range",
      "type": 4,
      "label": "Time Range",
      "value": { "durationMs": 86400000 },
      "typeSettings": { "selectableValues": [
        { "durationMs": 900000, "label": "Last 15 minutes" },
        { "durationMs": 3600000, "label": "Last 1 hour" },
        { "durationMs": 86400000, "label": "Last 24 hours" },
        { "durationMs": 604800000, "label": "Last 7 days" }
      ]}
    },
    {
      "id": "service-filter",
      "type": 2,
      "label": "Service",
      "query": "AppRequests | distinct AppRoleName",
      "typeSettings": { "multiSelect": true }
    }
  ]
}
```

## Azure Managed Grafana

Use Azure Managed Grafana (Standard tier) for:
- Kubernetes / AKS infrastructure dashboards (backed by Azure Monitor managed Prometheus)
- Cross-service Prometheus metric views
- Combined KQL + Prometheus panels on a single canvas

**Setup pattern**:
1. Create an Azure Monitor workspace (receives Prometheus scrape data from AKS).
2. Enable Azure Monitor managed Prometheus on the AKS cluster.
3. Create Azure Managed Grafana (Standard tier) and link to the Azure Monitor workspace.
4. Grafana managed identity receives `Monitoring Data Reader` on the Azure Monitor workspace automatically.
5. Import community AKS dashboards (IDs: 15760, 14205, 16611) as starting templates.

Managed Grafana uses Managed Identity; no static API keys. Grafana Standard tier supports Azure AD SSO natively; configure Entra ID app registration for user access.

```hcl
resource "azurerm_dashboard_grafana" "main" {
  name                              = "grafana-${var.workload}-${var.environment}"
  resource_group_name               = var.resource_group_name
  location                          = var.location
  sku                               = "Standard"
  grafana_major_version             = 11
  zone_redundancy_enabled           = var.environment == "prod"
  api_key_enabled                   = false  # Use Managed Identity only
  deterministic_outbound_ip_enabled = false

  azure_monitor_workspace_integrations {
    resource_id = azurerm_monitor_workspace.main.id
  }

  identity {
    type = "SystemAssigned"
  }
}
```

## Azure Monitor Alert Rules

### Alert hierarchy

Three layers of alerting, each with appropriate severity and action group:

| Layer | Alert type | Examples | Severity |
|---|---|---|---|
| SLO signals | Burn-rate log search alerts | Fast burn, slow burn (see slo-design.md) | 0 (Critical), 1 (Error) |
| Operational signals | Metric + log search alerts | Error rate spike, p99 > threshold, dependency failures | 1 (Error), 2 (Warning) |
| Infrastructure signals | Platform metric alerts | CPU > 80%, memory pressure, disk full | 2 (Warning), 3 (Informational) |

### Action group hierarchy

```hcl
# Critical -- wake someone up immediately
resource "azurerm_monitor_action_group" "critical" {
  name                = "ag-${var.workload}-critical"
  resource_group_name = var.resource_group_name
  short_name          = "critical"

  email_receiver {
    name          = "on-call-team"
    email_address = var.oncall_email
  }

  webhook_receiver {
    name        = "pagerduty"
    service_uri = var.pagerduty_webhook_url
  }

  arm_role_receiver {
    name                    = "monitoring-contributor"
    role_id                 = "749f88d5-cbae-40b8-bcfc-e573ddc772fa"
    use_common_alert_schema = true
  }
}

# Warning -- Teams channel notification
resource "azurerm_monitor_action_group" "warning" {
  name                = "ag-${var.workload}-warning"
  resource_group_name = var.resource_group_name
  short_name          = "warning"

  microsoft_teams_receiver {
    name    = "ops-channel"
    webhook = var.teams_webhook_url
  }
}
```

### Standard metric alert rules

Provision these alert rules for every App Service / Functions / Container Apps deployment:

```hcl
# HTTP 5xx rate alert
resource "azurerm_monitor_metric_alert" "http5xx" {
  name                = "alert-${var.app_name}-http5xx"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_linux_web_app.main.id]
  description         = "HTTP 5xx error rate elevated"
  severity            = 1
  frequency           = "PT1M"
  window_size         = "PT5M"

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "Http5xx"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 10  # adjust per SLO budget
  }

  action {
    action_group_id = azurerm_monitor_action_group.warning.id
  }
}

# Response time p95 alert
resource "azurerm_monitor_metric_alert" "response_time" {
  name                = "alert-${var.app_name}-response-time"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_linux_web_app.main.id]
  description         = "Average response time exceeds 2 seconds"
  severity            = 2
  frequency           = "PT5M"
  window_size         = "PT15M"

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "AverageResponseTime"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 2  # seconds
  }

  action {
    action_group_id = azurerm_monitor_action_group.warning.id
  }
}
```

## Dashboard-as-Code discipline

- All Workbook JSON in source control under `infra/monitoring/workbooks/`.
- All alert rule definitions in Terraform under `infra/monitoring/alerts.tf`.
- All action groups in Terraform under `infra/monitoring/action-groups.tf`.
- Deployed in CI/CD as part of the infrastructure pipeline; never manually created.
- Workbook JSON exported from portal after initial design, committed, reviewed in PR.
