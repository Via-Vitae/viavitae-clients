## Pull Request — viavitae-clients

<!-- Complete every checklist item. If an item does not apply, annotate "n/a" with a reason. -->

### Change type

- [ ] New client onboarding
- [ ] Tenant change (tier, pages, add-ons, domains)
- [ ] Content update (LT/EN/RU)
- [ ] Theme override
- [ ] Schema or policy change
- [ ] Script or CI change
- [ ] Documentation only
- [ ] Client offboarding

### Conventional Commit title

<!-- Title must follow: <type>(<scope>): <imperative summary> -->
<!-- Examples: feat(kauno-sv-petro-parapija): onboard new tenant -->
<!--           fix(content): add missing ru contact page -->

- [ ] Title follows Conventional Commits format

### Tenant validation (for client changes)

- [ ] `tenant.yaml` validates against `schemas/tenant.schema.json`
- [ ] Slug matches `^[a-z0-9]+(-[a-z0-9]+)*$` and is unique across all tenants
- [ ] Tier/add-on combination is allowed by `policies/allowed-addons.yaml`
- [ ] Maintenance plan is €30 or €50/mo per `policies/pricing-limits.yaml`
- [ ] Pages list matches `content/<lang>/pages/` directory structure
- [ ] Default language (lt) has all pages present
- [ ] Content parity noted for EN/RU (warning in v1, hard fail in v2)

### Consent and compliance

- [ ] No PII beyond public contacts in `tenant.yaml` (data-boundary.yaml)
- [ ] Any `consent_flags: true` has a record in `docs/consent-registry/<slug>.yaml`
- [ ] DPIA completed if new personal data processing is introduced
- [ ] No secrets, tokens or credentials anywhere in the diff
- [ ] Assets have copyright/consent note in `assets/README.md`

### Quality gates

- [ ] `python scripts/validate_tenants.py` passes
- [ ] `python scripts/slug_check.py` passes
- [ ] `python scripts/parity_check.py` passes (or warnings acknowledged)
- [ ] `yamllint clients/` passes
- [ ] `python scripts/check_data_boundary.py` passes
- [ ] `python scripts/check_consent_dpias.py` passes

### Generated artifacts

- [ ] No files under `generated/` were hand-edited (diff-guard.yml will block)

### Documentation

- [ ] CHANGELOG.md updated
- [ ] ADR added if schema, policy or architectural change

### Linked issue

<!-- Use Closes #123 to auto-close -->

Closes #

### AI assistance

<!-- If AI assistance was used, note which parts -->

- [ ] AI assistance used: _describe which parts_
