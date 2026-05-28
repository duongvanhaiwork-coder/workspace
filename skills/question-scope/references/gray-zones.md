# Gray-zone decisions (question-scope)

Load when **two levels both fit** and the user has not sent **`/question-scope L1`…`L4`**. Core gates stay in [SKILL.md](../SKILL.md).

## Rules

- **User picks** (or sends **`/question-scope Lx`** only — `level Lx` does not activate). **Suggest** must name the gray zone and tradeoff in one line.
- **Escalate** when work exceeds the chosen level — do not silently absorb L3 work inside L2.
- **Do not** default to the **heavier** level when a lighter one is plausible.

## L1 vs L2 (explain vs patch)

| Prefer **L1** when (most true) | Prefer **L2** when (any true) |
| ------------------------------ | ----------------------------- |
| User wants understanding, naming, or comparison only | User expects **code changes** or a fix in the repo |
| No acceptance criteria for implementation | Measurable AC, repro steps, or “make it work” |
| `@` files optional (0–2) for illustration | Symptom + likely paths; will need Spec/Patch |

If **both** fit (e.g. “explain then fix”), use **four options** or ask: **L1** (answer only now) vs **L2** (patch). Do not start Patch on L1.

## L2 vs L3 (e.g. “add one endpoint”)

### Quick checklist (L2 vs L3)

Answer for the **current** work item. If **any** is **yes** → prefer **L3** (or AskQuestion L2 vs L3). If **all no** → **L2** is appropriate (note in `STATUS.md` / `l2-patch.md` level check).

| # | Question |
| - | -------- |
| 1 | **New** top-level module, package, or folder boundary? |
| 2 | **New** worker, queue consumer, cron, or async pipeline? |
| 3 | Likely **> ~5 files** or **multi-session** / multi-PR? |
| 4 | **Multiple** endpoints, public contract doc, or API versioning? |
| 5 | Need full **Regression + Ship** / rollout notes (not scoped Verify only)? |

Human copy (Vietnamese): [README.md § Checklist L2 ↔ L3](../README.md#checklist-l2--l3-5-câu).

| Prefer **L2** when (most true) | Prefer **L3** when (any true) |
| ------------------------------ | ----------------------------- |
| Extends an **existing** route/module pattern (clone neighbor handler) | **New** module, package boundary, or top-level folder |
| Touch **≤ ~5 files** (route, service, test, config, i18n) | **New** worker, queue consumer, cron, or async pipeline |
| **One** endpoint or narrow contract change; no API versioning story | **Multiple** endpoints, public contract doc, or versioning |
| Single session / single PR likely | Likely **multi-session** or needs phased `l3-*` + Regression + Ship |
| User wants **less ceremony** (scoped Verify, no full regression gate) | User wants Plan, test-before-code gate, regression, rollout notes |

**Agent:** If suggesting L3 but user may want light touch, add: `Override: /question-scope L2 — same task, less ceremony.`

**Examples:**

- `POST /users/:id/avatar` next to existing user routes, same service → **L2**.
- New `notifications/` module + email + push interface → **L3**.

## L3 vs L4 (e.g. migration in one service vs many)

| Prefer **L3** when (most true) | Prefer **L4** when (any true) |
| ------------------------------ | ----------------------------- |
| **One** deployable (one repo/service) with clear module boundary | **Two or more** services/repos or teams must coordinate releases |
| Risks fit in **assumptions** bullets in `l3-01-define.md` | Needs formal **Validate** (go/no-go) before heavy design |
| Migration/flag rollback **inside one** codebase | Cross-service **data migration**, compat window, or shared auth platform |
| **`analyze-impact`** bounded to one service is enough | MCP / AI platform / org-wide infra / large auth overhaul |

**Examples:**

- Auth cookie → JWT in **api** only, feature flag, one repo → **L3** (risks in define).
- OIDC across **api + worker + admin**, shared session store migration → **L4**.

**L3 vs L4 Validate:** Bounded L3 folds validation into **Spec / assumptions** in `l3-01-define.md`. **L4** adds formal **Validate** in `l4-01-discover.md` before heavy design.

## L2 documentation (patch MD)

| Use | When |
| --- | ---- |
| **No** `docs/work/` | Trivial one-shot (typo, comment); optional |
| **Single rollup** [`rollup/work-item.md`](../templates/phases/rollup/work-item.md) | One session; ≤ ~3 files; AC + verify notes fit one page; no rollout |
| **`STATUS.md` + `l2-patch.md`** | Bug needs **root cause** trail; or task may **continue next session** |
| Phased folder (same files) | Team policy requires `STATUS.md` for all L2+ |

Rollup is **not** a different level — it is L2 with lighter MD.

## Gray-zone AskQuestion

When **both** levels in a pair above fit and the user has **not** sent **`/question-scope Lx`**:

- **Cursor:** `AskQuestion` with **exactly two** options (labels + one-line tradeoff each). **STOP** until the user picks.
- **Kiro / fallback:** numbered list of the same two options; accept `L2`, `choose L3`, etc.

| Gray pair | Option A | Option B |
| --------- | -------- | -------- |
| **L1 vs L2** | **L1** — Answer only; no repo edits | **L2** — Patch with Spec → Verify |
| **L2 vs L3** | **L2** — Patch: less ceremony; scoped Verify; rollup MD OK | **L3** — Small feature: Plan, test before code, Regression + Ship |
| **L3 vs L4** | **L3** — Bounded feature: one service/repo; risks in define | **L4** — Large system: multi-service; formal Validate before heavy design |

If **three or more** levels could fit, use the normal **four options** in [SKILL.md § Scope Level](../SKILL.md#scope-level--user-chooses-do-not-auto-lock) instead of a two-option question.

**After the user picks:** emit header `Level: Lx | Pipeline: …` and run that level only. Fill the **30-second level check** in [`l2-patch.md`](../templates/phases/l2/l2-patch.md) or [`l3-01-define.md`](../templates/phases/l3/l3-01-define.md) when creating those files.

**Not AskQuestion:** user already set **`/question-scope Lx`**; mid-task **escalation** — explain, re-present at least the higher adjacent pair, continue after confirm.
