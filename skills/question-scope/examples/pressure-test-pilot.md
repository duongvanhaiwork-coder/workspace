# Pressure tests — pilot in a product repo (question-scope)

This skill does **not** ship automated tests under `skills/`. When your team implements trigger/gate logic in **application code**, or you want **CI guardrails** for agent prompt fixtures, add tests in **that repo** using this spec.

**Contract source:** [SKILL.md](../SKILL.md) · scenarios: [pressure-scenarios.md](../references/pressure-scenarios.md)

## Suggested layout (product repo)

```text
tests/question-scope/
  triggers.test.ts          # or test_question_scope.py — match your stack
  fixtures/
    messages.json           # rows from pressure-scenarios.md
```

## Minimum cases (mirror pressure-scenarios)

| ID | Input (abbrev) | Expect |
| -- | -------------- | ------ |
| 1 | `/question-scope` + task, no L on command | `needsLevelPick: true` |
| 2 | Long sentence, no `/question-scope` | `active: false` |
| 3 | `quick: fix typo` | `active: false` |
| 4 | `/question-scope L2` then escalate signal | `escalate: L3` |
| 5 | `/question-scope L3` + `sp:off` | `active: true`, `supplement: false` |
| 6 | Sticky L2 second turn | `reaskLevel: false` |
| 8 | `/question-scope L2` + `quick:` same message | `active: false` |
| 11 | `?explain` only (removed trigger) | `active: false` — use `/question-scope` |
| 12 | `/question-scope l2` (lowercase) | `level: L2` |

## Parsing rules to assert (from SKILL)

- `/question-scope` token: `(^|\s)/question-scope\b` — **not** required at line start.
- Level on command: `L1`…`L4` case-insensitive (`l2` → `L2`).
- Opt-out `quick:`: starts with `quick:` OR `(^|\s)quick:` (colon required).
- Opt-out `qs:off` / `no-scope`: `(^|\s)(qs:off|no-scope)\b`.
- **`level L2 — …` without `/question-scope`:** must **not** activate scope.
- **`?` + keyword:** must **not** activate scope.

## Pilot checklist (team)

- [ ] Pick one repo (e.g. internal agent wrapper or CLI).
- [ ] Copy fixture messages from [pressure-scenarios.md](../references/pressure-scenarios.md).
- [ ] Implement parser module; wire tests in CI on PR.
- [ ] On SKILL/rule change in AI Core: re-run pilot + update fixtures.
- [ ] Link this file from repo README “Agent prompts” section.

Use skill **`generate-test`** in the pilot repo to match existing test patterns.
