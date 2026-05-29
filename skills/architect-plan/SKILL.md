---
name: architect-plan
description: >
  Bounded implementation plans in phase files or chat. Standalone or L3 Plan when scope
  active. Escalate to writing-plans for large handoff or subagents. Pair with executing-plans (B).
---

# Architect Plan

**Announce when applying:** `Using architect-plan for <feature/slug>.`

**Stop when:** Plan has scope, dependencies (if any), DoD per slice/task, test traceability (L3+), and open uncertainties — then hand off per [Handoff](#handoff).

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User wants a bounded plan for a feature — write tasks in chat, `docs/plans/…`, or a work folder the user names; no `/question-scope` required.

### With question-scope

L3–L4 Plan phase — checkbox tasks in `l3-01-define.md` (or L4 define); escalate to **`writing-plans`** when pre-flight fails.

### Combines with (optional)

- `brainstorming` — when spec not approved
- `executing-plans` (B) — after plan
- `writing-plans` — when pre-flight escalates

### Requires (hard)

- Spec / AC before planning (existing spec, brainstorming, or user AC)

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).
See [CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes.

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bounded plan in `docs/work/…` with `### Tasks` → **`executing-plans` (B)** | **`subagent-driven-development` (A)** without `docs/plans/…` from **`writing-plans`** and explicit user/plan choice |
| Stay in phase file when pre-flight ≤12 tasks / ≤8 files | **`writing-plans`** when the plan still fits architect-plan pre-flight |
| Escalate to **`writing-plans`** when over pre-flight limits | Duplicate full RED/GREEN in the phase file when they live in `docs/plans/…` |

**REQUIRES:** spec / AC · **NEXT:** `executing-plans` (B) default · **ALT:** `writing-plans` → `subagent-driven-development` (A)

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## Prerequisites (before planning)

- **Spec / AC exists** in the phase file (or linked spec) — do not plan on a vague idea alone; use **`orchestra-decision`** first under **`question-scope`**, then return here.
- **L3–L4 with Superpowers supplement (default):** Design is approved — spec in phase file and/or `docs/specs/YYYY-MM-DD-<topic>-design.md` after **`brainstorming`** when `design-approval-gate` applies. **REQUIRES:** approved spec content, not a blank Plan section.
- **L2:** No Plan step — AC + patch notes in `l2-patch.md` only; do not run this skill.

## Terminology

| Term | Meaning |
| ---- | ------- |
| **Slice** | One implementable unit in this skill (file(s) + DoD + verify). |
| **Task** | Same unit when written under `### Tasks` in `l3-01-define.md` / L4 define phase. |

One slice → one checkbox under **### Tasks** in the phase template.

## Pre-flight (choose this skill or escalate)

Use **`architect-plan`** when **all** are true:

- Spec/AC exists (see Prerequisites).
- Work fits **one** phase file in `docs/work/…` (roughly **≤12** slices/tasks, **≤8** primary files).
- Default execute is **`executing-plans`** (B) in the same or resumed session.

**NEXT: `writing-plans`** when **any** apply:

- User wants **subagents per task** (**A**) — requires `docs/plans/YYYY-MM-DD-<feature>.md`.
- **>12** slices/tasks or **>8** primary files and a zero-context handoff.
- Multiple independent subsystems that each need their own plan file.
- User explicitly asks for `docs/plans/…`.

Link from the phase file to `docs/plans/…`; do not duplicate full task lists in both places.

**Gray zone:** Complex slices (auth, migration) count as 2 toward the limit only when they clearly need separate PRs or sessions — use judgment; prefer escalate if the phase file would exceed ~80 lines of tasks.

## Without question-scope

When scope is off (`qs:off`, `quick:`, or no `/question-scope`):

- Prefer `docs/work/YYYY-MM-DD-<slug>/` + phase file if the repo uses that layout (`AGENTS.md`).
- Otherwise a short plan in `docs/plans/…` may use **`writing-plans`** instead — do not force architect-plan if there is no work folder convention.

## `sp:off` (supplement off, scope on)

- Still use this skill for bounded Plan in `docs/work/…`.
- **Do not** require **`using-git-worktrees`** or **`writing-plans`** unless the user asks.
- Handoff: **`executing-plans`** (B) on the phase file unless user requests subagents → then **`writing-plans`** + **A**.

## Mindset

You are helping a human think through a problem before writing code.
Your job is to surface risks and dependencies they might miss, not to fill in a template.
Scale your effort to the problem — a one-file fix needs a one-line plan.

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

## What NOT to do

- Don't over-plan trivial changes.
- Don't invent risks that aren't there.
- Don't prescribe solutions you're not confident about.
- Don't assume your plan is complete — use **## Open questions**.
- Don't write full `docs/plans/…` RED/GREEN here when pre-flight says stay on architect-plan.

## Self-review (before handoff)

1. **AC coverage:** Each `Then` / AC row maps to a task or **TC-xx**.
2. **Order:** Dependencies noted in **### Plan checklist** or task text.
3. **Paths:** Every task names files (no vague "update service").
4. **Phase template:** **Done when** checkboxes satisfied for L3/L4.
5. **Escalation:** Over pre-flight limits → **NEXT: `writing-plans`**.

## Handoff

| Situation | **NEXT** |
| --------- | -------- |
| L3 bounded, plan in phase file | **`executing-plans`** (**B**) — after **Test** gate if scope requires test cases before Code |
| Subagents or `docs/plans/…` | **`writing-plans`** → **`subagent-driven-development`** (**A**) |
| Tests not yet written | **`generate-test`** (L3 **Test** phase) before **Code** when AC demands new tests |

Update `STATUS.md` (`current_phase`, links to plan/spec, `next_actions`).

## After implementation

If the plan contained critical tasks, add a Human Todo suggesting retrospective.
Do NOT auto-run retrospective — the human decides when to reflect.
Most plans won't need it.
