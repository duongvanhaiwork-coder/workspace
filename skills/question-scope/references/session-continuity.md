# Session continuity (L2–L4)

## Session continuity — phased `.md` files (L2–L4)

**Approach:** `docs/work/YYYY-MM-DD-<slug>/` with **`STATUS.md`** (read first in new sessions) + **one file per phase**. Files are source of truth for decisions, AC, commands, blockers.

**Doc root:** Prefer `docs/work/...`. If `docs/` is absent or forbidden: **ask once** or use `<doc-root>/work/...` (`specs/`, `design/`, `notes/`, …) with the same layout. L1 optional: `docs/answers/` or `<doc-root>/answers/`.

**Convention:** [templates/phases/README.md](templates/phases/README.md).

| Level | Files |
| ----- | ----- |
| L2 | `STATUS.md` + `l2-patch.md` ([l2](templates/phases/l2)) |
| L3 | `STATUS.md` + `l3-01` … `l3-03` ([l3](templates/phases/l3)) |
| L4 | `STATUS.md` + `l4-00` … `l4-05` ([l4](templates/phases/l4)) |

**Agent rules:**

1. After choosing L2–L4, create folder + templates; fill **`STATUS.md`** (`current_phase`, **5-line summary**, links, `next_actions`).
2. **End of each phase:** update phase file + `STATUS.md`; create next phase file **on entry** (default).
3. **New session:** `@` `STATUS.md` + current phase file — do not re-derive from chat alone.
4. L1: optional [answer.md](templates/phases/l1/answer.md); phased folder not required.
5. Tiny L2: single [rollup](templates/phases/rollup/work-item.md) allowed; use phased folder if multi-session.

