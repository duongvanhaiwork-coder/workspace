from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AI_CORE_", env_file=".env", extra="ignore")
    projects_file: str = "projects.json"
    data_dir: str = "data"
    embedding_dim: int = 384

    # Reranker config
    use_cross_encoder: bool = False
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    reranker_top_k: int = 10

    # Graph pruning
    graph_max_depth: int = 2
    graph_max_nodes: int = 50
    graph_include_tests: bool = False

    # Retrieval cache
    retrieval_cache_ttl_minutes: int = 30

    @property
    def root_dir(self) -> Path:
        return Path.cwd()

    @property
    def lancedb_dir(self) -> Path:
        return Path(self.data_dir) / "lancedb"

    @property
    def graph_dir(self) -> Path:
        return Path(self.data_dir) / "graph"

    @property
    def file_state_dir(self) -> Path:
        return Path(self.data_dir) / "file_state"

    @property
    def symbol_index_dir(self) -> Path:
        return Path(self.data_dir) / "symbol_index"

    @property
    def relationship_index_dir(self) -> Path:
        return Path(self.data_dir) / "relationship_index"

    @property
    def retrieval_cache_dir(self) -> Path:
        return Path(self.data_dir) / "retrieval_cache"


@lru_cache
def get_settings() -> Settings:
    return Settings()
