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

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use [plan-output-guide.md](references/plan-output-guide.md) for paths, phase mapping, TDD handoff | **`subagent-driven-development` (A)** without `docs/plans/…` from **`writing-plans`** and explicit user/plan choice |
| Bounded plan in `docs/work/…` with `### Tasks` → **`executing-plans` (B)** | Duplicate full RED/GREEN in phase file when they live in `docs/plans/…` |
| Stay in phase file when pre-flight ≤12 tasks / ≤8 files | **`writing-plans`** when the plan still fits architect-plan pre-flight |
| Escalate to **`writing-plans`** when over pre-flight limits | Invent micro-steps only to satisfy executing-plans checkpoints |

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

## Plan output (paths, phase mapping, L4, TDD handoff)

Full detail: [references/plan-output-guide.md](references/plan-output-guide.md).

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
