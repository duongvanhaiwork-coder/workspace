# L4 — Phase 1: Discover

**Canonical steps:** Context, Validate

## Context collected

- Repos / modules: …
- Key files / entrypoints: …
- Constraints (perf, compliance): …

### Context checklist

- [ ] Unknowns listed explicitly
- [ ] `analyze-impact` or equivalent run if blast radius unclear

## Validate (stakeholder / worth doing)

- Who needs this?
- Risks if we do not ship / ship wrong?
- **Go / no-go** (or defer): …

### Validate — Given / When / Then (decision quality)

| ID | Given | When | Then |
| -- | ----- | ---- | ---- |
| V1 | Stakeholder agrees problem exists | We propose minimal slice | They accept scope for phase 2 |
| V2 | … | … | … |

## analyze-impact / exploration notes

Use **`analyze-impact`** (MCP `analyze_impact` or search fallback). List **services/repos** and key paths — this section drives **Regression** scope in `l4-04-prove.md`.

- Impacted services: …
- Key symbols / paths: …
- Truncated / search-only? (yes/no + reason): …

## Done when

- [ ] Go/no-go recorded; if Go, V1 `Then` satisfied or documented exception
- [ ] Enough context to write Spec; `STATUS.md` updated → **Phase 2**
