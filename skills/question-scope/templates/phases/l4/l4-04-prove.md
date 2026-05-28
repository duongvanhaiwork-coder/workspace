# L4 — Phase 4: Prove

**Canonical steps:** Verify, Review, Regression, Iterate

## Verify (smoke + commands)

### Command log vs test cases

| TC ID | Given | When | Then | Command | Result |
| ----- | ----- | ---- | ---- | ------- | ------ |
| TC-01 | … | … | … | `…` | pass / fail |
| TC-02 | … | … | … | `…` | … |

### Verify checklist

- [ ] Every P0 TC executed once
- [ ] Failures copied to Iterate with TC ID

## Review (security + SOLID + perf)

- …

### Review checklist

- [ ] STRIDE / OWASP-style pass on new surface (short notes)
- [ ] SOLID / layering on diff
- [ ] Perf: N+1, timeouts, payload size

## Regression

| TC ID | Suite / area | Given | When | Then | Result |
| ----- | ------------ | ----- | ---- | ---- | ------ |
| TC-10 | `npm test` | CI deps installed | Full unit suite | 0 failures | … |
| TC-11 | … | … | … | … | … |

### Regression checklist

- [ ] Impacted integration / e2e (if any) listed
- [ ] Flakes documented with rerun policy

## Iterate log

| Date | TC ID | Symptom | Fix | Retest |
| ---- | ----- | ------- | --- | ------ |
| … | TC-02 | … | … | pass |

## Done when

- [ ] All P0 TC + regression rows pass or waived with owner + reason
- [ ] `STATUS.md` → **Phase 5**
