#!/usr/bin/env bash
# Warn when question-scope contract files changed — run manual behavioral eval before merge.
# Non-failing: prints hints only. Called from scripts/verify.sh.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CONTRACT_PATHS=(
  skills/question-scope/SKILL.md
  rules/cursor/question-scope.mdc
  skills/question-scope/references/gray-zones.md
  skills/question-scope/references/pressure-scenarios.md
  skills/question-scope/references/behavioral-eval-fixtures.json
)

if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

changed=()
for rel in "${CONTRACT_PATHS[@]}"; do
  if git -C "$ROOT" diff --name-only HEAD -- "$rel" 2>/dev/null | grep -q .; then
    changed+=("$rel")
  fi
  if git -C "$ROOT" diff --name-only --cached -- "$rel" 2>/dev/null | grep -q .; then
    changed+=("$rel")
  fi
done

if [[ "${#changed[@]}" -eq 0 ]]; then
  exit 0
fi

# Deduplicate (bash 3.2 compatible — no mapfile)
unique="$(printf '%s\n' "${changed[@]}" | sort -u)"

echo "== question-scope contract changed =="
printf '%s\n' "$unique" | sed 's/^/  - /'
echo ""
echo "Default gate: make verify (already run if you use make verify)."
echo "Optional: spot-check fixtures #1, #6, #8 or #21 in a NEW chat — see behavioral-gates.md"
echo "Then: make sync-ide + reload Cursor (sync installs rules/skills only, not scripts)."
echo ""
