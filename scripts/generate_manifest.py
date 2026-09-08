#!/usr/bin/env python3
"""Generate generated/manifest.json — full inventory of tenants with hashes."""

import hashlib
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = REPO_ROOT / "clients"
GENERATED_DIR = REPO_ROOT / "generated"


def file_hash(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def main() -> int:
    tenants = {}

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("_"):
            continue
        tenant_file = client_dir / "tenant.yaml"
        if not tenant_file.exists():
            continue

        with open(tenant_file) as f:
            data = yaml.safe_load(f)

        slug = data.get("identity", {}).get("slug", client_dir.name)
        tenants[slug] = {
            "path": str(client_file.relative_to(REPO_ROOT))
            if (client_file := tenant_file).exists()
            else "",
            "hash": file_hash(tenant_file),
            "status": data.get("status", "unknown"),
            "tier": data.get("tier", {}).get("package", "unknown"),
        }

    manifest = {
        "schema_version": 1,
        "tenant_count": len(tenants),
        "tenants": tenants,
    }

    GENERATED_DIR.mkdir(exist_ok=True)
    manifest_path = GENERATED_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Generated manifest.json with {len(tenants)} tenant(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
