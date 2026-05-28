# Question Scope — sample prompts (English)

Copy-paste into chat. Replace `<description>`, `@path`, date/slug. Agent contract: [SKILL.md](../SKILL.md).

## Quick reference

| Situation | Paste into chat |
| --------- | ---------------- |
| One-line fix, no L1–L4 | `quick: <description>` |
| Patch / bug, few files | `level L2 — <description> (@file)` |
| New bounded feature | `level L3 — <description>` |
| Multi-service / migration | `level L4 — <description>` |
| Explain only, no code | `level L1 — <question>` |
| Unsure which level | `/question-scope` + task description |
| Know level, shortcut | `/question-scope L2` + description |
| Disable scope ceremony | `qs:off — <description>` |
| L3/L4 without SP supplement | `level L3 — <description>. sp:off` |
| Resume session | `@docs/work/.../STATUS.md` + phase file + `continue level L3` |
| `?` tight match | `?fix <description>` or `fix <description>?` |

## `quick:` — no scope

```text
quick: fix typo "teh" → "the" in README.md
```

```text
quick: remove unused import in @src/utils/date.ts
```

## `level L1`

```text
level L1 — explain login flow from @src/auth/login.ts to session cookie.
```

```text
?explain why auth middleware runs before validator (@src/middleware/auth.ts)
```

## `level L2`

```text
level L2 — fix: API returns 400 when phone field missing (@src/routes/user.ts).
```

```text
level L2 — bug: UserService.create test fails after schema change (@tests/user.service.test.ts @src/services/user.ts).
```

```text
/fix typo in 404 error message (@src/i18n/en.json)
```

## `level L3`

```text
level L3 — add GET /orders/export CSV with date and status filters.

AC: auth required; max 10k rows; Content-Type text/csv.
docs/work/2026-05-22-order-export/ + STATUS + l3 phases.
```

```text
level L3 — worker sends payment reminder email after 24h, idempotent by orderId.

sp:off — plan in l3-01-define, no writing-plans/worktree.
```

## `level L4`

```text
level L4 — migrate auth from session cookie to OIDC (api, worker, admin).

Two-week backward compatibility; rollout + rollback in docs/work/.
```

## `/question-scope`

```text
/question-scope

Need product image upload max 5MB, store on S3, public URL with 7-day TTL.
```

After agent shows 4 options: `L3` or `level L3 — continue as described above.`

## Opt-out & session

```text
qs:off — review PR #42 diff, focus on security and SQL injection.
```

```text
level L3 — product tags CRUD. sp:off — architect-plan in docs/work/, no worktree.
```

```text
@docs/work/2026-05-22-order-export/STATUS.md
@docs/work/2026-05-22-order-export/l3-02-build-prove.md

level L3 — continue from Build phase.
```

## Bug (L2)

```text
level L2 — bug: submit form returns 500 when email already exists (@api/register.ts).
```
