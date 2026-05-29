# Rules (canonical)

**Language:** All rule bodies and frontmatter in `rules/cursor/` are **English**. Localized human guides live under `docs/` or `skills/*/README.md` — not inside `.mdc` files.

**Source of truth:** `cursor/*.mdc` only.

**Generated output:** `kiro/<stem>.md` is produced from `cursor/<stem>.mdc` (1:1 stem). **Do not edit `kiro/` by hand.** Index: [cursor/README.md](./cursor/README.md), [kiro/README.md](./kiro/README.md).

## Quick links

| Doc | Audience |
| --- | -------- |
| [CONVENTIONS.md](./CONVENTIONS.md) | Frontmatter, language policy, **Rule authoring** (polarity), edit checklist |
| [QUICKSTART.md](./QUICKSTART.md) | English workflow + prompt cheat sheet |
| [RECOVERY.md](./RECOVERY.md) | Post-restore notes (what was merged / not restored) |
| [cursor/workflow.mdc](./cursor/workflow.mdc) | Superpowers rule IDs (on demand) |
| [../skills/question-scope/README.md](../skills/question-scope/README.md) | Extended prompt examples (VI) |

Legacy Vietnamese workflow guide (optional): [../docs/WORKFLOW-QUICKSTART.md](../docs/WORKFLOW-QUICKSTART.md) — prefer [QUICKSTART.md](./QUICKSTART.md) for English.

## Frontmatter convention (Cursor)

Every `rules/cursor/*.mdc` file starts with YAML frontmatter:

| Field | Required | Values |
| ----- | -------- | ------ |
| `description` | yes | One line (or folded `>`) — **English**; shown in Cursor rule picker |
| `alwaysApply` | yes | `true` = every session; `false` = file-scoped or on demand |
| `globs` | when `alwaysApply: false` and file-scoped | Comma-separated patterns, e.g. `"**/*.ts"` or `"**/*.tsx, **/*.jsx"` |

Do **not** use non-standard keys (`glob`, `priority`, …). Do not set `globs` when `alwaysApply: true`.

| Intent | Cursor frontmatter | Kiro `inclusion` |
| ------ | ------------------ | ---------------- |
| Always on | `alwaysApply: true` | `always` |
| By file type | `alwaysApply: false` + `globs: "..."` | `fileMatch` + `fileMatchPattern` |
| On demand (skills/workflows) | `alwaysApply: false` (no `globs`) | `manual` |

Details: [CONVENTIONS.md](./CONVENTIONS.md).

## `cursor/` files

| File | `alwaysApply` | `globs` | Contents |
| ---- | ------------- | ------- | -------- |
| `code-standards.mdc` | `true` | — | Shared defaults (all files) |
| `question-scope.mdc` | `true` | — | Question Scope triggers → skill **`question-scope`** |
| `typescript.mdc` | `false` | `**/*.ts` | Backend / shared TS |
| `react.mdc` | `false` | `**/*.tsx`, `**/*.jsx`, `**/app/**/*.js` | React UI |
| `python.mdc` | `false` | `**/*.py` | Python services/workers |
| `dotnet.mdc` | `false` | `**/*.cs` | .NET / C# |
| `java.mdc` | `false` | `**/*.java` | Java backend |
| `workflow.mdc` | `false` | — | Workflow rule IDs & handoffs (on demand; Kiro: load `workflow.md` steering) |

## Supported stacks & gaps

Stack rules **detect** what the repo uses — they do not mandate a framework. Current file-scoped coverage:

| Stack rule | Primary patterns | Not covered (add a rule if the team needs it) |
| ---------- | ---------------- | --------------------------------------------- |
| `typescript.mdc` | NestJS, TypeORM, Node backend TS | Go, Rust, Kotlin, Vue/Svelte |
| `react.mdc` | Redux Saga, legacy `app/containers/` | Next.js App Router-only repos without saga |
| `python.mdc` | FastAPI, async workers | Django-only layouts |
| `dotnet.mdc` | Layered .NET, EF Core | — |
| `java.mdc` | Spring Boot, JPA | — |

No rule yet for shell (`scripts/**/*.sh`), SQL migrations, or Terraform — follow `code-standards.mdc` and repo conventions.

## Sync to IDE

After editing `rules/cursor/*.mdc`, run from the workspace root:

```bash
make sync-ide
```

Then **reload the Cursor window** or start a **new chat** — always-on rules are cached in open sessions.

## Layout

```text
rules/
  cursor/*.mdc          ← edit (canonical)
  kiro/<stem>.md        ← generated (1:1 stem)
  README.md
  CONVENTIONS.md
  QUICKSTART.md
  RECOVERY.md
```

| Directory | IDE | Format |
| --------- | --- | ------ |
| `cursor/` | Cursor | `*.mdc` — **edit here** |
| `kiro/` | Kiro | `<stem>.md` — **generated** (same stem as cursor) |
