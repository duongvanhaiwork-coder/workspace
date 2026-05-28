# question-scope — references

Load on demand (not every turn). **Naming:** kebab-case, one topic per file; see table below.

| File | When to read |
| ---- | ------------ |
| [gray-zones.md](./gray-zones.md) | L1/L2, L2/L3, L3/L4; **Quick checklist L2 vs L3**; AskQuestion pairs; L2 work-folder choice |
| [level-picker.md](./level-picker.md) | Trigger flow (mermaid) + host UI (Cursor vs Kiro) |
| [playbooks.md](./playbooks.md) | Step-by-step L1–L4 execution |
| [superpowers-supplement.md](./superpowers-supplement.md) | L2+ supplement, rule IDs, plan A/B |
| [pressure-scenarios.md](./pressure-scenarios.md) | Pressure scenarios + baseline results |
| [behavioral-gates.md](./behavioral-gates.md) | Behavioral fixtures + live-paste eval runbook |
| [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json) | Optional agent spot-check turns (schema v2) |
| [l3-vs-l4-diff.md](./l3-vs-l4-diff.md) | L3 vs L4 decision checklist + examples |
| [CHEATSHEET.md](./CHEATSHEET.md) | Human one-pager (English): triggers, tokens, levels |

**Vietnamese (this skill only):** [README.md](../README.md) — presets, anti-patterns, Regression. **English one-pager:** [CHEATSHEET.md](./CHEATSHEET.md). **English prompt samples:** [examples/sample-prompts.md](../examples/sample-prompts.md). **Pressure test pilot:** [examples/pressure-test-pilot.md](../examples/pressure-test-pilot.md).

## Layout (skill root)

| Path | Role |
| ---- | ---- |
| `SKILL.md` | Agent contract (English) |
| `README.md` | Human guide (Vietnamese only) |
| `examples/sample-prompts.md` | Copy-paste prompts (English) |
| `references/*.md` | Deep dives (this folder) |
| `templates/phases/**` | Copy-out work files (`l2-patch.md`, `l3-01-define.md`, …) — **stable names** in target `docs/work/` |
