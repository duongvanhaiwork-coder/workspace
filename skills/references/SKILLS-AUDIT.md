# Skills audit — polarity, composition, handoffs

Audit of all **26** skills under `skills/<skill-id>/SKILL.md` using the same frame as [rules/CONVENTIONS.md](../../rules/CONVENTIONS.md) § Rule authoring and [skills/CONVENTIONS.md](../CONVENTIONS.md) § Rules vs skills.

**Status:** P0–P4 + post-P3 polish **complete**. **You run:** `make sync-ide` + reload Cursor after **rule** edits only (P4 was skills-only; see [Post-P3 operator steps](#post-p3-operator-steps)).

---

## Executive summary

### Strengths

- **26/26** skills include § **Invocation modes** (standalone / coordinated / Combines / Requires).
- **Discipline skills** (`systematic-debugging`, `test-driven-development`, `verification-before-completion`) use **negative-heavy** gates (Iron Law, Red Flags) — correct polarity for “block wrong completion.”
- **Process skills** (`executing-plans`, `brainstorming`) pair STOP gates with positive step lists.
- Shared composition mistakes live in [invocation-anti-patterns.md](./invocation-anti-patterns.md) — good single source of truth.
- **`question-scope`** is the intentional canonical contract; `question-scope.mdc` is a short mirror (`qs-2026-05-29.3`).

### Top 5 risks (remediated)

1. **Token bloat** — reduced via P2/P3/P4 reference splits (`question-scope` 257, `subagent-driven-development` 195, `TDD` 151 lines).
2. **Composition quick ref** — **26/26** skills link [invocation-anti-patterns.md](./invocation-anti-patterns.md).
3. **Rules duplication** — git gates in `code-standards`; skills cite rule IDs / one-liners.
4. **Handoff holes** — NEXT/Stop when added on key skills (verify → finish → receiving, generate-test → worktree, etc.).
5. **Contract sync** — `qs-2026-05-29.3`; [CONTRACT-SYNC.md](../question-scope/references/CONTRACT-SYNC.md).

---

## Summary table (26 skills)

| Skill | Lines | Polarity | Quick ref | Announce | Stop when | Status |
| ----- | ----: | -------- | :-------: | :------: | :-------: | ------ |
| `refactor-code` | 72 | Mixed | Yes | Yes | — | Done |
| `commit-message` | 74 | Positive | Yes | Yes | — | Done |
| `explain-code` | 81 | Mixed | Yes | Yes | Yes | Done |
| `caveman-review` | 85 | Positive | Yes | Yes | — | Done |
| `caveman-commit` | 93 | Positive | Yes | — | — | Done |
| `analyze-impact` | 102 | Neg § | Yes | Yes | Yes | Done |
| `generate-test` | 103 | Mixed | Yes | Yes | RED | Done |
| `cavecrew` | 119 | Balanced | Yes | Yes | — | Done |
| `caveman` | 125 | Positive | Yes | — | Mode | Done |
| `executing-plans` | 136 | Neg+flow | Yes | Yes | Blocked | Done |
| `systematic-debugging` | 141 | Neg-heavy | Yes | Yes | 4 phases | Done (P3) |
| `test-driven-development` | 151 | Very neg | Yes | Yes | Red Flags | Done (P3) |
| `writing-skills` | 154 | Mixed | Yes | Yes | — | Done (P3) |
| `requesting-code-review` | 167 | Balanced | Yes | Yes | When NOT | Done |
| `orchestra-decision` | 191 | Pos+gate | Yes | Yes | Decide | Done |
| `verification-before-completion` | 204 | Very neg | Yes | Yes | Iron Law | Done |
| `writing-plans` | 208 | Pos+STOP | Yes | Yes | architect | Done |
| `dispatching-parallel-agents` | 219 | Balanced | Yes | Yes | When NOT | Done |
| `architect-plan` | 137 | Mixed | Yes | Yes | Yes | Done (P4) |
| `brainstorming` | 113 | Balanced | Yes | Yes | spec OK | Done (P4) |
| `question-scope` | 257 | Mixed | Yes | Yes | STOP | Done (P3, `qs-2026-05-29.3`) |
| `finishing-a-development-branch` | 85 | Neg-heavy | Yes | Yes | Red flags | Done (P2+P4) |
| `using-git-worktrees` | 138 | Neg-heavy | Yes | Yes | Red flags | Done (P2+P4) |
| `receiving-code-review` | 106 | Neg-heavy | Yes | Yes | verify | Done (P4) |
| `subagent-driven-development` | 195 | Neg-heavy | Yes | Yes | Red Flags | Done (P4) |
| `superpowers` | 168 | Neg-heavy | Yes | Yes | — | Done (P4) |

---

## Per-skill detail

### `superpowers` (~210 lines)

- **Polarity:** Negative-heavy (Red Flags, MUST check skills first) + positive invoke-skill map.
- **Composition:** Quick ref present; links anti-patterns.
- **Gaps:** Overlaps `@workflow` `skill-check-first`; no bundled prompts.
- **Fix:** P2 — keep SKILL lean; anti-patterns already shared.

### `question-scope` (255 lines after P3)

- **Polarity:** Mixed — STOP/level picker (negative) + pipelines (positive).
- **Contract:** `qs-2026-05-29.3` — [CONTRACT-SYNC.md](../question-scope/references/CONTRACT-SYNC.md).
- **P3:** Parsing, session, JIT, level-picker runtime → `references/`.

### `writing-skills` (~673 lines)

- **Polarity:** Mixed; teaches concise skills while SKILL is largest in repo.
- **Gaps:** CSO, rationalization tables, checklist bloat inline.
- **Fix:** P2 — move discipline blocks to `references/discipline-cso-and-checklist.md`.

### `orchestra-decision` (~189 lines)

- **Polarity:** Positive phased playbook; weak hard STOP before implementation.
- **Fix:** P1 — add “no production code / no Spec until Decide phase completes.”

### `brainstorming` (~217 lines)

- **Polarity:** Balanced; `<HARD-GATE>` + checklist.
- **Gaps:** Missing composition quick ref; blur with `orchestra-decision`.
- **Fix:** P0 quick ref row: orchestra = direction only.

### `writing-plans` (~199 lines)

- **Polarity:** Positive plan steps + STOP when `architect-plan` fits.
- **Fix:** P0 quick ref; pointer to plan path in supplement.

### `architect-plan` (~223 lines)

- **Polarity:** Mixed; strong Handoff + Stop when + Announce.
- **Gaps:** Duplicated qs pipeline text — prefer links.
- **Fix:** None critical.

### `executing-plans` (~137 lines)

- **Polarity:** Strong STOP + positive steps 1–3.
- **Fix:** None critical.

### `subagent-driven-development` (~316 lines)

- **Polarity:** Negative-heavy (Never Red Flags).
- **Gaps:** Examples imply agent commits — conflicts **`code-standards`** git gates; per-task review vs `requesting-code-review`.
- **Fix:** P0 quick ref; clarify no commit unless user asked.

### `using-git-worktrees` (~285 lines)

- **Polarity:** Strong NEVER red flags.
- **Gaps:** `.gitignore` commit note vs git policy in rules.
- **Fix:** P2 — move Red flags / Common mistakes to `references/red-flags.md`.

### `dispatching-parallel-agents` (~217 lines)

- **Polarity:** Balanced pattern + When NOT.
- **Fix:** P1 — REQUIRES `systematic-debugging` per failure domain before fix integration.

### `systematic-debugging` (~336 lines)

- **Polarity:** Negative-heavy (Iron Law, 4 phases).
- **Fix:** P0 quick ref; P2 optional trim of rationalization tables to references.

### `test-driven-development` (~441 lines)

- **Polarity:** Very negative — correct for discipline.
- **Gaps:** Bloat; overlap with `generate-test` Test phase.
- **Fix:** P0 quick ref; P2 move rationalizations + example to `references/pressure-and-examples.md`.

### `verification-before-completion` (~193 lines)

- **Polarity:** Iron Law + gate function — exemplary negative gates.
- **Fix:** P0 quick ref; P1 **NEXT:** `finishing-a-development-branch` when shipping.

### `generate-test` (~104 lines)

- **Polarity:** Mixed RED gate + positive steps.
- **Fix:** P1 **NEXT:** `using-git-worktrees` (L3–L4) before Code.

### `requesting-code-review` (~155 lines)

- **Polarity:** Balanced when/when-not.
- **Fix:** P0 quick ref (vs subagent A per-task review).

### `receiving-code-review` (~261 lines)

- **Polarity:** Strong NEVER + verify before implement.
- **Fix:** P0 quick ref; P1 **NEXT** in invocation block after fixes.

### `analyze-impact` (~100 lines)

- **Polarity:** Do not claim tests pass — good negative.
- **Fix:** P1 **Stop when:** blast radius documented; **Handoff** to Regression scope.

### `explain-code` (~79 lines)

- **Polarity:** Was weak negative — read-only boundary added.
- **Fix:** P1 **Stop when:** user has flow summary; **NEXT** TDD/refactor if patching.

### `refactor-code` (~72 lines)

- **Polarity:** Mixed; cites behavior preservation.
- **Fix:** None critical.

### `finishing-a-development-branch` (~292 lines)

- **Polarity:** Strong NEVER red flags.
- **Fix:** P0 quick ref; P1 **NEXT:** `receiving-code-review` when PR open; P2 red-flags ref.

### `commit-message` (~65 lines)

- **Polarity:** Positive template workflow.
- **Fix:** P0 quick ref (OR `caveman-commit`).

### `caveman-commit` (~84 lines)

- **Polarity:** Positive format; negative = never in subject.
- **Fix:** P0 quick ref; pointer **`code-standards`** Commits for git gates.

### `caveman-review` (~75 lines)

- **Polarity:** Positive format.
- **Fix:** P0 quick ref vs `requesting-code-review`.

### `caveman` (~115 lines)

- **Polarity:** Positive compression.
- **Fix:** P0 quick ref; clarify not every response unless user enabled mode.

### `cavecrew` (~119 lines)

- **Polarity:** Balanced ✅/❌ + contracts.
- **Fix:** None critical.

---

## Remediation matrix (implemented)

| Tier | Action | Files |
| ---- | ------ | ----- |
| **P0** | § Skill authoring polarity in CONVENTIONS | `skills/CONVENTIONS.md` |
| **P0** | Composition quick ref (14 skills) | `skills/*/SKILL.md` |
| **P1** | Handoffs / Stop when / gates | 6–8 skills (see table) |
| **P2** | Split long sections to `references/` | `writing-skills`, `test-driven-development`, `question-scope`, `using-git-worktrees`, `finishing-a-development-branch` |
| **Follow-up** | Dedup CONVENTIONS lines, Announce/Stop/NEXT, git gates, TDD/debug pressure refs | 2026-05-29 second pass |
| **P3** | Contract `qs-2026-05-29.3`; trim SKILL → `references/` | question-scope, TDD, systematic-debugging, writing-skills |

### P3 line counts (SKILL.md)

| Skill | Before P3 (~) | After P3 |
| ----- | ------------- | -------- |
| `question-scope` | 374 | **255** |
| `test-driven-development` | 331 | **151** |
| `systematic-debugging` | 306 | **141** |
| `writing-skills` | 197 | **153** |

### P3 new references

| Skill | Reference files |
| ----- | ---------------- |
| `question-scope` | `parsing-tokens.md`, `session-continuity.md`, `progressive-context-jit.md`, `level-picker-runtime.md`, `CONTRACT-SYNC.md` |
| `test-driven-development` | `tdd-cycle.md`, `tdd-completion-checklist.md` (+ existing `pressure-and-examples.md`) |
| `systematic-debugging` | `four-phases.md` (+ existing `debugging-pressure.md`) |
| `writing-skills` | `skill-md-skeleton.md` (+ existing `discipline-cso-and-checklist.md`) |

Run `make sync-ide` after rule contract bump so `~/.cursor/rules/question-scope.mdc` shows `qs-2026-05-29.3`.

---

## Post-P3 operator steps

**You (manual):**

```bash
cd /Users/chanh/workspace && make sync-ide
```

Then reload the Cursor window or start a new chat.

Optional:

```bash
./scripts/check-question-scope-session.sh
```

**Agent-completed:** P0–P4 (announce lines, reference splits, composition quick refs, contract `qs-2026-05-29.3`). [question-scope/references/README.md](../question-scope/references/README.md) indexes P3 files.

---

## P4 complete

Long operational sections moved to `references/` with **full content preserved** (header `P4 trim` in reference files). SKILL.md keeps Invocation modes, gates, Integration, and links; **MUST read** on operational refs where steps run in-session.

| Skill | SKILL.md lines | Reference file(s) |
| ----- | -------------: | ----------------- |
| `subagent-driven-development` | 195 | `references/example-advantages-red-flags.md` |
| `receiving-code-review` | 106 | `references/feedback-playbook.md` |
| `architect-plan` | 137 | `references/plan-output-guide.md` |
| `brainstorming` | 113 | `references/design-process.md` (+ existing `visual-companion.md`) |
| `superpowers` | 168 | `references/red-flags.md`, `references/invoke-flow.md` |
| `using-git-worktrees` | 138 | `references/worktree-steps.md` (+ `red-flags.md` P2) |
| `finishing-a-development-branch` | 85 | `references/ship-process.md` (+ `red-flags.md` P2) |

**Fix applied:** `ship-process.md` was truncated during extraction — restored from git `c054fd4` (181 lines); corrupted duplicate in `SKILL.md` removed.

Stack rules (`shell`, `sql`, `terraform`) remain under `rules/` — out of scope unless requested.

---

## Per-skill detail (archive)

Historical notes from the audit pass. **Current status:** see [Summary table](#summary-table-26-skills) — all **26/26 Done** (P0–P4).

---

## Maintenance checklist

When editing any skill:

- [ ] English body + YAML `description` (“Use when…”, not workflow summary)
- [ ] § Invocation modes + Composition quick ref → anti-patterns
- [ ] Negatives for gates; positives for steps; cite **`code-standards`** / rule IDs instead of restating
- [ ] Bump `question-scope` contract in rule + skill together if triggers change
- [ ] Run `make sync-ide` after rule edits only (not required for skill-only changes)

**Verification:** [SKILLS-VERIFY.md](./SKILLS-VERIFY.md) — `make verify` OK after P4 + script updates.

**Related:** [SKILLS-REGISTRY.md](../SKILLS-REGISTRY.md) · [COMPOSITION.md](../COMPOSITION.md) · [STRUCTURE.md](../STRUCTURE.md)
