# Behavioral gates (question-scope)

**Parsing** (one message): [SKILL.md § Parsing](../SKILL.md#parsing) and [pressure-scenarios.md](./pressure-scenarios.md). Automated in the AI Core repo via **repo verification** ([README.md](../../../README.md) — trigger parser + contract anchors).

**Behavioral** (multi-turn, LLM): [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json). **Optional** spot-check — not required for every PR.

**Fixture IDs (full list):** **1, 4, 4b, 6, 6b, 6c, 7, 8, 9, 10, 11, 14, 15, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 49, 49b**

## Default gate (enough for most changes)

| Where | Action |
| ----- | ------ |
| **AI Core repo** (has `scripts/`) | **Repo verification** ([README.md](../../../README.md)) — sufficient for README, CHEATSHEET, templates, playbooks, sticky-scope wording, etc. |
| **After IDE sync** | Only rules + skills land in `~/.cursor/` — **no** `scripts/`, **no** repo verification from IDE. Sync: [README.md](../../../README.md). Reload window or **new chat** if rules look stale (`level Lx`, `?` + keyword as triggers). |

Do **not** require optional behavioral-eval helper script for routine merges ([README.md](../../../README.md)).

## Optional agent spot-check (trigger / meta / large contract)

Run only when a PR touches **Parsing, Meta, Scope Level, tokens**, `rules/cursor/question-scope.mdc`, or `references/gray-zones.md`.

**Minimum (2–3 chats)** — paste `user` lines from [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json); tick `expect` bullets:

| Priority | ID | Why |
| -------- | -- | --- |
| 1 | **#1** | Gray zone: exactly **L2 vs L3** + **STOP** (export on existing API) |
| 2 | **#6** | **Sticky** L2 — turn 2 must not re-ask four levels |
| 3 | **#8** or **#21** | Opt-out wins (#8) or meta beats token (#21) |
| 4 | **#49** or **#49b** | §12 STOP + Other (#49); `clarify:off` skips picker (#49b) |

Full 16 scenarios: optional before a **major** contract release; log in [pressure-scenarios.md § Behavioral eval log](./pressure-scenarios.md#behavioral-eval-log-manual) if you run them.

Optional repo helper prints the checklist — AI Core workspace only, not installed in IDE ([README.md](../../../README.md)).

## PR / contract-change checklist

| Change type | Required |
| ----------- | -------- |
| Docs, CHEATSHEET, templates, playbooks (no trigger/meta) | Repo verification **or** spot-review diff |
| Parsing, Meta, tokens, `question-scope.mdc`, gray-zones | Repo verification + **optional** spot-check **#1, #6, #8/#21** in new chat |
| Rule + skill trigger change | Same as row above + edit rule + SKILL together |

Steps when editing contract in **AI Core repo**:

1. Repo verification ([README.md](../../../README.md))
2. (Optional) spot-check 2–3 fixtures above in a **new** chat
3. IDE sync + reload window / new chat (any host) if rules changed ([README.md](../../../README.md))
4. Edit SKILL.md + `question-scope.mdc` together when triggers/tokens change

## Gates

| ID | Pressure row | Gate |
| -- | ------------ | ---- |
| **1** | Level pick (no L on command) | Structured Idea + Suggest; options with **For this task:** (and gray comparison when 2 options); **exactly L2 vs L3** for export-on-existing-API; **STOP** before Spec/Patch/Code |
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
| **24** | L3 bounded plan | **`architect-plan`** in phase file; **no** `docs/plans/` / **`writing-plans`** as primary |
| **25** | L2 rename only | **No** new failing TDD; **no** `writing-plans` / worktree default |
| **26** | L3 Test gate | **`Level: L3` header** includes **Test** before Code; **TC table** / **`generate-test`** before prod implementation |
| **27** | Test design RED | **`generate-test`**: failing tests OK; **no** prod code to green in Test phase |
| **28** | L3 bounded execute | **`executing-plans` (B)** on phase plan; **not** `subagent-driven-development` without `docs/plans/` |
| **29** | `docs/plans/` + user B | **`executing-plans` (B)** when user chose inline; **no** auto-A because plan file exists |
| **30** | No claim without verify | **No** “tests pass” / “done” without **fresh** command output |
| **31** | L3 Test RED + verify log | Test design: **RED expected** — not “all pass”; log evidence in **phase file** |
| **32** | Ship tests fail | **No** merge/PR while tests failing |
| **33** | Ship PR keeps worktree | Option 2: **no** `worktree remove` |
| **34** | Execute done ≠ Ship | **Review** + `l3-03` before **`finishing-a-development-branch`** only |
| **35** | L4 discover impact | **`analyze-impact`** in discover when radius unclear |
| **43** | Assessment-only L3 | Gap/review question → **Assessment** pipeline; **no** Code/Regression until user asks implement |
| **44** | Plan attach Spec | Approved plan in message → **no** duplicate `docs/work/` unless archive requested |
| **45** | Verify chat evidence | **No** “done” / “tests pass” without command + exit code in **chat** |
| **46** | `scope:light` L2 | Scope **on**; **no** mandatory `docs/work/`; rollup in chat OK |
| **47** | L3 test tier | Config/comment-only → Verify only; **new contract** → Test before Code |
| **48** | L2–L3 review short | Default **≤5** caveman lines unless security-sensitive diff or `audit:` |
| **49** | Clarifying options §12 | **Decision** + **Why it matters**; **2–4** options (behavior + trade-off) + **Other**; **STOP** before Patch/Code; [confirmation-prompts.md](./confirmation-prompts.md) § B |
| **49b** | `clarify:off` | Scope on; **no** §12 multi-option picker / numbered fork block; may implement when AC clear |
| **36** | L4 Regression scope | Per **impacted service** — not whole monorepo by default |
| **37** | Impact search fallback | **search-based** — no **graph-complete** claim |
| **38** | L4 pre-merge review | **`requesting-code-review`** before Ship merge/PR when supplement on |
| **39** | Subagent A no duplicate | **Not** `requesting-code-review` every task — bundled reviewers per task |
| **40** | Critical before merge | **No** merge/PR with unfixed **Critical** review findings |
| **41** | Incoming PR verify | **No** blind implement — **`receiving-code-review`** / verify before fix |
| **42** | Incoming PR clarify | **Clarify** unclear items before claiming full review addressed |

Parsing rows **8–11, 14, 15, 19, 21, 23** are covered by the automated trigger parser in repo verification — no manual paste needed for those alone.

**Supplement routing (#24–#42):** optional spot-check when editing execute/verify/ship/review/impact skills or L4 templates.
