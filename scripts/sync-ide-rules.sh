#!/usr/bin/env bash
# Canonical: rules/cursor/*.mdc → generate rules/kiro/*.md → symlink ~/.cursor/rules + ~/.kiro/steering
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

for mdc in sorted(cursor_src.glob("*.mdc")):
    text = mdc.read_text(encoding="utf-8")
    body = text
    front: dict[str, str] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    front[k.strip()] = v.strip()
            body = parts[2].lstrip("\n")

    kiro_lines: list[str] = []
    if front.get("alwaysApply", "false").lower() == "true":
        kiro_lines.append("inclusion: always")
    elif front.get("globs"):
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
    out_path = kiro_src / f"rules-{mdc.stem}.md"
    out_path.write_text(out, encoding="utf-8")
    print(f"  rules/cursor/{mdc.name} → rules/kiro/{out_path.name}")

stems = {p.stem for p in cursor_src.glob("*.mdc")}
for stale in kiro_src.glob("rules-*.md"):
    if stale.stem.removeprefix("rules-") not in stems:
        stale.unlink()
        print(f"  removed stale {stale.name}")

print(f"Generated Kiro rules in {kiro_src}")
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
kiro_count=$(find "$KIRO_SRC" -mindepth 1 -maxdepth 1 -name 'rules-*.md' 2>/dev/null | wc -l | tr -d ' ')
echo "Linked $cursor_count .mdc → $CURSOR_DEST"
echo "Linked $kiro_count steering files → $KIRO_DEST"
