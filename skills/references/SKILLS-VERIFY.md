# Skills verification report

Full pass over **26** skills under `skills/`. Automated gates: `make verify` (structure + audit + question-scope contract + behavior anchors).

**Result:** `make verify` → **OK** (after P3/P4 reference splits reflected in verify scripts).

---

## Automated checks (all skills)

| Check | Tool | Result |
| ----- | ---- | ------ |
| `SKILL.md` exists, YAML `name` + `description` | `verify-skills-structure.sh` | 26/26 PASS |
| § Invocation modes + § Composition quick ref | `verify-skills-audit.sh` | 26/26 PASS |
| Relative links + local `prompts/` | `verify-skills-audit.sh` | 26/26 PASS |
| No `rules/` paths in SKILL (except `writing-skills` polarity link) | audit | PASS |
| question-scope contract + cross-skill behavioral anchors | `verify-question-scope-*.sh` | PASS |

**New/updated scripts:** `scripts/verify-skills-audit.sh`, `scripts/lib/question-scope-contract.sh` (grep SKILL + key `references/` for moved P3 content).

---

## Per-skill simulation (trigger → expected behavior)

“Simulation” = contract review: if the user message matches the YAML `description` / **When to use**, the agent should follow the playbook and handoffs below. Not an LLM run — use [behavioral-gates.md](../question-scope/references/behavior-gates.md) for optional live spot-checks.

| Skill | Example trigger | Expected announce / gate | Key NEXT / REQUIRES | Refs to load when executing |
| ----- | ----------------- | ------------------------ | --------------------- | ---------------------------- |
| `superpowers` | Any non-trivial task | Check skills first; scope STOP wins | `question-scope` before other process skills when triggered | `references/red-flags.md`, `invoke-flow.md` |
| `question-scope` | `/question-scope` at start/end | Level picker → **STOP** (or preset Lx) | Phase skills per L; supplement table | `parsing-tokens.md`, `level-picker-runtime.md` |
| `brainstorming` | New feature, behavior change | Design gate; user approve spec | `architect-plan` / `writing-plans` | `references/design-process.md` |
| `orchestra-decision` | Ambiguous direction | Q1–Q4 matrix; no prod code until Decide | `brainstorming` or scope | SKILL only |
| `architect-plan` | Bounded L3 plan in phase file | Plan in `docs/work/…` | `executing-plans` (B) default | `references/plan-output-guide.md` |
| `writing-plans` | Large / handoff plan | `docs/plans/…` | `subagent-driven-development` (A) or B | `prompts/` |
| `executing-plans` | Plan with tasks | Inline checkpoints | `verification-before-completion` → Ship chain | `prompts/` |
| `subagent-driven-development` | User chose A + `docs/plans/…` | Per-task implement + review | `verification-before-completion`; no commit unless asked | `references/example-advantages-red-flags.md`, `prompts/*` |
| `using-git-worktrees` | L3–L4 before Code | Isolation before execute | `executing-plans` or A | **MUST** `references/worktree-steps.md` |
| `generate-test` | L3–L4 Test phase | RED; no prod in Test phase | Code / TDD | SKILL + TC templates |
| `test-driven-development` | Behavior change | RED→GREEN | — | `references/tdd-cycle.md`, etc. |
| `systematic-debugging` | Bug / test fail | 4 phases before fix | TDD when behavior changes | `references/four-phases.md` |
| `verification-before-completion` | Before “done” | Iron Law: evidence | `finishing-a-development-branch` | SKILL |
| `finishing-a-development-branch` | Tasks done, tests green | Fresh verify → 4 options | `receiving-code-review` on PR comments | **MUST** `references/ship-process.md` |
| `requesting-code-review` | Pre-merge / formal review | Outgoing review | After `caveman-review` (L4) | `prompts/code-reviewer.md` |
| `receiving-code-review` | PR comments | Verify before implement | `verification-before-completion` per fix | `references/feedback-playbook.md` |
| `dispatching-parallel-agents` | 2+ independent failures | **REQUIRES** `systematic-debugging` per domain | — | SKILL |
| `analyze-impact` | Cross-module / L4 discover | Blast radius, not test run | Regression scope input | SKILL |
| `explain-code` | How does X work? | Read-only explain | Optional patch skills | SKILL |
| `refactor-code` | Refactor / cleanup | Preserve behavior | `verification-before-completion` | SKILL |
| `generate-test` | Test design gate | TC table / failing tests | TDD in Code | SKILL |
| `caveman-review` | Terse diff review | One-line comments | — | SKILL |
| `caveman-commit` | Short conventional commit | ≤50 char subject | — | SKILL |
| `commit-message` | LINKID template | Company format | — | `templates/` |
| `caveman` | caveman mode | Ultra-terse replies | — | SKILL |
| `cavecrew` | Delegate subagents | locate / build / review roles | — | SKILL |
| `writing-skills` | Author/verify skills | TDD for skills | `test-driven-development` | `references/discipline-cso-and-checklist.md` |

---

## P4 operational refs (must load when executing)

| Skill | MUST read reference | Lines (approx) |
| ----- | --------------------- | --------------: |
| `using-git-worktrees` | `worktree-steps.md` | 132 |
| `finishing-a-development-branch` | `ship-process.md` | 181 |
| `subagent-driven-development` | `example-advantages-red-flags.md` | 143 |
| `receiving-code-review` | `feedback-playbook.md` | 180 |
| `architect-plan` | `plan-output-guide.md` | 93 |
| `brainstorming` | `design-process.md` | 124 |
| `superpowers` | `red-flags.md`, `invoke-flow.md` | 24 + 32 |

---

## Fixes applied during this verification

1. **`finishing-a-development-branch`** — restored full `ship-process.md` (was truncated); removed duplicate steps from `SKILL.md`.
2. **`question-scope`** — contract anchors in SKILL (Sticky scope, parsing/meta, Impact analysis vs Regression, incoming PR).
3. **`receiving-code-review`** — clarify-all-items anchor in SKILL + playbook.
4. **Verify scripts** — contract grep across SKILL + `references/` after P3/P4 splits; new `verify-skills-audit.sh`.

---

## Optional manual spot-checks (LLM)

Not required for `make verify`. See `question-scope/references/behavioral-gates.md` — fixtures **#1, #6, #8/#21, #24–#42** in a **new chat** after `make sync-ide`.

**Related:** [SKILLS-AUDIT.md](./SKILLS-AUDIT.md) · [STRUCTURE.md](../STRUCTURE.md)
