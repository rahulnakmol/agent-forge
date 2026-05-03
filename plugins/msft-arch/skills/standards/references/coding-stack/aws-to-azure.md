---
category: coding-stack
loading_priority: 2
tokens_estimate: 2800
keywords:
  - AWS
  - Azure
  - cloud migration
  - service mapping
  - conversion guide
  - compute
  - storage
  - database
  - networking
  - security
  - AI/ML
  - DevOps
version: "1.0"
last_updated: "2026-03-21"
---

# AWS-to-Azure Service Mapping and Conversion Guide

## Overview

The skill can convert any AWS-specific design to Azure-native design. This reference provides comprehensive service mapping for every major cloud service category.

---

## Compute

| AWS | Azure | Notes |
|-----|-------|-------|
| EC2 | Virtual Machines | Prefer PaaS (App Service) when possible |
| Lambda | Azure Functions | Consumption, Premium, or Dedicated plans |
| ECS/Fargate | Container Apps | Simpler container hosting |
| EKS | AKS | Kubernetes managed service |
| Elastic Beanstalk | App Service | PaaS web hosting |
| Step Functions | Durable Functions / Logic Apps | Workflow orchestration |
| Batch | Azure Batch | HPC workloads |

---

## Storage

| AWS | Azure | Notes |
|-----|-------|-------|
| S3 | Blob Storage | Object storage, tiers: Hot/Cool/Archive |
| EBS | Managed Disks | Block storage for VMs |
| EFS | Azure Files | Shared file storage, SMB/NFS |
| Glacier | Archive Storage | Long-term archival |

---

## Database

| AWS | Azure | Notes |
|-----|-------|-------|
| RDS (PostgreSQL) | Azure Database for PostgreSQL | Flexible Server preferred |
| RDS (MySQL) | Azure Database for MySQL | Flexible Server |
| RDS (SQL Server) | Azure SQL Database | Prefer PaaS, elastic pools |
| DynamoDB | Cosmos DB | Multi-model, global distribution |
| Aurora | Azure SQL Hyperscale | High-scale relational |
| Redshift | Synapse Analytics | Data warehouse |
| ElastiCache (Redis) | Azure Cache for Redis | Managed Redis |
| DocumentDB | Cosmos DB (MongoDB API) | MongoDB-compatible |

---

## Networking

| AWS | Azure | Notes |
|-----|-------|-------|
| VPC | Virtual Network | CIDR planning, NSGs |
| ALB/NLB | Load Balancer / App Gateway | L4/L7 load balancing |
| CloudFront | Azure CDN / Front Door | Global CDN, WAF |
| Route 53 | Azure DNS / Traffic Manager | DNS, traffic routing |
| API Gateway | API Management | Full API lifecycle |
| Direct Connect | ExpressRoute | Dedicated connectivity |
| Transit Gateway | Virtual WAN | Hub-spoke networking |

---

## Messaging and Integration

| AWS | Azure | Notes |
|-----|-------|-------|
| SQS | Storage Queue / Service Bus Queue | Simple vs enterprise messaging |
| SNS | Event Grid / Service Bus Topics | Pub/sub |
| EventBridge | Event Grid | Event routing |
| Kinesis | Event Hubs | Streaming |
| MQ | Service Bus | Enterprise messaging |

---

## Security and Identity

| AWS | Azure | Notes |
|-----|-------|-------|
| IAM | Entra ID + RBAC | Identity + authorization |
| Cognito | Azure AD B2C / Entra External ID | Customer identity |
| KMS | Key Vault | Key management, secrets |
| WAF | Azure WAF (with Front Door/AppGW) | Web application firewall |
| GuardDuty | Microsoft Defender for Cloud | Threat detection |
| CloudTrail | Azure Monitor / Activity Log | Audit logging |
| Secrets Manager | Key Vault (Secrets) | Secret storage |

---

## AI/ML

| AWS | Azure | Notes |
|-----|-------|-------|
| Bedrock | Azure OpenAI Service | Foundation model access |
| SageMaker | Azure Machine Learning | ML platform |
| Comprehend | Azure AI Language | NLP |
| Rekognition | Azure AI Vision | Computer vision |
| Lex | Copilot Studio / Bot Service | Conversational AI |

---

## DevOps and Monitoring

| AWS | Azure | Notes |
|-----|-------|-------|
| CloudFormation | Terraform / Bicep / ARM | IaC (prefer Terraform) |
| CodePipeline | Azure DevOps / GitHub Actions | CI/CD |
| CloudWatch | Azure Monitor + Log Analytics | Monitoring, logging |
| X-Ray | Application Insights | Distributed tracing |
| CodeBuild | Azure DevOps Pipelines | Build service |

---

## Data and Analytics

| AWS | Azure | Notes |
|-----|-------|-------|
| Glue | Azure Data Factory | ETL/ELT |
| Athena | Synapse Serverless SQL | Query data lake |
| Lake Formation | Azure Purview / Unity Catalog | Data governance |
| EMR | HDInsight / Databricks | Big data processing |
| QuickSight | Power BI | Business intelligence |

---

## Conversion Checklist

When converting AWS to Azure:

1. Map every AWS service to Azure equivalent using tables above
2. Identify Azure-native advantages (Entra ID integration, Power Platform connectors)
3. Replace CloudFormation with Terraform (portable across clouds)
4. Map IAM roles/policies to Entra ID RBAC
5. Convert VPC design to VNet with NSGs/ASGs
6. Map container orchestration (EKS to AKS, Fargate to Container Apps)
7. Update CI/CD pipelines (GitHub Actions works for both, or migrate to Azure DevOps)
8. Adapt monitoring (CloudWatch to Azure Monitor + Application Insights)
9. Generate ADRs for each major conversion decision
10. Validate cost comparison using Azure Pricing Calculator

---

## Architecture Pattern Conversions

| AWS Pattern | Azure Equivalent |
|-------------|-----------------|
| AWS Well-Architected | Azure Well-Architected (direct pillar mapping) |
| AWS Landing Zone | Azure Landing Zone (CAF) |
| AWS Organizations | Azure Management Groups |
| AWS Service Control Policies | Azure Policy |
| AWS Control Tower | Azure Landing Zone Accelerator |
