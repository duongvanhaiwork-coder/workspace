"""Graph pruning — reduce noise in dependency traversal.

When traversing a code graph for impact analysis or dependency paths,
raw traversal returns too many irrelevant nodes (utils, constants, loggers).

GraphPruner filters out noise nodes and keeps only architecturally significant
results, dramatically reducing token usage while preserving accuracy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import networkx as nx


# --- Default noise patterns ---

# File path patterns to deprioritize (still included if directly connected)
NOISE_PATH_PATTERNS: list[re.Pattern] = [
    re.compile(r"(^|/)utils?(/|\.)", re.I),
    re.compile(r"(^|/)helpers?(/|\.)", re.I),
    re.compile(r"(^|/)constants?(/|\.)", re.I),
    re.compile(r"(^|/)config(/|\.)", re.I),
    re.compile(r"(^|/)logger(/|\.)", re.I),
    re.compile(r"(^|/)shared(/|\.)", re.I),
    re.compile(r"(^|/)common(/|\.)", re.I),
    re.compile(r"(^|/)index\.(ts|js)$", re.I),
    re.compile(r"\.spec\.(ts|js)$", re.I),
    re.compile(r"\.test\.(ts|js|py)$", re.I),
    re.compile(r"(^|/)test_", re.I),
    re.compile(r"(^|/)__tests__/", re.I),
]

# File path patterns that are HIGH priority (always keep)
PRIORITY_PATH_PATTERNS: list[re.Pattern] = [
    re.compile(r"(^|/)entit(y|ies)(/|\.)", re.I),
    re.compile(r"(^|/)model(s)?(/|\.)", re.I),
    re.compile(r"(^|/)dto(/|\.)", re.I),
    re.compile(r"(^|/)Dto(/|\.)", re.I),
    re.compile(r"(^|/)repositor(y|ies)(/|\.)", re.I),
    re.compile(r"(^|/)service(s)?(/|\.)", re.I),
    re.compile(r"(^|/)controller(s)?(/|\.)", re.I),
    re.compile(r"(^|/)migration(s)?(/|\.)", re.I),
    re.compile(r"(^|/)guard(s)?(/|\.)", re.I),
    re.compile(r"(^|/)pipe(s)?(/|\.)", re.I),
    re.compile(r"(^|/)interceptor(s)?(/|\.)", re.I),
]


@dataclass
class PruningConfig:
    """Configuration for graph pruning behavior."""

    # Maximum traversal depth
    max_depth: int = 2

    # Maximum total nodes in result
    max_nodes: int = 50

    # Noise patterns (paths to deprioritize)
    noise_patterns: list[re.Pattern] = field(default_factory=lambda: list(NOISE_PATH_PATTERNS))

    # Priority patterns (paths to always keep)
    priority_patterns: list[re.Pattern] = field(default_factory=lambda: list(PRIORITY_PATH_PATTERNS))

    # Whether to include test files in impact results
    include_tests: bool = False

    # Minimum score threshold for keeping a node (0.0 = keep all)
    min_relevance: float = 0.0


class GraphPruner:
    """Prune graph traversal results to remove noise and keep relevant nodes.

    Usage:
        pruner = GraphPruner()
        raw_nodes = get_all_impacted_nodes(graph, target, depth=3)
        pruned = pruner.prune(raw_nodes, target)
    """

    def __init__(self, config: PruningConfig | None = None) -> None:
        self.config = config or PruningConfig()

    def prune_impact(
        self,
        graph: nx.DiGraph,
        target_node: str,
        depth: int | None = None,
    ) -> list[dict]:
        """Traverse graph from target and return pruned impact results.

        Args:
            graph: the code graph
            target_node: starting node ID in the graph
            depth: traversal depth (default from config)

        Returns:
            Pruned list of impacted nodes, sorted by relevance.
        """
        max_depth = depth or self.config.max_depth

        if target_node not in graph:
            return []

        # Reverse traversal: find what depends on target
        raw: list[dict] = []
        for node, distance in nx.single_source_shortest_path_length(
            graph.reverse(copy=False), target_node, cutoff=max_depth
        ).items():
            if node == target_node:
                continue
            data = dict(graph.nodes[node])
            data["node"] = node
            data["distance"] = distance
            raw.append(data)

        return self._apply_pruning(raw)

    def prune_nodes(self, nodes: list[dict]) -> list[dict]:
        """Prune an already-collected list of nodes."""
        return self._apply_pruning(nodes)

    def _apply_pruning(self, nodes: list[dict]) -> list[dict]:
        """Core pruning logic: score, filter, sort, limit."""
        scored: list[tuple[float, dict]] = []

        for node in nodes:
            score = self._score_node(node)
            # -1.0 means hard exclude
            if score < 0:
                continue
            if score >= self.config.min_relevance:
                node["_relevance"] = score
                scored.append((score, node))

        # Sort by: relevance DESC, then distance ASC (closer = more relevant)
        scored.sort(key=lambda x: (-x[0], x[1].get("distance", 99)))

        # Limit to max_nodes
        result = [item for _, item in scored[: self.config.max_nodes]]

        # Clean up internal scoring field
        for r in result:
            r.pop("_relevance", None)

        return result

    def _score_node(self, node: dict) -> float:
        """Score a node by relevance. Higher = more relevant.

        Returns -1.0 for nodes that should be excluded entirely.
        """
        path = node.get("path", "") or node.get("node", "")
        node_type = node.get("type", "")
        distance = node.get("distance", 1)

        # Hard exclude: test files when not configured
        if self._is_test(path) and not self.config.include_tests:
            return -1.0

        # Base score from distance (closer = higher)
        score = 1.0 / distance if distance > 0 else 1.0

        # Priority boost
        if self._matches_priority(path):
            score += 0.5

        # Noise penalty
        if self._matches_noise(path):
            score -= 0.4

        # Type-based boost
        if node_type == "symbol":
            score += 0.1  # symbols more specific than files
        elif node_type == "module":
            score -= 0.1  # modules are often barrel exports

        return max(0.0, score)

    def _matches_priority(self, path: str) -> bool:
        return any(p.search(path) for p in self.config.priority_patterns)

    def _matches_noise(self, path: str) -> bool:
        return any(p.search(path) for p in self.config.noise_patterns)

    def _is_test(self, path: str) -> bool:
        lower = path.lower()
        return (
            ".spec." in lower
            or ".test." in lower
            or "/test_" in lower
            or "/__tests__/" in lower
            or lower.startswith("test_")
        )


def prune_dependency_paths(
    paths: list[dict],
    config: PruningConfig | None = None,
) -> list[dict]:
    """Prune dependency paths, removing noise edges.

    Keeps paths involving priority patterns, removes paths that
    only connect noise nodes.
    """
    cfg = config or PruningConfig()
    pruner = GraphPruner(cfg)

    result: list[dict] = []
    for path in paths:
        source = path.get("source", "")
        target = path.get("target", "")

        # Always keep if either end is a priority pattern
        if pruner._matches_priority(source) or pruner._matches_priority(target):
            result.append(path)
            continue

        # Skip if both ends are noise
        if pruner._matches_noise(source) and pruner._matches_noise(target):
            continue

        # Keep otherwise
        result.append(path)

    return result[: cfg.max_nodes]
