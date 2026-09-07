#!/usr/bin/env python3
"""Check slug format and uniqueness across all tenants including _archive."""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = REPO_ROOT / "clients"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def main() -> int:
    errors: list[str] = []
    seen_slugs: dict[str, Path] = {}

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir():
            continue
        slug = client_dir.name
        if slug.startswith("_"):
            continue

        if not SLUG_PATTERN.match(slug):
            errors.append(f"Invalid slug format: '{slug}' at {client_dir}")

        if slug in seen_slugs:
            errors.append(f"Duplicate slug '{slug}': {client_dir} and {seen_slugs[slug]}")
        seen_slugs[slug] = client_dir

    # Check archive slugs too (strip .archived suffix)
    archive_dir = CLIENTS_DIR / "_archive"
    if archive_dir.exists():
        for archived in sorted(archive_dir.iterdir()):
            if not archived.is_dir():
                continue
            raw_slug = archived.name
            slug = raw_slug.removesuffix(".archived")
            if not SLUG_PATTERN.match(slug):
                errors.append(f"Invalid archived slug: '{slug}' at {archived}")
            if slug in seen_slugs:
                errors.append(f"Slug '{slug}' exists in both active and archive: {seen_slugs[slug]} and {archived}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(f"Slug check passed. {len(seen_slugs)} unique slug(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
