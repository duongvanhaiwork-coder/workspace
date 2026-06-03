from functools import lru_cache
from intelligence_engine.config.settings import get_settings
from .lancedb_store import LanceDBStore
from .graph_store import GraphStore
from .file_state_store import FileStateStore


@lru_cache
def get_vector_store() -> LanceDBStore:
    return LanceDBStore(get_settings().lancedb_dir)


@lru_cache
def get_graph_store() -> GraphStore:
    return GraphStore(get_settings().graph_dir)


@lru_cache
def get_file_state_store() -> FileStateStore:
    return FileStateStore(get_settings().file_state_dir)
