from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.retrieval.reranker import SimpleReranker
from intelligence_engine.storage import get_vector_store


class RetrievalEngine:
    """High-level retrieval facade combining vector search + reranking."""

    def __init__(self, project: str = "__default__") -> None:
        self.project = project
        self._store = get_vector_store()
        self._embedder = Embedder()
        self._hybrid = HybridSearch(self._store, self._embedder)
        self._reranker = SimpleReranker()

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        rows = self._hybrid.search(query, top_k=top_k * 2, project=self.project)
        rows = self._reranker.rerank(query, rows)
        return rows[:top_k]
