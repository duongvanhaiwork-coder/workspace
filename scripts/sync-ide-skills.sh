#!/usr/bin/env bash
# Symlink canonical skills/ → ~/.cursor/skills and ~/.kiro/skills only.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/skills"
CURSOR_DEST="${CURSOR_SKILLS:-$HOME/.cursor/skills}"
KIRO_DEST="${KIRO_SKILLS:-$HOME/.kiro/skills}"

if [[ ! -d "$SRC" ]]; then
  echo "Error: $SRC not found."
  exit 1
fi

shopt -s nullglob
entries=("$SRC"/*)
if [[ ${#entries[@]} -eq 0 ]]; then
  echo "Error: $SRC is empty."
  exit 1
fi

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

echo "== Skills → home IDE dirs =="
link_dir "$CURSOR_DEST" "$SRC"
link_dir "$KIRO_DEST" "$SRC"

count=$(find "$SRC" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
echo "Skills in $SRC: $count"
