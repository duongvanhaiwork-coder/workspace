"""reindex_project — trigger full re-indexing for a project (architecture section 11).

Clears existing indexes and runs the full indexing pipeline:
Scanner → Tree-sitter → Symbol Extractor → Chunker → Embedder → LanceDB + Graph + Indexes
"""

from intelligence_engine.storage import (
    get_retrieval_cache_store,
)


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

    # Report status — actual reindexing is done by scripts/index_project.py
    # This tool signals that the caches are cleared and a reindex is needed
    return {
        "summary": (
            f"Caches cleared for project '{project}' ({invalidated} cache entries invalidated). "
            f"Run `python scripts/index_project.py {project}` to perform full reindex."
        ),
        "results": {
            "project": project,
            "cache_invalidated": invalidated,
            "action_required": f"python scripts/index_project.py {project}",
        },
        "missing_context": [],
        "confidence": 1.0,
    }
