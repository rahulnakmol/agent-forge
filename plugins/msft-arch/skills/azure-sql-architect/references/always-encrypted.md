# Always Encrypted

**Applies to**: Azure SQL Database, Azure SQL Managed Instance, SQL Server 2019+ (some features).

> Codified opinion: Always Encrypted (deterministic) for searchable PII. Randomized for non-searchable.

Always Encrypted protects sensitive data from anyone with access to the server (DBAs, cloud admins, infrastructure operators) by encrypting client-side and never letting plaintext or column encryption keys reach the database engine. The classic mode supports equality comparison only on deterministic columns; secure enclaves extend support to richer queries.

## Encryption type per column

Classify every sensitive column into one of three buckets.

| Need | Encryption type | Trade-offs |
|---|---|---|
| Lookup PII by exact value (email, SSN, last name in equality search) | Deterministic | Same plaintext maps to same ciphertext. Vulnerable to inference if the value distribution is predictable (e.g., gender, status). Acceptable for high-cardinality fields. |
| Sensitive values that are never searched directly (notes, free-text PHI, document blobs) | Randomized | Different ciphertext for the same plaintext. Strongest protection. No equality, no range, no pattern matching outside enclaves. |
| Range queries, LIKE, or aggregates on sensitive columns | Always Encrypted with secure enclaves | Requires the database to be configured for enclaves. Two enclave technologies on Azure SQL DB: VBS enclaves (default, software-based, available in nearly all regions and SKUs) and Intel SGX enclaves (DC-series hardware only, with Microsoft Azure Attestation). |

Verify enclave availability and current attestation requirements with `microsoft_docs_search` before promising enclave support: regional availability and SKU constraints change.

## VBS vs SGX enclaves on Azure SQL Database

- VBS enclaves: software-based, ride on Windows Hypervisor, available across standard SKUs and most regions. Sufficient when the threat model is unauthorised access from highly-privileged users (DBAs, cloud ops). VBS enclaves on Azure SQL DB do not support attestation.
- Intel SGX enclaves: hardware-based trusted execution, require DC-series hardware, support Microsoft Azure Attestation. Use when the threat model includes OS-level admin attacks or when attestation is a regulatory requirement.

DC-series caveats to surface in the ADR: physical cores (not logical), max 40 cores, no serverless, regional availability is narrower than standard-series.

## CMK and CEK hierarchy

Always Encrypted uses two key types:

- Column Master Key (CMK): asymmetric key stored in a key store outside the database. On Azure, this is Azure Key Vault. The DB only knows the CMK metadata (provider + path).
- Column Encryption Key (CEK): symmetric key stored in the database, encrypted by the CMK. The CEK encrypts column data.

Rules:

- CMK lives in Key Vault. Never in app config, never in source. Rotate on a documented schedule.
- App identity that decrypts must have `wrapKey` and `unwrapKey` permissions on the CMK; SQL itself does not need them, only the client.
- Use Managed Identity for the app's access to Key Vault (`/identity-architect`).
- Two CMKs registered at any time during rotation: this enables zero-downtime CMK rotation by re-encrypting CEKs under the new CMK while the old one is still valid.

## CMK rotation workflow

1. Create the new CMK version in Key Vault.
2. Register the new CMK in the database (`CREATE COLUMN MASTER KEY`).
3. Use the AlwaysEncrypted PowerShell or .NET tooling to re-encrypt every CEK under the new CMK.
4. Verify all clients use a driver version that knows the new CMK metadata.
5. After a soak period: remove the old CMK registration; mark the old CMK key version as disabled in Key Vault but do not delete it for the data retention period (you may need it to decrypt restored backups).

Document each rotation step in the ADR. Schedule rotations: the cadence depends on regulatory regime (annual is the floor for most regimes; quarterly for high-sensitivity workloads).

## Operational guardrails

- Schema changes on encrypted columns require client-side tooling that holds the CMK. Plan deployments accordingly: schema migrations cannot run from a pipeline that does not have CMK access.
- Drivers: use the most recent SqlClient and EF Core packages. Older drivers do not understand newer enclave attestation protocols.
- Test the recovery path: restore a backup to a non-prod server, verify a test client with the right CMK access can decrypt. A backup you cannot decrypt is not a backup.
- For migration planning: existing plaintext columns can be encrypted in place using enclaves (with secure enclaves enabled) without exporting data outside the database. Without enclaves, the data must be moved client-side, encrypted, and reinserted.

## Don'ts

- Do not use deterministic encryption on low-cardinality columns (boolean flags, status enums, gender). Inference attacks are trivial.
- Do not encrypt foreign key columns with randomized encryption. Joins and equality lookups on the FK will fail. Use deterministic with the high-cardinality understanding above.
- Do not store the CMK in an HSM you cannot access from the app's runtime identity. The app needs unwrapKey on every read.
- Do not skip the test restore path. CMK loss is data loss.
