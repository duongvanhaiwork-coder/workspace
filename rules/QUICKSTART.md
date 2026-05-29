# Rules quickstart — question-scope + Superpowers

Short guide for Cursor/Kiro using this repo’s **English** rules and skills. Full scope contract: skill **`question-scope`** (invoke-skill). Workflow rule IDs: `@workflow` or `rules/cursor/workflow.mdc`.

Human guide (Vietnamese): **`question-scope`** → `README.md`. English one-pager: **`question-scope`** → `references/CHEATSHEET.md`. English prompts: **`question-scope`** → `examples/sample-prompts.md`.

## Two layers (one sentence)

| Layer | Answers | Source |
| ----- | ------- | ------ |
| **Question-scope** | How **much** work (L1–L4), `docs/work/…`, gates | `question-scope.mdc` + skill |
| **Superpowers supplement** | How to execute with discipline (TDD, verify, plan, worktree) | `workflow.mdc` + skills |

**Default:** L3/L4 → supplement on. L2 → TDD + verify minimal. L1 → no full Superpowers flow.

## Pick a level

| Level | When |
| ----- | ---- |
| **L1** | Explain / compare only; no repo edits |
| **L2** | Small patch, few files, clear AC |
| **L3** | Bounded feature (module, API, worker) |
| **L4** | Multi-service, large migration, AI platform |

## Copy-paste prompts

| Situation | Prompt |
| --------- | ------ |
| Tiny one-liner | `quick: <description>` |
| Patch / bug | `/question-scope L2 — <description> (@file)` |
| Feature | `/question-scope L3 — <description>` |
| Large system | `/question-scope L4 — <description>` |
| Unsure of level | `/question-scope` + task description → pick L1–L4 |
| Skip scope ceremony | `qs:off — <description>` |
| Scope on, no Superpowers | `/question-scope L3 — <task>. sp:off` |

## Opt-out tokens

| Token | Question-scope | Superpowers supplement |
| ----- | ---------------- | ---------------------- |
| `qs:off` / `no-scope` | Off | Off |
| `quick:` | Off (fast path) | Off |
| `qs:meta` / `audit:` | Off (explicit audit) | Off |
| `sp:off` / `no-sp` | On | Off |
| `/question-scope L2` … `L4` | On; skip level picker | Per level table in skill |

**Note:** `quick:` is **not** “L3 without design” — use `/question-scope L3` + `sp:off` for that. `quick:` is **not** “L2 with light rollup MD” — use `/question-scope L2` + “Rollup MD OK.” **Audit/review** skill or rules: `qs:meta — …` or `audit: — …` (preferred over keyword-only meta). `level Lx` without `/question-scope` does **not** activate scope. Level requires a **space** (`/question-scope L2`, not `/question-scopeL2`). Reviewing the skill/rules without running work does **not** activate scope (see skill **Meta discussion**).

## On-disk docs (target repo)

| Content | Path |
| ------- | ---- |
| STATUS, phases, blockers | `docs/work/YYYY-MM-DD-<slug>/` (L2–L4) |
| Design spec (optional) | `docs/specs/…` — link from phase file |
| Task plan (optional) | `docs/plans/…` — link from work folder |

One source of truth — see `skills/CONVENTIONS.md`.

## L3 skill chain (typical, supplement on)

```text
/question-scope L3 → docs/work/ + STATUS.md
  → brainstorming (spec approve) — skip if AC approved
  → architect-plan (l3-01) | writing-plans (docs/plans/) — see Plan path in supplement
  → generate-test (l3-02 TC table) — before Code
  → using-git-worktrees — skip with sp:off
  → executing-plans (B) | subagent-driven-development (A)
  → test-driven-development (per task during Code)
  → Verify → Regression (both use verification-before-completion; log l3-02)
  → caveman-review → l3-03-ship.md (rollout/rollback) → finishing-a-development-branch (Ship; fresh verify)
```

Rule IDs (`design-approval-gate`, `isolated-workspace`, …): `@workflow`.

## L2 skill chain (minimal supplement)

```text
/question-scope L2 — <task> (@files)
  → Spec + TC rows in l2-patch (if behavior changes; optional generate-test)
  → Patch + test-driven-development (if behavior)
  → verification-before-completion → Review (caveman-review)
```

## Bug (usually L2)

```text
/question-scope L2 — bug: <symptom> (@files)
→ systematic-debugging → test-driven-development (repro)
→ verification-before-completion
```

## Load full workflow graph

Cursor: `@workflow` or read `rules/cursor/workflow.mdc`.

## References

- Rules layout: [CONVENTIONS.md](./CONVENTIONS.md)
- Sync after rule edits: `make sync-ide` then reload Cursor window or new chat ([README.md](./README.md) § Sync to IDE)
- Skills layout: [../skills/STRUCTURE.md](../skills/STRUCTURE.md)
- Agent policy: [../AGENTS.md](../AGENTS.md)
