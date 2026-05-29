# L3 — Phase 2: Build + Prove

**Canonical steps:** Scaffold (if needed), Test Design, Implement, Verify, Review, Regression (required for L3), Iterate

## Isolated workspace (before code)

Fill after **`using-git-worktrees`** (L3 default; skip if `sp:off` or user works in place):

| Field | Value |
| ----- | ----- |
| Branch | `feature/…` |
| Worktree / checkout path | `.worktrees/…` or main repo path |
| Baseline test command | e.g. `npm test` |
| Baseline result | pass / fail (date) |

## Test design (before code — STOP without this table filled)

Use **`generate-test`** to author tests; map each row to Spec `Then` from `l3-01-define.md`.

| TC ID | Given | When | Then | Type |
| ----- | ----- | ---- | ---- | ---- |
| TC-01 | … | … | … | happy |
| TC-02 | … | … | … | error |
| TC-03 | … | … | … | edge |

### Test design checklist

- [ ] Maps to Spec `Then` rows from `l3-01-define.md`
- [ ] Includes ≥1 error path if user/system can send bad input
- [ ] IDs stable (do not renumber mid-flight; append TC-04…)

### Test design — command log (RED)

Use **`verification-before-completion`** — log **expected failures**, not “all pass”:

| Command | Output summary | Status |
| ------- | ---------------- | ------ |
| `npm test -- …` | e.g. `2 failed` — missing impl | RED expected |

## Scaffold (if any)

- [ ] New paths listed
- [ ] …

## Implementation log

**Execute (pick one):** **`executing-plans` (B, default)** — inline checkpoints per plan task · **`subagent-driven-development` (A)** — only with `docs/plans/…` and user chose A. Use **`test-driven-development`** per task when behavior changes.

- …

### Implementation checklist

- [ ] Each TC-XX traceable to code / test file
- [ ] No behavior change without updating TC table above

## Verify + regression

Use **`verification-before-completion`** for every run — log commands and output here (not chat-only).

| Step | Scope (L3 default) |
| ---- | ------------------ |
| **Verify** | Each TC row / smoke for changed behavior |
| **Regression** | Tests for touched **module/package** + **1-hop** callers of changed API/surface |

### Execution vs test cases (Verify)

| TC ID | Command / step | Result | Log / link |
| ----- | ---------------- | ------ | ---------- |
| TC-01 | `npm test -- foo` | pass / fail | … |
| TC-02 | … | … | … |

## Review notes

- …

### Review checklist

- [ ] Security + SOLID (skill)
- [ ] Each failed TC has ticket in Iterate below

## Iterate log (if failures)

| Date | TC ID | Symptom | Fix |
| ---- | ----- | ------- | --- |
| … | TC-02 | … | … |

## PR feedback / Iterate (after PR open)

When the PR has **incoming review comments**, use **`receiving-code-review`** (rule `incoming-code-review`) — not the same as Review step or `requesting-code-review`.

| Round | Comment / link | Action | Verify command | Result |
| ----- | ---------------- | ------ | -------------- | ------ |
| 1 | … | … | `npm test …` | pass |
| 2 | … | … | … | … |

- [ ] Clarified all items before implementing partial list
- [ ] Each fix has fresh **`verification-before-completion`** evidence

## Done when

- [ ] All P0 TC rows show pass (or accepted waiver with reason)
- [ ] `STATUS.md` updated → next file `l3-03-ship.md`
