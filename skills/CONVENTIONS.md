# Skills conventions (portable)

Canonical rules for **all** skills under `skills/<skill-id>/` in this repo (Superpowers bundle + team catalog). Not Claude Code plugin IDs; not host-specific paths unless noted as examples.

**Directory layout (prompts / references / templates):** [STRUCTURE.md](./STRUCTURE.md).

## Language

| Location | Language |
| -------- | -------- |
| `skills/**/SKILL.md` | **English only** (body, headings, YAML `description`) |
| `skills/**/README.md` | **English** (default) |
| `skills/question-scope/README.md` | **Vietnamese** (team exception — human prompt cheat sheet) |
| `prompts/`, `references/`, `templates/` under skills | **English** |
| Optional Vietnamese; prefer [rules/QUICKSTART.md](../rules/QUICKSTART.md) for English workflow |

Do not add Vietnamese (or other languages) to `SKILL.md` or supporting skill docs except **`question-scope/README.md`**. User prompts in chat may be any language; skill contracts stay English for agents.

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

**question-scope** work folders (`docs/work/...`) are the team workflow for L2–L4 phased work. Superpowers does not replace them. When both apply, see `skills/question-scope/SKILL.md` § **Superpowers supplement** and `rules/workflow.mdc` (rule IDs). Opt out supplement only: `sp:off` / `no-sp` (not `superpowers:<id>`).

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

- [ ] Body and `description` in English (except `question-scope/README.md`)
- [ ] Layout matches [STRUCTURE.md](./STRUCTURE.md) (supporting `.md` in `prompts/`, `references/`, or `templates/`)
- [ ] References use `` `skill-id` `` or `**REQUIRES:**` / `**NEXT:**`, not `superpowers:…`
- [ ] Paths use `docs/specs/` and `docs/plans/` defaults (or doc-root override pattern)
- [ ] Tool names are canonical or “map per references/”
- [ ] Examples are labeled as examples, not requirements
