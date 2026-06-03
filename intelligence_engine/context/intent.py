"""Intent classification for user queries.

Determines what the user wants so the retrieval planner can fetch
only the relevant pieces (no fixed output for every query).
"""

from __future__ import annotations

import re
from enum import Enum


class QueryIntent(Enum):
    SEARCH = "search"
    EXPLAIN = "explain"
    REFACTOR = "refactor"
    IMPACT = "impact"
    DEBUG = "debug"
    TEST = "test"
    GENERATE = "generate"


# Pattern → intent, ordered by specificity (first match wins)
_RULES: list[tuple[re.Pattern, QueryIntent]] = [
    # Refactor
    (re.compile(
        r"\b(rename|đổi tên|refactor|extract|move method|split)\b", re.I,
    ), QueryIntent.REFACTOR),
    # Impact
    (re.compile(
        r"\b(impact|blast radius|ảnh hưởng|affected|breaking change)\b", re.I,
    ), QueryIntent.IMPACT),
    # Debug
    (re.compile(
        r"\b(why|tại sao|debug|always 0|null|undefined|error|bug|fail|wrong)\b", re.I,
    ), QueryIntent.DEBUG),
    # Test
    (re.compile(
        r"\b(tests?|specs?|unit tests?|generate tests?|viết test)\b", re.I,
    ), QueryIntent.TEST),
    # Generate
    (re.compile(
        r"\b(thêm field|add field|create|generate|implement|tạo)\b", re.I,
    ), QueryIntent.GENERATE),
    # Explain
    (re.compile(
        r"\b(how does|giải thích|explain|flow|luồng|what does|describe)\b", re.I,
    ), QueryIntent.EXPLAIN),
    # Search (most generic — "where", "find", "dùng ở đâu")
    (re.compile(
        r"\b(where|ở đâu|find|tìm|dùng ở|used in|references)\b", re.I,
    ), QueryIntent.SEARCH),
]


def classify_intent(query: str) -> QueryIntent:
    """Classify a user query into an intent.

    Uses keyword rules for now; can be swapped with LLM classification later.
    """
    for pattern, intent in _RULES:
        if pattern.search(query):
            return intent
    # Default: search (safest — return references)
    return QueryIntent.SEARCH
