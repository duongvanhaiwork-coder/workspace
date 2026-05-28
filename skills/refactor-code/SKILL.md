---
name: refactor-code
description: >
  Refactor safely with minimal scope: match project style, preserve behavior, use
  analyze_impact before cross-module changes. Use for "refactor", "clean up",
  "extract", "rename", or reducing duplication.
---

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
