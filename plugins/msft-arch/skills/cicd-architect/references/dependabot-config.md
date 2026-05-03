# Dependabot Configuration

Dependabot version updates must be configured on every repository. Ungrouped Dependabot generates one PR per dependency update; teams learn to ignore them within weeks. Grouping by package ecosystem batches updates into one PR per ecosystem per sprint. Auto-merge is enabled for minor and patch updates when all required status checks pass.

---

## Core Opinions

- Dependabot groups by package ecosystem. One PR per ecosystem update, not one PR per package.
- Auto-merge applies to minor and patch semver bumps with green CI. Major version bumps require human review; breaking changes are common.
- Security updates (Dependabot alerts) bypass the schedule and open PRs immediately regardless of grouping; do not block these.
- The `commit-message` prefix must match Conventional Commits `chore(deps)` so that commitlint does not block Dependabot PRs.
- Update frequency: weekly for most ecosystems (daily would saturate the PR queue). Security alerts are always immediate.

---

## `.github/dependabot.yml`: Full Configuration

```yaml
# .github/dependabot.yml
version: 2

updates:
  # ─────────────────────────────────────────────
  # NuGet (.NET)
  # ─────────────────────────────────────────────
  - package-ecosystem: nuget
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: '09:00'
      timezone: 'Australia/Melbourne'
    groups:
      nuget-minor-patch:
        applies-to: version-updates
        update-types:
          - minor
          - patch
    open-pull-requests-limit: 5
    labels:
      - dependencies
      - nuget
    commit-message:
      prefix: 'chore'
      prefix-development: 'chore'
      include: scope        # Produces: chore(deps): bump <package> from x to y
    reviewers:
      - my-org/platform-team
    ignore:
      # Pin major version upgrades to a dedicated upgrade PR authored manually
      - dependency-name: '*'
        update-types: ['version-update:semver-major']

  # ─────────────────────────────────────────────
  # npm / Node.js
  # ─────────────────────────────────────────────
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: '09:00'
      timezone: 'Australia/Melbourne'
    groups:
      npm-minor-patch:
        applies-to: version-updates
        update-types:
          - minor
          - patch
      npm-dev-dependencies:
        applies-to: version-updates
        dependency-type: development
        patterns:
          - '*'
    open-pull-requests-limit: 5
    labels:
      - dependencies
      - npm
    commit-message:
      prefix: 'chore'
      include: scope
    reviewers:
      - my-org/platform-team
    ignore:
      - dependency-name: '*'
        update-types: ['version-update:semver-major']

  # ─────────────────────────────────────────────
  # pip / Python
  # ─────────────────────────────────────────────
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
      day: tuesday
      time: '09:00'
      timezone: 'Australia/Melbourne'
    groups:
      pip-minor-patch:
        applies-to: version-updates
        update-types:
          - minor
          - patch
    open-pull-requests-limit: 3
    labels:
      - dependencies
      - python
    commit-message:
      prefix: 'chore'
      include: scope
    ignore:
      - dependency-name: '*'
        update-types: ['version-update:semver-major']

  # ─────────────────────────────────────────────
  # Docker (Dockerfile base images)
  # ─────────────────────────────────────────────
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly
      day: wednesday
      time: '09:00'
      timezone: 'Australia/Melbourne'
    groups:
      docker-base-images:
        applies-to: version-updates
        patterns:
          - '*'
    labels:
      - dependencies
      - docker
    commit-message:
      prefix: 'chore'
      include: scope

  # ─────────────────────────────────────────────
  # GitHub Actions
  # ─────────────────────────────────────────────
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
      day: wednesday
      time: '09:00'
      timezone: 'Australia/Melbourne'
    groups:
      github-actions-minor-patch:
        applies-to: version-updates
        update-types:
          - minor
          - patch
    labels:
      - dependencies
      - github-actions
    commit-message:
      prefix: 'chore'
      include: scope

  # ─────────────────────────────────────────────
  # Terraform providers (if applicable)
  # ─────────────────────────────────────────────
  - package-ecosystem: terraform
    directory: /infrastructure
    schedule:
      interval: weekly
      day: thursday
      time: '09:00'
      timezone: 'Australia/Melbourne'
    groups:
      terraform-providers:
        applies-to: version-updates
        update-types:
          - minor
          - patch
    labels:
      - dependencies
      - terraform
    commit-message:
      prefix: 'chore'
      include: scope
    ignore:
      # AzureRM major bumps (3.x → 4.x) require explicit validation
      - dependency-name: 'hashicorp/azurerm'
        update-types: ['version-update:semver-major']
```

---

## Auto-Merge Workflow

The auto-merge workflow runs when Dependabot opens a PR. It merges the PR automatically if and only if:

1. The update is a minor or patch semver bump (not major).
2. All required status checks pass (build, test, commitlint).
3. The PR was opened by the `dependabot[bot]` actor.

```yaml
# .github/workflows/dependabot-auto-merge.yml
name: Dependabot Auto-Merge

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    name: Auto-Merge Dependabot PRs
    runs-on: ubuntu-24.04
    if: github.actor == 'dependabot[bot]'

    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Enable auto-merge for minor and patch updates
        if: |
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "${{ github.event.pull_request.html_url }}"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Label major version updates for manual review
        if: steps.metadata.outputs.update-type == 'version-update:semver-major'
        run: |
          gh pr edit "${{ github.event.pull_request.html_url }}" \
            --add-label "major-version-bump"
          gh pr comment "${{ github.event.pull_request.html_url }}" \
            --body "Major version update; requires manual review for breaking changes. Do not auto-merge."
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Auto-merge requires branch protection to be configured**; without required status checks, auto-merge would merge without CI passing. Configure the following branch protection rules on `main`:

- Require status checks to pass before merging
- Required checks: `build`, `test`, `commitlint` (all jobs that validate the PR)
- Require branches to be up to date before merging
- Allow auto-merge: enable in repository settings

---

## Security Updates vs Version Updates

Dependabot runs two separate processes:

| Mode | Trigger | Schedule | PR urgency |
|---|---|---|---|
| **Security updates** | New CVE in advisory database | Immediate | High; merge ASAP |
| **Version updates** | New package version published | Per schedule above | Normal sprint cadence |

Security update PRs bypass grouping; they open one PR per vulnerable dependency immediately. Do not block these PRs in branch protection rules based on staleness. Treat security PRs as hotfixes and merge them within 48 hours.

---

## Azure DevOps (Dependabot via GitHub Advanced Security)

Azure DevOps does not natively run Dependabot version updates, but GitHub Advanced Security for Azure DevOps (GHAzDO) brings Dependabot security alerts to ADO repositories. As of 2025, GHAzDO can automatically create PRs for security vulnerabilities in ADO repos.

For version updates in Azure DevOps, use one of these alternatives:

- **Dependabot ADO extension** (community-maintained): reads `dependabot.yml` and opens ADO PRs
- **Renovate Bot** (self-hosted or app): supports ADO natively with equivalent grouping and auto-merge configuration
- **GitHub mirroring**: mirror the ADO repo to GitHub to get native Dependabot; push auto-merged changes back

For new enterprise repos, Renovate Bot is recommended when the source of truth is Azure Repos. Configure `renovate.json` at the repo root.

---

## Renovate Bot Alternative Configuration

If using Renovate instead of Dependabot (common for Azure DevOps organisations):

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "commitMessagePrefix": "chore(deps):",
  "schedule": ["before 10am on Monday"],
  "timezone": "Australia/Melbourne",
  "groupName": "all minor and patch dependencies",
  "groupSlug": "all-minor-patch",
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["major-version-bump"],
      "reviewers": ["team:platform-team"]
    },
    {
      "matchPackagePatterns": ["^@commitlint/", "^eslint", "^prettier"],
      "groupName": "linting and formatting tools",
      "groupSlug": "linting"
    }
  ],
  "prConcurrentLimit": 5,
  "prHourlyLimit": 2
}
```
