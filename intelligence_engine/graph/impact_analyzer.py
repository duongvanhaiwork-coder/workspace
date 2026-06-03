import networkx as nx

class ImpactAnalyzer:
    def analyze(self, graph: nx.DiGraph, node: str, depth: int = 2) -> list[dict]:
        if node not in graph:
            return []
        impacted = []
        for target, distance in nx.single_source_shortest_path_length(graph.reverse(copy=False), node, cutoff=depth).items():
            if target != node:
                impacted.append({"node": target, "distance": distance, "data": graph.nodes[target]})
        return impacted
