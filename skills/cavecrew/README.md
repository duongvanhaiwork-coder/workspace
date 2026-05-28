# cavecrew

Decision guide: when to delegate **compressed** subagent work (three **roles**: locate, build, review) instead of doing everything inline.

## What it does

Subagent tool results are injected into the main thread verbatim. Terse “caveman-style” output is roughly **smaller** than long prose, so repeated delegation burns less context.

| Role | Job | Use when |
|------|-----|----------|
| **Locate** | Read-only: definitions, callers, tests | “Where is X / what calls Y / list uses” |
| **Build** | Surgical edit, 1–2 files | Scope obvious; refuses large multi-file refactors |
| **Review** | Diff / file review | One-line findings with optional severity |

Your IDE may label these presets `cavecrew-investigator`, `cavecrew-builder`, `cavecrew-reviewer` — those names are **examples**, not requirements. Map by **role**.

Use a verbose explore/reviewer when you want prose and architecture commentary. Use the main thread for one-line answers and large refactors.

## How to invoke

Phrases like “delegate to subagent”, “use cavecrew”, “spawn investigator”, “save context”, “compressed agent output”.

## Example chaining

Locate → build → verify:

1. **Locate** returns `path:line — symbol — note` list  
2. Main thread picks 1–2 sites → **Build**  
3. **Review** on the resulting diff  

## See also

- [`SKILL.md`](./SKILL.md) — full matrix and output contracts  
