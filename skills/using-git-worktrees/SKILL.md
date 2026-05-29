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

**L3–L4** default before Code (after Plan + Test gate when required); skip when **`sp:off`**, L2, or user declines.

### Combines with (optional)

- `executing-plans` or `subagent-driven-development` — after isolation
- `test-driven-development` — during Code

### Requires (hard)

- None

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

1. System/developer constraints  
2. User request (decline worktree = work in place)  
3. **`question-scope`** level + supplement (`sp:off` skips mandatory worktree) — **only when scope active**  
4. This skill  

See [CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes.

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
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

## Step 0: Detect existing isolation

**Before creating anything**, check whether you are already in a linked worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside submodules. Before treating that as a worktree:

```bash
git rev-parse --show-superproject-working-tree 2>/dev/null
```

If this prints a path, you are in a **submodule** — treat as a normal repo (Step 1 may apply).

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** Already isolated. **Skip Step 1** → go to Step 2.

Report:

- On a branch: `Already in isolated workspace at <path> on branch <name>.`
- Detached HEAD: `Already in isolated workspace at <path> (detached HEAD). Branch may be needed at finish time.`

**If `GIT_DIR == GIT_COMMON` (or submodule):** Normal checkout.

Ask once unless instructions already declare a preference:

> Would you like an isolated worktree? It keeps your current branch unchanged.

If the user declines, work in place → Step 2 (setup in current directory).

## Step 1: Create isolated workspace

Try **1a** first; use **1b** only when no native worktree tool exists.

### 1a. Native worktree tools (preferred)

If the platform exposes worktree creation (`EnterWorktree`, `WorktreeCreate`, `/worktree`, `--worktree`, Cursor worktree flow, etc.), **use it** and go to Step 2.

Do **not** run `git worktree add` when a native tool exists — the harness may not see manual worktrees.

### 1b. Git worktree fallback

Use only when **1a** does not apply.

#### 1. Directory (project-local only)

Priority: user/team instruction (`AGENTS.md`, message) → existing `.worktrees/` → existing `worktrees/` → create **`.worktrees/`**.

```bash
ROOT=$(git rev-parse --show-toplevel)
if [ -d "$ROOT/.worktrees" ]; then
  WORKTREE_DIR=".worktrees"
elif [ -d "$ROOT/worktrees" ]; then
  WORKTREE_DIR="worktrees"
else
  WORKTREE_DIR=".worktrees"
fi
```

#### 2. Ignore check (required before first create)

```bash
git -C "$ROOT" check-ignore -q "$WORKTREE_DIR" || {
  echo "$WORKTREE_DIR/" >> "$ROOT/.gitignore"
  git -C "$ROOT" add .gitignore
}
```

**Commit `.gitignore` only when the user explicitly asks** (or team convention requires it). Otherwise leave staged/uncommitted and tell the user: *"Added `$WORKTREE_DIR/` to `.gitignore` — commit when ready."*

If hooks block staging, still ensure the path is listed and `git check-ignore -q "$WORKTREE_DIR"` passes before `worktree add`.

#### 3. Branch name

Derive `BRANCH_NAME` from the plan, ticket, or feature slug (kebab-case). Never implement on `main` / `master` without explicit user consent.

#### 4. Create and enter

```bash
BRANCH_NAME="<feature-branch>"   # required — set from plan / user
path="$ROOT/$WORKTREE_DIR/$BRANCH_NAME"
mkdir -p "$ROOT/$WORKTREE_DIR"
git -C "$ROOT" worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Sandbox fallback:** If `git worktree add` fails (permissions), say the sandbox blocked creation, stay in the current directory, and continue Step 2–3 there.

## Step 2: Project setup

From the **active workspace root** (worktree or main checkout):

```bash
if [ -f package.json ]; then npm install; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi
if [ -f go.mod ]; then go mod download; fi
```

Skip installs when no manifest exists.

## Step 3: Verify clean baseline

Run the project’s test command (from README, `AGENTS.md`, or CI config):

```bash
# examples — use the repo’s real command
npm test
# cargo test
# pytest
# go test ./...
```

- **Failures:** Report output; ask whether to proceed or fix baseline first.
- **Pass:** Report ready.

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

Update **`STATUS.md`** when question-scope is active: note branch path, baseline command, pass/fail.

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

## Common mistakes

| Problem | Fix |
| ------- | --- |
| `git worktree add` while native tool exists | Step 1a first |
| Nested worktree inside worktree | Step 0 every time |
| Tracked worktree files | `git check-ignore` before create |
| Wrong directory | Project-local only; team doc → `.worktrees/` |
| Implement on `main` | Named feature branch + user consent |
| Skip baseline tests | Step 3 required |
| Worktree during Plan/Spec only | Wait until before Code |
| Worktree at Workspace root | Use app repo under `projects/…` |

## Red flags

**Never:**

- Create a worktree when Step 0 shows existing isolation
- Skip 1a when a native worktree tool is available
- Create project-local worktree without ignore verification
- Proceed past failing baseline tests without asking
- Require worktree on L2 default path without user opt-in

**Always:**

- Step 0 → 1a → 1b (only if needed) → 2 → 3
- Prefer `.worktrees/` at repo root for new dirs
- Hand off cleanup to **`finishing-a-development-branch`**
