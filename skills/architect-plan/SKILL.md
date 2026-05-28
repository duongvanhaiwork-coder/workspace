---
name: architect-plan
description: Help create implementation plans by thinking through scope, dependencies, execution order, and completion criteria. Use when the user asks to plan, architect, or design a feature.
---

# Architect Plan

## Mindset

You are helping a human think through a problem before writing code.
Your job is to surface risks and dependencies they might miss, not to fill in a template.
Scale your effort to the problem -- a one-file fix needs a one-line plan.

## Where to write the plan

When **question-scope** is active, put the plan in the work folder phase file (do not duplicate full AC elsewhere). See **`question-scope`** → [Plan choice (L3–L4)](../question-scope/references/superpowers-supplement.md#plan-choice-l3l4):

| Level | Default path |
| ----- | ------------ |
| L3 | `docs/work/YYYY-MM-DD-<slug>/l3-01-define.md` (bounded feature; pair with **execute-inline-checkpoints**) |
| L4 | `docs/work/YYYY-MM-DD-<slug>/l4-02-define.md` (or the repo’s L4 define phase file) |

Use **`writing-plans`** → `docs/plans/YYYY-MM-DD-<feature>.md` only when the supplement table calls for a large handoff or subagents (A). Link from the phase file and `STATUS.md`.

## What to think about

1. **Scope**: What is actually changing? Read the codebase to understand, don't guess.
   If unclear, ask the user (max 2 questions, be specific).

2. **Dependencies**: Which files/modules depend on each other?
   This determines what can happen in parallel vs what must be sequential.
   State the reasoning, not just the grouping.

3. **Definition of Done**: For each piece of work, what does "finished" look like?
   This can be one sentence. It can also include rollback plans or performance targets
   when the stakes justify it -- use judgment.

4. **Risks worth naming**: Not every plan needs a risk section.
   But if you see something that could break production, lose data, or degrade performance
   significantly -- name it. Briefly. With a mitigation if you have one.

## What NOT to do

- Don't over-plan trivial changes. A rename doesn't need 5 sections.
- Don't invent risks that aren't there. If it's safe, say it's safe.
- Don't prescribe solutions you're not confident about.
  "This might benefit from caching but I'd need to see the data volume" is better
  than "Use Redis here".
- Don't assume your plan is complete. End with what you're uncertain about.

## After implementation

If the plan contained critical tasks, add a Human Todo suggesting retrospective.
Do NOT auto-run retrospective -- the human decides when to reflect.
Most plans won't need it.
