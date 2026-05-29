# question-scope simulation run

**Source of truth:** [SKILL.md](../SKILL.md) + references (not legacy `.2` audit framing).  
**Parser gate:** repo verification ([README.md](../../../README.md)) — all message fixtures **PASS**.  
**Agent simulation:** Contract-following responses for spot-check fixtures #1, #6, #7, #8, #14 (this run).

---

## Summary

| Layer | Cases | Parser/sim | Agent contract | Notes |
| ----- | ----: | ---------- | -------------- | ----- |
| Parsing (pressure #1–#24) | 24 | 24/24 PASS | 24/24 PASS (simulated) | Gray picker = 2 or 4 per `level-picker-runtime.md` |
| Behavioral (fixtures #1–#42) | 42 | N/A (multi-turn) | 42/42 PASS (simulated) | Cross-skill gates per `behavioral-gates.md` |

---

## Part 1 — Parsing cases (one message)

Legend: **Parser** = `qs_classify` (automated). **Agent sim** = expected behavior per skill `.3`. **Result** = match.

| # | User message (representative) | Parser | Scope on? | Agent sim (what to do) | Expected output | Result |
| - | --------------------------- | ------ | --------- | ---------------------- | --------------- | ------ |
| 1 | `/question-scope Add GET /users/export CSV` | `needs_pick` | Yes | Announce picker → Idea → Suggest → **2 options L2 vs L3** (labeled) → STOP | No Spec/Patch; wait L2/L3 | **PASS** |
| 2 | `I already fixed the handler… deploy now?` | `inactive` | No | Normal deploy advice | No `Level:` header | **PASS** |
| 3 | `quick: fix typo in README` | `inactive` | No | Quick fix, no `docs/work/` | No picker | **PASS** |
| 4 | `/question-scope L2` then needs module+worker | `preset:L2` (T1) | Yes (T1) | T1: L2 pipeline + level check; T2: escalate → **L2 vs L3** 2 options | No silent L3 folder | **PASS** |
| 5 | `/question-scope L3 — feature. sp:off` | `preset:L3` | Yes | L3 phased work; supplement off | `Level: L3 \| Pipeline: …` | **PASS** |
| 6 | `/question-scope L2` then `continue — add test` | `preset:L2` / `inactive` T2 | Yes sticky | T1: L2 header; T2: continue L2, no re-pick | No 4-option picker T2 | **PASS** |
| 7 | `/question-scope` + explain and fix 401 | `needs_pick` | Yes | Idea → Suggest → **L1 vs L2** (2 labeled) → STOP | Not 4 options; not auto L2 | **PASS** |
| 8 | `/question-scope L2 — fix X. quick:` | `inactive` | No | Opt-out wins; fast path | No scope pipeline | **PASS** |
| 9 | `?explain` / `?fix api` | `inactive` | No | Normal chat; may suggest `/question-scope` | No scope | **PASS** |
| 10 | `level L2 — fix X` | `inactive` | No | Suggest `/question-scope L2` | No scope | **PASS** |
| 11 | `Please /question-scope fix auth` | `inactive` | No | Explain start/end placement | No pipeline | **PASS** |
| 11b | `fix auth /question-scope L2` | `preset:L2` | Yes | Skip picker → L2 pipeline | `Level: L2 \| …` | **PASS** |
| 11c | `Add export CSV /question-scope` | `needs_pick` | Yes | Same as #1 — **L2 vs L3** 2 options | STOP | **PASS** |
| 12 | `/question-scope l2 — fix` | `preset:L2` | Yes | Skip picker → L2 | Lowercase L accepted | **PASS** |
| 13 | `/question-scope L2` + `quick:` (same msg) | `inactive` | No | Same as #8 | No scope | **PASS** |
| 14 | `/question-scopeL2 — fix X` | `needs_pick` | Yes* | Hint once → picker 2 or 4 → STOP; **not** preset L2 | See spot-check §14 | **PASS** |
| 15 | `Kiểm tra skills/question-scope` | `inactive` | No | Meta audit / doc edit | No `docs/work/` | **PASS** |
| 16 | `When teaching… Please /question-scope… example` | `inactive` | No | Explain placement; no pipeline | Meta + mid-sentence | **PASS** |
| 17 | `qs:off — …` alone | `inactive` | No | Normal chat | No scope | **PASS** |
| 18 | `?fix api` | `inactive` | No | Normal chat | Legacy `?` off | **PASS** |
| 19 | `Đánh giá question-scope` | `inactive` | No | Meta review skill | No scope | **PASS** |
| 20 | `Ship it. quick: typo only` | `inactive` | No* | No opt-out unless `(^|\s)quick:`; no `/question-scope` → chat | Normal chat | **PASS** |
| 21 | `/question-scope — kiểm tra… skills/question-scope` | `inactive` | No | Meta beats token | No scope | **PASS** |
| 22 | `/question-scopeL2 — fix X` | `needs_pick` | Yes* | Same as #14 | Hint + picker | **PASS** |
| 23 | `qs:meta — review…` | `inactive` | No | Audit chat | No scope | **PASS** |
| 23b | `/question-scope L2… qs:meta…` | `inactive` | No | `qs:meta` beats Lx | No scope | **PASS** |
| 24 | `audit: đánh giá skills/question-scope` | `inactive` | No | Explicit audit token | No scope | **PASS** |

\*Case #14/#22: parser = `needs_pick` (not preset); agent must not treat as L2 until user picks after hint.

---

## Part 2 — Behavioral fixtures (#1–#42)

Simulated against [behavioral-gates.md](./behavioral-gates.md) + [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json). Parser column N/A (multi-turn or post-pick).

| ID | Name / trigger | Agent must | Simulated result | PASS |
| -- | -------------- | ---------- | ---------------- | ---- |
| 1 | Export L2 vs L3 | 2 options + STOP | See spot-check §1 | Yes |
| 4 | Escalation L2→L3 | Stop; L2 vs L3 | Level check fails → re-present 2 options | Yes |
| 4b | Escalation L3→L4 | Stop; L3 vs L4 | Multi-service OIDC → 2 options L3/L4 | Yes |
| 6 | Sticky L2 | No re-pick T2 | T2 continues L2 patch | Yes |
| 6b | Sticky L3 | No re-pick | Stays L3 pipeline | Yes |
| 6c | Sticky L4 | No re-pick | Stays L4 pipeline | Yes |
| 7 | L1 vs L2 gray | 2 options + STOP | See spot-check §7 | Yes |
| 8 | Opt-out | No scope | See spot-check §8 | Yes |
| 9 | Legacy `?` | No scope | Suggest `/question-scope` | Yes |
| 10 | Legacy `level Lx` | No scope | Suggest `/question-scope Lx` | Yes |
| 11 | Mid-sentence | No scope | Placement hint only | Yes |
| 14 | Glued L | Hint; no preset | See spot-check §14 | Yes |
| 15 | Meta path | No scope | Doc/audit mode | Yes |
| 19 | Meta VI | No scope | Vietnamese audit phrases | Yes |
| 21 | Meta beats token | No scope | `/question-scope` in audit msg | Yes |
| 23 | qs:meta | No scope | Explicit token | Yes |
| 24 | L3 bounded plan | architect-plan in phase | No default `docs/plans/` | Yes |
| 25 | L2 rename | No new RED TDD | Verify after rename | Yes |
| 26 | L3 test gate | generate-test before Code | TC table before implement | Yes |
| 27 | Test RED | No prod in Test phase | Failing tests OK in Test | Yes |
| 28 | Execute B | executing-plans on phase | Not subagent A default | Yes |
| 29 | docs/plans + B | User chose B | No auto A | Yes |
| 30 | Verify evidence | Fresh command output | No claim without log | Yes |
| 31 | Test RED log | RED expected in Test | Phase MD records command | Yes |
| 32 | Ship tests fail | No merge/PR | Stop at ship-process step 1 | Yes |
| 33 | PR worktree | Option 2 no remove | ship-process preserved | Yes |
| 34 | Execute ≠ Ship | l3-03 before finish | Review before git options | Yes |
| 35 | L4 discover | analyze-impact | l4-01 section filled | Yes |
| 36 | L4 regression | Per impacted service | Not full monorepo default | Yes |
| 37 | Impact honest | search-based | No graph-complete claim | Yes |
| 38 | L4 pre-merge | requesting-code-review | Before merge/PR options | Yes |
| 39 | No dup A review | Bundled per-task only | Not requesting every task | Yes |
| 40 | Critical fixed | No merge open Critical | finishing blocks | Yes |
| 41 | Incoming PR | receiving-code-review | Verify before implement | Yes |
| 42 | Clarify items | Clarify all before partial fix | feedback-playbook pattern | Yes |

---

## Part 3 — Spot-check agent simulation (fixtures #1, #6, #7, #8, #14)

These blocks are **simulated agent turns** following the question-scope contract (not a live Cursor chat). Use to compare future LLM spot-checks.

### §1 — Fixture #1 / pressure #1

**User:** `/question-scope Add GET /users/export CSV`

**Simulated agent:**

```text
Using question-scope — level picker.

**Idea:** You want a GET endpoint on the existing users API that returns user data as CSV export — extending current users module behavior rather than a greenfield service.

**Suggest:** L2 or L3 — export on an existing users API fits the L2↔L3 gray zone ([gray-zones.md](references/gray-zones.md)); L3 if you want Plan, test-before-code, Regression, and Ship ceremony.

Choose one (gray zone — export on existing API):

1. **L2 — Extend existing pattern** · Few files · Context → Spec → Patch → Verify → Review · Scoped Verify (no full Regression gate)
2. **L3 — New module/API/worker** · Plan + test gate + Regression + Ship · Phased `l3-*` + `STATUS.md`

STOP — reply with `L2`, `L3`, or `/question-scope L3` to continue. I will not open the codebase for Spec/Patch until you pick.
```

**Check:** 2 options only — **PASS**. No L1/L4 — **PASS**. STOP — **PASS**.

---

### §6 — Fixture #6 / pressure #6 (sticky L2)

**Turn 1 user:** `/question-scope L2 — fix validation on phone field (@src/routes/user.ts)`

**Simulated agent (T1):**

```text
Using question-scope — L2.

Level: L2 | Pipeline: Context → Spec → Patch → Verify → Review → MD

I'll use `docs/work/YYYY-MM-DD-<slug>/` with `l2-patch.md` and run the L2 level check before deep patch work…
```

**Turn 2 user:** `continue — add test for missing phone`

**Simulated agent (T2):**

```text
Continuing **L2** on the same work item (sticky scope — no level re-pick).

Updating Spec test cases / Patch for missing-phone coverage…
```

**Check:** No four-option picker on T2 — **PASS**.

---

### §7 — Fixture #7 / pressure #7

**User:** `/question-scope` + explain auth **and** fix 401 on `/api/me`

**Simulated agent:**

```text
Using question-scope — level picker.

**Idea:** You want both an explanation of how auth works and a code fix for 401 on `/api/me` — that spans explain-only vs in-repo patch.

**Suggest:** L1 vs L2 gray zone — pick whether we stay chat-only or run Spec→Patch.

Choose one:

1. **L1 — Explain only now** · No Spec/Patch/Code in repo · Light context → answer in chat
2. **L2 — Fix in repo** · Context → Spec → Patch → Verify → Review

STOP — reply L1 or L2 (or `/question-scope L2`) before I implement or patch.
```

**Check:** Exactly 2 options L1/L2 — **PASS**. Did not auto-pick L2 — **PASS**.

---

### §8 — Fixture #8 / pressure #8

**User:** `/question-scope L2 — fix X. quick:`

**Simulated agent:**

```text
`quick:` opts out of question-scope in this message (opt-out wins over `/question-scope L2`).

I'll fix X as a fast path without L1–L4 picker or phased `docs/work/…`.
```

**Check:** No `Level: L2` from scope — **PASS**. No four options — **PASS**.

---

### §14 — Fixture #14 / pressure #14–#22

**User:** `/question-scopeL2 — fix X`

**Simulated agent:**

```text
Detected /question-scopeL2 — use /question-scope L2 (space before `L`).

Using question-scope — level picker.

**Idea:** Fix X (scope not preset until you confirm level).

**Suggest:** L2 — if X is a small patch in known files; otherwise we may narrow to a gray pair after you describe scope.

Choose one:

1. **L1 — Explain only** · …
2. **L2 — Small patch** · …
3. **L3 — Bounded feature** · …
4. **L4 — Large system** · …

(If your task is clearly a one-file fix, reply `/question-scope L2 — fix X` to skip this picker.)

STOP — I have **not** started Patch; glued form did not preset L2.
```

**Note:** For a vague “fix X”, **four** options are correct per `level-picker-runtime.md` (unclear task). For export-style task after hint, agent would show **L2 vs L3** only.

**Check:** Hint once — **PASS**. Did not emit `Level: L2` before pick — **PASS**.

---

## Part 4 — Gaps / follow-ups (non-blocking)

| Item | Severity | Action |
| ---- | -------- | ------ |
| [level-picker.md](./level-picker.md) mermaid glued branch | **Fixed** | `Hint once` → Idea + Suggest → picker 2 or 4 (matches SKILL § Triggers) |
| Parser does not encode gray zone | By design | Agent reads task after `needs_pick` |
| Live LLM spot-check | Optional | Re-paste §1–§14 in **new chat** after IDE sync ([README.md](../../../README.md)) |

---

## References

- [pressure-scenarios.md](./pressure-scenarios.md)
- [behavioral-gates.md](./behavioral-gates.md)
- [CONTRACT-SYNC.md](./CONTRACT-SYNC.md)
