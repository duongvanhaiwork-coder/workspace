---
name: analyze-impact
description: >
  Blast radius before shared-symbol or cross-service changes (MCP analyze_impact or
  search fallback). Also on user request for refactors/renames. L4 discover when scope
  active; L3 optional one-service. Does not run tests.
---

**Announce when applying:** `Using analyze-impact for <symbol>.`

**Stop when:** Blast radius (files/services/symbols) is documented or honestly bounded (search-only cap stated).

If using editor fallback, state results are **search-based**, not graph-complete (rule **`mcp-code-intelligence`**).

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

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md). **Handoff:** Record in phase MD → **`refactor-code`** or Regression via **`verification-before-completion`** (not in this skill).

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

1. Follow rule **`mcp-code-intelligence`** — MCP up: **`analyze_impact`** with `{ "project": "<name>", "symbol": "<symbol>" }`; MCP down or graph inconclusive: editor fallback per rule.
2. Summarize affected files, services, and symbols; suggest edit order and test suites for Regression scope.
3. If using editor fallback: cap listing (~30 paths, state **truncated**); include re-exports when obvious. If uncertain after tools, state gaps — do not claim all consumers found.

## Output shape

- Group by service or module when multi-repo
- List symbols and file paths from tool results; do not invent paths
- Label **graph-backed** vs **search-based** in the summary

## Prerequisites

- **Best:** project indexed; MCP healthy (rule **`mcp-code-intelligence`**).
- **Fallback:** search-based blast radius — cap and state truncated when large; do not imply graph-complete coverage.

## Do not

- Guess affected files without tools or explicit search when the symbol is shared
- Assume impact is only within one file when the symbol is exported
- Claim **graph-complete** coverage when using search-only fallback
- Run full-org test suites as a substitute for this skill — list targets; **`verification-before-completion`** runs tests in Regression
