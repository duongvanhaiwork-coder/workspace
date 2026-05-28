# Level playbooks (question-scope)

Load when executing a chosen level. Pipeline summary and gates: [SKILL.md](../SKILL.md). Phase file checklists: [templates/phases/](../templates/phases/).

## L1

- Context: user text + `@file` only; max **1–2 files**; no codebase-wide scan.
- **Answer** in chat; optional `docs/answers/YYYY-MM-DD-<slug>.md` ([template](../templates/phases/l1/answer.md)).
- No Spec, Patch, Verify suite, Regression.

## L2

Use [`l2-patch.md`](../templates/phases/l2/l2-patch.md) + `STATUS.md` (or [rollup](../templates/phases/rollup/work-item.md) for tiny patches).

- **Context (initial):** **Symptom** + **user-provided paths** (`@` or paths in message). No codebase-wide search before **Spec**.
- **Context (expand):** After **Spec** — impacted paths + callers **1 hop** ([context budgets](../SKILL.md#context-budgets)); list extra paths in Spec before opening file 3+ in one turn when practical.
- **Spec:** AC (bullets or Given/When/Then). **Bugs:** root cause before Patch ([Bug overlay](../SKILL.md#bug-overlay-any-level-with-a-defect)).
- **Test gate:** Behavior/contract changes → test cases in Spec **before Patch**. Pure refactor/rename → skip new tests.
- **Patch:** incremental edits; rule **`code-standards`** / stack rules in touched scope.
- **Verify:** impacted tests / smoke; not full-system regression.
- **Review:** [Review checklist](../SKILL.md#review-checklist-l2) + **`caveman-review`** mindset.
- **MD:** phased `docs/work/…` or single work-item per [gray-zones § L2 documentation](./gray-zones.md#l2-documentation-patch-md).

## L3

Use phased [`l3-*`](../templates/phases/l3/) + `STATUS.md`. **Regression** and **Ship** are required.

- Context: module boundary, API contract, tests dir, related config (usually after **define**).
- **Spec:** AC; assumptions / out of scope (3 bullets). **Bugs:** root cause in Spec or `STATUS.md` before Code.
- **Plan:** **`architect-plan`** in `l3-01-define.md` (default).
- **Scaffold** (if needed): after Plan, before Test.
- **Test** before **Code** — gate: test cases listed ([Gates](../SKILL.md#gates-at-a-glance)).
- **Code:** **`code-standards`** / stack rules.
- **Verify** → **Regression** → **Review**; on fail → **Iterate** → **Refine** → **Ship** (`l3-03-ship.md`).
- **Supplement:** [superpowers-supplement.md](./superpowers-supplement.md) (default L3).

## L4 — Full Flow (15 steps)

1. Idea · 2. Scope · 3. Context · 4. Validate · 5. Spec · 6. Plan · 7. Scaffold · 8. Test Design · 9. Implement · 10. Verify · 11. Review · 12. Regression · 13. Iterate · 14. Refine · 15. Document

Step **15. Document** = finalize phased MD + **Ship** in `l4-05-ship.md` (rollout, rollback, architecture/AI/delivery) — same intent as L3 **Ship**.

**If user already sent `level L4`:** steps **1–2 done** — start at **3. Context**. No second Idea/Scope ceremony.

Use `CreatePlan` + **`architect-plan`**. In Cursor plan mode, **extend** the existing plan file — no duplicate.

**Layers (when relevant):**

- **Architecture:** dependency graph, boundaries, scale, observability, security, deploy, rollback, cost.
- **AI:** token/memory, retrieval, embedding, chunking, caching.
- **Delivery:** rollout, migration, backward compatibility.

**MD:** phased [`l4-*`](../templates/phases/l4/); optional [rollup](../templates/phases/rollup/work-item.md) at end.

**Supplement:** [superpowers-supplement.md](./superpowers-supplement.md) (near-full L4).
