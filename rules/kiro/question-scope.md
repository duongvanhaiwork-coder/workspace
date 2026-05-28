---
inclusion: always
---

# Question Scope

When the user message matches a trigger below, follow the **question-scope** skill (invoke-skill). **Canonical triggers, tight match, opt-outs, and pipelines** are in that skill’s `SKILL.md` — this file is a short reminder only.

## Triggers (skill runs)

- **`level L1` … `level L4`** or **`/question-scope`** / **`/question-scope L2`** (explicit level skips the options step; see skill).
- **`?` + dev keyword** (fix, add, explain, api, bug, test, …) **only with tight match** (see **When this skill applies** in **question-scope**): after trim, either the **first character** is `?`, or the **first alphanumeric token** is a dev keyword (case-insensitive). A keyword buried after a long sentence with only a trailing `?` does **not** activate.

## Not a trigger / opt-out

- **`?` alone** ("ok?", "done?") — normal reply.
- **Body contains** `qs:off`, `no-scope`, or `quick:` (case-insensitive) — do **not** activate question-scope (`quick:` = fast path, not “skip design only”; see skill **Opt-out tokens**).
- **Body contains** `sp:off` or `no-sp` — skip Superpowers supplement only (scope still applies).
- **`?` + keyword without tight match** — answer in chat; user may send `/question-scope` or `level Lx`.

## First actions

1. Short **Idea** (problem + outcome)
2. **Suggest** a level — user **must choose** L1–L4 (options); skip if level already set. **Gray zone (L2↔L3 or L3↔L4):** two-option `AskQuestion` only — do not default to the heavier level (see skill **Gray-zone AskQuestion**).
3. **STOP** until chosen — then run that level's pipeline and header `Level: Lx | Pipeline: …`
4. **L2–L4 long work:** create `docs/work/YYYY-MM-DD-<slug>/` (or `<doc-root>/work/...` per **question-scope**) with `STATUS.md` + phase templates from **`question-scope`** → `templates/phases/`

**Superpowers supplement (L3–L4 default, L2 minimal):** Rule IDs in `@workflow` or **`question-scope`** → `references/superpowers-supplement.md`. Opt out supplement: `sp:off` / `no-sp`.

**Human guide (Vietnamese):** **`question-scope`** → `README.md` — only VI file in that skill; agent contract is English (`SKILL.md`, `references/`). **Rules quickstart:** `rules/QUICKSTART.md`.

Kiro: same flow; present scope options as a numbered list if `AskQuestion` is unavailable.
