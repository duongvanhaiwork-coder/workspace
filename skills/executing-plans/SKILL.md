---
name: executing-plans
description: >
  Execute a written plan with inline checkpoints (same or new session). Standalone or
  default execute (B) under question-scope L3–L4 unless user chooses subagent-driven-development (A).
  Plan from architect-plan phase file or docs/plans from writing-plans.
---

# Executing Plans

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User provides or points to a plan (`docs/plans/…`, phase file, or checklist in chat) — execute with inline checkpoints; no `/question-scope` required.

### With question-scope

Default **execute (B)** for L3–L4 when scope active; plan from **`architect-plan`** phase or **`writing-plans`**; honor `docs/work/…` and Verify/Regression gates.

### Combines with (optional)

- `architect-plan` or `writing-plans` — plan source
- `using-git-worktrees` — before implement (optional)
- `test-driven-development` — per task when behavior changes
- `verification-before-completion` — per task and before done
- `finishing-a-development-branch` — after all tasks

### Requires (hard)

- Written plan with executable tasks (chat, `docs/plans/…`, or phase `### Tasks`)

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).
See [CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes.

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| **`architect-plan`** phase `### Tasks` + inline checkpoints (**B**, default L3) | **`subagent-driven-development` (A)** on architect-plan-only phase file (no `docs/plans/…`) |
| Execute `docs/plans/…` with **B** when user or plan header chose B | Treat `docs/plans/…` alone as auto-selecting **A** |
| **`verification-before-completion`** per task and before done | Claim done / phase complete without fresh command output |
| One checkpoint = one task slice + TDD inside the slice | Invent micro-steps in a phase file to mimic **`writing-plans`** |

**REQUIRES:** written plan with executable tasks · **NEXT:** `verification-before-completion` → `finishing-a-development-branch` · **ALT:** `subagent-driven-development` (A) when `docs/plans/…` exists and user/plan explicitly chose A

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Inline checkpoints in the **same or resumed session** (no subagent per task). Under **question-scope L3–L4**, this is the default **execute-inline-checkpoints (B)** unless the user or plan header chose **`subagent-driven-development` (A)**. Having `docs/plans/…` from **`writing-plans`** does **not** auto-select A — **B** may still execute that file. Use **A** only when explicitly chosen and `docs/plans/…` exists.

## The Process

### Step 1: Load and Review Plan

**Plan source (one of):**
- `docs/plans/YYYY-MM-DD-<feature>.md` from **`writing-plans`**, or
- **`architect-plan`** output in `docs/work/YYYY-MM-DD-<slug>/` phase file (`l3-01-define.md`, L4 define phase, etc.) with checkbox tasks and file paths

1. Read the active plan (file above)
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create **task-tracker** items and proceed (map per `superpowers/references/`)

### Step 2: Execute Tasks

### Plan source (B)

| Source | One checkpoint = | Typical L3 path |
| ------ | ------------------ | --------------- |
| **`architect-plan`** (phase `### Tasks`) | One checkbox (T-n: files, DoD, **verify:**) + **`test-driven-development`** inside the slice | Bounded L3 default |
| **`writing-plans`** (`docs/plans/…`) | Follow micro-steps (RED/GREEN, commands) in each ### Task — skip duplicate RED if **`generate-test`** already added tests | Large plan / user chose `docs/plans/` but execute **B** |

Do not invent micro-steps in a phase file to mimic `writing-plans` — checkpoints stay **tasks** for **`architect-plan`**.

For each task:
1. Mark as in_progress
2. Follow steps (micro-steps **or** slice DoD + TDD as above)
3. Run **verify:** from the task line or plan step
4. Mark as completed

### Step 3: Execute complete (not Ship yet)

After all plan tasks are complete and each task’s **verify:** passed:

**L3–L4 (question-scope):** do **not** jump straight to Ship. Order:

1. **Verify + Regression** in `l3-02-build-prove.md` / `l4-04-prove.md` — **`verification-before-completion`**
2. **Review** — `caveman-review` (L4 + supplement: add **`requesting-code-review`** formal pre-merge unless waived)
3. **Ship phase file** — `l3-03-ship.md` / `l4-05-ship.md` (refine, rollout, rollback, links)
4. **`finishing-a-development-branch`** — fresh test run + merge / PR / keep / discard

**L2:** scoped Verify in `l2-patch.md`; full Ship ceremony only when escalated to L3 or AC requires it.

When Ship applies, announce: "I'm using the finishing-a-development-branch skill to complete this work."

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **REQUIRES:** `using-git-worktrees` — isolated workspace (create or verify) **unless** **`sp:off`** / user declined worktree / **L2** — then verify branch and baseline in place
- **REQUIRES (plan):** A written plan with executable tasks — from **`writing-plans`** (`docs/plans/…`) **or** **`architect-plan`** in `docs/work/…` (default L3 **B** path; see **`question-scope`** → `references/superpowers-supplement.md`)
- **REQUIRES:** `test-driven-development` — during each task when behavior/contract changes (skip pure rename/config per skill § When NOT)
- **REQUIRES:** `verification-before-completion` — after each task verification and before “done”
- **NEXT (L3–L4):** Verify/Regression → Review → phase Ship MD → **`finishing-a-development-branch`**
