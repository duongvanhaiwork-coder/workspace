# Example — bounded L3 plan in `l3-01-define.md`

Copy into **`docs/work/YYYY-MM-DD-<slug>/l3-01-define.md`** under **## Plan** (after **### Architecture (bounded)**). Link full spec: `docs/specs/YYYY-MM-DD-phone-validation-design.md`. Do **not** duplicate Given/When/Then here.

```markdown
### Architecture (bounded)

- Extend existing `PATCH /users/:id` validation; reuse `UserValidator` in `src/users/`.
- Phone: E.164 optional field; reject invalid format with 400 + field error (same envelope as email).

### Tasks

- [ ] T-1: `src/users/validator.ts` — add `phone` rule + unit tests — verify: `npm test -- validator`
- [ ] T-2: `src/users/routes.ts` — wire validator on PATCH — verify: `npm test -- routes/users`
- [ ] T-3: `openapi/users.yaml` — document optional `phone` — verify: `npm run lint:openapi`

### Plan checklist

- [ ] Order: T-1 → T-2 → T-3
- [ ] Rollback: revert route + validator if staging smoke fails

## Done when

- [ ] S1/S2 from Spec → TC-01, TC-02 reserved in `l3-02-build-prove.md`
- [ ] Plan frozen; `STATUS.md` → `l3-02-build-prove.md`
```

**Handoff:** **`executing-plans`** (B) on this phase file. Escalate to **`writing-plans`** only if **>12** tasks or **>8** primary files.
