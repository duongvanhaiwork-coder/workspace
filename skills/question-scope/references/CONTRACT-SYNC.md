# question-scope contract sync (`qs-2026-05-29.3`)

When changing triggers, tokens, STOP gates, or precedence, update **both** in one change set:

| Artifact | Path |
| -------- | ---- |
| Always-on rule (short mirror) | `rules/cursor/question-scope.mdc` |
| Canonical skill | `skills/question-scope/SKILL.md` |
| Parsing / meta / tokens (detail) | `references/parsing-tokens.md` |
| Kiro generated | `rules/kiro/question-scope.md` — run `make sync-ide` |

## Bump checklist

1. Choose new tag `qs-YYYY-MM-DD.N` (patch `.N` for same-day edits).
2. Set **Contract** / **Contract version** in rule + skill (search `qs-2026` in repo).
3. Update `references/pipelines-skill-map.md` contract line.
4. Run from workspace root: `make sync-ide` then reload Cursor window or new chat.
5. Optional: `./scripts/check-question-scope-session.sh` (compares installed rule vs repo).
6. If Parsing/Meta/tokens change: spot-check `references/behavioral-gates.md` / pressure scenarios.

## P3 note (2026-05-29.2)

- Long skill sections moved to `references/` (parsing, session, JIT, level-picker runtime).
- Rule body unchanged in semantics — still short mirror; skill holds canonical tables.

## P3.1 note (2026-05-29.3)

- **Level picker:** `/question-scope` without `Lx` → **2** labeled options when only one gray pair fits (e.g. L2 vs L3 export), else **4** — aligns SKILL, rule, `level-picker-runtime.md`, pressure #1/#7/#11c.
- **Glued `L`:** explicit row in SKILL § Triggers (hint once, no preset).
- **Doc sync (same day):** [level-picker.md](./level-picker.md) mermaid glued branch; fixture #14 expect; reference tag headers `.3`.
