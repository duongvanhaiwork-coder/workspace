#!/usr/bin/env bash
# Per-skill structural audit: frontmatter, invocation modes, links, prompts.
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

echo "== Per-skill audit (26 skills) =="

SKILLS_ROOT="$SKILLS" python3 <<'PY'
import os, re, sys
from pathlib import Path

skills_root = Path(os.environ["SKILLS_ROOT"])
skill_ids = sorted(
    p.name for p in skills_root.iterdir()
    if p.is_dir() and p.name != "references" and (p / "SKILL.md").is_file()
)
registry = set(skill_ids)
issues = {}

for skill_id in skill_ids:
    skill_dir = skills_root / skill_id
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    errs = []

    m = re.search(r"^name:\s*(\S+)\s*$", text, re.M)
    if not m or m.group(1) != skill_id:
        errs.append("frontmatter name mismatch or missing")

    for sec in ("## Invocation modes", "### Composition (quick ref)"):
        if sec not in text:
            errs.append(f"missing {sec}")

    if "invocation-anti-patterns" not in text and skill_id != "writing-skills":
        errs.append("missing invocation-anti-patterns link")

    if "COMPOSITION.md" not in text:
        errs.append("missing COMPOSITION.md")

    if skill_id != "writing-skills" and re.search(r"(?<![./])rules/(?:cursor/)?", text):
        errs.append("rules/ path in SKILL (use rule IDs)")

    for _, target in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text):
        if target.startswith(("http", "mailto", "#")):
            continue
        path_part = target.split("#")[0]
        if not path_part:
            continue
        if not (skill_dir / path_part).resolve().exists():
            errs.append(f"broken link: {target}")

    for pm in re.findall(r"prompts/([a-zA-Z0-9_.-]+\.md)", text):
        if not (skill_dir / "prompts" / pm).exists():
            if skill_id == "requesting-code-review" and pm in (
                "spec-reviewer-prompt.md",
                "code-quality-reviewer-prompt.md",
            ):
                continue  # documents subagent prompts, not local files
            errs.append(f"broken prompt: prompts/{pm}")

    if errs:
        issues[skill_id] = errs

for sid, errs in sorted(issues.items()):
    print(f"FAIL\t{sid}\t" + " | ".join(errs))
for sid in skill_ids:
    if sid not in issues:
        print(f"PASS\t{sid}")

sys.exit(1 if issues else 0)
PY

audit_status=$?
tests=$((tests + 26))
if [[ "$audit_status" -eq 0 ]]; then
  pass "all 26 skills structural audit"
else
  fail "structural audit reported failures (see above)"
  failures=$((failures + 1))
fi

echo ""
echo "Ran audit; failures: $failures"
exit "$failures"
