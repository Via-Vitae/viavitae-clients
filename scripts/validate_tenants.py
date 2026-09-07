#!/usr/bin/env python3
"""Validate all tenant.yaml files against the master JSON Schema."""
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "tenant.schema.json"
CLIENTS_DIR = REPO_ROOT / "clients"


def load_schema() -> dict:
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def find_tenants() -> list[Path]:
    tenants = []
    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("_"):
            continue
        tenant_file = client_dir / "tenant.yaml"
        if tenant_file.exists():
            tenants.append(tenant_file)
    return tenants


def validate_tenant(tenant_path: Path, schema: dict) -> list[str]:
    errors = []
    with open(tenant_path) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return [f"{tenant_path}: YAML parse error: {e}"]

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"{tenant_path}: {path}: {error.message}")
    return errors


def main() -> int:
    schema = load_schema()
    tenants = find_tenants()
    if not tenants:
        print("No tenant.yaml files found under clients/.")
        return 0

    all_errors: list[str] = []
    for tenant_path in tenants:
        all_errors.extend(validate_tenant(tenant_path, schema))

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"\n{len(all_errors)} validation error(s) across {len(tenants)} tenant(s).")
        return 1

    print(f"Validated {len(tenants)} tenant(s). All passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
