#!/usr/bin/env python3
"""Scan PR diff for PII patterns beyond public contacts.

Enforces data-boundary.yaml: no personal phone numbers, personal emails,
national ID numbers, or other PII beyond what tenant.yaml contacts allow.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Patterns that suggest PII beyond public contacts
PII_PATTERNS = [
    (re.compile(r"\b\d{11}\b"), "Possible personal code (11-digit number)"),
    (
        re.compile(
            r"\b[A-Z][a-z]+ [A-Z][a-z]+ .* (?:tel|mob|cell|phone)[:\s]", re.IGNORECASE
        ),
        "Personal name with phone",
    ),
    (
        re.compile(
            r"(?:password|passwd|secret|token|api_key)\s*[:=]\s*\S+", re.IGNORECASE
        ),
        "Possible credential",
    ),
]


def get_changed_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False,
        )
        return [
            f
            for f in result.stdout.strip().split("\n")
            if f and not f.startswith("generated/")
        ]
    except OSError:
        return []


def scan_file(filepath: Path) -> list[str]:
    findings: list[str] = []
    try:
        content = filepath.read_text(errors="ignore")
    except OSError:
        return findings

    for pattern, description in PII_PATTERNS:
        for match in pattern.finditer(content):
            line_num = content[: match.start()].count("\n") + 1
            findings.append(
                f"{filepath}:{line_num}: {description} — '{match.group()[:30]}...'"
            )
    return findings


def main() -> int:
    changed = get_changed_files()
    if not changed:
        print("No changed files to scan.")
        return 0

    all_findings: list[str] = []
    for f in changed:
        fp = REPO_ROOT / f
        if fp.exists() and fp.is_file():
            all_findings.extend(scan_file(fp))

    if all_findings:
        for finding in all_findings:
            print(f"WARNING: {finding}")
        print(f"\n{len(all_findings)} potential PII pattern(s) found. Review manually.")
        # v1: warnings only, do not block
        return 0

    print("Data boundary check passed. No PII patterns detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
