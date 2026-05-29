---
name: explain-code
description: >
  Explain how code works using AI Core search and context tools. Use when the user
  asks "how does this work", "explain this flow", "what calls X", or wants a
  walkthrough before editing unfamiliar code.
---

**Announce when applying:** `Using explain-code to walk through <feature/symbol>.`

**Stop when:** User has entry → flow → side effects (and unknowns stated); offer patch only if they ask.

Before claiming tests or behavior are verified, use **`verification-before-completion`** when the user asked for proof — this skill is read-only explanation.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User asks how code works — run this skill; default path (no scope, no repo edits).

### With question-scope

**L1** default; optional before Patch on L2+ when context is unclear — does not replace Spec.

**Assessment-only:** IDE-ALIGNED §3. **Plan attach:** IDE-ALIGNED §1 — explain per plan sections.

### Combines with (optional)

- `refactor-code` or `test-driven-development` — if user moves to change after explain

### Requires (hard)

- None

**Instruction precedence:** User message → this skill → **`question-scope`** L1/L2 context rules when scope active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Read-only walkthrough; then **`test-driven-development`** if user patches | Claim tests/behavior verified from explanation alone |
| **L1** default; optional before unclear L2+ context | Replace Spec or Patch gates when scope active |
| **NEXT:** `refactor-code` or `test-driven-development` when user moves to change | Mix implementation into the explain pass without announcing the next skill |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use

- User wants understanding, not a code change yet
- Entry point is unclear (symbol, file, or feature name)

## Steps

1. Follow rule **`mcp-intelligence`** — MCP up: **`get_context`** then **`search_code`** if thin; MCP down: editor fallback only.
2. Explain in order: entry → main flow → side effects → dependencies. If uncertain after tools, state unknowns — do not infer from names alone.
3. Cite file paths from tool results; do not invent paths.

## Output shape

- Short summary (1–2 sentences); note **graph-backed** vs **search-based** if editor fallback was used
- Numbered flow steps
- Optional diagram (mermaid) only if the flow has 4+ steps

## Prerequisites

- **Best:** project indexed; MCP healthy (rule **`mcp-intelligence`**).
- **Fallback:** any repo with readable source — do not imply graph-backed results when using editor fallback.
