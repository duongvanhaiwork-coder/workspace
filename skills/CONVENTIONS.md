# Skills conventions (portable)

Canonical rules for **all** skills under `skills/<skill-id>/` in this repo (Superpowers bundle + team catalog). Not Claude Code plugin IDs; not host-specific paths unless noted as examples.

**Directory layout (prompts / references / templates):** [STRUCTURE.md](./STRUCTURE.md).

## Language

| Location | Language |
| -------- | -------- |
| `skills/**/SKILL.md` | **English only** (body, headings, YAML `description`) |
| `skills/**/README.md` | **English** (default) |
| `prompts/`, `references/`, `templates/`, `examples/` under skills | **English** |
| Optional localized human workflow outside `skills/` | e.g. `docs/WORKFLOW-QUICKSTART.md`, `AGENTS.md`, rule `@workflow` (on demand) |

All prose under `skills/` is **English** for agents and humans. User messages in chat may be any language; skill contracts and skill docs stay English.

## Invocation modes (standalone, coordinated, composition)

Every skill under `skills/<skill-id>/` is:

1. **Standalone** — invokable when its `SKILL.md` matches, **without** `/question-scope`
2. **Coordinated** — same skill at the mapped phase when `/question-scope Lx` is active
3. **Composable** — may run **together with other skills** in one session when each skill’s **When to use** matches

**Mandatory combinations only:** [COMPOSITION.md](./COMPOSITION.md) § Requires (hard). Do **not** require the whole pipeline for a small task.

| Mode | Trigger | Agent behavior |
| ---- | ------- | -------------- |
| **Standalone** | Task matches this skill; no scope (or `qs:off`, `quick:`, …) | Follow **this** skill’s playbook. **`superpowers`** (`skill-check-first`) may add other skills — each must match its own **When to use**. |
| **Coordinated** | `/question-scope` or `/question-scope Lx` | Scope **L**, gates, and `docs/work/…` first; invoke this skill at the mapped phase ([pipelines-quickref](./question-scope/references/pipelines-quickref.md)). |
| **Composition** | Multiple skills fit (e.g. debug + TDD + verify) | Invoke in sensible order; respect **Requires (hard)** in [COMPOSITION.md](./COMPOSITION.md) and each skill’s § **Invocation modes**. |
| **User override** | Explicit instruction | User message wins for that turn. |

**Each `SKILL.md`** must include § **Invocation modes** (standalone, coordinated, optional **Combines with**, **Requires (hard)** if any).

**YAML `description`:** Prefer “Also on user request” / composable wording — not “only under question-scope Lx” unless **Requires (hard)** applies.

## Referencing Cursor rules (from skills)

Do **not** embed `rules/…` or `../rules/…` file paths in `SKILL.md`, `references/`, `templates/`, or `examples/`. Rules are loaded by the IDE; skills cite **rule IDs** or **@mentions**:

| Need | Cite |
| ---- | ---- |
| L1–L4 scope, opt-outs, phased `docs/work/` | Rule **`question-scope`** (always on) + this skill’s `SKILL.md` |
| Workflow handoffs, Superpowers rule IDs | **`@workflow`** (on demand) or rule ID (`design-approval-gate`, …) |
| Code style, security, APIs | Rule **`code-standards`** (always on) + stack rules by file type (`typescript`, `react`, …) |
| Human English quickstart | `AGENTS.md` — not duplicated inside skills |

Phase → rule ID map: **`question-scope`** → `references/superpowers-supplement.md`.

## Rules vs skills (where content lives)

| Layer | Edit | Holds |
| ----- | ---- | ----- |
| **Rules** | `rules/cursor/*.mdc` only — sync via repo [README.md](../README.md) | Triggers, STOP, hard gates, short WHEN→THEN tables |
| **Skills** | `skills/<skill-id>/SKILL.md` | Multi-step playbooks, TC tables, pressure scenarios |

**Runnable commands:** Do **not** put `make …`, `./scripts/…`, or workspace shell entrypoints in `skills/` or `rules/`. Canonical list: repo [README.md](../README.md) § *Lệnh chạy*. Skills/rules may say “run repo verification” or link README — not copy commands.

**Polarity (negative vs positive phrasing):** [rules/CONVENTIONS.md](../rules/CONVENTIONS.md) § **Rule authoring** — goal→polarity table, templates, anti-patterns. When trimming a skill, move gates into rules; keep steps in skills.

## Skill authoring (positive + negative)

Skills are **playbooks** (multi-step, judgment). Rules are **gates** (short, always-on). Do not paste rule trigger tables into `SKILL.md`.

| Goal | Prefer in skill | Example |
| ---- | ---------------- | ------- |
| Block wrong phase (no code before spec) | **Negative** | `Do not implement until user approves design` |
| Step-by-step workflow | **Positive** | `1. Run repro test 2. …` |
| Discipline (TDD, verify, debug) | **Negative** gates + **positive** cycle | Iron Law + RED→GREEN→REFACTOR |
| Scope / handoff | **Mixed** | `Do not skip Regression` + `NEXT: verification-before-completion` |
| Security / git / secrets | **One line + rule ID** | Follow **`code-standards`** — do not restate full Security section |

**Checklist for a new or edited skill:**

1. YAML `description`: **Use when…** (symptoms only — not workflow summary; see `writing-skills`).
2. § **Invocation modes**: standalone, coordinated, Combines, Requires (hard).
3. § **Composition (quick ref)**: 3–6 rows + link [references/invocation-anti-patterns.md](./references/invocation-anti-patterns.md).
4. **Announce** line when the skill is non-obvious (`Using <skill-id> to …`).
5. **Stop when** / **NEXT** for handoff-heavy skills.
6. Heavy tables, pressure scenarios, CSO → `references/` not inline bloat.

**Audit:** [references/SKILLS-AUDIT.md](./references/SKILLS-AUDIT.md).

## Referencing other skills

Portable cross-skill rules for `SKILL.md`, `references/`, `templates/`, and `examples/`:

| Need | Cite |
| ---- | ---- |
| Run / hand off another skill | `` `skill-id` `` + `**REQUIRES:**` / `**NEXT:**` / `**ALT:**` (invoke via `invoke-skill`; do not link to `SKILL.md`) |
| File in **this** skill | `references/foo.md`, `prompts/bar.md`, `templates/...` (relative to skill root) |
| File in **another** skill (deep link) | `` `other-skill` `` + path under that skill, e.g. `` `question-scope` `` → `references/superpowers-supplement.md`; optional markdown `../other-skill/references/foo.md` from a sibling `SKILL.md` |
| Prompt/template owned by another skill | `` `requesting-code-review` `` → `prompts/code-reviewer.md` (skill ID + path; no `skills/` prefix) |

**Do not** in skill bodies: host absolute paths (`/Users/...`, `~/.cursor/...`, `~/.kiro/...`), repo-root `skills/<id>/SKILL.md`, `@skills/.../SKILL.md`, or `superpowers:<id>`.

**Catalog meta** (`skills/README.md`, `SKILLS-REGISTRY.md`, `STRUCTURE.md`): may use `question-scope/references/...` paths relative to the `skills/` directory for human navigation.

## Skill directory layout

Every skill uses the same folder pattern:

```text
skills/<skill-id>/
  SKILL.md          # required — agent playbook
  README.md         # optional — human usage (e.g. question-scope, caveman-*)
  prompts/          # optional — subagent / reviewer templates (*.md)
  references/       # optional — deep-dive docs (*.md)
  templates/        # optional — copy-out artifacts (e.g. question-scope/templates/phases/)
  examples/         # optional
  scripts/          # optional — non-markdown helpers
```

**Do not** place supporting `*.md` at the skill root (except `SKILL.md` and optional `README.md`). New skills: create subfolders when adding the first supporting file.

## Skill identity

| Concept | Use in skills |
| -------- | ------------- |
| **Skill ID** | Directory name: `writing-plans`, `test-driven-development` |
| **Invoke** | Load skill by ID via your platform’s skill mechanism (see `superpowers`) |
| **Handoff** | `**NEXT:** \`skill-id\`` · `**REQUIRES:** \`a\`, \`b\`` · `**ALT:** \`x\` \| \`y\`` |

**Do not** use `superpowers:<skill-id>` in skill bodies. That prefix is **legacy** (Claude Code marketplace plugin) only — document it in `SKILLS-REGISTRY.md` for upstream parity, not in runnable instructions.

**Do not** use made-up plugin sub-skills (e.g. `superpowers:implementer`). Bundled prompts live under `prompts/`, e.g. `subagent-driven-development/prompts/implementer-prompt.md`.

## Artifacts (repo paths)

Default layout (override via user request or repo `AGENTS.md` / team rules):

| Artifact | Default path |
| -------- | ------------- |
| Design spec (after brainstorming) | `docs/specs/YYYY-MM-DD-<topic>-design.md` |
| Implementation plan | `docs/plans/YYYY-MM-DD-<feature>.md` |

Legacy upstream path `docs/superpowers/{specs,plans}/` is equivalent if the team already uses it — pick **one** tree per repo and stay consistent.

**question-scope** work folders (`docs/work/...`) are the team workflow for L2–L4 phased work. Superpowers does not replace them. When both apply, see **`question-scope`** → `references/superpowers-supplement.md` and load **`@workflow`** for rule IDs. Opt out supplement only: `sp:off` / `no-sp` (not `superpowers:<id>`).

### One source of truth (avoid drift)

| Default | When to add `docs/specs/` or `docs/plans/` |
| ------- | -------------------------------------------- |
| **L2** and **bounded L3:** AC, assumptions, and plan tasks live in **`docs/work/...`** phase files (`l2-patch.md`, `l3-01-define.md`, …). | Only if the supplement table calls for it (large L3/L4, `writing-plans`, design gate). |
| Phase define file | Short summary + **links** to spec/plan files — do not copy full AC or task lists in two places. |
| `docs/specs/…`, `docs/plans/…` | L3 large / L4, subagents (`execute-via-subagents`), or explicit user request. Always link from the active phase file and `STATUS.md`. |

## Tools (canonical names)

Skills are written with **canonical** tool names. Map to your IDE/CLI using `superpowers/references/`:

| Canonical | Purpose |
| --------- | ------- |
| `invoke-skill` | Load a skill by ID (do not `read` skill files as a shortcut) |
| `task-tracker` | Checklist / todo list for skill steps |
| `subagent` | Dispatch an isolated agent with a prompt template |
| `plan-mode` | Dedicated planning UI mode (if the platform has one) |

Platform-specific names (Claude Code `Skill`, `TodoWrite`, `Task`, Copilot `skill`, Gemini `activate_skill`, etc.) belong only in `superpowers` and `references/*.md`.

## User / agent instructions

Highest priority: explicit user message, then repo **agent instructions file** (e.g. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` — whichever the project uses). Skills never override an explicit user “skip TDD” (or similar).

## Announce line

When a skill applies, announce once: `Using <skill-id> to <purpose>.` (Use the skill ID, not a vendor prefix.)

## Editing checklist

When changing any skill:

- [ ] Body and `description` in English
- [ ] Layout matches [STRUCTURE.md](./STRUCTURE.md) (supporting `.md` in `prompts/`, `references/`, or `templates/`)
- [ ] Cross-skill: `` `skill-id` `` or `**REQUIRES:**` / `**NEXT:**`; not `../other/SKILL.md`, `skills/<id>/`, `@skills/…`, or `superpowers:…`
- [ ] Paths use `docs/specs/` and `docs/plans/` defaults (or doc-root override pattern)
- [ ] Tool names are canonical or “map per references/”
- [ ] Examples are labeled as examples, not requirements
