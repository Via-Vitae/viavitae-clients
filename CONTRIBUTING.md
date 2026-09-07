# Contributing

Thank you for contributing to viavitae-clients. This document describes the workflow
for client onboarding, content changes and offboarding.

Read [QODER.md](QODER.md) before contributing with AI assistance, and
[SECURITY.md](SECURITY.md) before reporting anything security-related.

---

## Code of conduct

Contributors, reviewers and maintainers are expected to treat each other with respect.
Because ViaVitae serves religious communities, contributors additionally commit to
respecting the confidentiality and dignity of data subjects — many of whom are members of
a congregation and never consented to their data being discussed in a public forum.

Report a concern to `legal@viavitae.com`.

## The Golden Rule

**Humans never hand-edit generated artifacts.** The only hand-edited files are:

- `clients/<slug>/tenant.yaml`
- `clients/<slug>/content/`
- `clients/<slug>/theme/overrides.yaml`
- `clients/<slug>/assets/`

Everything under `generated/` is produced by the provisioning pipeline and protected by
`diff-guard.yml`.

## Development model: trunk-based

- Branch from `main`, merge back to `main`. No long-lived branches.
- `main` is always protected. Force-pushes and review dismissal are disabled.
- Administrators are not exempt from branch protection.

## Branch naming

| Prefix | Use | Example |
| --- | --- | --- |
| `feat/` | New client onboarding | `feat/kauno-sv-petro-parapija` |
| `fix/` | Correct a tenant.yaml or content error | `fix/parapija-tier-typo` |
| `chore/` | Maintenance, scripts, schemas | `chore/bump-schema-v2` |
| `docs/` | Documentation only | `docs/onboarding-runbook-update` |
| `ci/` | CI configuration only | `ci/add-parity-hard-fail` |

## Conventional Commits

Every commit follows [Conventional Commits](https://www.conventionalcommits.org/).

```text
<type>(<scope>): <imperative summary, max 72 characters>

Signed-off-by: Your Name <you@viavitae.com>
```

Configure sign-off:

```bash
git config --local user.name "Your Name"
git config --local user.email "you@viavitae.com"
git config --local format.signOff true
```

## Pull request rules

A PR may be merged only when **all** hold:

1. **One approving review** from `@JourneyOfLife` or `@IterVitae`.
2. **Green CI** — ci.yml, validate-tenant.yml, lint.yml, compliance-check.yml, codeql.yml.
3. **The PR template checklist completed.**
4. **Linear history.** Rebase onto `main`; merge method is squash.

## Client onboarding checklist

When onboarding a new client, confirm in the PR description:

- [ ] `tenant.yaml` validates against `schemas/tenant.schema.json`
- [ ] Slug matches `^[a-z0-9]+(-[a-z0-9]+)*$` and is unique
- [ ] Tier/add-on combination is allowed by `policies/allowed-addons.yaml`
- [ ] Maintenance plan is €30 or €50/mo
- [ ] Pages list matches `content/<lang>/pages/` structure
- [ ] LT content (default language) has all pages present
- [ ] EN/RU content parity is noted (warning in v1)
- [ ] Any `consent_flags: true` has a record in `docs/consent-registry/<slug>.yaml`
- [ ] No PII beyond public contacts in tenant.yaml
- [ ] Assets have copyright/consent note in `assets/README.md`
- [ ] CHANGELOG.md updated

## Local quality gates

```bash
# Validate all tenants
python scripts/validate_tenants.py

# Check slug format and uniqueness
python scripts/slug_check.py

# Check content parity
python scripts/parity_check.py

# Check consent/DPIA compliance
python scripts/check_consent_dpias.py

# Check data boundary (no PII beyond contacts)
python scripts/check_data_boundary.py

# YAML lint
yamllint clients/

# Secret scan (local)
python scripts/secret_scan_local.py
```

## AI-assisted contributions

AI assistance is welcome. You are accountable for everything in your PR. Before opening,
confirm no file was invented, no placeholder reached the diff, and the golden rule was
not violated. Note in the PR description that AI assistance was used.

## Getting help

| Question | Where |
| --- | --- |
| Onboarding workflow | [docs/onboarding-runbook.md](docs/onboarding-runbook.md) |
| Schema questions | `schemas/tenant.schema.json` + ADR-102 |
| Personal data, DPIA | `dpo@viavitae.com` |
| Vulnerabilities | `security@viavitae.com` — private, per SECURITY.md |
