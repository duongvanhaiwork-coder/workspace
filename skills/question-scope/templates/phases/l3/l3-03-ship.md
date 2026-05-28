# L3 — Phase 3: Ship

**Canonical steps:** Refine (light), Document

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

## Ship checklist

- [ ] Rollout R1 satisfied or waived with owner sign-off
- [ ] Rollback steps tested or rehearsed on paper
- [ ] `STATUS.md` marked complete; summary filled
