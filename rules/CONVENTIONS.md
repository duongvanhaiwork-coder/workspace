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

## Runnable commands

Do **not** document `make …`, `./scripts/…`, or other workspace shell entrypoints in `.mdc` bodies, `rules/*.md`, or `skills/`. Operators use repo [README.md](../README.md) § *Lệnh chạy*.

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
| `mcp-code-intelligence.mdc` | `true` | MCP up → use `get_context` / `search_code` / `analyze_impact`; MCP down → editor fallback |
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
| Always-on guardrails (`code-standards`, `mcp-code-intelligence`, `question-scope`) | Playbooks (`skills/<id>/SKILL.md`) |
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
5. Edit **rule + skill** in the same change set when triggers, gates, or default/precedence semantics change (`question-scope` — see skill `CONTRACT-SYNC.md`).

**Do not:** paste full L3/L4 pipelines into `.mdc`; set `workflow.mdc` to `alwaysApply: true` without team agreement; add Vietnamese prose in rule bodies (see **Language** above).

### Goal → polarity (how agents weight instructions)

Models tend to treat **negatives** as hard constraints and **positives** as planning context. Match polarity to the goal:

| Goal | Prefer | Example phrasing |
| ---- | ------ | ---------------- |
| Block dangerous behavior | **Negative** | `NEVER log tokens`; `Do not commit unless the user asked` |
| Steer workflow / multi-step work | **Positive** | `When scope is on → follow supplement table`; `NEXT → verify-before-done` |
| Coding style / conventions | **Positive** | `Match existing layout`; `Prefer early returns` |
| Security / auth boundary | **Negative** | `Parameterized queries only`; `deny by default` |
| Scope control (task size) | **Mixed** | Negative: `Do not expand beyond the request`; positive: `Prefer the smallest correct change` |

### Two-line templates

```text
Negative:  NEVER <forbidden action> (no exceptions on <path>).
Positive:  When <trigger> → <required action> (see skill `<skill-id>`).
Mixed:     Do not <creep>. Prefer <minimal correct approach> in touched files.
```

### Anti-patterns

- **Too many negatives** in one always-on rule → agent freezes or over-asks; cap at ~five scoped negatives per rule (see checklist).
- **Positive disguised as negative** → `avoid X unless necessary` still allows X; use `Do not X` for boundaries.
- **Vague positive for boundaries** → `be careful with secrets` → use `Never log tokens, passwords, or API keys`.
- **Full pipelines in `.mdc`** → put steps in skills; rules only gate and point.

### Where polarity lives today

| File | Role | Polarity mix |
| ---- | ---- | ------------- |
| `question-scope.mdc` | Triggers, STOP, opt-outs | Mixed (trigger table + negatives) |
| `mcp-code-intelligence.mdc` | MCP vs editor discovery | Positive (when→then) + negative (gates) + mixed (scope) |
| `code-standards.mdc` | Style, security, change scope, git gates | Positive (Clean Code) + negative (Security, Change scope, Commits) |
| `workflow.mdc` | Handoffs, flows | Positive (flows) + **Hard gates** (negatives) |
| Stack `*.mdc` | Framework patterns | Mostly positive; security lines negative |

Localized human guide (optional): [../docs/WORKFLOW-QUICKSTART.md](../docs/WORKFLOW-QUICKSTART.md). Skill authors: [../skills/CONVENTIONS.md](../skills/CONVENTIONS.md) § Rules vs skills.

## Editing checklist

- [ ] Change only `rules/cursor/*.mdc`
- [ ] Body and `description` in English
- [ ] Valid frontmatter (`description`, `alwaysApply`, `globs` if needed)
- [ ] Do not hand-edit `rules/kiro/`
- [ ] After bulk restore: see [RECOVERY.md](./RECOVERY.md); remove stale archives under `rules/`
