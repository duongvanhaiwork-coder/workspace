"""Intent-aware prompt templates for MCP tool output.

Each template provides structured instructions that guide the LLM (Cursor/Kiro)
on how to interpret and use the retrieved context effectively.

Templates are injected into the tool output as `prompt_guidance` field,
giving the LLM explicit rules for using the provided context.
"""

from __future__ import annotations

from intelligence_engine.context.intent import QueryIntent


# --- Base rules (always included) ---

_BASE_RULES = """\
Rules for using this context:
1. Use ONLY the provided code context. Do not hallucinate missing code.
2. If context is insufficient, say so explicitly — do not guess.
3. Cite file paths and line numbers when referencing code.
4. Prefer definitions over usages when explaining structure.
5. Prefer service/domain logic over controller/transport layer."""


# --- Intent-specific templates ---

_TEMPLATES: dict[QueryIntent, str] = {
    QueryIntent.SEARCH: """\
You are locating references to a symbol in a codebase.

{base_rules}

Focus on:
- Where the symbol is DEFINED (class, function, interface)
- Where it is IMPORTED
- Where it is READ or WRITTEN
- Group by usage type: definition > import > write > read

If no references found, suggest alternative symbol names or partial matches.""",

    QueryIntent.EXPLAIN: """\
You are explaining how code works.

{base_rules}

Focus on:
- Start from the entrypoint (where the flow begins)
- Follow the dependency chain: caller → service → repository → entity
- Explain data transformations at each step
- Note any side effects (events, logging, external calls)

Structure your explanation as a flow, not a flat list.""",

    QueryIntent.REFACTOR: """\
You are planning a safe refactor.

{base_rules}

Focus on:
- ALL references that must change (find them all before starting)
- DTO/contract changes (API consumers may break)
- Entity/model changes (migrations may be needed)
- Test files that assert on the old behavior
- Import paths that reference the old name

Priority order: Entity → DTO → Service → Controller → Test
Always check if a database migration is needed.""",

    QueryIntent.IMPACT: """\
You are analyzing blast radius before a change.

{base_rules}

Focus on:
- Direct dependents (files that import/call the target)
- Transitive dependents (files that depend on direct dependents)
- Contract boundaries (DTOs, API responses, event payloads)
- Risk assessment: how many consumers? Any external APIs?

Ignore:
- Utility imports (logger, constants, helpers) unless the change IS in a utility
- Test files (they should change, but don't add risk)
- Unrelated files that happen to share a keyword""",

    QueryIntent.DEBUG: """\
You are investigating a bug.

{base_rules}

Focus on:
- WHERE the value is WRITTEN (assignments, mutations, DB writes)
- The CALL CHAIN that leads to the write location
- CONDITIONAL BRANCHES that could skip or alter the write
- State that flows BETWEEN functions (params, returns, shared state)
- Race conditions or async ordering issues

Do NOT focus on:
- Read-only usages (unless they reveal expected vs actual)
- Unrelated code that happens to use the same variable name""",

    QueryIntent.TEST: """\
You are writing or analyzing tests.

{base_rules}

Focus on:
- The METHOD DEFINITION (exact signature, parameters, return type)
- Dependencies that need mocking (external services, DB, time)
- Edge cases visible in the code (null checks, empty arrays, zero values)
- Error paths (throw statements, try/catch, error returns)
- Business rules embedded in conditionals

Suggest test cases for:
- Happy path (normal input → expected output)
- Error path (invalid input → proper error handling)
- Edge cases (boundary values, empty collections, null/undefined)""",

    QueryIntent.GENERATE: """\
You are generating new code that fits the existing codebase.

{base_rules}

Focus on:
- Existing patterns (naming conventions, file structure, import style)
- Related entities/DTOs (match field naming and types)
- Service patterns (constructor injection, method signatures, error handling)
- Existing validation patterns (decorators, guards, pipes)

Match the project's existing:
- Naming: camelCase vs snake_case vs PascalCase
- Structure: where new files should go
- Patterns: repository pattern, service layer, etc.""",
}


def get_prompt_template(intent: QueryIntent) -> str:
    """Get the prompt guidance template for a given intent."""
    template = _TEMPLATES.get(intent, _TEMPLATES[QueryIntent.SEARCH])
    return template.format(base_rules=_BASE_RULES)


def get_base_rules() -> str:
    """Get base rules only (for tools that don't use intent)."""
    return _BASE_RULES
