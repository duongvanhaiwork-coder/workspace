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

## P3.2 note (IDE-aligned practices)

- New reference: [ide-aligned-practices.md](./ide-aligned-practices.md) — plan attach = Spec, assessment sub-pipeline, `scope:light`, tiered test gates, Verify evidence in chat, short L2–L3 review, regression from diff.
- Updated: `SKILL.md`, `parsing-tokens.md`, `progressive-context-jit.md`, `session-continuity.md`, `level-picker-runtime.md`, `behavioral-gates.md` (#43–#48), `README.md`, `CHEATSHEET.md`, `rules/cursor/question-scope.mdc`.
- Optional behavioral spot-check: assessment-only turn (#43), plan attach (#44), verify evidence (#45).

## P3.3 note (child skills + quickref)

- [pipelines-quickref.md](./pipelines-quickref.md) — IDE-aligned table, L3 Assessment chain, `scope:light` L2.
- [pipelines-skill-map.md](./pipelines-skill-map.md) — §2–§3 rows annotated for ide-aligned.
- [ide-aligned-practices.md](./ide-aligned-practices.md) §11 — child skill matrix.
- Workspace `skills/` updated: `verification-before-completion`, `generate-test`, `architect-plan`, `writing-plans`, `executing-plans`, `caveman-review`, `brainstorming`, `using-git-worktrees`, `superpowers`, [COMPOSITION.md](../../COMPOSITION.md) § Task kind.
- Sync rule + `question-scope` skill to IDE after pull; reload Cursor.

## P3.4 note (IDE-ALIGNED reference IDs)

- Child skills cite **`IDE-ALIGNED §N`** instead of `../question-scope/references/…` paths — [CONVENTIONS.md](../../CONVENTIONS.md) § Cross-referencing question-scope.
- Lookup table at top of [ide-aligned-practices.md](./ide-aligned-practices.md).

## P3.5 note (clarifying options §12)

- New: [clarifying-options.md](./clarifying-options.md) — **scope active only**; 2–4 options + **`Other — I'll specify`**; STOP before Patch/Code.
- [ide-aligned-practices.md](./ide-aligned-practices.md) §12; [CONVENTIONS.md](../../CONVENTIONS.md) § table; [SKILL.md](../SKILL.md) gates + IDE-aligned summary.
- [level-picker-runtime.md](./level-picker-runtime.md), [gray-zones.md](./gray-zones.md), [CHEATSHEET.md](./CHEATSHEET.md), phase templates § Decisions.
- Optional behavioral: gate **#49** in [behavioral-gates.md](./behavioral-gates.md).
- Edit **rule + skill** together when changing §12 STOP semantics.

## P3.6 note (clarify:off + pressure pilot)

- Token **`clarify:off`**: scope on; skip §12 — [parsing-tokens.md](./parsing-tokens.md), [SKILL.md](../SKILL.md) tokens table, [clarifying-options.md](./clarifying-options.md).
- Pressure parsing **#25–#26**; behavioral **#49**, **#49b**; [SIMULATION-RUN.md](./SIMULATION-RUN.md) Part 1 rows + Part 3 §49/§49b.
- Spot-check when §12 changes: **#49**, **#49b** ([behavioral-gates.md](./behavioral-gates.md)).
