# Rules recovery notes (2026-05-22)

After `rules/` was emptied, content was partially recreated from agent transcripts. This file records what was missing, what was restored, and what was intentionally **not** re-added.

## Restored (2026-05-22)

| File | Issue | Action |
| ---- | ----- | ------ |
| `cursor/typescript.mdc` | ~15-line stub | Full NestJS/TypeORM rule (~72 lines) from `_recover_from_transcript/` |
| `cursor/react.mdc` | stub | Full Redux/saga + layout rule (~64 lines) |
| `cursor/python.mdc` | stub | Full FastAPI rule (~50 lines) |
| `cursor/dotnet.mdc` | stub | Full .NET/EF rule (~63 lines) |
| `cursor/java.mdc` | stub | Full Spring Boot rule (~81 lines) |

Regenerate `rules/kiro/` from `rules/cursor/` when cursor rules change (generated 1:1 stem).

**Naming (2026-05):** Kiro steering files use the **same stem** as Cursor (`code-standards.md`, not `rules-code-standards.md`). Legacy `rules-*.md` prefixes are obsolete.

## Already complete (no change needed)

- `code-standards.mdc` (formerly `general.mdc`), `question-scope.mdc`, `workflow.mdc` — match transcript recovery
- `README.md`, `CONVENTIONS.md`, `QUICKSTART.md` — current tree is canonical

## Not restored (by design)

| Artifact | Reason |
| -------- | ------ |
| `cursor/stack.mdc` | Superseded by per-language `*.mdc` files (same content split; avoids duplicate globs) |
| `cursor/question-scope-flow.mdc` | Renamed to `question-scope.mdc`; skill is `skills/question-scope/` (old `question-scope-flow` path is obsolete) |
| `cursor/superpowers-workflow.mdc` | Merged into `workflow.mdc` |

## Archive

Transcript snapshot `rules/_recover_from_transcript/` was removed after merge into `rules/cursor/` (2026-05-22).

## Prevent repeat loss

Commit `rules/` and `skills/` to your repo (`.gitignore` no longer ignores them). Use your normal git workflow.
