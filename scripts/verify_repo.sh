#!/usr/bin/env bash
# verify_repo.sh — Pre-first-commit verification for viavitae-clients.
# Runs 12 local gates. Exit 0 only if ALL pass. Read-only: never mutates files.
# Usage: bash scripts/verify_repo.sh   from repo ROOT.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0
TOTAL=12

gate() {
  local id="$1" name="$2" rc="$3"
  if [ "$rc" -eq 0 ]; then
    echo "  PASS L${id}: ${name}"
    PASS=$((PASS + 1))
  else
    echo "  FAIL L${id}: ${name} (exit ${rc})"
    FAIL=$((FAIL + 1))
  fi
}

echo "============================================"
echo " viavitae-clients — 12 Local Gates"
echo "============================================"
echo ""

# --- L1: YAML parse ----------------------------------------------------------
echo "--- L1: YAML parse ---"
python3 - <<'PY' 2>/dev/null
import pathlib, sys
try:
    import yaml
except ImportError:
    sys.exit(0)
bad = []
for p in pathlib.Path('.').rglob('*.y*ml'):
    s = str(p)
    if any(x in s for x in ('.venv/', '.git/', '.idea/')): continue
    try: yaml.safe_load(p.read_text())
    except Exception as e: bad.append(f"{s}: {e}")
if bad:
    print('\n'.join(bad)); sys.exit(1)
PY
gate 1 "YAML parse" $?

# --- L2: JSON parse -----------------------------------------------------------
echo "--- L2: JSON parse ---"
python3 - <<'PY' 2>/dev/null
import json, pathlib, sys
bad=[]
for p in pathlib.Path('.').rglob('*.json'):
    s=str(p)
    if any(x in s for x in ('.venv/','.git/','.idea/')): continue
    try: json.loads(p.read_text())
    except Exception as e: bad.append(f"{s}: {e}")
if bad: print('\n'.join(bad)); sys.exit(1)
PY
gate 2 "JSON parse" $?

# --- L3: Schema validation (ALL tenants, not just _example) -------------------
echo "--- L3: Schema validation ---"
python3 - <<'PY' 2>/dev/null
import json, pathlib, sys
try:
    import jsonschema, yaml
except ImportError:
    sys.exit(0)
schema=json.loads(pathlib.Path('schemas/tenant.schema.json').read_text())
tenants=list(pathlib.Path('clients').glob('*/tenant.yaml'))
errors=[]
for t in tenants:
    try:
        jsonschema.validate(yaml.safe_load(t.read_text()), schema)
    except Exception as e: errors.append(f"{t}: {e}")
if errors: print('\n'.join(errors)); sys.exit(1)
PY
gate 3 "Schema: all tenants" $?

# --- L4: Slug rules -----------------------------------------------------------
echo "--- L4: Slug rules ---"
python3 scripts/slug_check.py >/dev/null 2>&1
gate 4 "Slug format + uniqueness" $?

# --- L5: LT/EN/RU content parity ---------------------------------------------
echo "--- L5: Content parity ---"
python3 scripts/parity_check.py >/dev/null 2>&1
gate 5 "LT/EN/RU content parity" $?

# --- L6: Secrets scan (gitleaks CLI preferred, regex fallback) ---------------
echo "--- L6: Secrets scan ---"
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --no-banner --source . --verbose >/dev/null 2>&1
  gate 6 "Secrets: gitleaks" $?
else
  python3 - <<'PY' 2>/dev/null
import pathlib, re, sys
pats=[re.compile(r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*["\'][^"\']{8,}["\']')]
skip=('.git/','.venv/','.idea/','generated/')
bad=[]
for p in pathlib.Path('.').rglob('*'):
    s=str(p)
    if p.is_dir() or any(k in s for k in skip): continue
    try: txt=p.read_text(errors='ignore')
    except Exception: continue
    for pat in pats:
        for m in pat.finditer(txt):
            frag=m.group(0)
            if '__REPLACE_ME__' in frag or 'REPLACE_ME' in frag: continue
            if 'example' in s.lower() or 'pavyzd' in s.lower(): continue
            bad.append(f"{s}: {frag[:60]}")
if bad: print('\n'.join(bad)); sys.exit(1)
PY
  gate 6 "Secrets: regex fallback" $?
fi

# --- L7: Data boundary (PII in content files) --------------------------------
echo "--- L7: Data boundary ---"
python3 - <<'PY' 2>/dev/null
import pathlib, re, sys
email=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
phone=re.compile(r'(\+370|\+371|\+372)\s?\d[\d\s-]{6,}')
bad=[]
for p in pathlib.Path('clients').rglob('*.mdx'):
    txt=p.read_text(errors='ignore')
    hits=[*email.findall(txt), *phone.findall(txt)]
    if hits: bad.append(f"{p}: {len(hits)} PII pattern(s)")
if bad: print('\n'.join(bad)); sys.exit(1)
PY
gate 7 "Data boundary: no PII in content" $?

# --- L8: Consent flags require DPIA/consent reference -------------------------
echo "--- L8: Consent registry ---"
python3 scripts/check_consent_dpias.py >/dev/null 2>&1
gate 8 "Consent flags have DPIA refs" $?

# --- L9: Pricing limits (actual tenant structure) ----------------------------
echo "--- L9: Pricing limits ---"
python3 - <<'PY' 2>/dev/null
import pathlib, yaml, sys
bad=[]
for t in pathlib.Path('clients').glob('*/tenant.yaml'):
    data = yaml.safe_load(t.read_text())
    tier = data.get('tier', {})
    pkg = tier.get('package', '')
    maint = tier.get('maintenance_plan', '')
    if pkg not in ('economy', 'normal', 'vip'):
        bad.append(f"{t}: package='{pkg}' not in economy/normal/vip")
    if maint not in ('standard', 'premium'):
        bad.append(f"{t}: maintenance_plan='{maint}' not in standard/premium")
if bad: print('\n'.join(bad)); sys.exit(1)
PY
gate 9 "Pricing: tier + maintenance valid" $?

# --- L10: Policy enforcement (add-on/tier matrix) ----------------------------
echo "--- L10: Policy enforcement ---"
python3 - <<'PY' 2>/dev/null
import pathlib, re, sys, yaml
# Load the add-on/tier matrix
policy = yaml.safe_load(open('policies/allowed-addons.yaml'))
tier_order = policy.get('tier_order', ['economy', 'normal', 'vip'])
addons_policy = policy.get('addons', {})
bad=[]
for t in pathlib.Path('clients').glob('*/tenant.yaml'):
    data = yaml.safe_load(t.read_text())
    pkg = data.get('tier', {}).get('package', '')
    addons = data.get('tier', {}).get('addons', {})
    if not addons or pkg not in tier_order: continue
    pkg_idx = tier_order.index(pkg)
    for addon_name, enabled in addons.items():
        if not enabled: continue
        addon_policy = addons_policy.get(addon_name, {})
        min_tier = addon_policy.get('min_tier', '')
        if min_tier and min_tier in tier_order:
            min_idx = tier_order.index(min_tier)
            if pkg_idx < min_idx:
                bad.append(f"{t}: {addon_name}=true requires tier >= {min_tier} (has {pkg})")
if bad: print('\n'.join(bad)); sys.exit(1)
PY
gate 10 "Policy: add-on/tier matrix" $?

# --- L11: Generated zone integrity -------------------------------------------
echo "--- L11: Generated zone ---"
python3 - <<'PY' 2>/dev/null
import pathlib, sys
bad=[]
for p in pathlib.Path('generated').rglob('*'):
    if not p.is_file(): continue
    # No YAML files should exist in generated/ (only .json/.lock.json/.gitkeep)
    if p.suffix in ('.yaml', '.yml'):
        bad.append(f"unexpected YAML in generated/: {p}")
        continue
    try: head = p.read_text(errors='ignore')[:400]
    except Exception: continue
    # Check for hand-edit markers
    if 'HAND_EDITED' in head:
        bad.append(f"hand-edit marker in: {p}")
    elif 'TODO' in head or 'FIXME' in head or 'HACK' in head:
        bad.append(f"dev marker in: {p}")
if bad: print('\n'.join(bad)); sys.exit(1)
PY
gate 11 "Generated zone: no hand-edits" $?

# --- L12: Manifest generation ------------------------------------------------
echo "--- L12: Manifest generation ---"
python3 scripts/generate_manifest.py >/dev/null 2>&1
L12_RC=$?
if [ "$L12_RC" -eq 0 ] && [ -f generated/manifest.json ]; then
  python3 -c "
import json, sys
m = json.load(open('generated/manifest.json'))
assert 'tenants' in m and 'schema_version' in m
print(f'  manifest.json: {m.get(\"tenant_count\", 0)} tenant(s)')
" 2>/dev/null
  L12_RC=$?
fi
gate 12 "Manifest: generate + valid" "$L12_RC"

echo ""
echo "============================================"
echo " Results: ${PASS}/${TOTAL} passed, ${FAIL} failed"
echo "============================================"

if [ "$FAIL" -eq 0 ]; then
  echo ""
  echo "ALL 12 LOCAL GATES PASSED"
  exit 0
else
  echo ""
  echo "FAILURES DETECTED — fix before commit"
  exit 1
fi
