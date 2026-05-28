---
name: generate-test
description: >
  Generate unit tests for changed or new code. Use when the user asks for tests,
  coverage for a function, or test cases for a bug fix. Match the project's
  existing test framework and patterns.
---

**Announce when applying:** `Using generate-test for <module/symbol>.`

Run the project's test command before claiming success — **`verification-before-completion`**.

## When to use

- Behavior or contract changed (tests required)
- User explicitly requests tests for a file or symbol

## Steps

1. Read the target module and **existing tests** in the same area (naming, mocks, fixtures).
2. Use `get_context` / `search_code` if helpers or dependencies are unclear.
3. For shared symbols, call `analyze_impact` to see what else might need test updates.
4. Write tests: happy path, error path, one edge case from requirements.
5. Run the project's test command if available; fix failures before finishing.

## Editor fallback (MCP down or thin context)

When `get_context`, `search_code`, or `analyze_impact` is unavailable, errors, or returns nothing useful:

1. **read_file** the target module and the nearest existing test file(s) in the repo.
2. Use `rg`/grep for the symbol, route, or handler name to find helpers and call sites.
3. Infer mocks/fixtures from those tests — do not invent a new framework or folder layout.
4. State that coverage reasoning is **search-based**, not graph-backed, if impact was not verified.

## Conventions

- Same directory layout as the repo (`test/`, `*.spec.ts`, `*Tests.cs`, etc.)
- Mock external IO; no real DB/API in unit tests
- Test names describe behavior, not implementation

## Do not

- Add tests for config-only or pure refactor changes unless asked
- Introduce a new test framework without user approval
