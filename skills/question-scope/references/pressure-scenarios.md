# Pressure scenarios (question-scope)

Use when changing triggers, gates, or gray-zone logic. In a **product repo**, add automated tests; here use this table + baseline runs (see **`writing-skills`** → `examples/question-scope-pressure.md`).

## Scenarios

| # | User message | Expected |
| - | ------------ | -------- |
| 1 | `/question-scope` + “Add GET /users/export CSV” (no L on command) | Suggest level; if L2 and L3 both fit → **AskQuestion L2 vs L3**, do **not** auto L3 |
| 2 | `I already fixed the handler in the api route, can we deploy now?` (no `/question-scope`) | **No** scope activation |
| 3 | `quick: fix typo in README` | No L1–L4 options; no `docs/work/` |
| 4 | `/question-scope L2` then work needs new module + worker | **Escalate** L2→L3; stop patch; re-present options |
| 5 | `/question-scope L3` + `sp:off` | Scope L3 + phased work; **no** worktree/writing-plans supplement |
| 6 | `/question-scope L2` sticky; next turn continues patch | Sticky L2; no re-ask level every turn |
| 7 | `/question-scope` + ambiguous explain vs fix | **L1 vs L2** two-option AskQuestion or four options |
| 8 | `/question-scope L2 — fix X. quick:` or `qs:off /question-scope L3` | **No** scope activation; opt-out wins |
| 9 | `?explain` or `fix something?` (no `/question-scope`) | **No** scope activation — use `/question-scope` |
| 10 | `level L2 — fix X` (no `/question-scope`) | **No** scope — use `/question-scope L2` |
| 13 | `/question-scope L2` + `quick:` same message | Same as #8 — opt-out wins |
| 11 | `Please /question-scope fix auth` (mid-sentence) | **Yes** — priority 2; token not line-start |
| 12 | `/question-scope l2` (lowercase L) | **Yes** — priority 1 at L2 |

## Baseline run (2026-05-28)

Manual check against [SKILL.md](../SKILL.md) + [gray-zones.md](./gray-zones.md) after references split.

| # | Result | Evidence in contract |
| - | ------ | -------------------- |
| 1 | **PASS** | Gray-zone: do not auto-pick heavier; L2 vs L3 AskQuestion table |
| 2 | **PASS** | Tight match: trailing `?` only → no trigger |
| 3 | **PASS** | `quick:` row: scope off, no phased `docs/work/` |
| 4 | **PASS** | Escalation + l2-patch level check → stop L2 |
| 5 | **PASS** | `sp:off`: supplement off; scope on per opt-out table |
| 6 | **PASS** | Sticky scope explicit in SKILL |
| 7 | **PASS** | L1 vs L2 pair in gray-zones AskQuestion table |
| 8 | **PASS** | Conflicting tokens § in SKILL.md |
| 9 | **PASS** | `?` does not activate — SKILL § Parsing |
| 10 | **PASS** | `level L2` alone does not activate |
| 13 | **PASS** | `/question-scope Lx` + opt-out in Conflicting tokens |
| 11 | **PASS** | `/question-scope` anywhere — Parsing table |
| 12 | **PASS** | Case-insensitive `l2` → `L2` |

**Automated pilot:** [examples/pressure-test-pilot.md](../examples/pressure-test-pilot.md) in a product repo.

**Next:** Re-run after skill edits; optional subagent RED if an agent violates a row — tighten SKILL or gray-zones, then re-baseline.
