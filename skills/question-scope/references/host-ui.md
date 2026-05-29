# Host UI (all AI IDEs)

**One contract** for Cursor, Kiro, Windsurf, Copilot, JetBrains AI, Claude Code, and any other agent host. Hosts differ only in **whether a native multi-option picker tool exists** — not in Idea, option copy, or STOP gates.

**Rich confirmation shape (all hosts):** [confirmation-prompts.md](./confirmation-prompts.md).

---

## Universal minimum (every host — required)

Regardless of IDE, the agent **must**:

1. Emit structured **Idea** + **Suggest** + **full option labels** (`For this task:` when level pick).
2. **STOP** explicitly — no Spec / Patch / Code / `docs/work/` until the user picks.
3. Accept replies: `L2`, `choose L3`, `/question-scope L3 — …`, `1` / `2`, `A` / `B`, or **Other** text for §12.

**Chat-only presentation is always valid** (numbered list, markdown table, or bullets). Never skip STOP because the host has no picker tool.

---

## Structured choice UI (when the host provides it)

Some hosts expose a **multi-option picker** in the tool layer (examples — not exhaustive):

| Host (examples) | Tool (examples) |
| ---------------- | ----------------- |
| Cursor | `AskQuestion` |
| Others | Host-native “choose one” / multiple-choice UI if available |

**When available:**

| Use | Rule |
| --- | ---- |
| Level pick | 2 (gray) or 4 options; **full** string in each option **label** / title field |
| §12 clarifying | 2–4 options + **`Other — I'll specify`** as **last** option |
| Labels | Same text as chat fallback — user must read pipeline + **For this task:** without opening the skill |

**When unavailable:** use [Chat fallback](#chat-fallback-all-hosts) below — **same strings**, same STOP.

**Do not** assume only Cursor has a picker; **do not** require a picker tool in behavioral tests — require **full labels + STOP**.

---

## Chat fallback (all hosts)

Use when there is no structured picker, the tool errors, or the user is on a plain chat surface:

```text
Choose one:

1. **L2 — … · …** · **For this task:** …
2. **L3 — … · …** · **For this task:** …

STOP — reply `L2`, `L3`, or `/question-scope L3 — …`.
```

§12: `A`…`D` or `1`…`4` plus **`Other — I'll specify`**.

Optional: **If you pick | You get | You skip** table (especially gray zone) — works in every IDE.

---

## Level pick vs §12 (all hosts)

| Picker | Question | Same turn? |
| ------ | -------- | ---------- |
| **Level** (L1–L4) | How much ceremony? | **No** §12 in the same structured block |
| **§12** | How to build? | **After** `Level: Lx` header |

---

## Plan / attach (all hosts)

| Situation | Rule |
| --------- | ---- |
| User attached **approved plan** (`.plan.md`, PRD, host **Plan mode** output) | Spec/Plan satisfied — delta only; §12 only for TBD items |
| Host **Plan mode** (read-only plan step) | Equals **Plan** in pipeline; §12 on open items **before** user confirms plan → then Test (L3+) → Code |

“Plan mode” is the host’s read-only planning step — **not** Cursor-specific.

---

## Rules and skills (all hosts)

| Artifact | Load |
| -------- | ---- |
| Always-on | `question-scope`, `code-standards` (or repo equivalent rule IDs) |
| On demand | `@workflow` / Superpowers supplement |
| Skill ID | `question-scope` (`invoke-skill` where supported) |

After rule/skill sync in the AI Core repo: **reload the IDE window** or start a **new chat** (any host).
