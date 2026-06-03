"""Orchestrator — executes a RetrievalPlan and assembles tool-specific output.

Flow:
    User Query → Intent Analyzer → Retrieval Planner → Orchestrator
    Orchestrator calls: Search Layer / Graph Layer / Context Builder
    Returns: only the fields the intent needs.
"""

from __future__ import annotations

from intelligence_engine.context.intent import QueryIntent, classify_intent
from intelligence_engine.context.planner import (
    RetrievalNeed,
    RetrievalPlan,
    plan_retrieval,
)
from intelligence_engine.context.prompt_templates import get_prompt_template
from intelligence_engine.context.token_budget import TokenBudget
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.retrieval.reranker import get_reranker
from intelligence_engine.storage import get_graph_store, get_vector_store

import networkx as nx


class Orchestrator:
    """Execute a retrieval plan and produce intent-specific output."""

    def __init__(self, project: str, max_tokens: int = 12000, top_k: int = 20) -> None:
        self.project = project
        self.max_tokens = max_tokens
        self.top_k = top_k
        self._store = get_vector_store()
        self._embedder = Embedder()
        self._hybrid = HybridSearch(self._store, self._embedder)

        from intelligence_engine.config.settings import get_settings
        settings = get_settings()
        self._reranker = get_reranker(
            use_cross_encoder=settings.use_cross_encoder,
            model_name=settings.reranker_model,
        )
        self._reranker_top_k = settings.reranker_top_k

    def run(self, query: str) -> dict:
        intent = classify_intent(query)
        plan = plan_retrieval(intent, query)
        return self._execute(query, plan)

    def run_with_intent(self, query: str, intent: QueryIntent) -> dict:
        plan = plan_retrieval(intent, query)
        return self._execute(query, plan)

    def _execute(self, query: str, plan: RetrievalPlan) -> dict:
        """Assemble output by fetching only what the plan requires."""
        target = plan.target_symbol or query
        needs = set(plan.needs)
        output: dict = {
            "query": query,
            "intent": plan.intent.value,
        }

        # --- Search Layer ---
        search_rows = []
        if needs & {
            RetrievalNeed.REFERENCES,
            RetrievalNeed.CODE_CHUNKS,
            RetrievalNeed.ENTRYPOINTS,
            RetrievalNeed.METHOD_DEFINITION,
            RetrievalNeed.WRITE_LOCATIONS,
            RetrievalNeed.READ_LOCATIONS,
            RetrievalNeed.DEPENDENCIES,
            RetrievalNeed.EDGE_CASES,
        }:
            search_rows = self._search(target)

        # --- Graph Layer ---
        graph = None
        if needs & {
            RetrievalNeed.DEPENDENCY_PATHS,
            RetrievalNeed.CALL_CHAIN,
            RetrievalNeed.IMPACT,
            RetrievalNeed.REFERENCES,
        }:
            graph = get_graph_store().load(project=self.project)

        # --- Assemble per intent ---
        if plan.intent == QueryIntent.SEARCH:
            output.update(self._build_search(target, search_rows, graph))
        elif plan.intent == QueryIntent.EXPLAIN:
            output.update(self._build_explain(target, search_rows, graph))
        elif plan.intent == QueryIntent.REFACTOR:
            output.update(self._build_refactor(target, search_rows, graph))
        elif plan.intent == QueryIntent.IMPACT:
            output.update(self._build_impact(target, graph))
        elif plan.intent == QueryIntent.DEBUG:
            output.update(self._build_debug(target, search_rows, graph))
        elif plan.intent == QueryIntent.TEST:
            output.update(self._build_test(target, search_rows, graph))
        elif plan.intent == QueryIntent.GENERATE:
            output.update(self._build_generate(target, search_rows, graph))

        # Common footer
        output["missing_context"] = output.get("missing_context", [])
        output["confidence"] = output.get("confidence", 0.0)
        output["prompt_guidance"] = get_prompt_template(plan.intent)
        return output

    # --- Search helper ---

    def _search(self, query: str, top_k: int | None = None) -> list[dict]:
        k = top_k or self.top_k
        rows = self._hybrid.search(query, top_k=k, project=self.project)
        return self._reranker.rerank(query, rows, top_k=self._reranker_top_k)

    # --- Intent builders ---

    def _build_search(self, target: str, rows: list[dict], graph: nx.DiGraph | None) -> dict:
        refs = self._extract_references(target, rows, graph)
        return {
            "summary": f"Found {len(refs)} reference(s) for '{target}'.",
            "references": refs,
            "confidence": self._score_confidence(refs, rows),
            "missing_context": self._search_missing(refs, target),
        }

    def _build_explain(self, target: str, rows: list[dict], graph: nx.DiGraph | None) -> dict:
        budget = TokenBudget(self.max_tokens)
        chunks = self._build_chunks(rows, budget, target)
        entrypoints = self._find_entrypoints(rows)
        paths = self._find_dependency_paths(target, graph) if graph else []

        used = sum(budget.estimate(c.get("content", "")) for c in chunks)
        return {
            "summary": self._make_summary(target, chunks, entrypoints),
            "entrypoints": entrypoints,
            "dependency_paths": paths,
            "chunks": chunks,
            "token_budget": {"max_tokens": self.max_tokens, "used_tokens": used},
            "confidence": self._score_confidence(chunks, rows),
            "missing_context": self._explain_missing(entrypoints, paths),
        }

    def _build_refactor(self, target: str, rows: list[dict], graph: nx.DiGraph | None) -> dict:
        refs = self._extract_references(target, rows, graph)
        paths = self._find_dependency_paths(target, graph) if graph else []
        affected_files = list(dict.fromkeys(r["file"] for r in refs))
        risk = "high" if len(affected_files) >= 10 else "medium" if len(affected_files) >= 3 else "low"

        return {
            "summary": f"Refactor '{target}': {len(refs)} reference(s) in {len(affected_files)} file(s). Risk: {risk}.",
            "affected_files": [{"file": f, "reason": "Contains reference"} for f in affected_files],
            "affected_symbols": [{"name": r["symbol"], "kind": r.get("kind", ""), "file": r["file"]} for r in refs if r.get("symbol")],
            "dependency_paths": paths,
            "risk_level": risk,
            "suggested_actions": self._refactor_actions(target, affected_files),
            "confidence": self._score_confidence(refs, rows),
            "missing_context": self._refactor_missing(refs, paths),
        }

    def _build_impact(self, target: str, graph: nx.DiGraph | None) -> dict:
        if not graph or not graph.nodes:
            return {
                "summary": f"Cannot analyze impact for '{target}' — graph not available.",
                "affected_files": [],
                "affected_symbols": [],
                "risk_level": "low",
                "dependency_paths": [],
                "suggested_actions": [],
                "confidence": 0.0,
                "missing_context": ["Code graph not built — run indexer first"],
            }

        affected = self._graph_impact(target, graph)
        paths = self._find_dependency_paths(target, graph)
        risk = "high" if len(affected) >= 10 else "medium" if len(affected) >= 3 else "low"
        return {
            "summary": f"Impact for '{target}': {len(affected)} node(s) affected. Risk: {risk}.",
            "affected_files": [a for a in affected if "file:" in a.get("node", "")],
            "affected_symbols": [a for a in affected if "symbol:" in a.get("node", "")],
            "risk_level": risk,
            "dependency_paths": paths,
            "suggested_actions": [f"Review {len(affected)} affected node(s)"],
            "confidence": min(0.9, 0.5 + len(affected) * 0.03),
            "missing_context": [] if affected else [f"'{target}' not found in graph"],
        }

    def _build_debug(self, target: str, rows: list[dict], graph: nx.DiGraph | None) -> dict:
        budget = TokenBudget(self.max_tokens)
        chunks = self._build_chunks(rows, budget, target)
        writes = [c for c in chunks if self._is_write(c, target)]
        reads = [c for c in chunks if self._is_read(c, target)]
        call_chain = self._find_dependency_paths(target, graph) if graph else []

        return {
            "summary": f"Debug '{target}': {len(writes)} write location(s), {len(reads)} read location(s).",
            "possible_sources": writes[:5],
            "call_chain": call_chain,
            "write_locations": writes[:5],
            "read_locations": reads[:5],
            "chunks": chunks[:5],
            "confidence": self._score_confidence(chunks, rows),
            "missing_context": self._debug_missing(writes, reads, call_chain),
        }

    def _build_test(self, target: str, rows: list[dict], graph: nx.DiGraph | None) -> dict:
        budget = TokenBudget(self.max_tokens)
        chunks = self._build_chunks(rows, budget, target)
        definition = next((c for c in chunks if target.lower() in c.get("symbol", "").lower()), None)
        deps = self._find_graph_dependencies(target, graph) if graph else []

        return {
            "summary": f"Test context for '{target}': definition {'found' if definition else 'not found'}, {len(deps)} dependency(ies).",
            "symbol": target,
            "method_definition": definition,
            "dependencies": deps,
            "edge_cases": self._suggest_edge_cases(target, chunks),
            "chunks": chunks[:5],
            "confidence": 0.7 if definition else 0.4,
            "missing_context": [] if definition else [f"Definition of '{target}' not found in index"],
        }

    def _build_generate(self, target: str, rows: list[dict], graph: nx.DiGraph | None) -> dict:
        budget = TokenBudget(self.max_tokens)
        chunks = self._build_chunks(rows, budget, target)
        refs = self._extract_references(target, rows, graph)
        deps = self._find_graph_dependencies(target, graph) if graph else []

        return {
            "summary": f"Generate context for '{target}': {len(chunks)} chunk(s), {len(deps)} dependency(ies).",
            "references": refs[:10],
            "dependencies": deps,
            "chunks": chunks[:8],
            "suggested_actions": self._generate_actions(target, chunks),
            "confidence": self._score_confidence(chunks, rows),
            "missing_context": self._generate_missing(chunks),
        }

    # --- Utility methods ---

    def _extract_references(self, symbol: str, rows: list[dict], graph: nx.DiGraph | None) -> list[dict]:
        """Find references from search results + graph."""
        refs: list[dict] = []
        seen: set[str] = set()

        # From search results (exact content match)
        for row in rows:
            content = row.get("content", "")
            if symbol not in content:
                continue
            file_path = row.get("file_path", "")
            key = f"{file_path}:{row.get('start_line', 0)}"
            if key in seen:
                continue
            seen.add(key)

            snippet = ""
            line = 0
            for i, text_line in enumerate(content.splitlines(), start=row.get("start_line", 1)):
                if symbol in text_line:
                    snippet = text_line.strip()
                    line = i
                    break

            refs.append({
                "file": file_path,
                "symbol": row.get("symbol", ""),
                "kind": row.get("kind", "unknown"),
                "line": line,
                "usage": self._classify_usage(snippet, symbol),
                "snippet": snippet[:200],
            })

        # From graph
        if graph and graph.nodes:
            for node, data in graph.nodes(data=True):
                if data.get("name") == symbol or symbol in node:
                    for pred in graph.predecessors(node):
                        pred_data = graph.nodes[pred]
                        if pred_data.get("type") == "file":
                            path = pred_data.get("path", "")
                            key = f"{path}:graph"
                            if key not in seen:
                                seen.add(key)
                                edge = graph.edges[pred, node]
                                refs.append({
                                    "file": path,
                                    "symbol": data.get("name", symbol),
                                    "kind": data.get("kind", ""),
                                    "line": edge.get("line", 0),
                                    "usage": self._relation_to_usage(edge.get("relation", "")),
                                    "snippet": "",
                                })
        return refs

    def _build_chunks(self, rows: list[dict], budget: TokenBudget, target: str) -> list[dict]:
        """Build chunks within token budget, prioritizing target matches."""
        chunks: list[dict] = []
        used = 0
        for row in rows:
            content = row.get("content", "")
            cost = budget.estimate(content)
            if used + cost > budget.max_tokens:
                break
            symbol = row.get("symbol", "")
            chunks.append({
                "file": row.get("file_path", ""),
                "symbol": symbol if self._valid_symbol(symbol) else "",
                "kind": row.get("kind", "unknown"),
                "line_start": row.get("start_line", 0),
                "line_end": row.get("end_line", 0),
                "reason": self._chunk_reason(target, row),
                "content": content,
            })
            used += cost
        return chunks

    def _find_entrypoints(self, rows: list[dict]) -> list[dict]:
        """First high-score result per file = entrypoint."""
        seen: set[str] = set()
        entries: list[dict] = []
        for row in rows[:10]:
            f = row.get("file_path", "")
            if f in seen or row.get("score", 0) < 0.3:
                continue
            seen.add(f)
            symbol = row.get("symbol", "")
            entries.append({
                "file": f,
                "symbol": symbol if self._valid_symbol(symbol) else "",
                "kind": row.get("kind", ""),
                "line_start": row.get("start_line", 0),
                "line_end": row.get("end_line", 0),
            })
        return entries[:5]

    def _find_dependency_paths(self, target: str, graph: nx.DiGraph) -> list[dict]:
        if not graph.nodes:
            return []
        from intelligence_engine.graph.pruning import prune_dependency_paths
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
        return prune_dependency_paths(paths)

    def _find_graph_dependencies(self, target: str, graph: nx.DiGraph) -> list[str]:
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

    def _graph_impact(self, target: str, graph: nx.DiGraph) -> list[dict]:
        from intelligence_engine.graph.pruning import GraphPruner
        pruner = GraphPruner()
        for node, data in graph.nodes(data=True):
            if data.get("name") == target or target in node:
                return pruner.prune_impact(graph, node)
        return []

    def _make_summary(self, target: str, chunks: list[dict], entrypoints: list[dict]) -> str:
        if not chunks:
            return f"No context found for '{target}'."
        files = list(dict.fromkeys(c["file"] for c in chunks))
        symbols = list(dict.fromkeys(
            c["symbol"] for c in chunks if c.get("symbol") and self._valid_symbol(c["symbol"])
        ))
        parts = [f"Found {len(chunks)} chunk(s) across {len(files)} file(s)."]
        if symbols:
            parts.append(f"Key symbols: {', '.join(symbols[:5])}.")
        if entrypoints:
            parts.append(f"Entrypoint(s): {', '.join(e.get('symbol', e['file']) for e in entrypoints[:3])}.")
        return " ".join(parts)

    # --- Classification helpers ---

    def _classify_usage(self, snippet: str, symbol: str) -> str:
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

    def _relation_to_usage(self, relation: str) -> str:
        return {"defines": "definition", "imports": "import", "references": "read", "calls": "read"}.get(relation, "read")

    def _is_write(self, chunk: dict, target: str) -> bool:
        content = chunk.get("content", "")
        return f"{target} =" in content or f"{target}=" in content or f".{target} =" in content

    def _is_read(self, chunk: dict, target: str) -> bool:
        content = chunk.get("content", "")
        return target in content and not self._is_write(chunk, target)

    def _valid_symbol(self, name: str) -> bool:
        if not name or len(name) > 80:
            return False
        return not any(ch in name for ch in ("\n", "{", "}", "()", ";"))

    def _chunk_reason(self, target: str, row: dict) -> str:
        content = row.get("content", "").lower()
        if target.lower() in content:
            return f"Contains '{target}'"
        return "Semantically relevant"

    # --- Confidence ---

    def _score_confidence(self, items: list, rows: list[dict]) -> float:
        if not items:
            return 0.0
        if not rows:
            return 0.3
        top = rows[0].get("score", 0) if rows else 0
        item_factor = min(1.0, len(items) * 0.1)
        return round(min(0.95, top * 0.5 + item_factor * 0.4 + 0.1), 2)

    # --- Missing context detectors ---

    def _search_missing(self, refs: list, target: str) -> list[str]:
        if not refs:
            return [f"No references found for '{target}' — may not be indexed"]
        return []

    def _explain_missing(self, entrypoints: list, paths: list) -> list[str]:
        m = []
        if not entrypoints:
            m.append("No clear entrypoint found — results may be low relevance")
        if not paths:
            m.append("No dependency paths — code graph may not be built")
        return m

    def _refactor_missing(self, refs: list, paths: list) -> list[str]:
        m = []
        if not refs:
            m.append("No references found — symbol may not exist in indexed code")
        if not paths:
            m.append("No dependency paths — cannot verify full blast radius")
        files = [r["file"] for r in refs]
        if not any("migration" in f.lower() for f in files):
            m.append("No migration file found — may need manual check")
        if not any("test" in f.lower() or "spec" in f.lower() for f in files):
            m.append("No test file found — tests may need update")
        return m

    def _debug_missing(self, writes: list, reads: list, chain: list) -> list[str]:
        m = []
        if not writes:
            m.append("No write locations found — variable may be set indirectly")
        if not chain:
            m.append("No call chain — graph not available for flow tracing")
        return m

    def _generate_missing(self, chunks: list) -> list[str]:
        if not chunks:
            return ["No context found — cannot determine affected files"]
        return []

    # --- Action suggesters ---

    def _refactor_actions(self, target: str, files: list[str]) -> list[str]:
        actions = []
        has_entity = any("entity" in f.lower() or "model" in f.lower() for f in files)
        has_dto = any("dto" in f.lower() for f in files)
        has_service = any("service" in f.lower() for f in files)
        has_test = any("test" in f.lower() or "spec" in f.lower() for f in files)

        if has_entity:
            actions.append("Rename in entity/model definition")
        if has_dto:
            actions.append("Update DTO contracts")
        if has_service:
            actions.append("Update service logic")
        if has_test:
            actions.append("Update tests")
        if has_entity and not any("migration" in f.lower() for f in files):
            actions.append("Check if migration is needed")
        if not actions:
            actions.append(f"Update all {len(files)} file(s) containing '{target}'")
        return actions

    def _suggest_edge_cases(self, target: str, chunks: list[dict]) -> list[str]:
        """Suggest test edge cases based on code patterns."""
        cases = []
        for chunk in chunks:
            content = chunk.get("content", "")
            if "null" in content or "undefined" in content:
                cases.append("Null/undefined input")
            if "throw" in content or "Error" in content:
                cases.append("Error handling path")
            if "length" in content or "empty" in content:
                cases.append("Empty collection")
            if "0" in content and target.lower() in content.lower():
                cases.append("Zero value")
        return list(dict.fromkeys(cases))[:5]

    def _generate_actions(self, target: str, chunks: list[dict]) -> list[str]:
        actions = []
        files = [c["file"] for c in chunks]
        if any("entity" in f.lower() for f in files):
            actions.append("Add field to entity")
        if any("dto" in f.lower() for f in files):
            actions.append("Add field to DTO")
        if any("service" in f.lower() for f in files):
            actions.append("Update service logic")
        actions.append("Create migration if schema changed")
        return actions
