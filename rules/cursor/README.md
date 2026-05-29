# Cursor rules (canonical)

Edit **`*.mdc` here only.** Kiro copies are generated under `../kiro/<same-stem>.md` on IDE sync — [README.md](../../README.md).

| File | `alwaysApply` | `globs` | Kiro output |
| ---- | ------------- | ------- | ----------- |
| `code-standards.mdc` | `true` | `—` | `code-standards.md` |
| `dotnet.mdc` | `false` | `"**/*.cs"` | `dotnet.md` |
| `java.mdc` | `false` | `"**/*.java"` | `java.md` |
| `mcp-code-intelligence.mdc` | `true` | `—` | `mcp-code-intelligence.md` |
| `python.mdc` | `false` | `"**/*.py"` | `python.md` |
| `question-scope.mdc` | `true` | `—` | `question-scope.md` |
| `react.mdc` | `false` | `"**/*.tsx, **/*.jsx, **/app/**/*.js"` | `react.md` |
| `typescript.mdc` | `false` | `"**/*.ts"` | `typescript.md` |
| `workflow.mdc` | `false` | `—` | `workflow.md` |

Naming: **kebab-case** stem; same basename in `rules/kiro/` (`.md`). See [../CONVENTIONS.md](../CONVENTIONS.md).
