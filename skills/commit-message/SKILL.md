---
name: commit-message
description: >
  Company commit template with LINKID ticket prefix and full PR description block
  (AI Contribution, API/DB, scope). Use when the user wants LINKID format, team
  commit template, or branch ticket prefix. Do NOT use for short Conventional Commits
  — use caveman-commit instead.
---

# Branch Commit Message

> Output MUST include **Title** and **Description** per `templates/TEMPLATE.md` in this skill.

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

## Workflow

1. `git status --short`, `git diff --staged`, `git diff` if needed
2. Infer intent: feature, fix, refactor, test, docs, chore
3. Title: `[LINKID-XXXX] - <outcome-focused title>`
4. Description: follow **`commit-message/templates/TEMPLATE.md`** exactly (self-assess AI Contribution honestly). Present the filled description in **one** fenced code block so the user gets a **Copy** button.

## Quality

- Title matches actual diff; no secrets; no vague "update code"
- Prefix matches branch ticket after normalization

## Boundaries

- Generate message only — do not run `git commit` or stage files unless user asks
