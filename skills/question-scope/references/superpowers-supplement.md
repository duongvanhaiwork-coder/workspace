# Superpowers supplement (question-scope)

Load **after** level is chosen (L2–L4). STOP gates and level budgets in [SKILL.md](../SKILL.md) win.

**Question-scope** sets **how much** work (L1–L4), gates, and **`docs/work/…`**. The **Superpowers** bundle ([SKILLS-REGISTRY.md](../../SKILLS-REGISTRY.md), rule IDs in **`@workflow`**) adds **how** to execute: design gate, plans, worktree, TDD, verify, subagents.

**Precedence:** Superpowers playbooks **must not** skip L1–L4 choice, `docs/work/` continuity, or rule **`code-standards`** / stack rules. User may say **`sp:off`** (or `no-sp`) to skip the supplement only. Do not use `superpowers: off` (legacy plugin prefix).

**Default:** Supplement for **L3–L4** unless opted out. **L2** — minimal row only. **L1** — no feature flow (`explain-code` optional).

## By level

| Level | Question-scope (primary) | Superpowers supplement |
| ----- | ------------------------ | ---------------------- |
| L1 | Answer; no patch | None (optional `explain-code`) |
| L2 | Spec → Patch → Verify → Review | `tdd-during-implementation` if behavior changes; `verify-before-done` before “done”; skip `design-approval-gate` / `implementation-plan` unless user escalates to L3 |
| L3 | Spec → Plan → Test → Code → … → phased `docs/work/…` | `isolated-workspace` before code; `tdd-during-implementation`; **default execute:** `execute-inline-checkpoints` (B); `execute-via-subagents` (A) **only** with `writing-plans` or user asks for subagents; `verify-before-done`; `finish-branch-options` at ship |
| L4 | Full 15-step + architecture/AI/delivery layers | Near-full feature flow + `design-approval-gate` and `implementation-plan` when scope is large; `outgoing-code-review` before merge when applicable |

**Bug / test failure:** [SKILL.md § Bug overlay](../SKILL.md#bug-overlay-any-level-with-a-defect) (not a separate level).

## Phase → workflow rule ID

Map rule IDs from **`@workflow`** (invoke skill ID in the Playbook column):

| Question-scope phase | Rule ID | Playbook (skill ID) |
| -------------------- | ------- | ------------------- |
| Discover / impact (L4) | — | **`analyze-impact`** in `l4-01` when blast radius unclear; notes feed Prove Regression |
| Spec (L3–L4, large L2) | `design-approval-gate` | `brainstorming` (skip on L2 default; not while scope waits for L — see skill § When NOT) |
| Plan (L3–L4) | `implementation-plan` **or** team plan | `writing-plans` or `architect-plan` |
| Test design (L3–L4 before Code; L2 optional TC rows) | — | `generate-test` — TC table in `l3-02` / `l4-03`; L2: `l2-patch` optional; skip rename/config-only |
| Before Patch/Code (L3: after Test gate, before Code; L2: skip default) | `isolated-workspace` | `using-git-worktrees` (skip when `sp:off` or L2 unless user opts in — see skill § When NOT) |
| Code / Patch | `tdd-during-implementation` (if behavior/contract changes) | `test-driven-development` — L2: after Spec test rows; L3: after `generate-test` + worktree; skip pure rename/config |
| Execute plan (L3–L4) | **Default:** `execute-inline-checkpoints` (B). **ALT:** `execute-via-subagents` (A) — user chose A + `docs/plans/…` from `writing-plans` (not phase-file-only) | `executing-plans` \| `subagent-driven-development` |
| Verify | `verify-before-done` | `verification-before-completion` |
| Review (L2–L3 diff) | — (question-scope Review checklist) | `caveman-review` — terse diff review; log in phase MD |
| Review (L4 pre-merge) | — | `outgoing-code-review` → `requesting-code-review` when formal review before merge |
| Ship (L3–L4) | `finish-branch-options` | `finishing-a-development-branch` |

**Review vs Ship:** `caveman-review` = during/after **Review** step (quick diff pass). `requesting-code-review` = **formal pre-merge** (L4 + supplement **default**; L3 only if AC asks) — **after** `caveman-review`, **before** Ship git options; **not** a second per-task review when execute **A** already used bundled reviewers. **`receiving-code-review`** = **incoming** PR/comment feedback after PR is open (`incoming-code-review`) — verify each item; log rounds in phase **PR feedback**; not a substitute for outgoing review. **Ship phase MD** (`l3-03`, `l4-05`) = rollout/rollback/refine; **`finishing-a-development-branch`** = git integration only — run **after** phase Ship content. Do not skip **`verification-before-completion`** before merge/PR or before claiming fixes addressed.

Run **`superpowers`** (`skill-check-first`) once per session when the supplement applies — **after** level is chosen, not instead of scope options.

## Plan path decision (L3–L4)

Use this table after design approval (`brainstorming` or spec in phase file). **One primary plan location** — link elsewhere; do not duplicate full task lists.

**Numeric pre-flight (skills):** **`architect-plan`** § Pre-flight and **`writing-plans`** § When to use — default escalate to `writing-plans` when **>12** slices/tasks or **>8** primary files, subagents (**A**), or zero-context handoff.

**Terminology:** **slice** (`architect-plan`) = **task** checkbox under `### Tasks` in `l3-01-define.md` / L4 define — not the same as `writing-plans` micro-steps (RED/GREEN).

| Situation | Plan skill | Plan lives at | Execute |
| --------- | ---------- | ------------- | ------- |
| Bounded L3; tasks fit one phase file | **`architect-plan`** | `docs/work/…/l3-01-define.md` (checkbox tasks + paths) | **`executing-plans`** (B) default |
| Many tasks/files; zero-context handoff | **`writing-plans`** | `docs/plans/YYYY-MM-DD-<feature>.md` | User picks **B** or **A** |
| User wants subagents per task | **`writing-plans`** (required) | `docs/plans/…` | **`subagent-driven-development`** (A) |
| L4 large | **`architect-plan`** + often **`writing-plans`** | Phase MD + `docs/plans/…` linked from `STATUS.md` | B and/or A per plan header |

**After `brainstorming`:** default **NEXT** is **`architect-plan`** when question-scope L3 bounded; **`writing-plans`** when the row above requires `docs/plans/…`.

**Rules:**
- Do not run both execute ALT branches on the same plan.
- **Do not** use execute (A) with only **`architect-plan`** and no `docs/plans/…` — **`subagent-driven-development`** requires a task-level plan file.
- **`sp:off`:** team may use **`architect-plan`** only in work folder without worktree/`writing-plans` (see examples below).

## Where files live

| Content | Canonical for question-scope | Superpowers artifact (optional) |
| ------- | ---------------------------- | ------------------------------- |
| STATUS, blockers, commands run, phase state | `docs/work/YYYY-MM-DD-<slug>/` | — |
| Design spec | `l3-01-define.md` / `l4-02-define.md` | `docs/specs/YYYY-MM-DD-<topic>-design.md` (link from work file) |
| Implementation plan | Same phase MD or tasks in plan section | `docs/plans/YYYY-MM-DD-<feature>.md` |

Pick **one** plan/spec tree per repo; do not duplicate without links. See [CONVENTIONS.md](../../CONVENTIONS.md).

## User prompt examples

```text
/question-scope L3 — API export CSV. Superpowers supplement: worktree, inline execute, TDD, verify.
```

```text
/question-scope L4 — Auth migration. Superpowers: full feature flow + subagents. Phased docs/work/.
```

```text
/question-scope L2 — Fix validation on X. Superpowers minimal: TDD + verify only.
```

```text
/question-scope L3 — L3 feature. sp:off — architect-plan in docs/work/, no writing-plans/worktree.
```
