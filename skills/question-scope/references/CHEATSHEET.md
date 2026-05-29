# Question Scope — one-page cheat sheet (English)

Full contract: [SKILL.md](../SKILL.md). User guide: [README.md](../README.md) (§ **Common workflow preset Lx only**). **Agent default:** [pipelines-quickref.md](./pipelines-quickref.md). Full tables: [pipelines-skill-map.md](./pipelines-skill-map.md) (one § at a time).

## Power user — preset `/question-scope Lx` only

Canonical path when you **already know L** (skips 4-option picker; pipeline + gates still apply).

```text
/question-scope L2 — <task> (@files)

/question-scope L3 — <task>
AC: …
docs/work/YYYY-MM-DD-<slug>/
```

| Rule | Detail |
| ---- | ------ |
| Placement | **Start or end** of message — not mid-sentence |
| Format | Space before `L`: `/question-scope L2` — not `/question-scopeL2` |
| Legacy | `level L2 — …`, `?fix …` — **do not** activate scope |
| New work item | Send `/question-scope Ly` again in same chat |
| Unsure L2 vs L3 once | `/question-scope` + task → agent asks **two** options (gray zone) |

**Agent off-track?** No `Level: Lx` header · no `docs/work/` (L2–L4) · L3 code before `generate-test` / RED · “done” without test command output → cite gate; see [pipelines-quickref.md](./pipelines-quickref.md).

## Activate scope (only these)

| You want | Paste |
| -------- | ----- |
| Unsure of level | `/question-scope` + task → pick **L1–L4** (each option shows **what that L does**; agent **STOP**s) |
| Known level | `/question-scope L2 — <task>` (L1/L3/L4) |
| Resume work | `@docs/work/.../STATUS.md` + `/question-scope L3 — continue` |

**Placement:** command at **start or end** of message — not mid-sentence.  
**Format:** `/question-scope L2` (space before `L`) — not `/question-scopeL2`.  
**Legacy (off):** `level L2 — …`, `?fix …` — use `/question-scope` instead.

## Turn scope off

| Token | Effect |
| ----- | ------ |
| `quick: <task>` | Fast path — no L1–L4, no `docs/work/` |
| `qs:off` / `no-scope` | Normal chat |
| `qs:meta — …` / `audit: — …` | Review skill/rules — no pipeline |
| Same message as `/question-scope Lx` | **Opt-out wins** |

`quick:` ≠ L2 with rollup MD → use `/question-scope L2 — … Rollup MD OK.`

## Levels (pick one)

| L | When | Code? |
| - | ---- | ----- |
| **L1** | Explain / compare only | No |
| **L2** | Patch, few files, clear AC | Yes |
| **L3** | Module, API, worker (bounded) | Yes + Regression + Ship |
| **L4** | Multi-service, large migration | Yes + 15-step flow |

**Gray zone:** agent asks **2 labeled options** only (e.g. L2 vs L3 for export on existing API) — each with a short “what happens” note — you must pick before work starts.

## Superpowers supplement (second layer)

| L | Default supplement |
| - | ------------------ |
| L1 | Off |
| L2 | TDD + verify (minimal) |
| L3–L4 | Worktree, TDD, inline execute (B), verify, ship |

Turn supplement off: `/question-scope L3 — <task>. sp:off`

## L3 skill chain (after level chosen)

```text
brainstorming → architect-plan | writing-plans
  → generate-test (l3-02) → using-git-worktrees
  → executing-plans (B) | subagent-driven-development (A)
  → test-driven-development (per task)
  → Verify + Regression → verification-before-completion (log in l3-02)
  → caveman-review → l3-03-ship.md (refine, rollout, rollback)
  → finishing-a-development-branch (fresh verify; merge | PR | keep | discard)
```

Plan: ≤12 tasks + ≤8 files → `architect-plan`; larger or subagents → `writing-plans`.

## L4 skill chain (after level chosen)

```text
l4-01-discover → analyze-impact (if unclear) + Validate (go/no-go)
  → l4-02-define (architect-plan | writing-plans) → l4-03-build (generate-test, execute, TDD)
  → l4-04-prove: Verify + Regression → caveman-review
  → [L4 supplement: requesting-code-review pre-merge]
  → l4-05-ship → finishing-a-development-branch
  → [after PR open] receiving-code-review (incoming comments; log PR feedback in phase MD)
```

Impact analysis ≠ Regression: `analyze-impact` lists blast radius; Regression **runs** tests named in prove phase. **Outgoing** review = `requesting-code-review`; **incoming** PR comments = `receiving-code-review`.

## L2 skill chain (minimal)

```text
Spec + TC rows (l2-patch; optional generate-test) → Patch + test-driven-development (if behavior)
  → verification-before-completion → caveman-review
```

## Common mistakes

| Wrong | Right |
| ----- | ----- |
| `Please /question-scope fix auth` | `/question-scope L2 — fix auth` or `fix auth /question-scope L2` |
| `quick:` but want L2 + rollup | `/question-scope L2 — … Rollup MD OK.` |
| `sp:off` alone | `/question-scope L3 — … sp:off` |
| New task, same chat, no new command | Send `/question-scope` or `/question-scope Ly` again |

## On disk (L2–L4)

```text
docs/work/YYYY-MM-DD-<slug>/
  STATUS.md          ← @ first in new session
  l2-patch.md        ← L2 (or rollup for tiny patches)
  l3-01-define.md …  ← L3
  l4-00-frame.md …   ← L4
```

## Stale Cursor rules?

After `make sync-ide`, only rules/skills install — **no scripts**. Reload window or new chat if chat shows old triggers (`level Lx`, `?` + keyword). In AI Core repo: `./scripts/check-question-scope-session.sh`.
