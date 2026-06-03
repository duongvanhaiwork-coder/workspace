"""search_code — find code by semantic similarity + keyword overlap.

Output schema:
{
    "summary": "...",
    "results": [...],
    "missing_context": [],
    "confidence": 0.92
}
"""

from intelligence_engine.context.context_builder import _valid_symbol
from intelligence_engine.retrieval.retrieval_engine import RetrievalEngine


def search_code(args: dict) -> dict:
    query = args["query"]
    top_k = int(args.get("top_k", 10))
    project = args.get("project", "__default__")

    engine = RetrievalEngine(project=project)
    rows = engine.search(query, top_k=top_k * 2)[:top_k]

    results = []
    for row in rows:
        symbol = row.get("symbol", "")
        results.append({
            "file": row.get("file_path", ""),
            "symbol": symbol if _valid_symbol(symbol) else "",
            "kind": row.get("kind", "unknown"),
            "line_start": row.get("start_line", 0),
            "line_end": row.get("end_line", 0),
            "score": round(row.get("score", 0), 4),
            "reason": _build_reason(query, row),
            "snippet": _truncate(row.get("content", ""), 300),
        })

    confidence = _compute_confidence(results)
    top_files = list(dict.fromkeys(r["file"] for r in results[:5]))
    summary = f"Found {len(results)} result(s) for '{query}'."
    if top_files:
        summary += f" Top files: {', '.join(top_files)}."

    return {
        "summary": summary,
        "results": results,
        "missing_context": _detect_missing(rows, query),
        "confidence": confidence,
    }


def _build_reason(query: str, row: dict) -> str:
    content = row.get("content", "").lower()
    terms = query.lower().split()
    matched = [t for t in terms if t in content]
    if matched:
        return f"Contains: {', '.join(matched)}"
    symbol = row.get("symbol", "")
    if symbol:
        return f"Symbol '{symbol}' semantically similar"
    return "Semantic similarity match"


def _compute_confidence(results: list[dict]) -> float:
    if not results:
        return 0.0
    top_score = results[0]["score"]
    if top_score >= 0.8:
        return min(0.95, top_score)
    if top_score >= 0.5:
        return round(top_score * 0.85, 2)
    return round(top_score * 0.6, 2)


def _detect_missing(rows: list[dict], query: str) -> list[str]:
    if not rows:
        return ["No indexed code found — project may not be indexed"]
    if all(r.get("score", 0) < 0.3 for r in rows):
        return ["All results have low relevance — query may need refinement"]
    return []


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "…"
