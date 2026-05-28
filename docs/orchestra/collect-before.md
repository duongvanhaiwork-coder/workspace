# Collect before (orchestra Phase 3)

Use with **`skills/orchestra-decision`** — gather only enough context to pick quadrant + output shape. Stop when you can proceed without guessing.

## Checklist

| Item | Notes |
| ---- | ----- |
| **Task type** | ideation, decision, implementation, operations |
| **Default policy** | e.g. tutor vs direct answer; retention vs delete |
| **Hard blockers** | auth, permissions, compliance, required output format |
| **Latency / SLA** | only if it changes solution shape |

## Sources (priority)

1. User `@` paths
2. Repo `README`, config, `rules/cursor/*.mdc`
3. This folder (`INDEX.md`, this file)
4. Workspace manifest (e.g. `projects.json`) if multi-repo — skip if absent

## Stop condition

Quadrant (Q1–Q4), one-sentence goal, constraints, and expected artifact type are explicit — then run retrieval passes (default max 2) per the skill.
