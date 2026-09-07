# viavitae-clients

[![CI](https://github.com/Via-Vitae/viavitae-clients/actions/workflows/ci.yml/badge.svg)](https://github.com/Via-Vitae/viavitae-clients/actions/workflows/ci.yml)
[![Compliance](https://github.com/Via-Vitae/viavitae-clients/actions/workflows/compliance-check.yml/badge.svg)](https://github.com/Via-Vitae/viavitae-clients/actions/workflows/compliance-check.yml)
[![CodeQL](https://github.com/Via-Vitae/viavitae-clients/actions/workflows/codeql.yml/badge.svg)](https://github.com/Via-Vitae/viavitae-clients/actions/workflows/codeql.yml)
[![Licence](https://img.shields.io/badge/licence-Proprietary-0E1B3D?labelColor=F7F4EC)](LICENSE)
[![EU hosted](https://img.shields.io/badge/hosted-EU-0E1B3D?labelColor=F7F4EC)](SECURITY.md)

> Per-client tenant registry for ViaVitae. Each client is a folder under `clients/`
> containing a `tenant.yaml`, multilingual MDX content, theme overrides and assets.
> This repository is the **audit trail** — humans edit only `tenant.yaml` and `content/`.

---

## The Golden Rule

**Humans never hand-edit generated artifacts.** The only hand-edited files are
`tenant.yaml` and `content/` — always via Pull Request. Everything else under
`generated/` is produced by the provisioning pipeline.

## Provisioning flow

```
PR opened → CI validates schema, lint, parity, secrets, consent
         → CODEOWNERS review (@JourneyOfLife @IterVitae)
         → Merge to main
         → provision-dispatch.yml → viavitae-api /v1/tenants/<slug>/provision
         → Staging deploy → Playwright smoke test (viavitae-qa)
         → Production sync via Argo CD
         → generated/manifest.json + lockfiles regenerated
```

## Repository layout

```text
viavitae-clients/
+-- clients/                      # One folder per client (hand-edited zone)
|   +-- _example/                 # Annotated reference tenant (fictional)
|   +-- <client-slug>/            # e.g. kauno-sv-petro-parapija
|   +-- _archive/                 # Offboarded tenants (24-month GDPR retention)
+-- generated/                    # Machine-generated — DO NOT EDIT
|   +-- manifest.json             # Full tenant inventory with hashes
|   +-- lockfiles/                # Resolved config per tenant
|   +-- reports/                  # CI artifacts
+-- schemas/                      # JSON Schemas for tenant.yaml, content, theme, billing
+-- scripts/                      # Validation tooling (run in CI)
+-- policies/                     # Addon matrix, domain rules, data boundary, pricing
+-- docs/                         # ADRs, DPIA, runbooks, consent registry
```

## Onboarding a new client

1. Copy `clients/_example/` to `clients/<slug>/`.
2. Fill in `tenant.yaml` — follow the annotated comments.
3. Add content under `content/lt/`, `content/en/`, `content/ru/`.
4. If any `consent_flags` are `true`, add a record in `docs/consent-registry/<slug>.yaml`.
5. Open a PR — CI validates schema, slug format, parity, secrets and consent.
6. After merge, the provisioning pipeline deploys the tenant.

See [docs/onboarding-runbook.md](docs/onboarding-runbook.md) for the full step-by-step.

## Guardrails (enforced in CI)

| ID | Rule | Enforcement |
| --- | --- | --- |
| G1 | Slug: `^[a-z0-9]+(-[a-z0-9]+)*$`, unique | `slug_check.py` |
| G2 | Tier/add-on matrix | `policies/allowed-addons.yaml` |
| G3 | Maintenance €30–50/mo | `policies/pricing-limits.yaml` |
| G4 | LT/EN/RU content parity (warn v1, fail v2) | `parity_check.py` |
| G5 | consent_flags=true requires DPIA record | `check_consent_dpias.py` |
| G6 | No secrets/PII | TruffleHog + `check_data_boundary.py` |
| G7 | `generated/` read-only for humans | `diff-guard.yml` |
| G8 | Offboarding = archive + 24-month retention | PR workflow |
| G9 | Action SHA pinning (rule R4) | `compliance-check.yml` |

## Security and compliance

- Report vulnerabilities privately per [SECURITY.md](SECURITY.md). Do **not** open a public issue.
- Personal-data processing requires a completed [DPIA](docs/DPIA-template.md).
- Architectural decisions are recorded as [ADRs](docs/architecture.md).

## Licence

Proprietary — All Rights Reserved. (c) ViaVitae IT Technologies. See [LICENSE](LICENSE).
