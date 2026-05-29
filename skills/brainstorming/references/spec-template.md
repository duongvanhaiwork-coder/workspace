# Spec template (brainstorming)

Copy into `docs/specs/YYYY-MM-DD-<topic>-design.md`. Omit empty sections. For **question-scope L3**, also mirror AC rows in `l3-01-define.md` (link here — do not duplicate long prose).

```markdown
# [Feature / topic] — Design spec

**Status:** Draft | Approved (date)
**Work folder:** `docs/work/YYYY-MM-DD-<slug>/` (if question-scope)

## Goal

[One sentence outcome]

## Non-goals

- …

## Actors & boundaries

- …

## Acceptance criteria

### Given / When / Then

| ID | Given | When | Then |
| -- | ----- | ---- | ---- |
| S1 | … | … | … |

*(L4: may use A1, A2… per phase template)*

## Architecture (bounded)

- Components, data flow, key interfaces

## Error handling & edge cases

- …

## Security & compliance (when applicable)

- AuthZ/tenant, PII, migration/rollback — or “N/A”

## Testing approach

- How each critical `Then` will be verified (observable; reserve **TC-xx** for L3 phase **Done when**)

## Risks & mitigations (only if real)

- …

## Open questions

- …
```

**Approved:** User explicitly approves in chat before **NEXT:** `architect-plan` or `writing-plans`.
