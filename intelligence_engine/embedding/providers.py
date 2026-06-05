"""Embedding providers for code search.

Providers:
- HashEmbeddingProvider: deterministic hash-based (fast, no GPU, low quality)
- SentenceTransformerProvider: ML model (bge-base-en-v1.5, 768d, good for code)
"""

import hashlib
import logging
import re
from typing import Protocol

import numpy as np

logger = logging.getLogger(__name__)


def _tokenize(text: str) -> list[str]:
    """Split text into tokens, handling camelCase, PascalCase, snake_case, and kebab-case.
    
    Used by BM25 keyword scoring and hash embeddings.
    """
    # Split by whitespace and common delimiters (keep original case for camelCase split)
    raw_tokens = re.split(r'[\s\.\,\;\:\(\)\[\]\{\}\=\+\-\*/&\|!@#$%^~`"\'<>?/\\]+', text)
    tokens = []
    for token in raw_tokens:
        if not token:
            continue
        # Split snake_case / kebab-case
        parts = re.split(r'[_\-]', token)
        for part in parts:
            if not part:
                continue
            # Split camelCase / PascalCase
            sub_parts = re.sub(r'([a-z])([A-Z])', r'\1 \2', part)
            sub_parts = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', sub_parts)
            sub_parts = sub_parts.lower().split()
            tokens.extend(sub_parts)
            # Also keep the full compound token for exact matching
            if len(sub_parts) > 1:
                tokens.append(part.lower())
    return tokens


class EmbeddingProvider(Protocol):
    """Interface for embedding providers."""
    dim: int
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...


class HashEmbeddingProvider:
    """Deterministic hash-based embedding (fast fallback, no model download).
    
    Uses camelCase-aware tokenization for better code matching.
    """
    def __init__(self, dim: int = 384) -> None:
        self.dim = dim

    def embed(self, text: str) -> list[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        tokens = _tokenize(text)
        for token in tokens:
            h = int(hashlib.sha1(token.encode()).hexdigest(), 16)
            vec[h % self.dim] += 1.0
        norm = float(np.linalg.norm(vec)) or 1.0
        return (vec / norm).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(t) for t in texts]


class SentenceTransformerProvider:
    """ML-based embedding using sentence-transformers.
    
    Default: BAAI/bge-base-en-v1.5 (768d, good balance for code search).
    Alternatives:
      - BAAI/bge-large-en-v1.5 (1024d, better quality, slower)
      - Qwen3-Embedding-0.6B (newer, stronger)
    """

    _UNLOADED = object()

    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5", dim: int = 768) -> None:
        self._model_name = model_name
        self.dim = dim
        self._model = SentenceTransformerProvider._UNLOADED

    def _load(self):
        if self._model is not SentenceTransformerProvider._UNLOADED:
            return
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._model_name)
            self.dim = self._model.get_embedding_dimension()
            logger.info(f"Loaded embedding model: {self._model_name} (dim={self.dim})")
        except ImportError:
            logger.warning(
                "sentence-transformers not installed — falling back to HashEmbeddingProvider. "
                "Install with: pip install sentence-transformers"
            )
            self._model = None
        except Exception as exc:
            logger.warning(f"Failed to load model '{self._model_name}': {exc}. Falling back.")
            self._model = None

    def embed(self, text: str) -> list[float]:
        self._load()
        if self._model is None:
            return HashEmbeddingProvider(dim=self.dim).embed(text)
        # bge models benefit from "Represent this sentence:" prefix for queries
        embedding = self._model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        self._load()
        if self._model is None:
            fallback = HashEmbeddingProvider(dim=self.dim)
            return [fallback.embed(t) for t in texts]
        embeddings = self._model.encode(texts, normalize_embeddings=True, batch_size=64)
        return embeddings.tolist()
