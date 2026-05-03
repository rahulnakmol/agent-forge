# Secret Scanning

## The Problem

Inline secrets committed to source control are the single most common root cause of cloud data breaches. They survive long after rotation because git history preserves them. The controls below form a layered defence: prevent → detect in PR → detect post-merge → detect in running pipelines → rotate after breach.

## GitHub Secret Scanning + Push Protection

**Secret scanning** scans all commits, issues, PR descriptions, wikis, and discussions for known secret patterns (220+ supported types including Azure SAS tokens, storage keys, Entra app secrets, AWS keys, Stripe, Twilio, etc.).

Enable at the organisation level (covers all repos automatically):

```bash
gh api \
  --method PATCH \
  /orgs/{org} \
  -f secret_scanning="enabled" \
  -f secret_scanning_push_protection="enabled"
```

**Push protection** blocks the push at the client before it reaches GitHub if a secret is detected. This is the highest-leverage control: it stops the credential before it enters git history at all. Users can bypass with a reason code (false-positive, used-in-test, will-fix-later); every bypass is logged and visible to security teams.

Alert on bypasses using GitHub webhook → Azure Event Grid → alert workflow. Treat a push protection bypass as a security incident requiring follow-up within 24 hours.

**Custom patterns**: Extend scanning to cover organisation-specific tokens (internal API keys, HMAC signing secrets):

```yaml
# .github/secret_scanning.yml
custom_patterns:
  - name: "Internal API Key"
    regex: "INTERNAL_[A-Z0-9]{32}"
    secret_group: 1
```

## Azure DevOps: Credential Scanner (CredScan)

Microsoft Security DevOps (MSDO) extension for Azure Pipelines includes CredScan, which scans source tree and pipeline outputs for credential patterns.

```yaml
# azure-pipelines.yml: MSDO security scan step
- task: MicrosoftSecurityDevOps@1
  inputs:
    categories: 'secrets'
    break: true   # fail pipeline on detected secrets
```

Enable "Advanced Security" on the Azure DevOps organisation to get CredScan running on all PRs with inline PR annotations. Advanced Security also includes dependency scanning and code scanning (CodeQL).

## gitleaks: Fallback / Local Developer Scanning

Use `gitleaks` as a pre-commit hook for local developer workstations and as a pipeline safety net for repos not covered by GitHub Advanced Security or ADO Advanced Security:

```bash
# Install gitleaks
brew install gitleaks   # macOS
# or via aqua / mise

# Scan full repo history
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# Pre-commit hook (add to .pre-commit-config.yaml)
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.x.x
    hooks:
      - id: gitleaks
```

Maintain a `.gitleaks.toml` at repo root to suppress false positives (test fixtures, example values):

```toml
[allowlist]
  paths = ["tests/fixtures/", "docs/examples/"]
  regexes = ["EXAMPLE_TOKEN_.*"]
```

## Post-Leak Rotation Playbook

If a secret is discovered in git history (past or present), treat it as compromised immediately. Do not assume "nobody found it yet".

1. **Rotate immediately**: Invalidate the secret at the issuing service before any other step. For Azure: regenerate the storage account key, expire the Entra app secret, revoke the SAS token.
2. **Audit access logs**: Check the relevant service's audit log (Azure Monitor / Entra sign-in logs / Key Vault audit logs) for access events since the commit timestamp of the exposure. Look for unfamiliar IPs, unusual access times, or access patterns that differ from normal app behaviour.
3. **Revoke all active sessions** associated with the compromised credential.
4. **Remove from git history**: Use `git filter-repo` (not `git filter-branch`) to rewrite history. Force-push all branches. Invalidate GitHub's cache: contact GitHub support with the repo name and commit SHA if the secret appears in GitHub's search index.
5. **Update Key Vault reference**: Ensure the replacement value lands in Key Vault and the app picks up the new reference (App Service restart, Container App revision update).
6. **Post-incident review**: Document root cause, contributing factors, and control gaps. Add the secret pattern as a custom gitleaks rule if it wasn't detected automatically.

## Scanning Coverage Checklist

- [ ] GitHub secret scanning enabled at org level
- [ ] Push protection enabled at org level
- [ ] Bypass alert workflow configured
- [ ] Custom patterns defined for internal tokens
- [ ] MSDO CredScan in every Azure DevOps pipeline (if ADO used)
- [ ] gitleaks pre-commit hook in repo template
- [ ] gitleaks CI step for repos without GHAS / ADO Advanced Security
- [ ] Post-leak playbook linked in security runbook
