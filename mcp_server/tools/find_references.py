from intelligence_engine.storage import get_graph_store
from intelligence_engine.graph.reference_finder import GraphReferenceFinder


def find_references(args: dict) -> dict:
    graph = get_graph_store().load()
    return {"items": GraphReferenceFinder().find_references(graph, args["symbol"])}
