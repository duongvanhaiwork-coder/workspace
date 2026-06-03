import json
from pathlib import Path
import networkx as nx
from networkx.readwrite import json_graph


class GraphStore:
    """Persist NetworkX graph as JSON (safe, inspectable, no pickle deserialization risk).

    Supports per-project scoping: each project gets its own graph file.
    """

    def __init__(self, base_dir: str | Path = "data/graph") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _project_path(self, project: str) -> Path:
        safe_name = project.replace("/", "_").replace("\\", "_")
        return self.base_dir / f"{safe_name}.json"

    def save(self, graph: nx.DiGraph, project: str = "__default__") -> None:
        data = json_graph.node_link_data(graph)
        self._project_path(project).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, project: str = "__default__") -> nx.DiGraph:
        path = self._project_path(project)
        if not path.exists():
            return nx.DiGraph()
        data = json.loads(path.read_text(encoding="utf-8"))
        return json_graph.node_link_graph(data, directed=True)
