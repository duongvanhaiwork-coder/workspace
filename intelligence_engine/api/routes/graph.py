from fastapi import APIRouter
from intelligence_engine.storage import get_graph_store
from intelligence_engine.graph.reference_finder import GraphReferenceFinder
from intelligence_engine.graph.impact_analyzer import ImpactAnalyzer

router = APIRouter()


@router.get("/references/{symbol}")
def find_references(symbol: str, project: str = "__default__"):
    graph = get_graph_store().load(project=project)
    return {"items": GraphReferenceFinder().find_references(graph, symbol)}


@router.get("/impact")
def analyze_impact(node: str, project: str = "__default__", depth: int = 2):
    graph = get_graph_store().load(project=project)
    return {"items": ImpactAnalyzer().analyze(graph, node, depth)}
