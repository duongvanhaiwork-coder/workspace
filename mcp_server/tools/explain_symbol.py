"""explain_symbol — summarize a symbol's role and relationships.

Output schema:
{
    "summary": "...",
    "symbol": "OrderService.createOrder",
    "kind": "method",
    "file": "...",
    "dependencies": [...],
    "called_by": [...],
    "calls": [...],
    "important_chunks": [...],
    "missing_context": [],
    "confidence": 0.78
}
"""

from intelligence_engine.retrieval.retrieval_engine import RetrievalEngine


def explain_symbol(args: dict) -> dict:
    symbol = args["symbol"]
    project = args.get("project", "__default__")

    engine = RetrievalEngine(project=project)

    # 1. Graph: get relationships
    graph = engine.load_graph()
    info = engine.get_symbol_info(symbol, graph)
    deps = engine.get_dependencies(symbol, graph)
    callers = engine.get_callers(symbol, graph)
    calls = []
    # calls = outgoing "calls" edges (get_dependencies already covers imports+calls)
    # separate calls from imports
    if graph.nodes:
        for node, data in graph.nodes(data=True):
            if data.get("name") == symbol or symbol in node:
                for succ in graph.successors(node):
                    succ_data = graph.nodes[succ]
                    edge = graph.edges[node, succ]
                    if edge.get("relation") == "calls":
                        calls.append(succ_data.get("name", succ))

    # 2. Vector search: get code chunks
    rows = engine.search(symbol, top_k=20)
    chunks = _get_important_chunks(symbol, rows)

    # Determine definition location from search results
    definition = _find_definition(symbol, rows)

    # 3. Build output
    file_path = info.get("file", "") or definition.get("file", "")
    kind = info.get("kind", "") or definition.get("kind", "")

    summary = _build_summary(symbol, kind, file_path, info, deps, callers, calls)
    missing = _detect_missing(info, chunks, callers, calls)
    confidence = _compute_confidence(info, chunks, callers, calls)

    return {
        "summary": summary,
        "symbol": symbol,
        "kind": kind,
        "file": file_path,
        "line_start": definition.get("line_start", 0),
        "line_end": definition.get("line_end", 0),
        "dependencies": deps[:10],
        "called_by": callers[:10],
        "calls": calls[:10],
        "important_chunks": chunks[:5],
        "missing_context": missing,
        "confidence": confidence,
    }


def _get_important_chunks(symbol: str, rows: list[dict]) -> list[dict]:
    """Get code chunks that contain the symbol."""
    chunks = []
    for row in rows:
        content = row.get("content", "")
        row_symbol = row.get("symbol", "")
        if symbol in content or symbol in row_symbol or row_symbol == symbol:
            chunks.append({
                "file": row.get("file_path", ""),
                "line_start": row.get("start_line", 0),
                "line_end": row.get("end_line", 0),
                "content": content[:500],
            })
    return chunks[:5]


def _find_definition(symbol: str, rows: list[dict]) -> dict:
    """Find the definition location from search results."""
    for row in rows:
        row_symbol = row.get("symbol", "")
        if row_symbol == symbol or symbol in row_symbol:
            return {
                "kind": row.get("kind", "unknown"),
                "file": row.get("file_path", ""),
                "line_start": row.get("start_line", 0),
                "line_end": row.get("end_line", 0),
            }
    return {}


def _build_summary(symbol: str, kind: str, file: str, info: dict, deps: list, callers: list, calls: list) -> str:
    parts = []
    if kind:
        parts.append(f"'{symbol}' is a {kind}")
        if file:
            parts.append(f"defined in {file}")
    else:
        parts.append(f"'{symbol}' — limited information available")

    if calls:
        parts.append(f"Calls: {', '.join(calls[:5])}")
    if callers:
        parts.append(f"Called by: {', '.join(callers[:5])}")
    if deps:
        parts.append(f"Dependencies: {', '.join(deps[:5])}")

    return ". ".join(parts) + "."


def _detect_missing(info: dict, chunks: list, callers: list, calls: list) -> list[str]:
    missing = []
    if not info.get("found"):
        missing.append("Symbol not found in code graph — relationship data may be incomplete")
    if not chunks:
        missing.append("No code chunks found — symbol may not be indexed")
    if not callers and not calls:
        missing.append("No call relationships found — graph may lack call edges")
    return missing


def _compute_confidence(info: dict, chunks: list, callers: list, calls: list) -> float:
    score = 0.3
    if info.get("found"):
        score += 0.3
    if chunks:
        score += 0.2
    if callers or calls:
        score += 0.15
    return round(min(0.95, score), 2)
