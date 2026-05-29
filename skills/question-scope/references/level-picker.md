# Level picker (question-scope)

Use when **suggesting** level or presenting options (heuristic only — user chooses unless `/question-scope Lx` preset).

## Trigger flow

```mermaid
flowchart TD
  A[User message] --> B{qs:off / no-scope / quick: / qs:meta / audit:?}
  B -->|yes| Z[Normal chat + code-standards rule]
  B -->|no| C{Meta keywords or discuss /question-scope without run intent?}
  C -->|yes| Z
  C -->|no| D{/question-scope + whitespace + L1-L4?}
  D -->|yes| RUN[Run pipeline preset Lx]
  D -->|no| E{/question-scope at start or end?}
  E -->|no| Z
  E -->|yes| G{/question-scopeL1-L4 glued no space?}
  G -->|yes| HINT[Hint once - no preset Lx]
  G -->|no| F[Idea + Suggest Lx]
  HINT --> F
  F --> H{Only one gray pair fits?}
  H -->|no| I[4 options L1-L4 STOP]
  H -->|L1 vs L2| T[Exactly 2 options STOP]
  H -->|L2 vs L3| T
  H -->|L3 vs L4| T
  T --> J[User picks]
  I --> J
  J --> RUN
```

Details: [gray-zones.md](./gray-zones.md) · triggers: [SKILL.md](../SKILL.md#when-this-skill-applies)

## Host UI (all AI IDEs)

Same skill contract ([SKILL.md](../SKILL.md)) on every host. **Full host rules:** [host-ui.md](./host-ui.md).

| Topic | All hosts |
| ----- | --------- |
| **Level pick** | Structured picker tool **or** numbered list — **same full labels**; **STOP** until pick |
| **Gray zone** | Exactly **2** options (not four) |
| **After pick** | Header `Level: Lx \| Pipeline: …` |
| **§12** | Decision + Why + 2–4 options + **Other**; picker tool **or** `A`/`B`/numbered list |

**Agent:** Do not re-ask level every turn (**sticky scope**). **New unrelated task** → `/question-scope` or `/question-scope Ly` again. **Never** skip STOP because the host has no picker tool — use chat fallback ([host-ui.md](./host-ui.md)).

## Clarifying options (after level pick)

**Level picker** chooses **L1–L4**. **How** to build (API, UX, config) uses **IDE-ALIGNED §12** — [clarifying-options.md](./clarifying-options.md) — not this file.

## Option copy (required — user must read before pick)

Every level pick (4 options, 2 gray options, or **escalation** re-pick) must show **what that L will do** next to the ID — not ID-only (`L1`, `L2`, …).

**Full turn shape (Idea, Suggest, comparison table, §12):** [confirmation-prompts.md](./confirmation-prompts.md).

| Part | Rule |
| ---- | ---- |
| **Format** | `Lx — <short title> · <what happens>` (use `·` between clauses; keep each option ≤ ~2 lines) |
| **Structured picker** (when host provides) | Put the **full** string in each option **label** / title field — [host-ui.md](./host-ui.md) |
| **Chat fallback** (always valid) | Numbered list `1.` … or table — **same** full strings; **STOP** until pick |
| **Do not** | Bare `L1`…`L4` buttons with no pipeline note; walls of prose before the list |
| **Task clause** | After canonical label, add `For this task: <one line>` — see [confirmation-prompts.md § A](./confirmation-prompts.md#a-level-pick-idea--suggest--options) |

After the user picks, emit header `Level: Lx | Pipeline: …` then run that pipeline ([SKILL.md § Pipelines](../SKILL.md#pipelines-ui)).

### Four options (default picker)

Use these lines verbatim or tighten wording only if the task needs one extra clause (e.g. “no `@` required” for L1).

| ID | Option label (copy for structured picker or numbered list) |
| -- | ---------------------------------------------------- |
| **L1** | **L1 — Explain only** · No repo edits · Light context → answer in chat (optional `docs/answers/` archive) |
| **L2** | **L2 — Small patch** · Context → Spec (+ TC if behavior change) → Patch → Verify → Review · Few files · `docs/work/` rollup or `l2-patch.md` |
| **L3** | **L3 — Bounded feature** · Context → Spec → Plan → **Test** (`generate-test`, `l3-02`, RED) → Code → Verify → Regression → Review → Ship · Phased `l3-*` + `STATUS.md` |
| **L4** | **L4 — Large system** · Full 15-step flow (incl. **Test Design** step 8) · Multi-service impact / validate · Phased `l4-*` + `STATUS.md` |

### Two options (gray zone only)

Present **only** the matching pair from [gray-zones.md](./gray-zones.md) — same note style:

| Pair | Lighter option note | Heavier option note |
| ---- | -------------------- | ------------------- |
| **L1 vs L2** | **L1 — Explain only now** · No Spec/Patch/Code in repo | **L2 — Fix in repo** · Spec → Patch → Verify → Review |
| **L2 vs L3** | **L2 — Extend existing pattern** · TC in Spec if behavior change · Scoped Verify (no full Regression gate) | **L3 — New module/API/worker** · Plan → **Test** (`l3-02`) before Code → Regression + Ship |
| **L3 vs L4** | **L3 — One service/repo** · Bounded feature pipeline | **L4 — Multi-service / platform** · Validate + architecture + full delivery flow |

**Example (L2 vs L3):** export CSV on existing users API → show **only** the L2 and L3 rows above, not all four levels.

### Escalation re-pick

When work **exceeds** the chosen L, re-present **at least** the adjacent pair using the same **Option copy** table (explain why in one line, then the two/four labeled options, then **STOP**).
