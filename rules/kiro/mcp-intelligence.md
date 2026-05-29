---
inclusion: always
---

# MCP intelligence

**Server:** AI Core MCP (`ai-core`). Tools: `get_context`, `search_code`, `analyze_impact`.

## When → then (positive — workflow)

| Situation | Do |
| --------- | -- |
| MCP **connected** (panel green; tools callable) and task needs **code discovery** | 1. Resolve **`project`** (user id → manifest `name` → repo folder → ask once). 2. Pick tool: **`get_context`** (flow / entry / deps) → **`search_code`** (symbol, call sites, thin context) → **`analyze_impact`** (blast radius before shared-symbol edit). 3. Empty but MCP works → note project may be unindexed → editor fallback for that need. |
| MCP **not connected** (no server, tools missing, connection/tool error) | Editor fallback: `@file` / symbol hint → else `rg` entry → **Read** entry module → one import hop → widen only if needed. |
| User **`mcp:off`** / **`no-mcp`** | Editor fallback for the turn (even if MCP connected). |

**Playbooks (output shape):** skill **`explain-code`**, **`analyze-impact`**, **`generate-test`**.

## Do not (negative — constraints)

- **Do not** call MCP when MCP is not connected or tools error.
- **Do not** start code discovery with `Grep` or wide `Read` when MCP is connected.
- **Do not** treat empty MCP results as “MCP down” — connected + empty usually means unindexed or wrong **`project`**.
- **Do not** claim graph-backed or complete blast radius when using editor fallback — state **search-based** results.
- **Do not** retry MCP after a connection/tool error in the same turn; use editor fallback.

## Scope (mixed)

- **Do not** expand discovery beyond what the task needs (no repo-wide grep when entry is known).
- Prefer the **smallest correct path**: one MCP tool per need before widening to fallback.

**Precedence:** explicit user message (incl. `mcp:off`) → this rule → skill playbooks above.
