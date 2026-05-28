# Agent instructions — AI Core workspace

Instructions for agents working in this repository or in repos under `projects/` with this workspace’s skills and rules linked.

## Workflow (default for non-trivial tasks)

1. **Question-scope** — infer or ask L1–L4; sticky until done. Triggers: `level Lx`, `/question-scope`, tight-match `?` + dev keyword. Opt-out scope: `qs:off`, `no-scope`, `quick:` (same effect). Opt-out Superpowers supplement only: `sp:off`, `no-sp`.
2. **Superpowers supplement** — default on L3–L4, minimal on L2. L3 execute default: **inline checkpoints (B)**; subagents (A) only with `writing-plans`. Opt-out: `sp:off` / `no-sp`. Do not use legacy plugin IDs `superpowers:<skill-id>`; use skill IDs and rule IDs in `rules/cursor/workflow.mdc` (gates defer to question-scope when scope is on).
3. **Code quality** — `rules/cursor/code-standards.mdc` and stack `*.mdc` by file type always apply.

Quick reference: [rules/QUICKSTART.md](rules/QUICKSTART.md) (English). Optional Vietnamese: [docs/WORKFLOW-QUICKSTART.md](docs/WORKFLOW-QUICKSTART.md).

## Documentation policy

### Where to write files

| Context | Location |
| ------- | -------- |
| Phased work (L2–L4), STATUS, blockers, commands run | `<target-repo>/docs/work/YYYY-MM-DD-<slug>/` |
| Optional Superpowers design spec | `<target-repo>/docs/specs/YYYY-MM-DD-<topic>-design.md` — link from work phase file |
| Optional Superpowers implementation plan (writing-plans) | `<target-repo>/docs/plans/YYYY-MM-DD-<feature>.md` — link from work folder |
| L1 optional archive | `<target-repo>/docs/answers/YYYY-MM-DD-<slug>.md` |

**`<target-repo>`** = the git repo you are changing (e.g. `projects/my-app/`), not `Workspace/docs/` unless the task is meta work on AI Core itself.

### Rules

- **One source of truth** per spec/plan: either content in `docs/work/…` phase markdown **or** a linked `docs/specs|plans/…` file — not both without cross-links.
- If `<target-repo>` has no `docs/` or policy forbids it: ask once, then use an existing doc root (`specs/`, `design/`, `notes/`) with the same `work/YYYY-MM-DD-<slug>/` shape (see skill **`question-scope`**).
- Do not create `docs/superpowers/` unless the team already standardised that tree; prefer `docs/specs/` and `docs/plans/` per `skills/CONVENTIONS.md`.

### Meta work on this workspace (skills, rules, MCP)

Use the same L2–L4 convention under **`Workspace/docs/work/…`** when the change spans multiple sessions; otherwise a single PR description may suffice for tiny L2 edits.

## Skills and rules layout

| Path | Role |
| ---- | ---- |
| `skills/` | Canonical skills (English; except `skills/question-scope/README.md` VI); layout: `skills/STRUCTURE.md`; edit here, then `make sync-ide` |
| `rules/cursor/` | Canonical Cursor rules |
| `rules/kiro/` | Generated from cursor — do not edit by hand |
| `~/.cursor/rules/`, `~/.cursor/skills/` | Symlinks after `make sync-ide` → this repo’s `rules/cursor/`, `skills/` |
| `~/.kiro/steering/`, `~/.kiro/skills/` | Same sync → `rules/kiro/`, `skills/` |

## User overrides

Explicit user message beats skills. Repo-specific overrides may be added below as the team grows.
