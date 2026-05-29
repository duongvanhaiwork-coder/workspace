# Progressive context (JIT)

Contract qs-2026-05-29.3. Load when expanding `@` files per level.

## Progressive context (JIT)

Add context **when the active pipeline step needs it**, not all at task start.

| Term | Meaning |
| ---- | ------- |
| **Symptom** | Problem statement in chat — **`@` not required** |
| **User-provided paths** | `@` attachments or paths in the message |

**Initial turn:**

| Level | Start with |
| ----- | ---------- |
| L1 | Symptom; `@` **0–2** files when answer needs code |
| L2 | Symptom + **0–1** primary `@`; **no** wide search before **Spec** |
| L3 | Symptom + AC; code `@` usually after **define** |
| L4 | Frame/discover; bounded impact after discover/validate |

**Expand** when Spec (L2+), Plan (L3+), or a gate shows a gap. Budgets are **ceilings per expansion**, not “read everything on step 1.”

| Level | Budget (max per expansion) |
| ----- | -------------------------- |
| L1    | 0–2 files, no wide search  |
| L2    | Impacted + 1-hop callers   |
| L3    | Module + API + tests + config |
| L4    | Wider; **`analyze-impact`** bounded |

**New session:** `@` `STATUS.md` + current phase file.

