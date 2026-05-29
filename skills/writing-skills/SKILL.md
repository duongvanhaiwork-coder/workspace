---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

**Announce when applying:** `Using writing-skills to <author|verify> skill <skill-id>.`

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md).

### Standalone

Authoring/verifying skills — independent of `/question-scope`.

### With question-scope

Not an application pipeline step.

### Combines with (optional)

- **`test-driven-development`** — RED/GREEN discipline for skill pressure tests

### Requires (hard)

- None

When editing skills, preserve § **Invocation modes** per [CONVENTIONS.md](../CONVENTIONS.md).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| TDD for skills: baseline fail → write SKILL → verify pass | Ship skill without pressure scenario |
| Gates in **rules**; playbooks in **skills** | Paste `/question-scope` trigger tables into `SKILL.md` |
| Deep CSO / checklists in `references/` | Restate full **`code-standards`** Security in skills |

**Polarity guide:** [CONVENTIONS.md](../CONVENTIONS.md) § Skill authoring · [rules/CONVENTIONS.md](../../rules/CONVENTIONS.md) § Rule authoring

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**Skills are identified by skill ID** (kebab-case directory name under `skills/<skill-id>/`). See [CONVENTIONS.md](../CONVENTIONS.md) for layout and cross-skill cites.

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand `test-driven-development` before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

**Official guidance:** For Anthropic's official skill authoring best practices, see [references/anthropic-best-practices.md](references/anthropic-best-practices.md). This document provides additional patterns and guidelines that complement the TDD-focused approach in this skill.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations agent uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify agent now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

The entire skill creation process follows RED-GREEN-REFACTOR.

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (if it's enforceable with regex/validation, automate it—save documentation for judgment calls)

## Skill Types

### Technique
Concrete method with steps to follow (condition-based-waiting, root-cause-tracing)

### Pattern
Way of thinking about problems (flatten-with-flags, test-invariants)

### Reference
API docs, syntax guides, tool documentation (office docs)

## Directory Structure

Follow the repo canonical layout: **[../STRUCTURE.md](../STRUCTURE.md)** and **[../CONVENTIONS.md](../CONVENTIONS.md)** (skills vs rules split and rule polarity: § **Rules vs skills**).

```text
skills/<skill-id>/
  SKILL.md              # Required — agent playbook
  README.md             # Optional — human usage
  prompts/              # Subagent / reviewer templates (*.md)
  references/           # Deep-dive docs (*.md)
  templates/            # Copy-out artifacts (e.g. question-scope/templates/phases/)
  examples/             # Sample outputs
  scripts/              # Shell, JS helpers
```

**Flat namespace** — skill ID = directory name under `skills/`.

**Keep inline in SKILL.md:** principles, short patterns (< 50 lines).

**Move to subfolders:** heavy reference → `references/`; dispatch templates → `prompts/`; copy-out MD → `templates/`.

## SKILL.md skeleton

[references/skill-md-skeleton.md](references/skill-md-skeleton.md).

## Deep reference (CSO, discipline, checklist)

Full content: [references/discipline-cso-and-checklist.md](references/discipline-cso-and-checklist.md) — CSO, rationalization tables, RED-GREEN-REFACTOR for skills, deployment checklist.

## Discovery Workflow

How future Claude finds your skill:

1. **Encounters problem** ("tests are flaky")
3. **Finds SKILL** (description matches)
4. **Scans overview** (is this relevant?)
5. **Reads patterns** (quick reference table)
6. **Loads example** (only when implementing)

**Optimize for this flow** - put searchable terms early and often.

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).
Same benefits: Better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills. It's the same discipline applied to documentation.
