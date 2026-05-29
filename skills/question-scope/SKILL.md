---
name: question-scope
description: Use when the user sends /question-scope or /question-scope L1–L4 only. Opt-out qs:off, no-scope, quick:, qs:meta, audit:. Modifiers scope:light (L2 chat rollup), sp:off. Clarifying options IDE-ALIGNED §12 when scope on. Coordinated skills cite IDE-ALIGNED §N per CONVENTIONS. level Lx and ?+keyword do not activate.
---

# Question Scope

**Announce when applying:** `Using question-scope — <Lx or level picker>.`

**Mirror rule:** always-on **`question-scope`** rule — when triggers/gates change, edit rule + skill in one change set. Maintainer checklist: [references/CONTRACT-SYNC.md](references/CONTRACT-SYNC.md).

**Language:** English only in this skill (`SKILL.md`, [README.md](README.md), `references/`, `templates/`, `examples/`).

**All AI IDEs** (Cursor, Kiro, Windsurf, Copilot, JetBrains AI, Claude Code, …) share this skill. **User invocation (canonical):** `/question-scope` or `/question-scope L1`…`L4` only — see [README.md](README.md). **Host UI:** same Idea/options/STOP everywhere; use native multi-option picker when the host provides one, else numbered list — [references/host-ui.md](references/host-ui.md).

**Deep dives (load when needed):** [references/README.md](references/README.md) — [parsing-tokens](references/parsing-tokens.md), [session-continuity](references/session-continuity.md), [progressive-context-jit](references/progressive-context-jit.md), **[ide-aligned-practices](references/ide-aligned-practices.md)**, [host-ui](references/host-ui.md), [confirmation-prompts](references/confirmation-prompts.md), gray-zones, level-picker, playbooks, pipelines-quickref, pipelines-skill-map, superpowers-supplement, pressure-scenarios, [CONTRACT-SYNC](references/CONTRACT-SYNC.md).

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
- [IDE-aligned practices](#ide-aligned-practices)
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

**Suggest level / option labels:** [references/level-picker.md](references/level-picker.md) (flow, host UI, **Option copy**) · **rich confirmations:** [references/confirmation-prompts.md](references/confirmation-prompts.md).

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
| Idea → **level picker** (2 labeled options if one gray pair fits, else 4) → **STOP** until L picked | Run **`brainstorming`** / **`writing-plans`** while STOP waits for level |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## Gates at a glance

| Gate | When |
| ---- | ---- |
| **STOP after options** | Presented L1–L4 (or gray pair) — no Context/Spec/Patch/Code until user picks (unless `/question-scope Lx` preset) |
| **STOP before wide context (L2)** | No codebase-wide search / unbounded grep before **Spec** drafted — **exception:** approved plan attach or ≤3 primary `@` files with AC ([ide-aligned-practices](references/ide-aligned-practices.md)) |
| **STOP before Patch (L2)** | Behavior/contract change without test cases in Spec (tiered — see IDE-aligned §4); **bug** without **root cause** in Spec/`STATUS.md` |
| **STOP before Code (L3–L4)** | **Test** (L3) or **Test Design** (L4 §8) not done for **new contract/module** — not for assessment-only or config-only ([ide-aligned-practices](references/ide-aligned-practices.md)) |
| **Assessment-only** | Gap/review (“cần sửa gì”, “vs plan”) → **no** Patch/Code until user asks to implement |
| **Gray zone** | Two levels fit → two-option level pick (structured UI or numbered list); never auto-pick heavier level — [gray-zones](references/gray-zones.md) |
| **STOP before Patch/Code (§12)** | Open **how** decision in Spec/Plan → clarifying options (2–4 + **Other — I'll specify**); scope active only — [clarifying-options](references/clarifying-options.md) |
| **Escalation** | Work exceeds chosen L → stop; re-present adjacent levels; user confirms |
| **Sticky scope** | Same work item keeps L until done or new `/question-scope` / `/question-scope Ly` — no second four-option picker mid-task — [level-picker-runtime](references/level-picker-runtime.md) |

## When this skill applies

Activate only when a trigger matches. Otherwise respond normally.

### Default (no trigger)

No `/question-scope` at **message start or end** (after trim) → **normal chat** (answer or edit as the user asked).

- **Do not** infer L1–L4 from task size, file count, or “sounds like L3”.
- **Do not** create `docs/work/…` or run phased pipelines unless the user chose scope (`/question-scope` / `/question-scope Lx`) or explicitly asked for phased docs.

Rule reminder (always-on mirror): **`question-scope`** rule § Default, § Precedence — keep in sync with this skill (see **Mirror rule** above and [CONTRACT-SYNC.md](references/CONTRACT-SYNC.md)).

### User invocation (canonical — tell users this only)

| User sends | Action |
| ---------- | ------ |
| **`/question-scope`** + task (no `L1`…`L4` on the command) | Idea → suggest → **level picker** (**2** labeled options if only one gray pair fits, else **4**) → **STOP** — [level-picker-runtime](references/level-picker-runtime.md) |
| **`/question-scope L1`…`L4`** + task | Skip picker → run that level’s pipeline |

Human guide: [README.md](README.md). **`level Lx` and `?` + keyword do not activate** — only `/question-scope` forms below.

### Triggers (agent)

| Priority | Trigger | Action |
| -------- | ------- | ------ |
| 1 | **`/question-scope L1`…`L4`** (see **Parsing**) | Skip options → run pipeline for that level |
| 2 | **`/question-scope`** without `L1`…`L4` on the command | Idea → suggest → **level picker** (2 or 4 per gray-zones) → **STOP** |
| — | Glued **`/question-scopeL1`…`L4`** (no space before `L`) | Reply once: `Detected /question-scopeL2 — use /question-scope L2`; **no** preset level — then level picker (2 or 4) → **STOP** |
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
| **`scope:light`** | On — L2 **chat rollup** instead of required `docs/work/` ([ide-aligned-practices](references/ide-aligned-practices.md)) | Unchanged |
| **`clarify:off`** | On — **skip** §12 clarifying options ([clarifying-options](references/clarifying-options.md)); level picker unchanged | Unchanged |
| **`/question-scope`** (no `L1`…`L4` on command) | On → level picker (2 or 4) → STOP | Per level after pick |
| `/question-scope Lx` | On (skip level picker) | Per [supplement by level](references/superpowers-supplement.md#by-level) |

**Scope opt-out patterns** (off even with `/question-scope Lx` in the same message):

| Token | Match |
| ----- | ----- |
| **`quick:`** | Message **starts with** `quick:` OR `(^|\s)quick:` (colon required) |
| **`qs:off` / `no-scope`** | `(^|\s)(qs:off|no-scope)\b` |
| **`qs:meta`** | Message **starts with** `qs:meta` OR `(^|\s)qs:meta\b` |
| **`audit:`** | Message **starts with** `audit:` OR `(^|\s)audit:` (colon required) |

**`quick:` is not** “skip design/plan only” while scope runs — use **`sp:off`** for that. **`quick:` is not** “L2 with light docs” — use **`/question-scope L2`** + **`scope:light`** or **Rollup MD OK** (see [README.md](README.md) § Presets **Light patch** / **scope:light**).

## Parsing, meta, and conflicting tokens

Full detail: [references/parsing-tokens.md](references/parsing-tokens.md) (placement, opt-out wins, audit/meta signals).

**Contract anchors:** **Glued `L`** (no space) → reply once: `Detected /question-scopeL2 — use /question-scope L2`. **Meta / audit** (no run intent): path `skills/question-scope`, phrases e.g. **kiểm tra lại về rule**, **discussing** `/question-scope` **without intent to run** — scope off even if token present.

## Output header (after level is chosen)

Emit **`Level: Lx | Pipeline: …`** using the canonical pipeline for that level ([Pipelines (UI)](#pipelines-ui)). Include **Test** on **L3** implement paths; on **L2** note **(+ TC if behavior change)** in Spec when relevant.

```text
Level: L2 | Pipeline: Context → Spec (+ TC if behavior change) → Patch → Verify → Review → MD

Level: L3 | Pipeline: Context → Spec → Plan → [Scaffold] → Test → Code → Verify → Regression → Review → [Iterate] → [Refine] → Ship → MD

Level: L3 | Pipeline: Context → Assessment → Answer
```
(Second line = **assessment-only** — no Test/Code until user asks to implement.)

```text
Level: L4 | Pipeline: Full Flow (15 steps; Test Design before Implement)
```

List steps **1–15** only when the user asks or you need step numbers ([playbooks § L4](references/playbooks.md#l4--full-flow-15-steps)).

## Session continuity

[references/session-continuity.md](references/session-continuity.md) · templates: [templates/phases/README.md](templates/phases/README.md).

## Scope Level — user chooses (do not auto-lock)

1. **Idea** — structured restatement (Goal, Where, Done when; optional Open/Out of scope) — not one vague sentence.
2. **Suggest** — `Suggest: Lx (lean) — <reason tied to this message>`; if gray zone, name the pair (`L2 ↔ L3`) and lean (heuristic only — user picks).
3. **Level picker** — canonical labels + **`For this task:`** clause per option; gray zone → optional comparison table — then **STOP**.

**Required shape (examples):** [references/confirmation-prompts.md](references/confirmation-prompts.md) § A. **§12 how-to-build:** same file § B + [clarifying-options.md](references/clarifying-options.md).

| ID  | Label                                                         |
| --- | ------------------------------------------------------------- |
| L1  | Chat Answer — explain / naming / compare; no repo edits       |
| L2  | Patch — change existing code (few files)                      |
| L3  | Small Feature — new module/API/worker (bounded)               |
| L4  | Large System — multi-service, MCP, AI platform, big migration |

### Level picker (one rule)

[references/level-picker-runtime.md](references/level-picker-runtime.md) · option strings: [level-picker.md](references/level-picker.md).

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
| **Assessment** | Gap/review vs plan or AC — **no** Patch/Code unless user asks to implement ([ide-aligned-practices](references/ide-aligned-practices.md)) |
| Verify     | Smoke / happy path; **paste command + exit code in chat** before “done” (`verification-before-completion`) |
| Regression | **L3 default:** tests under touched **module/package** (infer from diff) + **1-hop** integration; log in **chat** + optional phase MD. **L4:** per impacted service (`analyze-impact` bounded). **L2:** scoped Verify only. Human presets: [README.md § Regression](README.md#regression-l3l4) |
| Iterate    | Fix failures from Verify / Review / Regression |

**Playbooks (step detail):** [references/playbooks.md](references/playbooks.md)

## Progressive context (JIT)

[references/progressive-context-jit.md](references/progressive-context-jit.md).

## IDE-aligned practices

Borrow IDE strengths (speed, plan reuse, diff-scoped tests) **without** dropping scope gates. Full rules: [references/ide-aligned-practices.md](references/ide-aligned-practices.md).

**Summary:** (1) Attached approved plan = Spec; skip duplicate `docs/work/` unless archiving. (2) **Assessment-only** sub-pipeline when user asks review/gap, not implement. (3) **`scope:light`** = L2 with chat rollup, scope still on. (4) Test gates **tiered** by change type. (5) **Verify** = command output in chat. (6) L2–L3 review ≈ **≤5** caveman lines unless security-sensitive diff. (7) **§12** — Spec/Plan ambiguity → 2–4 options + **Other**; STOP before Patch/Code ([clarifying-options](references/clarifying-options.md)).

## Bug overlay (any level with a defect)

Runs **inside** the active L pipeline (usually **L2**):

1. **`debug-root-cause-first`** → **`systematic-debugging`** — root cause in Spec or `STATUS.md` before Patch/Code
2. **`tdd-failing-repro`** → **`test-driven-development`** when behavior changes
3. Fix → **`verify-fix-evidence`** → **`verification-before-completion`**

Multiple independent failure domains → `parallel-failure-domains`. **L1** is explain-only; if fixing code, re-scope to **L2+**.

## Code policy (L2–L4)

Do **not** duplicate SOLID/architecture here — rule **`code-standards`** and stack rules are authoritative. Review the diff against those rules.

## Review checklist (L2+)

- **L2–L3 default:** **`caveman-review`**, ~**5** lines max on the diff ([ide-aligned-practices](references/ide-aligned-practices.md))
- **L2–L3 security depth** when diff touches public routes, webhooks, auth/authZ, PII/secrets: validation, tenant scope, no secrets in logs, safe queries/paths, N+1
- **`code-standards` / stack** violations (one line each if clear)
- L4 formal pre-merge: full checklist + **`requesting-code-review`** (see supplement)
- **Impact analysis** (L4 Discover): **`analyze-impact`** — blast radius / impacted paths; **not** the Regression test step
- **Incoming PR feedback:** **`receiving-code-review`** (rule **`incoming-code-review`**) after PR open — verify each comment before fix

## Definition of Done

| Level | DoD                                                  |
| ----- | ---------------------------------------------------- |
| L1    | Answer meets outcome; MD if user wants archive       |
| L2    | AC met; tests pass; Verify evidence in chat; Review done; `docs/work/` **or** chat rollup (`scope:light` / Rollup MD OK) |
| L3    | Contract + tests; Regression pass; phased L3 + `STATUS.md` |
| L4    | Full flow + layers; **Test Design** done for new contracts; tests + Regression pass; phased L4 + `STATUS.md` complete |

## Superpowers supplement

**Summary:** L3–L4 default on; L2 minimal; L1 none. Opt out: `sp:off` / `no-sp`. Full tables, rule IDs, plan choice, prompts: **[references/superpowers-supplement.md](references/superpowers-supplement.md)**.

## Pipeline skills

Standalone vs coordinated vs composition: [COMPOSITION.md](../COMPOSITION.md) (includes **Task kind** when scope active). Per-level chains: [references/pipelines-quickref.md](references/pipelines-quickref.md) (default during work), [references/pipelines-skill-map.md](references/pipelines-skill-map.md) (detail), [references/superpowers-supplement.md](references/superpowers-supplement.md), [references/ide-aligned-practices.md](references/ide-aligned-practices.md) §11 (child skills), [SKILLS-REGISTRY.md](../SKILLS-REGISTRY.md).

Do **not** run design/plan/worktree while scope **STOP** waits for L1–L4.

## Token depth

| Level | Effort                  |
| ----- | ----------------------- |
| L1    | Low / shallow           |
| L2    | Medium / focused        |
| L3    | High / feature-wide     |
| L4    | Very high / system-wide |
