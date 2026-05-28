---
inclusion: fileMatch
fileMatchPattern: ["**/*.tsx", "**/*.jsx", "**/app/**/*.js"]
---

# React

Rules for React UI. Match the repo's stack before adding libraries. For TypeScript UI (`.tsx`), also apply type discipline for props and events.

## Match Existing Stack

- **Redux + redux-saga** (legacy container/saga repos): keep actions → saga → API → reducer flow; do not migrate to React Query/SWR unless explicitly requested.
- **React Query / SWR:** use only when the repo already depends on them.
- Prefer the repo's React major version (e.g. React 17 patterns) — do not use APIs from newer versions without upgrading the project.

## Project Layout (container pattern)

When the repo uses `app/containers/<Feature>/`:

| File | Role |
| ---- | ---- |
| `constants.js` | Action type constants |
| `actions.js` | Action creators |
| `reducer.js` | Pure reducer (no side effects) |
| `saga.js` | Side effects, API calls |
| `selectors.js` | Memoized selectors when present |
| `index.js` | Container / page wiring |
| `components/` | Presentational UI |
| `Loadable.js` | Code-split entry when used |

Follow the same structure for new features.

## Components

- Keep components small; separate container (data) from presentational (UI) when the repo does.
- Prefer composition over inheritance.
- Avoid deep prop drilling — use Redux selectors or context already in the project.

## Redux and Sagas

- **API calls in sagas**, not scattered in components (use `app/utils/request.js` or existing helpers).
- Reducers stay pure: no `fetch`, no timers, no mutations of state — return new objects.
- Action types from `constants.js`; avoid magic strings.
- Use `takeLatest` / `takeEvery` consistently with existing sagas in the file.
- Select data with `useSelector`; dispatch with `useDispatch` — match hooks vs `connect()` style already used nearby.

## Hooks and Effects

- Extract custom hooks when logic is reused or complex.
- Side effects in `useEffect` or sagas — not during render.
- List all `useEffect` dependencies; avoid infinite loops when syncing props to local state.
- Colocate UI-only state in the component; shared/async state in Redux.

## Forms and UX

- Reuse existing form components (`FormBox`, validators in `validate.js`) before creating new patterns.
- Preserve accessibility: labels for inputs, meaningful button text, keyboard-friendly controls.

## Do Not

- Introduce a new global state library without user approval.
- Call APIs directly from many components when the feature already has a saga.
- Mix Redux state with duplicate server cache unless the repo already does.
