# Phase templates — session continuity

**Why:** Long chats lose context. One **folder per work item** + **one file per phase** + **`STATUS.md`** = handoff surface for new sessions or compaction.

**Templates use:** **Given / When / Then** tables for scenarios + **fixed test case tables** (`TC ID`, `Given`, `When`, `Then`, `Type`) where tests apply. Fill or mark **N/A** — do not leave ambiguous blanks.

## Layout (agent creates under repo root)

**Default doc root:** `docs/`. If the repo forbids or omits `docs/`, use another agreed root (see main **question-scope** skill: `specs/work/...`, `notes/work/...`, etc.) — keep the same inner layout: `work/YYYY-MM-DD-<slug>/` + `STATUS.md` + phase files.

```text
docs/work/YYYY-MM-DD-<slug>/     # or <doc-root>/work/YYYY-MM-DD-<slug>/
  STATUS.md           ← always read first; current phase + 5-line summary + links
  l4-00-frame.md      ← L4 only (or l3-*, l2-* naming below)
  l4-01-discover.md
  ...
```

**Slug:** kebab-case, short (e.g. `mcp-indexing`).

## Which set to use

| Level | Templates (this folder) |
| ----- | ------------------------ |
| **L1** | [`l1/answer.md`](l1/answer.md) — optional archive to `docs/answers/`; no phased folder required |
| **L2** | `STATUS.md` + [`l2/l2-patch.md`](l2/l2-patch.md) **or** one-file [`rollup/work-item.md`](rollup/work-item.md) for tiny patches |
| **L3** | `STATUS.md` + `l3-01-define.md` … `l3-03-ship.md` in [`l3/`](l3/) |
| **L4** | `STATUS.md` + `l4-00-frame.md` … `l4-05-ship.md` in [`l4/`](l4/) |
| **Rollup** | [`rollup/work-item.md`](rollup/work-item.md) — single MD summary when not splitting by phase |

Copy from `templates/phases/` subfolders in this skill directory. Do not leave empty shells: create the **next** phase file when entering that phase (or create all at start with `TODO` — team choice; default = **create on entry**).

## Session handoff (agent + human)

1. End of turn: update **`STATUS.md`** (`current_phase`, `summary`, `blockers`, `next_actions`).
2. New session: `@docs/work/.../STATUS.md` + current phase file.
3. Never rely on chat alone for decisions already written — **re-read the phase file**.

## Map phases → canonical steps

| Phase | Name | Steps (canonical) |
| ----- | ---- | ------------------ |
| 0 | Frame | Idea, Scope |
| 1 | Discover | Context, Validate |
| 2 | Define | Spec, Plan |
| 3 | Build | Scaffold, Test Design, Implement |
| 4 | Prove | Verify, Review, Regression, Iterate |
| 5 | Ship | Refine, Document (+ Architecture / AI / Delivery in doc) |

**L3** maps to 3 files: `l3-01-define` (Context+Spec+Plan) → `l3-02-build-prove` (Test→Code→Verify→Regression→Review→Iterate) → `l3-03-ship` (Refine+rollout). **L2** = `l2-patch` + `STATUS` (or rollup). **L1** = optional `docs/answers/` only.
