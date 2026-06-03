class SimpleReranker:
    def rerank(self, query: str, rows: list[dict]) -> list[dict]:
        terms = set(query.lower().split())
        def boost(row):
            content = row.get("content", "").lower()
            overlap = sum(1 for t in terms if t in content)
            return row.get("score", 0) + overlap * 0.05
        return sorted(rows, key=boost, reverse=True)
