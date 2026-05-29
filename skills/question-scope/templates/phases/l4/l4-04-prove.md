# L4 — Phase 4: Prove

**Canonical steps:** Verify, Review, Regression, Iterate

## Verify (smoke + commands)

Use **`verification-before-completion`** — log every command + output in tables below (not chat-only).

### Command log vs test cases

| TC ID | Given | When | Then | Command | Result |
| ----- | ----- | ---- | ---- | ------- | ------ |
| TC-01 | … | … | … | `…` | pass / fail |
| TC-02 | … | … | … | `…` | … |

### Verify checklist

- [ ] Every P0 TC executed once
- [ ] Failures copied to Iterate with TC ID

## Review (security + SOLID + perf)

Use **`caveman-review`** mindset — log terse findings here. **Formal pre-merge** (`requesting-code-review`) runs after prove Review when L4 supplement applies — before `l4-05-ship` git options.

- …

### Review checklist

- [ ] STRIDE / OWASP-style pass on new surface (short notes)
- [ ] SOLID / layering on diff
- [ ] Perf: N+1, timeouts, payload size

## Regression

**Phase Regression** (broader than Verify) — **`verification-before-completion`**: fresh run, log evidence.

**Scope (L4 default):** Each **impacted service** listed in `l4-01` § *analyze-impact / exploration notes* and/or `l4-02-define` plan — one row per service/suite below. **Not** full monorepo/org suite unless AC names it in phase MD.

- [ ] Regression targets trace to discover/plan impact list (or documented exception)

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

## PR feedback (incoming review comments)

Use **`receiving-code-review`** when PR reviewers comment — verify before implement; log here (see `l3-02` § PR feedback for table shape).

- [ ] Each round: link → fix → **`verification-before-completion`**

## Done when

- [ ] All P0 TC + regression rows pass or waived with owner + reason
- [ ] `STATUS.md` → **Phase 5**
