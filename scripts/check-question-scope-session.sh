#!/usr/bin/env bash
# Compare installed Cursor question-scope rule vs repo contract version.
# Use after make sync-ide when a chat may have stale always-on rule cache.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RULE_REPO="$ROOT/rules/cursor/question-scope.mdc"
SKILL_REPO="$ROOT/skills/question-scope/SKILL.md"
CURSOR_RULE="${CURSOR_RULES:-$HOME/.cursor/rules}/question-scope.mdc"

failures=0

qs_extract_tag() {
  local file="$1"
  grep -oE 'qs-[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+' "$file" 2>/dev/null | head -1
}

CANONICAL_TAG="$(qs_extract_tag "$RULE_REPO")"
if [[ -z "$CANONICAL_TAG" ]]; then
  echo "ERROR: no qs-… contract tag in $RULE_REPO" >&2
  exit 1
fi
TAG="$CANONICAL_TAG"

echo "== question-scope session check =="
echo "Canonical contract: $TAG"
echo ""

echo "Stale always-on rule — if ANY appear in this chat's injected rules, reload window or new chat:"
echo "  - Section: ## Triggers (skill runs)"
echo "  - level L1 … L4 listed as triggers (without 'do not activate')"
echo "  - ? + keyword / tight match as a trigger"
echo "  - Missing contract line: **Contract:** \`$TAG\`"
echo "  - /question-scope matched mid-sentence (contract requires start or end only)"
echo ""
echo "Disk contract uses explicit audit tokens: qs:meta, audit: (see SKILL § Meta)."
echo "After qs-… bump in AI Core repo: make verify; optional spot-check #1, #6, #8/#21 (behavioral-gates.md)."
echo ""

qs_rule_is_legacy() {
  grep -qE '^## Triggers \(skill runs\)' "$1" 2>/dev/null
}

check_file_version() {
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
  if grep -qF "$TAG" "$file"; then
    echo "OK:   $label contains $TAG"
  else
    echo "FAIL: $label missing $TAG — update rule/skill and run make sync-ide"
    failures=$((failures + 1))
  fi
}

check_file_version "repo rule" "$RULE_REPO"
check_file_version "installed rule" "$CURSOR_RULE"

skill_tag="$(qs_extract_tag "$SKILL_REPO")"
if [[ "$skill_tag" != "$TAG" ]]; then
  echo "FAIL: SKILL.md tag ($skill_tag) != rule tag ($TAG)"
  failures=$((failures + 1))
else
  echo "OK:   SKILL.md tag matches rule ($TAG)"
fi

if [[ -L "$CURSOR_RULE" ]]; then
  target="$(readlink -f "$CURSOR_RULE" 2>/dev/null || readlink "$CURSOR_RULE")"
  echo "INFO: installed rule symlink → $target"
fi

echo ""
if [[ "$failures" -gt 0 ]]; then
  echo "Session check: $failures issue(s). Run: make sync-ide && $0"
  echo "Then reload Cursor window or start a new chat."
  exit 1
fi

echo "Disk contract OK. If the agent still follows old triggers, the open chat cached an older rule body — reload window or new chat."
exit 0
