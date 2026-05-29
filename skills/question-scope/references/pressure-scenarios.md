# Pressure scenarios (question-scope)

Reference table for triggers, gates, and gray-zone logic. Contract: [SKILL.md](../SKILL.md), [gray-zones.md](./gray-zones.md).

## Scenarios (parsing — one message)

| # | User message | Expected |
| - | ------------ | -------- |
| 1 | `/question-scope` + “Add GET /users/export CSV” (no L on command) | Idea + Suggest; **exactly L2 vs L3** (export on existing API — [gray-zones](./gray-zones.md)); **STOP**; never auto-pick heavier. Use **four options** only when three+ levels fit |
| 2 | `I already fixed the handler in the api route, can we deploy now?` (no `/question-scope`) | **No** scope activation |
| 3 | `quick: fix typo in README` | No L1–L4 options; no `docs/work/` |
| 4 | `/question-scope L2` then work needs new module + worker | **Escalate** L2→L3; stop patch; re-present options |
| 5 | `/question-scope L3` + `sp:off` | Scope L3 + phased work; **no** worktree/writing-plans supplement |
| 6 | `/question-scope L2` sticky; next turn continues patch | Sticky L2; no re-ask level every turn |
| 7 | `/question-scope` + ambiguous explain vs fix | **Exactly two labeled** options: **L1 vs L2** (each with what-that-L-does note); STOP; no four-option picker; no auto-pick L2 |
| 8 | `/question-scope L2 — fix X. quick:` or `qs:off /question-scope L3` | **No** scope activation; opt-out wins |
| 9 | `?explain` or `fix something?` (no `/question-scope`) | **No** scope activation — use `/question-scope` |
| 10 | `level L2 — fix X` (no `/question-scope`) | **No** scope — use `/question-scope L2` |
| 11 | `Please /question-scope fix auth` (mid-sentence) | **No** — token must be at **start or end**; use `/question-scope L2 — fix auth` or `fix auth /question-scope L2` |
| 11b | `fix auth /question-scope L2` (end placement) | **Yes** — priority 1 at L2 |
| 11c | `Add export CSV /question-scope` (end, no L) | **Yes** — priority 2; **L2 vs L3** two-option picker (export gray — same as #1) |
| 16 | `When teaching, say Please /question-scope fix auth as an example` | **No** — mid-sentence (meta optional) |
| 12 | `/question-scope l2` (lowercase L) | **Yes** — priority 1 at L2 |
| 13 | `/question-scope L2` + `quick:` same message | Same as #8 — opt-out wins |
| 14 | `/question-scopeL2 — fix X` (no space before L) | **No** preset L2 — hint once; level picker (2 or 4); tell user correct form |
| 15 | `Kiểm tra skills/question-scope` or `Don't use /question-scope for this audit` | **No** scope — meta/audit (optional `qs:off`) |
| 17 | `qs:off — …` or `no-scope — …` alone (no `/question-scope`) | **No** scope — normal chat |
| 18 | `?fix api` or `?explain` (no `/question-scope`) | **No** scope — legacy `?` + keyword does not activate |
| 19 | `Kiểm tra lại rule question-scope` / `Đánh giá question-scope` (no path) | **No** scope — meta (Vietnamese audit phrases) |
| 20 | `Ship it. quick: typo only` (`quick:` not at line start) | **No** scope — `(^|\s)quick:` opt-out |
| 21 | `/question-scope — kiểm tra lại về rule` + path `skills/question-scope` | **No** scope — meta beats token |
| 22 | `/question-scopeL2 — fix X` | **No** preset L2 — hint once; level picker (2 or 4); agent says `Detected /question-scopeL2 — use /question-scope L2` once |
| 23 | `qs:meta — review question-scope rules` | **No** scope — explicit audit token |
| 23b | `/question-scope L2 — fix X. qs:meta — audit only` | **No** scope — `qs:meta` beats `/question-scope Lx` |
| 24 | `audit: đánh giá skills/question-scope` | **No** scope — explicit `audit:` token |
| 25 | `/question-scope L2 clarify:off — patch handler` | **Yes** L2 — **no** §12 AskQuestion block; may patch when AC clear |
| 26 | `/question-scope L2 — callback JSON or redirect?` (ambiguous how) | **Yes** L2 — **§12**: 2–4 options + **Other**; **STOP** before Patch |

## Behavioral (multi-turn)

Fixtures **1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 49, 49b** — turns and expectations in [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json); summary in [behavioral-gates.md](./behavioral-gates.md).

## Contract cross-check

| Topic | Where |
| ----- | ----- |
| Parsing | [SKILL.md § Parsing](../SKILL.md#parsing) |
| Behavioral | [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json) |
| Rule + skill mirror | `question-scope.mdc` + `SKILL.md` edited together — see [CONTRACT-SYNC.md](./CONTRACT-SYNC.md) |

## Behavioral eval log (manual)

**Default:** repo verification in AI Core ([README.md](../../../README.md)). **Optional** log below — spot-check **#1, #6, #8/#21** in new chats when Parsing/Meta/tokens change; **#49, #49b** when §12 / `clarify:off` change; full 16 only for major releases. After IDE sync ([README.md](../../../README.md)), no scripts in IDE — paste from [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json) if spot-checking.

| Date | Agent / chat | Scenarios | Result | Notes |
| ---- | ------------ | --------- | ------ | ----- |
| 2026-05-28 | meta audit chat | 15, 19, 21 | PASS (meta) | Path + VI audit phrases — scope correctly off |
| 2026-05-29 | contract sim | Parsing #1–#24 + fixtures 1–42 | PASS (sim) | Full log: [SIMULATION-RUN.md](./SIMULATION-RUN.md); parser: repo verification ([README.md](../../../README.md)); spot-check text #1, #6, #7, #8, #14 |
