class HybridSearch:
    """Combines vector similarity with keyword overlap for retrieval."""

    def __init__(self, vector_store, embedder) -> None:
        self.vector_store = vector_store
        self.embedder = embedder

    def search(self, query: str, top_k: int = 10, project: str = "__default__") -> list[dict]:
        qv = self.embedder.embed_text(query)
        vector_results = self.vector_store.search(qv, top_k=top_k, project=project)
        terms = set(query.lower().split())
        for row in vector_results:
            content = row.get("content", "").lower()
            keyword_hits = sum(1 for t in terms if t in content)
            row["score"] = row.get("score", 0) * 0.7 + keyword_hits * 0.1
        return sorted(vector_results, key=lambda r: r["score"], reverse=True)
