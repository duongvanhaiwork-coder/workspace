---
name: question-scope
description: Use when the user sends /question-scope or /question-scope L1–L4 only. Opt-out qs:off, no-scope, quick:, qs:meta, audit:, sp:off, no-sp. level Lx and ?+keyword do not activate.
---

# Question Scope

**Contract version:** `qs-2026-05-29.1` — keep in sync with `question-scope.mdc` when triggers/gates change.

**Language:** English only in this skill (`SKILL.md`, [README.md](README.md), `references/`, `templates/`, `examples/`).

Cursor + Kiro share this skill. **User invocation (canonical):** `/question-scope` or `/question-scope L1`…`L4` only — see [README.md](README.md). **Difference:** Cursor may use `AskQuestion` for level pick; Kiro uses a numbered list — wait for `L1`…`L4` or `/question-scope Lx`.

**Deep dives (load when needed):** [references/README.md](references/README.md) — gray-zones, level-picker, playbooks, **pipelines-quickref** (default skill chains), pipelines-skill-map (sections only), superpowers-supplement, pressure-scenarios.

**Rules (IDE — cite rule IDs only):** Always-on **`question-scope`**, **`code-standards`**, stack rules by file type. On demand: **`@workflow`** (Superpowers rule IDs). **This skill:** `question-scope`.

## Contents

- [Instruction precedence](#instruction-precedence)
- [Gates at a glance](#gates-at-a-glance)
- [When this skill applies](#when-this-skill-applies)
- [Output header](#output-header-after-level-is-chosen)
- [Session continuity (L2–L4)](#session-continuity-phased-md-files-l2l4)
- [Scope Level — user chooses](#scope-level--user-chooses-do-not-auto-lock)
- [Pipelines (UI)](#pipelines-ui)
- [Progressive context (JIT)](#progressive-context-jit)
- [Bug overlay](#bug-overlay-any-level-with-a-defect)
- [Code policy & review](#code-policy-l2l4)
- [Definition of Done](#definition-of-done)
- [Superpowers supplement](#superpowers-supplement)
- [Pipeline skills — standalone, coordinated, composition](#pipeline-skills--standalone-coordinated-and-composition)
- [Related skills](#related-skills)
- [Token depth](#token-depth)

## Instruction precedence

1. System/developer constraints
2. Explicit **user message** (including opt-out tokens; scope opt-outs beat `/question-scope Lx` when both appear — **Conflicting tokens**)
3. Repo **`AGENTS.md`** (when present)
4. This skill (pipelines, gates, work-folder layout, STOP gates)
5. Rule **`code-standards`** and stack rules (`typescript`, `react`, `python`, …) — canonical for code style, architecture, security, SOLID, size limits, and API conventions; this skill **does not redefine** those
6. **`@workflow`** / Superpowers supplement — when scope is active or the user loads workflow

**Pipeline skills (composable):** Skills in [Related skills](#related-skills) run **standalone**, **with scope**, or **combined with each other** — see [CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes and [COMPOSITION.md](../COMPOSITION.md). This skill **coordinates** when active; it does **not** block other skills.

**Suggest level / option labels:** [references/level-picker.md](references/level-picker.md) (flow, host UI, **Option copy** for pickers).

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md). This skill **coordinates** when active; it does **not** block other skills from running standalone.

### Standalone (other skills)

Pipeline skills (`test-driven-development`, `systematic-debugging`, `refactor-code`, …) run on task fit without `/question-scope` unless the user opts in.

### Coordinated

User sends **`/question-scope`** or **`/question-scope Lx`** — L, STOP gates, `docs/work/…`, and supplement table apply.

### Requires (hard)

- None for other skills; when this skill is active, **STOP after L pick** before Spec/Plan/Code unless `/question-scope Lx` preset the level.

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| **`test-driven-development`** standalone when behavior changes | Require `/question-scope` before every TDD patch |
| **L2** patch: **`systematic-debugging`** for bugs; optional TC rows in `l2-patch` | **`brainstorming`** for every L2 patch |
| **`using-git-worktrees`** on L3–L4 before Code (supplement default) | Mandate worktrees on L2, `sp:off`, or user decline |
| Idea → four options → **STOP** until L1–L4 chosen | Run **`brainstorming`** / **`writing-plans`** while STOP waits for level |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## Gates at a glance

| Gate | When |
| ---- | ---- |
| **STOP after options** | Presented L1–L4 (or gray pair) — no Context/Spec/Patch/Code until user picks (unless `/question-scope Lx` preset) |
| **STOP before wide context (L2)** | No codebase-wide search / unbounded grep before **Spec** drafted |
| **STOP before Patch (L2)** | Behavior/contract change without test cases in Spec; **bug** without **root cause** in Spec/`STATUS.md` |
| **STOP before Code (L3–L4)** | **Test** (L3) or **Test Design** (L4 §8) not done — test cases listed first |
| **Gray zone** | Two levels fit → two-option AskQuestion; never auto-pick heavier level — [gray-zones](references/gray-zones.md) |
| **Escalation** | Work exceeds chosen L → stop; re-present adjacent levels; user confirms |

## When this skill applies

Activate only when a trigger matches. Otherwise respond normally.

### Default (no trigger)

No `/question-scope` at **message start or end** (after trim) → **normal chat** (answer or edit as the user asked).

- **Do not** infer L1–L4 from task size, file count, or “sounds like L3”.
- **Do not** create `docs/work/…` or run phased pipelines unless the user chose scope (`/question-scope` / `/question-scope Lx`) or explicitly asked for phased docs.

Rule reminder: `rules/cursor/question-scope.mdc` § Default, § Precedence.

### User invocation (canonical — tell users this only)

| User sends | Action |
| ---------- | ------ |
| **`/question-scope`** + task (no `L1`…`L4` on the command) | Idea → suggest → **4 options** → **STOP** |
| **`/question-scope L1`…`L4`** + task | Skip options → run that level’s pipeline |

Human guide: [README.md](README.md). **`level Lx` and `?` + keyword do not activate** — only `/question-scope` forms below.

### Triggers (agent)

| Priority | Trigger | Action |
| -------- | ------- | ------ |
| 1 | **`/question-scope L1`…`L4`** (see **Parsing**) | Skip options → run pipeline for that level |
| 2 | **`/question-scope`** without `L1`…`L4` on the command | Idea → suggest → **4 options** → **STOP** |
| — | Scope **opt-out** detected (see **Parsing**) | Do **not** activate question-scope |
| — | `sp:off` or `no-sp` | Supplement off only when scope is active; does not activate scope |
| — | **`level L1`…`L4` or `?` + keyword** (any form) | **Do not** activate — normal chat; ask user to send `/question-scope` or `/question-scope Lx` |

### Tokens (scope + supplement)

Same meaning in rule **`@workflow`** when scope is off. Rule **`question-scope`** summarizes; this table is canonical.

| Token / entry | Question-scope | Superpowers supplement |
| ------------- | ---------------- | ------------------------ |
| `qs:off`, `no-scope` | Off | Off |
| **`quick:`** | Off — fast path, **no** L1–L4 options, **no** phased `docs/work/` | Off |
| **`qs:meta`**, **`audit:`** | Off — explicit audit/review (no L1–L4); see **Meta discussion** | Off |
| `sp:off`, `no-sp` | On **only when scope already active**; does **not** activate scope | Off |
| **`/question-scope`** (no `L1`…`L4` on command) | On → four options → STOP | Per level after pick |
| `/question-scope Lx` | On (skip level picker) | Per [supplement by level](references/superpowers-supplement.md#by-level) |

**Scope opt-out patterns** (off even with `/question-scope Lx` in the same message):

| Token | Match |
| ----- | ----- |
| **`quick:`** | Message **starts with** `quick:` OR `(^|\s)quick:` (colon required) |
| **`qs:off` / `no-scope`** | `(^|\s)(qs:off|no-scope)\b` |
| **`qs:meta`** | Message **starts with** `qs:meta` OR `(^|\s)qs:meta\b` |
| **`audit:`** | Message **starts with** `audit:` OR `(^|\s)audit:` (colon required) |

**`quick:` is not** “skip design/plan only” while scope runs — use **`sp:off`** for that. **`quick:` is not** “L2 with light `docs/work/` rollup” — use **`/question-scope L2`** + rollup note in the task (see [README.md](README.md) § Preset **Light patch**).

### Parsing

Case-insensitive matching after trim unless noted. **Only** `/question-scope` forms activate this skill.

| Pattern | Activates scope? |
| ------- | ---------------- |
| **`/question-scope`** token | Yes → priority 2 (four options) — only at **message start or end** (after trim); **not** mid-sentence |
| **`/question-scope L1`…`L4`** | Yes → priority 1 — same **start/end** placement; `/question-scope` + **whitespace** + `L1`…`L4` (`l2` → `L2`) |
| **`/question-scopeL1`…`L4`** (no space before `L`) | **No** preset level — priority 2 if at start/end. **Reply once:** `Detected /question-scopeL2 — use /question-scope L2` (substitute level digit) |
| **Mid-sentence** `/question-scope` (text before and after token) | **No** — put command at **start** or **end** (e.g. `/question-scope L2 — fix auth` or `fix auth /question-scope L2`) |
| **`level L1`…`L4`** (without `/question-scope`) | **No** — use `/question-scope Lx` |
| **`?` + keyword** | **No** |
| **`sp:off` / `no-sp`** | Does not activate scope by itself |
| **`qs:meta` / `audit:`** | **No** — explicit audit (same effect as meta below) |
| **Meta / audit** (see below) | **No** — normal chat or doc edit |

### Meta discussion (do not run scope)

Activate scope only when the user intends to **run** L1–L4 work on a **target repo**, not when they are **reviewing or editing** this skill or rules.

**Explicit audit tokens (recommended):** Message **starts with** `qs:meta` or `audit:` (or `(^|\s)qs:meta` / `(^|\s)audit:`) — scope **off** even if `/question-scope` appears in the same message. Prefer these over keyword-only meta when reviewing rules/skills.

**Meta wins over `/question-scope` in the same message** — do not activate when **any** signal below matches (path optional; EN/VI; diacritics optional):

- **Path:** `skills/question-scope`, `question-scope/SKILL.md`, `question-scope.mdc`, or repo path ending in `/question-scope/`
- **Audit / review (examples):** “check question-scope rules”, “đánh giá skill”, “đánh giá question-scope”, “đánh giá rule”, “kiểm tra lại rule”, “kiểm tra lại về rule”, “kiểm tra rule question-scope”, “rà soát skill”
- Discussing without running: “don’t use `/question-scope` for this”, “when does `/question-scope` apply?”
- **Quoting, teaching, or discussing** `/question-scope` **without intent to run** L1–L4 on a target repo (docs, audit, examples)
- Editing SKILL.md / `question-scope.mdc` unless the user also sends **`/question-scope Lx`** at **start or end** for that edit task

**Placement:** After trim, the `/question-scope` command must be at **message start** (`^/question-scope`) or **message end** (`/question-scope` or `/question-scope Lx` immediately before end). Mid-sentence tokens (text before and after on the same line) do **not** activate — ask user to move the command to start or end.

**Signals that scope should run:** `/question-scope` or `/question-scope Lx` at **start or end**, plus task on application code, AC, or `@` repo paths outside `skills/question-scope/`.

User may add **`qs:off`**, **`qs:meta`**, or **`audit:`** to be explicit. If ambiguous, ask once whether to run scope or answer in chat.

### Conflicting tokens

If the same message contains **both** a scope trigger (`/question-scope` or `/question-scope Lx`) **and** a scope opt-out (`qs:off`, `no-scope`, `quick:`, `qs:meta`, `audit:` per tables above):

- **Opt-out wins** — do **not** activate question-scope.
- **`/question-scope Lx` does not override** `qs:off`, `no-scope`, `quick:`, `qs:meta`, or `audit:` in the same message.

`sp:off` / `no-sp` with `/question-scope Lx` (and **no** scope opt-out): run question-scope at that level; supplement off per [supplement by level](references/superpowers-supplement.md#by-level).

**Product-repo parsers (optional):** If triggers are implemented in application code, mirror [references/pressure-scenarios.md](references/pressure-scenarios.md) and [examples/pressure-test-pilot.md](examples/pressure-test-pilot.md) in that repo — not under `skills/`.

**Vague idea (no problem statement):** Run **`orchestra-decision`** first, then return to scope options.

## Output header (after level is chosen)

```text
Level: L2 | Pipeline: Context → Spec → Patch → Verify → Review → MD
```

List canonical steps 1–15 only for **L4** or when the user asks.

## Session continuity — phased `.md` files (L2–L4)

**Approach:** `docs/work/YYYY-MM-DD-<slug>/` with **`STATUS.md`** (read first in new sessions) + **one file per phase**. Files are source of truth for decisions, AC, commands, blockers.

**Doc root:** Prefer `docs/work/...`. If `docs/` is absent or forbidden: **ask once** or use `<doc-root>/work/...` (`specs/`, `design/`, `notes/`, …) with the same layout. L1 optional: `docs/answers/` or `<doc-root>/answers/`.

**Convention:** [templates/phases/README.md](templates/phases/README.md).

| Level | Files |
| ----- | ----- |
| L2 | `STATUS.md` + `l2-patch.md` ([l2](templates/phases/l2)) |
| L3 | `STATUS.md` + `l3-01` … `l3-03` ([l3](templates/phases/l3)) |
| L4 | `STATUS.md` + `l4-00` … `l4-05` ([l4](templates/phases/l4)) |

**Agent rules:**

1. After choosing L2–L4, create folder + templates; fill **`STATUS.md`** (`current_phase`, **5-line summary**, links, `next_actions`).
2. **End of each phase:** update phase file + `STATUS.md`; create next phase file **on entry** (default).
3. **New session:** `@` `STATUS.md` + current phase file — do not re-derive from chat alone.
4. L1: optional [answer.md](templates/phases/l1/answer.md); phased folder not required.
5. Tiny L2: single [rollup](templates/phases/rollup/work-item.md) allowed; use phased folder if multi-session.

## Scope Level — user chooses (do not auto-lock)

1. **Idea** (2–4 lines): problem + expected outcome.
2. **Suggest** one line: `Suggest: Lx — <short reason>` (heuristic only).
3. **Level picker** — then **STOP** (one rule below).

| ID  | Label                                                         |
| --- | ------------------------------------------------------------- |
| L1  | Chat Answer — explain / naming / compare; no repo edits       |
| L2  | Patch — change existing code (few files)                      |
| L3  | Small Feature — new module/API/worker (bounded)               |
| L4  | Large System — multi-service, MCP, AI platform, big migration |

### Level picker (one rule)

After **Idea** + **Suggest**, present options and **STOP** — do **not** run Context / Spec / Patch / Code until the user picks **one** level:

| Situation | Present | Host UI |
| --------- | ------- | ------- |
| User sent **`/question-scope L1`…`L4`** (preset) | **Skip** picker — run that pipeline | — |
| **Only one gray pair** fits ([gray-zones](references/gray-zones.md)) | **Exactly two** adjacent options (e.g. L2 vs L3) | Cursor: `AskQuestion` (2); Kiro: numbered list |
| **Three or more** levels plausible, or still unclear | **Four** options (table above) | Cursor: `AskQuestion` (4); Kiro: numbered list |

### Option copy (required)

Each option the user sees must include **what that L will do** (pipeline + code? + `docs/work/`), not bare `L1`…`L4`.

- **Canonical strings:** [references/level-picker.md § Option copy](references/level-picker.md#option-copy-required--user-must-read-before-pick) (4-option table + gray pairs).
- **Cursor:** `AskQuestion` — put the full `Lx — … · …` string in each option **`label`**.
- **Kiro / fallback:** numbered list or table with the **same** labels; then **STOP**.

**Examples:** `Add GET /users/export CSV` on an **existing** users API → **L2 vs L3 only** (two labeled options, not four). Greenfield multi-service platform → **four** labeled options.

Accept: `L2`, `choose L3`, `/question-scope L3`, etc.

**Sticky scope:** Keep chosen level for the **same work item** until done or user sends `/question-scope` / `/question-scope Ly`. Do **not** re-present the four-option picker mid-task. **New unrelated task** in the same chat → user must send `/question-scope` or `/question-scope Ly` again — do not carry over the previous level.

**Escalation:** Work exceeds level → stop; re-present options (at least adjacent pair); continue after confirm.

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
| Fix or extend **existing** code in a few files | L2 | `/question-scope L2` for one new endpoint if less ceremony than L3 |
| New module, API contract, worker, or multi-file feature | L3 | — |
| Multi-service, platform, large migration | L4 | — |

**Gray zones (L1/L2, L2/L3, L3/L4, L2 MD):** [references/gray-zones.md](references/gray-zones.md) · **L3 vs L4:** [references/l3-vs-l4-diff.md](references/l3-vs-l4-diff.md)

## Pipelines (UI)

| Level | Pipeline (canonical)                                           |
| ----- | -------------------------------------------------------------- |
| L1    | Context (light) → Answer → MD                                  |
| L2    | Context → Spec (+ tests in Spec if behavior changes) → Patch → Verify → Review → MD |
| L3    | Context → Spec → Plan → [Scaffold] → Test → Code → Verify → Regression → Review → [Iterate] → [Refine] → Ship → MD |
| L4    | Full Flow (15 steps; skip 1–2 if `/question-scope L4` set) — [playbooks § L4](references/playbooks.md#l4--full-flow-15-steps) |

| Step       | Meaning                                        |
| ---------- | ---------------------------------------------- |
| Verify     | Smoke / happy path; log commands run           |
| Regression | **L3 default:** all tests under the touched **module/package** + **1-hop** integration tests that call the changed API or public surface; log commands in phase MD. **L4:** test targets for each **impacted service** per validate/plan (`analyze-impact` bounded); CI slice OK when named in phase MD. **Not** full monorepo/entire suite unless AC or user requires. **L2:** scoped Verify only (no Regression step). Human presets: [README.md § Regression](README.md#regression-l3l4) |
| Iterate    | Fix failures from Verify / Review / Regression |

**Playbooks (step detail):** [references/playbooks.md](references/playbooks.md)

## Progressive context (JIT)

Add context **when the active pipeline step needs it**, not all at task start.

| Term | Meaning |
| ---- | ------- |
| **Symptom** | Problem statement in chat — **`@` not required** |
| **User-provided paths** | `@` attachments or paths in the message |

**Initial turn:**

| Level | Start with |
| ----- | ---------- |
| L1 | Symptom; `@` **0–2** files when answer needs code |
| L2 | Symptom + **0–1** primary `@`; **no** wide search before **Spec** |
| L3 | Symptom + AC; code `@` usually after **define** |
| L4 | Frame/discover; bounded impact after discover/validate |

**Expand** when Spec (L2+), Plan (L3+), or a gate shows a gap. Budgets are **ceilings per expansion**, not “read everything on step 1.”

| Level | Budget (max per expansion) |
| ----- | -------------------------- |
| L1    | 0–2 files, no wide search  |
| L2    | Impacted + 1-hop callers   |
| L3    | Module + API + tests + config |
| L4    | Wider; **`analyze-impact`** bounded |

**New session:** `@` `STATUS.md` + current phase file.

## Bug overlay (any level with a defect)

Runs **inside** the active L pipeline (usually **L2**):

1. **`debug-root-cause-first`** → **`systematic-debugging`** — root cause in Spec or `STATUS.md` before Patch/Code
2. **`tdd-failing-repro`** → **`test-driven-development`** when behavior changes
3. Fix → **`verify-fix-evidence`** → **`verification-before-completion`**

Multiple independent failure domains → `parallel-failure-domains`. **L1** is explain-only; if fixing code, re-scope to **L2+**.

## Code policy (L2–L4)

Do **not** duplicate SOLID/architecture here — rule **`code-standards`** and stack rules are authoritative. Review the diff against those rules.

## Review checklist (L2+)

- Input validation, authZ/tenant, no secrets/PII in logs, safe queries/paths
- Obvious perf issues (N+1, unbounded load)
- **`code-standards` / stack** rule violations in the diff (one line each if clear)
- Diff review tone: **`caveman-review`**. L4 formal pre-merge: **`requesting-code-review`** (see supplement)

## Definition of Done

| Level | DoD                                                  |
| ----- | ---------------------------------------------------- |
| L1    | Answer meets outcome; MD if user wants archive       |
| L2    | AC met; tests pass; Review done; work folder or rollup MD |
| L3    | Contract + tests; Regression pass; phased L3 + `STATUS.md` |
| L4    | Full flow + layers; phased L4 + `STATUS.md` complete |

## Superpowers supplement

**Summary:** L3–L4 default on; L2 minimal; L1 none. Opt out: `sp:off` / `no-sp`. Full tables, rule IDs, plan choice, prompts: **[references/superpowers-supplement.md](references/superpowers-supplement.md)**.

## Pipeline skills — standalone, coordinated, and composition

| | Standalone | Coordinated (`/question-scope Lx`) | Composition (same session) |
| --- | --- | --- | --- |
| **Who sets L / gates** | Each skill + optional **`superpowers`** | **question-scope** L + STOP + `docs/work/…` | Multiple skills when each **When to use** matches |
| **Example** | Debug → **`systematic-debugging`** + **`test-driven-development`** | `/question-scope L2 — bug` → overlay + L2 | Explain → patch: **`explain-code`** then **`test-driven-development`** |
| **Hard deps only** | [COMPOSITION.md](../COMPOSITION.md) § Requires (hard) | Same | e.g. **A** needs `docs/plans/…`; not whole pipeline for small tasks |

Do **not** tell users bundle skills work **only** with `/question-scope`. Opt-outs: `qs:off`, `quick:`, `no-scope` → compose per **`superpowers`** + [COMPOSITION.md](../COMPOSITION.md).

## Pipeline skills (supplement — after level chosen)

Do **not** run design/plan/worktree while scope **STOP** waits for L1–L4. Detail: [superpowers-supplement.md](references/superpowers-supplement.md) · [README.md](README.md) (human skill chain).

**L2 (minimal supplement):**

```text
Spec (+ TC rows in l2-patch if behavior changes; optional generate-test)
  → Patch → test-driven-development (if behavior changes)
  → Verify → verification-before-completion
  → Review (caveman-review mindset) → MD
```

**Bug overlay (usually L2):** `systematic-debugging` → `test-driven-development` (repro) → `verification-before-completion`

**L3 (default supplement):**

```text
brainstorming (spec approve) → architect-plan | writing-plans
  → generate-test (l3-02 TC table) → using-git-worktrees
  → executing-plans (B) | subagent-driven-development (A)
  → test-driven-development (per task)
  → Verify → verification-before-completion (per task + phase)
  → Regression → verification-before-completion (L3–L4; broader suite)
  → Review (caveman-review) → [L4: requesting-code-review if supplement on]
  → Refine + rollout/rollback in l3-03-ship.md / l4-05-ship.md
  → finishing-a-development-branch (git: merge | PR | keep | discard; fresh verify)
```

## Related skills

| Phase / need | Skill | Notes |
| ------------ | ----- | ----- |
| Vague idea (before or early define) | `orchestra-decision` | Not a substitute for `brainstorming` after L3–L4 chosen |
| Spec / design (L3–L4) | `brainstorming` | Skip L2 default; skip if spec already approved |
| Plan | `architect-plan` (bounded) · `writing-plans` (large / A) | See supplement § Plan path decision |
| Test design | `generate-test` | **L3–L4:** gate before Code (`l3-02` / `l4-03`). **L2:** optional TC rows in `l2-patch` |
| Isolated branch (L3–L4) | `using-git-worktrees` | Skip L2, `sp:off`, user decline |
| Execute plan | `executing-plans` (B) · `subagent-driven-development` (A) | **B (default L3):** `architect-plan` phase **or** `docs/plans/`. **A:** user chose A + `docs/plans/…` only — not phase-file-only |
| Patch / Code | `test-driven-development` | If behavior/contract changes |
| Verify / Regression / “done” | `verification-before-completion` | **L2:** Verify only (scoped). **L3–L4:** Verify + Regression steps; log in phase MD. Test design RED: log failures, do not claim suite green |
| Review (diff tone) | `caveman-review` | L2+ playbook Review step |
| Review (pre-merge, L4) | `requesting-code-review` | **L4 + supplement:** default formal pre-merge (waive explicitly). **L3:** only if AC asks. Not duplicate of subagent A per-task reviewers |
| Feedback PR (incoming) | `receiving-code-review` | When PR/review comments arrive — rule `incoming-code-review`; verify before implement; log in phase **PR feedback** / Iterate |
| Ship (L3–L4) | `finishing-a-development-branch` | After Verify/Regression green + Review; fill `l3-03` / `l4-05` (rollout/rollback) then git options + fresh verify |
| Bug | `systematic-debugging` | Before Patch; see Bug overlay |
| Impact analysis | `analyze-impact` | **L4:** discover/plan cross-service (bounded). **L3:** optional, one-service. **Not** Regression — feeds Regression scope in phase MD |
| Meta / skill pick | `superpowers` | `skill-check-first` once per session |
| Workflow rule IDs | **`@workflow`** | On demand — maps rule ID → skill ID |

## Token depth

| Level | Effort                  |
| ----- | ----------------------- |
| L1    | Low / shallow           |
| L2    | Medium / focused        |
| L3    | High / feature-wide     |
| L4    | Very high / system-wide |
