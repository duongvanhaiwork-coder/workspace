#!/usr/bin/env bash
# Contract tests for question-scope trigger parsing (SKILL.md § Parsing, Meta).
# Run: ./scripts/verify-question-scope-triggers.sh
# Wired from: ./scripts/verify.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/skills/question-scope/SKILL.md"
RULE="$ROOT/rules/cursor/question-scope.mdc"
README_HUMAN="$ROOT/skills/question-scope/README.md"
SCENARIOS="$ROOT/skills/question-scope/references/pressure-scenarios.md"
CURSOR_RULE="${CURSOR_RULES:-$HOME/.cursor/rules}/question-scope.mdc"

failures=0
tests=0

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

# Legacy always-on rule: had section "## Triggers (skill runs)".
qs_rule_is_legacy() {
  local f="$1"
  grep -qE '^## Triggers \(skill runs\)' "$f" 2>/dev/null
}

pass() {
  echo "PASS: $*"
}

assert_eq() {
  local name="$1" expected="$2" actual="$3"
  tests=$((tests + 1))
  if [[ "$expected" == "$actual" ]]; then
    pass "$name"
  else
    fail "$name (expected=$expected actual=$actual)"
  fi
}

# --- Parsing helpers (mirror SKILL.md) ---

qs_trim() {
  local msg="$1"
  local trimmed
  trimmed="$(printf '%s' "$msg" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  printf '%s' "$trimmed"
}

# /question-scope command only at message start or end (after trim), not mid-sentence.
qs_at_start() {
  local trimmed="$1"
  [[ "$trimmed" =~ ^/question-scope ]]
}

qs_at_end() {
  local trimmed="$1"
  [[ "$trimmed" =~ /question-scope[[:space:]]*$ ]] \
    || [[ "$trimmed" =~ /question-scope[[:space:]]+[Ll][1-4][[:space:]]*$ ]] \
    || [[ "$trimmed" =~ /question-scope[Ll][1-4][[:space:]]*$ ]]
}

qs_has_boundary() {
  local msg="$1"
  local trimmed
  trimmed="$(qs_trim "$msg")"
  qs_at_start "$trimmed" || qs_at_end "$trimmed"
}

qs_has_preset_level() {
  local msg="$1"
  local trimmed
  trimmed="$(qs_trim "$msg")"
  if [[ "$trimmed" =~ ^/question-scope[[:space:]]+[Ll][1-4]([^0-9]|$) ]]; then
    return 0
  fi
  if [[ "$trimmed" =~ /question-scope[[:space:]]+[Ll][1-4]([^0-9]|$)[[:space:]]*$ ]]; then
    return 0
  fi
  return 1
}

qs_preset_level_label() {
  local msg="$1"
  local trimmed
  trimmed="$(qs_trim "$msg")"
  if [[ "$trimmed" =~ ^/question-scope[[:space:]]+[Ll]([1-4])([^0-9]|$) ]]; then
    echo "preset:L${BASH_REMATCH[1]}"
    return 0
  fi
  if [[ "$trimmed" =~ /question-scope[[:space:]]+[Ll]([1-4])([^0-9]|$)[[:space:]]*$ ]]; then
    echo "preset:L${BASH_REMATCH[1]}"
    return 0
  fi
  return 1
}

qs_has_glued_level() {
  local msg="$1"
  local trimmed
  trimmed="$(qs_trim "$msg")"
  if [[ "$trimmed" =~ ^/question-scope[Ll][1-4] ]]; then
    return 0
  fi
  if [[ "$trimmed" =~ /question-scope[Ll][1-4]([^0-9a-zA-Z]|$)[[:space:]]*$ ]]; then
    return 0
  fi
  return 1
}

qs_has_token() {
  local msg="$1"
  qs_has_boundary "$msg"
}

qs_scope_opt_out() {
  local msg="$1"
  local lower
  lower="$(printf '%s' "$msg" | tr '[:upper:]' '[:lower:]')"
  if [[ "$lower" =~ ^quick: ]]; then
    return 0
  fi
  if [[ "$lower" =~ (^|[[:space:]])quick: ]]; then
    return 0
  fi
  if [[ "$lower" =~ (^|[[:space:]])(qs:off|no-scope)([^a-z0-9_-]|$) ]]; then
    return 0
  fi
  if [[ "$lower" =~ ^qs:meta ]]; then
    return 0
  fi
  if [[ "$lower" =~ (^|[[:space:]])qs:meta([^a-z0-9_-]|$) ]]; then
    return 0
  fi
  if [[ "$lower" =~ ^audit: ]]; then
    return 0
  fi
  if [[ "$lower" =~ (^|[[:space:]])audit: ]]; then
    return 0
  fi
  return 1
}

qs_is_legacy_question_trigger() {
  local msg="$1"
  [[ "$msg" =~ (^|[[:space:]])\?[[:space:]]*[a-zA-Z] ]]
}

qs_is_meta_audit() {
  local msg="$1"
  local lower
  lower="$(printf '%s' "$msg" | tr '[:upper:]' '[:lower:]')"
  if [[ "$lower" == *"skills/question-scope"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"question-scope/skill.md"* ]] || [[ "$lower" == *"question-scope.mdc"* ]]; then
    return 0
  fi
  if [[ "$lower" =~ (^|[[:space:]/])question-scope/ ]]; then
    return 0
  fi
  if [[ "$lower" == *"check question-scope"* ]] || [[ "$lower" == *"question-scope rules"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"đánh giá skill"* ]] || [[ "$lower" == *"danh gia skill"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"đánh giá question-scope"* ]] || [[ "$lower" == *"danh gia question-scope"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"đánh giá rule"* ]] || [[ "$lower" == *"danh gia rule"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"kiểm tra lại rule"* ]] || [[ "$lower" == *"kiem tra lai rule"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"kiểm tra lại về rule"* ]] || [[ "$lower" == *"kiem tra lai ve rule"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"kiểm tra rule question-scope"* ]] || [[ "$lower" == *"kiem tra rule question-scope"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"rà soát skill"* ]] || [[ "$lower" == *"ra soat skill"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"don't use /question-scope"* ]] || [[ "$lower" == *"dont use /question-scope"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"when does /question-scope apply"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"discussing /question-scope"* ]] || [[ "$lower" == *"without intent to run"* ]]; then
    return 0
  fi
  if [[ "$lower" == *"as an example"* ]] && qs_has_boundary "$msg"; then
    return 0
  fi
  if [[ "$lower" == *"when teaching"* ]] && qs_has_boundary "$msg"; then
    return 0
  fi
  return 1
}

# scope_active: should question-scope pipeline run?
# Returns: inactive | preset:L1..L4 | needs_pick
qs_classify() {
  local msg="$1"
  local preset
  if qs_scope_opt_out "$msg"; then
    echo "inactive"
    return
  fi
  if qs_is_meta_audit "$msg"; then
    echo "inactive"
    return
  fi
  if qs_has_preset_level "$msg"; then
    preset="$(qs_preset_level_label "$msg")"
    echo "$preset"
    return
  fi
  if qs_has_token "$msg"; then
    echo "needs_pick"
    return
  fi
  if [[ "$msg" =~ (^|[[:space:]])level[[:space:]]+[Ll][1-4] ]]; then
    echo "inactive"
    return
  fi
  if qs_is_legacy_question_trigger "$msg"; then
    echo "inactive"
    return
  fi
  if [[ "$msg" =~ \?[[:space:]]*$ ]]; then
    echo "inactive"
    return
  fi
  echo "inactive"
}

run_message_fixtures() {
  echo "== Message fixtures (pressure-scenarios) =="
  assert_eq "#1 needs pick" "needs_pick" "$(qs_classify '/question-scope Add GET /users/export CSV')"
  assert_eq "#2 no token" "inactive" "$(qs_classify 'I already fixed the handler, can we deploy now?')"
  assert_eq "#3 quick:" "inactive" "$(qs_classify 'quick: fix typo in README')"
  assert_eq "#5 L3 + sp:off" "preset:L3" "$(qs_classify '/question-scope L3 — feature. sp:off')"
  assert_eq "#8 opt-out beats Lx" "inactive" "$(qs_classify '/question-scope L2 — fix X. quick:')"
  assert_eq "#8b qs:off beats Lx" "inactive" "$(qs_classify 'qs:off /question-scope L3 — feature')"
  assert_eq "#8c no-scope alone" "inactive" "$(qs_classify 'no-scope — explain auth flow')"
  assert_eq "#8d qs:off alone" "inactive" "$(qs_classify 'qs:off — patch login')"
  assert_eq "#9 ?explain" "inactive" "$(qs_classify '?explain')"
  assert_eq "#9b ?fix api" "inactive" "$(qs_classify '?fix api timeout')"
  assert_eq "#9c fix something?" "inactive" "$(qs_classify 'fix something?')"
  assert_eq "#10 level L2 alone" "inactive" "$(qs_classify 'level L2 — fix X')"
  assert_eq "#11 mid-sentence no trigger" "inactive" "$(qs_classify 'Please /question-scope fix auth')"
  assert_eq "#11b end placement preset" "preset:L2" "$(qs_classify 'fix auth /question-scope L2')"
  assert_eq "#11c end placement needs pick" "needs_pick" "$(qs_classify 'Add export CSV /question-scope')"
  assert_eq "#12 lowercase l2" "preset:L2" "$(qs_classify '/question-scope l2 — fix')"
  assert_eq "#12b preset L1" "preset:L1" "$(qs_classify '/question-scope L1 — what is JWT?')"
  assert_eq "#12c preset L4" "preset:L4" "$(qs_classify '/question-scope L4 — platform migration')"
  assert_eq "#14 glued L" "needs_pick" "$(qs_classify '/question-scopeL2 — fix X')"
  assert_eq "#15 meta audit path" "inactive" "$(qs_classify 'Kiểm tra skills/question-scope')"
  assert_eq "#15b meta VI no path" "inactive" "$(qs_classify 'Kiểm tra lại rule question-scope')"
  assert_eq "#15c meta đánh giá" "inactive" "$(qs_classify 'Đánh giá question-scope giúp tôi')"
  assert_eq "#15d meta ve rule" "inactive" "$(qs_classify 'Kiểm tra lại về rule question-scope')"
  assert_eq "#15e meta token+audit" "inactive" "$(qs_classify '/question-scope — kiểm tra lại về rule skills/question-scope')"
  assert_eq "#16 meta quote mid-sentence" "inactive" "$(qs_classify 'When teaching, say Please /question-scope fix auth as an example')"
  assert_eq "sp:off alone" "inactive" "$(qs_classify 'sp:off — fix auth')"
  assert_eq "preset L3" "preset:L3" "$(qs_classify '/question-scope L3 — feature')"
  assert_eq "quick: mid-message" "inactive" "$(qs_classify 'Ship it. quick: typo only')"
  assert_eq "#23 qs:meta" "inactive" "$(qs_classify 'qs:meta — review question-scope rules')"
  assert_eq "#23b qs:meta beats Lx" "inactive" "$(qs_classify '/question-scope L2 — fix X. qs:meta — audit only')"
  assert_eq "#24 audit:" "inactive" "$(qs_classify 'audit: đánh giá skills/question-scope')"
}

check_readme_human() {
  echo "== README.md (human guide) =="
  local phrases=(
    'No longer supported'
    'Light patch'
    'start or end'
    'qs:meta'
    'Rollup MD OK'
    'Common workflow preset Lx only'
  )
  for p in "${phrases[@]}"; do
    tests=$((tests + 1))
    if grep -qF "$p" "$README_HUMAN" 2>/dev/null; then
      pass "README contains: $p"
    else
      fail "README.md missing phrase: $p"
    fi
  done
  tests=$((tests + 1))
  if grep -q 'quick:` but want L2' "$README_HUMAN" 2>/dev/null; then
    pass "README anti-pattern: quick vs Light patch"
  else
    fail "README missing anti-pattern quick vs Light patch"
  fi
}

check_repo_docs() {
  echo "== Repo doc consistency =="

  local qs_rule_tag qs_skill_tag
  qs_rule_tag="$(grep -oE 'qs-[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+' "$RULE" 2>/dev/null | head -1)"
  qs_skill_tag="$(grep -oE 'qs-[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+' "$SKILL" 2>/dev/null | head -1)"
  tests=$((tests + 1))
  if [[ -n "$qs_rule_tag" && "$qs_rule_tag" == "$qs_skill_tag" ]]; then
    pass "contract tag synced in SKILL + rule ($qs_rule_tag)"
  else
    fail "contract tag mismatch — rule=$qs_rule_tag skill=$qs_skill_tag"
  fi
  tests=$((tests + 1))
  if [[ -f "$ROOT/scripts/check-question-scope-session.sh" ]]; then
    pass "check-question-scope-session.sh exists"
  else
    fail "missing scripts/check-question-scope-session.sh"
  fi

  tests=$((tests + 1))
  if ! grep -q 'questionScopeContract' "$RULE" 2>/dev/null; then
    pass "rule has no questionScopeContract frontmatter"
  else
    fail "rule still has questionScopeContract frontmatter"
  fi

  tests=$((tests + 1))
  if grep -q 'Detected /question-scopeL2' "$SKILL" && grep -q 'Detected /question-scopeL2' "$RULE"; then
    pass "glued-L user hint in rule + SKILL"
  else
    fail "glued-L user hint missing in rule or SKILL"
  fi

  tests=$((tests + 1))
  if grep -q 'level Lx' "$RULE" && grep -q '?.*keyword do not' "$RULE"; then
    pass "rule documents level Lx and ? do not activate"
  else
    fail "rule missing 'level Lx and ? do not activate'"
  fi

  tests=$((tests + 1))
  if qs_rule_is_legacy "$RULE"; then
    fail "rule still has legacy '## Triggers (skill runs)' section"
  else
    pass "rule has no legacy Triggers section"
  fi

  tests=$((tests + 1))
  if grep -q 'kiểm tra lại về rule' "$SKILL"; then
    pass "SKILL meta: kiểm tra lại về rule"
  else
    fail "SKILL missing meta phrase kiểm tra lại về rule"
  fi

  tests=$((tests + 1))
  if grep -q 'discussing.*without intent to run' "$SKILL"; then
    pass "SKILL meta: discuss without run intent"
  else
    fail "SKILL missing meta: discuss without run intent"
  fi

  tests=$((tests + 1))
  if grep -q '| 21 |' "$SCENARIOS" && grep -q '| 22 |' "$SCENARIOS" && grep -q '| 23 |' "$SCENARIOS"; then
    pass "pressure-scenarios includes scenario 21+22+23"
  else
    fail "pressure-scenarios missing scenario 21, 22, or 23"
  fi

  tests=$((tests + 1))
  if grep -q '### Level picker (one rule)' "$SKILL"; then
    pass "SKILL has unified Level picker section"
  else
    fail "SKILL missing ### Level picker (one rule)"
  fi

  tests=$((tests + 1))
  if grep -q 'qs:meta' "$SKILL" && grep -q 'audit:' "$SKILL"; then
    pass "SKILL documents qs:meta and audit:"
  else
    fail "SKILL missing qs:meta or audit: tokens"
  fi

  tests=$((tests + 1))
  if grep -q 'quick:' "$SKILL" && grep -q 'Light patch' "$SKILL" && grep -q 'rollup' "$SKILL"; then
    pass "SKILL clarifies quick: vs L2 rollup"
  else
    fail "SKILL missing quick: vs L2 rollup clarification"
  fi

  tests=$((tests + 1))
  if grep -q 'Escalation' "$SKILL" && grep -q 'Sticky scope' "$SKILL" && grep -q 'Gray zone' "$SKILL"; then
    pass "SKILL documents escalation, sticky, gray (behavioral #4 #6 #7)"
  else
    fail "SKILL missing escalation/sticky/gray gates for behavioral scenarios"
  fi

  tests=$((tests + 1))
  if grep -q 'start or end' "$SKILL" && grep -q 'start or end' "$RULE"; then
    pass "SKILL + rule document start/end placement"
  else
    fail "SKILL or rule missing start/end placement for /question-scope"
  fi
}

check_cursor_rule_link() {
  echo "== Installed Cursor rule (~/.cursor/rules) =="
  tests=$((tests + 1))
  if [[ ! -e "$CURSOR_RULE" ]]; then
    fail "missing $CURSOR_RULE — sync IDE rules from repo"
    return
  fi
  if [[ "$(readlink -f "$CURSOR_RULE" 2>/dev/null || realpath "$CURSOR_RULE" 2>/dev/null || echo "")" == "$(readlink -f "$RULE" 2>/dev/null || realpath "$RULE")" ]]; then
    pass "~/.cursor/rules/question-scope.mdc resolves to repo rule"
  elif cmp -s "$CURSOR_RULE" "$RULE" 2>/dev/null; then
    pass "~/.cursor/rules/question-scope.mdc matches repo rule"
  else
    fail "~/.cursor/rules/question-scope.mdc differs from $RULE — sync IDE rules from repo"
  fi

  tests=$((tests + 1))
  if qs_rule_is_legacy "$CURSOR_RULE"; then
    fail "installed rule has legacy ## Triggers (skill runs) — sync + reload Cursor"
  else
    pass "installed rule has no legacy Triggers section"
  fi

  tests=$((tests + 1))
  if ! grep -q 'questionScopeContract' "$CURSOR_RULE" 2>/dev/null; then
    pass "installed rule has no questionScopeContract"
  else
    fail "installed rule still has questionScopeContract — sync IDE rules + reload chat"
  fi
}

run_message_fixtures
check_repo_docs
check_readme_human
check_cursor_rule_link

echo ""
echo "Note: behavioral fixtures 1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23 are agent gates (not qs_classify)."
echo ""
echo "Ran $tests checks; failures: $failures"
if [[ "$failures" -gt 0 ]]; then
  exit 1
fi
echo "All question-scope trigger checks passed."
