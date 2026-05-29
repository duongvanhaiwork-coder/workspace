# question-scope — references

Load on demand (not every turn). **Naming:** kebab-case, one topic per file; see table below.

| File | When to read |
| ---- | ------------ |
| [CONTRACT-SYNC.md](./CONTRACT-SYNC.md) | Sync rule + skill when triggers/gates change — IDE sync: [README.md](../../../README.md) |
| [parsing-tokens.md](./parsing-tokens.md) | Parsing table, meta/audit, conflicting tokens, placement |
| [session-continuity.md](./session-continuity.md) | `docs/work/…`, `STATUS.md`, phase files (L2–L4) |
| [progressive-context-jit.md](./progressive-context-jit.md) | When to `@` files per level (JIT budgets) |
| [level-picker-runtime.md](./level-picker-runtime.md) | STOP, sticky scope, escalation (option copy in [level-picker.md](./level-picker.md)) |
| [gray-zones.md](./gray-zones.md) | L1/L2, L2/L3, L3/L4; **Quick checklist L2 vs L3**; AskQuestion pairs; L2 work-folder choice |
| [level-picker.md](./level-picker.md) | Trigger flow (mermaid) + host UI (Cursor vs Kiro) |
| [playbooks.md](./playbooks.md) | Step-by-step L1–L4 execution |
| **[pipelines-quickref.md](./pipelines-quickref.md)** | **Default during work** — skill chains by level (~120 lines); low token |
| [pipelines-skill-map.md](./pipelines-skill-map.md) | Full map — load **one § only** (level table or single §6 skill); §9 audit |
| [superpowers-supplement.md](./superpowers-supplement.md) | L2+ supplement, rule IDs, plan A/B |
| [pressure-scenarios.md](./pressure-scenarios.md) | Pressure scenarios + baseline results |
| [SIMULATION-RUN.md](./SIMULATION-RUN.md) | Full case-by-case sim — parsing #1–#24 + behavioral #1–#42 |
| [behavioral-gates.md](./behavioral-gates.md) | Behavioral fixtures + live-paste eval runbook |
| [behavioral-eval-fixtures.json](./behavioral-eval-fixtures.json) | Optional agent spot-check turns (schema v2) |
| [l3-vs-l4-diff.md](./l3-vs-l4-diff.md) | L3 vs L4 decision checklist + examples |
| [CHEATSHEET.md](./CHEATSHEET.md) | Human one-pager (English): triggers, tokens, levels |

**Human guide:** [README.md](../README.md) — **Lx-only workflow**, presets, anti-patterns, Regression. **One-pager:** [CHEATSHEET.md](./CHEATSHEET.md). **Prompt samples:** [examples/sample-prompts.md](../examples/sample-prompts.md). **Pressure test pilot:** [examples/pressure-test-pilot.md](../examples/pressure-test-pilot.md).

## Layout (skill root)

| Path | Role |
| ---- | ---- |
| `SKILL.md` | Agent contract (English) |
| `README.md` | Human guide (English) |
| `examples/sample-prompts.md` | Copy-paste prompts (English) |
| `references/*.md` | Deep dives (this folder) |
| `templates/phases/**` | Copy-out work files (`l2-patch.md`, `l3-01-define.md`, …) — **stable names** in target `docs/work/` |
