#!/usr/bin/env bash
# Sync rules + skills: canonical repo dirs → ~/.cursor and ~/.kiro only.
# Does not create Workspace/.cursor or Workspace/.kiro symlinks.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== Sync IDE config (home: ~/.cursor, ~/.kiro) =="
echo "Source repo: $ROOT"
echo ""

if [[ -d "$ROOT/skills" ]]; then
  bash "$ROOT/scripts/sync-ide-skills.sh"
else
  echo "Skip skills: $ROOT/skills not found"
fi

echo ""

if [[ -d "$ROOT/rules/cursor" ]]; then
  bash "$ROOT/scripts/sync-ide-rules.sh"
else
  echo "Skip rules: $ROOT/rules/cursor not found"
fi

echo ""
echo "Done. Verify:"
echo "  ls -la ~/.cursor/skills ~/.cursor/rules ~/.kiro/skills ~/.kiro/steering"
