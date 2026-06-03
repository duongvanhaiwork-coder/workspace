"""Retrieval Planner — decides what data to fetch based on intent.

Maps QueryIntent → a set of retrieval needs, then orchestrates
Search Layer + Graph Layer + Context Builder to produce
only the relevant output fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .intent import QueryIntent


class RetrievalNeed(Enum):
    """Atomic retrieval capabilities the engine can provide."""
    SUMMARY = "summary"
    ENTRYPOINTS = "entrypoints"
    REFERENCES = "references"
    DEPENDENCY_PATHS = "dependency_paths"
    CODE_CHUNKS = "code_chunks"
    IMPACT = "impact"
    CALL_CHAIN = "call_chain"
    WRITE_LOCATIONS = "write_locations"
    READ_LOCATIONS = "read_locations"
    METHOD_DEFINITION = "method_definition"
    DEPENDENCIES = "dependencies"
    EDGE_CASES = "edge_cases"
    SUGGESTED_ACTIONS = "suggested_actions"


@dataclass
class RetrievalPlan:
    intent: QueryIntent
    needs: list[RetrievalNeed] = field(default_factory=list)
    # Hints extracted from the query
    target_symbol: str = ""
    target_file: str = ""


# Intent → required retrieval needs
_INTENT_NEEDS: dict[QueryIntent, list[RetrievalNeed]] = {
    QueryIntent.SEARCH: [
        RetrievalNeed.REFERENCES,
    ],
    QueryIntent.EXPLAIN: [
        RetrievalNeed.SUMMARY,
        RetrievalNeed.ENTRYPOINTS,
        RetrievalNeed.DEPENDENCY_PATHS,
        RetrievalNeed.CODE_CHUNKS,
    ],
    QueryIntent.REFACTOR: [
        RetrievalNeed.REFERENCES,
        RetrievalNeed.IMPACT,
        RetrievalNeed.DEPENDENCY_PATHS,
        RetrievalNeed.SUGGESTED_ACTIONS,
    ],
    QueryIntent.IMPACT: [
        RetrievalNeed.IMPACT,
        RetrievalNeed.DEPENDENCY_PATHS,
        RetrievalNeed.SUGGESTED_ACTIONS,
    ],
    QueryIntent.DEBUG: [
        RetrievalNeed.CALL_CHAIN,
        RetrievalNeed.WRITE_LOCATIONS,
        RetrievalNeed.READ_LOCATIONS,
        RetrievalNeed.CODE_CHUNKS,
    ],
    QueryIntent.TEST: [
        RetrievalNeed.METHOD_DEFINITION,
        RetrievalNeed.DEPENDENCIES,
        RetrievalNeed.EDGE_CASES,
        RetrievalNeed.CODE_CHUNKS,
    ],
    QueryIntent.GENERATE: [
        RetrievalNeed.REFERENCES,
        RetrievalNeed.DEPENDENCIES,
        RetrievalNeed.CODE_CHUNKS,
        RetrievalNeed.SUGGESTED_ACTIONS,
    ],
}


def plan_retrieval(intent: QueryIntent, query: str) -> RetrievalPlan:
    """Create a retrieval plan based on intent and query hints."""
    needs = _INTENT_NEEDS.get(intent, [RetrievalNeed.REFERENCES])
    target_symbol = _extract_symbol_hint(query)

    return RetrievalPlan(
        intent=intent,
        needs=list(needs),
        target_symbol=target_symbol,
    )


def _extract_symbol_hint(query: str) -> str:
    """Try to extract a symbol/identifier from the query.

    Looks for PascalCase, camelCase, or quoted identifiers.
    """
    import re

    # Quoted identifier: 'ServiceProviderId' or "ServiceProviderId"
    quoted = re.search(r"['\"]([A-Za-z_][\w.]*)['\"]", query)
    if quoted:
        return quoted.group(1)

    # dotted: OrderService.createOrder
    dotted = re.findall(r"\b([A-Za-z_][\w]*\.[A-Za-z_][\w]*)\b", query)
    if dotted:
        return dotted[0]

    # PascalCase identifiers (at least 2 capital transitions)
    pascal = re.findall(r"\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b", query)
    if pascal:
        return pascal[0]

    # camelCase identifiers (lowercase start + at least 1 uppercase transition)
    camel = re.findall(r"\b([a-z]+[A-Z][a-zA-Z]*)\b", query)
    if camel:
        return camel[0]

    return ""
