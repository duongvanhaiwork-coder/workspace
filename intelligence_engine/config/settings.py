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


@lru_cache
def get_settings() -> Settings:
    return Settings()
