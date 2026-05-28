# L3 — Phase 2: Build + Prove

**Canonical steps:** Scaffold (if needed), Test Design, Implement, Verify, Review, Regression (required for L3), Iterate

## Test design (before code — STOP without this table filled)

| TC ID | Given | When | Then | Type |
| ----- | ----- | ---- | ---- | ---- |
| TC-01 | … | … | … | happy |
| TC-02 | … | … | … | error |
| TC-03 | … | … | … | edge |

### Test design checklist

- [ ] Maps to Spec `Then` rows from `l3-01-define.md`
- [ ] Includes ≥1 error path if user/system can send bad input
- [ ] IDs stable (do not renumber mid-flight; append TC-04…)

## Scaffold (if any)

- [ ] New paths listed
- [ ] …

## Implementation log

- …

### Implementation checklist

- [ ] Each TC-XX traceable to code / test file
- [ ] No behavior change without updating TC table above

## Verify + regression

### Execution vs test cases

| TC ID | Command / step | Result | Log / link |
| ----- | ---------------- | ------ | ---------- |
| TC-01 | `npm test -- foo` | pass / fail | … |
| TC-02 | … | … | … |

## Review notes

- …

### Review checklist

- [ ] Security + SOLID (skill)
- [ ] Each failed TC has ticket in Iterate below

## Iterate log (if failures)

| Date | TC ID | Symptom | Fix |
| ---- | ----- | ------- | --- |
| … | TC-02 | … | … |

## Done when

- [ ] All P0 TC rows show pass (or accepted waiver with reason)
- [ ] `STATUS.md` updated → next file `l3-03-ship.md`
