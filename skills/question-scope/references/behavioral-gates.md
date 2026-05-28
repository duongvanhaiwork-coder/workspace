# Behavioral gates (question-scope)

**Parsing** (one message): [SKILL.md § Parsing](../SKILL.md#parsing) and [pressure-scenarios.md](./pressure-scenarios.md). Automated in AI Core repo via `make verify` → `verify-question-scope-triggers.sh`.

**Behavioral** (multi-turn, LLM): [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json). **Optional** spot-check — not required for every PR.

**Fixture IDs (full list):** **1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23**

## Default gate (enough for most changes)

| Where | Action |
| ----- | ------ |
| **AI Core repo** (has `scripts/`) | `make verify` — trigger parser + contract anchors (~70 checks). **Sufficient** for README, CHEATSHEET, templates, playbooks, sticky-scope wording, etc. |
| **After `make sync-ide`** | Only rules + skills land in `~/.cursor/` — **no** `scripts/`, **no** `make verify`. Reload window or open a **new chat** if injected rules look stale (`level Lx`, `?` + keyword as triggers). |

Do **not** require `./scripts/run-question-scope-behavioral-eval.sh` for routine merges.

## Optional agent spot-check (trigger / meta / large contract)

Run only when a PR touches **Parsing, Meta, Scope Level, tokens**, `rules/cursor/question-scope.mdc`, or `references/gray-zones.md`, or bumps **`qs-…`**.

**Minimum (2–3 chats)** — paste `user` lines from [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json); tick `expect` bullets:

| Priority | ID | Why |
| -------- | -- | --- |
| 1 | **#1** | Gray zone: exactly **L2 vs L3** + **STOP** (export on existing API) |
| 2 | **#6** | **Sticky** L2 — turn 2 must not re-ask four levels |
| 3 | **#8** or **#21** | Opt-out wins (#8) or meta beats token (#21) |

Full 16 scenarios: optional before a **major** contract release; log in [pressure-scenarios.md § Behavioral eval log](./pressure-scenarios.md#behavioral-eval-log-manual) if you run them.

Repo helper (optional): `./scripts/run-question-scope-behavioral-eval.sh` prints the checklist — only in AI Core workspace, not after sync.

## PR / contract-change checklist

| Change type | Required |
| ----------- | -------- |
| Docs, CHEATSHEET, templates, playbooks (no trigger/meta) | `make verify` in repo **or** spot-review diff |
| Parsing, Meta, tokens, `question-scope.mdc`, gray-zones | `make verify` + **optional** spot-check **#1, #6, #8/#21** in new chat |
| Bump `qs-…` tag | Same as row above + sync tag in SKILL + rule |

Steps when editing contract in **AI Core repo**:

1. `make verify`
2. (Optional) spot-check 2–3 fixtures above in a **new** chat
3. `make sync-ide` + reload Cursor if rules changed
4. Bump `qs-…` in SKILL.md + `question-scope.mdc` when triggers/tokens change

## Gates

| ID | Pressure row | Gate |
| -- | ------------ | ---- |
| **1** | Level pick (no L on command) | Idea + Suggest; **exactly L2 vs L3** for export-on-existing-API; **STOP** before Spec/Patch/Code |
| **4** | Escalation L2→L3 | Stop patch; re-present **L2 vs L3**; continue only after user confirms |
| **4b** | Escalation L3→L4 | Stop L3 heavy design; re-present **L3 vs L4** before full L4 folder |
| **6** | Sticky scope L2 | No second four-option picker while L2 continues |
| **6b** | Sticky scope L3 | No second four-option picker while L3 continues |
| **6c** | Sticky scope L4 | No second four-option picker while L4 continues |
| **7** | Gray zone L1 vs L2 | **Exactly two** options (L1 vs L2); **STOP** until pick |
| **8** | Opt-out vs `/question-scope Lx` | **No** scope pipeline; opt-out wins |
| **9** | Legacy `?` + keyword | **No** scope; suggest `/question-scope` |
| **10** | Legacy `level Lx` | **No** scope; suggest `/question-scope Lx` |
| **11** | Mid-sentence command | **No** scope pipeline; tell user start/end placement |
| **14** | Glued `L` | Hint once; **no** preset L2; STOP before Patch |
| **15** | Meta path | **No** scope pipeline on audit |
| **19** | Meta VI (no path) | **No** scope pipeline |
| **21** | Meta beats token | **No** scope despite `/question-scope` in message |
| **23** | Explicit `qs:meta` | **No** scope; beats `/question-scope Lx` in same message |

Parsing rows **8–11, 14, 15, 19, 21, 23** are covered by `verify-question-scope-triggers.sh` — no manual paste needed for those alone.
