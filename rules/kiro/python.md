---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Python

Rules for Python services (FastAPI, workers). If the repo is not FastAPI, match its existing layout and libraries.

## Naming

| Context                    | Convention       | Example                                |
| -------------------------- | ---------------- | -------------------------------------- |
| Class                      | PascalCase       | `ProjectConfig`, `FileStateStore`      |
| Function, method, variable | snake_case       | `run_pipeline`, `content_hash`         |
| Constant (module-level)    | UPPER_SNAKE_CASE | `IGNORED_DIRS`, `RELATION_IMPORTS`     |
| File/module                | snake_case       | `graph_builder.py`, `hybrid_search.py` |

## Configuration and Logging

- Load secrets and service URLs from environment variables or config modules — never hardcode.
- Use the project's logger; no `print` in production paths.
- External HTTP/DB calls must have timeouts.

## FastAPI Patterns

- Use APIRouter organized by module/domain.
- Request/response models use Pydantic `BaseModel`; validate at the router boundary.
- Dependency injection for services and repositories.
- Keep route handlers thin; delegate to services.
- Use `async` endpoints for IO-bound work.

## Task Queue

- Offload long-running or CPU-heavy work to a queue/worker (RQ, Celery, etc.).
- Never block request handlers on indexing, embedding, or batch jobs.
- Task handlers must be idempotent.

## Type Hints

- Type hints on all public function signatures.
- Use `dataclass` or Pydantic models for structured data; avoid untyped dicts at boundaries.
- Prefer `list[str]` over `List[str]` (Python 3.9+).

## Testing

- Tests in a dedicated `tests/` tree (not beside production modules).
- Use `pytest`; mock HTTP, Redis, DB, and filesystem in unit tests.
- Cover happy path, error path, and one edge case per behavior change.
