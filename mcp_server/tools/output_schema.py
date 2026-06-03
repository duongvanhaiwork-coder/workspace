"""Strict Output Schema wrapper (architecture section 12).

All tools should return:
{
    "meta": {
        "intent": "refactor",
        "confidence": 0.91,
        "token_budget": {
            "max": 12000,
            "used": 6200
        }
    },
    "summary": "...",
    "results": {},
    "missing_context": []
}
"""


def wrap_output(
    summary: str,
    results: dict | list,
    missing_context: list[str] | None = None,
    intent: str = "search",
    confidence: float = 0.0,
    max_tokens: int = 12000,
    used_tokens: int = 0,
) -> dict:
    """Wrap tool output in the strict schema defined in the architecture."""
    return {
        "meta": {
            "intent": intent,
            "confidence": round(confidence, 2),
            "token_budget": {
                "max": max_tokens,
                "used": used_tokens,
            },
        },
        "summary": summary,
        "results": results,
        "missing_context": missing_context or [],
    }
