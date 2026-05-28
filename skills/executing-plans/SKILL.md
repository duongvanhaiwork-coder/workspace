---
name: executing-plans
description: >
  Use when you have a written implementation plan to execute with inline checkpoints
  (same or new session). Default execute path (B) under question-scope L3–L4 unless
  user chooses subagent-driven-development (A). Pair with architect-plan phase files
  or docs/plans from writing-plans.
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** This path works without subagents (inline checkpoints in the current or a resumed session). Under **question-scope L3**, this is the default **execute-inline-checkpoints (B)** path unless the user chose **writing-plans** + subagents (A). If your platform supports **subagent** dispatch and a task-level `docs/plans/…` file exists, **`subagent-driven-development`** is the ALT when the supplement table or user requests it.

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

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRES:** `finishing-a-development-branch`
- Follow that skill to verify tests, present options, execute choice

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
- **REQUIRES:** `using-git-worktrees` — isolated workspace (create or verify)
- **REQUIRES (plan):** A written plan with executable tasks — from **`writing-plans`** (`docs/plans/…`) **or** **`architect-plan`** in `docs/work/…` (default L3 **B** path; see **`question-scope`** → `references/superpowers-supplement.md`)
- **NEXT:** `finishing-a-development-branch` — after all tasks
