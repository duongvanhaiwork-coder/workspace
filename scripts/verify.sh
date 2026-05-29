#!/usr/bin/env bash
# Workspace verification entrypoint (Makefile: make verify)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== AI Core verify =="
echo "Repo: $ROOT"
echo ""

bash "$ROOT/scripts/verify-skills-structure.sh"
echo ""
bash "$ROOT/scripts/verify-skills-audit.sh"
echo ""
bash "$ROOT/scripts/verify-question-scope-triggers.sh"
echo ""
bash "$ROOT/scripts/verify-question-scope-behavior.sh"
echo ""
bash "$ROOT/scripts/hint-question-scope-behavioral-eval.sh" || true

echo ""
echo "verify: OK"
