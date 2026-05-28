#!/usr/bin/env bash
# Enforce skills/STRUCTURE.md: SKILL.md required; root *.md only SKILL.md + README.md;
# YAML frontmatter name + description on every SKILL.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS="$ROOT/skills"

failures=0
tests=0

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

pass() {
  echo "PASS: $*"
}

echo "== Skills directory structure =="

if [[ ! -d "$SKILLS" ]]; then
  echo "FAIL: missing $SKILLS" >&2
  exit 1
fi

skill_count=0
while IFS= read -r -d '' skill_dir; do
  skill_id="$(basename "$skill_dir")"
  [[ "$skill_id" == .* ]] && continue
  skill_count=$((skill_count + 1))

  tests=$((tests + 1))
  skill_md="$skill_dir/SKILL.md"
  if [[ ! -f "$skill_md" ]]; then
    fail "$skill_id — missing SKILL.md"
    continue
  fi
  pass "$skill_id — SKILL.md exists"

  while IFS= read -r -d '' stray; do
    tests=$((tests + 1))
    fail "$skill_id — stray root markdown: $(basename "$stray") (move under references/, examples/, …)"
  done < <(find "$skill_dir" -mindepth 1 -maxdepth 1 -type f -name '*.md' \
    ! -name 'SKILL.md' ! -name 'README.md' -print0 2>/dev/null)

  tests=$((tests + 1))
  if head -1 "$skill_md" | grep -q '^---$'; then
    pass "$skill_id — frontmatter opener"
  else
    fail "$skill_id — SKILL.md missing opening ---"
    continue
  fi

  tests=$((tests + 1))
  if grep -qE '^name:' "$skill_md"; then
    pass "$skill_id — frontmatter name"
  else
    fail "$skill_id — SKILL.md missing name:"
  fi

  tests=$((tests + 1))
  if grep -qE '^description:' "$skill_md"; then
    pass "$skill_id — frontmatter description"
  else
    fail "$skill_id — SKILL.md missing description:"
  fi
done < <(find "$SKILLS" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

tests=$((tests + 1))
if [[ "$skill_count" -ge 26 ]]; then
  pass "skill count >= 26 ($skill_count dirs)"
else
  fail "expected >= 26 skill dirs, found $skill_count"
fi

tests=$((tests + 1))
if [[ -f "$SKILLS/question-scope/references/CHEATSHEET.md" ]]; then
  pass "question-scope references/CHEATSHEET.md"
else
  fail "question-scope references/CHEATSHEET.md missing"
fi

tests=$((tests + 1))
if [[ ! -f "$SKILLS/question-scope/CHEATSHEET.md" ]]; then
  pass "question-scope root CHEATSHEET.md removed"
else
  fail "question-scope/CHEATSHEET.md still at skill root — move to references/"
fi

echo ""
echo "Ran $tests checks; failures: $failures"
if [[ "$failures" -gt 0 ]]; then
  echo "Skills structure checks failed." >&2
  exit 1
fi
echo "All skills structure checks passed."
