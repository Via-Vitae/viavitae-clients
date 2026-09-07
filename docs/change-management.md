# Change Management

Process for modifying an existing tenant's configuration.

## Types of changes

| Change | Risk | Approval |
| --- | --- | --- |
| Tier upgrade | Low — additive | Standard review |
| Tier downgrade | Medium — may disable features | Standard review + client confirmation |
| Add-on toggle | Low — additive or removal | Standard review |
| Page add/remove | Low — content only | Standard review |
| Domain change | Medium — DNS propagation | Standard review + infra coordination |
| Contact update | Low — public data only | Standard review |
| Theme override | Low — visual only | Standard review |
| Consent flag change | High — GDPR implications | Standard review + DPIA update |

## Process

1. Open a "Tenant change request" issue
2. Create a branch: `fix/<slug>-<change-type>`
3. Modify only the affected files under `clients/<slug>/`
4. If consent flags change, update `docs/consent-registry/<slug>.yaml`
5. Open PR with the tenant change checklist
6. After merge, provisioning pipeline re-deploys the tenant
