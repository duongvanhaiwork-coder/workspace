---
inclusion: always
---

# Code standards

Universal principles for every language and framework. For stack-specific patterns, see `typescript.mdc`, `react.mdc`, `python.mdc`, `dotnet.mdc`, or `java.mdc`. Match the repo's existing layout and libraries before introducing new ones.

## Clean Code

- Small functions with a single, clear responsibility.
- Prefer early returns and guard clauses over deep nesting.
- Names reflect business meaning; no unclear abbreviations.
- No commented-out dead code or debug logs in final changes.
- No silent exception swallowing.
- Extract duplicated logic to the repo's existing shared module path — do not invent a new folder name.
- Remove unused imports and dead code in touched files.
- Prefer explicit over clever implementations.

### Size Limits (new code)

Defaults for **new or heavily edited** code. Do not refactor unrelated large files only to meet limits.

| Unit | Soft limit | Hard limit |
| ---- | ---- | ---- |
| Function/method body | 40 lines | 80 lines (extract) |
| Class/module file | 200 lines | 400 lines (split) |

## Architecture

- Separate transport, application logic, and persistence.
- Keep handlers/controllers thin; business logic in services or domain layer.
- Strict module boundaries; avoid circular dependencies.
- In **monorepos**, respect package boundaries and shared-kernel rules already in the repo; do not introduce new cross-package cycles or “reach into” internal modules.
- Depend on interfaces at boundaries when the project already uses them.
- No new abstraction unless there is a second consumer or a testability need.

### SOLID principles

- Apply **SRP, OCP, LSP, ISP, DIP** when writing or changing code: one clear responsibility per unit, extend via composition/interfaces instead of god classes and `if type` sprawl.
- Keep dependencies on abstractions at layer boundaries when the project already uses DI; do not add interfaces or layers only to satisfy SOLID without a second consumer or testability need (see Architecture above).

## Error Handling

- Reuse existing exception/error types before creating new ones.
- Services throw domain errors; avoid catch-and-rethrow in controllers without adding value.
- Custom API errors: HTTP status, machine-readable code, human-readable message.
- Never expose stack traces, SQL errors, or internal service names to clients.
- Preserve the project's existing error response shape; no new formats without a migration plan.

## Security

- **No hardcoded secrets** — use environment variables or approved config services.
- When the project already **validates required config at startup**, keep that pattern — fail fast on missing or invalid settings for deployable services.
- Validate all input at system boundaries (HTTP, queue, events).
- Parameterized queries only; no string concatenation with user input.
- Sanitize file paths from user input.
- Reuse existing auth; no parallel auth flows.
- Never log tokens, passwords, API keys, or PII.
- Scope data access to the authenticated user/tenant.
- **Least privilege:** credentials, roles, and API scopes should be as narrow as the task allows.
- **Authorization:** if a permission check is ambiguous, **deny** by default; do not fall through to allow.
- **File uploads** (when the feature exists): enforce size/type limits and storage/virus-scan patterns the repo already uses.

## Web hardening (when browsers, cookies, or user-generated HTML exist)

- **Cookie-based sessions:** use the stack’s **CSRF** protection; set **cookie flags** (`Secure`, `HttpOnly`, `SameSite`) consistent with existing auth.
- **CORS:** allow **explicit** origins; avoid `Access-Control-Allow-Origin: *` together with credentials.
- **XSS:** rely on framework defaults for escaping; never introduce raw HTML sinks (e.g. `dangerouslySetInnerHTML`) with user-controlled strings unless the repo already uses a **vetted** sanitization layer.

## Data & time (when APIs or persistence apply)

- Store and compare **timestamps in UTC**; convert to local time only at UI or reporting boundaries, per project convention.
- **Money:** use minor units in integers, a decimal type, or the repo’s money abstraction — **not** binary floating point for currency.
- **Identifiers:** follow the repo’s existing strategy (UUID, ULID, snowflake, …); do not introduce a new ID scheme without an agreed migration.

## Performance

- Paginate or filter large datasets; do not load full tables.
- Set timeouts on external API calls.
- Use indexes for frequently queried columns when changing schema.

## Reliability & external systems

- **Retries:** use **bounded backoff** and only when the operation is **idempotent** or de-duplicated; no unbounded retry loops on request paths.
- Respect **rate limits** and error budgets of third-party APIs; surface clear errors when quotas are exceeded.
- **Circuit breakers / bulkheads:** use when the project already has them; do not add new resilience primitives without a clear need and team pattern.

## Concurrency

- Avoid unnecessary shared mutable state.
- Keep transactions and locks as short as the stack allows.
- Queue and event handlers should be idempotent.

## Dependencies

- Pin or exact versions; no open ranges for production dependencies.
- Prefer maintained packages; avoid heavy trees for trivial needs.
- Commit lockfiles with dependency changes.
- When the repo uses **`npm audit` / Dependabot / Renovate** (or equivalent), treat **high-severity** issues as the team already does — do not silently ignore without a recorded exception or fix.

## Observability

- Structured logging with correlation IDs where the project supports them.
- Use the project logger in production — not ad-hoc debug prints.

## Testing

- **Behavior or contract change** → tests required. Config-only / type-only / pure refactor → no new tests unless asked.
- Minimum: happy path, error path, one relevant edge case.
- Unit tests by default; integration tests only when behavior needs real infrastructure.
- Tests in a dedicated directory; mock external IO in unit tests.
- Names describe behavior: `should reject expired token`, not `test validateToken`.

## API Design (HTTP services)

- Consistent response envelope within a project.
- Paginated lists: items + total + page/limit metadata.
- Correct HTTP status codes; do not return 200 for errors.
- One naming style per project (camelCase or snake_case) — match existing APIs.
- Breaking changes: version or document migration; deprecate before remove.
- New **public** endpoints: follow the repo's existing rate-limit pattern when present.

## Self-Review (before marking work complete)

- [ ] Acceptance criteria met
- [ ] No secrets or PII in logs
- [ ] Input validated at boundaries
- [ ] Error paths handled
- [ ] No unused imports or dead code in touched files
- [ ] Tests updated if behavior changed
- [ ] No scope creep beyond the task
- [ ] Authz / web exposure / uploads reviewed if those areas changed
- [ ] README or runbook updated if setup or operator-facing behavior changed

## Documentation

- Public APIs: brief purpose, parameters, return value when the project documents them.
- Comment **why**, not **what**; TODOs include context and reason.
- When **setup, env vars, or run commands** change, update **`README`** or the team’s canonical onboarding/runbook.
- **User-facing UI:** preserve **accessibility** expectations (labels, focus order, contrast) per product standard; stack details in `react.mdc` when the change touches UI.

## Deployment Safety

- Deployments must be reversible (rollback = redeploy previous version).
- Irreversible schema changes: add new → migrate data → remove old.

## Commits and PRs

- Follow the repo branch policy (feature branches, no direct commits to main/master).
- One logical change per commit; do not commit secrets or generated env-specific files.
- **PR body (when non-trivial):** what changed, **how to verify**, and **risk or rollback** so reviewers can decide quickly.
- Commit message format: use team skills (`commit-message`, `caveman-commit`) when the user asks.
