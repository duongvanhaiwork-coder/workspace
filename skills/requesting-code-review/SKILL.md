---
name: requesting-code-review
description: >
  Formal pre-merge review via subagent + code-reviewer prompt. Also when user asks
  for formal review before merge/PR. L4 supplement default when scope active; L3 if AC asks.
  Not duplicate per-task reviewers in subagent-driven-development (A).
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

User asks for formal review before merge, or after a feature slice — run this skill; no `/question-scope` required.

### With question-scope

**L4** supplement default after `caveman-review` + prove green; **L3** only if AC/user asks; log in phase MD before Ship.

### Combines with (optional)

- `caveman-review` — quick pass before formal review
- `verification-before-completion` — tests green first

### Requires (hard)

- None

**Instruction precedence:** User message → this skill → **`question-scope`** Ship/Review order only when scope active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

## With question-scope (vs `caveman-review`)

| Review type | Skill | When |
| ----------- | ----- | ---- |
| **Quick diff** (L2+) | **`caveman-review`** | Review step in phase MD — terse comments, security/SOLID |
| **Formal pre-merge** (L4 supplement) | **This skill** | After Verify/Regression green; before Ship merge/PR — rule `outgoing-code-review` |
| **Per-task (execute A only)** | **`subagent-driven-development`** bundled prompts | Spec + code-quality reviewer **each task** — **do not** also run this skill every task |

**Levels:** **L3** — this skill only if AC/user asks. **L4** + supplement on — **default** formal pre-merge (waive if user/`sp:off`/AC says skip). Always after **`verification-before-completion`** evidence.

**Incoming human PR comments:** **`receiving-code-review`** — different direction.

## When to Request Review

**Use this skill (whole-branch / pre-merge):**
- **L4** supplement on — before merge/PR (after `caveman-review` + prove phase Review)
- **L3** or **L2** — when AC or user asks for formal subagent review
- After completing a major feature slice (before Ship)
- Before merge to main / before `finishing-a-development-branch` option 1 or 2

**Do not use as duplicate per-task review when:**
- **`subagent-driven-development` (A)** already ran spec + code-quality reviewers for that task — use this skill once for **whole branch** if needed (RECOMMENDED in that skill), not again per task

**Optional but valuable:**
- When stuck (fresh perspective)
- Before large refactor (baseline check)
- After fixing complex bug (before claiming done)

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Fill template at `prompts/code-reviewer.md`. Map **subagent** to your platform:

| Platform | Mechanism |
| -------- | --------- |
| Cursor | **Task** tool — `subagent_type: generalPurpose` (or team reviewer preset) |
| Claude Code | **Task** tool with reviewer type |
| Other | Isolated agent with prompt body from the template |

**Note:** **`subagent-driven-development`** uses its own `prompts/spec-reviewer-prompt.md` and `prompts/code-quality-reviewer-prompt.md` per task — use **this** skill for ad-hoc or whole-branch review, not as a hard duplicate of every task review.

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Question-scope L3–L4 (after execute):**
```text
Verify/Regression → caveman-review → [L4: this skill if supplement/AC] → Ship phase MD → finishing-a-development-branch
```

**Subagent-Driven Development (A):**
- Per-task review = bundled prompts only
- **Once** before Ship: optional/recommended **whole-branch** pass with this skill — not mandatory after every task

**Executing Plans (B):**
- `caveman-review` at Review step; **L4:** add this skill when supplement/AC requires formal pre-merge

**Finishing a Development Branch:**
- Before merge locally or **Push + PR** — confirm formal review done when L4 supplement applies; fix Critical/Important findings first

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: requesting-code-review/prompts/code-reviewer.md
