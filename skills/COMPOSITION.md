# Skill composition (all skills under `skills/`)

Every skill may run **standalone**, **with `/question-scope Lx`**, or **combined with other skills** in the same session. Combine when the task needs it — do not invoke every skill in the catalog.

**Global rules:** [CONVENTIONS.md](./CONVENTIONS.md) § Invocation modes · Per-skill detail: each `SKILL.md` § **Invocation modes**.

## Default

| Rule | Meaning |
| ---- | ------- |
| **Composable** | If another skill’s **When to use** matches, invoke it — unless a **Requires (hard)** row blocks |
| **Standalone OK** | No `/question-scope` required; user message or task fit is enough |
| **Order** | User message → active skill(s) → **`question-scope`** gates only when scope is on |
| **Do not stack duplicates** | e.g. **`requesting-code-review`** per task when **`subagent-driven-development` (A)** already ran bundled reviewers |

## Requires (hard) — only these block composition

Use this table when unsure. Everything **not** listed is optional pairing.

| Skill | Requires (hard) | Standalone note |
| ----- | ---------------- | ---------------- |
| **`executing-plans`** | A **written plan** with executable tasks (`docs/plans/…`, phase `### Tasks`, or user paste in chat) | Plan can be informal in chat for tiny work |
| **`subagent-driven-development`** | **Task-level** plan file (`docs/plans/…` from **`writing-plans`**, or equivalent) — **not** **`architect-plan`**-only phase file | Use **`executing-plans` (B)** for phase-file-only plans |
| **`architect-plan`** | **Spec / AC** exists (from **`brainstorming`**, phase define, or user) — not a blank idea | **`orchestra-decision`** first if still fuzzy |
| **`writing-plans`** | **Approved spec** (or explicit AC) before large `docs/plans/…` | Small plan without full spec only if user accepts risk |
| **`finishing-a-development-branch`** | Fresh **`verification-before-completion`** before merge/PR options | — |
| **`systematic-debugging`** (before fix, behavior change) | **Root cause** documented; **`test-driven-development`** repro when behavior changes | Standalone: root cause in chat OK |
| **`subagent-driven-development`** (coordinated L3–L4) | **`generate-test`** / TC gate done before implement when scope requires Test-before-Code | Same as execute **B** |
| **`receiving-code-review`** | **`verification-before-completion`** after each fix before “done” | — |

**Not hard requirements (common mistakes):**

| Pair | Truth |
| ---- | ----- |
| **`brainstorming`** before every patch | **No** — L2 skip; standalone patch needs no spec file |
| **`using-git-worktrees`** always | **No** — optional standalone; skip L2, `sp:off`, user decline |
| **`question-scope`** before **`test-driven-development`** | **No** — TDD standalone is valid |
| **`writing-plans`** before **`architect-plan`** | **No** — choose one plan path per [superpowers-supplement](./question-scope/references/superpowers-supplement.md) |

## Common compositions (optional)

| Goal | Typical chain |
| ---- | ------------- |
| Fuzzy idea | **`orchestra-decision`** → **`brainstorming`** → **`architect-plan`** or **`writing-plans`** |
| Bounded feature + scope | **`/question-scope L3`** → **`brainstorming`** → **`architect-plan`** → **`generate-test`** → **`using-git-worktrees`** → **`executing-plans`** → **`verification-before-completion`** → **`finishing-a-development-branch`** |
| Bug | **`systematic-debugging`** → **`test-driven-development`** → **`verification-before-completion`** |
| Refactor | **`analyze-impact`** → **`refactor-code`** → **`verification-before-completion`** |
| Explain then patch | **`explain-code`** → **`test-driven-development`** (no scope required) |
| Review only | **`caveman-review`** or **`requesting-code-review`** alone |
| Parallel failures | **`dispatching-parallel-agents`** + per-domain **`systematic-debugging`** |

## question-scope

**Optional coordinator** — not a prerequisite for other skills. When active, it sets **L**, gates, and `docs/work/…`; skills still follow their own **Invocation modes** sections.
