# L2 — Patch session

- **Work folder**: `docs/work/YYYY-MM-DD-<slug>/`
- **Pair with**: `STATUS.md` in same folder

## Level check (~30s) — is L2 enough?

Complete **before** deep Spec/Patch. If **any** box is checked → **stop**: do not patch on L2; run [gray-zone level pick](../../../references/gray-zones.md#gray-zone-level-pick-all-ai-ides) (L2 vs L3) or user sends `/question-scope L3`.

- [ ] **New** top-level module, package, or folder boundary
- [ ] **New** worker, queue consumer, cron, or async pipeline
- [ ] Likely **> ~5 files** or **multi-session** / multi-PR
- [ ] Needs full **Regression + Ship** / rollout doc (not scoped Verify only)

**All unchecked** → L2 is appropriate for this work item. Agent: note `Level check: L2 OK` in `STATUS.md` or below.

## Context collected

- [ ] Paths / symbols touched: …
- [ ] Callers (1 hop): …

## Spec / AC

### Open decisions (IDE-ALIGNED §12)

If **how** to build is ambiguous, agent **STOP**s with §12 shape (**Decision**, **Why it matters**, 2–4 options + **`Other — I'll specify`**) before Patch — [confirmation-prompts.md](../../../references/confirmation-prompts.md) § B. Record chosen options here:

| ID | Decision | Chosen |
| -- | -------- | ------ |
| D1 | … | … |

### Checklist (high level)

- [ ] Problem stated
- [ ] Success criteria measurable
- [ ] Out of scope noted (if any)

### Given / When / Then (scenarios)

| ID | Given | When | Then |
| -- | ----- | ---- | ---- |
| S1 | User authenticated; `Order` exists | `PATCH /orders/:id` with valid body | `200` + body matches schema |
| S2 | Invalid payload | Same request | `400` + validation errors |
| S3 | … | … | … |

## Test cases (before patch — if behavior changes)

Author with **`generate-test`** or by hand. **During Patch:** **`test-driven-development`** (RED→GREEN) per change. Pure rename/refactor → skip new tests; verify only.

| TC ID | Given | When | Then | Type |
| ----- | ----- | ---- | ---- | ---- |
| TC-01 | … | … | … | happy |
| TC-02 | … | … | … | error |
| TC-03 | … | … | … | edge |

**Checklist**

- [ ] Every `Then` in Spec maps to ≥1 row above (or marked N/A)
- [ ] At least one **error** path if inputs exist

## Patch notes

- Files changed: …
- Key edits: …

## Verify

Use **`verification-before-completion`** — scoped tests/smoke for patch + 1-hop (not full monorepo unless AC says so). Log **command + output** before claiming pass or Done.

| Command | Result |
| ------- | ------ |
| … | … |

## Review (security + SOLID)

- [ ] Input / authZ / secrets / queries (see skill checklist)
- [ ] SOLID quick pass on diff

## Done

- [ ] AC met (all `Then` checked)
- [ ] Tests above executed or explicitly N/A
- [ ] `STATUS.md` updated for handoff
