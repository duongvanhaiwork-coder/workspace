#!/usr/bin/env bash
# Canonical: rules/cursor/<name>.mdc → rules/kiro/<name>.md (1:1 stems) → symlink ~/.cursor/rules + ~/.kiro/steering
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CURSOR_SRC="$ROOT/rules/cursor"
KIRO_SRC="$ROOT/rules/kiro"
CURSOR_DEST="${CURSOR_RULES:-$HOME/.cursor/rules}"
KIRO_DEST="${KIRO_STEERING:-$HOME/.kiro/steering}"

if [[ ! -d "$CURSOR_SRC" ]]; then
  echo "Error: $CURSOR_SRC not found — add .mdc files there."
  exit 1
fi

mkdir -p "$CURSOR_SRC" "$KIRO_SRC"

ROOT="$ROOT" python3 - <<'PY'
import os
from pathlib import Path

root = Path(os.environ["ROOT"])
cursor_src = root / "rules" / "cursor"
kiro_src = root / "rules" / "kiro"

KIRO_README = """# Kiro steering (generated)

**Do not edit files in this folder by hand.** They are regenerated from `rules/cursor/*.mdc` on every `make sync-ide`.

| Cursor (canonical) | Kiro (this folder) | `inclusion` |
| ------------------ | ------------------ | ----------- |
{rows}

Body text matches the Cursor rule; only frontmatter differs (`alwaysApply`/`globs` → `inclusion`/`fileMatchPattern`).

Edit **`rules/cursor/<name>.mdc`** only. See [../README.md](../README.md) and [../CONVENTIONS.md](../CONVENTIONS.md).
"""

CURSOR_README = """# Cursor rules (canonical)

Edit **`*.mdc` here only.** Kiro copies are generated under `../kiro/<same-stem>.md` by `make sync-ide`.

| File | `alwaysApply` | `globs` | Kiro output |
| ---- | ------------- | ------- | ----------- |
{rows}

Naming: **kebab-case** stem; same basename in `rules/kiro/` (`.md`). See [../CONVENTIONS.md](../CONVENTIONS.md).
"""


def parse_mdc(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    front: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    front[k.strip()] = v.strip()
            body = parts[2].lstrip("\n")
    return front, body


def kiro_inclusion_label(front: dict[str, str]) -> str:
    if front.get("alwaysApply", "false").lower() == "true":
        return "always"
    if front.get("globs"):
        return "fileMatch"
    return "manual"


mdc_files = sorted(cursor_src.glob("*.mdc"))
stems = {p.stem for p in mdc_files}
table_rows: list[tuple[str, str, str, str, str]] = []

for mdc in mdc_files:
    front, body = parse_mdc(mdc)
    inclusion = kiro_inclusion_label(front)
    kiro_lines: list[str] = []
    if inclusion == "always":
        kiro_lines.append("inclusion: always")
    elif inclusion == "fileMatch":
        raw = front["globs"].strip().strip('"').strip("'")
        patterns = [p.strip().strip('"').strip("'") for p in raw.split(",") if p.strip()]
        kiro_lines.append("inclusion: fileMatch")
        if len(patterns) == 1:
            kiro_lines.append(f'fileMatchPattern: "{patterns[0]}"')
        else:
            joined = ", ".join(f'"{p}"' for p in patterns)
            kiro_lines.append(f"fileMatchPattern: [{joined}]")
    else:
        kiro_lines.append("inclusion: manual")

    out = "---\n" + "\n".join(kiro_lines) + "\n---\n\n" + body
    out_path = kiro_src / f"{mdc.stem}.md"
    out_path.write_text(out, encoding="utf-8")
    print(f"  rules/cursor/{mdc.name} → rules/kiro/{out_path.name}")

    always = front.get("alwaysApply", "false")
    globs = front.get("globs", "—")
    table_rows.append((mdc.name, always, globs, f"{mdc.stem}.md", inclusion))

# Remove stale Kiro files (old rules-* prefix or deleted cursor rules)
for md in kiro_src.glob("*.md"):
    if md.name == "README.md":
        continue
    if md.stem not in stems:
        md.unlink()
        print(f"  removed stale {md.name}")

kiro_table = "\n".join(
    f"| `{c}` | `{k}` | `{inc}` |" for c, _a, _g, k, inc in table_rows
)
(kiro_src / "README.md").write_text(
    KIRO_README.format(rows=kiro_table), encoding="utf-8"
)

cursor_table = "\n".join(
    f"| `{c}` | `{a}` | `{g}` | `{k}` |"
    for c, a, g, k, _inc in table_rows
)
(cursor_src / "README.md").write_text(
    CURSOR_README.format(rows=cursor_table), encoding="utf-8"
)

print(f"Generated {len(mdc_files)} Kiro steering file(s) in {kiro_src}")
print(f"Updated {cursor_src / 'README.md'} and {kiro_src / 'README.md'}")
PY

link_dir() {
  local target="$1"
  local source="$2"
  if [[ ! -d "$source" ]]; then
    echo "Error: missing source $source"
    exit 1
  fi
  if [[ -e "$target" && ! -L "$target" ]]; then
    local bak="${target}.bak.$(date +%Y%m%d%H%M%S)"
    mv "$target" "$bak"
    echo "  backed up: $bak"
  fi
  mkdir -p "$(dirname "$target")"
  rm -rf "$target"
  ln -sfn "$source" "$target"
  echo "  $target → $source"
}

echo "== Rules → home IDE dirs =="
link_dir "$CURSOR_DEST" "$CURSOR_SRC"
link_dir "$KIRO_DEST" "$KIRO_SRC"

cursor_count=$(find "$CURSOR_SRC" -mindepth 1 -maxdepth 1 -name '*.mdc' 2>/dev/null | wc -l | tr -d ' ')
kiro_count=$(find "$KIRO_SRC" -mindepth 1 -maxdepth 1 -name '*.md' ! -name 'README.md' 2>/dev/null | wc -l | tr -d ' ')
if [[ "$cursor_count" != "$kiro_count" ]]; then
  echo "Warning: cursor .mdc count ($cursor_count) != kiro steering count ($kiro_count)"
  exit 1
fi
echo "Linked $cursor_count .mdc → $CURSOR_DEST"
echo "Linked $kiro_count steering files → $KIRO_DEST (1:1 stems)"

QS_INSTALLED="$CURSOR_DEST/question-scope.mdc"
if [[ -f "$QS_INSTALLED" ]]; then
  if grep -qE '^## Triggers \(skill runs\)' "$QS_INSTALLED" 2>/dev/null; then
    echo "ERROR: $QS_INSTALLED still has legacy '## Triggers (skill runs)' — fix rules/cursor/question-scope.mdc"
    exit 1
  fi
  QS_TAG="$(grep -oE 'qs-[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+' "$QS_INSTALLED" 2>/dev/null | head -1 || true)"
  if [[ -n "$QS_TAG" ]]; then
    echo "question-scope contract: $QS_TAG (session check: ./scripts/check-question-scope-session.sh)"
  fi
  echo "After rule edits: reload Cursor window or start a new chat (always-on rules cache in open sessions)."
fi
