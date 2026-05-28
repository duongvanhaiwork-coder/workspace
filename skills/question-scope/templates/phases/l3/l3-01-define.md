# L3 — Phase 1: Define

**Canonical steps:** Context (in `STATUS.md` or below), Spec, Plan — L3 has no separate Validate phase; assumptions / risks live here as bullets

## Level check (~30s) — is L3 right?

Complete **before** heavy Plan. See [gray-zones](../../../references/gray-zones.md).

### Could this be **L2** instead? (less ceremony)

If **all** are true → ask user [L2 vs L3](../../../references/gray-zones.md#gray-zone-askquestion) before continuing on L3:

- [ ] Extends **existing** route/module pattern only (no new package boundary)
- [ ] **≤ ~5 files**, **one** endpoint or narrow change
- [ ] **Single session** / single PR likely; scoped Verify is enough

User picks **L2** → stop L3 define; switch to [`l2-patch.md`](../l2/l2-patch.md) per skill escalation.

### Need **L4** instead?

If **any** is true → stop; [L3 vs L4 AskQuestion](../../../references/gray-zones.md#gray-zone-askquestion) or `level L4`:

- [ ] **≥ 2** services/repos must coordinate release
- [ ] Cross-service **data migration** or shared auth platform
- [ ] Formal **Validate** (go/no-go) required before heavy design

**L3 OK** when L2 downgrade boxes are not all true **and** no L4 box is checked. Agent: note `Level check: L3 OK` in `STATUS.md` or below.

## Spec / acceptance criteria

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
- [ ] `STATUS.md` updated → next file `l3-02-build-prove.md`
