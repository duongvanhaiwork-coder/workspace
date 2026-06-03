"""Reranking strategies for retrieval results.

SimpleReranker: keyword-overlap boost (no external model, fast).
CrossEncoderReranker: cross-encoder model for high-quality reranking.
"""

from __future__ import annotations

import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class Reranker(Protocol):
    """Interface for reranking implementations."""

    def rerank(self, query: str, rows: list[dict], top_k: int | None = None) -> list[dict]: ...


class SimpleReranker:
    """Keyword-overlap reranker with opinionated domain priority (section 10).

    Priority boost: entity, dto, service, repository
    Lower priority: helpers, utils, logger, constants
    """

    # Opinionated retrieval rules (section 10)
    _PRIORITY_PATTERNS = ("entity", "dto", "service", "repository", "repo")
    _NOISE_PATTERNS = ("helper", "util", "logger", "constant", "config", "common")

    def rerank(self, query: str, rows: list[dict], top_k: int | None = None) -> list[dict]:
        terms = set(query.lower().split())

        def boost(row: dict) -> float:
            content = row.get("content", "").lower()
            file_path = row.get("file_path", "").lower()
            overlap = sum(1 for t in terms if t in content)
            base = row.get("score", 0) + overlap * 0.05

            # Opinionated domain priority
            if any(p in file_path for p in self._PRIORITY_PATTERNS):
                base += 0.08
            elif any(p in file_path for p in self._NOISE_PATTERNS):
                base -= 0.05

            return base

        ranked = sorted(rows, key=boost, reverse=True)
        if top_k:
            ranked = ranked[:top_k]
        return ranked


class CrossEncoderReranker:
    """Cross-encoder reranker using sentence-transformers.

    Takes top-N candidate chunks, scores each (query, chunk) pair
    with a cross-encoder model, returns top-K by cross-encoder score.

    Models (small → large):
    - cross-encoder/ms-marco-MiniLM-L-6-v2  (fastest, ~22MB)
    - BAAI/bge-reranker-base                 (balanced, ~278MB)
    - cross-encoder/ms-marco-MiniLM-L-12-v2  (better quality, ~33MB)
    """

    _UNLOADED = object()  # sentinel: model not yet attempted

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        self._model_name = model_name
        self._model: object = CrossEncoderReranker._UNLOADED  # lazy load

    def _load_model(self):
        """Lazy load to avoid slow startup when reranker isn't used."""
        if self._model is not CrossEncoderReranker._UNLOADED:
            return
        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self._model_name)
            logger.info(f"Loaded cross-encoder model: {self._model_name}")
        except ImportError:
            logger.warning(
                "sentence-transformers not installed — falling back to SimpleReranker. "
                "Install with: pip install sentence-transformers"
            )
            self._model = None
        except Exception as exc:
            logger.warning(
                f"Failed to load cross-encoder model '{self._model_name}': {exc} "
                "— falling back to SimpleReranker."
            )
            self._model = None

    def rerank(self, query: str, rows: list[dict], top_k: int | None = None) -> list[dict]:
        """Rerank rows using cross-encoder scoring.

        Args:
            query: user query
            rows: candidate chunks from initial retrieval
            top_k: number of results to return (default: min(10, len(rows)))

        Returns:
            Reranked rows with updated scores, limited to top_k.
        """
        if not rows:
            return []

        top_k = top_k or min(10, len(rows))

        self._load_model()
        if self._model is None:
            # Fallback to simple reranker if model not available
            return SimpleReranker().rerank(query, rows, top_k=top_k)

        # Build (query, document) pairs for cross-encoder
        pairs = []
        for row in rows:
            content = row.get("content", "")
            # Truncate long content to avoid OOM (cross-encoder max ~512 tokens)
            doc = content[:1500] if len(content) > 1500 else content
            pairs.append((query, doc))

        # Score all pairs
        scores = self._model.predict(pairs)

        # Attach cross-encoder score and sort
        for row, ce_score in zip(rows, scores):
            row["ce_score"] = float(ce_score)
            # Blend: cross-encoder dominates, original score as tiebreaker
            row["score"] = float(ce_score) * 0.8 + row.get("score", 0) * 0.2

        ranked = sorted(rows, key=lambda r: r["score"], reverse=True)
        return ranked[:top_k]


def get_reranker(use_cross_encoder: bool = False, model_name: str | None = None) -> Reranker:
    """Factory to get the appropriate reranker.

    Args:
        use_cross_encoder: whether to use cross-encoder model
        model_name: override default model name
    """
    if use_cross_encoder:
        name = model_name or "cross-encoder/ms-marco-MiniLM-L-6-v2"
        return CrossEncoderReranker(model_name=name)
    return SimpleReranker()
