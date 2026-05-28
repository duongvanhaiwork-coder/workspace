---
name: analyze-impact
description: >
  Before renaming or changing a symbol, call MCP tool `analyze_impact` to list
  affected files from the code graph. Use when the user asks about blast radius,
  downstream impact, "what breaks if I change X", or before large refactors.
---

**Announce when applying:** `Using analyze-impact for <symbol>.`

If MCP is down, follow **Search-only fallback** and state results are bounded — not graph-complete.

## When to use

- User will modify, rename, or delete a function, class, or exported symbol
- User asks which files or services are affected
- Planning a refactor across modules

## Steps

1. Resolve **`project`** (MCP / indexed graph):
   - Prefer the **exact id** the user states.
   - Else, if the workspace defines a manifest (e.g. `projects.json`), match the current repo folder to a **`name`** field there.
   - Else use a **short slug from the repo root folder** or ask once: "Which app name should MCP use?"
   - Do not assume a local folder literally named `projects/` is the MCP id.
2. If MCP **`analyze_impact`** is available and the project is indexed: call it with `{ "project": "<name>", "symbol": "<symbol>" }`.
3. Summarize affected files; suggest order of edits and tests.
4. If the tool is unavailable, errors, empty, or the symbol cannot be resolved on the graph: run **Search-only fallback** (below). Say clearly the list is **search-based**, not graph-complete — do **not** claim all consumers are found.

## Search-only fallback (MCP down, unindexed, or inconclusive)

Use this when Step 2 does not yield a trustworthy graph:

1. **Say upfront** that results are bounded search, not a full code graph.
2. Find the **definition** (open the declaring file from user hint or `rg`/IDE search for the symbol).
3. List **imports and call sites** in the open repo: `rg`/grep for the symbol name with sensible filters; include re-exports if obvious.
4. **Cap** listing (e.g. first 30 unique paths) if huge; state **truncated**.
5. If partial MCP works, still prefer **`search_code`** / **`get_context`** before blind grep; otherwise **read_file** + workspace search tools.

## Prerequisites (full graph mode)

- MCP server running and healthy (your workspace may use `make health` or equivalent)
- Project indexed (your workspace may use `./scripts/index-all.sh`, `index_project`, or equivalent)

## Do not

- Guess affected files without tools or explicit search when the symbol is shared
- Assume impact is only within one file when the symbol is exported
