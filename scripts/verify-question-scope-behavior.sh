#!/usr/bin/env bash
# Contract anchors for behavioral gates (see behavioral-eval-fixtures.json).
# Does not run LLM/agent eval — optional spot-checks: behavioral-gates.md (not required every PR).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURES="$ROOT/skills/question-scope/references/behavioral-eval-fixtures.json"
SKILL="$ROOT/skills/question-scope/SKILL.md"
GRAY="$ROOT/skills/question-scope/references/gray-zones.md"
LEVEL_PICKER="$ROOT/skills/question-scope/references/level-picker.md"
L2_PATCH="$ROOT/skills/question-scope/templates/phases/l2/l2-patch.md"
L3_DEFINE="$ROOT/skills/question-scope/templates/phases/l3/l3-01-define.md"
SCENARIOS="$ROOT/skills/question-scope/references/pressure-scenarios.md"
RULE="$ROOT/rules/cursor/question-scope.mdc"

BEHAVIORAL_IDS=(1 4 4b 6 6b 6c 7 8 9 10 11 14 15 19 21 23)

failures=0
tests=0

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

pass() {
  echo "PASS: $*"
}

require_pattern() {
  local name="$1"
  local file="$2"
  local pattern="$3"
  tests=$((tests + 1))
  if [[ ! -f "$file" ]]; then
    fail "$name — missing file $file"
    return
  fi
  if grep -qi "$pattern" "$file"; then
    pass "$name"
  else
    fail "$name — pattern not in $(basename "$file"): $pattern"
  fi
}

echo "== Behavioral contract anchors (SKILL + templates) =="

# Scenario 1 — level pick L2 vs L3 (export CSV)
require_pattern "#1 do not auto-lock" "$SKILL" "do not auto-lock"
require_pattern "#1 Level picker one rule" "$SKILL" "Level picker (one rule)"
require_pattern "#1 exactly two adjacent" "$SKILL" "Exactly two"
require_pattern "#1 export gray" "$GRAY" "users/export"
require_pattern "#1 gray heavier" "$GRAY" "heavier"

# Scenario 4 — escalation L2→L3
require_pattern "#4 escalation in SKILL" "$SKILL" "Escalation"
require_pattern "#4 re-present in SKILL" "$SKILL" "re-present"
require_pattern "#4 exceeds in SKILL" "$SKILL" "exceeds"
require_pattern "#4 gray Escalate" "$GRAY" "Escalate"
require_pattern "#4 l2 level check stop" "$L2_PATCH" "stop"
require_pattern "#4 l2 vs L3" "$L2_PATCH" "L2 vs L3"

# Scenario 4b — escalation L3→L4
require_pattern "#4b L3 vs L4 gray" "$GRAY" "L3 vs L4"
require_pattern "#4b l3 define stop" "$L3_DEFINE" "stop"
require_pattern "#4b Need L4" "$L3_DEFINE" "Need \*\*L4\*\*"

# Scenario 6 — sticky scope L2
require_pattern "#6 sticky in SKILL" "$SKILL" "Sticky scope"
require_pattern "#6 until done" "$SKILL" "until done"
require_pattern "#6 level-picker sticky" "$LEVEL_PICKER" "Do not re-ask level every turn"

# Scenario 7 — gray zone
require_pattern "#7 two-option in SKILL" "$SKILL" "two-option"
require_pattern "#7 STOP after options" "$SKILL" "STOP"
require_pattern "#7 no heavier default gray" "$GRAY" "heavier"
require_pattern "#7 AskQuestion gray" "$GRAY" "AskQuestion"

# Scenario 8 — opt-out
require_pattern "#8 Opt-out wins" "$SKILL" "Opt-out wins"
require_pattern "#8 Conflicting tokens" "$SKILL" "Conflicting tokens"

# Scenario 9 / 10 — legacy triggers off
require_pattern "#9 ? keyword in SKILL" "$SKILL" '?` + keyword'
require_pattern "#10 level Lx in SKILL" "$SKILL" "level L1"

# Scenario 11 — mid-sentence
require_pattern "#11 Mid-sentence in SKILL" "$SKILL" "Mid-sentence"
require_pattern "#11 start or end placement" "$SKILL" "message start or end"

# Scenario 14 — glued L
require_pattern "#14 glued hint SKILL" "$SKILL" "Detected /question-scopeL2"
require_pattern "#14 glued hint rule" "$RULE" "Detected /question-scopeL2"
require_pattern "#14 glued hint SKILL" "$SKILL" "Detected /question-scopeL2"
require_pattern "#14 glued parsing row" "$SKILL" "/question-scopeL1"

# Scenario 15 / 19 / 21 — meta
require_pattern "#15 Meta discussion" "$SKILL" "Meta discussion"
require_pattern "#19 đánh giá question-scope" "$SKILL" "đánh giá question-scope"
require_pattern "#21 Meta wins" "$SKILL" "Meta wins"

require_pattern "#23 qs:meta in SKILL" "$SKILL" "qs:meta"
require_pattern "#23 explicit audit tokens" "$SKILL" "Explicit audit tokens"

echo ""
echo "== Behavioral eval tooling =="

tests=$((tests + 1))
if [[ -x "$ROOT/scripts/run-question-scope-behavioral-eval.sh" ]]; then
  pass "run-question-scope-behavioral-eval.sh exists and is executable"
else
  fail "missing or non-executable scripts/run-question-scope-behavioral-eval.sh"
fi

tests=$((tests + 1))
if [[ -f "$ROOT/scripts/hint-question-scope-behavioral-eval.sh" ]]; then
  pass "hint-question-scope-behavioral-eval.sh exists"
else
  fail "missing scripts/hint-question-scope-behavioral-eval.sh"
fi

require_pattern "PR checklist" "$ROOT/skills/question-scope/references/behavioral-gates.md" "PR / contract-change checklist"
require_pattern "behavioral eval log" "$SCENARIOS" "Behavioral eval log"

echo ""
echo "== Behavioral eval fixtures =="

tests=$((tests + 1))
if [[ -f "$FIXTURES" ]]; then
  pass "behavioral-eval-fixtures.json exists"
else
  fail "missing $FIXTURES"
fi

for id in "${BEHAVIORAL_IDS[@]}"; do
  tests=$((tests + 1))
  if grep -q "\"id\": \"${id}\"" "$FIXTURES" 2>/dev/null; then
    pass "fixture includes scenario id ${id}"
  else
    fail "fixture missing scenario id ${id}"
  fi
done

tests=$((tests + 1))
if grep -q '"schema": "question-scope-behavioral-eval/v2"' "$FIXTURES"; then
  pass "fixtures schema v2"
else
  fail "fixtures missing or wrong schema (expected question-scope-behavioral-eval/v2)"
fi

tests=$((tests + 1))
if grep -q '"turns"' "$FIXTURES" && grep -q 'escalation_l2_to_l3' "$FIXTURES"; then
  pass "fixtures document manual eval turns"
else
  fail "fixtures missing turns for manual eval"
fi

tests=$((tests + 1))
  if grep -q 'Fixtures \*\*1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23\*\*' "$SCENARIOS"; then
  pass "pressure-scenarios lists behavioral fixture ids"
else
  fail "pressure-scenarios missing behavioral fixture id list"
fi

tests=$((tests + 1))
if [[ -f "$ROOT/skills/question-scope/references/behavioral-gates.md" ]]; then
  pass "behavioral-gates.md exists"
else
  fail "missing references/behavioral-gates.md"
fi

GATES_MD="$ROOT/skills/question-scope/references/behavioral-gates.md"
require_pattern "#7 fixture two options only" "$FIXTURES" "Exactly two options only"
require_pattern "#1 fixture L2 vs L3 export" "$FIXTURES" "L2 vs L3"
tests=$((tests + 1))
if grep -qE 'OR four options|four options —' "$FIXTURES" 2>/dev/null; then
  fail "fixture #1/#7 must not allow OR four options fallback"
else
  pass "fixtures #1/#7 have no OR four options ambiguity"
fi

require_pattern "behavioral-gates fixture 6b" "$GATES_MD" "6b"
require_pattern "behavioral-gates fixture 6c" "$GATES_MD" "6c"
require_pattern "behavioral-gates fixtures json" "$GATES_MD" "behavioral-eval-fixtures.json"
require_pattern "behavioral-gates gates table" "$GATES_MD" "## Gates"
require_pattern "pressure-scenarios behavioral section" "$SCENARIOS" "## Behavioral (multi-turn)"

tests=$((tests + 1))
if grep -q '"id": "21"' "$FIXTURES" 2>/dev/null; then
  pass "behavioral-eval-fixtures includes meta scenario 21"
else
  fail "behavioral-eval-fixtures missing scenario 21"
fi

echo ""
echo "Note: make verify is the default gate. Optional LLM spot-check (#1, #6, #8/#21): behavioral-gates.md."
echo ""
echo "Ran $tests checks; failures: $failures"
if [[ "$failures" -gt 0 ]]; then
  exit 1
fi
echo "All question-scope behavioral contract checks passed."
