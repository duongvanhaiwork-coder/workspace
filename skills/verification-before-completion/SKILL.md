---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

**Announce when applying:** `Using verification-before-completion before claiming <done|fixed|tests pass>.`

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

Before “done”, “fixed”, or “tests pass” in any task — run fresh commands and paste evidence; applies with or without scope.

### With question-scope

Required at L2 Verify, L3–L4 Verify + Regression, Ship, and after bug fixes; log in phase MD when scope active.

### Combines with (optional)

- `Any skill that claims done — invoke before success claims`
- `finishing-a-development-branch` — Step 1

### Requires (hard)

- None

**Instruction precedence:** User message → this skill → **`question-scope`** gates only when `/question-scope Lx` is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Fresh command output in **this** message before “done” / “fixed” / “pass” | Previous run, linter-only, or “should pass” |
| Log Verify + Regression in phase MD when scope on | Skip Regression on L3–L4 when supplement requires it |
| **NEXT:** **`finishing-a-development-branch`** when integrating work | Merge/PR claims without Step 1 verify here |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## Terminology (question-scope)

| Term | Meaning |
| ---- | ------- |
| **Phase Verify** | Scoped check after Code/Patch — TC rows, smoke, impacted tests (L2: patch scope + 1-hop; L3: per TC in `l3-02`) |
| **Phase Regression** (L3–L4 only) | **Broader** than Verify — touched **module/package** + **1-hop** integration; separate step in pipeline; still log commands + output here |
| **TDD regression (red-green repro)** | Bugfix discipline below — **not** the same as phase Regression |

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| TDD regression (red-green) works | Revert-fix-fail-restore cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**TDD regression (red-green repro — not phase Regression):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Test design (RED — `generate-test` before Code):**
```
✅ [Run test command] [See: N failures — missing implementation] "RED as expected; not ready for done"
❌ "All tests pass" / "Phase complete" while behavior tests still fail for missing code
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## With question-scope (L2–L4)

Rule IDs: **`verify-before-done`** (Verify / done / ship) · **`verify-fix-evidence`** (bug overlay — same skill).

| Level | Pipeline step | What to verify | Where to log |
| ----- | ------------- | -------------- | ------------ |
| **L2** | **Verify** only (no Regression step) | Impacted tests / smoke for patch + 1-hop | `l2-patch.md` § Verify |
| **L3** | **Verify** then **Regression** (both required) | Verify: TC/smoke per row · Regression: module/package + 1-hop suite | `l3-02-build-prove.md` — Test design log (RED) + **Verify + regression** tables |
| **L4** | **Prove:** Verify → Review → Regression | Per `l4-04-prove.md`; service-scoped when AC requires | `l4-04-prove.md` |

**Per task during Code:** run verify after each task (`executing-plans` / TDD) — same gate, can log in Implementation log.

**Ship:** **`finishing-a-development-branch`** Step 1 runs tests again — **fresh** evidence; do not skip because Verify/Regression logged earlier.

When **`docs/work/…`** is active, record in the phase file — **not chat-only**. Copy **exact command** + **output summary** (e.g. `34 passed, 0 failed`). Update **`STATUS.md`** when the phase completes.

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
