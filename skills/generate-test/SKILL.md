---
name: generate-test
description: >
  Test design before Code (L3–L4 gate) or optional L2 TC rows. Author TC table + failing
  tests; no production code in Test phase. Also on user request.
---

**Announce when applying:** `Using generate-test for <module/symbol>.`

Run the project's test command before claiming success — **`verification-before-completion`**.

## When to use

| Situation | Run? |
| --------- | ---- |
| User asks for tests / coverage for a symbol | **Yes** |
| Behavior or contract changed (tests required) | **Yes** |
| **question-scope L2** — behavior change in `l2-patch.md` | **Optional** — fill TC rows in phase file (or by hand); then **`test-driven-development`** during Patch |
| **question-scope L3** — **Test design** phase before **Code** | **Yes** (gate) — `l3-02-build-prove.md` TC table + tests per TC-xx |
| **L4** — Test design in `l4-03-build.md` before implement | **Yes** (gate) — map TC to A* rows |
| Config-only or pure rename (no behavior change) | **No** unless asked |
| Tests already exist for all TC-xx in phase file | **Verify only** — extend if gaps |

**Pipeline (L3–L4):** Spec reserves TC-xx → **this skill** (Test design) → **`using-git-worktrees`** → Code with **`test-driven-development`** per task.

Do not skip the TC table gate (L3–L4) to write production code first.

## Steps

1. Read Spec / `Then` rows from `l3-01-define.md` (or linked `docs/specs/…`).
2. Read the target module and **existing tests** (naming, mocks, fixtures).
3. Use `get_context` / `search_code` if helpers or dependencies are unclear.
4. For shared symbols, call **`analyze-impact`** to see what else might need test updates.
5. Fill or update the **TC table** in the phase file; write test files: happy, error, one edge per AC.
6. Run the project's test command. **RED gate:** tests must **fail for missing behavior** (not yet implemented). Fix only **test/setup/compile** issues — **do not** add production code in this phase to make tests pass.
7. Log commands and output in **Test design — command log** (see `l3-02` template). Use **`verification-before-completion`** for the run — claim **RED as expected** (e.g. `3 failed — handler not implemented`), **not** “all tests pass” or “done”.

## With test-driven-development

| Phase | This skill | **`test-driven-development`** |
| ----- | ---------- | ----------------------------- |
| **Test design** (L3–L4 before Code) | TC table + acceptance tests in **RED** (fail until Code) | **Do not** run full TDD loop here |
| **Patch / Code** | — | RED→GREEN→REFACTOR per slice; reuse existing failing tests — **do not** rewrite TC table from scratch |

See **`test-driven-development`** § Pipeline and § When NOT (tests already failing).

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
- **TC ID** in phase table ↔ test name or file comment when practical (traceability)

## Do not

- Add tests for config-only or pure refactor changes unless asked
- **Implement production code** in Test design to green the suite (that is **Code** + TDD)
- Introduce a new test framework without user approval
- Renumber TC-xx mid-flight — append TC-04…
