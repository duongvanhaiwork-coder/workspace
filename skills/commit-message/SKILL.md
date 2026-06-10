---
name: commit-message
description: >
  Company commit template with LINKID ticket prefix and full PR description block
  (AI Contribution, API/DB, scope). Use when the user wants LINKID format, team
  commit template, or branch ticket prefix. Do NOT use for short Conventional Commits
  — use caveman-commit instead.
---

# Branch Commit Message

**Announce when applying:** `Using commit-message for LINKID commit/PR body.`

> Output MUST include **Title** and **Description** per `templates/TEMPLATE.md` in this skill.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard).

### Standalone

Invoke when the user wants a commit/PR message — no `/question-scope` required.

### With question-scope

Not a pipeline phase; may run after **`finishing-a-development-branch`** on L3–L4 Ship, or anytime.

### Combines with (optional)

- **`finishing-a-development-branch`** — when user chooses commit/PR

### Requires (hard)

- None

### Composition (quick ref)

| ✅ Do                                                                | ❌ Don't                                                      |
| -------------------------------------------------------------------- | ------------------------------------------------------------- |
| LINKID template from `templates/TEMPLATE.md` when user/repo requires | **`caveman-commit`** short Conventional format in same commit |
| User asked for commit message / PR body                              | Create git commit unless user asked — **`code-standards`**    |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use

- User asks for LINKID / team / company commit message format
- Branch like `feature/linkid-6313` and full description sections required
- User explicitly names this skill or the LINKID template

## When NOT to use

- User wants terse Conventional Commits (`feat(scope): …`) → **caveman-commit**
- User says "caveman commit" or "/commit" without LINKID

## Branch ticket

1. `git branch --show-current`
2. Extract `linkid-\d+` (case-insensitive) → normalize to `LINKID-6313`
3. If missing: ask once for ticket, or `[NO-TICKET] - <title>`

## ⛔ Do not

- **Do not** generate the commit message from memory or assumed format. You **MUST read** `templates/TEMPLATE.md` (via `read_file`) **every time** before producing output — no exceptions.
- **Do not** skip the template read step even if you "remember" the format from a previous turn or session.
- **Do not** output Title or Description until the template file content is loaded in context.

## Workflow

1. **Read template:** open `templates/TEMPLATE.md` in this skill folder — confirm structure is in context.
2. `git status --short`, `git diff --staged`, `git diff` if needed
3. Infer intent: feature, fix, refactor, test, docs, chore
4. Title: `[LINKID-XXXX] - <outcome-focused title>`
5. Description: follow **`commit-message/templates/TEMPLATE.md`** exactly (self-assess AI Contribution honestly). Present the filled description in **one** fenced code block so the user gets a **Copy** button.

## Quality

- Title matches actual diff; no secrets; no vague "update code"
- Prefix matches branch ticket after normalization

## Boundaries

- Generate message only — do not run `git commit` or stage files unless user asks
