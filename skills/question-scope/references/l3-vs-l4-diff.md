# L3 vs L4 — when to pick which (question-scope)

Load when **L3 and L4 both seem plausible** or the user asks “is this L3 or L4?”. Gray-zone AskQuestion: [gray-zones.md § L3 vs L4](./gray-zones.md#l3-vs-l4-eg-migration-in-one-service-vs-many). Human (VI): [README.md § Gray zone — L3 vs L4](../README.md#gray-zone--chọn-l-khi-ranh-giới-mơ) + [Quick checklist below](#quick-checklist-l3-vs-l4).

## One-line rule

| Pick | When |
| ---- | ---- |
| **`/question-scope L3`** | One deployable (one repo/service), bounded module/feature, risks fit in define assumptions |
| **`/question-scope L4`** | Two+ services/repos/teams, formal **Validate** before heavy design, cross-service migration or platform work |

## Comparison

| Topic | L3 | L4 |
| ----- | -- | -- |
| **Deployables** | Usually **one** service/repo | **Two or more** coordinated releases |
| **Validate** | Risks in `l3-01-define` assumptions | Formal **Validate** in `l4-01-discover` (go/no-go) |
| **Pipeline** | Spec → Plan → Test → Code → Regression → Ship | Full **15-step** flow + Architecture / AI / Delivery layers |
| **Phase files** | `l3-01` … `l3-03` | `l4-00` … `l4-05` |
| **Impact tool** | Module + 1-hop; `analyze-impact` bounded to one service | Wider; per impacted **service** in plan |
| **Regression** | Module/package + 1-hop integration | Per impacted service; CI slice named in phase MD |
| **Typical examples** | New module in API; auth cookie→JWT **in one repo** with flag | OIDC across api + worker + admin; org-wide auth; MCP/AI platform |

## Quick checklist (L3 vs L4)

If **any** is **yes** → lean **L4** (or two-option AskQuestion L3 vs L4).

| # | Question |
| - | -------- |
| 1 | **Two or more** services/repos (or teams) must ship in a coordinated window? |
| 2 | Need formal **Validate** (go/no-go) before heavy design or wide implementation? |
| 3 | Cross-service **data migration**, shared session store, or long compat window? |
| 4 | MCP / AI platform / org-wide infra (not one bounded feature)? |

**All no** → **`/question-scope L3`** is appropriate.

## Prompt examples

```text
/question-scope L3 — JWT in api only; feature flag; rollback in one repo.
```

```text
/question-scope L4 — OIDC across api, worker, admin; shared session migration; coordinated release.
```

## Agent

- Do **not** auto-pick L4 when L3 is plausible.
- If user sent **`/question-scope L4`**, steps 1–2 (Idea/Scope) are done — start at Context ([playbooks § L4](./playbooks.md#l4--full-flow-15-steps)).
