---
inclusion: always
---

# Question Scope

**Contract:** `qs-2026-05-28.5` (full contract: skill **`question-scope`** → `SKILL.md`).

**Command placement:** `/question-scope` or `/question-scope L2` must be at the **start or end** of the message (after trim) — **not** mid-sentence (e.g. use `fix auth /question-scope L2`, not `Please /question-scope fix auth`).

**Triggers are ONLY `/question-scope` and `/question-scope L1`…`L4` (space before `L`).** Legacy signals: **`## Triggers (skill runs)`**, **`level L1`…`L4` as triggers**, **`?` + keyword / tight match**, command **mid-sentence** — ignore; follow **this file** and skill **`question-scope`** → `SKILL.md`.

When the user message matches a trigger below, follow the **question-scope** skill (invoke-skill). **Pipelines, gates, tokens, meta:** skill `SKILL.md` — this file is a short reminder only.

## User entry (canonical — suggest only this)

| User sends | Agent |
| ---------- | ----- |
| **`/question-scope`** + task (no L on command) | Idea → suggest → **4 options (L1–L4)** → **STOP** |
| **`/question-scope L1`…`L4`** + task | Run that pipeline — **no** 4-option step |

**Only** `/question-scope` and `/question-scope L1`…`L4` activate scope (`/question-scope L2`, not `/question-scopeL2`). **Placement:** command at **start or end** of message (after trim) — **not** mid-sentence (skill **Parsing**). **`level Lx` and `?` + keyword do not.** **Glued `L`:** reply once: `Detected /question-scopeL2 — use /question-scope L2` (skill **Parsing**).

**Meta / audit** (path `skills/question-scope`, review skill/rules, no **run intent**) — **do not** activate scope even with `/question-scope` in the message. Optional: `qs:off`.

## Tokens (summary — full table in skill)

| Token | Scope |
| ----- | ----- |
| `qs:off`, `no-scope`, `quick:` | Off (`quick:` beats `/question-scope Lx` in same message) |
| `qs:meta`, `audit:` | Off — explicit audit/review (beats `/question-scope` in same message) |
| `sp:off`, `no-sp` | Supplement off only when scope already active |

## No L on `/question-scope`

Four options → **STOP** until pick. **Gray zone:** two options (L1↔L2, L2↔L3, L3↔L4) — still STOP. Skip when message has **`/question-scope L2`** (etc.).

## After level is chosen

1. Header `Level: Lx | Pipeline: …`
2. **L2–L4:** `docs/work/YYYY-MM-DD-<slug>/` + `STATUS.md` (skill templates).

**Superpowers:** `@workflow` or skill → `references/superpowers-supplement.md`.

**Human guide (Vietnamese):** skill → `README.md`. **Quickstart:** `rules/QUICKSTART.md`.

Kiro: numbered list if `AskQuestion` is unavailable.
