# Supply Chain Security & SBOM

## Why Supply Chain Matters

Supply chain attacks (SolarWinds, Log4Shell, XZ Utils) compromise software not by attacking your code but by attacking your dependencies, build tools, or distribution pipeline. The controls below implement SLSA (Supply-chain Levels for Software Artifacts) and produce artefacts that let you answer: "What is in this build? Where did it come from? Has it been tampered with?"

## SBOM Generation: syft + CycloneDX

Generate a Software Bill of Materials in every CI pipeline run for every deployable artefact (container image, NuGet package, ZIP deployment).

**Tool**: `syft` (Anchore). Supports CycloneDX JSON and SPDX formats.

```yaml
# .github/workflows/build.yml: SBOM generation step
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    image: ${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }}
    format: cyclonedx-json
    output-file: sbom.cyclonedx.json
    upload-artifact: true

# Or via CLI for non-image artefacts (e.g. .NET publish output)
- name: Generate SBOM for .NET artefact
  run: |
    syft dir:./publish \
      --output cyclonedx-json=sbom.cyclonedx.json \
      --file sbom.cyclonedx.json
```

Attach the SBOM as a build artefact and retain it for the same period as the deployment artefact. For container images, attach the SBOM to the OCI image index using `cosign attach sbom`.

**Format**: CycloneDX JSON (preferred: richer component metadata, schema-validated, wide tool support). SPDX acceptable for compliance contexts requiring NTIA minimum element alignment.

## Dependency Review: Dependabot + Renovate

**Dependabot** (GitHub native): Automates dependency version updates as PRs; scans for known CVEs in the dependency graph.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "nuget"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    groups:
      microsoft:
        patterns: ["Microsoft.*", "Azure.*"]

  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

Enable the GitHub dependency review action to block PRs that introduce new High/Critical CVEs:

```yaml
# .github/workflows/dependency-review.yml
- name: Dependency Review
  uses: actions/dependency-review-action@v4
  with:
    fail-on-severity: high
    allow-licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
```

**Renovate** (alternative): More configurable than Dependabot; preferred for monorepos or when fine-grained automerge rules are needed (e.g., automerge patch bumps for well-tested packages, require review for major bumps).

## Signed Commits: Sigstore / GPG

Require signed commits on all default and release branches. This provides non-repudiation for who authored each change.

```bash
# Developer setup: Sigstore gitsign (keyless, certificate-based)
brew install sigstore/tap/gitsign

git config --global gpg.x509.program gitsign
git config --global gpg.format x509
git config --global commit.gpgsign true
```

Enforce via branch protection:

```yaml
# GitHub branch protection rule (via API / Terraform)
resource "github_branch_protection" "main" {
  repository_id = github_repository.repo.node_id
  pattern       = "main"

  required_status_checks {
    strict   = true
    contexts = ["ci / build", "dependency-review"]
  }

  required_pull_request_reviews {
    required_approving_review_count = 1
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = true
  }

  require_signed_commits = true
  enforce_admins         = true
}
```

**Branch protection baseline** (non-negotiable for all repos):
- Require PR with at least 1 approving review
- Dismiss stale reviews on new push
- Require status checks to pass (build, dependency review, secret scan)
- Require signed commits
- Restrict force pushes and branch deletion

## Provenance Attestation: SLSA

SLSA (Supply-chain Levels for Software Artifacts) defines four levels. Target SLSA Level 2 for all production workloads; Level 3 for security-critical components.

| Level | Requirement | Implementation |
|---|---|---|
| L1 | SBOM present, build scripted | syft SBOM in CI ✓ |
| L2 | Build on hosted CI, signed provenance | GitHub Actions + `slsa-github-generator` |
| L3 | Hardened build environment, non-falsifiable provenance | GitHub Actions with isolated runners + Sigstore Rekor transparency log |

**SLSA L2 provenance** via GitHub Actions:

```yaml
# .github/workflows/release.yml
jobs:
  provenance:
    needs: [build]
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v2
    with:
      base64-subjects: ${{ needs.build.outputs.digests }}
    permissions:
      id-token: write
      contents: write
      attestations: write
```

Store provenance attestations alongside artefacts in GitHub Releases or OCI registry (via `cosign attest`).

## Container Image Signing: cosign

Sign every container image pushed to a registry:

```bash
# Sign with keyless (OIDC-based, Sigstore Rekor transparency log)
cosign sign --yes $REGISTRY/$IMAGE@$DIGEST

# Verify in CD pipeline before deployment
cosign verify \
  --certificate-identity "https://github.com/<org>/<repo>/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  $REGISTRY/$IMAGE@$DIGEST
```

Configure Azure Container Registry (ACR) content trust or Azure Policy to deny unsigned images in production AKS clusters.

## Supply Chain Artefacts Checklist (per repo)

- [ ] `dependabot.yml` or `renovate.json` at repo root
- [ ] Dependency review GitHub Action (blocks High/Critical CVEs on PR)
- [ ] SBOM generated in CI (syft, CycloneDX JSON format)
- [ ] SBOM attached to build artefact and retained
- [ ] Signed commits required (branch protection `require_signed_commits: true`)
- [ ] Branch protection enforced on `main` and all release branches
- [ ] Container images signed with cosign (if applicable)
- [ ] SLSA L2 provenance generated for release builds
