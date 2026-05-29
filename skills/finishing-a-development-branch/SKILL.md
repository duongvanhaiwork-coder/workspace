---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

Implementation done, tests green — present merge / PR / keep / discard; fresh verify per this skill.

### With question-scope

L3–L4 **Ship** after phase rollout/rollback in `l3-03` / `l4-05`; rule **`finish-branch-options`**.

### Combines with (optional)

- `verification-before-completion` — fresh run first
- `receiving-code-review` — after PR open

### Requires (hard)

- Fresh `verification-before-completion` before presenting git options

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Fresh **`verification-before-completion`** before git options | Present merge/PR while tests unverified |
| **MUST read** [ship-process.md](references/ship-process.md) when executing Steps 1–6 | Duplicate ship steps only in chat — follow reference |
| Fill `l3-03` / `l4-05` rollout/rollback when scope on | Skip Ship phase MD when L3–L4 active |
| **NEXT:** **`receiving-code-review`** when PR is open and comments arrive | Confuse with **`requesting-code-review`** (outgoing) |

Red flags: [references/red-flags.md](references/red-flags.md). Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## With question-scope (L3–L4)

Rule ID: **`finish-branch-options`**.

| Layer | Responsibility |
| ----- | ---------------- |
| **Phase Ship MD** (`l3-03-ship.md`, `l4-05-ship.md`) | Refine (no new behavior), rollout/rollback tables, PR links, **`STATUS.md`** complete — **before or while** presenting git options |
| **This skill** | Fresh **`verification-before-completion`** → detect repo/worktree → **user picks one** option → merge / PR / keep / discard → worktree cleanup per option |

Do **not** skip Review or phase Ship content because execute skills finished tasks. **`executing-plans`** / **`subagent-driven-development`** end at “tasks done”; Ship is a separate pipeline step.

**Commits / PR:** create commits or `gh pr create` only when **user or repo policy** allows agent commits and PR creation.

**L4 pre-merge:** When supplement applies, **`requesting-code-review`** should be done (or explicitly waived) before options **merge** or **Push + PR** — after **`caveman-review`** and Verify/Regression green. Fix Critical/Important review findings first.

**Option 2 (Push + PR):** Keep worktree for iteration. When reviewers comment, use **`receiving-code-review`** (`incoming-code-review`) — verify feedback, fix, **`verification-before-completion`**, push; log rounds in `docs/work/…` **PR feedback** section.

## Ship process

**MUST read** when running this skill.

Full detail: [references/ship-process.md](references/ship-process.md).

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes (force) |

## Mistakes and red flags

See [references/red-flags.md](references/red-flags.md).

