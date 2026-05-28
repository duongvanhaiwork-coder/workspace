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
| `requesting-code-review` | Quality | After task/feature; before merge |
| `receiving-code-review` | Quality | Incoming review feedback |
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
| `analyze-impact` | AI Core | Blast radius before large rename/refactor |
| `refactor-code` | AI Core | Safe structural edits preserving behavior |
| `generate-test` | AI Core | Tests after behavior or contract changes |
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
brainstorming ──NEXT──► architect-plan (bounded L3 / work phase)
    │                 └──► writing-plans (large handoff / subagents)
    │                      │
    │ FORBIDDEN: any       ├── ALT-A ──NEXT──► subagent-driven-development
    │ implementation       │                      │
    │ before design        │                      ├── REQUIRES: using-git-worktrees
    │ approved             │                      ├── REQUIRES: test-driven-development
    │                      │                      ├── REQUIRES: requesting-code-review (per task)
    │                      │                      └── NEXT ──► finishing-a-development-branch
    │                      │
    │                      └── ALT-B ──NEXT──► executing-plans
    │                                             │
    │                                             ├── REQUIRES: using-git-worktrees
    │                                             ├── REQUIRES: test-driven-development
    │                                             └── NEXT ──► finishing-a-development-branch
    │
    └── spec path: docs/specs/YYYY-MM-DD-<topic>-design.md
        plan path: docs/plans/YYYY-MM-DD-<feature>.md
```

**ALT-A vs ALT-B:** User (or plan header) chooses exactly one after `writing-plans`. Do not run both on the same plan.

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
- **REQUIRES (context):** `using-git-worktrees` at execution time (isolated workspace)
- **NEXT (user choice):** `subagent-driven-development` **OR** `executing-plans`
- **Artifacts:** `docs/plans/YYYY-MM-DD-<feature>.md` (see CONVENTIONS.md)

### `subagent-driven-development`
- **REQUIRES:** `writing-plans` (`docs/plans/…` task file), `using-git-worktrees`, `test-driven-development`
- **REQUIRES (per-task review):** bundled `prompts/implementer-prompt.md`, `prompts/spec-reviewer-prompt.md`, `prompts/code-quality-reviewer-prompt.md`
- **RECOMMENDED:** `requesting-code-review` for ad-hoc / whole-branch review (not every task)
- **NEXT:** `finishing-a-development-branch`
- **ALT:** `executing-plans` (different session / no subagents / architect-plan-only phase plan)

### `executing-plans`
- **REQUIRES:** written plan (`writing-plans` **or** `architect-plan` in `docs/work/…`), `using-git-worktrees`, `test-driven-development`
- **NEXT:** `finishing-a-development-branch`
- **RECOMMENDED instead when possible:** `subagent-driven-development` (only with `docs/plans/…`)

### `finishing-a-development-branch`
- **REQUIRES:** tests passing (`verification-before-completion` immediately before)
- **Terminal:** user picks merge / PR / keep / discard

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
