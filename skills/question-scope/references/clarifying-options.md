# Clarifying options (question-scope only)

**Applies only when** `/question-scope` or `/question-scope Lx` activated scope (not `quick:`, `qs:off`, meta/audit). Normal chat and Plan mode **without** scope do **not** require this contract.

**Opt-out (scope still on):** **`clarify:off`** — skip §12 for this message/work item until user removes it or picks explicitly in chat ([parsing-tokens.md](./parsing-tokens.md)).

**Cross-reference:** **IDE-ALIGNED §12** · level depth: [level-picker-runtime.md](./level-picker-runtime.md) · gray **levels**: [gray-zones.md](./gray-zones.md).

## What this is (vs level picker)

| Picker | Question | When |
| ------ | -------- | ---- |
| **Level picker** | “How much ceremony?” (**L1–L4**) | `/question-scope` **without** `Lx` on command → **STOP** before Context/Spec |
| **Clarifying options** | “How should we build it?” (API, UX, config, trade-off) | **After** level header, during **Spec** or **Plan** (and host Plan confirm) |

Do **not** use clarifying options to re-ask L1–L4. Do **not** use the level picker for technical forks (e.g. JSON vs redirect).

## When to run

| Run §12 | Skip §12 |
| ------- | ---------- |
| Open decision blocks AC, contract, UX, security, or rollout | AC and plan are fully specified |
| Attached plan lists **Open decisions** / TBD | Plan attach answers everything — only **delta** in Spec |
| L2+ **Spec** or L3/L4 **Spec / Plan** before Patch/Code | **Assessment-only** (gap/review) unless user must pick scope for the answer |
| Host Plan mode **before** user confirms plan | L1 explain-only (optional one fork if it changes the answer) |
| User sent **`clarify:off`** | Agent proceeds with stated AC or asks one plain question — no multi-option picker |

**Batching:** Prefer **one** clarifying question per turn (one structured picker block **or** one numbered list). If multiple independent decisions exist, list them in Spec as **Pending** and resolve **highest impact first**.

## STOP gate

After presenting clarifying options:

1. **STOP** — no Patch, Test authoring for new contract, or Code until the user picks **A–D** or **Other**.
2. **Other** means the user will reply in chat with their own wording — treat that reply as the decision; do not invent a default.
3. Record the chosen option in **Spec**, plan **delta**, `STATUS.md`, or phase MD (**one bullet** per decision).

## Option format (required)

Present **2–4** options. Each option label must include:

- **Short name** (what we’re choosing)
- **Behavior** (what happens for user/system)
- **One-line trade-off** (cost, test impact, client impact)

**Before options:** one **Decision** headline (`?`) + **Why it matters** (1–2 lines). **Do not** jump straight to A/B/C.

**Worked examples + decision scan:** [confirmation-prompts.md](./confirmation-prompts.md) § B.

**Viability (without full brainstorming):** [confirmation-prompts.md § Grounding](./confirmation-prompts.md#grounding--viability-without-full-brainstorming) — each option **Fits repo** *or* **New here** (idea-driven); trade-offs + STOP + Verify. Repo read is **optional** when forks are product/architecture alternatives. Use **`brainstorming`** when *many* directions are still open, not for every single §12 fork.

**Always include a final option:**

| Presentation | Last option label (canonical English) |
| ------------ | ------------------------------------- |
| Structured picker or numbered list | **`Other — I'll specify`** |

**Do not** mark a technical default as “recommended” unless the user asked for a recommendation or one option is clearly required by repo policy / security (then say **why** in one line).

### Example (OAuth callback) — minimal vs required

**Too thin (do not):**

```text
JSON or redirect?
A — JSON
B — Redirect
```

**Required shape:** see [confirmation-prompts.md § B](./confirmation-prompts.md#b-clarifying-options-12) (Decision + Why it matters + labeled consequences + **Other**).

## Host UI (all AI IDEs)

| Presentation | Behavior |
| ------------ | -------- |
| **Structured picker** (when host provides) | 2–4 options + **Other** last; full label per option |
| **Chat fallback** (always valid) | Numbered **A–D** or `1.`…`4.` + **Other — I'll specify**; **STOP** until reply |

Details: [host-ui.md](./host-ui.md). Same sticky rules as level picker.

## Plan attach and host Plan mode

| Situation | Action |
| --------- | ------ |
| Approved plan with no open questions | **Skip** §12 |
| Plan has TBD / “TBD” / “decide later” | §12 for each TBD **before** Code |
| Host Plan mode (read-only) | Treat as **Plan** step; §12 on open items **before** user confirms plan |
| User confirms plan with unresolved TBD | **STOP** — clarify or update plan delta |

Align with **IDE-ALIGNED §1** (plan attach = Spec).

## Recording decisions

In phase MD or chat rollup, use:

```markdown
## Decisions
- **D1 (chosen):** <option label or user Other text> — <date or turn>
```

For `scope:light` L2, decisions may live only in **chat rollup** if no `docs/work/`.

## Related skills (scope on)

| Skill | §12 interaction |
| ----- | ----------------- |
| `brainstorming` | **Whole** feature/spec still open (L3–L4, no approved spec) — approved design before Plan. **Not** for a single §12 fork — use §12 + [grounding](./confirmation-prompts.md#grounding--viability-without-full-brainstorming). **After** spec approved → **no** §12 for same decision ([confirmation-prompts § After brainstorming](./confirmation-prompts.md#after-brainstorming--do-not-duplicate-12)) |
| `architect-plan` / `writing-plans` | Open decisions in plan → §12 before execute |
| `orchestra-decision` | Idea **before** `/question-scope` — not a substitute for §12 after level is set |
| `gray-zones` | Level pairs only — not technical forks |

## What not to do

- Clarifying options **without** active scope (user did not send `/question-scope`)
- More than **four** technical options without grouping or a follow-up turn
- Skipping **Other** to force a pick
- Implementing a heavy default while “waiting” for user
- Re-running §12 for decisions already recorded in `STATUS.md` / Spec / **approved brainstorming spec** for this work item
