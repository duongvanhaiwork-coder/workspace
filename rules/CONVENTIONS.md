# Rules conventions

Canonical Cursor rules live under **`rules/cursor/*.mdc`**. Kiro steering files in **`rules/kiro/`** are **generated** — do not edit by hand.

## Language

| Location | Language |
| -------- | -------- |
| `rules/cursor/*.mdc` | **English only** (body, headings, tables, `description` frontmatter) |
| `rules/kiro/*.md` (except `README.md`) | English (generated from Cursor; 1:1 stem) |
| `rules/README.md`, `rules/CONVENTIONS.md`, `rules/QUICKSTART.md` | English |
| `docs/WORKFLOW-QUICKSTART.md` | Optional Vietnamese for humans; **agent rules** stay in `rules/` |
| `skills/question-scope/README.md` | Vietnamese exception; all other `skills/**` docs English |

Do not add Vietnamese (or other) prose inside `.mdc` rule bodies. Put localized cheat sheets in `docs/` or `skills/<id>/README.md`.

## File naming

| Layer | Pattern | Example |
| ----- | ------- | ------- |
| Cursor (canonical) | `<stem>.mdc` kebab-case | `code-standards.mdc`, `question-scope.mdc` |
| Kiro (generated) | `<stem>.md` — **same stem** | `code-standards.md`, `question-scope.md` |

Do not use a `rules-` prefix in `rules/kiro/` (legacy). Counts must match: one `.mdc` per steering `.md`.

## Source of truth

```text
rules/cursor/<name>.mdc     ← edit here
rules/kiro/<name>.md        ← generated (same stem)
```

## Frontmatter (Cursor)

Every `rules/cursor/*.mdc` file **must** start with YAML frontmatter:

| Field | Required | Values |
| ----- | -------- | ------ |
| `description` | yes | One line (or folded `>`) — English; shown in Cursor rule picker |
| `alwaysApply` | yes | `true` = every session; `false` = file-scoped or on demand |
| `globs` | when `alwaysApply: false` and file-scoped | Comma-separated patterns, e.g. `"**/*.ts"` |

**Do not** use non-standard keys (`glob`, `priority`, …). **Do not** set `globs` when `alwaysApply: true`.

| Intent | Cursor | Kiro (`inclusion`) |
| ------ | ------ | ------------------ |
| Always on | `alwaysApply: true` | `always` |
| By file type | `alwaysApply: false` + `globs` | `fileMatch` + `fileMatchPattern` |
| On demand | `alwaysApply: false` (no `globs`) | `manual` |

## Rule files

| File | `alwaysApply` | Scope |
| ---- | ------------- | ----- |
| `code-standards.mdc` | `true` | All projects — clean code, security, testing, APIs |
| `question-scope.mdc` | `true` | L1–L4 triggers → skill **`question-scope`** |
| `typescript.mdc` | `false` | `**/*.ts` |
| `react.mdc` | `false` | `**/*.tsx`, `**/*.jsx` |
| `python.mdc` | `false` | `**/*.py` |
| `dotnet.mdc` | `false` | `**/*.cs` |
| `java.mdc` | `false` | `**/*.java` |
| `workflow.mdc` | `false` | Superpowers rule IDs & handoffs (load `@workflow` or skill supplement table) |

Stack rules **detect** frameworks from the repo — they do not mandate NestJS, Spring, etc.

## Relationship to skills

| Rules | Skills |
| ----- | ------ |
| Always-on guardrails (`code-standards`, `question-scope`) | Playbooks (`skills/<id>/SKILL.md`) |
| On-demand workflow graph (`workflow.mdc`) | Superpowers + team skills |
| File-type conventions (`typescript`, `react`, …) | Stack helpers (`generate-test`, …) |

**Precedence:** explicit user message → repo `AGENTS.md` → question-scope STOP gates → `code-standards.mdc` / stack rules → `@workflow` (when loaded) → skill playbooks.

## Rule authoring (positive + negative)

Always-on rules stay **short**. Full pipelines live in **skills** (`skills/<id>/SKILL.md`).

| Layer | Put in `.mdc` rule | Put in skill (not rule) |
| ----- | ------------------- | ------------------------ |
| **Positive** | WHEN → THEN (trigger table, required header, `docs/work/…` when scope on) | Step playbooks, TC tables, phase templates |
| **Negative** | False triggers, opt-outs, STOP, “do not infer L from task size”, precedence | Pressure scenarios, parsing edge cases, behavioral fixtures |

**Checklist for a new or edited always-on rule:**

1. One **trigger / action** table (positive).
2. Up to **five** scoped negatives (legacy signals, meta, token conflicts, default path when no trigger).
3. **Precedence** line if the rule can conflict with `code-standards`, scope STOP, or `@workflow`.
4. **Pointer** to the skill ID — do not duplicate multi-step pipelines in the rule body.
5. Bump **contract version** in rule + skill when triggers, gates, or default/precedence semantics change (`question-scope`).

**Do not:** paste full L3/L4 pipelines into `.mdc`; set `workflow.mdc` to `alwaysApply: true` without team agreement; add Vietnamese prose in rule bodies (see **Language** above).

## Editing checklist

- [ ] Change only `rules/cursor/*.mdc`
- [ ] Body and `description` in English
- [ ] Valid frontmatter (`description`, `alwaysApply`, `globs` if needed)
- [ ] Do not hand-edit `rules/kiro/`
- [ ] After bulk restore: see [RECOVERY.md](./RECOVERY.md); remove stale archives under `rules/`
