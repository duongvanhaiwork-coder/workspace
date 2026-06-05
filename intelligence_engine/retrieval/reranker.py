"""Reranking strategies for retrieval results.

Production stack:
  bge-reranker-base (CrossEncoderReranker) — default
  SimpleReranker — fallback when model unavailable

Scoring blend (CrossEncoder):
  final = 0.6 * normalized_ce_score + 0.3 * hybrid_score + 0.1 * symbol_bonus
"""

from __future__ import annotations

import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class Reranker(Protocol):
    """Interface for reranking implementations."""

    def rerank(self, query: str, rows: list[dict], top_k: int | None = None) -> list[dict]: ...


class SimpleReranker:
    """Lightweight fallback reranker — uses hybrid score + symbol name boost."""

    _PRIORITY_PATTERNS = ("entity", "dto", "service", "repository", "repo")
    _NOISE_PATTERNS = ("helper", "util", "logger", "constant", "config", "common")

    def rerank(self, query: str, rows: list[dict], top_k: int | None = None) -> list[dict]:
        query_lower = query.lower()

        for row in rows:
            symbol = (row.get("symbol") or "").lower()
            file_path = (row.get("file_path") or "").lower()

            base = row.get("score", 0)

            # Symbol name match bonus
            if query_lower == symbol or query_lower == symbol.split(".")[-1]:
                base += 0.1
            elif query_lower in symbol:
                base += 0.05

            # Domain priority
            if any(p in file_path for p in self._PRIORITY_PATTERNS):
                base += 0.02
            elif any(p in file_path for p in self._NOISE_PATTERNS):
                base -= 0.01

            row["score"] = base

        ranked = sorted(rows, key=lambda r: r["score"], reverse=True)
        if top_k:
            ranked = ranked[:top_k]
        return ranked


class CrossEncoderReranker:
    """Production reranker using bge-reranker-base.

    Flow:
      1. Receive candidates from hybrid search (already scored by vector + BM25 + symbol)
      2. Score top-N pairs with cross-encoder
      3. Blend: 0.6 * CE + 0.3 * hybrid + 0.1 * symbol_bonus
      4. Return top-K

    bge-reranker-base outputs raw logits — higher = more relevant.
    We normalize to [0, 1] using sigmoid for blending.
    """

    _UNLOADED = object()

    def __init__(self, model_name: str = "BAAI/bge-reranker-base") -> None:
        self._model_name = model_name
        self._model: object = CrossEncoderReranker._UNLOADED

    def _load_model(self):
        """Lazy load model on first use."""
        if self._model is not CrossEncoderReranker._UNLOADED:
            return
        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self._model_name)
            logger.info(f"Loaded reranker model: {self._model_name}")
        except ImportError:
            logger.warning(
                "sentence-transformers not installed — falling back to SimpleReranker."
            )
            self._model = None
        except Exception as exc:
            logger.warning(
                f"Failed to load reranker '{self._model_name}': {exc}. Falling back."
            )
            self._model = None

    def rerank(self, query: str, rows: list[dict], top_k: int | None = None) -> list[dict]:
        if not rows:
            return []

        top_k = top_k or min(10, len(rows))

        self._load_model()
        if self._model is None:
            return SimpleReranker().rerank(query, rows, top_k=top_k)

        # Build (query, document) pairs
        # Use symbol + content as document for better matching
        pairs = []
        for row in rows:
            symbol = row.get("symbol") or ""
            content = row.get("content") or ""
            # Prefix symbol name for the reranker to see it clearly
            doc = f"{symbol}\n{content[:1200]}" if symbol else content[:1500]
            pairs.append((query, doc))

        # Cross-encoder scoring
        raw_scores = self._model.predict(pairs)

        # Normalize CE scores within this batch using min-max → [0, 1]
        raw_floats = [float(s) for s in raw_scores]
        min_score = min(raw_floats)
        max_score = max(raw_floats)
        score_range = max_score - min_score
        if score_range > 0.01:
            ce_scores = [(s - min_score) / score_range for s in raw_floats]
        else:
            # All scores nearly identical — use sigmoid fallback
            import math
            ce_scores = [1.0 / (1.0 + math.exp(-s)) for s in raw_floats]

        # Blend scores
        query_lower = query.lower()
        for row, ce_score in zip(rows, ce_scores):
            hybrid_score = row.get("score", 0)
            # Normalize hybrid score (may be > 1 from the formula)
            max_possible_hybrid = 1.0  # 0.45 + 0.35 + 0.20
            norm_hybrid = min(hybrid_score / max_possible_hybrid, 1.0) if max_possible_hybrid > 0 else 0

            # Symbol bonus: exact match in symbol name
            symbol = (row.get("symbol") or "").lower()
            symbol_bonus = 0.0
            if query_lower == symbol or query_lower == symbol.split(".")[-1]:
                symbol_bonus = 1.0
            elif query_lower in symbol:
                symbol_bonus = 0.8
            elif any(part in symbol for part in query_lower.split(".")):
                symbol_bonus = 0.4

            # Final blend: CE dominant, hybrid for diversity, symbol for precision
            row["score"] = (
                0.6 * ce_score
                + 0.3 * norm_hybrid
                + 0.1 * symbol_bonus
            )
            row["ce_score"] = ce_score

        ranked = sorted(rows, key=lambda r: r["score"], reverse=True)
        return ranked[:top_k]


def get_reranker(use_cross_encoder: bool = True, model_name: str | None = None) -> Reranker:
    """Factory for reranker.

    Default: bge-reranker-base (CrossEncoderReranker)
    Fallback: SimpleReranker when model unavailable
    """
    if use_cross_encoder:
        name = model_name or "BAAI/bge-reranker-base"
        return CrossEncoderReranker(model_name=name)
    return SimpleReranker()
