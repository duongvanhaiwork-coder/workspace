# TDD pressure scenarios and examples

Moved from `test-driven-development/SKILL.md` (2026-05-29). Load when agent rationalizes skipping RED or needs a bug-fix walkthrough.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test (when **behavior** changes)
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once" on a **behavior** change
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."
- Writing a **new failing test** for **rename/move/format-only** with unchanged behavior

**All of these mean: Delete code. Start over with TDD** — when the change actually affects behavior.

**Not red flags (no new RED required):** refactor with **same** observable behavior (tests stay green); rename/move; config-only — run existing tests after (**`question-scope`** L2 playbook).

## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

## Why order matters (Q&A)

**"I'll write tests after to verify it works"** — Tests written after code pass immediately. Passing immediately proves nothing (wrong target, implementation bias, missed edges). Test-first forces you to see the test fail.

**"I already manually tested all the edge cases"** — Manual testing is ad-hoc: no record, no re-run, easy to forget cases under pressure.

**"Deleting X hours of work is wasteful"** — Sunk cost. Keeping unverified code is technical debt; delete and rewrite with TDD when behavior must be trusted.

**"TDD is dogmatic; pragmatic means adapting"** — TDD finds bugs before commit, prevents regressions, documents behavior, enables refactor. Shortcuts = production debugging.

**"Tests after achieve the same goals"** — Tests-after ask “what does this do?” Tests-first ask “what should this do?” Thirty minutes of tests-after ≠ TDD proof.
