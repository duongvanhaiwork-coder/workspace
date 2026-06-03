"""find_references — find all usages of a symbol.

Combines graph-based lookup + vector search fallback.
Output schema:
{
    "summary": "Found 12 reference(s).",
    "references": [...],
    "missing_context": [],
    "confidence": 0.85
}
"""

from intelligence_engine.context.context_builder import ContextBuilder
from intelligence_engine.retrieval.retrieval_engine import RetrievalEngine


def find_references(args: dict) -> dict:
    symbol = args["symbol"]
    project = args.get("project", "__default__")

    engine = RetrievalEngine(project=project)
    # ContextBuilder used only for dedup — no token budget needed
    builder = ContextBuilder()

    # 1. Try graph-based lookup
    graph = engine.load_graph()
    refs = engine.find_references_in_graph(symbol, graph)

    # 2. Supplement with vector search (exact text match)
    rows = engine.search(symbol, top_k=20)
    search_refs = engine.find_references_in_search(symbol, rows)

    # 3. Merge (graph refs first, then search refs avoiding duplicates)
    seen_keys = {f"{r['file']}:{r['line']}" for r in refs}
    for sr in search_refs:
        key = f"{sr['file']}:{sr['line']}"
        if key not in seen_keys:
            seen_keys.add(key)
            refs.append(sr)

    # 4. Context Builder trims & deduplicates
    refs = builder.build_references(refs)

    confidence = _compute_confidence(refs, symbol)
    summary = f"Found {len(refs)} reference(s) for '{symbol}'."
    missing = []
    if not refs:
        missing.append(
            f"No references found for '{symbol}'"
            " — symbol may not be indexed or graph not built"
        )

    return {
        "summary": summary,
        "references": refs,
        "missing_context": missing,
        "confidence": confidence,
    }


def _compute_confidence(refs: list[dict], symbol: str) -> float:
    if not refs:
        return 0.0
    exact = sum(1 for r in refs if symbol in r.get("snippet", "") or r["usage"] == "definition")
    ratio = exact / len(refs) if refs else 0
    return round(min(0.95, 0.5 + ratio * 0.4), 2)
