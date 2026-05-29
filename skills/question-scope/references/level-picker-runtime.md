# Level picker runtime rules

Option copy: [level-picker.md](level-picker.md).

### Level picker (one rule)

After **Idea** + **Suggest**, present options and **STOP** — do **not** run Context / Spec / Patch / Code until the user picks **one** level:

| Situation | Present | Host UI |
| --------- | ------- | ------- |
| User sent **`/question-scope L1`…`L4`** (preset) | **Skip** picker — run that pipeline | — |
| **Only one gray pair** fits ([gray-zones](references/gray-zones.md)) | **Exactly two** adjacent options (e.g. L2 vs L3) | Cursor: `AskQuestion` (2); Kiro: numbered list |
| **Three or more** levels plausible, or still unclear | **Four** options (table above) | Cursor: `AskQuestion` (4); Kiro: numbered list |

### Option copy (required)

Each option the user sees must include **what that L will do** (pipeline + code? + `docs/work/`), not bare `L1`…`L4`.

- **Canonical strings:** [references/level-picker.md § Option copy](references/level-picker.md#option-copy-required--user-must-read-before-pick) (4-option table + gray pairs).
- **Cursor:** `AskQuestion` — put the full `Lx — … · …` string in each option **`label`**.
- **Kiro / fallback:** numbered list or table with the **same** labels; then **STOP**.

**Examples:** `Add GET /users/export CSV` on an **existing** users API → **L2 vs L3 only** (two labeled options, not four). Greenfield multi-service platform → **four** labeled options.

Accept: `L2`, `choose L3`, `/question-scope L3`, etc.

**Sticky scope:** Keep chosen level for the **same work item** until done or user sends `/question-scope` / `/question-scope Ly`. Do **not** re-present the four-option picker mid-task. **New unrelated task** in the same chat → user must send `/question-scope` or `/question-scope Ly` again — do not carry over the previous level.

**Escalation:** Work exceeds level → stop; re-present options (at least adjacent pair); continue after confirm.

### Task kind (same level, different pipeline)

| User intent | After level is set | Do not run |
| ----------- | ------------------ | ---------- |
| **Implement** (fix, add, patch, build) | Full pipeline for L | — |
| **Assessment** (gap, “need changes?”, review vs plan, compare) | Context → **Assessment** → Answer | Plan/Test/Code/Regression until user asks to implement |

Assessment keeps **sticky L** — do not re-show the four-option picker. See [ide-aligned-practices.md](ide-aligned-practices.md) §3.

### Clarifying options (not level picker)

After the user picks **L1–L4**, ambiguous **how** decisions (API shape, UX, config) use **IDE-ALIGNED §12** — [clarifying-options.md](clarifying-options.md). **2–4** technical options + **`Other — I'll specify`**; **STOP** before Patch/Code. Do **not** mix level pick (L2 vs L3) with §12 in one `AskQuestion` block.

### Suggest heuristic (not a decision)

| Signal                                   | Suggest |
| ---------------------------------------- | ------- |
| No code change, explain/compare          | L1      |
| Specific files, fix/field/validation     | L2      |
| New module/API/worker/migration          | L3      |
| Multi-service, MCP, AI infra, large auth | L4      |

