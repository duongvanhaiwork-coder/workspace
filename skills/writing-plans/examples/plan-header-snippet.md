# Example — `docs/plans/` header + one task

Use when pre-flight requires **`writing-plans`** (large handoff or subagents). Replace bracketed fields. Match repo test runner and commit policy.

```markdown
# Phone validation on PATCH /users Implementation Plan

> **For agentic workers:** **REQUIRES (pick one):** `executing-plans` (**default** under question-scope L3–L4) **or** `subagent-driven-development` (subagents per task). Checkbox (`- [ ]`) steps.

**Goal:** Add optional E.164 `phone` to user PATCH with validation and OpenAPI docs.

**Spec:** `docs/work/2026-05-29-phone-validation/l3-01-define.md` § Spec; design: `docs/specs/2026-05-29-phone-validation-design.md`

**Work phase:** `docs/work/2026-05-29-phone-validation/STATUS.md`

**Architecture:** Reuse `UserValidator`; extend PATCH handler only; no new module boundary.

**Tech stack:** Node 20, Express, Jest, OpenAPI 3.1

---

### Task 1: Validator — phone rule

**Traces:** S1, TC-01

**Files:**
- Modify: `src/users/validator.ts`
- Test: `tests/users/validator.test.ts`

- [ ] **Step 1: Write the failing test**

```typescript
it('rejects invalid phone format', () => {
  expect(validateUserPatch({ phone: 'not-a-phone' }).ok).toBe(false);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test -- tests/users/validator.test.ts -t "invalid phone"`
Expected: FAIL — `validateUserPatch` undefined or validation missing

- [ ] **Step 3: Write minimal implementation**

Add `phone` optional E.164 check in `validateUserPatch` (see spec for regex).

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test -- tests/users/validator.test.ts -t "invalid phone"`
Expected: PASS

- [ ] **Step 5: Ready to commit (human)**

```bash
git add src/users/validator.ts tests/users/validator.test.ts
# git commit -m "feat(users): validate optional phone on patch"
```
```

**After file is complete:** optional review via `prompts/plan-document-reviewer-prompt.md` → **NEXT:** `executing-plans` or `subagent-driven-development`.
