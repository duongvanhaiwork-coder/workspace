from fastapi import APIRouter
from intelligence_engine.storage import get_graph_store
from intelligence_engine.graph.reference_finder import GraphReferenceFinder
from intelligence_engine.graph.impact_analyzer import ImpactAnalyzer

router = APIRouter()


@router.get("/references/{symbol}")
def find_references(symbol: str):
    graph = get_graph_store().load()
    return {"items": GraphReferenceFinder().find_references(graph, symbol)}


@router.get("/impact")
def analyze_impact(node: str, depth: int = 2):
    graph = get_graph_store().load()
    return {"items": ImpactAnalyzer().analyze(graph, node, depth)}
