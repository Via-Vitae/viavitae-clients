# Onboarding Runbook

Step-by-step guide to onboarding a new client tenant.

## Prerequisites

- GitHub issue opened via the "New client onboarding" form
- Written consent on file for any clergy personal data
- Client domain DNS can be pointed to the cluster
- Tier and add-on selection confirmed with the client

## Steps

### 1. Create the client directory

```bash
cp -r clients/_example clients/<slug>
```

### 2. Fill in tenant.yaml

Copy the annotated example and replace all values. Key fields:

- `identity.slug` — lowercase, hyphen-separated, no diacritics
- `identity.display_name` — full official name with Lithuanian characters
- `tier.package` — economy/normal/vip
- `tier.maintenance_plan` — standard (€30) or premium (€50)
- `pages` — must match the content directory structure
- `domains.primary` — the client's main domain
- `contacts` — public emails only, no personal data

### 3. Add content

Create MDX files under `content/lt/pages/` for each page listed in tenant.yaml.
Then mirror to `content/en/pages/` and `content/ru/pages/`.

v1: EN/RU parity is warning-only. LT (default) must be complete.

### 4. Handle consent flags

If any `consent_flags` are `true`:

1. Create `docs/consent-registry/<slug>.yaml` with DPIA reference
2. Include consent date, approver name, and document reference

### 5. Add theme overrides (optional)

Edit `theme/overrides.yaml` if the client has brand requirements.
Colors must pass WCAG AA contrast.

### 6. Add assets (if needed)

Place client-provided images in `assets/client-owns/`.
Update `assets/README.md` with copyright/consent confirmation.

### 7. Open a PR

Use the PR template checklist. CI will validate:
- Schema compliance
- Slug format and uniqueness
- Content parity
- Consent/DPIA records
- Data boundary (no PII)

### 8. After merge

`provision-dispatch.yml` automatically triggers the provisioning pipeline.
The tenant is deployed to staging, smoke-tested, then promoted to production.
`generated/manifest.json` and lockfiles are regenerated.
