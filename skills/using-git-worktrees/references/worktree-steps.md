# Worktree steps 0–3

P4 trim 2026-05-29 — full content preserved in references/

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

