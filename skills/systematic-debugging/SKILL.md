---
name: systematic-debugging
description: >
  Root cause before fixes for any bug, test failure, or unexpected behavior. Standalone
  or question-scope L2+ bug overlay. Do not patch until investigation completes.
---

# Systematic Debugging

**Announce when applying:** `Using systematic-debugging for <symptom/test failure>.`

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

Bug, failing test, or unexpected behavior — run this skill immediately; root cause in chat or a note file; no `/question-scope` required.

### With question-scope

`/question-scope L2+` bug overlay — root cause in Spec or `STATUS.md` **before** Patch; same four-phase process.

**JIT (scope on):** IDE-ALIGNED §2 — stack trace + `@file` first; no repo-wide grep before hypothesis.

### Combines with (optional)

- `test-driven-development` — when fix changes behavior
- `verification-before-completion` — after fix

### Requires (hard)

- Root cause documented before code fix (this skill’s Iron Law)

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Four phases complete; root cause written before fix | Patch or “try this” before Phase 1 |
| **`test-driven-development`** repro when behavior changes | Skip verify — use **`verification-before-completion`** after fix |
| **NEXT:** **`test-driven-development`** → **`verification-before-completion`** | Substitute **`analyze-impact`** for debugging |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## Question-scope bug overlay (usually L2)

When **`question-scope`** is active and the item is a **defect**, this skill runs **inside** the level pipeline — not as a separate level. See **`question-scope`** → [Bug overlay](../question-scope/SKILL.md#bug-overlay-any-level-with-a-defect).

| Step | Skill / rule |
| ---- | ------------- |
| 1 | **`systematic-debugging`** (this skill) — root cause in Spec or `STATUS.md` **before** Patch |
| 2 | **`test-driven-development`** — failing repro (`tdd-failing-repro`) when behavior changes |
| 3 | Fix (minimal) |
| 4 | **`verification-before-completion`** — evidence before “fixed” |

- **Do not** run **`brainstorming`** for a narrow bug on L2 unless the user escalates to L3.
- **Do not** skip root cause to patch symptoms.

## Four phases (root cause first)

Full detail: [references/four-phases.md](references/four-phases.md).

## Red flags and rationalizations

See [references/debugging-pressure.md](references/debugging-pressure.md).

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

These techniques are part of systematic debugging — see `references/`:

- **[references/root-cause-tracing.md](references/root-cause-tracing.md)** — trace bugs backward through call stack
- **[references/defense-in-depth.md](references/defense-in-depth.md)** — validation at multiple layers after root cause
- **[references/condition-based-waiting.md](references/condition-based-waiting.md)** — condition polling instead of arbitrary timeouts

**Related skills:**
- **REQUIRES (phase 4):** `test-driven-development` — failing test case (Phase 4, Step 1)
- **NEXT:** `verification-before-completion` — before claiming fixed

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common
