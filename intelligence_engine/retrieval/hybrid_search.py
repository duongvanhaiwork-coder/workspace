"""Hybrid Search — 4-signal retrieval combining vector, BM25, symbol index, and graph.

Scoring formula:
    final_score = 0.35 * vector + 0.30 * keyword(BM25) + 0.20 * symbol + 0.15 * graph

Stack:
- Embedding: BAAI/bge-base-en-v1.5 (768d) via LanceDB
- Keyword: BM25 with camelCase-aware tokenization
- Symbol: exact/substring match from symbol index
- Graph: NetworkX relationship index (callers, callees, imports)
- Reranker: BAAI/bge-reranker-base (applied after this stage)
"""

from __future__ import annotations

import logging
from typing import Any

from intelligence_engine.embedding.providers import _tokenize
from intelligence_engine.retrieval.bm25 import BM25Scorer
from intelligence_engine.storage import get_symbol_index_store, get_relationship_index_store

logger = logging.getLogger(__name__)

# Scoring weights — tuned for code search
VECTOR_WEIGHT = 0.35   # semantic understanding
KEYWORD_WEIGHT = 0.30  # exact name/token matching (critical for code)
SYMBOL_WEIGHT = 0.20   # structural: symbol index match
GRAPH_WEIGHT = 0.15    # graph: relationship context (callers, deps)


class HybridSearch:
    """4-signal hybrid search: vector + BM25 + symbol + graph."""

    def __init__(self, vector_store, embedder) -> None:
        self.vector_store = vector_store
        self.embedder = embedder
        self._bm25_cache: dict[str, tuple[BM25Scorer, list[str]]] = {}

    def _get_bm25(self, project: str) -> tuple[BM25Scorer, list[str]]:
        """Get or build BM25 index for a project."""
        # Check class-level invalidation
        if hasattr(self.__class__, '_invalidated_projects') and project in self.__class__._invalidated_projects:
            self._bm25_cache.pop(project, None)
            self.__class__._invalidated_projects.discard(project)

        if project in self._bm25_cache:
            return self._bm25_cache[project]

        rows = self.vector_store._get_rows(project)
        if not rows:
            scorer = BM25Scorer()
            scorer.index([])
            self._bm25_cache[project] = (scorer, [])
            return scorer, []

        chunk_ids = list(rows.keys())
        documents = []
        for cid in chunk_ids:
            row = rows[cid]
            symbol = row.get("symbol") or ""
            content = row.get("content") or ""
            file_path = row.get("file_path") or ""
            doc_text = f"{symbol} {file_path} {content}"
            documents.append(doc_text)

        scorer = BM25Scorer()
        scorer.index(documents)
        self._bm25_cache[project] = (scorer, chunk_ids)
        return scorer, chunk_ids

    def invalidate_cache(self, project: str) -> None:
        """Clear BM25 cache for a project."""
        self._bm25_cache.pop(project, None)

    @classmethod
    def _invalidate_project_cache(cls, project: str) -> None:
        """Class-level invalidation for external reindex."""
        if not hasattr(cls, '_invalidated_projects'):
            cls._invalidated_projects: set[str] = set()
        cls._invalidated_projects.add(project)

    def _compute_graph_scores(
        self, query: str, candidate_cids: set[str], all_rows: dict, project: str
    ) -> dict[str, float]:
        """Compute graph-based relevance scores for candidates.
        
        Uses relationship index to boost chunks that are:
        - Directly related to symbols matching the query (callers/callees)
        - In the same call chain as matched symbols
        - Connected via imports to matched symbols
        """
        rel_store = get_relationship_index_store()
        symbol_store = get_symbol_index_store()

        # Find symbols matching the query
        symbol_matches = symbol_store.search(query, project=project)
        if not symbol_matches:
            return {}

        # Collect related symbols from graph
        related_symbols: dict[str, float] = {}  # symbol_qname -> relevance

        for sym in symbol_matches:
            qname = sym.get("qualified_name", "")
            if not qname:
                continue
            # Direct match gets full score
            related_symbols[qname.lower()] = 1.0

            # Get relationship data
            rel_entry = rel_store.get(qname, project=project)
            if not rel_entry:
                continue

            # Callers and callees get partial score
            for caller in rel_entry.get("called_by", []):
                related_symbols.setdefault(caller.lower(), 0.6)
            for callee in rel_entry.get("calls", []):
                related_symbols.setdefault(callee.lower(), 0.5)
            # DTO/model usage
            for dto in rel_entry.get("uses_dto", []):
                related_symbols.setdefault(dto.lower(), 0.4)
            for model in rel_entry.get("uses_model", []):
                related_symbols.setdefault(model.lower(), 0.4)

        # Score each candidate chunk based on graph relationships
        graph_scores: dict[str, float] = {}
        for cid in candidate_cids:
            if cid not in all_rows:
                continue
            row = all_rows[cid]
            chunk_symbol = (row.get("symbol") or "").lower()

            # Check if chunk's symbol is in the related set
            score = 0.0
            if chunk_symbol in related_symbols:
                score = related_symbols[chunk_symbol]
            else:
                # Check partial match (e.g. "Service.method" in "ClassName.method")
                for rel_sym, rel_score in related_symbols.items():
                    if rel_sym in chunk_symbol or chunk_symbol in rel_sym:
                        score = max(score, rel_score * 0.7)
                        break

            if score > 0:
                graph_scores[cid] = score

        return graph_scores

    def search(self, query: str, top_k: int = 10, project: str = "__default__") -> list[dict]:
        """4-signal hybrid search.
        
        Returns top_k * 2 candidates for reranker to refine.
        """
        all_rows = self.vector_store._get_rows(project)
        if not all_rows:
            return []

        # --- 1. Vector search (embedding similarity) ---
        qv = self.embedder.embed_text(query)
        vector_results = self.vector_store.search(qv, top_k=top_k * 5, project=project)
        max_vscore = max((r.get("score", 0) for r in vector_results), default=1.0) or 1.0

        # --- 2. BM25 keyword search ---
        bm25_scorer, chunk_ids = self._get_bm25(project)
        bm25_results = bm25_scorer.search(query, top_k=top_k * 5)
        max_bm25 = max((score for _, score in bm25_results), default=1.0) or 1.0

        # --- 3. Symbol index (exact/substring) ---
        symbol_store = get_symbol_index_store()
        symbol_matches = symbol_store.search(query, project=project)
        symbol_files: set[str] = set()
        symbol_qnames: set[str] = set()
        for s in symbol_matches:
            fp = s.get("file_path", "")
            qname = s.get("qualified_name", "")
            if fp:
                symbol_files.add(fp)
            if qname:
                symbol_qnames.add(qname.lower())

        # --- 4. Merge candidates ---
        candidate_scores: dict[str, dict[str, float]] = {}

        # Vector candidates
        for row in vector_results:
            cid = row.get("chunk_id", "")
            if not cid:
                continue
            vscore = row.get("score", 0) / max_vscore
            candidate_scores.setdefault(cid, {"vector": 0, "bm25": 0, "symbol": 0, "graph": 0})
            candidate_scores[cid]["vector"] = vscore

        # BM25 candidates
        for doc_idx, bm25_score in bm25_results:
            if doc_idx >= len(chunk_ids):
                continue
            cid = chunk_ids[doc_idx]
            normalized = bm25_score / max_bm25
            candidate_scores.setdefault(cid, {"vector": 0, "bm25": 0, "symbol": 0, "graph": 0})
            candidate_scores[cid]["bm25"] = normalized

        # Symbol index: inject matching chunks
        query_lower = query.lower()
        for cid, row in all_rows.items():
            row_symbol = (row.get("symbol") or "").lower()
            row_file = row.get("file_path") or ""

            if query_lower in row_symbol or row_symbol in query_lower:
                candidate_scores.setdefault(cid, {"vector": 0, "bm25": 0, "symbol": 0, "graph": 0})
                candidate_scores[cid]["symbol"] = 1.0
            elif row_file in symbol_files and any(query_lower in qn for qn in symbol_qnames):
                candidate_scores.setdefault(cid, {"vector": 0, "bm25": 0, "symbol": 0, "graph": 0})
                candidate_scores[cid]["symbol"] = 0.8
            elif row_file in symbol_files:
                candidate_scores.setdefault(cid, {"vector": 0, "bm25": 0, "symbol": 0, "graph": 0})
                candidate_scores[cid]["symbol"] = 0.5

        # --- 5. Graph scoring ---
        graph_scores = self._compute_graph_scores(
            query, set(candidate_scores.keys()), all_rows, project
        )
        for cid, gscore in graph_scores.items():
            if cid in candidate_scores:
                candidate_scores[cid]["graph"] = gscore

        # --- 6. Final score computation ---
        scored_results: list[dict[str, Any]] = []
        for cid, scores in candidate_scores.items():
            if cid not in all_rows:
                continue
            row = all_rows[cid]
            final_score = (
                VECTOR_WEIGHT * scores["vector"]
                + KEYWORD_WEIGHT * scores["bm25"]
                + SYMBOL_WEIGHT * scores["symbol"]
                + GRAPH_WEIGHT * scores["graph"]
            )
            result = {k: v for k, v in row.items() if k != "vector"}
            result["score"] = final_score
            result["_debug_scores"] = scores
            scored_results.append(result)

        scored_results.sort(key=lambda r: r["score"], reverse=True)
        # Return more candidates than top_k for reranker to work with
        return scored_results[:top_k * 2]
