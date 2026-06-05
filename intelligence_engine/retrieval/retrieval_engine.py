"""Retrieval Engine — unified facade for LanceDB + NetworkX + Symbol Index.

Responsibilities:
- Vector search (LanceDB via HybridSearch)
- Graph queries (NetworkX)
- Combine both sources for references, impact, dependencies

Each MCP tool calls specific methods here instead of directly
touching storage or search layers.
"""

from __future__ import annotations

import networkx as nx

from intelligence_engine.config.settings import get_settings
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.graph.pruning import GraphPruner, PruningConfig
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.retrieval.reranker import get_reranker
from intelligence_engine.storage import get_graph_store, get_vector_store


class RetrievalEngine:
    """High-level retrieval facade combining vector search + graph."""

    def __init__(self, project: str = "__default__") -> None:
        self.project = project
        self._store = get_vector_store()
        self._embedder = Embedder()
        self._hybrid = HybridSearch(self._store, self._embedder)

        settings = get_settings()
        self._reranker = get_reranker(
            use_cross_encoder=settings.use_cross_encoder,
            model_name=settings.reranker_model,
        )
        self._reranker_top_k = settings.reranker_top_k
        self._pruner = GraphPruner(PruningConfig(
            max_depth=settings.graph_max_depth,
            max_nodes=settings.graph_max_nodes,
            include_tests=settings.graph_include_tests,
        ))

    # --- Search Layer ---

    def search(self, query: str, top_k: int = 20) -> list[dict]:
        """Full retrieval pipeline: hybrid (vector + BM25 + symbol + graph) → reranker.
        
        Flow:
          1. HybridSearch returns top_k*2 candidates scored by 4 signals
          2. CrossEncoderReranker (bge-reranker-base) refines to top_k
        """
        candidates = self._hybrid.search(query, top_k=top_k, project=self.project)
        return self._reranker.rerank(query, candidates, top_k=top_k)

    # --- Graph Layer ---

    def load_graph(self) -> nx.DiGraph:
        """Load the code graph (NetworkX) scoped to this project."""
        return get_graph_store().load(project=self.project)

    def find_references_in_graph(self, symbol: str, graph: nx.DiGraph) -> list[dict]:
        """Find all graph nodes that reference a symbol."""
        refs: list[dict] = []
        if not graph.nodes:
            return refs

        for node, data in graph.nodes(data=True):
            if data.get("name") == symbol or symbol in node:
                for pred in graph.predecessors(node):
                    pred_data = graph.nodes[pred]
                    edge = graph.edges[pred, node]
                    if pred_data.get("type") == "file":
                        refs.append({
                            "file": pred_data.get("path", ""),
                            "symbol": data.get("name", symbol),
                            "kind": data.get("kind", ""),
                            "line": edge.get("line", 0),
                            "usage": _relation_to_usage(edge.get("relation", "")),
                            "snippet": "",
                        })
        return refs

    def find_references_in_search(self, symbol: str, rows: list[dict]) -> list[dict]:
        """Find references by exact text match in search results."""
        refs: list[dict] = []
        for row in rows:
            content = row.get("content", "")
            if symbol not in content:
                continue

            snippet = ""
            line = 0
            for i, text_line in enumerate(content.splitlines(), start=row.get("line_start", 1)):
                if symbol in text_line:
                    snippet = text_line.strip()
                    line = i
                    break

            refs.append({
                "file": row.get("file_path", ""),
                "symbol": row.get("symbol", ""),
                "kind": row.get("kind", "unknown"),
                "line": line,
                "usage": _classify_usage(snippet, symbol),
                "snippet": snippet[:200],
            })
        return refs

    def get_dependency_paths(self, target: str, graph: nx.DiGraph) -> list[dict]:
        """Get incoming and outgoing edges for a symbol in the graph."""
        if not graph.nodes:
            return []
        paths: list[dict] = []
        for node, data in graph.nodes(data=True):
            if data.get("name") == target or target in node:
                for pred in graph.predecessors(node):
                    pred_data = graph.nodes[pred]
                    edge = graph.edges[pred, node]
                    paths.append({
                        "source": pred_data.get("name", pred),
                        "target": data.get("name", target),
                        "relation": edge.get("relation", "unknown"),
                    })
                for succ in graph.successors(node):
                    succ_data = graph.nodes[succ]
                    edge = graph.edges[node, succ]
                    paths.append({
                        "source": data.get("name", target),
                        "target": succ_data.get("name", succ),
                        "relation": edge.get("relation", "unknown"),
                    })
        return paths

    def get_dependencies(self, target: str, graph: nx.DiGraph) -> list[str]:
        """Get what a symbol imports/calls."""
        if not graph.nodes:
            return []
        deps: list[str] = []
        for node, data in graph.nodes(data=True):
            if data.get("name") == target or target in node:
                for succ in graph.successors(node):
                    succ_data = graph.nodes[succ]
                    edge = graph.edges[node, succ]
                    if edge.get("relation") in ("imports", "calls"):
                        deps.append(succ_data.get("name", succ))
        return deps

    def get_callers(self, target: str, graph: nx.DiGraph) -> list[str]:
        """Get what calls this symbol."""
        if not graph.nodes:
            return []
        callers: list[str] = []
        for node, data in graph.nodes(data=True):
            if data.get("name") == target or target in node:
                for pred in graph.predecessors(node):
                    pred_data = graph.nodes[pred]
                    edge = graph.edges[pred, node]
                    if edge.get("relation") == "calls":
                        callers.append(pred_data.get("name", pred))
        return callers

    def get_impact(self, target: str, graph: nx.DiGraph, depth: int = 2) -> list[dict]:
        """Get nodes affected by changes to target (pruned reverse traversal)."""
        if not graph.nodes:
            return []
        for node, data in graph.nodes(data=True):
            if data.get("name") == target or target in node:
                return self._pruner.prune_impact(graph, node, depth=depth)
        return []

    def get_symbol_info(self, symbol: str, graph: nx.DiGraph) -> dict:
        """Get metadata about a symbol from the graph."""
        info = {"kind": "", "file": "", "found": False}
        if not graph.nodes:
            return info
        for node, data in graph.nodes(data=True):
            if data.get("name") == symbol and data.get("type") == "symbol":
                info["kind"] = data.get("kind", "")
                info["file"] = data.get("path", "")
                info["found"] = True
                # Get file from defines edge
                for pred in graph.predecessors(node):
                    pred_data = graph.nodes[pred]
                    edge = graph.edges[pred, node]
                    if edge.get("relation") == "defines" and pred_data.get("type") == "file":
                        info["file"] = pred_data.get("path", info["file"])
                break
        return info


def _relation_to_usage(relation: str) -> str:
    mapping = {
        "defines": "definition",
        "imports": "import",
        "references": "read",
        "calls": "read",
    }
    return mapping.get(relation, "read")


def _classify_usage(snippet: str, symbol: str) -> str:
    if not snippet:
        return "read"
    if any(kw in snippet for kw in ("class ", "interface ", "export class")):
        return "definition"
    if f"{symbol}:" in snippet and "import" not in snippet:
        return "definition"
    if "import" in snippet:
        return "import"
    if f"{symbol} =" in snippet or f"{symbol}=" in snippet:
        return "write"
    return "read"
