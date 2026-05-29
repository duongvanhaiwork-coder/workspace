# Plan output paths, phase mapping, L4 dual plan, execute vs TDD

P4 trim 2026-05-29 — full content preserved in references/

## Where to write the plan

When **question-scope** is active, put the plan in the work folder phase file (do not duplicate full AC elsewhere). See **`question-scope`** → [Plan path decision (L3–L4)](../question-scope/references/superpowers-supplement.md#plan-path-decision-l3l4):

| Level | Default path |
| ----- | ------------ |
| L3 | `docs/work/YYYY-MM-DD-<slug>/l3-01-define.md` under **## Plan** (pair with **execute-inline-checkpoints**) |
| L4 | `docs/work/YYYY-MM-DD-<slug>/l4-02-define.md` — summary + task IDs; detail may live in `docs/plans/…` (see [L4 dual plan](#l4-dual-plan)) |

Use **`writing-plans`** → `docs/plans/YYYY-MM-DD-<feature>.md` only when pre-flight says escalate. Link from the phase file and `STATUS.md`.

**Example (bounded L3 phase plan):** [examples/l3-bounded-plan-snippet.md](examples/l3-bounded-plan-snippet.md).

### Map into phase templates

Write into the existing **## Plan** section — do not invent parallel headings.

**L3 (`l3-01-define.md`):**

- **### Architecture (bounded)** — 2–5 bullets (approach, boundaries).
- **### Tasks** — one checkbox per slice: `[ ] T-n: <files> — <DoD> — verify: <command or TC-id>`.
- **### Plan checklist** — complete template items (order, dependencies, rollback sketch).
- **## Done when** — every critical `Then` → **TC-xx** reserved or linked; plan frozen; `STATUS.md` → `l3-02-build-prove.md`.

**L4 (`l4-02-define.md`):**

- Map each P0 **A\*** row to task ID (e.g. T-3) in **### Tasks**.
- Complete **Done when** (P0 → planned TC IDs).

## L4 dual plan

When L4 is large but still uses architect-plan for the frame:

1. **Phase file (`l4-02-define.md`):** Goal, architecture summary, ordered **### Tasks** with IDs, dependencies, rollback/migration one-liners, links only.
2. **`docs/plans/YYYY-MM-DD-<feature>.md`:** Full task steps from **`writing-plans`** when handoff or **>12** tasks — link **both ways** from phase file and `STATUS.md`.
3. Do not duplicate full RED/GREEN steps in the phase file if they live in `docs/plans/…`.

**Before locking public API / cross-service tasks:** run **`analyze-impact`** (bounded) and note impacted surfaces in **### Architecture** or task notes.

## Context (question-scope JIT)

- Read only what Spec and the task list require — **impacted module + 1-hop** callers ([**question-scope**](../question-scope/SKILL.md#progressive-context-jit) budgets).
- List paths you will open in the plan **before** reading file 4+ in one turn when practical.
- If scope is unclear after Spec, ask the user (max **2** specific questions) before expanding search.

## What to think about

1. **Scope**: What is actually changing? Read the codebase to understand, don't guess.

2. **Dependencies**: Which files/modules depend on each other?
   Sequential vs parallel — state reasoning.

3. **Definition of Done**: Per slice/task — one sentence; add rollback or perf targets when stakes justify it.

4. **Risks**: Only real production/data/security/perf risks — brief + mitigation if known.

5. **Auth / PII / migration**: Name explicitly when in scope (rule **`code-standards`** applies at implementation).

## Minimal output (mental model)

Use sections below inside the phase **## Plan** block — omit empty parts for trivial work.

| Section in phase file | Content |
| --------------------- | ------- |
| **### Architecture (bounded)** | Short approach |
| **### Tasks** | Checkboxes with T-n, files, DoD, **verify:** |
| **### Plan checklist** | Template checkboxes |
| **## Open questions** | Uncertainties |

**Per-task line shape:**

```markdown
- [ ] T-1: `src/foo.ts` — add validation for phone — verify: `npm test -- foo` or TC-01
```

For a one-file fix: one task line is enough.

## Execute (B) vs TDD — no RED/GREEN here

This skill does **not** write bite-sized RED/GREEN steps (that is **`writing-plans`**).

| Phase | Skill / action |
| ----- | ---------------- |
| **Plan (now)** | Slices/tasks + **verify:** (command, smoke, or **TC-xx** id) |
| **Test (L3–L4 gate, before Code)** | Reserve/link **TC-xx** for each critical `Then`; **`generate-test`** in `l3-02` / `l4-03` when cases need authoring |
| **Code / execute B** | **`executing-plans`** treats each checkbox as one checkpoint; **`test-driven-development`** during implementation when behavior changes |

Do not invent micro-steps in the phase file to satisfy executing-plans — checkpoints are **tasks**, TDD runs inside each task during Code.

