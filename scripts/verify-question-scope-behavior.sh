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
ARCH_PLAN="$ROOT/skills/architect-plan/SKILL.md"
WRITING_PLANS="$ROOT/skills/writing-plans/SKILL.md"
EXEC_PLANS="$ROOT/skills/executing-plans/SKILL.md"
SUBAGENT_DEV="$ROOT/skills/subagent-driven-development/SKILL.md"
VERIFY_SKILL="$ROOT/skills/verification-before-completion/SKILL.md"
FINISH_BRANCH="$ROOT/skills/finishing-a-development-branch/SKILL.md"
L3_SHIP="$ROOT/skills/question-scope/templates/phases/l3/l3-03-ship.md"
L4_DISCOVER="$ROOT/skills/question-scope/templates/phases/l4/l4-01-discover.md"
ANALYZE_IMPACT="$ROOT/skills/analyze-impact/SKILL.md"
REQ_REVIEW="$ROOT/skills/requesting-code-review/SKILL.md"
TDD="$ROOT/skills/test-driven-development/SKILL.md"
PLAYBOOKS="$ROOT/skills/question-scope/references/playbooks.md"
L4_PROVE="$ROOT/skills/question-scope/templates/phases/l4/l4-04-prove.md"
RECEIVING_REVIEW="$ROOT/skills/receiving-code-review/SKILL.md"
L3_PROVE="$ROOT/skills/question-scope/templates/phases/l3/l3-02-build-prove.md"

BEHAVIORAL_IDS=(1 4 4b 6 6b 6c 7 8 9 10 11 14 15 19 21 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42)

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
require_pattern "#7 option copy in SKILL" "$SKILL" "Option copy (required)"
require_pattern "#7 option copy canonical" "$LEVEL_PICKER" "Option copy (required"
require_pattern "#7 AskQuestion label" "$LEVEL_PICKER" "AskQuestion"

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
  if grep -q 'Fixtures \*\*1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42\*\*' "$SCENARIOS"; then
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

# Scenario 24 — L3 bounded → architect-plan, not writing-plans
require_pattern "#24 pre-flight architect" "$ARCH_PLAN" "NEXT: \`writing-plans\`"
require_pattern "#24 writing-plans STOP architect" "$WRITING_PLANS" "architect-plan"
require_pattern "#24 fixture no docs/plans" "$FIXTURES" "does not create docs/plans"
require_pattern "#24 fixture l3_bounded" "$FIXTURES" "l3_bounded_no_writing_plans"

# Scenario 25 — L2 rename → no new TDD
require_pattern "#25 TDD When NOT rename" "$TDD" "When NOT"
require_pattern "#25 TDD rename red flag" "$TDD" "rename/move/format"
require_pattern "#25 playbook pure refactor" "$PLAYBOOKS" "Pure refactor"
require_pattern "#25 fixture l2_rename" "$FIXTURES" "l2_rename_no_new_tdd"

GEN_TEST="$ROOT/skills/generate-test/SKILL.md"
L3_BUILD="$ROOT/skills/question-scope/templates/phases/l3/l3-02-build-prove.md"
L4_BUILD="$ROOT/skills/question-scope/templates/phases/l4/l4-03-build.md"

# Scenario 26 — L3 Test gate before Code
require_pattern "#26 generate-test L3 gate" "$GEN_TEST" "Do not skip the TC table gate"
require_pattern "#26 l3-02 STOP generate-test" "$L3_BUILD" "STOP without this table filled"
require_pattern "#26 fixture l3_test_gate" "$FIXTURES" "l3_test_gate_before_code"

# Scenario 27 — generate-test RED, no prod in Test phase
require_pattern "#27 generate-test RED gate" "$GEN_TEST" "RED gate"
require_pattern "#27 generate-test no prod" "$GEN_TEST" "Implement production code"
require_pattern "#27 TDD generate-test defer" "$TDD" "must not implement production"
require_pattern "#27 fixture generate_test_red" "$FIXTURES" "generate_test_red_no_prod"

# L4 template names generate-test
require_pattern "l4-03 generate-test" "$L4_BUILD" "generate-test"

# Scenario 28 — bounded L3 → executing-plans B
require_pattern "#28 executing-plans default" "$EXEC_PLANS" "default"
require_pattern "#28 executing-plans architect-plan" "$EXEC_PLANS" "architect-plan"
require_pattern "#28 subagent architect-plan only" "$SUBAGENT_DEV" "architect-plan"
require_pattern "#28 fixture l3_bounded_execute_b" "$FIXTURES" "l3_bounded_execute_b_not_subagent"

# Scenario 29 — docs/plans does not auto-select A
require_pattern "#29 executing-plans no auto A" "$EXEC_PLANS" "auto-select A"
require_pattern "#29 writing-plans executing-plans default" "$WRITING_PLANS" "executing-plans"
require_pattern "#29 fixture docs_plans_execute_b" "$FIXTURES" "docs_plans_still_allows_execute_b"

# l3-02 implementation execute handoff
require_pattern "l3-02 executing-plans" "$L3_BUILD" "executing-plans"

# L3 pipeline includes Regression step
require_pattern "L3 supplement Regression" "$SKILL" "Regression"
require_pattern "verify skill phase Regression" "$VERIFY_SKILL" "Phase Regression"

# Scenario 30 — no done without fresh verify
require_pattern "#30 verify Iron Law" "$VERIFY_SKILL" "NO COMPLETION CLAIMS"
require_pattern "#30 fixture no_done_claim" "$FIXTURES" "no_done_claim_without_fresh_verify"

# Scenario 31 — RED test design + phase log
require_pattern "#31 verify RED expected" "$VERIFY_SKILL" "RED as expected"
require_pattern "#31 l3-02 test design log" "$L3_BUILD" "Test design — command log"
require_pattern "#31 l3-02 verify regression skill" "$L3_BUILD" "verification-before-completion"
require_pattern "#31 fixture l3_verify_red" "$FIXTURES" "l3_verify_log_and_red_test_design"

# l2/l4 templates + finishing fresh verify
require_pattern "l2-patch verify skill" "$L2_PATCH" "verification-before-completion"
require_pattern "l4-04 prove verify skill" "$L4_PROVE" "verification-before-completion"
require_pattern "finishing fresh verify" "$FINISH_BRANCH" "verification-before-completion"

# Scenario 32–34 — Ship
require_pattern "#32 finishing tests fail" "$FINISH_BRANCH" "Cannot proceed"
require_pattern "#32 fixture ship_no_merge" "$FIXTURES" "ship_no_merge_when_tests_fail"

require_pattern "#33 finishing PR worktree" "$FINISH_BRANCH" "Do NOT clean up worktree"
require_pattern "#33 fixture ship_pr_worktree" "$FIXTURES" "ship_pr_keeps_worktree"

require_pattern "#34 executing not Ship yet" "$EXEC_PLANS" "not Ship yet"
require_pattern "#34 finishing l3-03" "$FINISH_BRANCH" "l3-03-ship"
require_pattern "#34 fixture execute_not_skip_ship" "$FIXTURES" "execute_done_not_skip_l3_03_ship"

require_pattern "l3-03 ship order" "$L3_SHIP" "finishing-a-development-branch"
require_pattern "executing NEXT ship phase" "$EXEC_PLANS" "l3-03-ship"

# Scenario 35–37 — analyze-impact / L4 Regression
require_pattern "#35 analyze-impact l4-01" "$ANALYZE_IMPACT" "l4-01-discover"
require_pattern "#35 l4-01 analyze-impact section" "$L4_DISCOVER" "analyze-impact / exploration"
require_pattern "#35 fixture l4_discover" "$FIXTURES" "l4_discover_analyze_impact"

require_pattern "#36 SKILL impacted service" "$SKILL" "impacted service"
require_pattern "#36 l4-04 l4-01 link" "$L4_PROVE" "l4-01"
require_pattern "#36 fixture l4_regression" "$FIXTURES" "l4_regression_per_service_not_monorepo"

require_pattern "#37 analyze search-based" "$ANALYZE_IMPACT" "search-based"
require_pattern "#37 analyze not graph-complete" "$ANALYZE_IMPACT" "not graph-complete"
require_pattern "#37 fixture analyze_fallback" "$FIXTURES" "analyze_impact_search_fallback_honest"

require_pattern "question-scope Impact analysis row" "$SKILL" "Impact analysis"
require_pattern "analyze-impact not Regression" "$ANALYZE_IMPACT" "replace Regression"

# Scenario 38–40 — requesting-code-review
require_pattern "#38 requesting caveman L4" "$REQ_REVIEW" "caveman-review"
require_pattern "#38 supplement review vs ship" "$ROOT/skills/question-scope/references/superpowers-supplement.md" "requesting-code-review"
require_pattern "#38 fixture l4_premerge" "$FIXTURES" "l4_premerge_requesting_code_review"

require_pattern "#39 requesting no duplicate subagent" "$REQ_REVIEW" "Do not use as duplicate"
require_pattern "#39 subagent not per task requesting" "$SUBAGENT_DEV" "not per task"
require_pattern "#39 fixture subagent_no_duplicate" "$FIXTURES" "subagent_a_no_duplicate_requesting_per_task"

require_pattern "#40 requesting Critical unfixed" "$REQ_REVIEW" "Proceed with unfixed"
require_pattern "#40 finishing Critical" "$FINISH_BRANCH" "Critical"
require_pattern "#40 fixture review_critical" "$FIXTURES" "review_critical_before_merge"

require_pattern "l4-04 prove caveman requesting" "$L4_PROVE" "requesting-code-review"
require_pattern "l4-05 pre-merge review section" "$ROOT/skills/question-scope/templates/phases/l4/l4-05-ship.md" "Pre-merge review"

# Scenario 41–42 — receiving-code-review (incoming PR)
require_pattern "question-scope Feedback PR row" "$SKILL" "receiving-code-review"
require_pattern "question-scope incoming rule" "$SKILL" "incoming-code-review"
require_pattern "#41 receiving With question-scope" "$RECEIVING_REVIEW" "incoming-code-review"
require_pattern "#41 receiving verify before" "$RECEIVING_REVIEW" "Verify before implementing"
require_pattern "#41 superpowers incoming" "$ROOT/skills/superpowers/SKILL.md" "receiving-code-review"
require_pattern "#41 finishing PR iteration" "$FINISH_BRANCH" "receiving-code-review"
require_pattern "#41 l3 PR feedback section" "$L3_PROVE" "PR feedback"
require_pattern "#41 l4 PR feedback section" "$L4_PROVE" "receiving-code-review"
require_pattern "#41 playbooks PR feedback" "$PLAYBOOKS" "receiving-code-review"
require_pattern "#41 fixture incoming_verify" "$FIXTURES" "incoming_pr_verify_before_implement"

require_pattern "#42 receiving Clarify All" "$RECEIVING_REVIEW" "Clarify All Items"
require_pattern "#42 receiving need clarification" "$RECEIVING_REVIEW" "Need clarification"
require_pattern "#42 fixture incoming_clarify" "$FIXTURES" "incoming_pr_clarify_before_partial_fix"

echo ""
echo "Note: make verify is the default gate. Optional LLM spot-check (#1, #6, #8/#21, #24–#42): behavioral-gates.md."
echo ""
echo "Ran $tests checks; failures: $failures"
if [[ "$failures" -gt 0 ]]; then
  exit 1
fi
echo "All question-scope behavioral contract checks passed."
