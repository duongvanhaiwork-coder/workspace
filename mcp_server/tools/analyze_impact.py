from intelligence_engine.storage import get_graph_store
from intelligence_engine.graph.impact_analyzer import ImpactAnalyzer


def analyze_impact(args: dict) -> dict:
    graph = get_graph_store().load()
    return {"items": ImpactAnalyzer().analyze(graph, args["node"], int(args.get("depth", 2)))}
