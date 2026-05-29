# Worktree mistakes and red flags

Moved from `using-git-worktrees/SKILL.md` (2026-05-29).

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
