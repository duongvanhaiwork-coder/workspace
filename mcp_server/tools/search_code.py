"""search_code — find candidate files/symbols by semantic similarity + keyword overlap.

Use search_code only to find candidate files/symbols.
Do NOT edit code based only on search_code results.
After search_code returns relevant results, call get_context with the selected
file_path/symbol to load full implementation and related context before making changes.

When include_context=true, search_code automatically calls get_context internally
and returns full context inline — use this when the intent is to modify or understand code.

Output schema:
{
    "summary": "...",
    "results": [...],
    "next_recommended_tool": { "name": "get_context", "reason": "...", "input": {...} },
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
    include_context = args.get("include_context", False)

    engine = RetrievalEngine(project=project)
    rows = engine.search(query, top_k=top_k * 2)[:top_k]

    results = []
    for row in rows:
        symbol = row.get("symbol", "")
        results.append({
            "file": row.get("file_path", ""),
            "symbol": symbol if _valid_symbol(symbol) else "",
            "kind": row.get("kind", "unknown"),
            "line_start": row.get("line_start", 0),
            "line_end": row.get("line_end", 0),
            "score": round(row.get("score", 0), 4),
            "reason": _build_reason(query, row),
            "snippet": _truncate(row.get("content", ""), 300),
        })

    confidence = _compute_confidence(results)
    top_files = list(dict.fromkeys(r["file"] for r in results[:5]))
    summary = f"Found {len(results)} result(s) for '{query}'."
    if top_files:
        summary += f" Top files: {', '.join(top_files)}."

    # If include_context=true, auto-call get_context and merge results
    if include_context and results:
        from mcp_server.tools.get_context import get_context
        context_result = get_context({
            "query": query,
            "project": project,
            "top_k": top_k,
            "max_tokens": int(args.get("max_tokens", 12000)),
        })
        return {
            "summary": summary,
            "results": results,
            "context": context_result,
            "missing_context": _detect_missing(rows, query),
            "confidence": confidence,
        }

    # Build next_recommended_tool from top results
    next_tool = _build_next_recommended_tool(results, project, query)

    output = {
        "summary": summary,
        "results": results,
        "missing_context": _detect_missing(rows, query),
        "confidence": confidence,
    }
    if next_tool:
        output["next_recommended_tool"] = next_tool

    return output


def _build_next_recommended_tool(results: list[dict], project: str, query: str) -> dict | None:
    """Build next_recommended_tool suggestion from top search results."""
    if not results:
        return None

    # Pick top results with score >= 0.3 as targets
    targets = []
    seen_files: set[str] = set()
    for r in results:
        if r["score"] < 0.3:
            break
        file_path = r["file"]
        if file_path in seen_files:
            continue
        seen_files.add(file_path)
        target = {"file_path": file_path}
        if r["symbol"]:
            target["symbol"] = r["symbol"]
        targets.append(target)
        if len(targets) >= 3:
            break

    if not targets:
        return None

    return {
        "name": "get_context",
        "reason": (
            "Use get_context to load full implementation, imports, references, "
            "and related files before editing or answering implementation questions."
        ),
        "input": {
            "query": query,
            "project": project,
            "max_tokens": 12000,
        },
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
