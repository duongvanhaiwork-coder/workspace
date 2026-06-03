import networkx as nx


class ImpactAnalyzer:
    def analyze(self, graph: nx.DiGraph, node: str, depth: int = 2) -> list[dict]:
        if node not in graph:
            return []
        impacted = []
        reversed_graph = graph.reverse(copy=False)
        path_lengths = nx.single_source_shortest_path_length(
            reversed_graph, node, cutoff=depth,
        )
        for target, distance in path_lengths.items():
            if target != node:
                impacted.append({
                    "node": target,
                    "distance": distance,
                    "data": graph.nodes[target],
                })
        return impacted
