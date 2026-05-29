# question-scope contract sync

When changing triggers, tokens, STOP gates, or precedence, update **both** in one change set:

| Artifact | Path |
| -------- | ---- |
| Always-on rule (short mirror) | `rules/cursor/question-scope.mdc` |
| Canonical skill | `skills/question-scope/SKILL.md` |
| Parsing / meta / tokens (detail) | `references/parsing-tokens.md` |
| Kiro generated | `rules/kiro/<stem>.md` — run `./scripts/sync-ide-rules.sh` from AI Core repo ([README.md](../../../README.md)) |

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
- Sync rule + `question-scope` skill to IDE after pull; reload IDE window / new chat (any host).

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

## P3.7 note (test visibility L2–L4)

- **Level picker / gray zone:** L2 (+ TC in Spec); L3 explicit **Test** (`generate-test`, `l3-02`); L4 step 8 **Test Design** — [level-picker.md](./level-picker.md), [gray-zones.md](./gray-zones.md).
- **Output header:** [SKILL.md](../SKILL.md) § Output header — L3 implement must list **Test** before **Code**; L3 assessment-only header unchanged.
- **Phase:** [l3-01-define.md](../templates/phases/l3/l3-01-define.md) — next phase Test before Code.
- **CHEATSHEET**, [pipelines-quickref.md](./pipelines-quickref.md), [README.md](../README.md) signal table, [SIMULATION-RUN.md](./SIMULATION-RUN.md) §6b; fixtures **#6b**, **#26** expect L3 header with **Test** before **Code**.
- **Rule mirror:** `rules/cursor/question-scope.mdc` § After level is chosen — one-line header hints (L2 TC, L3 Test, L4 Test Design); reload IDE after sync.

## P3.8 note (confirmation prompts — rich options)

- New: [confirmation-prompts.md](./confirmation-prompts.md) — structured **Idea**, **Suggest**, task **`For this task:`** on level labels, gray-zone comparison table, §12 **Decision + Why it matters** + consequence labels.
- Wired: [SKILL.md](../SKILL.md) § Scope Level, [level-picker-runtime.md](./level-picker-runtime.md), [level-picker.md](./level-picker.md), [clarifying-options.md](./clarifying-options.md), [gray-zones.md](./gray-zones.md), [README.md](../README.md) § No L on command, [CHEATSHEET.md](./CHEATSHEET.md).
- Behavioral: fixtures **#1**, **#49** — richer expects; [SIMULATION-RUN.md](./SIMULATION-RUN.md) §1 / §49 examples updated.
- Rule mirror unchanged (detail in skill); spot-check new chat after sync.

## P3.9 note (all AI IDEs — host UI)

- New: [host-ui.md](./host-ui.md) — universal minimum + structured picker vs chat fallback; not Cursor-only.
- Renamed: gray-zones **Gray-zone level pick (all AI IDEs)** (was Cursor/Kiro AskQuestion).
- Updated: [confirmation-prompts.md](./confirmation-prompts.md), [level-picker.md](./level-picker.md), [level-picker-runtime.md](./level-picker-runtime.md), [clarifying-options.md](./clarifying-options.md), [ide-aligned-practices.md](./ide-aligned-practices.md) §12, [SKILL.md](../SKILL.md) intro, [README.md](../README.md), `rules/cursor/question-scope.mdc` (description + fallback line).
- Behavioral **#49b**: no longer requires “AskQuestion” by name.

## P3.10 note (option viability without brainstorming)

- [confirmation-prompts.md](./confirmation-prompts.md) § **Grounding & viability** — §12 options from **Fits repo** *or* **New here** (idea-driven); JIT optional; escalate when many directions open.
- [clarifying-options.md](./clarifying-options.md), [ide-aligned-practices.md](./ide-aligned-practices.md) §11 child row for `brainstorming` vs §12.

## P3.11 note (dedup §12 + README flow)

- [confirmation-prompts.md](./confirmation-prompts.md): §12 count **2–4** unified; § **After brainstorming — do not duplicate §12**.
- [clarifying-options.md](./clarifying-options.md), [skills/brainstorming/SKILL.md](../../brainstorming/SKILL.md) cross-link.
- [README.md](../README.md): § **Flow overview** + § **Trồng chéo — đọc file nào**.

## Rules sync (cursor ↔ kiro)

After editing **`rules/cursor/*.mdc`**, from workspace root:

```bash
./scripts/sync-ide-rules.sh
```

Regenerates **`rules/kiro/<stem>.md`** (1:1) and symlinks `~/.cursor/rules`, `~/.kiro/steering`. **Do not** hand-edit `rules/kiro/*.md`.
