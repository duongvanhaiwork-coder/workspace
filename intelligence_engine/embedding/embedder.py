"""Embedder facade — selects provider based on settings.

Uses SentenceTransformerProvider (bge-base-en-v1.5) by default for quality.
Falls back to HashEmbeddingProvider if model fails to load.
"""

from intelligence_engine.config.settings import get_settings
from .providers import SentenceTransformerProvider, HashEmbeddingProvider


def _make_provider():
    """Create the appropriate embedding provider based on settings."""
    settings = get_settings()
    embedding_model = getattr(settings, "embedding_model", None)

    if embedding_model == "hash":
        return HashEmbeddingProvider(dim=settings.embedding_dim)

    # Default: use sentence-transformer model
    model_name = embedding_model or "BAAI/bge-base-en-v1.5"
    return SentenceTransformerProvider(model_name=model_name, dim=settings.embedding_dim)


class Embedder:
    def __init__(self, provider=None) -> None:
        self.provider = provider or _make_provider()

    @property
    def dim(self) -> int:
        return self.provider.dim

    def embed_text(self, text: str) -> list[float]:
        return self.provider.embed(text)

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return self.provider.embed_batch(texts)
