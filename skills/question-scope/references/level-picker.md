# Level picker (question-scope)

Use when **suggesting** level or presenting options (heuristic only — user chooses unless `/question-scope Lx` preset).

## Trigger flow

```mermaid
flowchart TD
  A[User message] --> B{qs:off / no-scope / quick: / qs:meta / audit:?}
  B -->|yes| Z[Normal chat + code-standards rule]
  B -->|no| C{Meta keywords or discuss /question-scope without run intent?}
  C -->|yes| Z
  C -->|no| D{/question-scope + whitespace + L1-L4?}
  D -->|yes| RUN[Run pipeline preset Lx]
  D -->|no| E{/question-scope at start or end?}
  E -->|no| Z
  E -->|yes| G{/question-scopeL1-L4 glued no space?}
  G -->|yes| WARN[4 options STOP + tell user add space before L]
  G -->|no| F[Idea + Suggest Lx]
  F --> H{Only one gray pair fits?}
  H -->|no| I[4 options L1-L4 STOP]
  H -->|L1 vs L2| T[Exactly 2 options STOP]
  H -->|L2 vs L3| T
  H -->|L3 vs L4| T
  T --> J[User picks]
  I --> J
  J --> RUN
  WARN --> J
```

Details: [gray-zones.md](./gray-zones.md) · triggers: [SKILL.md](../SKILL.md#when-this-skill-applies)

## Host UI (Cursor vs Kiro)

Same skill contract ([SKILL.md](../SKILL.md)); host differs for **level pick** and **tool names**.

| Topic | Cursor | Kiro |
| ----- | ------ | ---- |
| **Level pick (no L on `/question-scope`)** | `AskQuestion` with 4 options (or 2 in gray zone) | Numbered list; user replies `L2`, `choose L3`, `/question-scope L3`, … |
| **Gray zone** | `AskQuestion` with exactly 2 options; **STOP** until pick | Same two options as numbered list |
| **After pick** | Header `Level: Lx \| Pipeline: …` | Same |
| **Rules (IDE)** | Always-on: `question-scope`, `code-standards`. On demand: `@workflow` | Same rule IDs (host loads steering by ID) |
| **Skills** | `question-scope` skill ID | Same skill ID (`invoke-skill`) |

**Agent:** Do not re-ask level every turn (**sticky scope**) for the same work item. **New unrelated task** → user sends `/question-scope` or `/question-scope Ly` again. On Kiro without `AskQuestion`, never skip the STOP after presenting options.
