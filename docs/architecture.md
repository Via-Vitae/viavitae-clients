# Architecture Decision Records

This file is the ADR index and template for the repository. Every architectural decision
with a security, privacy, data-residency, cost or maintainability consequence is recorded
here. Decisions are made in conversations and lost; ADRs are how a team remembers why the
system is shaped the way it is, which is what makes it safe to change later.

Records follow [MADR](https://adr.github.io/madr/) adapted for a regulated EU context: the
**Compliance impact** section is mandatory here, because under rules R1 and R5 a decision
that touches personal data or residency cannot be taken without it.

---

## When an ADR is required

Write an ADR before implementing, not after. An ADR written afterwards is a justification;
an ADR written before is a decision.

| Situation | ADR required |
| --- | --- |
| Introducing or replacing a framework, runtime, database or message broker | Yes |
| Adding a third-party processor, SaaS provider, API or AI endpoint | Yes |
| Any change to where personal data is stored, backed up or processed | Yes |
| Changing an authentication, authorisation or tenancy mechanism | Yes |
| Changing a retention period or a lawful basis | Yes |
| Diverging from `viavitae-template` governance or CI defaults (rule R1) | Yes |
| Accepting a dependency with a licence outside the allow list | Yes |
| Accepting a known security or accessibility finding as tolerable | Yes |
| Choosing a deployment topology, region or hosting provider | Yes |
| A bug fix inside an existing agreed design | No |
| Adding a test, a translation, or documentation | No |

## Numbering convention

- Format: `ADR-NNN`, zero-padded to three digits, starting at `ADR-001`.
- Numbers are allocated sequentially from the index below and are **never reused**, even
  when a record is superseded or withdrawn. A retired number stays in the index so links
  from old pull requests and issues continue to resolve.
- The file heading is `## ADR-NNN: <short title in sentence case>`.
- Superseding a record does not delete it. Set its status to `Superseded by ADR-MMM` and
  leave the body intact. The history of what was tried and rejected is as valuable as the
  current decision.
- The ADR number is referenced in the commit message footer, the pull request description
  and any DPIA that depends on it.

## Status values

| Status | Meaning |
| --- | --- |
| `Proposed` | Under discussion. Implementation must not start. |
| `Accepted` | Agreed and in force. Implementation may proceed. |
| `Deprecated` | No longer applies to new work; existing systems may still depend on it. |
| `Superseded by ADR-MMM` | Replaced. Kept for history, links updated to the successor. |
| `Rejected` | Considered and declined. Kept so the question is not re-litigated. |

---

## Index

| ADR | Title | Status | Owner | Date |
| --- | --- | --- | --- | --- |
| [ADR-001](#adr-001-adopt-viavitae-template-as-the-repository-baseline) | Adopt viavitae-template as the repository baseline | Accepted | Architects | 2026-09-06 |
| _ADR-002_ | _next available number_ | — | — | — |

New records are added at the end of this file and referenced from the table above, in the
same pull request. An ADR that is not in the index has not been made.

---

## ADR-001: Adopt viavitae-template as the repository baseline

| Field | Value |
| --- | --- |
| **Status** | Accepted |
| **Owner** | `@JourneyOfLife @IterVitae` |
| **Date** | 2026-09-06 |
| **Deciders** | Architects, Security, Compliance, DPO |
| **Consulted** | Platform, Legal |
| **Supersedes** | — |
| **Superseded by** | — |

### Context

ViaVitae operates ten repositories spanning a Next.js marketing site, a FastAPI backend,
Terraform and Kubernetes infrastructure, a documentation and compliance hub, shared QA
assets, a marketplace fork and per-client tenant repositories. Before this decision each
repository assembled its own governance, CI and privacy artefacts by hand, or inherited
them from whichever project was cloned most recently.

The consequences were concrete: secret scanning was present in some repositories and
absent in others; ownership rules used placeholder team handles that resolved to nobody,
so no reviewer was ever requested; a performance gate referenced a path in a sibling
repository that did not exist once the repositories were separated, and the trailing
`|| true` meant the gate reported success while testing nothing; and no repository could
state where its personal data was stored.

The organisation is subject to GDPR, targets WCAG 2.2 AA, and requires that personal data
remain in the EEA on self-hosted Proxmox infrastructure. Compliance evidence has to be
producible per repository, on demand, without an archaeology project.

### Decision

Every ViaVitae repository is generated from `viavitae-template` using GitHub's template
mechanism, and the template is the single source of truth for governance, CI, compliance
and privacy artefacts. Rule R1 in `README.md` states this as binding.

Specifically:

1. New repositories are created with `gh repo create --template`, never by cloning a
   sibling or copying files.
2. The template's governance files are present and non-empty in every repository; their
   presence is verified mechanically by `compliance-check.yml`, not by review discipline.
3. Divergence from the template requires a further ADR stating the reason, the risk
   accepted and a review date. Silent divergence is a defect.
4. Improvements flow into the template first, then out to consumers by merging
   `upstream/main`. A fix applied to one repository only is an unfinished fix.
5. Third-party GitHub Actions are pinned to full-length commit SHAs and workflows declare
   least-privilege `permissions`, enforced by the `action-pinning` gate.

### Consequences

**Positive**

- A new repository is compliant on its first commit rather than after its first incident.
- Compliance evidence is uniform across repositories, so an audit or a supervisory-authority
  request can be answered with the same artefacts everywhere.
- One place to fix a governance defect, and a mechanical path to propagate the fix.
- Ownership rules resolve to real teams, so required review actually blocks a merge.
- Reviewers learn one CI shape, which makes an unfamiliar repository readable in minutes.

**Negative and accepted**

- A uniform template does not fit every repository type equally. A documentation site
  carries gates it does not need. This is mitigated by the repo-type adaptation checklist
  in `README.md`, and the cost of a redundant gate is accepted as lower than the cost of a
  missing one.
- Template updates require a merge into ten repositories. Propagation is manual and will
  lag. Accepted, because the alternative — no shared baseline — is what produced the
  original problem.
- The template becomes a single point of failure: a defect in it is a defect everywhere.
  Mitigated by `CODEOWNERS` requiring architect and compliance review for changes to
  `.github/`, and by the template's own CI running against itself.
- SHA pinning adds maintenance: Dependabot must move pins weekly. Accepted, because a
  mutable tag on a third-party action is a supply-chain exposure in a repository that
  handles special category data.

### Alternatives considered

| Alternative | Why rejected |
| --- | --- |
| Keep per-repository hand-maintained governance | This is the status quo that produced inconsistent secret scanning, unresolved ownership and a silently dead gate. It does not produce auditable evidence. |
| A monorepo containing all ten projects | Simplifies propagation but conflicts with the repository index, with per-repository ownership and licensing, with the marketplace fork's upstream sync requirement, and with GitHub's template-repository feature. It also widens the blast radius of any single credential compromise to every product. |
| An external configuration-management tool that pushes governance into each repository | Adds a moving part and a credential with write access to every repository, and the pushed state drifts the moment someone edits a file directly. A template plus a presence gate achieves the same guarantee with no additional secret. |
| GitHub organisation-level defaults only, without a template | Organisation defaults cover community-health files but cannot supply CI, dependency configuration, ADR and DPIA structure. They complement the template; they do not replace it. |
| Adopt an existing public enterprise template | None carried the EU data-residency constraint, the GDPR Article 33 breach workflow, WCAG 2.2 AA as a merge gate, or the Article 9 handling that a church vertical requires. Adapting one would cost more than writing one. |

### Compliance impact

| Area | Impact |
| --- | --- |
| GDPR | Positive. Makes the DPIA requirement discoverable in every repository and ties it to rule R5, so an assessment is raised before processing starts rather than after. |
| Article 9 special categories | Positive. The DPIA template and the feature-request form both ask explicitly about religious belief, which is the sensitive category most likely to arise in this vertical. |
| Data residency | Positive. The template states the EEA constraint in `README.md`, `SECURITY.md` and `QODER.md`, and makes it a stop-condition under QODER rule 7. |
| Breach notification, Art. 33 | Positive. One disclosure and breach workflow, identical in every repository, with a documented 72-hour path. |
| Accessibility, WCAG 2.2 AA | Positive. Present in the pull-request checklist and as a QODER stop-condition, so it is raised at design time. |
| Licensing | Positive. The allow list is enforced mechanically rather than by memory, and an unknown licence fails closed. |
| Supply chain | Positive. SHA pinning plus least-privilege tokens reduce the risk that a compromised upstream action reaches a repository holding personal data. |
| New processors introduced | None. The template introduces no third-party service. |
| Personal data processed | None. The template contains no personal data. |

---

## ADR template

Copy everything below the line into a new section at the end of this file, assign the next
number from the index, and add the index row in the same pull request.

```markdown
## ADR-NNN: <short title in sentence case>

| Field | Value |
| --- | --- |
| **Status** | Proposed |
| **Owner** | <team handle, for example @JourneyOfLife @IterVitae> |
| **Date** | <YYYY-MM-DD> |
| **Deciders** | <roles and teams that agreed> |
| **Consulted** | <roles and teams whose input was sought> |
| **Supersedes** | <ADR-NNN or —> |
| **Superseded by** | <ADR-NNN or —> |

### Context

<The situation and the forces acting on it. What is true today, what constraint applies,
and why a decision is needed now. State the problem, not the preferred answer. Name the
regulatory, operational and technical constraints explicitly — GDPR, WCAG 2.2 AA, EEA data
residency, self-hosted Proxmox, existing contracts. Include the cost of doing nothing.>

### Decision

<The decision, in the active voice, specific enough to be implemented without further
interpretation. Number the constituent parts where there is more than one. A reader should
be able to tell whether an implementation conforms to this decision.>

### Consequences

<What becomes easier, what becomes harder, and what risk is knowingly accepted. Include the
negative consequences — an ADR that lists only benefits has not been thought through. State
migration cost, operational burden and what has to be undone if the decision is reversed.>

### Alternatives considered

<Each rejected alternative and the reason for rejection, as a table. Recording why an option
was declined prevents the same debate recurring when the person who declined it has left.>

### Compliance impact

<Effects on GDPR, lawful basis, special category data, data residency and transfers,
retention, breach exposure, accessibility and licensing. Whether a DPIA is required, and its
reference if one exists. Whether a new processor is introduced and whether a DPA is in place.
State "none" explicitly where there is genuinely no impact — a blank section is ambiguous.>
```
