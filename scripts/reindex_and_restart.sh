#!/bin/bash
# Reindex project and signal MCP server to reload.
# Usage: ./scripts/reindex_and_restart.sh [project_name] [--full]

set -e

PROJECT="${1:-business-lounge-api}"
FULL_FLAG="${2:---full}"
VENV="/Users/chanh/workspace/.venv/bin/python"
WORKSPACE="/Users/chanh/workspace"

echo "=== Reindexing project: $PROJECT ($FULL_FLAG) ==="
cd "$WORKSPACE"
$VENV scripts/index_project.py "$PROJECT" $FULL_FLAG

echo ""
echo "=== Killing MCP server (Kiro will auto-restart) ==="
pkill -f "mcp_server.server" 2>/dev/null && echo "Server killed" || echo "No server running"

echo ""
echo "Done. Reconnect MCP from Kiro (Cmd+Shift+P → MCP: Reconnect)"
