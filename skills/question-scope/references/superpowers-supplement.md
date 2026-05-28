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
| Spec (L3–L4, large L2) | `design-approval-gate` | `brainstorming` |
| Plan (L3–L4) | `implementation-plan` **or** team plan | `writing-plans` or `architect-plan` |
| Before Patch/Code | `isolated-workspace` | `using-git-worktrees` |
| Code / Patch | `tdd-during-implementation` | `test-driven-development` |
| Execute plan (L3–L4) | **Default L3:** `execute-inline-checkpoints` (B). **ALT:** `execute-via-subagents` (A) — requires `writing-plans` plan file | `executing-plans` \| `subagent-driven-development` |
| Verify | `verify-before-done` | `verification-before-completion` |
| Ship (L3–L4) | `finish-branch-options` | `finishing-a-development-branch` |

Run **`superpowers`** (`skill-check-first`) once per session when the supplement applies — **after** level is chosen, not instead of scope options.

## Plan path decision (L3–L4)

Use this table after design approval (`brainstorming` or spec in phase file). **One primary plan location** — link elsewhere; do not duplicate full task lists.

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
level L3 — API export CSV. Superpowers supplement: worktree, inline execute, TDD, verify.
```

```text
level L4 — Auth migration. Superpowers: full feature flow + subagents. Phased docs/work/.
```

```text
level L2 — Fix validation on X. Superpowers minimal: TDD + verify only.
```

```text
sp:off — L3 feature, team plan only (architect-plan), no writing-plans/worktree.
```
