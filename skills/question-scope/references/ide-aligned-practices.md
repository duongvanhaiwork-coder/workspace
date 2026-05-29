# IDE-aligned practices

Adopt what autonomous IDE agents do well **without** removing question-scope gates (level pick, test-before-code on new contracts, bug root-cause).

**When to load:** L2–L4 implementation, review/assessment tasks, attached plans, or when the user asks how scope differs from “IDE tự chạy”.

**Cross-reference ID (other skills):** cite **`IDE-ALIGNED §N`** — no `../question-scope/…` paths in child `SKILL.md` files ([CONVENTIONS.md](../../CONVENTIONS.md) § Cross-referencing question-scope).

| § | Topic |
| - | ----- |
| §1 | Plan attach = Spec |
| §2 | JIT context |
| §3 | Assessment-only |
| §4 | Tiered test gates |
| §5 | Verify in chat |
| §6 | Regression from diff |
| §7 | Short review |
| §8 | `scope:light` |
| §9 | MCP |
| §11 | Child skills |
| §12 | Clarifying options (scope only) |

---

## 1. Attached plan = Spec (no duplicate docs)

| Signal | Agent action |
| ------ | ------------- |
| User attached an **approved** plan (e.g. `.plan.md`, Cursor Plan output, PRD with AC) | **Spec satisfied** — summarize plan + list **delta** only (what changed vs plan, open questions) |
| User says **follow attached plan** / plan is the task | **Do not** create `docs/work/…` unless user also wants team archive or multi-session handoff |
| No plan, L2–L4 multi-session | Create `docs/work/…` per [session-continuity.md](session-continuity.md) |

**Cursor Plan mode:** Treat read-only Plan step as **Plan** in the L3/L4 pipeline. After user **confirms** the plan → proceed to **Test** (L3+) then **Code** — do not re-write a second full plan in `docs/work/` unless archiving.

---

## 2. JIT context (borrow from IDE)

| Gate | Default | Plan / `@file` exception |
| ---- | ------- | ------------------------- |
| **STOP before wide context (L2)** | No unbounded grep before Spec | **Skip** if Spec/AC is already in attached plan or user `@` primary files (≤3) with clear task |
| Expansion | One hop from entry when Spec needs code | Use rule **`mcp-intelligence`**: `get_context` / `search_code` when MCP connected; else `@file` → Read → one import hop |

Budgets unchanged: [progressive-context-jit.md](progressive-context-jit.md).

---

## 3. Task kind: implement vs assessment

Detect **assessment** when the user asks for gap/review/comparison **without** asking to implement (e.g. “có cần sửa gì không”, “gap vs plan”, “review only”, “đánh giá”, “what’s missing”) — even under `/question-scope L3`.

| Task kind | Pipeline (after level header) | Skip |
| --------- | ------------------------------ | ---- |
| **Implement** | Full pipeline for chosen L | — |
| **Assessment** | Context (light) → **Assessment** → Answer → optional short MD | Plan, Scaffold, Test, Code, Regression, Ship — **unless** user then asks to fix |

**Sticky:** Same work item + assessment → stay assessment until user says implement/fix/patch.

**Header example:** `Level: L3 | Pipeline: Context → Assessment → Answer`

---

## 4. Test gate tiers (L2–L4)

Do **not** require a full TC table for every touch.

| Change type | Test gate |
| ----------- | --------- |
| Config-only, comments, typos, logging text | **Verify** (build/lint) only |
| Bugfix or behavior change in **existing** tested module | At least **one** new/updated test case in Spec; run scoped tests in **Verify** |
| New public API, module, or contract | L3+: **Test** / `generate-test` **before Code** (full gate) |
| Hardening only (security/ops) in module that already has tests | Add test for the hardening path when feasible; else document manual check in Verify |

L3 **STOP before Code** applies to **new contract / new module** rows — not to assessment-only or config-only rows.

---

## 5. Verify — evidence in chat (mandatory)

Before claiming **done**, **fixed**, or **tests pass** (L2+):

1. Run the relevant command(s) (`build`, `test`, `lint`, migration dry-run, …).
2. Paste in the **chat reply**: command + **exit code** + brief outcome (pass/fail count).
3. Optional: also log in phase MD / `STATUS.md` — **chat evidence is required**; MD alone is not enough.

Align with skill **`verification-before-completion`**.

---

## 6. Regression scope — infer from diff

L3 **Regression** default:

1. From changed paths (`git diff --name-only` or equivalent), derive test targets:
   - e.g. `src/client/social/**` → `test/unit/client/social/**`
2. Run those tests + **1-hop** integration tests that call the changed public surface.
3. Log commands in chat (§5) and optionally in phase MD.

Do **not** run the full monorepo suite unless AC or user requires it.

---

## 7. Review — short by default (L2–L3)

| Level | Review style |
| ----- | ------------- |
| L2–L3 | **`caveman-review`**: max **~5** one-liners on the diff (location · problem · fix) |
| L2–L3 security | Full checklist only when diff touches: **public routes**, **webhooks**, **auth/authZ**, **PII/secrets** |
| L4 | Full checklist + optional **`requesting-code-review`** per supplement |

Skip essay-length review unless user sent `audit:` or formal review is requested.

---

## 8. Tokens and L2 doc weight

| Token | Match | Effect |
| ----- | ----- | ------ |
| **`scope:light`** | `(^|\s)scope:light\b` | Scope **stays on**. L2: **no** required `docs/work/` folder — end with **chat rollup** (AC, commands, caveats). Same gates for Spec/Patch/Verify. |
| **`Rollup MD OK`** (in task) | User text | Same as `scope:light` for L2 doc — may combine |

**`scope:light` is not** `quick:` — scope pipelines and gates still apply.

**`quick:`** still turns scope **off** entirely.

---

## 9. MCP and IDE tools

When rule **`mcp-intelligence`** applies and MCP is connected:

- **L3** (before wide Patch): optional bounded `search_code` / `analyze_impact` for blast radius.
- **L4 Discover:** prefer **`analyze-impact`** skill / MCP over repo-wide grep.

When MCP is down: editor `@file` / Read / one-hop imports — state results are search-based.

---

## 10. What not to copy from IDE

Keep question-scope **stricter** than default IDE on:

- Inferring L1–L4 without `/question-scope` (rule Default)
- Code before tests on **new** public contracts (L3+)
- Bug patches without root cause (bug overlay)
- Scope creep / drive-by refactors (`code-standards` change scope)
- Claiming success without command output (§5)

---

## 11. Child skills (workspace `skills/`)

When **`/question-scope`** is active, each invoked skill should honor this table. Full chains: [pipelines-quickref.md](./pipelines-quickref.md) · [COMPOSITION.md](../../COMPOSITION.md#task-kind-question-scope-active).

| Skill | IDE-aligned adjustment |
| ----- | ------------------------ |
| `verification-before-completion` | Chat evidence **required** when scope on; phase MD optional |
| `generate-test` | Tiered gate; **skip** on assessment-only and config-only |
| `test-driven-development` | L2: only when Spec has TC rows; not for config-only |
| `systematic-debugging` | JIT from stack trace + `@file` before wide grep |
| `explain-code` | Plan attach → explain per plan sections |
| `analyze-impact` | L3 optional once before Patch; suggest regression paths from diff |
| `brainstorming` | **Skip** if plan attach, assessment-only, or AC on disk; else product forks → **§12** before heavy Plan |
| `architect-plan` / `writing-plans` | Plan attach → delta only; plan **TBD** → **§12** before Code; no duplicate `docs/plans/` |
| `executing-plans` | Approved plan attach = valid plan source; verify per slice in chat |
| `using-git-worktrees` | **Skip** on assessment-only, `scope:light`, unless user asks |
| `caveman-review` | L2–L3: ~5 lines; security deep only on sensitive diff |
| `superpowers` | `skill-check-first` → note ide-aligned when supplement on |

---

## 12. Clarifying options (scope active only)

Mirror Cursor Plan UX: when **how** to build is ambiguous, offer labeled choices + escape hatch — **only** when `/question-scope` is on.

| Step | Rule |
| ---- | ---- |
| **When** | After `Level: Lx` header, during **Spec** or **Plan** (L2–L4), or open items in attached plan / Cursor Plan **before** confirm |
| **Not for** | Level pick (L1–L4), assessment-only gap reports, or fully specified AC |
| **Present** | **2–4** options; each label = name + one-line consequence |
| **Last option** | **`Other — I'll specify`** (always) |
| **STOP** | No Patch / new-contract Test / Code until user picks or supplies Other text |
| **Record** | One bullet per decision in Spec, plan delta, or `STATUS.md` |
| **Skip** | Message contains **`clarify:off`** — scope on; no §12 picker ([parsing-tokens.md](parsing-tokens.md)) |

**Full runtime:** [clarifying-options.md](clarifying-options.md) · vs level picker: [level-picker-runtime.md](level-picker-runtime.md).

**Host:** Cursor → `AskQuestion`; Kiro → numbered list + **STOP** (same labels).
