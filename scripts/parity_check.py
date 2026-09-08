#!/usr/bin/env python3
"""Check LT/EN/RU content parity across all tenants.

v1: WARNING on missing keys in non-default languages.
    HARD FAIL only if default language (lt) is missing pages listed in tenant.yaml.
v2: HARD FAIL on any missing key across all languages.
"""

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = REPO_ROOT / "clients"
LANGUAGES = ["lt", "en", "ru"]
DEFAULT_LANG = "lt"


def get_expected_pages(tenant_dir: Path) -> list[str]:
    tenant_file = tenant_dir / "tenant.yaml"
    if not tenant_file.exists():
        return []
    with open(tenant_file) as f:
        data = yaml.safe_load(f)
    pages = data.get("pages", [])
    return [str(p) for p in pages] if pages else []


def get_actual_pages(content_dir: Path, lang: str) -> set[str]:
    pages_dir = content_dir / lang / "pages"
    if not pages_dir.exists():
        return set()
    return {p.stem for p in pages_dir.glob("*.mdx")}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("_"):
            continue
        content_dir = client_dir / "content"
        if not content_dir.exists():
            continue

        expected = get_expected_pages(client_dir)
        if not expected:
            continue

        for lang in LANGUAGES:
            actual = get_actual_pages(content_dir, lang)
            missing = set(expected) - actual
            if missing:
                msg = f"{client_dir.name}/{lang}: missing pages: {sorted(missing)}"
                if lang == DEFAULT_LANG:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Content parity check passed (v1: default language complete).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
