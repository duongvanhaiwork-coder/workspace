---
name: receiving-code-review
description: >
  Incoming PR/review feedback — verify before implementing (rule incoming-code-review).
  Runs after PR open with or without question-scope. Opposite of requesting-code-review.
---

# Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

**Announce when applying:** `Using receiving-code-review for incoming PR feedback.`

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

PR or review comments on your branch — run this skill; no `/question-scope` required.

### With question-scope

Same process; log rounds in `docs/work/…` **PR feedback** / Iterate when scope active (common L3–L4 Ship).

### Combines with (optional)

- `verification-before-completion` — after each fix

### Requires (hard)

- **`verification-before-completion`** after each fix batch before claiming addressed

**Instruction precedence:** User message → this skill → phase MD logging when coordinated scope is active ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

**Stop when:** All review items understood (or clarified) and either implemented with evidence or explicitly deferred with user agreement.

**NEXT:** **`verification-before-completion`** after each fix → push/update PR → optional **`requesting-code-review`** only if user asks for another outgoing pass.

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify each comment; implement only after understanding | Blind “thanks, fixed” without **`verification-before-completion`** |
| Use [feedback-playbook.md](references/feedback-playbook.md) for forbidden phrases / examples | Performative agreement without code change |
| **NEXT:** **`verification-before-completion`** after each fix batch | Treat as **`requesting-code-review`** (outgoing) |
| Log rounds in `docs/work/…` when scope on | Skip GitHub thread reply rules in SKILL when replying inline |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## With question-scope (incoming ≠ outgoing review)

Rule ID: **`incoming-code-review`** (`@workflow`). **Not** a numbered L1–L4 pipeline step — runs when **PR or review comments arrive** (often after **`finishing-a-development-branch`** option 2 Push + PR).

| Direction | Skill |
| --------- | ----- |
| **Outgoing** (you request review) | **`requesting-code-review`** — before merge |
| **Incoming** (others comment on your PR) | **This skill** |

| Related | Notes |
| ------- | ----- |
| **`subagent-driven-development` (A)** | Per-task spec/code-quality feedback is handled **inside** execute A — **not** a substitute for this skill on human PR threads |
| **`caveman-review`** | You **write** terse review comments — not receive |
| After each fix | **`verification-before-completion`** — log test command + output before “fixed” |
| Phase log | `l3-02` / `l4-04` § **PR feedback / Iterate** — link comment → fix → retest |

**Levels:** Any L2–L4 when a PR exists; common during L3–L4 Ship iteration (worktree kept for PR path).

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Feedback playbook

Full detail: [references/feedback-playbook.md](references/feedback-playbook.md).

**Unclear feedback:** **Clarify all items** before partial implementation — **Need clarification** on any unclear item first (see playbook § Handling Unclear Feedback).

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## After implementing fixes

1. Run tests — **`verification-before-completion`** (fresh evidence per claim).
2. Push to PR branch; update phase **PR feedback** table if `docs/work/…` is active.
3. Reply in thread with what changed (technical, no thanks — see Acknowledging Correct Feedback).

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Technical rigor always.
