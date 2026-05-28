# Question Scope — one-page cheat sheet (English)

Full contract: [SKILL.md](../SKILL.md). Vietnamese guide: [README.md](../README.md).

## Activate scope (only these)

| You want | Paste |
| -------- | ----- |
| Unsure of level | `/question-scope` + task → pick **L1–L4** (agent **STOP**s) |
| Known level | `/question-scope L2 — <task>` (L1/L3/L4) |
| Resume work | `@docs/work/.../STATUS.md` + `/question-scope L3 — continue` |

**Placement:** command at **start or end** of message — not mid-sentence.  
**Format:** `/question-scope L2` (space before `L`) — not `/question-scopeL2`.  
**Legacy (off):** `level L2 — …`, `?fix …` — use `/question-scope` instead.

## Turn scope off

| Token | Effect |
| ----- | ------ |
| `quick: <task>` | Fast path — no L1–L4, no `docs/work/` |
| `qs:off` / `no-scope` | Normal chat |
| `qs:meta — …` / `audit: — …` | Review skill/rules — no pipeline |
| Same message as `/question-scope Lx` | **Opt-out wins** |

`quick:` ≠ L2 with rollup MD → use `/question-scope L2 — … Rollup MD OK.`

## Levels (pick one)

| L | When | Code? |
| - | ---- | ----- |
| **L1** | Explain / compare only | No |
| **L2** | Patch, few files, clear AC | Yes |
| **L3** | Module, API, worker (bounded) | Yes + Regression + Ship |
| **L4** | Multi-service, large migration | Yes + 15-step flow |

**Gray zone:** agent asks **2 options** only (e.g. L2 vs L3 for export on existing API) — you must pick before work starts.

## Superpowers supplement (second layer)

| L | Default supplement |
| - | ------------------ |
| L1 | Off |
| L2 | TDD + verify (minimal) |
| L3–L4 | Worktree, TDD, inline execute (B), verify, ship |

Turn supplement off: `/question-scope L3 — <task>. sp:off`

## Common mistakes

| Wrong | Right |
| ----- | ----- |
| `Please /question-scope fix auth` | `/question-scope L2 — fix auth` or `fix auth /question-scope L2` |
| `quick:` but want L2 + rollup | `/question-scope L2 — … Rollup MD OK.` |
| `sp:off` alone | `/question-scope L3 — … sp:off` |
| New task, same chat, no new command | Send `/question-scope` or `/question-scope Ly` again |

## On disk (L2–L4)

```text
docs/work/YYYY-MM-DD-<slug>/
  STATUS.md          ← @ first in new session
  l2-patch.md        ← L2 (or rollup for tiny patches)
  l3-01-define.md …  ← L3
  l4-00-frame.md …   ← L4
```

## Stale Cursor rules?

After `make sync-ide`, only rules/skills install — **no scripts**. Reload window or new chat if chat shows old triggers (`level Lx`, `?` + keyword). In AI Core repo: `./scripts/check-question-scope-session.sh`.
