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

Do not use a `rules-` prefix in `rules/kiro/` (legacy). After sync, counts must match: one `.mdc` per steering `.md`.

## Source of truth

```text
rules/cursor/<name>.mdc     ← edit here
        ↓ sync-ide-rules.sh
rules/kiro/<name>.md        ← generated (same stem; in repo)
        ↓ directory symlinks (home only)
~/.cursor/rules/            → rules/cursor/   (whole folder)
~/.kiro/steering/           → rules/kiro/     (whole folder)
~/.cursor/skills/           → skills/         (whole folder)
~/.kiro/skills/             → skills/         (whole folder)
```

`make sync-ide` does **not** create symlinks under `Workspace/.cursor/` or `Workspace/.kiro/`.

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

**Precedence:** explicit user message → repo `AGENTS.md` → question-scope STOP gates → `code-standards.mdc` / stack rules → skill playbooks.

## Editing checklist

- [ ] Change only `rules/cursor/*.mdc`
- [ ] Body and `description` in English
- [ ] Valid frontmatter (`description`, `alwaysApply`, `globs` if needed)
- [ ] Run `make sync-ide` or `./scripts/sync-ide-rules.sh`
- [ ] Do not hand-edit `rules/kiro/`
- [ ] After bulk restore: see [RECOVERY.md](./RECOVERY.md); remove stale archives under `rules/`
