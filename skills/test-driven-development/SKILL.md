---
name: test-driven-development
description: >
  RED→GREEN→REFACTOR when behavior changes. Also on user request or bug repro — with or
  without question-scope. L3 coordinated path after generate-test/TC table. Skip rename/config-only.
---

# Test-Driven Development (TDD)

## Instruction precedence

Explicit **user** instructions and repo agent policy (e.g. `AGENTS.md`) override this skill — e.g. user says "skip TDD for this spike". Otherwise follow this skill. See **`superpowers`** § Instruction Priority and [CONVENTIONS.md](../CONVENTIONS.md).

## Overview

**Announce when applying:** `Using test-driven-development to <write failing test | implement fix>.`

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User asks to fix/add behavior, write tests first, or repro a bug — run this skill; no `/question-scope` or `docs/work/` required unless user wants them.

### With question-scope

`/question-scope Lx` — L2 Patch / L3–L4 Code per supplement; gates (Spec, `generate-test` before Code on L3–L4) from **`question-scope`** apply first.

### Combines with (optional)

- `systematic-debugging` — repro after root cause
- `verification-before-completion` — before claiming green
- `generate-test` — test design before implement (L3+ coordinated)

### Requires (hard)

- None

**Instruction precedence:** User message → this skill → **`question-scope`** Spec/Test gates when scope active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| RED before production code when **behavior** changes | Skip RED after **`generate-test`** Test phase (L3–L4) |
| **`generate-test`** owns TC table + failing tests in Test phase | Green tests inside Test phase to “save time” |
| **NEXT:** **`verification-before-completion`** before “done” | Claim pass without fresh command output |

Pressure tables + example: [references/pressure-and-examples.md](references/pressure-and-examples.md). Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use

Rule ID: **`tdd-during-implementation`** (normal change) or **`tdd-failing-repro`** (bug overlay).

| Situation | Use TDD? |
| --------- | -------- |
| **Standalone** — behavior/contract change or bug repro (any entry path) | **Yes** when table below applies |
| **Patch / Code** changes **observable behavior** or **contract** | **Yes** — RED → GREEN → REFACTOR |
| **Bug fix** (after root cause in Spec) | **Yes** — failing **repro** test first (`tdd-failing-repro`) |
| **Refactor** with **same** behavior (tests stay green) | **No new failing test** — keep suite green; small steps |
| **Rename / move / format** only — no behavior change | **No** — run existing tests after |
| **Config / deps / comments** only | **No** unless they change runtime behavior |
| **L1** explain-only | **No** |

**Exceptions (ask user once):** throwaway spike, generated code dump, explicit “skip TDD”.

Thinking "skip TDD just this once" for a **behavior** change? Stop — that's rationalization.

## When NOT to use

- Pure refactor/rename per **`question-scope`** L2 playbook — no new tests required; verify after.
- Tests already written and failing for this change (L3) — go to GREEN; do not rewrite from scratch without reason.
- **Before** Spec lists test cases (L2) or TC table filled (L3) — fill those first, then TDD during Patch/Code.

## Pipeline: Patch / Code (question-scope)

| Level | Before Patch/Code | During Patch/Code (this skill) |
| ----- | ----------------- | ------------------------------ |
| **L2** | Spec + **test case rows** in `l2-patch.md` (gate) — use **`generate-test`** if helpful | TDD per change; no worktree default |
| **L3** | **`generate-test`** → TC table in `l3-02` → **`using-git-worktrees`** | TDD **per task/slice** during Code / **`executing-plans`** |
| **L4** | Same as L3 in `l4-03-build.md` | TDD per increment |

**L3–L4 note:** Tests may already exist from **`generate-test`** (Test design) — TDD cycle = run RED on those tests (or add one missing case), then GREEN, then REFACTOR. Do not duplicate the whole TC table in chat. **`generate-test`** must not implement production code to green tests; that happens here in Code.

**After each cycle:** log command + result in phase file; **`verification-before-completion`** before claiming pass.

## Bug overlay (usually L2)

1. **`systematic-debugging`** — root cause in Spec / `STATUS.md` first  
2. **This skill** — write **failing repro** test (`tdd-failing-repro`)  
3. Minimal fix → **`verification-before-completion`**

## With question-scope (summary)

| Topic | Rule |
| ----- | ---- |
| **Plan (`architect-plan`)** | Tasks only — no RED/GREEN lines in phase file |
| **`sp:off`** | TDD still applies on behavior change unless user opts out |
| **Execute B / A** | TDD inside each checkpoint/task |

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## RED → GREEN → REFACTOR cycle

Full detail: [references/tdd-cycle.md](references/tdd-cycle.md).

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |

## Pressure scenarios and rationalizations

Red flags, excuse table, “why order matters,” and bug-fix walkthrough: [references/pressure-and-examples.md](references/pressure-and-examples.md).

## Verification and when stuck

[references/tdd-completion-checklist.md](references/tdd-completion-checklist.md).

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
