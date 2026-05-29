---
name: analyze-impact
description: >
  Blast radius before shared-symbol or cross-service changes (MCP analyze_impact or
  search fallback). Also on user request for refactors/renames. L4 discover when scope
  active; L3 optional one-service. Does not run tests.
---

**Announce when applying:** `Using analyze-impact for <symbol>.`

If MCP is down, follow **Search-only fallback** and state results are bounded — not graph-complete.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User asks what breaks if they change X, or before a refactor — run this skill; output in chat or a note; no `/question-scope` required.

### With question-scope

**L4** discover when radius unclear; **L3** optional (one service); record in phase MD — feeds Regression scope, does **not** replace running tests.

### Combines with (optional)

- `refactor-code` — before cross-module rename
- `architect-plan` / L4 discover — feed Regression scope

### Requires (hard)

- None

**Instruction precedence:** User message → this skill → **`question-scope`** Regression step only when scope active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| List blast radius (files, services, symbols) before large touch | Claim tests pass or replace **Regression** with this skill |
| Feed Regression scope in phase MD when scope on | Run as substitute for **`verification-before-completion`** |
| **NEXT:** `refactor-code` or plan with impacted scope noted | Skip when renaming shared symbols “because it’s small” |

**NEXT:** `refactor-code` / Regression scope · Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md)

## With question-scope (impact ≠ Regression)

| Topic | Skill / step |
| ----- | ------------- |
| **This skill** | **What** is affected (files, services, symbols) — graph or search |
| **Phase Regression (L3–L4)** | **Run tests** for impacted scope — **`verification-before-completion`** in `l3-02` / `l4-04-prove` |
| **Do not** | Claim tests pass here; do not replace Regression with impact analysis |

| Level | When to run `analyze-impact` |
| ----- | ------------------------------ |
| **L4** | **`l4-01-discover`** if blast radius unclear; before locking cross-service API in **`l4-02-define`** / **`architect-plan`** |
| **L3** | Optional — shared/exported symbol or cross-module plan; **bounded to one service** ([`l3-vs-l4-diff`](../question-scope/references/l3-vs-l4-diff.md)) |
| **L2** | Optional before large patch on shared code — scoped Verify still applies |

**Output:** Record in phase MD (`l4-01` § *analyze-impact / exploration notes*, plan **### Architecture**, or task notes) — feeds **L4 Regression** suite list per impacted **service**.

## When to use

- User will modify, rename, or delete a function, class, or exported symbol
- User asks which files or services are affected
- Planning a refactor across modules
- **L4** discover/validate or plan before multi-service implementation

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

- MCP server running and healthy (team health check or equivalent)
- Project indexed (MCP `index_project`, team indexer, or equivalent)

## Do not

- Guess affected files without tools or explicit search when the symbol is shared
- Assume impact is only within one file when the symbol is exported
- Claim **graph-complete** coverage when using search-only fallback
- Run full-org test suites as a substitute for this skill — list targets; **`verification-before-completion`** runs tests in Regression
