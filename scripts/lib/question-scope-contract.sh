#!/usr/bin/env bash
# Shared grep helpers: question-scope contract spans SKILL + key references (P3 split).
# Source from verify-question-scope-*.sh after ROOT is set.

qs_contract_files() {
  QS_CONTRACT_FILES=(
    "$ROOT/skills/question-scope/SKILL.md"
    "$ROOT/skills/question-scope/references/parsing-tokens.md"
    "$ROOT/skills/question-scope/references/level-picker-runtime.md"
    "$ROOT/skills/question-scope/references/pipelines-skill-map.md"
    "$ROOT/skills/question-scope/references/CHEATSHEET.md"
    "$ROOT/skills/question-scope/references/playbooks.md"
  )
}

# grep -E pattern across contract files
qs_contract_grep() {
  local pattern="$1"
  local f
  qs_contract_files
  for f in "${QS_CONTRACT_FILES[@]}"; do
    [[ -f "$f" ]] || continue
    if grep -qE "$pattern" "$f" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}

# grep -E pattern across any listed files (remaining args)
qs_grep_any() {
  local pattern="$1"
  shift
  local f
  for f in "$@"; do
    [[ -f "$f" ]] || continue
    if grep -qE "$pattern" "$f" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}
