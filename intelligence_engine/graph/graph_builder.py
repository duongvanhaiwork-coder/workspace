from __future__ import annotations

import networkx as nx
from intelligence_engine.symbols.models import Symbol, ImportRef
from intelligence_engine.symbols.calls import CallRef
from intelligence_engine.symbols.routes import RouteSymbol
from . import relation_types as R

class GraphBuilder:
    def build(
        self,
        symbols: list[Symbol],
        imports: list[ImportRef],
        routes: list[RouteSymbol] | None = None,
        calls: list[CallRef] | None = None,
    ) -> nx.DiGraph:
        g = nx.DiGraph()

        # Build a lookup map: name -> list of symbol nodes (for call resolution)
        symbol_node_map: dict[str, list[str]] = {}  # qualified_name -> [node_id]

        for s in symbols:
            file_node = f"file:{s.file_path}"
            sym_node = f"symbol:{s.qualified_name or s.name}:{s.file_path}:{s.line_start}"
            g.add_node(file_node, type="file", path=s.file_path)
            g.add_node(
                sym_node, type="symbol",
                name=s.name, kind=s.kind, path=s.file_path,
                qualified_name=s.qualified_name or s.name,
                line_start=s.line_start,
            )
            g.add_edge(file_node, sym_node, relation=R.DEFINES)

            # Track for call resolution
            qname = s.qualified_name or s.name
            symbol_node_map.setdefault(qname, []).append(sym_node)
            # Also index by bare name for cross-file calls
            if s.name != qname:
                symbol_node_map.setdefault(s.name, []).append(sym_node)

        # Build class membership edges (method → class)
        class_nodes: dict[str, str] = {}  # file:classname -> node_id
        for s in symbols:
            if s.kind == "class":
                qname = s.qualified_name or s.name
                node_id = f"symbol:{qname}:{s.file_path}:{s.line_start}"
                class_nodes[f"{s.file_path}:{s.name}"] = node_id

        for s in symbols:
            if s.kind == "method" and s.qualified_name and "." in s.qualified_name:
                class_name = s.qualified_name.rsplit(".", 1)[0]
                class_key = f"{s.file_path}:{class_name}"
                if class_key in class_nodes:
                    method_node = f"symbol:{s.qualified_name}:{s.file_path}:{s.line_start}"
                    class_node = class_nodes[class_key]
                    g.add_edge(class_node, method_node, relation=R.DEFINES)

        for imp in imports:
            file_node = f"file:{imp.file_path}"
            mod_node = f"module:{imp.module}"
            g.add_node(file_node, type="file", path=imp.file_path)
            g.add_node(mod_node, type="module", name=imp.module)
            g.add_edge(file_node, mod_node, relation=R.IMPORTS, line=imp.line)

        for route in routes or []:
            file_node = f"file:{route.file_path}"
            route_node = f"route:{route.method}:{route.path}"
            g.add_node(file_node, type="file", path=route.file_path)
            g.add_node(route_node, type="route", method=route.method, path=route.path)
            g.add_edge(file_node, route_node, relation=R.ROUTE, line=route.line)

        # Add CALLS edges from call references
        self._add_call_edges(g, calls or [], symbols, symbol_node_map)

        return g

    def _add_call_edges(
        self,
        g: nx.DiGraph,
        calls: list[CallRef],
        symbols: list[Symbol],
        symbol_node_map: dict[str, list[str]],
    ) -> None:
        """Resolve call refs to graph nodes and add CALLS edges."""
        # Build caller lookup: (file_path, qualified_name, line_start) -> node_id
        caller_lookup: dict[tuple[str, str, int], str] = {}
        for s in symbols:
            qname = s.qualified_name or s.name
            node_id = f"symbol:{qname}:{s.file_path}:{s.line_start}"
            caller_lookup[(s.file_path, qname, s.line_start)] = node_id

        # Build callee resolution: try to match callee_name to known symbols
        # Strategy: match last segment of callee to symbol names
        # e.g. "configService.get" → try "get", "ConfigService.get", etc.
        for call in calls:
            caller_key = (call.caller_file_path, call.caller_qualified_name, call.caller_line_start)
            caller_node = caller_lookup.get(caller_key)
            if not caller_node or not g.has_node(caller_node):
                continue

            # Try to resolve callee
            callee_nodes = self._resolve_callee(call.callee_name, symbol_node_map)
            for callee_node in callee_nodes:
                if callee_node != caller_node:  # No self-edges
                    g.add_edge(caller_node, callee_node, relation=R.CALLS, line=call.call_line)

    @staticmethod
    def _resolve_callee(
        callee_name: str, symbol_node_map: dict[str, list[str]],
    ) -> list[str]:
        """Resolve a callee name to graph node IDs.

        Tries multiple resolution strategies:
        1. Exact match on qualified_name
        2. Match on last segment (method name) for member calls
        3. Match "ClassName.methodName" pattern for this.xxx calls
        """
        # 1. Direct match
        if callee_name in symbol_node_map:
            return symbol_node_map[callee_name]

        # 2. For member chains like "service.method", try the last part
        if "." in callee_name:
            parts = callee_name.split(".")
            last = parts[-1]
            # Try "SomeClass.lastPart" patterns in symbol_node_map
            candidates = []
            for qname, nodes in symbol_node_map.items():
                if qname.endswith(f".{last}"):
                    candidates.extend(nodes)
            if candidates:
                return candidates

            # Fallback: just the bare method name
            if last in symbol_node_map:
                return symbol_node_map[last]

        return []

    def add_call_edges(
        self, g: nx.DiGraph, calls: list[tuple[str, str, str, int]],
    ) -> None:
        """Add CALLS edges to an existing graph.

        Args:
            g: The graph to add edges to.
            calls: List of (caller_node_id, callee_node_id, file_path, line).
        """
        for caller, callee, file_path, line in calls:
            if g.has_node(caller) and g.has_node(callee):
                g.add_edge(caller, callee, relation=R.CALLS, line=line)
