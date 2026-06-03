from .providers import HashEmbeddingProvider
from intelligence_engine.config.settings import get_settings


class Embedder:
    def __init__(self, provider: HashEmbeddingProvider | None = None) -> None:
        self.provider = provider or HashEmbeddingProvider(dim=get_settings().embedding_dim)

    def embed_text(self, text: str) -> list[float]:
        return self.provider.embed(text)

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]
