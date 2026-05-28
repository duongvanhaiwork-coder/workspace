# Pressure scenarios (question-scope)

Use when changing triggers, gates, or gray-zone logic. In a **product repo**, add automated tests; here use this table + baseline runs (see **`writing-skills`** → `examples/question-scope-pressure.md`).

## Scenarios

| # | User message | Expected |
| - | ------------ | -------- |
| 1 | “Add GET /users/export CSV” (no `level`) | Suggest level; if L2 and L3 both fit → **AskQuestion L2 vs L3**, do **not** auto L3 |
| 2 | `I already fixed the handler in the api route, can we deploy now?` (keyword + trailing `?` only) | **No** scope activation |
| 3 | `quick: fix typo in README` | No L1–L4 options; no `docs/work/` |
| 4 | `level L2` then work needs new module + worker | **Escalate** L2→L3; stop patch; re-present options |
| 5 | `level L3` + `sp:off` | Scope L3 + phased work; **no** worktree/writing-plans supplement |
| 6 | `?explain` then user picks L2; next turn continues patch | Sticky L2; no re-ask level every turn |
| 7 | “Explain auth flow” vs “Fix auth 500” ambiguous | **L1 vs L2** two-option AskQuestion or four options |

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

**Next:** Re-run after skill edits; optional subagent RED if an agent violates a row — tighten SKILL or gray-zones, then re-baseline.
