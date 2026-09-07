# Security Policy

ViaVitae IT Technologies takes the security of its systems and the privacy of the people
it serves seriously. This policy describes how to report a vulnerability, what to expect
from us, and the protections we extend to good-faith researchers.

## Reporting a vulnerability

**Please do not open a public GitHub issue.** Public disclosure before a fix is available
puts users at risk.

| Channel | Detail |
| --- | --- |
| **Email** | `security@viavitae.com` |
| **Encryption** | Strongly encouraged. Our PGP public key is published on the [OpenPGP key servers](https://keys.openpgp.org/search?q=security%40viavitae.com); fetch and verify the fingerprint out of band before first use. |
| **GitHub** | Private vulnerability reporting is enabled on repositories in the `Via-Vitae` organisation. Use *Security* -> *Report a vulnerability* when available. |

Include as much of the following as you can:

1. The type of issue (for example: SQL injection, broken access control, secret exposure,
   dependency vulnerability, misconfigured storage).
2. The affected repository, and the branch, tag or commit SHA.
3. The affected environment (production, staging, demo tenant) and URL or host.
4. Step-by-step instructions to reproduce the issue.
5. Proof of concept, exploit code, or a screenshot where it helps.
6. The impact you believe the issue has, and who is affected.
7. Whether you have already accessed, stored or altered any personal data. If you have,
   say so explicitly and stop — we will take over handling under the breach process below.

Please do not access, exfiltrate, modify or delete data belonging to other users beyond
the minimum needed to demonstrate the issue, and do not use an exploit to maintain
persistent access.

## Response service levels

### Acknowledgement and triage

| Stage | Target |
| --- | --- |
| **Acknowledgement** | Within **24 hours** of receipt. |
| **Triage and severity assignment** | Within **72 hours** of receipt. |
| **Status update cadence** | At least every 5 business days until closure. |
| **Researcher notification of fix** | Within 5 business days of deployment. |

If you have not received an acknowledgement within 24 hours, resend to the same address
and copy `legal@viavitae.com`.

### Remediation SLA

| Severity | CVSS | Containment | Remediation | Public advisory |
| --- | --- | --- | --- | --- |
| **Critical** | 9.0 - 10.0 | **72 hours** | 7 days | Within 5 business days of fix |
| **High** | 7.0 - 8.9 | 72 hours | **7 days** | Within 10 business days of fix |
| **Medium** | 4.0 - 6.9 | Best effort | **30 days** | At next scheduled release |
| **Low** | 0.1 - 3.9 | Best effort | Next scheduled release | Optional |

## GDPR breach notification workflow

A confirmed security incident involving personal data is handled under Regulation (EU)
2016/679 in parallel with technical remediation.

1. **Detect and log.** The incident is recorded with the time of awareness.
2. **Assess within 24 hours.** The DPO assesses whether the incident is a personal data
   breach under Article 4(12).
3. **Notify the supervisory authority within 72 hours** of becoming aware, per Article 33.
4. **Notify data subjects without undue delay** where the breach is likely to result in a
   high risk to them, per Article 34.
5. **Record internally** in every case, per Article 33(5).
6. **Close the loop.** The DPIA for the affected processing is revisited.

The DPO (`dpo@viavitae.com`) owns steps 2 to 5.

## Safe harbour for good-faith research

We will not initiate legal action against a researcher who:

- reports a vulnerability promptly through the channels above;
- accesses only the minimum data necessary to demonstrate the issue;
- performs testing only against accounts and demo tenants they own or control;
- avoids techniques that degrade service for others;
- does not maintain persistent access or move laterally beyond the initial finding;
- acts in good faith and does not seek compensation beyond any published bounty terms.

## Scope

| Scope | Detail |
| --- | --- |
| **Repositories** | All repositories in the `Via-Vitae` GitHub organisation. |
| **Domains and subdomains** | All `*.viavitae.com` hosts, including client tenant subdomains provisioned from this repository. |
| **Marketplace** | `jolarca.com` and the `jolarca` repository. |
| **Infrastructure** | Self-hosted Proxmox, k3s and Terraform-managed resources. |

## Contact

| Role | Contact |
| --- | --- |
| Security team | `security@viavitae.com` |
| Data Protection Officer | `dpo@viavitae.com` |
| Legal | `legal@viavitae.com` |

This policy is reviewed at least annually, and after any Critical severity incident.
