from functools import lru_cache
from intelligence_engine.config.settings import get_settings
from .lancedb_store import LanceDBStore
from .graph_store import GraphStore
from .file_state_store import FileStateStore
from .symbol_index_store import SymbolIndexStore
from .relationship_index_store import RelationshipIndexStore
from .retrieval_cache_store import RetrievalCacheStore


@lru_cache
def get_vector_store() -> LanceDBStore:
    return LanceDBStore(get_settings().lancedb_dir)


@lru_cache
def get_graph_store() -> GraphStore:
    return GraphStore(get_settings().graph_dir)


@lru_cache
def get_file_state_store() -> FileStateStore:
    return FileStateStore(get_settings().file_state_dir)


@lru_cache
def get_symbol_index_store() -> SymbolIndexStore:
    return SymbolIndexStore(get_settings().symbol_index_dir)


@lru_cache
def get_relationship_index_store() -> RelationshipIndexStore:
    return RelationshipIndexStore(get_settings().relationship_index_dir)


@lru_cache
def get_retrieval_cache_store() -> RetrievalCacheStore:
    return RetrievalCacheStore(get_settings().retrieval_cache_dir)
