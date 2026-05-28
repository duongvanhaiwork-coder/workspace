---
name: question-scope
description: >
  Scope Level workflow (L1–L4) for Cursor and Kiro. Triggers on /question-scope,
  level Lx, or ? + dev keyword only when leading-? or keyword-first (see skill body).
  Opt-out: qs:off, no-scope, quick:, sp:off. User picks level via options; then runs pipeline
  (Answer/Patch/Feature/Full Flow). Phased MD work folders for long sessions.
---

# Question Scope

Cursor + Kiro share this skill. **Difference:** Cursor may use `AskQuestion` for level pick; Kiro uses the same labels in a numbered markdown list — wait for `L1`…`L4` or `level Lx`.

## Contents

- [Instruction precedence](#instruction-precedence)
- [When this skill applies](#when-this-skill-applies)
  - [Opt-out tokens](#opt-out-tokens-canonical-same-meaning-in-rulescursorworkflowmdc)
- [Output header](#output-header-after-level-is-chosen)
- [Session continuity (L2–L4)](#session-continuity-phased-md-files-l2l4)
- [Scope Level — user chooses](#scope-level-user-chooses-do-not-auto-lock)
  - [Suggest heuristic](#suggest-heuristic-not-a-decision)
  - [Level boundaries](#level-boundaries-heuristic-user-may-override)
- [Pipelines (UI)](#pipelines-ui)
  - [L1 playbook](#l1-playbook)
  - [L2 playbook](#l2-playbook)
  - [L3 playbook](#l3-playbook)
  - [L4 playbook (15 steps)](#l4-playbook-full-flow-15-steps)
- [Verify vs Regression vs Iterate](#verify-vs-regression-vs-iterate)
- [Context budgets](#context-budgets)
- [Gates](#gates)
- [Bug overlay](#bug-overlay-any-level-with-a-defect)
- [Code policy (L2–L4)](#code-policy-l2l4)
- [Review checklist (L2+)](#review-checklist-l2)
- [Definition of Done](#definition-of-done)
- [Superpowers supplement](#superpowers-supplement-optional-playbook-layer)
  - [By level](#by-level)
  - [Phase → workflow rule ID](#phase-workflow-rule-id)
  - [Plan choice (L3–L4)](#plan-choice-l3l4)
  - [Where files live](#where-files-live)
  - [User prompt examples](#user-prompt-examples)
- [Related skills](#related-skills)
- [Token depth](#token-depth)

## Instruction precedence

1. System/developer constraints
2. User request (`level Lx` overrides everything)
3. This skill (pipelines, gates, work-folder layout only)
4. **`general.mdc` and stack `*.mdc` are canonical** for code style, architecture, security, SOLID, size limits, and API conventions — this skill **does not redefine** those; keep them in the rules files only.

## When this skill applies

Activate only when a trigger matches. Otherwise respond normally.

| Priority | Trigger                                      | Action                                         |
| -------- | -------------------------------------------- | ---------------------------------------------- |
| 1        | `level L1`…`L4`, `/question-scope L2`   | Skip options → run pipeline for that level     |
| 2        | `/question-scope` (no level)            | Idea → suggest level → **4 options** → STOP    |
| 3        | `?` + dev keyword (see **tight match** below) | Same as `/question-scope` (row 2)              |
| —        | Body contains `qs:off`, `no-scope`, or `quick:` (case-insensitive) | Do **not** activate question-scope (see **Opt-out tokens** below) |
| —        | Body contains `sp:off` or `no-sp` (case-insensitive) | Skip Superpowers supplement only; scope still applies |
| —        | `?` alone ("ok?", "done?")                  | Do **not** activate                          |
| —        | `?` + dev keyword but **not** a tight match | Do **not** activate; answer in chat (user may send `/question-scope` or `level Lx`) |

### Opt-out tokens (canonical — same meaning in `rules/workflow.mdc`)

| Token | Question-scope | Superpowers supplement |
| ----- | ---------------- | ------------------------ |
| `qs:off`, `no-scope` | Off | Off (no Lx → no supplement map) |
| **`quick:`** | Off — fast path, **no** L1–L4 options, **no** phased `docs/work/` | Off |
| `sp:off`, `no-sp` | On | Off |
| `level Lx` | On (skip level picker) | Per level table below |

**`quick:` is not** “skip design/plan only” while scope runs — use **`sp:off`** for that. **`quick:`** = normal chat + `general.mdc` / stack rules; trivial edits only.

**Tight match for priority 3:** After trim, the message must contain `?` **and** a dev keyword **and** **either**:

- **Leading question:** the first character is `?`, or
- **Keyword-first:** the first alphanumeric token (split on spaces/punctuation) equals a dev keyword (case-insensitive).

So trailing-only rhetorical questions with a keyword buried inside (e.g. reassurance after a long sentence) do **not** trigger this skill.

**Tests (when logic lives in a product repo):** This skill is **Markdown-only** here. If you implement these triggers or gates **in application code** (router, middleware, CLI, bot, …), add **automated tests only in the repository you are changing** — not under `skills/`. **Discover what that repo already uses:** `package.json` / `pyproject.toml` / `pom.xml` / `*.csproj`, existing `test/` or `tests/` layout, runner scripts, and CI config — then add tests **in the same language, framework, folder naming, and style** (imports, fixtures, describe/it vs test_, etc.). Cover at least: explicit `level Lx` / `/question-scope`, tight-match vs non-match, and opt-outs (`qs:off`, `no-scope`, `quick:`). Follow `general.mdc` testing expectations; use **`generate-test`** if you need help mirroring that repo’s patterns.

**Dev keywords (examples):** fix, add, change, implement, refactor, explain, why, naming, compare, design, api, bug, test, migrate, module, endpoint, worker.

**Vague idea (no problem statement):** Run [orchestra-decision](../orchestra-decision/SKILL.md) first, then return to scope options.

## Output header (after level is chosen)

```text
Level: L2 | Pipeline: Context → Spec → Patch → Verify → Review → MD
```

List canonical steps 1–15 only for **L4** or when the user asks.

## Session continuity — phased `.md` files (L2–L4)

**Problem:** Long sessions lose chat context.

**Approach:** One **work folder** per task: `docs/work/YYYY-MM-DD-<slug>/` with **`STATUS.md`** (always read first in a new session) + **one file per phase**. Chat is ephemeral; **files are the source of truth** for decisions, AC, commands run, blockers.

**Doc root (repo-specific):** Prefer `docs/work/...` under the repo root when `docs/` already exists or the team allows creating it. If `docs/` is absent, gitignored, or policy forbids it: **ask once** or use an existing doc area (`specs/`, `design/`, `notes/`, `documentation/`, `.github/`, etc.) and place the **same** folder shape there: `<doc-root>/work/YYYY-MM-DD-<slug>/` with `STATUS.md` + phase files. For **L1** optional archives, mirror the same root (`docs/answers/` or `<doc-root>/answers/`). Do not silently write outside the open repo without user confirmation.

**Convention:** See [templates/phases/README.md](templates/phases/README.md).

| Level | Files |
| ----- | ----- |
| L2 | `STATUS.md` + `l2-patch.md` ([templates/phases/l2](templates/phases/l2)) |
| L3 | `STATUS.md` + `l3-01-define.md` … `l3-03-ship.md` ([templates/phases/l3](templates/phases/l3)) |
| L4 | `STATUS.md` + `l4-00-frame.md` … `l4-05-ship.md` ([templates/phases/l4](templates/phases/l4)) |

**Agent rules:**

1. After **choosing level** (L2–L4), create the folder and copy/adapt templates; fill **`STATUS.md`** (`current_phase`, **5-line summary**, links, `next_actions`).
2. **End of each phase:** mark phase file state, update `STATUS.md`, then open/create the **next** phase file (default: create phase file **when entering** that phase — avoids empty shells).
3. **New session / compaction:** User `@`mentions `STATUS.md` + current phase file first — do not re-derive from chat alone.
4. L1 stays light: single optional `docs/answers/...` ([l1/answer.md](templates/phases/l1/answer.md)) or the same under your chosen **doc root**; phased folder **not** required.

**Single-file alternative:** For tiny L2, `docs/work/YYYY-MM-DD-<slug>.md` (or the same path under your chosen **doc root**) only ([rollup/work-item.md](templates/phases/rollup/work-item.md)) is still allowed; use phased folder when the task may span multiple sessions.

## Scope Level — user chooses (do not auto-lock)

1. **Idea** (2–4 lines): problem + expected outcome.
2. **Suggest** one line: `Suggest: Lx — <short reason>` (heuristic only).
3. **Present 4 options** — then **STOP** (no Context / Spec / Patch / Code until chosen):

| ID  | Label                                                         |
| --- | ------------------------------------------------------------- |
| L1  | Chat Answer — explain / naming / compare; no repo edits       |
| L2  | Patch — change existing code (few files)                      |
| L3  | Small Feature — new module/API/worker (bounded)               |
| L4  | Large System — multi-service, MCP, AI platform, big migration |

- **Cursor:** use `AskQuestion` with these four options when the tool is available.
- **Kiro / fallback:** numbered markdown list; accept `L2`, `choose L3`, etc.

**Skip options** if user already set level (priority 1).

**Sticky scope:** Keep the chosen level for the rest of the task until done or user sends `/question-scope` / `level Ly`. Do not re-ask every turn.

**Escalation L2 → L3:** Stop Patch; explain why; re-present options (at least L2 vs L3); continue only after user confirms.

### Suggest heuristic (not a decision)

| Signal                                   | Suggest |
| ---------------------------------------- | ------- |
| No code change, explain/compare          | L1      |
| Specific files, fix/field/validation     | L2      |
| New module/API/worker/migration          | L3      |
| Multi-service, MCP, AI infra, large auth | L4      |

### Level boundaries (heuristic — user may override)

| Situation | Typical level | Lighter option |
| --------- | ------------- | -------------- |
| Explain / compare only | L1 | — |
| Fix or extend **existing** code in a few files | L2 | `level L2` even for a single new endpoint if you want less ceremony than L3 |
| New module, API contract, worker, or multi-file feature | L3 | — |
| Multi-service, platform, large migration | L4 | — |

**L3 vs L4 Validate:** Bounded L3 folds validation into **Spec / assumptions** in `l3-01-define.md`. **L4** adds a formal **Validate** phase (`l4-01-discover.md`: go/no-go, risks) before heavy design — intentional for large scope.

## Pipelines (UI)

| Level | Pipeline (canonical — match playbook)                      |
| ----- | ---------------------------------------------------------- |
| L1    | Context (light) → Answer → MD                              |
| L2    | Context → Spec (+ test cases in Spec if behavior changes) → Patch → Verify → Review → MD |
| L3    | Context → Spec → Plan → [Scaffold] → Test → Code → Verify → Regression → Review → [Iterate] → [Refine] → Ship → MD |
| L4    | Full Flow (15 steps; skip 1–2 if `level L4` already set) — see L4 playbook |

### L1 playbook

- Context: user text + `@file` only; max **1–2 files**; no codebase-wide scan.
- **Answer** in chat; optional `docs/answers/YYYY-MM-DD-<slug>.md` ([template](templates/phases/l1/answer.md)).
- No Spec, Patch, Verify suite, Regression.

### L2 playbook

- Context: impacted paths + callers **1 hop**.
- **Spec:** acceptance criteria (bullets or Given/When/Then). For **bugs:** root cause here **before** Patch (see **Bug overlay** below).
- **Test gate:** If behavior/contract changes → failing repro / test cases in Spec **before Patch**. Pure refactor/rename → skip new tests.
- **Patch:** incremental edits; match **`general.mdc` / stack `*.mdc`** within touched scope (architecture, SOLID, size limits — do not restate here).
- **Verify:** impacted tests / smoke; not full-system regression.
- **Review:** security checklist + quick pass against **`general.mdc` / stack rules**; [caveman-review](../caveman-review/SKILL.md) mindset.
- **MD required:** Prefer phased folder `docs/work/YYYY-MM-DD-<slug>/` (or `<doc-root>/work/...` per doc-root rules above) ([phases](templates/phases/README.md)); or single dated work-item `.md` under the same root for very small patches.

### L3 playbook

Follow the **L3 pipeline row** above (Regression and Ship are required, not optional shortcuts).

- Context: module boundary, API contract, tests dir, related config.
- **Spec:** AC; assumptions / out of scope (3 bullets). For **bugs:** root cause in Spec or `STATUS.md` before Patch/Code.
- **Plan:** architecture + tasks; [architect-plan](../architect-plan/SKILL.md) in `l3-01-define.md` (default).
- **Scaffold** (if needed): new folders/modules after Plan, before Test.
- **Test** before **Code** — `STOP before Code` without test cases listed (same gate as L4 “Test Design”).
- **Code:** follow **`general.mdc` / stack `*.mdc`** (architecture, SOLID, size limits).
- **Verify:** smoke / happy path; log commands run.
- **Regression:** broader impacted suite (required for L3).
- **Review:** checklist L2+; on fail → **Iterate** → light **Refine** → **Ship** (`l3-03-ship.md`, rollout/rollback).
- **MD required:** phased folder **L3** ([templates/phases/l3](templates/phases/l3)) + `STATUS.md`.

### L4 playbook — Full Flow (15 steps)

1. Idea · 2. Scope (user choice) · 3. Context · 4. Validate · 5. Spec · 6. Plan · 7. Scaffold · 8. Test Design · 9. Implement · 10. Verify · 11. Review · 12. Regression · 13. Iterate · 14. Refine · 15. Document

Step **15. Document** = finalize phased MD + **Ship** delivery write-ups (`l4-05-ship.md`: rollout, rollback, architecture/AI/delivery layers) — same intent as L3 **Ship**, not a separate skip.

**If user already sent `level L4` (or `/question-scope L4`):** steps **1–2 are done** — start at **3. Context**. Do not re-run scope options or a second Idea/Scope ceremony.

Use `CreatePlan` + [architect-plan](../architect-plan/SKILL.md). If already in Cursor plan mode, **extend the existing plan file** — do not create a duplicate.

**Architecture layer:** dependency graph, domain boundaries, scale, observability, security, deploy, rollback, cost.

**AI layer (when relevant):** token/memory, retrieval, embedding, chunking, caching.

**Delivery layer:** rollout, migration, backward compatibility.

**MD required:** phased folder **L4** set ([templates/phases/l4](templates/phases/l4)); `l4-05-ship.md` holds Architecture / AI / Delivery write-ups. Single [rollup/work-item](templates/phases/rollup/work-item.md) is optional rollup at the end.

## Verify vs Regression vs Iterate

| Step       | Meaning                                        |
| ---------- | ---------------------------------------------- |
| Verify     | Smoke / happy path; log commands run           |
| Regression | Broader or full impacted suite (L3–L4)         |
| Iterate    | Fix failures from Verify / Review / Regression |

## Context budgets

| Level | Budget                                                                  |
| ----- | ----------------------------------------------------------------------- |
| L1    | 0–2 files, no wide search                                               |
| L2    | Impacted files + 1-hop callers                                          |
| L3    | Module + API + tests + config                                           |
| L4    | Wider; [analyze-impact](../analyze-impact/SKILL.md) with bounded passes |

## Gates

- **STOP** after scope options until user picks (unless `level Lx` preset).
- **STOP before Patch (L2):** if behavior/contract changes and Spec lacks test cases; if **bug**, Spec/`STATUS.md` lacks **root cause** (and repro test when behavior changes).
- **STOP before Code (L3–L4):** if **Test** (L3) or **Test Design** (L4 step 8) is not done — test cases listed before implementation.

## Bug overlay (any level with a defect)

Runs **inside** the active L pipeline (usually **L2**). Order:

1. `debug-root-cause-first` — no Patch/Code until root cause is written in Spec or `STATUS.md`
2. `tdd-failing-repro` — failing repro test when behavior changes
3. Fix (Patch / Implement) → `verify-fix-evidence`

Multiple independent failure domains → `parallel-failure-domains`. **L1** is explain-only; if fixing code, re-scope to **L2+**.

## Code policy (L2–L4)

Do **not** duplicate SOLID or architecture tables in this skill — **`general.mdc`** and language **`*.mdc`** are the single source of truth. During Review, check the diff against those rules (pragmatic, repo-aligned).

## Review checklist (L2+)

- Input validation, authZ/tenant, no secrets/PII in logs, safe queries/paths
- Obvious perf issues (N+1, unbounded load)
- Violations of **`general.mdc` / stack rules** in the diff (one line each if clear)

## Definition of Done

| Level | DoD                                                  |
| ----- | ---------------------------------------------------- |
| L1    | Answer meets outcome; MD if user wants archive       |
| L2    | AC met; tests pass; Review done; phased folder or work-item MD written |
| L3    | Contract + tests; Regression pass; phased L3 folder + `STATUS.md` |
| L4    | Full flow + layers; phased L4 folder + `STATUS.md` complete |

## Superpowers supplement (optional playbook layer)

**Question-scope** sets **how much** work (L1–L4), gates, and **`docs/work/…`** phased files. The **Superpowers** bundle (`skills/SKILLS-REGISTRY.md`, rule `workflow.mdc`) adds **how** to execute with discipline: design gate, detailed plans, worktree, TDD, verify, subagents.

**Precedence:** This skill’s STOP gates and level budgets win. Superpowers playbooks **must not** skip L1–L4 choice, `docs/work/` continuity, or `general.mdc` / stack rules. User may say **`sp:off`** (or `no-sp`) to skip the supplement only (question-scope still applies unless `qs:off` / `no-scope`). Do not use `superpowers: off` — that resembles the legacy plugin prefix `superpowers:<id>`.

**Default:** Apply the supplement rows below for **L3–L4** unless the user opts out. For **L2**, apply the **minimal** row only. **L1** — no Superpowers feature flow (team `explain-code` only if needed).

### By level

| Level | Question-scope (primary) | Superpowers supplement |
| ----- | ------------------------ | ---------------------- |
| L1 | Answer; no patch | None (optional `explain-code`) |
| L2 | Spec → Patch → Verify → Review | `tdd-during-implementation` if behavior changes; `verify-before-done` before “done”; skip `design-approval-gate` / `implementation-plan` unless user escalates to L3 |
| L3 | Spec → Plan → Test → Code → … → phased `docs/work/…` | `isolated-workspace` before code; `tdd-during-implementation`; **default execute:** `execute-inline-checkpoints` (B); `execute-via-subagents` (A) **only** with `writing-plans` or user asks for subagents; `verify-before-done`; `finish-branch-options` at ship — see plan choice below |
| L4 | Full 15-step + architecture/AI/delivery layers | Near-full feature flow above + `design-approval-gate` and `implementation-plan` when scope is large; `outgoing-code-review` before merge when applicable |

**Bug / test failure:** see **Bug overlay** above (not a separate level).

### Phase → workflow rule ID

Map Superpowers **rule IDs** from `rules/workflow.mdc` (playbooks under `skills/<id>/`):

| Question-scope phase | Rule ID | Playbook |
| -------------------- | ------- | -------- |
| Spec (L3–L4, large L2) | `design-approval-gate` | `skills/brainstorming/` |
| Plan (L3–L4) | `implementation-plan` **or** team plan below | `skills/writing-plans/` or `skills/architect-plan/` |
| Before Patch/Code | `isolated-workspace` | `skills/using-git-worktrees/` |
| Code / Patch | `tdd-during-implementation` | `skills/test-driven-development/` |
| Execute plan (L3–L4) | **Default L3:** `execute-inline-checkpoints` (B). **ALT:** `execute-via-subagents` (A) — requires `writing-plans` plan file | `skills/executing-plans/` \| `skills/subagent-driven-development/` |
| Verify | `verify-before-done` | `skills/verification-before-completion/` |
| Ship (L3–L4) | `finish-branch-options` | `skills/finishing-a-development-branch/` |

Run `skill-check-first` (`skills/superpowers/`) once per session when the supplement applies — after level is chosen, not instead of scope options.

### Plan choice (L3–L4)

| Situation | Use |
| --------- | --- |
| Bounded feature; plan fits one phase file | **`architect-plan`** in `l3-01-define.md` / L4 define phase (default) → pair with **execute-inline-checkpoints** (B) |
| Many tasks/files; zero-context handoff | **`writing-plans`** → `docs/plans/YYYY-MM-DD-<feature>.md`; link from work folder → may use **execute-via-subagents** (A) |
| L4 | Often **both**: architect framing in phase MD + `writing-plans` for execution tasks |

Do not run both execute ALT branches on the same plan. **Do not** use execute (A) with only `architect-plan` and no `writing-plans` — `subagent-driven-development` requires a task-level plan file.

### Where files live

| Content | Canonical for question-scope | Superpowers artifact (optional) |
| ------- | ---------------------------- | ------------------------------- |
| STATUS, blockers, commands run, phase state | `docs/work/YYYY-MM-DD-<slug>/` | — |
| Design spec | `l3-01-define.md` / `l4-02-define.md` | `docs/specs/YYYY-MM-DD-<topic>-design.md` (link from work file) |
| Implementation plan | Same phase MD or tasks in plan section | `docs/plans/YYYY-MM-DD-<feature>.md` |

Pick **one** plan/spec tree per repo; do not duplicate without links. See `skills/CONVENTIONS.md`.

### User prompt examples

```text
level L3 — API export CSV. Superpowers supplement: worktree, inline execute, TDD, verify.
```

```text
level L4 — Auth migration. Superpowers: full feature flow + subagents. Phased docs/work/.
```

```text
level L2 — Fix validation on X. Superpowers minimal: TDD + verify only.
```

```text
sp:off — L3 feature, team plan only (architect-plan), no writing-plans/worktree.
```

## Related skills

| Step          | Skill              |
| ------------- | ------------------ |
| Vague problem | orchestra-decision |
| Plan L3–L4    | architect-plan (default); **writing-plans** when Superpowers supplement + large plan |
| Superpowers meta | superpowers (`skill-check-first`) |
| Workflow rules | `rules/workflow.mdc` (rule IDs above) |
| Tests         | generate-test      |
| Review tone   | caveman-review     |
| L4 impact     | analyze-impact     |

## Token depth

| Level | Effort                  |
| ----- | ----------------------- |
| L1    | Low / shallow           |
| L2    | Medium / focused        |
| L3    | High / feature-wide     |
| L4    | Very high / system-wide |
