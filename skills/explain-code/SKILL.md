---
name: explain-code
description: >
  Explain how code works using AI Core search and context tools. Use when the user
  asks "how does this work", "explain this flow", "what calls X", or wants a
  walkthrough before editing unfamiliar code.
---

## When to use

- User wants understanding, not a code change yet
- Entry point is unclear (symbol, file, or feature name)

## Steps

1. Resolve **`project`** for MCP calls (when tools are used):
   - Prefer the **exact id** the user states.
   - Else, if the workspace defines a manifest (e.g. `projects.json`), map the open repo to a **`name`** field.
   - Else use the **repo folder name** or ask once for the MCP app id.
   - MCP file paths inside containers vary by setup — follow tool errors and adjust; do not hardcode host paths.
2. Call **`get_context`** with a focused natural-language query (feature + key symbols).
3. Use **`search_code`** for additional call sites or definitions if context is thin.
4. If MCP is unavailable, errors, or results are empty: run **Editor fallback** (below) before explaining; state that the walkthrough is **file/search-based**, not graph-backed.
5. Explain in order: entry → main flow → side effects → dependencies.
6. Cite file paths from tool results; do not invent paths.

## Editor fallback (MCP down or thin context)

1. Start from user **`@file`** / symbol hints; otherwise `rg`/grep for the entry symbol or route name.
2. **read_file** on the entry module and follow imports one level deep before widening.
3. Use **codebase_search** (if available) or more `rg` for call sites; avoid loading unrelated directories.
4. If still uncertain, say what is unknown instead of inferring behavior from names alone.

## Output shape

- Short summary (1–2 sentences)
- Numbered flow steps
- Optional diagram (mermaid) only if the flow has 4+ steps

## Prerequisites

- **Best:** project indexed; MCP healthy (`make health` or equivalent when your workspace documents it).
- **Fallback:** any repo with readable source — follow **Editor fallback**; do not imply you used the graph when you did not.
