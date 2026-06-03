import networkx as nx

class GraphReferenceFinder:
    def find_references(self, graph: nx.DiGraph, symbol_name: str) -> list[dict]:
        matches = []
        for node, data in graph.nodes(data=True):
            if data.get("name") == symbol_name or symbol_name in node:
                matches.append({"node": node, "data": data})
        return matches
