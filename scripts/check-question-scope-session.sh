#!/usr/bin/env bash
# Compare installed Cursor question-scope rule vs repo (content, not version tags).
# Use after IDE sync when a chat may have stale always-on rule cache (see README.md).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RULE_REPO="$ROOT/rules/cursor/question-scope.mdc"
SKILL_REPO="$ROOT/skills/question-scope/SKILL.md"
CURSOR_RULE="${CURSOR_RULES:-$HOME/.cursor/rules}/question-scope.mdc"

failures=0

echo "== question-scope session check =="
echo ""

echo "Stale always-on rule — if ANY appear in this chat's injected rules, reload window or new chat:"
echo "  - Section: ## Triggers (skill runs)"
echo "  - level L1 … L4 listed as triggers (without 'do not activate')"
echo "  - ? + keyword / tight match as a trigger"
echo "  - /question-scope matched mid-sentence (contract requires start or end only)"
echo ""
echo "Disk contract uses explicit audit tokens: qs:meta, audit: (see SKILL § Meta)."
echo "After rule/skill edits: see README.md § Lệnh chạy (verify, sync, optional spot-check #1, #6, #8/#21)."
echo ""

qs_rule_is_legacy() {
  grep -qE '^## Triggers \(skill runs\)' "$1" 2>/dev/null
}

check_file_legacy() {
  local label="$1"
  local file="$2"
  if [[ ! -f "$file" ]]; then
    echo "WARN: $label not found: $file"
    failures=$((failures + 1))
    return
  fi
  if qs_rule_is_legacy "$file"; then
    echo "FAIL: $label has legacy ## Triggers (skill runs)"
    failures=$((failures + 1))
    return
  fi
  echo "OK:   $label has no legacy Triggers section"
}

check_file_legacy "repo rule" "$RULE_REPO"
check_file_legacy "installed rule" "$CURSOR_RULE"

if [[ -f "$RULE_REPO" && -f "$CURSOR_RULE" ]]; then
  if cmp -s "$RULE_REPO" "$CURSOR_RULE"; then
    echo "OK:   installed rule matches repo file"
  else
    echo "FAIL: installed rule differs from repo — run IDE sync (README.md)"
    failures=$((failures + 1))
  fi
elif [[ ! -f "$CURSOR_RULE" ]]; then
  echo "WARN: installed rule not found: $CURSOR_RULE (run IDE sync — README.md)"
  failures=$((failures + 1))
fi

if grep -q 'Mirror rule' "$SKILL_REPO" 2>/dev/null; then
  echo "OK:   SKILL.md references mirror rule"
else
  echo "FAIL: SKILL.md missing Mirror rule section"
  failures=$((failures + 1))
fi

if [[ -L "$CURSOR_RULE" ]]; then
  target="$(readlink -f "$CURSOR_RULE" 2>/dev/null || readlink "$CURSOR_RULE")"
  echo "INFO: installed rule symlink → $target"
fi

echo ""
if [[ "$failures" -gt 0 ]]; then
  echo "Session check: $failures issue(s). See README.md § Lệnh chạy, then re-run: $0"
  echo "Then reload Cursor window or start a new chat."
  exit 1
fi

echo "Disk contract OK. If the agent still follows old triggers, the open chat cached an older rule body — reload window or new chat."
exit 0
