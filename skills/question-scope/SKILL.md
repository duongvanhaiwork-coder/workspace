---
name: question-scope
description: Use when the user sends /question-scope or /question-scope L1–L4 only. Opt-out qs:off, no-scope, quick:, sp:off, no-sp. level Lx and ?+keyword do not activate.
---

# Question Scope

**Language:** English only in this file and under `references/`, `templates/`, `examples/`. The **only** Vietnamese doc in this skill is [README.md](README.md) (human guide).

Cursor + Kiro share this skill. **User invocation (canonical):** `/question-scope` or `/question-scope L1`…`L4` only — see [README.md](README.md). **Difference:** Cursor may use `AskQuestion` for level pick; Kiro uses a numbered list — wait for `L1`…`L4` or `/question-scope Lx`.

**Deep dives (load when needed):** [references/README.md](references/README.md) — gray-zones, level-picker, playbooks, superpowers-supplement, pressure-scenarios.

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
- [Related skills](#related-skills)
- [Token depth](#token-depth)

## Instruction precedence

1. System/developer constraints
2. User request — `/question-scope`, `/question-scope Lx`, opt-out tokens; scope opt-outs beat `/question-scope Lx` when both appear (**Conflicting tokens**)
3. This skill (pipelines, gates, work-folder layout only)
4. Rule **`code-standards`** and stack rules (`typescript`, `react`, `python`, …) are canonical for code style, architecture, security, SOLID, size limits, and API conventions — this skill **does not redefine** those.

**Suggest level:** [references/level-picker.md](references/level-picker.md) (flow + host UI).

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

### Opt-out tokens (canonical — same meaning in rule **`@workflow`** when scope is off)

| Token | Question-scope | Superpowers supplement |
| ----- | ---------------- | ------------------------ |
| `qs:off`, `no-scope` | Off | Off |
| **`quick:`** | Off — fast path, **no** L1–L4 options, **no** phased `docs/work/` | Off |
| `sp:off`, `no-sp` | On **only when scope already active**; does **not** activate scope | Off |
| **`/question-scope`** (no `L1`…`L4` on command) | On → four options → STOP | Per level after pick |
| `/question-scope Lx` | On (skip level picker) | Per [supplement by level](references/superpowers-supplement.md#by-level) |

### Parsing

Case-insensitive matching after trim unless noted. **Only** `/question-scope` forms activate this skill.

| Pattern | Activates scope? |
| ------- | ---------------- |
| **`/question-scope`** token | Yes → priority 2 (four options) — match `(^|\s)/question-scope\b` **anywhere** in the message (not required at line start; e.g. `Please /question-scope fix X` **does** activate) |
| **`/question-scope L1`…`L4`** | Yes → priority 1 — `/question-scope` + whitespace + `L1`…`L4` (`l2` → `L2`) |
| **`level L1`…`L4`** (without `/question-scope`) | **No** — use `/question-scope Lx` |
| **`?` + keyword** | **No** |
| **`sp:off` / `no-sp`** | Does not activate scope by itself |

**Scope opt-out** (if any matches, scope is **off** even with `/question-scope Lx`):

| Token | Match |
| ----- | ----- |
| **`quick:`** | Message **starts with** `quick:` OR `(^|\s)quick:` (colon required — avoids matching unrelated prose) |
| **`qs:off` / `no-scope`** | `(^|\s)(qs:off|no-scope)\b` |

**`quick:` is not** “skip design/plan only” while scope runs — use **`sp:off`** for that. **`quick:`** = normal chat + **`code-standards`** / stack rules; trivial edits only.

### Conflicting tokens

If the same message contains **both** a scope trigger (`/question-scope` or `/question-scope Lx`) **and** a scope opt-out (`qs:off`, `no-scope`, `quick:` per table above):

- **Opt-out wins** — do **not** activate question-scope.
- **`/question-scope Lx` does not override** `qs:off`, `no-scope`, or `quick:` in the same message.

`sp:off` / `no-sp` with `/question-scope Lx` (and **no** scope opt-out): run question-scope at that level; supplement off per [supplement by level](references/superpowers-supplement.md#by-level).

**Tests (product code only):** If triggers/gates are implemented in app code, add tests in **that repo** (not under `skills/`). Pilot spec: [examples/pressure-test-pilot.md](examples/pressure-test-pilot.md). Cover: `/question-scope`, `/question-scope Lx`, opt-outs; **`level Lx` and `?` must not activate**. Use **`generate-test`** to mirror repo patterns.

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
3. **Present 4 options** — then **STOP**:

| ID  | Label                                                         |
| --- | ------------------------------------------------------------- |
| L1  | Chat Answer — explain / naming / compare; no repo edits       |
| L2  | Patch — change existing code (few files)                      |
| L3  | Small Feature — new module/API/worker (bounded)               |
| L4  | Large System — multi-service, MCP, AI platform, big migration |

- **Cursor:** `AskQuestion` with four options when available.
- **Kiro / fallback:** numbered list; accept `L2`, `choose L3`, etc.

**Skip options** if user already set level (priority 1): message contains **`/question-scope L1`…`L4`**.

**No preset level:** If scope activated with **`/question-scope`** (no `L1`…`L4` on the command):

1. **Idea** + **Suggest** (one line).
2. **Present exactly four options** (L1–L4 table below) — **Cursor:** `AskQuestion` with four choices when available; **Kiro:** numbered list.
3. **STOP** — do **not** run Context / Spec / Patch / Code until the user picks **one** of L1–L4 (accept `L2`, `choose L3`, `/question-scope L3`, …).
4. **Gray zone** (two levels both fit, user still has not picked): **two-option** AskQuestion (L1 vs L2, L2 vs L3, or L3 vs L4) instead of four — still **STOP** until pick. See [gray-zones](references/gray-zones.md).

**Sticky scope:** Keep chosen level until done or user sends `/question-scope` / `/question-scope Ly`.

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

## Definition of Done

| Level | DoD                                                  |
| ----- | ---------------------------------------------------- |
| L1    | Answer meets outcome; MD if user wants archive       |
| L2    | AC met; tests pass; Review done; work folder or rollup MD |
| L3    | Contract + tests; Regression pass; phased L3 + `STATUS.md` |
| L4    | Full flow + layers; phased L4 + `STATUS.md` complete |

## Superpowers supplement

**Summary:** L3–L4 default on; L2 minimal; L1 none. Opt out: `sp:off` / `no-sp`. Full tables, rule IDs, plan choice, prompts: **[references/superpowers-supplement.md](references/superpowers-supplement.md)**.

## Related skills

| Step          | Skill              |
| ------------- | ------------------ |
| Vague problem | orchestra-decision |
| Plan L3–L4    | architect-plan (default); writing-plans when supplement + large plan |
| Superpowers meta | superpowers (`skill-check-first`) |
| Workflow rule IDs | Load **`@workflow`** (on demand) |
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
