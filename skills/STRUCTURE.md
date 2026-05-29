# Skill directory structure (canonical)

Every skill under `skills/<skill-id>/` uses the **same folder pattern**. The agent contract lives in **`SKILL.md`** (required). Other `.md` files must not sit loose at the skill root except `SKILL.md` and (optionally) `README.md`.

Portable rules: [CONVENTIONS.md](./CONVENTIONS.md). Composition (standalone + combine): [COMPOSITION.md](./COMPOSITION.md). Catalog: [README.md](./README.md).

**Catalog-wide references** (not a skill ID): [references/invocation-anti-patterns.md](./references/invocation-anti-patterns.md) — shared ✅/❌ for composition; per-skill § **Composition (quick ref)** links here.

---

## Standard layout

```text
skills/<skill-id>/
  SKILL.md                 # Required — agent playbook (YAML frontmatter name + description)
  README.md                # Optional — human usage (prompt examples, when to use)
  prompts/                 # Optional — subagent / reviewer dispatch templates
  references/              # Optional — deep-dive docs (do not replace SKILL.md)
  templates/               # Optional — copy-out artifacts (phase MD, commit template, …)
  examples/                # Optional — sample outputs / fixtures
  scripts/                 # Optional — shell, JS, helpers (non-markdown)
```

### Where to put `.md` files

| Content type | Location | Not at skill root |
| ------------ | -------- | ----------------- |
| Main playbook | `SKILL.md` | — |
| Human cheat sheet | `README.md` | — |
| Reviewer / implementer prompts | `prompts/*.md` | ~~`implementer-prompt.md`~~ |
| Deep-dive, anti-patterns, tracing | `references/*.md` | ~~`root-cause-tracing.md`~~ |
| Templates copied to `docs/work`, commit body | `templates/**` | ~~`TEMPLATE.md`~~ |
| L1–L4 phase files (question-scope) | `templates/phases/**` | — |
| Multi-IDE tool mapping (e.g. superpowers) | `references/*.md` | — |

**Skill root contains only:** `SKILL.md`, and `README.md` when needed.

### Creating a new skill

1. Create `skills/<skill-id>/` (kebab-case = skill ID).
2. Write `SKILL.md` with frontmatter `name` + `description` (“Use when …”) in **English**.
3. If you add prompts, references, or templates → create the subfolder **immediately**; do not leave stray `.md` at root.
4. Update [SKILLS-REGISTRY.md](./SKILLS-REGISTRY.md) if the skill joins the Superpowers bundle or team catalog.

---

## `templates/` variants

| Skill | Path | Purpose |
| ----- | ---- | ------- |
| **question-scope** | `templates/phases/` | Copy → `<target-repo>/docs/work/YYYY-MM-DD-<slug>/` |
| **commit-message** | `templates/TEMPLATE.md` | LINKID commit description body |
| *(other)* | `templates/<name>.md` | Single-file template |

---

## Current skill map (26)

| skill-id | README | prompts | references | templates | examples | scripts |
| -------- | ------ | ------- | ---------- | --------- | -------- | ------- |
| superpowers | — | — | ✓ | — | — | — |
| question-scope | ✓ | — | ✓ | ✓ phases | ✓ sample-prompts | — |
| brainstorming | — | ✓ | ✓ | — | — | ✓ |
| writing-plans | — | ✓ | — | — | — | — |
| subagent-driven-development | — | ✓ | — | — | — | — |
| requesting-code-review | — | ✓ | — | — | — | — |
| systematic-debugging | — | — | ✓ | — | — | ✓ |
| test-driven-development | — | — | ✓ | — | — | — |
| writing-skills | — | — | ✓ | — | ✓ | ✓ |
| commit-message | — | — | — | ✓ | — | — |
| caveman, caveman-commit, caveman-review, cavecrew | ✓ | — | — | — | — | — |
| architect-plan, analyze-impact, explain-code, refactor-code, generate-test, orchestra-decision, executing-plans, dispatching-parallel-agents, using-git-worktrees, verification-before-completion, finishing-a-development-branch, receiving-code-review | — | — | — | — | — | — |

**Minimal skills** (`SKILL.md` only): sufficient for short playbooks — no empty subfolders required.

---

## Linking from `SKILL.md`

Use paths relative to the skill directory:

```markdown
See [references/root-cause-tracing.md](references/root-cause-tracing.md).
Dispatch: [prompts/implementer-prompt.md](prompts/implementer-prompt.md).
Output format: [templates/TEMPLATE.md](templates/TEMPLATE.md).
```

Cross-skill (handoff):

```markdown
**REQUIRES:** `requesting-code-review` — use `prompts/code-reviewer.md` in that skill.
```

Cross-skill (deep link to a supporting file, optional):

```markdown
`question-scope` → `references/superpowers-supplement.md`
```

**Cursor rules (from skills):** cite rule IDs or `@workflow` — do **not** use `rules/…` file paths. See [CONVENTIONS.md](./CONVENTIONS.md) § Referencing Cursor rules.

