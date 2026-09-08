#!/usr/bin/env python3
"""Validate that consent_flags set to true have corresponding DPIA records.

Enforces guardrail G5: any tenant with publishes_clergy_personal_data=true,
cemetery_grave_search=true, or ai_assistant_approved_by set must have a
corresponding file in docs/consent-registry/<slug>.yaml.
"""

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = REPO_ROOT / "clients"
CONSENT_DIR = REPO_ROOT / "docs" / "consent-registry"


def main() -> int:
    errors: list[str] = []

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("_"):
            continue
        tenant_file = client_dir / "tenant.yaml"
        if not tenant_file.exists():
            continue

        with open(tenant_file) as f:
            data = yaml.safe_load(f)

        consent = data.get("consent_flags", {})
        slug = data.get("identity", {}).get("slug", client_dir.name)

        needs_consent_record = any(
            [
                consent.get("publishes_clergy_personal_data") is True,
                consent.get("cemetery_grave_search") is True,
                consent.get("ai_assistant_approved_by") is not None,
            ]
        )

        if needs_consent_record:
            consent_file = CONSENT_DIR / f"{slug}.yaml"
            if not consent_file.exists():
                errors.append(
                    f"{slug}: consent_flags require a record at docs/consent-registry/{slug}.yaml"
                )

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"\n{len(errors)} consent/DPIA violation(s). See guardrail G5.")
        return 1

    print("Consent/DPIA check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
