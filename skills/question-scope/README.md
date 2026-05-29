# Question Scope — User guide

> **Language:** This file is the **English human guide**. The agent contract is **[SKILL.md](./SKILL.md)** (English).

User guide for choosing level, tokens, prompts, and on-disk docs. Agents read the contract in **[SKILL.md](./SKILL.md)** + **[references/](./references/)** when needed. Cursor rules (no file paths needed): always-on **`question-scope`**, **`code-standards`**; for Superpowers handoff → type **`@workflow`**.

**Related:** [AGENTS.md](../../AGENTS.md) · **`superpowers`** · [STRUCTURE](../STRUCTURE.md) · rule IDs: [superpowers-supplement.md](references/superpowers-supplement.md)

## Common workflow preset Lx only

If you **always pick L yourself** (no bare `/question-scope` or `quick:`) — this is the **standard** path, not a shortcut. The agent **skips** the 4L question step but still runs that level’s pipeline + gates.

**Pipeline skills are composable:** invoke **standalone**, **with `/question-scope Lx`**, or **combined** (e.g. debug + TDD + verify). Mandatory pairs only: [COMPOSITION.md](../COMPOSITION.md). See [CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes and [SKILL.md § Pipeline skills](./SKILL.md#pipeline-skills--standalone-coordinated-and-composition).

### Template (copy-paste)

```text
/question-scope L2 — <description> (@file if any)

/question-scope L3 — <description>
AC: …
docs/work/YYYY-MM-DD-<slug>/
```

Continue a session: `@docs/work/.../STATUS.md` + `/question-scope L3 — continue` (command at **start** or **end** of the line).

### Three typing rules

1. **Position:** `/question-scope Lx` at the **start or end** of the message; **space** before `L` (`/question-scope L2`, not `/question-scopeL2`).
2. **Do not** use `level L2 — …` or `?fix …` — scope **does not** activate (use `/question-scope L2 — …`).
3. **New work item** in the same chat → send `/question-scope Ly` again (same L persists until the task is done).

### Quick L pick (L2 vs L3)

Use [Checklist L2 ↔ L3 (5 questions)](#checklist-l2-vs-l3-five-questions): **one “yes”** → lean **L3**; **all five “no”** → **L2**. Not sure **once** → `/question-scope` + description (agent asks **L2 vs L3**, not all 4L).

| Preset | Also type |
| ------ | --------- |
| L2 one session, few files | `Rollup MD OK.` |
| L3 but skip worktree/SP plan | `sp:off` at end of line |

### Is the agent running the right pipeline?

| Signal | L2 | L3 |
| ------ | -- | -- |
| Header | `Level: L2 \| Pipeline: …` | `Level: L3 \| Pipeline: …` |
| Disk | `docs/work/…` + Spec in `l2-patch` (or rollup) | `l3-01`…`l3-03` + `STATUS.md` |
| Before behavior change | TC in Spec / `l2-patch` | **`generate-test`** (RED) in `l3-02` **before** code |
| Step done | Log test commands in phase MD | Verify + **Regression** (module + 1-hop) with output |

If the agent **jumps to code**, skips `docs/work/`, or claims **“done”** without test logs → remind the gate (“no Spec yet”, “no TC table”, “run verify and paste output”). Details: [pipelines-quickref.md](references/pipelines-quickref.md).

**Stale rule cache:** after `make sync-ide`, **reload window** or start a new chat if the agent still treats `level Lx` / `?` as triggers — `./scripts/check-question-scope-session.sh` (AI Core repo).

### Token decision tree (one line)

```text
(Most common — L already known) → /question-scope L2|L3|L4 — …  ← see § Common workflow preset above
What to do? → Ask only / no repo edits → /question-scope L1
            → Quick fix, scope off → quick: … or qs:off — …
            → Review/audit skill or rule → qs:meta — … or audit: — …
            → Patch a few files → /question-scope L2 — …
            → Bounded feature + Regression/Ship → /question-scope L3 — …
            → Multi-service / platform → /question-scope L4 — …
            → Unsure of L → /question-scope + description (agent asks 4L or 2L gray zone, STOP)
            → L3/L4 but skip worktree/SP plan → /question-scope L3 — … sp:off
            (Do not use level Lx or ?fix — skill does not activate.)
```

## Table of contents

- [Common workflow preset Lx only](#common-workflow-preset-lx-only)
- [Token decision tree](#token-decision-tree-one-line)
- [How to invoke — `/question-scope` only](#how-to-invoke-question-scope-only)
- [Sample prompts (copy-paste)](#sample-prompts-copy-paste)
- [Presets & anti-patterns](#presets-and-anti-patterns)
- [One-liner memory](#one-liner-memory)
- [Choose level (L1–L4)](#choose-level-l1-l4)
- [No L on command — level picker (2 or 4)](#no-l-on-command--level-picker-2-or-4-options)
- [Tokens — enable / disable & triggers](#tokens-enable-disable-triggers)
- [Pipeline skill summary](#pipeline-skill-summary)
- [Superpowers supplement by level](#superpowers-supplement-by-level)
- [On-disk docs](#on-disk-docs)
- [Per-level checklists (user)](#per-level-checklists-user)
- [Bug (usually L2)](#bug-usually-l2)
- [Quick decision](#quick-decision)
- [Files in this folder](#files-in-this-folder)

---

## How to invoke — `/question-scope` only

This is the **only** invocation style the team recommends (do not use a `level` prefix in the prompt).

| You want | Type |
| -------- | ---- |
| Unsure L1–L4 | `/question-scope` + task description → agent asks **pick 1 of 4L** → waits for you |
| Level already chosen | `/question-scope L2` + description (replace `L2` with L1/L3/L4) |
| No 4L ceremony | `quick: …` or `qs:off — …` |
| Review/audit skill or rule (no L1–L4 run) | `qs:meta — …` or `audit: — …` |
| L3/L4 but skip SP supplement | `/question-scope L3 — … sp:off` |

**No longer supported:** `level L2 — …` and `?fix …` — skill **does not** activate. Use `/question-scope` or `/question-scope L2`.

**Level format:** **space** required — `/question-scope L2` (correct), not `/question-scopeL2` (wrong → agent asks 4L again).

**Command position:** `/question-scope` only at **start** or **end** of the message (after trim) — not mid-sentence. Correct: `/question-scope L2 — fix auth` or `fix auth /question-scope L2`. Wrong: `Please /question-scope fix auth`.

**Review / audit skill** (e.g. path `skills/question-scope`, “don’t use `/question-scope` for this task”) — **does not** start the pipeline; prefer `qs:meta — …` or `audit: — …` (or `qs:off` to be sure).

---

## Sample prompts (copy-paste)

Replace `<description>`, `@path`, date/slug. English examples also in: [examples/sample-prompts.md](examples/sample-prompts.md).

| Situation | Paste into chat |
| --------- | --------------- |
| One-line fix, no L1–L4 | `quick: <description>` |
| Patch / bug, few files | `/question-scope L2 — <description> (@file)` |
| New feature (API, module) | `/question-scope L3 — <description>` |
| Migration / many services | `/question-scope L4 — <description>` |
| Ask only, no code changes | `/question-scope L1 — <question>` |
| Don’t know which L | `/question-scope` + task description |
| Turn off scope ceremony | `qs:off — <description>` |
| L3/L4 but no worktree/SP plan | `/question-scope L3 — <description>. sp:off` |
| Continue old session | `@docs/work/.../STATUS.md` + `/question-scope L3 — continue` (command at **start** or **end** of line) |

```text
quick: change "teh" to "the" in README.md
```

```text
/question-scope L2 — fix: API returns 400 when phone field is missing (@src/routes/user.ts).
```

```text
/question-scope L3 — add GET /orders/export endpoint returning CSV.

AC: auth required; max 10k rows. docs/work/2026-05-22-order-export/
```

```text
/question-scope

Need product image upload max 5MB, store on S3, public URL TTL 7 days.
```

```text
/question-scope L2 — bug: form submit returns 500 when email is duplicate (@api/register.ts).
```

---

## Presets & anti-patterns

English presets: [examples/sample-prompts.md § Presets](examples/sample-prompts.md#presets). Agent contract (Regression): [SKILL.md § Pipelines](./SKILL.md#pipelines-ui).

### Presets (copy-paste)

| Preset | When | Paste into chat |
| ------ | ---- | --------------- |
| **Fast** | Typo, one line, **scope off** (no L1–L4, no `docs/work/`) | `quick: <description>` |
| **Explain** | Ask only, no repo edits | `/question-scope L1 — <question>` |
| **Patch** | Fix/bug, few files, clear AC | `/question-scope L2 — <description> (@file)` |
| **Light patch** | L2 with minimal MD (one session, ≤ ~3 files) | `/question-scope L2 — <description>. Rollup MD OK.` |
| **Feature** | Bounded module/API/worker + AC | `/question-scope L3 — <description>` + AC; `docs/work/YYYY-MM-DD-<slug>/` |
| **Feature (minimal SP)** | L3 but no full worktree/SP plan | `/question-scope L3 — <description>. sp:off` |
| **System** | Multi-service, large migration | `/question-scope L4 — <description>` |
| **Pick L** | Unsure L1–L4 — agent runs **level picker** (**2** labeled options in gray zone, else **4**) | `/question-scope` + description (command **without** L1–L4) |
| **Continue session** | Work in progress | `@docs/work/.../STATUS.md` + `/question-scope L3 — continue` |
| **Vague idea** | No problem statement / AC yet | `/question-scope` + description; agent may run **orchestra-decision** before asking 4L |

**Use `/question-scope` only** — `?fix …` **does not** activate the skill.

### Vague idea (orchestra-decision)

When there is no problem statement or AC yet, the agent may run **`orchestra-decision`** before asking L1–L4:

```text
/question-scope

Need product image upload — unclear whether S3 or local storage, no size limit yet.
```

After 2–4 lines of problem + outcome, the agent returns to **Suggest** + level pick (often L2 vs L3 or 4L).

### Anti-patterns (avoid)

| Wrong | Consequence | Do instead |
| ----- | ----------- | ---------- |
| `level L2 — …` (no `/question-scope`) | Scope **does not** activate | `/question-scope L2 — …` |
| Long sentence without `/question-scope` | Scope **does not** activate | `/question-scope` or `/question-scope L2 — …` |
| `/question-scope L2` + `quick:` same message | Opt-out wins — **no** scope run | One only: `quick:` **or** `/question-scope L2` |
| `quick:` but want L2 + light rollup MD | Scope **off** — no STATUS/rollup | `/question-scope L2 — <description>. Rollup MD OK.` (**Light patch** preset) |
| `sp:off` alone without `/question-scope` | Scope **does not** auto-activate | `/question-scope L3 — … sp:off` |
| `/question-scopeL2` (no space before L) | Not L2 preset — agent asks 4L | `/question-scope L2 — …` |
| Audit/review skill, path `skills/question-scope` | Scope **does not** activate (meta) | `qs:meta — …` or `audit: — …` (or `qs:off — …`) |
| Large patch stuck at L2 (new module, >5 files) | Missing test/regression/ship | Escalate to L3 or send `/question-scope L3` |
| L3 without AC / `docs/work/` slug | Agent guesses scope | 3–5 AC bullets + folder slug in prompt |

### Checklist L2 ↔ L3 (5 questions)

Use when **unsure** patch vs feature. **One “yes” → lean L3** (or pick L2 with `Minimal ceremony` if you want it light on purpose).

| # | Question |
| - | -------- |
| 1 | New **top-level module/package/folder**? |
| 2 | New **worker / queue / cron / async pipeline**? |
| 3 | Expect **> ~5 files** or **multiple sessions / PRs**? |
| 4 | **Multiple endpoints**, public contract docs, or API **versioning**? |
| 5 | Need full **Regression + Ship** (not just patch-area tests)? |

**All five “no”** → **`/question-scope L2`** is reasonable. Agent: [gray-zones.md § Quick checklist](references/gray-zones.md#quick-checklist-l2-vs-l3) · template [`l2-patch.md`](templates/phases/l2/l2-patch.md).

```text
/question-scope L2 — add POST /products/export CSV (same pattern as GET /products). Minimal ceremony.
```

```text
/question-scope L3 — notifications/ module (email + push stub), new contract.
```

### Regression (L3/L4)

| Level | Default run | Not required (unless AC says so) |
| ----- | ----------- | -------------------------------- |
| **L2** | **Verify** — test/smoke patch area + 1-hop callers | Full repo / monorepo suite |
| **L3** | Tests for touched **module/package** + **1-hop** integration calling changed API/surface; log commands in `l3-02-build-prove.md` | Entire monorepo |
| **L4** | Tests per **affected service** (plan/validate); CI slice OK if noted in phase MD | “Run everything” unless named in plan |

**High-risk L2 patch** (shared lib, auth): still L2 but ask agent for broader suite in Verify, or switch to **`/question-scope L3`** if you need formal Regression gate.

---

## One-liner memory

| Layer | Answers |
| ----- | ------- |
| **Question-scope** | **How much** work (L1–L4), gates, `docs/work/…` |
| **Superpowers supplement** | **How well** (TDD, verify, worktree, plan…) — default L3/L4, minimal L2 |

The two layers **do not replace each other**. Scope picks “how much”; Superpowers (when on) picks “how to do each step”.

---

## Choose level (L1–L4)

### What is L?

**L** = **Level** (work **scope**). Higher **L1**–**L4** means fuller pipeline, tests, and `docs/work/` — **not** “read many files from the first message”. Context opens **gradually by step** (see [Progressive context (JIT)](#progressive-context-jit-summary) and [SKILL.md § Progressive context](./SKILL.md#progressive-context-jit)).

| Level | Use when | Edit code? | Pipeline (summary) |
| ----- | -------- | ---------- | ------------------- |
| **L1** | Explain, compare, naming; no patch | No | Light context → Answer |
| **L2** | Small patch, few files, clear AC | Yes | Context → Spec → Patch → Verify → Review → MD |
| **L3** | Bounded feature (module, API, worker) | Yes | Context → Spec → Plan → Test → Code → Verify → **Regression** → Review → Ship → MD |
| **L4** | Multi-service, large migration, AI platform | Yes | **15-step** Full Flow + Architecture / AI / Delivery |

**Quick hint (not locked):** ask only → L1 · few files / bug → L2 · new feature with contract → L3 · system / many services → L4.

**Pipeline & playbook:** [SKILL.md § Pipelines](./SKILL.md#pipelines-ui) · [playbooks.md](references/playbooks.md) · **[pipelines-quickref.md](references/pipelines-quickref.md)** (~120 lines — agent reads this when working, saves tokens) · [pipelines-skill-map.md](references/pipelines-skill-map.md) (detail — open **one §** by level/skill, not the whole file). **L4 preset:** skip Idea/Scope — start from Context.

**Phase file map (L2–L4):**

| Level | Phase files |
| ----- | ----------- |
| L2 | `STATUS.md` + `l2-patch.md` (or single rollup file) |
| L3 | `l3-01-define` (Context+Spec+Plan) → `l3-02-build-prove` (Test→…→Iterate) → `l3-03-ship` |
| L4 | `l4-00-frame` … `l4-05-ship` (see [templates/phases/README.md](./templates/phases/README.md)) |

### Progressive context (JIT) — summary

| Term | Meaning |
| ---- | ------- |
| **Symptom** | You **write** error/AC description in chat — **no** `@` required. |
| **Path from user** | File/folder you **`@`** or type in the message. |

**First turn (suggested):** `/question-scope Lx` + symptom; L2 add **0–1** suspected `@` file. Agent **expands** context after **Spec** / plan / gate — no repo-wide scan before Spec (L2).

**L2 example:**

```text
/question-scope L2 — POST /register returns 400 when phone is missing.

@src/routes/register.ts
```

Details: [SKILL.md § Progressive context (JIT)](./SKILL.md#progressive-context-jit).

### Level boundaries (heuristic — you may override)

Agent may suggest L3 for “new endpoint in one file”; if you want **lighter** (fewer phases, no full regression), state **`/question-scope L2`** clearly.

| Situation | Typical level | Choose lighter |
| --------- | ------------- | -------------- |
| Explain / compare only | **L1** | — |
| Fix or extend **existing** code, few files | **L2** | `/question-scope L2` even for one new endpoint if L3 ceremony not needed |
| New module, API contract, worker, many files | **L3** | — |
| Many services, platform, large migration | **L4** | — |

Gray zone detail: [references/gray-zones.md](references/gray-zones.md) · [SKILL.md § Level boundaries](./SKILL.md#level-boundaries-heuristic-user-may-override).

### Gray zone — pick L when boundary is fuzzy

Agent **does not** auto-pick a heavier level when a lighter one fits. Cursor: **AskQuestion** with two choices (L1/L2, L2/L3, or L3/L4) then **STOP**.

| Pair | Quick hint |
| ---- | ---------- |
| **L1 vs L2** | Explain only → L1 · need code change / AC → L2 |
| **L2 vs L3** | Use [Checklist L2 ↔ L3 (5 questions)](#checklist-l2-vs-l3-five-questions) |
| **L3 vs L4** | [l3-vs-l4-diff.md](references/l3-vs-l4-diff.md) · one repo → L3 · multi-service + Validate → L4 |

**Full table:** [references/gray-zones.md](references/gray-zones.md) · agent checklist: [Quick checklist L2 vs L3](references/gray-zones.md#quick-checklist-l2-vs-l3).

---

## No L on command — level picker (2 or 4 options)

When you type **`/question-scope`** + description and the command **does not** include `L1`…`L4` (i.e. not `/question-scope L2`):

1. Agent summarizes **Idea** + **suggests** one L (not locked).
2. Shows **4 choices** (or **2** in gray zone) — each option includes **what that L will do** so you can compare (Cursor: `AskQuestion` labels; Kiro: numbered list). Copy: [level-picker.md § Option copy](references/level-picker.md#option-copy-required--user-must-read-before-pick).
3. Agent **STOPs** — no Spec / code / `docs/work/` until you reply `L2`, `choose L3`, or resend `/question-scope L3 — …`
4. **Gray zone** (L1↔L2, L2↔L3, L3↔L4): only **2 labeled options** — still must choose before continuing.

| ID | What you get if you pick it (agent shows this beside each option) |
| -- | ------------------------------------------------------------------ |
| **L1** | Explain only · **no repo edits** · answer in chat (optional archive) |
| **L2** | Spec → patch **few files** → verify + review · light `docs/work/` |
| **L3** | Plan + **test-before-code** → feature build → regression + ship · phased `l3-*` |
| **L4** | **15-step** full flow · multi-service impact · phased `l4-*` |

**Skip the pick step** if the prompt already has `/question-scope L2 — …` (or L1/L3/L4) + description.

```text
/question-scope

Need image upload API max 5MB, S3, URL TTL 7 days.
→ Agent: Idea + Suggest + level picker (2 or 4) → you reply L3 → L3 pipeline starts
```

---

## Tokens — enable / disable & triggers

| Token / entry | Summary |
| ------------- | ------- |
| `/question-scope L1`…`L4` | Scope on, **no** 4-option ask — **standard when L is known** |
| `/question-scope` (no L) | Idea → suggest → **pick 1 of 4L** → **STOP** |
| `quick:` / `qs:off` / `no-scope` | **Off** scope (fast path or normal chat) |
| `qs:meta` / `audit:` | **Off** scope — audit/review skill or rule (recommended when reviewing) |
| `sp:off` / `no-sp` | Scope **on** (when trigger already active), supplement **off** — does not activate scope alone |
| `qs:off` + `/question-scope L2` same message | **Opt-out wins** — scope does not run (see SKILL § Conflicting tokens) |

Full table: [SKILL.md § When this skill applies](./SKILL.md#when-this-skill-applies).

---

## Pipeline skill summary

**When agent runs scope:** read [pipelines-quickref.md](references/pipelines-quickref.md) (~120 lines). One skill in depth: [pipelines-skill-map.md §6.x](references/pipelines-skill-map.md#6-skill-deep-dive--purpose-when-called-what-it-does) — **do not** load the full ~700-line file.

| Skill | Purpose (one line) | Usually at | Agent does (summary) |
| ----- | ------------------ | ---------- | -------------------- |
| `orchestra-decision` | Fast direction when idea is still vague | Before L pick / unclear AC | Q1–Q4 → 2–5 options → **1 decision**; no spec/plan write |
| `superpowers` | Know which skills run after L is chosen | Right after L2–L4 pick | Read supplement; map phase → skill; honor `sp:off` |
| `explain-code` | Explain code, no edits | L1; before editing unfamiliar code | `get_context` / read files → entry flow → dependencies |
| `brainstorming` | Spec/design **approved** before code | L3–L4 Spec (skip if spec exists) | Ask gradually → 2–3 directions → `docs/specs/…` → user approve |
| `architect-plan` | Moderate plan in phase file | L3 Plan (≤12 tasks) | Checkbox tasks + files + `verify:` in `l3-01` |
| `writing-plans` | Large plan / handoff / subagent A | >12 tasks or user picks A | Detailed `docs/plans/…`; phase file links only |
| `generate-test` | Tests **before** production code | L3–L4 Test; L2 optional | TC table + **RED** tests; log fail; no prod code |
| `using-git-worktrees` | Isolated branch/worktree | L3–L4 before Code | `.worktrees/…` + baseline test |
| `executing-plans` (B) | Execute plan same session, checkpoints | L3–L4 Code (default) | Per task: TDD → verify → done → Regression/Ship |
| `subagent-driven-development` (A) | One subagent per task + review | L3–L4 when `docs/plans/` + pick A | Implementer → spec review → code review / task |
| `test-driven-development` | Behavior change proven by tests | L2 Patch; each L3–L4 task; bugs | RED → GREEN → REFACTOR |
| `verification-before-completion` | No “done” without command log | Verify, Regression, Ship, bug fix | Run **fresh** commands → paste output → then claim |
| `systematic-debugging` | Root cause before fix | Bug (usually L2 Spec) | 4 investigation phases → record cause in Spec |
| `analyze-impact` | Which files/services are affected | L4 Discover; L3/L2 optional | MCP/rg → impact list; **does not** replace Regression tests |
| `caveman-review` | Short diff review with concrete fixes | Review L2+ | `L42: bug. fix.` per line |
| `requesting-code-review` | Formal pre-merge review | L4 (default); L3 if AC | Subagent reviewer after green tests + caveman |
| `receiving-code-review` | Handle PR comments correctly | After PR opened | Read → understand → verify → fix each item + test |
| `finishing-a-development-branch` | Finish git (merge/PR/…) | End of L3–L4 Ship | Re-verify → user picks 1 of 4 options |
| `dispatching-parallel-agents` | Many **independent** failures in parallel | Bug/Iterate multi-domain | 1 agent/domain; no same-file edits |
| `code-standards` | Quality & security on every edit | Every Patch/Code (rule) | Validate, SOLID, no secrets in logs |

**Full pipeline table (when needed):** [pipelines-skill-map.md](references/pipelines-skill-map.md) — open **one** § by level (§1–§5).

---

## Superpowers supplement by level

Applies **after** `/question-scope Lx` is set. Summary: **L3/L4** full on (worktree, TDD, verify…); **L2** minimal (TDD + verify on behavior change); **L1** none. Off: `sp:off` / `no-sp`.

| Level | Default |
| ----- | ------- |
| L1 | None |
| L2 | TDD + verify |
| L3 | worktree, TDD, execute **inline (B)**, verify, ship |
| L4 | Near full flow + design gate / plan when scope is large |

**Execute:** **B** (L3 default, plan in `docs/work/`) or **A** (subagents — **requires** `docs/plans/…` from `writing-plans`). Rule ID detail: [superpowers-supplement.md](references/superpowers-supplement.md) · load **`@workflow`** in chat.

**Agent:** While scope **waits for L pick**, do not run `brainstorming` / `writing-plans` / `using-git-worktrees` — see **`superpowers`**.

### Skill chain (L3 — after level is chosen)

```text
/orchestra-decision          ← only when idea still vague (before or early in define)
brainstorming                ← spec/design + user approve (L3–L4; L2 usually skip)
architect-plan  |  writing-plans   ← plan: phase file  |  docs/plans/ (large / subagents)
generate-test                ← TC table in l3-02 (BEFORE Code)
using-git-worktrees          ← branch/worktree (L3 default; skip if sp:off)
executing-plans (B)  |  subagent-driven-development (A)
test-driven-development      ← per task when behavior changes
Verify + Regression          ← verification-before-completion (log l3-02; L3 requires Regression)
caveman-review               ← quick diff review (L2+)
requesting-code-review       ← L4 supplement: formal pre-merge (before Ship git; not duplicate per-task review on path A)
l3-03-ship / l4-05-ship      ← refine, rollout, rollback
finishing-a-development-branch  ← merge/PR/keep/discard; re-verify (fresh)
receiving-code-review           ← after PR comments (incoming; rule incoming-code-review)
```

**Plan routing:** ≤12 tasks + ≤8 files → `architect-plan`; larger or subagents → `writing-plans`. Details: [superpowers-supplement.md](references/superpowers-supplement.md).

---

## On-disk docs

**`<target-repo>`** = repo you are editing (e.g. `projects/my-app/`), not `Workspace/` except AI Core meta work.

### Single source of truth (avoid drift)

| Scope | Where |
| ----- | ----- |
| L2, small L3 | AC + plan in **`docs/work/YYYY-MM-DD-<slug>/`** |
| Large L3 / L4 | May add `docs/specs/…`, `docs/plans/…` — phase file **links only**, do not duplicate full AC in two places |

### Structure by level

```text
docs/work/2026-05-22-my-feature/
  STATUS.md              ← read at new session start (@STATUS.md)
  l2-patch.md            ← L2
  l3-01-define.md        ← L3
  l3-02-build-prove.md
  l3-03-ship.md
  l4-00-frame.md …       ← L4
```

Templates: [templates/phases/](./templates/phases/) · L1 optional: `docs/answers/…`

**New session:** `@docs/work/.../STATUS.md` + current phase file — do not rely on old chat alone.

---

## Per-level checklists (user)

### L1

1. Send `/question-scope L1` + question (`@file` if needed, max 1–2 files).
2. Receive answer in chat.
3. (Optional) save `docs/answers/YYYY-MM-DD-<slug>.md`.

### L2

1. `/question-scope L2` + description + `@file`.
2. Agent: Spec (AC; bug → root cause first). If behavior changes: TC table in `l2-patch` (optional **`generate-test`**).
3. Patch → TDD if behavior changes → run tests in affected area → review.
4. Update `docs/work/…` (small patch may use one rollup file).

### L3

1. `/question-scope L3` + desired AC.
2. `docs/work/…` + define (spec/plan; may use `brainstorming` → `architect-plan`).
3. `l3-02`: **TC table** (`generate-test`) → **worktree** (`using-git-worktrees`) → code (TDD).
4. Verify → **regression** → ship (rollout/rollback).
5. Update `STATUS.md` each phase.

### L4

1. `/question-scope L4` — treat Idea/Scope as done.
2. **Discover** (`l4-01`): **`analyze-impact`** if blast radius unclear → Validate go/no-go.
3. Define → Build (`l4-03`: **`generate-test`** + TC) → **Prove**: Verify + **Regression** → **`caveman-review`** → **`requesting-code-review`** (default supplement).
4. Ship (`l4-05`) + `finishing-a-development-branch`.
5. Architecture / AI / Delivery in L4 phase files when applicable.

**Impact ≠ Regression:** `analyze-impact` = affected list; Regression = run tests + log (`verification-before-completion`).

---

## Bug (usually L2)

Order in pipeline:

1. Record **root cause** (Spec or `STATUS.md`) — do not fix randomly.
2. Failing test reproduces issue (if behavior changes).
3. Fix → verify with logged output.

Prompt:

```text
/question-scope L2 — bug: form submit returns 500 when email is duplicate (@api/register.ts).
```

More examples: [Sample prompts](#sample-prompts-copy-paste) above.

---

## Quick decision

Text: **One-liner memory** + level table above. Flowchart + IDE: [references/level-picker.md](references/level-picker.md).

---

## Files in this folder

| File | Who reads |
| ---- | --------- |
| **README.md** (this file) | Human — English guide: presets, anti-patterns, L2↔L3 checklist, Regression |
| **references/CHEATSHEET.md** | Human — one-pager English (trigger, token, level) |
| **examples/sample-prompts.md** | Human / agent — sample prompts (English) |
| **SKILL.md** | Agent — contract, gates, pipeline (core) |
| **references/** | Agent — **pipelines-quickref** (default), playbooks, pipelines-skill-map (per §), supplement ([index](references/README.md)) |
| **templates/phases/** | Agent copies when creating `docs/work/…` ([STRUCTURE.md](../STRUCTURE.md)) |

**Canonical:** If README and SKILL.md diverge, prefer **SKILL.md** and **references/**.
