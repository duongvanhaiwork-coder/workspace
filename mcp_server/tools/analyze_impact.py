"""analyze_impact — blast radius analysis for a symbol/file.

Combines graph traversal + vector search fallback.
Output schema:
{
    "summary": "Impact for 'X': 5 file(s), 3 symbol(s). Risk: medium.",
    "affected_files": [...],
    "affected_symbols": [...],
    "dependency_paths": [...],
    "risk_level": "medium",
    "suggested_actions": [...],
    "missing_context": [],
    "confidence": 0.82
}
"""

from intelligence_engine.context.context_builder import ContextBuilder
from intelligence_engine.retrieval.retrieval_engine import RetrievalEngine


def analyze_impact(args: dict) -> dict:
    target = args["node"]
    depth = int(args.get("depth", 2))
    project = args.get("project", "__default__")

    engine = RetrievalEngine(project=project)
    # ContextBuilder used only for trim/dedup — no token budget needed
    builder = ContextBuilder()
    graph = engine.load_graph()

    # 1. Try graph-based impact analysis
    if graph.nodes:
        result = _analyze_via_graph(engine, builder, target, graph, depth)
    else:
        result = _analyze_via_search(engine, builder, target)

    return result


def _analyze_via_graph(
    engine: RetrievalEngine, builder: ContextBuilder,
    target: str, graph, depth: int,
) -> dict:
    impacted = engine.get_impact(target, graph, depth)
    paths = engine.get_dependency_paths(target, graph)
    paths = builder.trim_dependency_paths(paths)

    affected_files: list[dict] = []
    affected_symbols: list[dict] = []
    seen_files: set[str] = set()

    for item in impacted:
        node_type = item.get("type", "")
        if node_type == "file":
            path = item.get("path", "")
            if path and path not in seen_files:
                seen_files.add(path)
                affected_files.append({
                    "file": path,
                    "reason": f"Depends on '{target}' (distance: {item.get('distance', '?')})",
                })
        elif node_type == "symbol":
            affected_symbols.append({
                "name": item.get("name", ""),
                "kind": item.get("kind", "unknown"),
                "file": item.get("path", ""),
            })

    risk = _assess_risk(affected_files, affected_symbols)
    actions = _suggest_actions(target, affected_files)
    confidence = min(0.95, 0.6 + len(affected_files) * 0.03)

    missing = []
    if not impacted:
        missing.append(f"'{target}' not found in code graph")

    summary = (
        f"Impact for '{target}': {len(affected_files)} file(s), "
        f"{len(affected_symbols)} symbol(s). Risk: {risk}."
    )

    return {
        "summary": summary,
        "affected_files": affected_files,
        "affected_symbols": affected_symbols,
        "dependency_paths": paths,
        "risk_level": risk,
        "suggested_actions": actions,
        "missing_context": missing,
        "confidence": round(confidence, 2),
    }


def _analyze_via_search(engine: RetrievalEngine, builder: ContextBuilder, target: str) -> dict:
    """Fallback: use vector search to estimate impact."""
    rows = engine.search(target, top_k=20)
    refs = engine.find_references_in_search(target, rows)

    affected_files: list[dict] = []
    affected_symbols: list[dict] = []
    seen: set[str] = set()

    for ref in refs:
        f = ref.get("file", "")
        if f and f not in seen:
            seen.add(f)
            affected_files.append({"file": f, "reason": f"Contains '{target}' usage"})
        symbol = ref.get("symbol", "")
        if symbol:
            affected_symbols.append({
                "name": symbol,
                "kind": ref.get("kind", "unknown"),
                "file": f,
            })

    risk = _assess_risk(affected_files, affected_symbols)
    actions = _suggest_actions(target, affected_files)
    confidence = round(min(0.7, 0.3 + len(affected_files) * 0.03), 2)

    summary = (
        f"Impact for '{target}': {len(affected_files)} file(s), "
        f"{len(affected_symbols)} symbol(s). Risk: {risk}."
    )

    return {
        "summary": summary,
        "affected_files": affected_files,
        "affected_symbols": affected_symbols,
        "dependency_paths": [],
        "risk_level": risk,
        "suggested_actions": actions,
        "missing_context": [
            "Analysis based on text search (graph unavailable)"
            " — may be incomplete"
        ],
        "confidence": confidence,
    }


def _assess_risk(files: list[dict], symbols: list[dict]) -> str:
    total = len(files) + len(symbols)
    if total >= 15:
        return "high"
    if total >= 5:
        return "medium"
    return "low"


def _suggest_actions(target: str, affected_files: list[dict]) -> list[str]:
    actions = []
    files = [f["file"] for f in affected_files]
    if not files:
        return [f"No affected files found for '{target}'"]

    actions.append(f"Update references in {len(files)} file(s)")

    has_entity = any("entity" in f.lower() or "model" in f.lower() for f in files)
    has_dto = any("dto" in f.lower() for f in files)
    has_service = any("service" in f.lower() for f in files)
    has_test = any("test" in f.lower() or "spec" in f.lower() for f in files)

    if has_entity:
        actions.append("Update entity/model definition")
    if has_dto:
        actions.append("Update DTO contracts")
    if has_service:
        actions.append("Update service logic")
    if has_test:
        actions.append("Update tests")
    if has_entity and not any("migration" in f.lower() for f in files):
        actions.append("Check if migration is needed")
    return actions
