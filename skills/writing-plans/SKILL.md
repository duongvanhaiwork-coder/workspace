---
name: writing-plans
description: >
  Zero-context plans in docs/plans/ for handoff or subagents (A). Standalone or L3-L4 when
  scope active. Prefer architect-plan for bounded work in phase files (B default).
---

# Writing Plans

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User wants a detailed `docs/plans/…` or zero-context handoff — run this skill when pre-flight criteria match; no `/question-scope` required.

### With question-scope

L3–L4 when plan is too large for **`architect-plan`** in phase file, user chose execute **(A)**, or L4 dual plan.

**Plan attach (scope on):** IDE-ALIGNED §1 — no competing `docs/plans/…` unless handoff **(A)** needs a sliced copy.

**Assessment-only:** IDE-ALIGNED §3 — skip until user asks to implement.

### Combines with (optional)

- `executing-plans` (B) or `subagent-driven-development` (A) — after plan
- `brainstorming` — when spec missing

### Requires (hard)

- Approved spec or explicit AC before large `docs/plans/…`

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Large / zero-context `docs/plans/…` + user chose execute **(A)** | Run when **≤12** tasks fit **`architect-plan`** + **`executing-plans` (B)** |
| Approved spec or explicit AC first | `docs/plans/…` alone does not force **A** without user choice |
| **NEXT:** **`subagent-driven-development` (A)** or **`executing-plans` (B)** per plan header | Both A and B on the same plan |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use (and when to stop)

**STOP — do not run this skill** when **all** apply:

- **question-scope** L3 **bounded** (single module/feature, AC in phase file).
- **≤12** implementation tasks and **≤8** primary files to touch.
- Plan can live in `docs/work/YYYY-MM-DD-<slug>/l3-01-define.md` (or L4 define phase summary only).

→ Use **`architect-plan`** on the phase file + **`executing-plans`** (**B**). Do not create `docs/plans/…`.

**Use this skill** when **any** apply:

- User wants **subagent-driven-development** (**A**) — plan file under `docs/plans/` is **required**.
- Large handoff (zero context): many tasks/files, separate session or engineer.
- Multiple subsystems → separate `docs/plans/…` per subsystem (link from `STATUS.md`).
- User explicitly requests `docs/plans/YYYY-MM-DD-<feature>.md`.
- **L4 dual plan:** detail file while phase file keeps summary (see below).

Routing: **`question-scope`** → `references/superpowers-supplement.md` § Plan path decision.

## Prerequisites

- **Approved spec** — AC in phase file and/or `docs/specs/…` after **`brainstorming`** when supplement applies. Do not plan from a blank requirement.
- If spec is missing, **STOP** — complete Spec/`brainstorming` first or ask the user (max 2 blocker questions).

## Without question-scope

- Save to `docs/plans/YYYY-MM-DD-<feature>.md` unless `AGENTS.md` defines another path.
- If the repo uses `docs/work/…` for all work, link the plan from `STATUS.md` when that folder exists.

## `sp:off`

- Use this skill only when pre-flight / user still needs `docs/plans/…` or subagents.
- Otherwise **`architect-plan`** in `docs/work/…` + **`executing-plans`** — no mandatory worktree.

## L4 dual plan

1. **`l4-02-define.md`:** Goal, architecture summary, task IDs (T-n), dependencies, migration/rollback bullets, **links** to plan file(s).
2. **`docs/plans/YYYY-MM-DD-<feature>.md`:** This skill — full steps, code, commands.
3. Header **Spec** and **Work phase** must point to the phase file; phase file links back to this plan.
4. For API or cross-service changes, note **`analyze-impact`** results in the plan **Architecture** section (bounded).

## Overview

Write comprehensive implementation plans assuming the engineer has **zero context**. Per task: files, code, tests, verify commands. Bite-sized steps. DRY. YAGNI. TDD in steps when behavior changes.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context (execution):** Before the first implementation task, run **`using-git-worktrees`** when **question-scope L3–L4** supplement is on (default). **Skip** when **`sp:off`**, **L2**, or the user declined — execute in the current checkout; verify branch + baseline. ([CONVENTIONS.md](../CONVENTIONS.md))

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md` (user/repo overrides allowed).

## Repo conventions (match the target repo)

- **Test runner:** Repo command (`npm test`, `pytest`, `dotnet test`, `go test ./...`, …) — not a default stack.
- **Commit messages:** Team style (`AGENTS.md`, `commit-message`, `caveman-commit`, …).
- **Paths / layout:** Match existing module boundaries.

## Commits in plans

- **Agent must not run `git commit`** unless the user explicitly asked for commits in this session.
- In plan steps, prefer: **"Ready to commit"** with suggested message and paths — or a commit step labeled **(human)**.
- If the user/repo policy allows agent commits, use explicit **Step: Commit** with full command.

## Scope Check

If the spec covers multiple independent subsystems, break into separate plans — one per subsystem. Each plan should produce working, testable software on its own. Link all plans from `STATUS.md`.

## Optional plan review (large plans)

Before execute handoff, for **>8** tasks or L4 detail plans, you may dispatch a reviewer using **`prompts/plan-document-reviewer-prompt.md`** (subagent: verify completeness vs spec, no placeholders). Fix blocking issues before **NEXT: `executing-plans`** or **A**.

## File Structure

Before tasks, map files to create/modify and responsibilities. Lock decomposition here. Follow existing repo patterns; do not unilaterally restructure large files unless the plan includes a justified split.

## Bite-Sized Task Granularity

**Each step is one action (2–5 minutes):** failing test → run fail → implement → run pass → verify/commit-ready.

## Plan Document Header

**Full example (header + one task):** [examples/plan-header-snippet.md](examples/plan-header-snippet.md).

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** **REQUIRES (pick one):** `executing-plans` (**default** under question-scope L3–L4) **or** `subagent-driven-development` (subagents per task). Checkbox (`- [ ]`) steps.

**Goal:** [One sentence]

**Spec:** [path: docs/work/…/l3-01-define.md § Spec, or docs/specs/…-design.md]

**Work phase:** [path: docs/work/…/STATUS.md and define phase file — omit if no work folder]

**Architecture:** [2–3 sentences]

**Tech stack:** [Key technologies]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Traces:** [S1 / A2 / TC-03 — spec or test id]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**
…
- [ ] **Step 5: Ready to commit (human)** or **Commit** if user allows agent commits

```bash
git add <paths>
# git commit -m "<message>"  # only when user requested agent commits
```
````

## No Placeholders

Plan failures — never write: TBD, vague validation, "similar to Task N", steps without code/commands where required, undefined symbols.

## Remember

- Exact file paths; complete code in code steps; exact test commands and expected output.
- Link tasks to spec IDs (**Traces:**) and **TC-xx** when question-scope L3+ applies.
- DRY, YAGNI, TDD in implementation steps — not redundant plan boilerplate.

## Self-Review

1. **Spec coverage** — every requirement has a task.
2. **Placeholder scan** — fix red flags.
3. **Type consistency** — names match across tasks.
4. **Right skill** — if ≤12 tasks, ≤8 files, L3 bounded → should be **`architect-plan`** in phase file instead.
5. **Dual plan** — L4: phase file has summary + links; no duplicate full step lists in both files.

## Execution Handoff

After saving the plan, offer execution **unless** the user already chose in the message or header:

**1. Inline (default)** — **`executing-plans`** (**B**): checkpoints between tasks.

**2. Subagent-driven (A)** — **`subagent-driven-development`**: per task + review between tasks.

| Choice | **REQUIRES** |
| ------ | ------------ |
| Inline (**default**) | **`executing-plans`** |
| Subagent-driven | **`subagent-driven-development`** |

Do not run both on the same plan.

**`docs/plans/` does not imply A:** User may execute this file with **`executing-plans` (B)** unless they chose subagents.

**L3 bounded with AC only in `docs/work/…`:** You should not have run this skill — **`architect-plan`** + **`executing-plans`** on the phase file.

**Test gate (L3–L4):** If tasks assume tests that do not exist yet, **NEXT:** **`generate-test`** in build phase before Code, per **`question-scope`** pipeline.

**After Test design:** If **`generate-test`** already added failing tests for a task, **do not** duplicate RED steps — run those tests (RED), then GREEN per **`test-driven-development`**.
