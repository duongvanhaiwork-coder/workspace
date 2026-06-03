import json
from pathlib import Path
import networkx as nx
from networkx.readwrite import json_graph


class GraphStore:
    """Persist NetworkX graph as JSON (safe, inspectable, no pickle deserialization risk)."""

    def __init__(self, path: str | Path = "data/graph/code_graph.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, graph: nx.DiGraph) -> None:
        data = json_graph.node_link_data(graph)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self) -> nx.DiGraph:
        if not self.path.exists():
            return nx.DiGraph()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return json_graph.node_link_graph(data, directed=True)
