# L3 — Phase 3: Ship

**Canonical steps:** Refine (light), Document

**Order:** Complete **Refine** + **Rollout/Rollback** sections below (phase content) → then run **`finishing-a-development-branch`** (git menu: merge / PR / keep / discard; fresh verify). Do not skip this file and jump straight from execute to git Ship skill.

## Refine (no behavior change)

- …

### Refine checklist

- [ ] No new `Then` added (only clarity / naming / perf safe refactors)
- [ ] Lint / format on touched files

## Rollout — Given / When / Then (smoke after deploy)

| ID | Given | When | Then |
| -- | ----- | ---- | ---- |
| R1 | New version deployed to staging | Smoke user hits critical path | No 5xx on core APIs |
| R2 | … | … | … |

## Rollback

- Trigger: …
- Steps (max 3 bullets): …

## Final doc / links

- PR: …
- Related paths: …

## Ship checklist (`finishing-a-development-branch`)

- [ ] Tests green — **`verification-before-completion`** logged in `l3-02`
- [ ] **`finishing-a-development-branch`** run — user chose: merge | PR | keep | discard
- [ ] Worktree removed / branch state documented (if worktree was used)
- [ ] Rollout R1 satisfied or waived with owner sign-off
- [ ] Rollback steps tested or rehearsed on paper
- [ ] `STATUS.md` marked complete; summary filled
