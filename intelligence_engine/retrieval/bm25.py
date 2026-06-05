"""BM25 keyword scoring for code search.

Provides term-frequency based scoring that understands camelCase/snake_case tokens.
Much better than simple keyword overlap for matching function names, class names, etc.
"""

import math
from collections import Counter

from intelligence_engine.embedding.providers import _tokenize


class BM25Scorer:
    """BM25 scoring over pre-indexed documents.
    
    Designed for in-memory use with moderate corpus sizes (< 100k chunks).
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._doc_freqs: dict[str, int] = {}  # term -> number of docs containing it
        self._doc_lens: list[int] = []
        self._avg_dl: float = 0.0
        self._n_docs: int = 0
        self._corpus_tokens: list[Counter] = []  # per-doc token counts

    def index(self, documents: list[str]) -> None:
        """Build BM25 index from document contents."""
        self._doc_freqs = {}
        self._doc_lens = []
        self._corpus_tokens = []
        self._n_docs = len(documents)

        for doc in documents:
            tokens = _tokenize(doc)
            token_counts = Counter(tokens)
            self._corpus_tokens.append(token_counts)
            self._doc_lens.append(len(tokens))

            # Document frequency: count each term once per document
            for term in token_counts:
                self._doc_freqs[term] = self._doc_freqs.get(term, 0) + 1

        total_len = sum(self._doc_lens)
        self._avg_dl = total_len / self._n_docs if self._n_docs > 0 else 1.0

    def score(self, query: str, doc_idx: int) -> float:
        """Score a single document against a query."""
        if doc_idx >= len(self._corpus_tokens):
            return 0.0

        query_tokens = _tokenize(query)
        doc_tokens = self._corpus_tokens[doc_idx]
        doc_len = self._doc_lens[doc_idx]

        score = 0.0
        for term in query_tokens:
            if term not in self._doc_freqs:
                continue
            df = self._doc_freqs[term]
            idf = math.log((self._n_docs - df + 0.5) / (df + 0.5) + 1.0)
            tf = doc_tokens.get(term, 0)
            tf_norm = (tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * doc_len / self._avg_dl)
            )
            score += idf * tf_norm

        return score

    def score_batch(self, query: str, doc_indices: list[int]) -> list[float]:
        """Score multiple documents against a query."""
        return [self.score(query, idx) for idx in doc_indices]

    def search(self, query: str, top_k: int = 20) -> list[tuple[int, float]]:
        """Search all documents and return top-k (doc_idx, score) pairs."""
        scores = [(i, self.score(query, i)) for i in range(self._n_docs)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
