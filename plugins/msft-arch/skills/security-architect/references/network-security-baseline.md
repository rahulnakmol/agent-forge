# Network Security Baseline

## Hub-Spoke Topology

All production deployments use hub-spoke topology. The hub VNet is the central connectivity and security enforcement point; spoke VNets contain workloads and connect to the hub via VNet peering.

```text
Internet
    |
Azure Front Door (WAF, global, OWASP 3.2)
    |
Hub VNet
├── Azure Firewall (egress control + DNS proxy)
├── Azure Bastion (jump-box replacement, no public IP on VMs)
├── Gateway subnet (ExpressRoute / VPN for hybrid)
└── Azure DDoS Protection Standard (covers Hub VNet + peered spokes)
    |
VNet Peering (no gateway transit unless hybrid)
    |
Spoke VNet(s)
├── App subnet → App Service VNet Integration / Container Apps Environment
├── API subnet → APIM (internal mode) / AKS node pools
├── Data subnet → Private Endpoints for SQL, Storage, Key Vault, Service Bus
└── Management subnet → Azure Monitor agents, backup
```

Key rules:
- No public IP addresses on workload VMs or data services. Public IP allowed only on Azure Firewall, Front Door, and Application Gateway.
- DDoS Protection Standard on the hub VNet. It protects all peered spoke VNets automatically.
- Azure Bastion for all VM administrative access. No jump-box VMs with public IPs.
- Azure Firewall in forced-tunnel mode for all spoke egress. All outbound traffic is inspected.

## NSG / ASG Patterns

**Network Security Groups (NSGs)** apply to subnets (preferred) or individual NICs (avoid unless absolutely necessary). NSG rules should be defined as code (Terraform / Bicep). Never define them manually in the portal.

**Application Security Groups (ASGs)** let you group NICs by role and reference the group in NSG rules instead of IP ranges. This decouples security rules from IP address management and survives VM scale-in/scale-out.

```hcl
# Terraform: ASG + NSG pattern
resource "azurerm_application_security_group" "api_servers" {
  name                = "asg-api-servers"
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_application_security_group" "db_servers" {
  name                = "asg-db-servers"
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_network_security_rule" "api_to_db" {
  name                                       = "allow-api-to-db-1433"
  priority                                   = 200
  direction                                  = "Inbound"
  access                                     = "Allow"
  protocol                                   = "Tcp"
  source_port_range                          = "*"
  destination_port_range                     = "1433"
  source_application_security_group_ids      = [azurerm_application_security_group.api_servers.id]
  destination_application_security_group_ids = [azurerm_application_security_group.db_servers.id]
  # ...
}
```

NSG design rules:
- Default deny all inbound from Internet. Add explicit allow rules only.
- Use service tags (`AzureMonitor`, `AzureActiveDirectory`, `Storage`, `AzureKeyVault`) instead of IP ranges for Microsoft-managed traffic.
- Log all NSG flow logs to Log Analytics (enabled via Network Watcher). Retention ≥ 90 days.
- Review NSG rules in quarterly access reviews. Remove unused allow rules.

## Azure Firewall vs WAF: When to Use Each

| Control | Azure Firewall | WAF (Front Door / App Gateway) |
|---|---|---|
| Layer | L3/L4 (+ L7 FQDN/URL filtering with Premium SKU) | L7 HTTP/HTTPS only |
| Scope | All protocols, all ports (VM/service egress and inter-spoke) | HTTP/HTTPS inbound to web applications only |
| Use for | Outbound internet filtering, east-west spoke traffic, hybrid on-prem | Inbound web traffic inspection, OWASP rule enforcement, bot protection |
| Cost signal | ~$1.25/hr for Standard SKU | Charged per policy + processed GB |

**Use Azure Firewall** for everything non-HTTP and for enforcing egress allow-lists (e.g., only allow spoke VMs to reach `*.microsoft.com`, `*.azure.com`).

**Use WAF** at the ingress layer for every internet-facing web application. Start in Detection mode; promote to Prevention after 2 weeks of false-positive review. Enable bot protection rules.

## Private Endpoints Baseline

Private endpoints for data services in production. Public endpoints only with WAF + IP restrictions justified by ADR.

```hcl
# Terraform: private endpoint for Azure SQL
resource "azurerm_private_endpoint" "sql" {
  name                = "pe-sql-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = azurerm_subnet.data.id

  private_service_connection {
    name                           = "psc-sql"
    private_connection_resource_id = azurerm_mssql_server.main.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "sql-dns-zone-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.sql.id]
  }
}

# Disable public access after private endpoint is healthy
resource "azurerm_mssql_server" "main" {
  # ...
  public_network_access_enabled = false
}
```

Private endpoint required for: Azure SQL, PostgreSQL Flexible Server, Cosmos DB, Storage accounts, Key Vault, Service Bus, Event Hub, Azure Cache for Redis, Azure Cognitive Services endpoints.

After provisioning, validate private DNS resolution from within the spoke VNet before disabling public access. DNS resolution must use the hub Azure Firewall as DNS proxy → forwarded to private DNS zones.

## Service Tag Usage

Use service tags in NSG rules instead of managing IP ranges manually. Microsoft maintains service tag IP lists; they update automatically.

Common service tags:
- `AzureMonitor`: outbound from VMs to Azure Monitor / Log Analytics
- `AzureActiveDirectory`: outbound for Entra ID authentication
- `AzureKeyVault`: outbound to Key Vault (before private endpoint)
- `Storage`: outbound to Azure Storage
- `AzureLoadBalancer`: required inbound for health probes
- `VirtualNetwork`: allow intra-VNet traffic

## Bastion for Jump-box Access

Azure Bastion replaces jump-box VMs and eliminates the need for any public IP on management VMs.

```hcl
resource "azurerm_bastion_host" "hub" {
  name                = "bastion-hub"
  resource_group_name = azurerm_resource_group.hub.name
  location            = var.location

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.bastion.id   # AzureBastionSubnet, /26 minimum
    public_ip_address_id = azurerm_public_ip.bastion.id
  }

  sku = "Standard"   # Required for native client support (RDP/SSH via Azure CLI)
}
```

Bastion Standard SKU is required for native RDP/SSH client access, session recording (audit), and shareable links. Do not use Basic SKU for production environments.
