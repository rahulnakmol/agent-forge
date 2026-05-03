# ADR 0005: DCO Over CLA

**Status:** Accepted (2026-05-03)
**Spec section:** D5

## Context

Open-source projects need IP provenance from contributors — a record that contributors
have the right to contribute the code they're submitting and that they agree to the
project's license. Two common mechanisms exist: a Contributor License Agreement (CLA),
which is a legal agreement signed separately, and the Developer Certificate of Origin
(DCO), which is a per-commit attestation embedded in the commit message via `git commit -s`.
For a community marketplace project, the right tradeoff between legal protection and
contributor friction is not obvious.

## Decision

Require DCO (Developer Certificate of Origin) sign-off via `git commit -s` instead of
a CLA agreement. Every commit merged to `main` must have a `Signed-off-by` line. CI
(via the DCO GitHub Action) verifies this automatically. The DCO text is:

> By making a contribution to this project, I certify that:
> (a) The contribution was created in whole or in part by me and I have the right to
> submit it under the open source license indicated in the file; or
> (b) The contribution is based upon previous work that, to the best of my knowledge,
> is covered under an appropriate open source license and I have the right to submit
> that work with modifications, whether created in whole or in part by me, under the
> same open source license; or
> (c) The contribution was provided directly to me by some other person who certified
> (a), (b) or (c) and I have not modified it.
> (d) I understand and agree that this project and the contribution are public and that
> a record of the contribution (including all personal information I submit with it,
> including my sign-off) is maintained indefinitely and may be redistributed consistent
> with this project or the open source license(s) involved.

## Consequences

**Positive:**
- Zero friction for contributors: `git commit -s` adds the sign-off automatically
- No legal agreement or GitHub bot authorization required
- Industry standard: used by the Linux kernel, Docker, and hundreds of major projects
- DCO is verifiable from the git log alone, without a separate database

**Negative:**
- DCO is weaker than a full CLA in certain jurisdictions — a CLA provides stronger
  protections for relicensing and patent grants
- No centralized record of agreements: if a contributor later disputes their sign-off,
  there is no separate agreement to reference
- Typos in the `Signed-off-by` line require a `git commit --amend` to fix before merge

## Alternatives considered

- **CLA with GitHub bot (e.g., CLA Assistant)** — rejected because it requires
  contributors to navigate an external agreement flow, which discourages small
  contributions (one-line typo fixes, rubric improvements) that are common in a
  content marketplace
- **No IP tracking** — rejected because it creates legal risk if the project is ever
  used commercially or if a contributor's employer claims ownership of submitted content
