# Pipelines quick reference (question-scope)

**~120 lines — read this during `/question-scope Lx` work.** Do **not** load [pipelines-skill-map.md](./pipelines-skill-map.md) (~700 lines) unless you need step tables, §6 skill detail, or §9 flow audit.

| Need | Read |
| ---- | ---- |
| Triggers, gates, STOP | [SKILL.md](../SKILL.md) only |
| Step checklists in phase files | [playbooks.md](./playbooks.md) + template under `docs/work/` |
| **Skill chain for your level** | **This file** § chains below |
| One skill’s full behavior | [pipelines-skill-map.md §6](./pipelines-skill-map.md#6-skill-deep-dive--purpose-when-called-what-it-does) — **one** subsection only |
| L2 vs L3 gray zone | [gray-zones.md](./gray-zones.md) |
| Supplement / plan A vs B | [superpowers-supplement.md](./superpowers-supplement.md) |

**After level chosen:** emit `Level: Lx | Pipeline: …` → run chain below → invoke each skill’s own `SKILL.md` when that step starts.

**Standalone / composition:** Skills below run without `/question-scope` when their `SKILL.md` matches, and combine per [COMPOSITION.md](../../COMPOSITION.md). Coordinated: [SKILL.md § Pipeline skills](../SKILL.md#pipeline-skills--standalone-coordinated-and-composition).

---

## Skill chains (by level)

### L1

```text
[explain-code?] → Answer in chat → [optional docs/answers/ MD]
```

No supplement. No `docs/work/`.

### L2

```text
Level check → Context → Spec
  → [generate-test? for TC rows]
  → Patch (test-driven-development if behavior changes)
  → verification-before-completion (scoped)
  → caveman-review → STATUS + l2-patch
```

**Bug overlay (before Patch):** `systematic-debugging` → TDD repro → fix → verify.

### L3 (supplement on, path B default)

```text
superpowers (once)
  → [brainstorming if no approved spec]
  → architect-plan | writing-plans (if >12 tasks / subagents)
  → [Scaffold?]
  → generate-test (RED — STOP before prod code)
  → using-git-worktrees (skip sp:off)
  → executing-plans OR subagent-driven-development (A + docs/plans/)
      └── test-driven-development per task
  → verification-before-completion (Verify)
  → verification-before-completion (Regression: module + 1-hop)
  → caveman-review → [requesting-code-review only if AC]
  → l3-03 rollout/rollback
  → finishing-a-development-branch
```

Record **B or A** in `STATUS.md` at Plan. **PR comments:** `receiving-code-review`.

### L4 (preset skips Idea/Scope)

```text
l4-01: Context + Validate + [analyze-impact]
  → brainstorming → architect-plan + [writing-plans dual]
  → generate-test → worktree → execute B/A + TDD
  → l4-04: Verify → caveman-review → requesting-code-review (default)
  → Regression per impacted service → Iterate
  → l4-05 Architecture/AI/Delivery → finishing-a-development-branch
```

**Execute order in `l4-04`:** Verify → Review → Regression (follow phase file, not 15-step list alone).

---

## Step → skill (compact)

| Step type | Skill | Done when |
| --------- | ----- | --------- |
| Vague idea | `orchestra-decision` | One decision; return to L pick |
| After L chosen | `superpowers` | Know which skills run; `sp:off` honored |
| Explain only | `explain-code` | User understands flow |
| Design gate | `brainstorming` | User **approved** spec on disk |
| Bounded plan | `architect-plan` | `### Tasks` in phase file |
| Large / subagents | `writing-plans` | `docs/plans/…` + link |
| Test before code | `generate-test` | TC table + RED logged |
| Isolate branch | `using-git-worktrees` | Path + baseline in phase MD |
| Execute inline | `executing-plans` | All tasks done → then Verify/Regression/Review/Ship |
| Execute subagents | `subagent-driven-development` | Needs `docs/plans/` + user chose A |
| Behavior change | `test-driven-development` | RED → GREEN → REFACTOR |
| Any “passes” / “done” | `verification-before-completion` | Fresh command output in phase MD |
| Bug | `systematic-debugging` | Root cause in Spec before patch |
| Blast radius | `analyze-impact` | Impact list; not test run |
| Quick review | `caveman-review` | Terse findings on diff |
| Formal pre-merge | `requesting-code-review` | L4 default; after green tests |
| PR comments | `receiving-code-review` | Each item verified + retested |
| Git endgame | `finishing-a-development-branch` | After l3-03/l4-05 content; user picked option |
| Every edit | `code-standards` (rule) | Diff meets security/style |

---

## When to open the full map

| Situation | Open in [pipelines-skill-map.md](./pipelines-skill-map.md) |
| --------- | ---------------------------------------------------------- |
| L2 patch | [§2](./pipelines-skill-map.md#2-l2--patch) only |
| L3 feature | [§3.1](./pipelines-skill-map.md#31-canonical-pipeline-all-l3) only |
| L4 system | [§4](./pipelines-skill-map.md#4-l4--large-system) only |
| “What does skill X do?” | [§6.x](./pipelines-skill-map.md#6-skill-deep-dive--purpose-when-called-what-it-does) **one** subsection |
| Audit / doc work | [§9](./pipelines-skill-map.md#9-per-flow-audit-skill-chains--recommended-adjustments) |

**Never** load §6.1–6.20 in one turn unless auditing the whole bundle.

---

## Human guide

Short skill table: [README.md § Pipeline skill summary](../README.md#pipeline-skill-summary). Tokens: prefer this quickref + target skill `SKILL.md`.
