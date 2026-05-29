# L3 — Phase 1: Define

**Canonical steps (this file):** Context (in `STATUS.md` or below), Spec, Plan — L3 has no separate Validate phase; assumptions / risks live here as bullets.

**Next phase (required for implement):** [`l3-02-build-prove.md`](l3-02-build-prove.md) — **Test** (`generate-test`, TC table, RED) → **STOP before production Code**. Full L3 pipeline: Context → Spec → Plan → [Scaffold] → **Test** → Code → … ([SKILL.md](../../../SKILL.md#pipelines-ui)).

## Level check (~30s) — is L3 right?

Complete **before** heavy Plan. See [gray-zones](../../../references/gray-zones.md).

### Could this be **L2** instead? (less ceremony)

If **all** are true → ask user [L2 vs L3](../../../references/gray-zones.md#gray-zone-level-pick-all-ai-ides) before continuing on L3:

- [ ] Extends **existing** route/module pattern only (no new package boundary)
- [ ] **≤ ~5 files**, **one** endpoint or narrow change
- [ ] **Single session** / single PR likely; scoped Verify is enough

User picks **L2** → stop L3 define; switch to [`l2-patch.md`](../l2/l2-patch.md) per skill escalation.

### Need **L4** instead?

If **any** is true → stop; [L3 vs L4 level pick](../../../references/gray-zones.md#gray-zone-level-pick-all-ai-ides) or `/question-scope L4`:

- [ ] **≥ 2** services/repos must coordinate release
- [ ] Cross-service **data migration** or shared auth platform
- [ ] Formal **Validate** (go/no-go) required before heavy design

**L3 OK** when L2 downgrade boxes are not all true **and** no L4 box is checked. Agent: note `Level check: L3 OK` in `STATUS.md` or below.

## Spec / acceptance criteria

### Open decisions (IDE-ALIGNED §12)

Resolve before **Plan** confirm / **Test** / **Code**. Format: [clarifying-options.md](../../../references/clarifying-options.md) · examples: [confirmation-prompts.md](../../../references/confirmation-prompts.md) § B.

| ID | Decision | Chosen |
| -- | -------- | ------ |
| D1 | … | … |

### Checklist

- [ ] Actors / boundaries clear
- [ ] Measurable outcomes
- [ ] Non-goals listed

### Given / When / Then (feature scenarios)

| ID | Given | When | Then |
| -- | ----- | ---- | ---- |
| S1 | … | … | … |
| S2 | … | … | … |

## Assumptions / out of scope

- …

## Plan

### Architecture (bounded)

- …

### Tasks

- [ ] …

### Plan checklist

- [ ] Each task has owner or order
- [ ] Dependencies between tasks noted
- [ ] Rollback idea sketched (even if rough)

## Open questions

- …

## Done when

- [ ] Every critical `Then` has a future test case ID reserved (e.g. TC-01) or linked
- [ ] Plan approved or frozen for this iteration
- [ ] `STATUS.md` updated → next phase **`l3-02`** — Test design before Code (do not implement production code in this file)
