# Skills (canonical)

**Language:** All `SKILL.md` files and supporting docs under `skills/` are **English**, except **`question-scope/README.md` only** (Vietnamese human guide; that skill’s `examples/`, `references/`, `templates/` stay English). See [CONVENTIONS.md](CONVENTIONS.md) § Language.

**Directory layout (all skills):** [STRUCTURE.md](STRUCTURE.md) — `SKILL.md`, `prompts/`, `references/`, `templates/`, …

**Portable conventions:** [CONVENTIONS.md](CONVENTIONS.md) — skill IDs, handoffs, paths, canonical tools. **Handoff graph:** [SKILLS-REGISTRY.md](SKILLS-REGISTRY.md).

**Agent policy:** [../AGENTS.md](../AGENTS.md) · **Workflow rules:** load `@workflow` on demand · **Always-on:** `question-scope`, `code-standards` (+ stack rules by file type)

## Superpowers bundle (14 skills)

Process / discipline skills from obra/superpowers. **Entry:** `superpowers`. **Do not** use legacy `superpowers:<id>` plugin IDs in instructions — use `` `skill-id` `` and `**REQUIRES:**` / `**NEXT:**`.

| ID | Role |
| --- | --- |
| superpowers | Meta — invoke skills first |
| brainstorming | Design before code |
| writing-plans | Detailed implementation plan |
| using-git-worktrees | Isolated workspace |
| subagent-driven-development | Execute plan via subagents (ALT-A) |
| executing-plans | Execute plan inline (ALT-B) |
| dispatching-parallel-agents | Parallel independent tasks |
| test-driven-development | Test before implementation |
| systematic-debugging | Root cause before fix |
| verification-before-completion | Evidence before “done” |
| requesting-code-review / receiving-code-review | Review workflow |
| finishing-a-development-branch | Merge / PR / cleanup |
| writing-skills | Authoring skills |

## Team catalog (12 skills) + Superpowers (14) = 26 total

Skills are **not executed automatically** by the IDE; clusters below are **recommended groupings**, **typical order**, and **when to read** each skill so agents and humans pick the right playbook.

### AI Core (MCP — need `make health` + indexed project for graph tools; **analyze-impact** / **explain-code** document editor fallbacks when MCP is down)

**Typical order on a code change**

1. **explain-code** — Understand flow and ownership before editing (`get_context`, `search_code`).
2. **analyze-impact** — Before large rename/refactor: blast radius (`analyze_impact`).
3. **refactor-code** — Change structure while preserving behavior, small diff (after you understand / measured impact if needed).
4. **generate-test** — After behavior or contract changes: tests matching repo conventions.

**When to use (quick meaning)**

| #   | Skill              | Question it answers |
| --- | ------------------ | -------------------- |
| 1   | **explain-code**   | “How does this work?” / trace call flow |
| 2   | **analyze-impact** | “If I rename/touch this, what breaks?” |
| 3   | **refactor-code**  | “Clean up / split / reshape without changing spec” |
| 4   | **generate-test**  | “Lock the change in with real tests” |

**Flow mapping**: *read codebase* → *measure blast radius* → *safe edit* → *prove with tests*.

### Workflow

**Common flows (suggested order)**

| Flow | Suggested order |
| ---- | ---------------- |
| **Large feature / task** | **question-scope** L3/L4 + Superpowers supplement (default) — plan path: [superpowers-supplement § Plan path decision](question-scope/references/superpowers-supplement.md#plan-path-decision-l3l4) — or **architect-plan** alone if `sp:off` → **AI Core** / execute → **generate-test** → commit pair |
| **Scoped answer → patch → full delivery** | **question-scope** (L1→L4) + **Superpowers supplement** on L2–L4 (`question-scope` → `references/superpowers-supplement.md`; rule IDs via `@workflow`) |
| **Ambiguous design / SOP / prompt** | **orchestra-decision** (Q1–Q4 matrix, narrow before coding) — may run **before** `architect-plan` or **replace** the “frame the problem” step when the problem is fuzzy |
| **PR / diff review** | **caveman-review** (after you have a diff; independent of commit style) |
| **Commit** | Pick **one**: **commit-message** (LINKID + template) **or** **caveman-commit** (short Conventional) — see **Pairs** |

*These skills have **no one global step order** relative to each other — pick a row in **Common flows** for ordering, or combine as the task needs.*

| Skill                   | Meaning |
| ----------------------- | ------- |
| **architect-plan**      | Implementation plan before heavy coding |
| **question-scope**      | L1–L4 work levels + phase templates (Cursor + Kiro); human prompts: [question-scope/README.md](question-scope/README.md) (VI); `?`+keyword **tight match**; opt-out: `qs:off` / `no-scope` / `quick:` |
| **orchestra-decision**  | Decide design/process when inputs are still open |
| **caveman-review**      | Terse line-oriented review |
| **commit-message**      | Company commit + LINKID |
| **caveman-commit**      | Short `feat(scope):`-style commits |

### Communication

**Order**: not fixed — enable **caveman** for ultra-terse replies; use **cavecrew** when splitting roles (locate / build / review) across subagents.

| Skill        | Meaning |
| ------------ | ------- |
| **caveman**  | Terse communication mode + `/caveman-help` |
| **cavecrew** | When to delegate compressed context to subagents |

### Pairs

| Task                        | Skill            |
| --------------------------- | ---------------- |
| Company LINKID commit       | `commit-message` |
| Short `feat(scope):` commit | `caveman-commit` |
