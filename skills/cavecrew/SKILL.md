---
name: cavecrew
description: >
  When to delegate compressed subagents: use three **roles** — locate (read-only),
  build (surgical edit), review (diff audit). Map roles to whatever subagent names
  your environment provides (e.g. Cursor presets often called cavecrew-investigator,
  cavecrew-builder, cavecrew-reviewer). Output stays terse to save main-thread context.
  Triggers: "delegate to subagent", "use cavecrew", "spawn investigator/builder/reviewer",
  "save context", "compressed agent output".
---

Cavecrew = **three roles** with **compressed** tool output (caveman-style), so results injected into the main thread cost fewer tokens than long prose. Same jobs as generic “explore / edit / review” flows; names like `cavecrew-investigator` are **one possible preset mapping** in Cursor, not a universal product ID.

## Roles vs generic tools

| Role | Job | Typical Cursor preset name (if configured) |
|------|-----|----------------------------------------------|
| **Locate** | Find definitions, call sites, tests — read-only, file:line first | often `cavecrew-investigator` |
| **Build** | Surgical edit, ≤2 files, scope already clear | often `cavecrew-builder` |
| **Review** | Diff / branch / file bug pass, terse findings | often `cavecrew-reviewer` |

## When to use cavecrew vs alternatives

| Task | Use |
|---|---|
| Where is X defined / what calls Y / list uses of Z | **Locate** role (compressed) |
| Same but you want architecture commentary in prose | Generic explore / main thread |
| Surgical edit, ≤2 files, scope obvious | **Build** role |
| New feature / 3+ files / cross-cutting refactor | Main thread or your full “architect” agent |
| Review diff, branch, or file for bugs | **Review** role |
| Deep review with long rationale + alternatives | Dedicated verbose reviewer agent |
| One-line answer you already know | Main thread, no subagent |

Rule of thumb: **if you want ~1/3 the tokens in the tool result, use these roles (cavecrew-style). If you want prose, use vanilla.**

## Why this exists (the real win)

Subagent tool results are injected verbatim. A verbose explore that returns 2k tokens costs 2k tokens of main-context budget every time. A compressed **Locate** result might return ~700 tokens. Across many delegations that is the difference between context exhaustion and finishing the task.

## Output contracts (by role)

Main thread should parse these shapes regardless of preset label.

**Locate**
```
<Header>:
- path:line — `symbol` — short note
totals: <counts>.
```
Or `No match.` Always file-path-first, line-number-attached, backticked symbols. Safe to grep with `path:\d+`.

**Build**
```
<path:line-range> — <change ≤10 words>.
verified: <re-read OK | mismatch @ path:line>.
```
Or one of: `too-big.` / `needs-confirm.` / `ambiguous.` / `regressed.` (terminal first token).

**Review**
```
path:line: <emoji> <severity>: <problem>. <fix>.
totals: N🔴 N🟡 N🔵 N❓
```
Or `No issues.` Findings sorted file → line ascending.

## Chaining patterns

**Locate → build → verify** (most common):
1. **Locate** returns site list.
2. Main thread picks 1–2 sites, hands paths to **Build**.
3. **Review** audits the diff.

**Parallel scout** (broad investigation):
Spawn 2–3 **Locate** calls in one message (different angles: defs vs callers vs tests). Aggregate in main thread.

**Single-shot build** (site already known):
Skip locate. Hand exact path:line to **Build** directly.

## What NOT to do

- Don't use **Build** when you don't already know the file. Run **Locate** first or the main thread will waste tokens passing context.
- Don't chain **Locate → Build** for a 5-file refactor. Build should return `too-big.` — use main thread.
- Don't ask **Review** for "general feedback" — findings only, no architecture essay. Use a verbose reviewer for that.
- Don't expect prose. Output is structured; paraphrase for humans if needed.

## Auto-clarity (inherited)

Subagents drop caveman → normal English for security warnings, irreversible-action confirmations, and any output where fragment ambiguity could be misread. Resume caveman after.
