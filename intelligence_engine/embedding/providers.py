import hashlib
import numpy as np

class HashEmbeddingProvider:
    """Deterministic local embedding fallback. Replace with OpenAI/local model provider later."""
    def __init__(self, dim: int = 384) -> None:
        self.dim = dim

    def embed(self, text: str) -> list[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        for token in text.lower().split():
            h = int(hashlib.sha1(token.encode()).hexdigest(), 16)
            vec[h % self.dim] += 1.0
        norm = float(np.linalg.norm(vec)) or 1.0
        return (vec / norm).tolist()
