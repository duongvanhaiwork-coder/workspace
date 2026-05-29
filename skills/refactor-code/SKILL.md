---
name: refactor-code
description: >
  Refactor safely with minimal scope: match project style, preserve behavior, use
  analyze_impact before cross-module changes. Use for "refactor", "clean up",
  "extract", "rename", or reducing duplication.
---

**Announce when applying:** `Using refactor-code for <scope>.`

For shared symbols, run **`analyze-impact`** first (or search fallback). After edits, run tests; before claiming pass, use **`verification-before-completion`**.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User asks to refactor/clean up/rename — run this skill; no `/question-scope` required.

### With question-scope

Fits **L2** patch or **L3** code tasks; honor Spec/plan and TDD gates when scope active — no behavior change unless requested.

### Combines with (optional)

- `analyze-impact` — shared symbols
- `verification-before-completion` — after edits

### Requires (hard)

- None for trivial local edits
- **`analyze-impact`** (or documented search fallback) when the change touches a **shared symbol** across modules or services

**Instruction precedence:** User message → this skill → **`question-scope`** Patch/Code gates when scope active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Smallest diff; preserve outward behavior | Behavior change unless the user explicitly asked |
| **`analyze-impact`** before rename/extract across modules | Skip impact on shared symbols because “it’s a small refactor” |
| **`verification-before-completion`** before claiming tests pass | “Should pass” / linter-only when compile or tests matter |
| One concern per change set | Mix refactor with unrelated features in the same commit |

**REQUIRES:** `analyze-impact` when shared symbols · **NEXT:** `verification-before-completion` after edits

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use

- User wants structure improved without changing outward behavior
- Rename or extract shared logic across files

## Steps

1. Read surrounding code; match naming, patterns, and layer boundaries.
2. If the change touches a shared symbol, run `analyze_impact` first.
3. Prefer the smallest diff: one concern per change set.
4. Update all call sites found by search/impact tools.
5. Run existing tests or linters for touched projects.

## Rules

- No behavior change unless explicitly requested
- No new abstractions for one-off use
- Do not mix refactor with unrelated features in the same commit

## After refactor

- List files touched and why
- Note any follow-up tests or index refresh if public API changed
