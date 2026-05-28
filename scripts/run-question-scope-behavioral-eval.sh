#!/usr/bin/env bash
# Optional: print agent spot-check checklist (AI Core repo only — not installed by make sync-ide).
# Default gate: make verify. Use this only for optional 2–3 chat spot-checks when Parsing/Meta/tokens change.
# See skills/question-scope/references/behavioral-gates.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURES="$ROOT/skills/question-scope/references/behavioral-eval-fixtures.json"
GATES="$ROOT/skills/question-scope/references/behavioral-gates.md"

BEHAVIORAL_IDS="1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23"

if [[ ! -f "$FIXTURES" ]]; then
  echo "ERROR: missing $FIXTURES" >&2
  exit 1
fi

echo "== question-scope spot-check checklist (optional) =="
echo ""
echo "Default gate: make verify. This script is optional — for Parsing/Meta/token contract changes."
echo "Minimum spot-check: scenarios #1, #6, #8 or #21 (see $GATES)."
echo "Open a NEW chat per scenario; paste user lines below; tick expect bullets."
echo ""

python3 - "$FIXTURES" <<'PY'
import json, sys
path = sys.argv[1]
data = json.load(open(path))
for s in data.get("scenarios", []):
    print(f"--- Scenario {s['id']} ({s['name']}) ---")
    print(f"Summary: {s.get('summary', '')}")
    print(f"Pressure row: #{s.get('pressure_row', '?')}")
    for i, turn in enumerate(s.get("turns", []), 1):
        print(f"\nTurn {i} — paste as user message:")
        print(turn["user"])
        print("\nExpect (all must pass):")
        for e in turn.get("expect", []):
            print(f"  [ ] {e}")
    print()
PY

echo "Done. Full list: $BEHAVIORAL_IDS — optional log in pressure-scenarios.md § Behavioral eval log."
