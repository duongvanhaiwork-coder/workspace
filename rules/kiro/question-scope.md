---
inclusion: always
---

# Question Scope

**Contract:** `qs-2026-05-29.2` (full contract: skill **`question-scope`** → `SKILL.md`).

**Command placement:** `/question-scope` or `/question-scope L2` must be at the **start or end** of the message (after trim) — **not** mid-sentence (e.g. use `fix auth /question-scope L2`, not `Please /question-scope fix auth`).

**Triggers are ONLY `/question-scope` and `/question-scope L1`…`L4` (space before `L`).** Legacy signals: **`## Triggers (skill runs)`**, **`level L1`…`L4` as triggers**, **`?` + keyword / tight match**, command **mid-sentence** — ignore; follow **this file** and skill **`question-scope`** → `SKILL.md`.

When the user message matches a trigger below, follow the **question-scope** skill (invoke-skill). **Pipelines, gates, tokens, meta:** skill `SKILL.md` — this file is a short reminder only.

## Default (no trigger)

No `/question-scope` at **message start or end** (after trim) → **normal chat** (answer or edit as the user asked).

- **Do not** infer L1–L4 from task size, file count, or “sounds like L3”.
- **Do not** create `docs/work/…` or run phased pipelines unless the user chose scope (`/question-scope` / `/question-scope Lx`) or explicitly asked for phased docs.

## Precedence

1. Explicit **user message** (including opt-out tokens)
2. Repo **`AGENTS.md`** (when present)
3. **This rule** + skill **`question-scope`** (STOP gates, level, `docs/work/…`)
4. **`code-standards.mdc`** and stack rules by file type
5. **`@workflow`** / Superpowers supplement — only when scope is active or user loads workflow

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

Four options → **STOP** until pick. Each option **must** include what that L does (pipeline note in `AskQuestion` label / numbered list) — skill `references/level-picker.md` § Option copy. **Gray zone:** two labeled options — still STOP. Skip when message has **`/question-scope L2`** (etc.).

## After level is chosen

1. Header `Level: Lx | Pipeline: …`
2. **L2–L4:** `docs/work/YYYY-MM-DD-<slug>/` + `STATUS.md` (skill templates).

**Superpowers:** `@workflow` or skill → `references/superpowers-supplement.md`.

**Human guide (Vietnamese):** skill → `README.md`. **Quickstart:** `rules/QUICKSTART.md`.

Kiro: numbered list if `AskQuestion` is unavailable.
