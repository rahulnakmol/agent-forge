# Azure Pricing API Patterns

This file covers the Azure Retail Prices API, Cost Management Query API, Cost Exports API, Benefit Recommendations API, and Carbon Optimization API. Use these patterns to build cost estimation tools, CI/CD cost gates, and FinOps dashboards.

Use `microsoft_docs_search` to verify current API versions before production use; Azure API versions increment regularly.

---

## Azure Retail Prices API (no auth required)

The Retail Prices API returns public list prices for any Azure service in any region. It does not require authentication and is suitable for pre-purchase cost estimation and CI/CD cost checks.

Base URL: `https://prices.azure.com/api/retail/prices`

### Get all prices for a service in a region

```bash
# All App Service Premium V3 prices in East US
curl "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&\$filter=serviceName eq 'Azure App Service' and armRegionName eq 'eastus' and skuName eq 'P1 v3'"
```

### Filter by meter name pattern

```bash
# Virtual Machine D-series prices in East US (Linux)
curl "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&\$filter=serviceName eq 'Virtual Machines' and armRegionName eq 'eastus' and contains(skuName, 'D4s') and priceType eq 'Consumption'"
```

### Response schema

```json
{
  "BillingCurrency": "USD",
  "CustomerEntityId": "Default",
  "CustomerEntityType": "Retail",
  "Items": [
    {
      "currencyCode":    "USD",
      "tierMinimumUnits": 0.0,
      "retailPrice":      0.192,
      "unitPrice":        0.192,
      "armRegionName":   "eastus",
      "location":        "US East",
      "effectiveStartDate": "2023-01-01T00:00:00Z",
      "meterId":         "abc123...",
      "meterName":       "D4s v5",
      "productId":       "DZH318Z0BPS6",
      "skuId":           "DZH318Z0BPS6/00CD",
      "productName":     "Virtual Machines D Series Windows",
      "skuName":         "D4s v5",
      "serviceName":     "Virtual Machines",
      "serviceId":       "DZH313Z7MMC8",
      "serviceFamily":   "Compute",
      "unitOfMeasure":   "1 Hour",
      "type":            "Consumption",
      "isPrimaryMeterRegion": true,
      "armSkuName":      "Standard_D4s_v5"
    }
  ],
  "NextPageLink": "https://prices.azure.com/api/retail/prices?...",
  "Count": 1
}
```

### Python: Retail Prices API client

```python
import httpx
from dataclasses import dataclass

PRICES_API_BASE = "https://prices.azure.com/api/retail/prices"
API_VERSION = "2023-01-01-preview"

@dataclass
class PriceItem:
    sku_name: str
    retail_price: float
    unit_of_measure: str
    arm_region_name: str
    service_name: str

def get_vm_prices(sku_name: str, region: str) -> list[PriceItem]:
    """Return retail prices for a VM SKU in a region."""
    filter_expr = (
        f"armSkuName eq '{sku_name}' "
        f"and armRegionName eq '{region}' "
        f"and priceType eq 'Consumption' "
        f"and contains(productName, 'Linux')"
    )
    params = {"api-version": API_VERSION, "$filter": filter_expr}
    items: list[PriceItem] = []

    url: str | None = PRICES_API_BASE
    while url:
        response = httpx.get(url, params=params if url == PRICES_API_BASE else None)
        response.raise_for_status()
        data = response.json()
        for item in data.get("Items", []):
            items.append(PriceItem(
                sku_name=item["skuName"],
                retail_price=item["retailPrice"],
                unit_of_measure=item["unitOfMeasure"],
                arm_region_name=item["armRegionName"],
                service_name=item["serviceName"],
            ))
        url = data.get("NextPageLink")

    return items


def estimate_monthly_cost(sku_name: str, region: str, hours_per_month: float = 730.0) -> float:
    """Estimate monthly VM cost in USD."""
    prices = get_vm_prices(sku_name, region)
    if not prices:
        raise ValueError(f"No prices found for {sku_name} in {region}")
    hourly = prices[0].retail_price
    return round(hourly * hours_per_month, 2)
```

---

## Cost Management Query API (authenticated)

Use the Query API to retrieve actual and amortised cost from your Azure subscriptions. Requires `Cost Management Reader` role or higher.

### Authentication: Managed Identity (preferred)

```python
from azure.identity import DefaultAzureCredential
import httpx

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default").token
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
```

### Query actual cost for a subscription: last 30 days, grouped by resource group

```python
import httpx, json

subscription_id = "your-subscription-id"
url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/query?api-version=2023-11-01"

payload = {
    "type": "ActualCost",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "Daily",
        "grouping": [
            {"type": "Dimension", "name": "ResourceGroupName"},
            {"type": "Dimension", "name": "ServiceName"}
        ],
        "aggregation": {
            "totalCost": {"name": "PreTaxCost", "function": "Sum"}
        }
    }
}

response = httpx.post(url, headers=headers, json=payload)
data = response.json()

# columns: [PreTaxCost, Currency, UsageDate, ResourceGroupName, ServiceName]
for row in data["properties"]["rows"]:
    print(f"RG: {row[3]:40s} | Service: {row[4]:30s} | Cost: ${row[0]:.2f}")
```

### Query amortised cost (for RI/Savings Plan chargeback)

```python
payload = {
    "type": "AmortizedCost",
    "timeframe": "LastMonth",
    "dataset": {
        "granularity": "Monthly",
        "grouping": [
            {"type": "Tag", "name": "cost-center"},
            {"type": "Dimension", "name": "ResourceGroupName"}
        ],
        "aggregation": {
            "totalCost": {"name": "PreTaxCost", "function": "Sum"}
        }
    }
}
```

---

## Cost Management Exports API

Use exports for large datasets, historical analysis, and integration with downstream tools (Power BI, Microsoft Fabric, custom ETL).

As of 2025, the improved exports experience supports the FOCUS (FinOps Open Cost and Usage Specification) format. Use FOCUS when integrating with FinOps Foundation-aligned tooling or when combining actual + amortised costs in a single dataset.

### Create a daily FOCUS export

```bash
PUT https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/exports/daily-focus-export?api-version=2025-03-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "properties": {
    "schedule": {
      "status": "Active",
      "recurrence": "Daily",
      "recurrencePeriod": {
        "from": "2025-06-01T00:00:00Z",
        "to": "2027-12-31T00:00:00Z"
      }
    },
    "deliveryInfo": {
      "destination": {
        "resourceId": "/subscriptions/{subscriptionId}/resourceGroups/finops-rg/providers/Microsoft.Storage/storageAccounts/finopsexports",
        "container": "cost-exports",
        "rootFolderPath": "focus/daily"
      }
    },
    "definition": {
      "type": "FocusCost",
      "timeframe": "MonthToDate",
      "dataSet": {
        "granularity": "Daily"
      }
    }
  }
}
```

### Trigger a one-time historical export (up to 7 years via API)

```bash
POST https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/exports/{exportName}/run?api-version=2025-03-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "timePeriod": {
    "from": "2024-01-01T00:00:00Z",
    "to": "2024-12-31T00:00:00Z"
  }
}
```

---

## Benefit Recommendations API (Savings Plans)

Use the Benefit Recommendations API to programmatically retrieve savings plan purchase recommendations. Recommendations are refreshed multiple times daily. Allow 7 days after any purchase before calling again.

```bash
# Get savings plan benefit recommendations -- 1-year term, 30-day lookback, shared scope
GET https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.CostManagement/benefitRecommendations?api-version=2023-11-01&$filter=properties/lookBackPeriod eq 'Last30Days' and properties/term eq 'P1Y' and properties/scope eq 'Shared'
Authorization: Bearer {token}
```

Response fields of interest:

| Field | Description |
|-------|-------------|
| `properties/recommendedQuantity` | Recommended hourly commitment in USD |
| `properties/totalSavings` | Estimated annual saving vs pay-as-you-go |
| `properties/coveragePercentage` | % of eligible compute covered by this commitment |
| `properties/term` | `P1Y` or `P3Y` |

### Reservation Recommendations API (Reserved Instances)

```bash
# Get RI recommendations -- subscription scope, 30-day lookback
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Consumption/reservationRecommendations?api-version=2023-05-01&$filter=properties/scope eq 'Single' and properties/lookBackPeriod eq 'Last30Days'
Authorization: Bearer {token}
```

---

## Carbon Optimization API

As of 2025, the Carbon Optimization service is GA. Include carbon metrics alongside cost when sustainability reporting is in scope. The API requires the `Carbon Optimization Reader` role.

```bash
# Query per-resource-group carbon emissions for April 2025
POST https://management.azure.com/providers/Microsoft.Carbon/carbonEmissionReports?api-version=2025-04-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "reportType": "ItemDetailsReport",
  "subscriptionList": ["{subscriptionId}"],
  "dateRange": {
    "start": "2025-04-01",
    "end": "2025-04-30"
  },
  "categoryType": "ResourceGroup"
}
```

Carbon data is updated monthly; previous month's data is available by day 19 of the current month. Schedule this API call monthly; daily polling returns stale data.

---

## CI/CD Cost Gate Pattern

Integrate the Retail Prices API into Terraform PR pipelines to surface cost estimates before deployment.

```yaml
# .github/workflows/cost-estimate.yml
name: Cost Estimate on PR

on:
  pull_request:
    paths:
      - "infra/**"

jobs:
  estimate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install httpx

      - name: Estimate infrastructure cost
        run: python infra/scripts/cost_estimate.py > cost_report.txt

      - name: Post cost report to PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('cost_report.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Cost Estimate\n\`\`\`\n${report}\n\`\`\``
            });
```

```python
# infra/scripts/cost_estimate.py
# Reads planned SKU changes from terraform plan output and prices them via Retail API

import subprocess, json, httpx, sys

PRICES_API = "https://prices.azure.com/api/retail/prices"

def get_price(sku: str, region: str) -> float:
    resp = httpx.get(PRICES_API, params={
        "api-version": "2023-01-01-preview",
        "$filter": f"armSkuName eq '{sku}' and armRegionName eq '{region}' and priceType eq 'Consumption' and contains(productName, 'Linux')"
    })
    items = resp.json().get("Items", [])
    return items[0]["retailPrice"] if items else 0.0

# Example: read planned resources from terraform show -json output
plan = json.loads(subprocess.check_output(["terraform", "show", "-json", "tfplan"]))
changes = plan.get("resource_changes", [])

total_monthly = 0.0
for change in changes:
    if change.get("type") == "azurerm_linux_virtual_machine" and "create" in change.get("change", {}).get("actions", []):
        sku  = change["change"]["after"].get("size", "Standard_D2s_v5")
        region = change["change"]["after"].get("location", "eastus").replace(" ", "").lower()
        hourly = get_price(sku, region)
        monthly = round(hourly * 730, 2)
        total_monthly += monthly
        print(f"  {change['address']:60s} {sku:20s}  ${monthly:>10.2f}/mo")

print(f"\nEstimated total new monthly spend: ${total_monthly:.2f}")
if total_monthly > 5000:
    print("WARNING: estimated monthly cost exceeds $5,000. Requires VP approval.")
    sys.exit(1)
```

---

## Required RBAC Roles

| API | Required Role |
|-----|--------------|
| Retail Prices API | None (public, unauthenticated) |
| Cost Management Query API | Cost Management Reader (minimum) |
| Cost Management Exports API (create/manage) | Cost Management Contributor |
| Benefit Recommendations API | Billing Reader on Billing Account |
| Reservation Recommendations (Consumption) | Reader on subscription |
| Carbon Optimization API | Carbon Optimization Reader |

Always use Managed Identity (`DefaultAzureCredential`) for service-to-service calls. Never embed client secrets in code or environment variables.
