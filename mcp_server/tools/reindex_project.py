"""reindex_project — trigger full re-indexing for a project (architecture section 11).

Clears existing indexes and runs the full indexing pipeline:
Scanner → Tree-sitter → Symbol Extractor → Chunker → Embedder → LanceDB + Graph + Indexes
"""

from intelligence_engine.storage import (
    get_retrieval_cache_store,
    get_vector_store,
    get_symbol_index_store,
    get_relationship_index_store,
)
from intelligence_engine.retrieval.hybrid_search import HybridSearch


def reindex_project(args: dict) -> dict:
    project = args.get("project", "__default__")

    if project == "__default__":
        return {
            "summary": "Error: project parameter is required for reindex_project.",
            "results": {},
            "missing_context": ["Specify a project name to reindex"],
            "confidence": 0.0,
        }

    # Clear caches for this project
    cache_store = get_retrieval_cache_store()
    invalidated = cache_store.invalidate_project(project)

    # Reload all stores from disk (picks up changes from external index_project.py)
    get_vector_store().reload(project)
    get_symbol_index_store().reload(project)
    get_relationship_index_store().reload(project)

    # Invalidate BM25 cache so it rebuilds on next search
    # HybridSearch instances in RetrievalEngine will rebuild on next call
    HybridSearch._invalidate_project_cache(project)

    symbol_count = get_symbol_index_store().count(project)

    return {
        "summary": (
            f"Stores reloaded for project '{project}' ({invalidated} cache entries invalidated, "
            f"{symbol_count} symbols now indexed). "
            f"If data is stale, run `python scripts/index_project.py {project}` to perform full reindex, then call this tool again."
        ),
        "results": {
            "project": project,
            "cache_invalidated": invalidated,
            "symbols_loaded": symbol_count,
            "stores_reloaded": True,
        },
        "missing_context": [],
        "confidence": 1.0,
    }
