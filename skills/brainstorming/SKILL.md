---
name: brainstorming
description: >
  Design + approved spec before Plan/Code. Standalone for new features or L3-L4 when
  scope active. Skip L2 patch, L1 explain, bugs. After approve → architect-plan or
  writing-plans. No code until approved.
---

# Brainstorming Ideas Into Designs

Turn ideas into **approved** designs and specs through dialogue — then hand off to planning skills. Rule ID: **`design-approval-gate`**.

**Announce when applying:** `Using brainstorming for <topic/slug>.`

**Stop when:** User explicitly approved the design/spec (or declined further design) — then **NEXT:** `architect-plan` or `writing-plans`; no production code before approval.

## Instruction precedence

1. System/developer constraints  
2. User request  
3. **`question-scope`** STOP gates and level (when active)  
4. This skill  

When **`question-scope`** is waiting for **L1–L4** choice → **do not** run brainstorming (no Spec/Plan/design gate yet).

## Invocation modes

See [COMPOSITION.md](../COMPOSITION.md) § Requires (hard). Skills **compose** unless noted in **Requires (hard)** below.

### Standalone

New feature or design — run this skill; save `docs/specs/…` per repo; no `/question-scope` required.

### With question-scope

**L3–L4** design gate before Plan; skip L2 default; **do not** run while scope waits for L1–L4 pick.

**When NOT (scope on):** IDE-ALIGNED §1 (plan/spec on disk), §3 (assessment-only), L2 default.

**Scope on + product fork:** Prefer **IDE-ALIGNED §12** (options + **Other**) once level is set; use this skill for open-ended design before Spec exists.

### Combines with (optional)

- `architect-plan` or `writing-plans` — after approve
- `orchestra-decision` — before, if idea still fuzzy

### Requires (hard)

- None for standalone; coordinated L3–L4 expects approved spec before Plan

**Instruction precedence:** User message → **`question-scope`** STOP if level not chosen → this skill ([CONVENTIONS.md](../CONVENTIONS.md) § Invocation modes).

### Composition (quick ref)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Follow [design-process.md](references/design-process.md) checklist + HARD-GATE | Treat **`orchestra-decision`** output as approved spec |
| User-approved spec in `docs/specs/…` before **`architect-plan`** / **`writing-plans`** | Production code before design approval |
| **L3–L4** design gate after level chosen | Run while scope **STOP** waits for L1–L4 |
| **NEXT:** `architect-plan` or `writing-plans` after approval | Skip user approve on L2 patches with clear AC (see When to use) |

Shared ✅/❌: [invocation-anti-patterns](../references/invocation-anti-patterns.md).

## When to use

| Situation | Run brainstorming? |
| --------- | -------------------- |
| **L3–L4** feature / behavior change (supplement default) | **Yes** — design gate before Plan |
| User already has **approved** spec/design on disk | **No** — link it; go to **`architect-plan`** / **`writing-plans`** |
| **`sp:off`** but L3–L4 and AC still fuzzy | **Lightweight OK** — spec in phase file only; skip Visual Companion unless UI |
| **Standalone** (no `/question-scope`) | **Yes** for new features; save `docs/specs/…` per repo convention |

## When NOT to use (do not invoke this skill)

| Situation | Use instead |
| --------- | ------------- |
| **`question-scope`** — Idea → suggest → **STOP** (no level yet) | Wait for L; optional **`orchestra-decision`** if idea is vague |
| **L1** explain / compare only | Answer in chat |
| **L2** patch, AC already clear in `l2-patch.md` | Spec bullets in phase file — **no** full brainstorming (supplement skips gate) |
| **Bug / defect** (L2+) | **`systematic-debugging`** — root cause in Spec/`STATUS.md` before Patch |
| **Meta / audit** (`qs:meta`, `audit:`) | Normal chat |
| **`quick:`** | Fast path — no L1–L4 pipeline |

**vs `orchestra-decision`:** Fuzzy problem **before** level pick → **`orchestra-decision`** first (fast direction). **After** L3–L4 is chosen and you need a **full approved spec** → this skill.

<HARD-GATE>
When **this skill is active**, do NOT invoke implementation skills, write production code, or scaffold until design is presented **and** the user approves the written spec.
</HARD-GATE>

**Scaled design:** Simple work still gets approval — a few sentences in chat + a short spec file is enough. That is not “skip brainstorming”; it is **minimal** brainstorming.

## Anti-Pattern: "This Is Too Simple To Need A Design"

Unexamined assumptions waste work even on small changes — **when this skill applies** (see tables above). Present design (brief if needed) and get approval. **L2 patches with clear AC are excluded** — do not force a `docs/specs/…` file for a one-line fix.

## Context (JIT)

- Explore **bounded** context first: relevant module, `README`, rules (**`code-standards`**), linked `@` paths.
- Under **question-scope**: **impacted module + 1-hop** — do not repo-wide search before scope is understood ([**question-scope**](../question-scope/SKILL.md#progressive-context-jit)).
- List paths you intend to read before opening many files in one turn.

## Design process (checklist, flow, visual companion)

Full detail: [references/design-process.md](references/design-process.md).

## Key Principles

- One question at a time · YAGNI · 2–3 approaches · incremental validation · flexible revision

## Visual Companion

Browser mockups/diagrams when **seeing** beats reading. **Skip offer** for non-UI work.

Offer in **one message only** (no combined questions). If declined, text-only.

Per question: browser for layout/mockup/diagram; terminal for concepts and tradeoffs.

Details: [references/visual-companion.md](references/visual-companion.md)
