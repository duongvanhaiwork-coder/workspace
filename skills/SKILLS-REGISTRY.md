# Superpowers Skills Registry

Canonical map for skill IDs, handoffs, and dependency strength. Use this when forking, porting a subset, or editing cross-references in `SKILL.md` files.

**With question-scope (this repo):** L1–L4 gates and `docs/work/…` are owned by **`question-scope`**; Superpowers playbooks layer on L2–L4 per `question-scope/references/superpowers-supplement.md`. Rule IDs (load `@workflow`) mirror handoffs below.

**Skill ID** = directory name under `skills/` (e.g. `writing-plans`).
**In skill bodies:** use skill ID + `**NEXT:**` / `**REQUIRES:**` only — see [CONVENTIONS.md](CONVENTIONS.md).
**Legacy plugin name** (Claude Code marketplace only): `superpowers:<skill-id>` — do not use in portable skill text.

## Dependency strength

| Label | Meaning |
|-------|---------|
| **NEXT** | Invoke immediately after the current skill completes its terminal step |
| **REQUIRES** | Must be available and followed while executing the current skill |
| **RECOMMENDED** | Use when platform or context supports it; skill may name an alternative |
| **ALT** | Valid alternative path (pick one, not both) |
| **FORBIDDEN** | Do not invoke before terminal step of current skill |

## Skill catalog

| ID | Role | Triggers (summary) |
|----|------|-------------------|
| `superpowers` | Meta | Session start; any task; before clarifying questions |
| `brainstorming` | Process | Creative work, features, behavior changes — before code |
| `writing-plans` | Process | Approved spec; multi-step implementation |
| `using-git-worktrees` | Process | Isolated feature work; before plan execution |
| `subagent-driven-development` | Execute | Plan + independent tasks + subagents (same session) |
| `executing-plans` | Execute | Plan + inline execution + checkpoints |
| `dispatching-parallel-agents` | Execute | 2+ independent failure domains |
| `test-driven-development` | Discipline | Feature, bugfix, refactor — before production code |
| `systematic-debugging` | Discipline | Bug, test fail, unexpected behavior — before fixes |
| `verification-before-completion` | Discipline | Before “done”, commit, PR, next task |
| `requesting-code-review` | Quality | Formal pre-merge (L4 supplement default); whole-branch — not duplicate subagent A per-task review |
| `receiving-code-review` | Quality | Incoming PR feedback (`incoming-code-review`); verify before implement — after PR open, not a scope phase step |
| `finishing-a-development-branch` | Close | All tasks done; tests pass |
| `writing-skills` | Meta | Authoring or changing skills |

## Team catalog (AI Core workspace)

Team skills live under `skills/<id>/`. They complement the Superpowers table above; **question-scope** owns L1–L4 gates and `docs/work/…`. See [README.md](README.md) for clusters and common flows.

| ID | Role | Typical use |
| ---- | ------ | ----------- |
| `question-scope` | Workflow | L1–L4 levels, phased `docs/work/`, triggers, opt-outs; human prompts in [question-scope/README.md](question-scope/README.md) (VI) |
| `architect-plan` | Plan | Bounded implementation plan in work phase files (default L3–L4 Plan; pair with execute **B**) |
| `orchestra-decision` | Process | Ambiguous problem — Q1–Q4 matrix before scope or design |
| `explain-code` | AI Core | How does this work? / call flow (MCP or editor fallback) |
| `analyze-impact` | AI Core | Blast radius (L4 discover/plan; L3 one-service optional); feeds Regression scope — not test execution |
| `refactor-code` | AI Core | Safe structural edits preserving behavior |
| `generate-test` | AI Core | Test design before Code (L3–L4 gate, `l3-02`/`l4-03` TC table); L2 optional TC rows |
| `caveman-review` | Quality | Terse PR/diff review |
| `commit-message` | Delivery | LINKID company commit template |
| `caveman-commit` | Delivery | Short Conventional Commits |
| `caveman` | Communication | Ultra-terse reply mode |
| `cavecrew` | Communication | When to delegate locate / build / review subagents |

**Typical order (code change):** `explain-code` → `analyze-impact` (if large touch) → `refactor-code` → `generate-test`. **With scope:** pick L1–L4 first via `question-scope`, then layer Superpowers supplement per level. **Plan routing (L3–L4):** see **`question-scope`** → `references/superpowers-supplement.md` § Plan path decision.

## Handoff graph (feature workflow)

```text
superpowers (always check skills first)
    │
    ▼
brainstorming ──NEXT──► architect-plan (bounded L3)  |  writing-plans (large / subagents)
    │                           │                              │
    │                           └──────────┬───────────────────┘
    │                                      ▼
    │                      generate-test (TC table; before Code)
    │                                      ▼
    │                      using-git-worktrees (skip sp:off / L2 / decline)
    │                                      ▼
    │ FORBIDDEN: any              pick ONE execute path:
    │ implementation       ├── ALT-B (default L3) ──► executing-plans
    │ before design        │       REQUIRES: plan (phase ### Tasks OR docs/plans/)
    │ approved             │       REQUIRES: test-driven-development, verification-before-completion
    │                      │       NEXT (after tasks): Verify + Regression → Review
    │                      │            → l3-03/l4-05 Ship phase → finishing-a-development-branch
    │                      │
    │                      └── ALT-A (user chose A) ──► subagent-driven-development
    │                              REQUIRES: docs/plans/ from writing-plans
    │                              REQUIRES: bundled prompts/ reviewers per task
    │                              REQUIRES: test-driven-development, verification-before-completion
    │                              NEXT (after tasks): same → finishing-a-development-branch
    │
    └── spec path: docs/specs/YYYY-MM-DD-<topic>-design.md
        plan path: docs/plans/YYYY-MM-DD-<feature>.md (A requires; B optional)
```

**ALT-A vs ALT-B:** User (or plan header) chooses **exactly one** after plan + Test gate — whether plan came from **`architect-plan`** or **`writing-plans`**. Do not run both on the same plan. **`docs/plans/` alone does not imply A.**

## Handoff graph (bug / fix)

```text
systematic-debugging (4 phases; no fix before root cause)
    │
    ├── REQUIRES at fix step: test-driven-development (failing repro test)
    └── NEXT before claiming fixed: verification-before-completion
```

Optional: `dispatching-parallel-agents` when multiple **independent** failure domains.

## Per-skill dependencies

### `superpowers`
- **NEXT (process before implementation):** `brainstorming` when entering plan/design mode without prior brainstorm
- **Priority:** process skills before implementation skills

### `brainstorming`
- **NEXT:** `architect-plan` (bounded L3 / `docs/work/…` phase) **or** `writing-plans` (`docs/plans/…` — large handoff / subagents). See **`question-scope`** → `references/superpowers-supplement.md` § Plan path decision.
- **FORBIDDEN-NEXT:** any implementation skill, code, scaffold
- **Optional:** `references/visual-companion.md` + `scripts/` (browser mockups)

### `writing-plans`
- **REQUIRES (at execute):** `using-git-worktrees` when supplement on (L3–L4 default) — **skip** if `sp:off` / user declined / work in place
- **NEXT (user choice):** `subagent-driven-development` **OR** `executing-plans`
- **Artifacts:** `docs/plans/YYYY-MM-DD-<feature>.md` (see CONVENTIONS.md)

### `subagent-driven-development`
- **REQUIRES:** `writing-plans` (`docs/plans/…` task file), `test-driven-development`, `verification-before-completion`
- **REQUIRES (L3–L4):** Test design gate — **`generate-test`** / TC table before Code (same as B)
- **REQUIRES:** `using-git-worktrees` when supplement on — **skip** if `sp:off` / user declined (verify branch + baseline in place)
- **REQUIRES (per-task review):** bundled `prompts/implementer-prompt.md`, `prompts/spec-reviewer-prompt.md`, `prompts/code-quality-reviewer-prompt.md`
- **RECOMMENDED:** `requesting-code-review` for ad-hoc / whole-branch review (not every task)
- **NEXT (L3–L4):** Verify/Regression → Review → Ship phase MD → **`finishing-a-development-branch`**
- **ALT:** `executing-plans` (**B** — default L3; inline same session; phase plan or `docs/plans/`)

### `executing-plans`
- **REQUIRES:** written plan (`architect-plan` in `docs/work/…` **or** `docs/plans/…` from `writing-plans`), `test-driven-development`
- **REQUIRES:** `using-git-worktrees` when supplement on — **skip** if `sp:off` / **L2** / user declined
- **REQUIRES:** `verification-before-completion` — per task and before done
- **NEXT (L3–L4):** Verify/Regression → Review → Ship phase MD → **`finishing-a-development-branch`**
- **ALT:** `subagent-driven-development` (**A**) — only when user/plan chose A and `docs/plans/…` exists

### `finishing-a-development-branch`
- **REQUIRES:** Verify + Regression green in phase file (L3–L4); Review done; `l3-03-ship.md` / `l4-05-ship.md` updated (rollout/rollback)
- **REQUIRES:** tests passing — **`verification-before-completion`** immediately before options (fresh run)
- **Terminal:** user picks merge / PR / keep / discard
- **PREVIOUS (do not skip):** `executing-plans` or `subagent-driven-development` ends at tasks done — not Ship

### `systematic-debugging`
- **REQUIRES (phase 4):** `test-driven-development`
- **RECOMMENDED:** `verification-before-completion`

### `writing-skills`
- **REQUIRES background:** `test-driven-development`

### `requesting-code-review` / `receiving-code-review`
- No hard NEXT; pair with execute/close skills as needed

## Port bundles (copy sets)

| Bundle | Skill IDs |
|--------|-----------|
| **lite** | `superpowers`, `test-driven-development`, `systematic-debugging`, `verification-before-completion` |
| **standard** | lite + `brainstorming`, `writing-plans`, `executing-plans`, `using-git-worktrees`, `finishing-a-development-branch`, `receiving-code-review` |
| **power** | standard − `executing-plans` + `subagent-driven-development` (+ `prompts/*`) + `requesting-code-review` (+ `prompts/code-reviewer.md`) |
| **optional** | `dispatching-parallel-agents`, `brainstorming/scripts/*`, `writing-skills` |

## Reference syntax (when editing SKILL.md)

Prefer one style per fork:

```markdown
**NEXT:** `writing-plans`
**REQUIRES:** `test-driven-development`, `using-git-worktrees`
**ALT:** `executing-plans` | `subagent-driven-development` (user chooses after plan)
```

Legacy plugin form (upstream Claude Code): `superpowers:<skill-id>` — equivalent to **Skill ID**; not used in this fork’s SKILL.md bodies.

## Not part of runtime port

- `tests/` — plugin eval only
- `docs/plans/*.md`, `docs/testing.md` in repo root — maintainer history
- Harness dirs: `.cursor-plugin/`, `.claude-plugin/`, `hooks/` (unless self-hosting plugin)
