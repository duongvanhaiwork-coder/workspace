# Invocation anti-patterns (shared)

Single source for common **composition** mistakes. Per-skill § **Composition (quick ref)** links here instead of duplicating full tables.

**Authority:** [COMPOSITION.md](../COMPOSITION.md) § Requires (hard) · [CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes.

## Common ✅ / ❌

| Topic | ✅ Do | ❌ Don't |
| ----- | ----- | -------- |
| **Plan size** | ≤12 tasks / ≤8 files → **`architect-plan`** + **`executing-plans` (B)** | **`writing-plans`** when architect pre-flight still fits |
| **Execute A vs B** | **A:** user/plan chose A + `docs/plans/…` from **`writing-plans`** | **A** on architect-only phase file; **B** because `docs/plans/…` exists alone |
| **Brainstorm** | **`brainstorming`** when L3–L4 needs approved spec | **`brainstorming`** for every L2 patch or narrow bug |
| **Worktree** | **`using-git-worktrees`** L3–L4 default before Code | Mandatory on L2, **`sp:off`**, or user decline |
| **Scope vs TDD** | **`test-driven-development`** standalone when behavior changes | Require **`/question-scope`** before every TDD session |
| **Review stack** | **`requesting-code-review`** once per branch (L4) | Per-task **`requesting-code-review`** when **`subagent-driven-development` (A)** already reviewed each task |
| **Impact vs Regression** | **`analyze-impact`** lists scope; Regression runs tests | Claim pass in impact skill; skip **`verification-before-completion`** |
| **Test design vs TDD** | **`generate-test`:** TC + RED in Test phase | Production code in Test phase to green tests |
| **Orchestra vs brainstorm** | **`orchestra-decision`:** fast direction | Orchestra output as approved spec or plan |
| **Commit style** | **`commit-message`** OR **`caveman-commit`** per repo policy | Both templates in one commit |

## Handoff reminders

| After | **NEXT** (typical) |
| ----- | ------------------ |
| **`architect-plan`** | **`executing-plans` (B)** |
| **`writing-plans`** | **`subagent-driven-development` (A)** or **`executing-plans` (B)** if user chose B |
| **`generate-test`** (L3–L4) | **`using-git-worktrees`** → Code + **`test-driven-development`** |
| **`refactor-code`** | **`verification-before-completion`** |
| **`explain-code`** → patch | **`test-driven-development`** |
| **`dispatching-parallel-agents`** | Integrate → **`verification-before-completion`** |

## Scope STOP (when **`/question-scope`** active)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Idea → four options → wait for L1–L4 | **`brainstorming`**, **`writing-plans`**, Code while STOP waits for level |
| Run **`skill-check-first`** after level chosen | Substitute other process skills for the level picker |
