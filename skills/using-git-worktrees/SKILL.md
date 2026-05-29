---
name: using-git-worktrees
description: >
  Isolated branch/workspace before multi-step implement. Standalone or L3-L4 when scope
  active. Skip L2/L1, sp:off, or user declines. Rule isolated-workspace. NEXT executing-plans
  or subagent-driven-development.
---

# Using Git Worktrees

Portable conventions: [../CONVENTIONS.md](../CONVENTIONS.md). Platform tools: **`superpowers`** → `references/`.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

Rule ID: **`isolated-workspace`** → this skill.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User starts multi-step implementation — run this skill before code; no `/question-scope` required.

### With question-scope

**L3–L4** default before Code (after Plan + Test gate when required); skip when **`sp:off`**, L2, user declines, **`scope:light`**, or assessment-only (**IDE-ALIGNED §3**, **§8**).

### Combines with (optional)

- `executing-plans` or `subagent-driven-development` — after isolation
- `test-driven-development` — during Code

### Requires (hard)

- None

**Instruction precedence** ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes):

1. System/developer constraints  
2. User request (decline worktree = work in place)  
3. **`question-scope`** level + supplement (`sp:off` skips mandatory worktree) — **only when scope active**  
4. This skill  

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| **MUST read** [worktree-steps.md](references/worktree-steps.md) when running Steps 0–3 | Skip provenance / baseline checks summarized in SKILL only |
| **L3–L4** before Code after Plan (+ Test gate when required) | Require worktree on **L2**, **`sp:off`**, or user decline |
| Verify or create isolation before **`executing-plans`** or **`subagent-driven-development`** | Start multi-step Code on shared dirty `main` without asking |
| **NEXT:** `executing-plans` (B) or `subagent-driven-development` (A) | Run during Plan-only phase |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use

| Situation | Run this skill? |
| --------- | ---------------- |
| **L3–L4** before **Code** (or **Patch** on L3 path) | **Yes** (supplement default) — after Plan (+ Test gate when scope requires tests before Code) |
| **`executing-plans`** or **`subagent-driven-development`** about to start | **Yes** — verify or create isolation first |
| User already in linked worktree (Step 0) | **Verify only** — skip create |
| **Standalone** feature (no scope) + multi-step implement | **Yes** — same flow |

**Pipeline position (question-scope L3):**

```text
… → Spec → Plan → [Scaffold] → Test (cases/TC-xx) → 【 worktree 】 → Code → Verify → …
```

Not during **`brainstorming`**, **`architect-plan`**, or **`writing-plans`** (design/plan only). Not while scope waits for **L1–L4** pick.

## When NOT to use

| Situation | Action |
| --------- | ------ |
| **L1** | No implementation |
| **L2** (default supplement) | **Skip** — patch in place on named branch or current checkout; optional ask if change is large |
| **`sp:off` / `no-sp`** | **Skip** unless user asks for worktree |
| User declined isolated worktree | Work in place → Step 2–3 in current directory |
| **Meta / `quick:`** | N/A |

**L2 high-risk patch** (shared lib, auth): user may escalate to L3 or explicitly request worktree — then run this skill.

## `sp:off`

Supplement off → **do not** require worktree before Code. **`executing-plans`** may run in current checkout. User can still opt in (Step 0 ask once).

## Overview

Ensure work happens in an **isolated workspace** before implementation.

**Core principle:** Detect existing isolation → native worktree tools → git worktree fallback. Never fight the harness.

**Worktree root:** Project-local **`.worktrees/`** (preferred) or **`worktrees/`** at the **git repo root** you are changing.

**Monorepo / AI Core workspace:** Run git commands in **`<target-repo>`** (the app repo under `projects/…`), not the meta `Workspace/` root unless that is the repo being edited.

## Worktree steps (0–3)

**MUST read** when executing this skill.

Full detail: [references/worktree-steps.md](references/worktree-steps.md).

## Integration

| When | Skill / rule |
| ---- | ------------- |
| **question-scope L3–L4** before Code/Patch | **`isolated-workspace`** → this skill |
| Before **`executing-plans`** or **`subagent-driven-development`** | Create or verify isolation (unless `sp:off` + user works in place) |
| After **`writing-plans`** / approved plan | Run before first implementation task |
| When done (L3–L4) | Verify/Regression → Review → **`l3-03-ship.md`** / **`l4-05-ship.md`** → **`finishing-a-development-branch`** (merge / PR / cleanup) |

**REQUIRES:** none (entry skill for isolated execution).

**NEXT (typical):** **`executing-plans`** (**B**) or **`subagent-driven-development`** (**A**) after baseline is green.

## Quick reference

| Situation | Action |
| --------- | ------ |
| Already in linked worktree | Skip Step 1 |
| Submodule | Not a worktree; Step 1 may apply |
| Native worktree tool | Step 1a only |
| No native tool | Step 1b |
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Prefer `.worktrees/` |
| Directory not ignored | Fix `.gitignore` before `worktree add` |
| Sandbox blocks `worktree add` | Work in place; report |
| Tests fail at baseline | Report; ask |
| **L2 / `sp:off`** | Skip unless user opts in |
| **Wrong git root** | `cd` to `<target-repo>` first |

## Mistakes and red flags

See [references/red-flags.md](references/red-flags.md).

