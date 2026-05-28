#!/usr/bin/env bash
# Alias for sync-ide.sh (global ~/.cursor + ~/.kiro only).
# Usage: IDE_GLOBAL_ROOT=~/Workspace ./scripts/link-global-ide.sh
set -euo pipefail

GLOBAL_ROOT="${IDE_GLOBAL_ROOT:-"$(cd "$(dirname "$0")/.." && pwd)"}"
GLOBAL_ROOT="${GLOBAL_ROOT/#\~/$HOME}"

if [[ ! -d "$GLOBAL_ROOT" ]]; then
  echo "Error: IDE_GLOBAL_ROOT is not a directory: $GLOBAL_ROOT"
  exit 1
fi

if [[ ! -f "$GLOBAL_ROOT/scripts/sync-ide.sh" ]]; then
  echo "Error: missing $GLOBAL_ROOT/scripts/sync-ide.sh"
  exit 1
fi

echo "link-global-ide → sync-ide.sh (targets ~/.cursor, ~/.kiro)"
echo ""
bash "$GLOBAL_ROOT/scripts/sync-ide.sh"
