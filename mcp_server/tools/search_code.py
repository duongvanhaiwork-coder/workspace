from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.storage import get_vector_store
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.retrieval.reranker import SimpleReranker


def search_code(args: dict) -> dict:
    query = args["query"]
    top_k = int(args.get("top_k", 10))
    project = args.get("project", "__default__")
    store = get_vector_store()
    rows = HybridSearch(store, Embedder()).search(query, top_k * 2, project=project)
    rows = SimpleReranker().rerank(query, rows)[:top_k]
    return {"items": rows}
