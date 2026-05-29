# question-scope contract sync

When changing triggers, tokens, STOP gates, or precedence, update **both** in one change set:

| Artifact | Path |
| -------- | ---- |
| Always-on rule (short mirror) | `rules/cursor/question-scope.mdc` |
| Canonical skill | `skills/question-scope/SKILL.md` |
| Parsing / meta / tokens (detail) | `references/parsing-tokens.md` |
| Kiro generated | `rules/kiro/question-scope.md` — regenerated on IDE sync ([README.md](../../../README.md)) |

## Change checklist

1. Edit **rule + skill** together (same PR / commit).
2. Update related `references/` when Parsing, Meta, level picker, or pipelines change.
3. Repo verification in the AI Core repo ([README.md](../../../README.md)); if rules changed, IDE sync + reload window or new chat.
4. Optional session check (AI Core repo only): [README.md](../../../README.md) § Script tùy chọn.
6. If Parsing/Meta/tokens change: spot-check `references/behavioral-gates.md` / pressure scenarios.

## P3 note (2026-05-29.2)

- Long skill sections moved to `references/` (parsing, session, JIT, level-picker runtime).
- Rule body unchanged in semantics — still short mirror; skill holds canonical tables.

## P3.1 note (2026-05-29.3)

- **Level picker:** `/question-scope` without `Lx` → **2** labeled options when only one gray pair fits (e.g. L2 vs L3 export), else **4** — aligns SKILL, rule, `level-picker-runtime.md`, pressure #1/#7/#11c.
- **Glued `L`:** explicit row in SKILL § Triggers (hint once, no preset).
- **Doc sync:** [level-picker.md](./level-picker.md) mermaid glued branch; fixture #14 expect.
