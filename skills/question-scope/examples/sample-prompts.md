# Question Scope — sample prompts (English)

Copy-paste into chat. Replace `<description>`, `@path`, date/slug. Agent contract: [SKILL.md](../SKILL.md).

## Quick reference

| Situation | Paste into chat |
| --------- | ---------------- |
| One-line fix, no L1–L4 | `quick: <description>` |
| Patch / bug, few files | `/question-scope L2 — <description> (@file)` |
| New bounded feature | `/question-scope L3 — <description>` |
| Multi-service / migration | `/question-scope L4 — <description>` |
| Explain only, no code | `/question-scope L1 — <question>` |
| Unsure which level | `/question-scope` + task description → pick L1–L4 |
| Disable scope ceremony | `qs:off — <description>` |
| Audit/review skill or rules | `qs:meta — <description>` or `audit: — <description>` |
| L3/L4 without SP supplement | `/question-scope L3 — <description>. sp:off` |
| Resume session | `@docs/work/.../STATUS.md` + `/question-scope L3 — continue` (command at **start** or **end** of message) |

## Presets

Full table + anti-patterns: [README.md § Presets & anti-patterns](../README.md#presets-and-anti-patterns).

| Preset | When | Paste |
| ------ | ---- | ----- |
| Fast | Typo / one line | `quick: <description>` |
| Explain | No repo edits | `/question-scope L1 — <question>` |
| Patch | Few files, clear AC | `/question-scope L2 — <description> (@file)` |
| Patch light | L2, minimal MD | `/question-scope L2 — <description>. Rollup MD OK.` |
| Feature | Bounded module/API + AC | `/question-scope L3 — <description>` + AC; `docs/work/YYYY-MM-DD-<slug>/` |
| Feature (less SP) | L3 without full supplement | `/question-scope L3 — <description>. sp:off` |
| System | Multi-service / large migration | `/question-scope L4 — <description>` |
| Pick level | Unsure L1–L4 | `/question-scope` + description (no L on command) |

**Anti-patterns:** no `/question-scope` in message (scope off); `level L2 — …` without `/question-scope` (scope off); `/question-scope L2` + `quick:` same message (opt-out wins); `quick:` when you want L2 + rollup MD (use `/question-scope L2 — … Rollup MD OK.`); `sp:off` alone; `?fix` without `/question-scope`; `/question-scopeL2` (no space before L); meta audit — prefer `qs:meta — …` or `audit: — …`.

**L2 vs L3 (5 questions):** any **yes** → lean L3 — see [gray-zones.md § Quick checklist](../references/gray-zones.md#quick-checklist-l2-vs-l3).

**Regression:** L3 = tests for touched **module/package** + **1-hop** integration on changed API; log commands in phase MD. L2 = scoped Verify only. Canonical: [SKILL.md § Pipelines](../SKILL.md#pipelines-ui).

## `quick:` — no scope

```text
quick: fix typo "teh" → "the" in README.md
```

```text
quick: remove unused import in @src/utils/date.ts
```

## `/question-scope L1`

```text
/question-scope L1 — explain login flow from @src/auth/login.ts to session cookie.
```

```text
?explain why auth middleware runs before validator (@src/middleware/auth.ts)
```

## `/question-scope L2`

```text
/question-scope L2 — fix: API returns 400 when phone field missing (@src/routes/user.ts).
```

```text
/question-scope L2 — bug: UserService.create test fails after schema change (@tests/user.service.test.ts @src/services/user.ts).
```

```text
/fix typo in 404 error message (@src/i18n/en.json)
```

## `/question-scope L3`

```text
/question-scope L3 — add GET /orders/export CSV with date and status filters.

AC: auth required; max 10k rows; Content-Type text/csv.
docs/work/2026-05-22-order-export/ + STATUS + l3 phases.
```

```text
/question-scope L3 — worker sends payment reminder email after 24h, idempotent by orderId.

sp:off — plan in l3-01-define, no writing-plans/worktree.
```

## `/question-scope L4`

```text
/question-scope L4 — migrate auth from session cookie to OIDC (api, worker, admin).

Two-week backward compatibility; rollout + rollback in docs/work/.
```

## `/question-scope`

```text
/question-scope

Need product image upload max 5MB, store on S3, public URL with 7-day TTL.
```

After agent runs level picker (2 or 4 labeled options): `L3` or `/question-scope L3 — continue as described above.`

## Opt-out & session

```text
qs:off — review PR #42 diff, focus on security and SQL injection.
```

```text
/question-scope L3 — product tags CRUD. sp:off — architect-plan in docs/work/, no worktree.
```

```text
@docs/work/2026-05-22-order-export/STATUS.md
@docs/work/2026-05-22-order-export/l3-02-build-prove.md

/question-scope L3 — continue from Build phase.
```

## Bug (L2)

```text
/question-scope L2 — bug: submit form returns 500 when email already exists (@api/register.ts).
```
