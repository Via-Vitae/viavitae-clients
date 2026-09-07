#!/usr/bin/env python3
"""Pre-commit TruffleHog --only-verified wrapper.

Runs TruffleHog locally against the working tree to catch secrets
before they reach CI. Requires trufflehog to be installed locally.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if not shutil.which("trufflehog"):
        print("WARNING: trufflehog not found in PATH. Install from https://github.com/trufflesecurity/trufflehog")
        print("Skipping local secret scan. CI will still run TruffleHog.")
        return 0

    result = subprocess.run(
        ["trufflehog", "filesystem", "--directory", str(REPO_ROOT), "--only-verified", "--no-update"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("ERROR: TruffleHog found verified secrets:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1

    print("Local secret scan passed (TruffleHog --only-verified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
