# Parsing and token patterns

Moved from `skills/question-scope/SKILL.md` (contract qs-2026-05-29.3).

### Parsing

Case-insensitive matching after trim unless noted. **Only** `/question-scope` forms activate this skill.

| Pattern | Activates scope? |
| ------- | ---------------- |
| **`/question-scope`** token | Yes → priority 2 (**level picker**: 2 labeled options if one gray pair fits, else 4) — only at **message start or end** (after trim); **not** mid-sentence |
| **`/question-scope L1`…`L4`** | Yes → priority 1 — same **start/end** placement; `/question-scope` + **whitespace** + `L1`…`L4` (`l2` → `L2`) |
| **`/question-scopeL1`…`L4`** (no space before `L`) | **No** preset level — priority 2 if at start/end. **Reply once:** `Detected /question-scopeL2 — use /question-scope L2` (substitute level digit) |
| **Mid-sentence** `/question-scope` (text before and after token) | **No** — put command at **start** or **end** (e.g. `/question-scope L2 — fix auth` or `fix auth /question-scope L2`) |
| **`level L1`…`L4`** (without `/question-scope`) | **No** — use `/question-scope Lx` |
| **`?` + keyword** | **No** |
| **`sp:off` / `no-sp`** | Does not activate scope by itself |
| **`qs:meta` / `audit:`** | **No** — explicit audit (same effect as meta below) |
| **Meta / audit** (see below) | **No** — normal chat or doc edit |


### Meta discussion (do not run scope)

Activate scope only when the user intends to **run** L1–L4 work on a **target repo**, not when they are **reviewing or editing** this skill or rules.

**Explicit audit tokens (recommended):** Message **starts with** `qs:meta` or `audit:` (or `(^|\s)qs:meta` / `(^|\s)audit:`) — scope **off** even if `/question-scope` appears in the same message. Prefer these over keyword-only meta when reviewing rules/skills.

**Meta wins over `/question-scope` in the same message** — do not activate when **any** signal below matches (path optional; EN/VI; diacritics optional):

- **Path:** `skills/question-scope`, `question-scope/SKILL.md`, `question-scope.mdc`, or repo path ending in `/question-scope/`
- **Audit / review (examples):** “check question-scope rules”, “đánh giá skill”, “đánh giá question-scope”, “đánh giá rule”, “kiểm tra lại rule”, “kiểm tra lại về rule”, “kiểm tra rule question-scope”, “rà soát skill”
- Discussing without running: “don’t use `/question-scope` for this”, “when does `/question-scope` apply?”
- **Quoting, teaching, or discussing** `/question-scope` **without intent to run** L1–L4 on a target repo (docs, audit, examples)
- Editing SKILL.md / `question-scope.mdc` unless the user also sends **`/question-scope Lx`** at **start or end** for that edit task

**Placement:** After trim, the `/question-scope` command must be at **message start** (`^/question-scope`) or **message end** (`/question-scope` or `/question-scope Lx` immediately before end). Mid-sentence tokens (text before and after on the same line) do **not** activate — ask user to move the command to start or end.

**Signals that scope should run:** `/question-scope` or `/question-scope Lx` at **start or end**, plus task on application code, AC, or `@` repo paths outside `skills/question-scope/`.

User may add **`qs:off`**, **`qs:meta`**, or **`audit:`** to be explicit. If ambiguous, ask once whether to run scope or answer in chat.

### Conflicting tokens

If the same message contains **both** a scope trigger (`/question-scope` or `/question-scope Lx`) **and** a scope opt-out (`qs:off`, `no-scope`, `quick:`, `qs:meta`, `audit:` per tables above):

- **Opt-out wins** — do **not** activate question-scope.
- **`/question-scope Lx` does not override** `qs:off`, `no-scope`, `quick:`, `qs:meta`, or `audit:` in the same message.

`sp:off` / `no-sp` with `/question-scope Lx` (and **no** scope opt-out): run question-scope at that level; supplement off per [supplement by level](references/superpowers-supplement.md#by-level).

**Product-repo parsers (optional):** If triggers are implemented in application code, mirror [references/pressure-scenarios.md](references/pressure-scenarios.md) and [examples/pressure-test-pilot.md](examples/pressure-test-pilot.md) in that repo — not under `skills/`.

**Vague idea (no problem statement):** Run **`orchestra-decision`** first, then return to scope options.

