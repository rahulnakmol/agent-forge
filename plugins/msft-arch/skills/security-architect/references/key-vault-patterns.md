# Key Vault Patterns

## Core Opinions

- **RBAC over access policies**. Always. Legacy access policies are still supported but should not appear in new deployments. Migrate existing vaults to RBAC permission model: `az keyvault update --name <vault> --enable-rbac-authorization true`.
- **One vault per environment boundary**. Dev, staging, and production vaults are separate resources with separate access grants. Never share a vault across environment boundaries.
- **Reference syntax everywhere**. App Service, Functions, Container Apps, and AKS workloads must access secrets via Key Vault references. Never use inline values in application settings, pipeline variables, or container environment variables.
- **Soft-delete + purge protection ON for every vault**. Soft-delete is now enabled by default and cannot be disabled. Purge protection is one-way: once enabled, it cannot be turned off. Enable it on all production vaults. For dev vaults, evaluate whether you need the ability to re-create the vault with the same name during infrastructure tear-down cycles; if yes, delay purge protection until the vault reaches a stable state.

## RBAC Role Assignments

| Role | Assign to | Scope |
|---|---|---|
| `Key Vault Secrets User` | App Managed Identity, Functions Managed Identity, Container Apps Managed Identity | Individual vault (not subscription) |
| `Key Vault Certificates User` | App identity needing TLS cert reads | Individual vault |
| `Key Vault Crypto User` | App identity performing encryption/decryption | Individual vault |
| `Key Vault Secrets Officer` | CI/CD service principal (for secret rotation workflows) | Individual vault |
| `Key Vault Certificates Officer` | CI/CD service principal (for cert renewal automation) | Individual vault |
| `Key Vault Administrator` | Break-glass / PIM-eligible admin group only | Individual vault |

Never assign `Key Vault Administrator` to application identities. Never assign `Owner` or `Contributor` to application identities on the vault resource.

## Reference Syntax by Host

### App Service / Azure Functions

```bash
# Bicep: application setting using Key Vault reference
resource appService 'Microsoft.Web/sites@2023-12-01' = {
  properties: {
    siteConfig: {
      appSettings: [
        {
          name: 'DatabaseConnectionString'
          value: '@Microsoft.KeyVault(SecretUri=https://${keyVault.name}.vault.azure.net/secrets/db-connection-string/)'
        }
      ]
    }
  }
}
```

The app's system-assigned Managed Identity must have `Key Vault Secrets User` on the vault before the reference resolves. If the reference fails to resolve, App Service surfaces a `Key Vault reference is invalid` error in the portal.

### Container Apps

```yaml
# container-apps.yaml: secret reference
secrets:
  - name: db-connection-string
    keyVaultUrl: https://<vault>.vault.azure.net/secrets/db-connection-string/
    identity: system-assigned   # or user-assigned managed identity resource ID

containers:
  - name: api
    env:
      - name: DATABASE_CONNECTION_STRING
        secretRef: db-connection-string
```

### AKS: Azure Key Vault Provider for Secrets Store CSI Driver

```yaml
# SecretProviderClass
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: app-secrets
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    clientID: "<workload-identity-client-id>"
    keyvaultName: "<vault-name>"
    tenantId: "<tenant-id>"
    objects: |
      array:
        - |
          objectName: db-connection-string
          objectType: secret
  secretObjects:
    - secretName: app-secrets-k8s
      type: Opaque
      data:
        - objectName: db-connection-string
          key: DATABASE_CONNECTION_STRING
```

Use Workload Identity (not pod identity v1) for AKS secret access. Reference `identity-architect` for Workload Identity Federation setup.

## Soft-Delete and Purge Protection Trade-offs

| Setting | Behaviour | Recommendation |
|---|---|---|
| Soft-delete (default ON) | Deleted vault/secret recoverable for 7–90 days (default 90) | Leave at default 90 days for production |
| Purge protection OFF | Soft-deleted items can be manually purged (permanently deleted) before retention expires | Default for dev vaults where you need full reset capability |
| Purge protection ON | Nothing can be permanently deleted until retention period expires (including by Microsoft) | Mandatory for production; enables only once, cannot be undone |

**Recovery retention period** cannot be changed after vault creation. Choose 30 days for dev (faster recycling), 90 days for production (maximum recovery window).

## Managed HSM: When Justified

Standard Key Vault uses software-protected keys by default and offers HSM-protected keys (Premium tier) backed by shared HSM hardware. Managed HSM provides a dedicated FIPS 140-2 Level 3 HSM cluster.

**Use Managed HSM when**:
- Regulatory requirement explicitly mandates dedicated HSM (PCI-DSS HSM requirement, FedRAMP High, government contracts)
- Customer-Managed Key (CMK) for Azure SQL TDE, Storage Service Encryption, or Azure Disk Encryption requires HSM-backed key material
- Certificate issuance must happen inside an HSM boundary (e.g., code signing for publicly distributed software)

**Do not use Managed HSM** for application secret storage. Standard Key Vault with RBAC is the correct pattern. Managed HSM costs ~$1.60/hour/partition (always-on billing, even when idle) and requires multi-person security domain custody.

## Certificate Lifecycle

Store TLS certificates as Key Vault `certificate` objects, not raw secrets. Configure auto-renewal via Key Vault's integrated CA:

- **DigiCert / GlobalSign**: Managed partnership; auto-issues and renews on expiry approach.
- **Let's Encrypt**: Use `keyvault-acmebot` (open source) for ACME protocol integration with Key Vault.
- **Self-signed**: Development only. Never in staging or production.

Enable certificate expiry alerts in Defender for Key Vault and Azure Monitor. Target alert at 60 days before expiry for time to investigate CA issues; hard alert at 30 days.
