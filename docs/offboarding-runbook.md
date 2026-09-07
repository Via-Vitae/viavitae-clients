# Offboarding Runbook

Process for removing a client tenant from the registry.

## Prerequisites

- Client has been notified in writing
- Database backup is scheduled
- Domain DNS handover plan is confirmed
- 24-month retention period acknowledged (GDPR Art. 5(1)(e))

## Steps

### 1. Open offboarding issue

Use the "Client offboarding" issue template. Confirm all checklist items.

### 2. Move to archive

```bash
git mv clients/<slug> clients/_archive/<slug>.archived
```

### 3. Update tenant status

If the tenant.yaml is still accessible, set `status: archived`.

### 4. Open PR

The PR should contain only the move to `_archive/`. CI validates slug uniqueness.

### 5. After merge

`provision-dispatch.yml` triggers deprovisioning:
- Tenant is removed from the cluster
- Database is archived (encrypted, EU storage)
- DNS records are removed or redirected
- After 24 months, the archive is permanently erased

### 6. Consent registry

Move `docs/consent-registry/<slug>.yaml` to the archive alongside the tenant.
Consent records are retained for the same 24-month period.
