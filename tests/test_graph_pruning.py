"""Tests for graph pruning — noise reduction in traversal results."""

import networkx as nx

from intelligence_engine.graph.pruning import (
    GraphPruner,
    PruningConfig,
    prune_dependency_paths,
)


def _build_test_graph() -> nx.DiGraph:
    """Build a realistic graph with service, entity, util, test nodes."""
    g = nx.DiGraph()

    # Core files
    g.add_node("file:src/service/OrderService.ts", type="file", path="src/service/OrderService.ts")
    g.add_node("file:src/entity/Order.ts", type="file", path="src/entity/Order.ts")
    g.add_node("file:src/dto/OrderDto.ts", type="file", path="src/dto/OrderDto.ts")
    g.add_node("file:src/repository/OrderRepository.ts", type="file", path="src/repository/OrderRepository.ts")
    g.add_node("file:src/controller/OrderController.ts", type="file", path="src/controller/OrderController.ts")

    # Noise files
    g.add_node("file:src/utils/logger.ts", type="file", path="src/utils/logger.ts")
    g.add_node("file:src/utils/date.util.ts", type="file", path="src/utils/date.util.ts")
    g.add_node("file:src/shared/constants.ts", type="file", path="src/shared/constants.ts")
    g.add_node("file:src/common/helpers.ts", type="file", path="src/common/helpers.ts")

    # Test files
    g.add_node("file:src/service/OrderService.spec.ts", type="file", path="src/service/OrderService.spec.ts")
    g.add_node("file:tests/test_order.py", type="file", path="tests/test_order.py")

    # Target symbol
    g.add_node("symbol:ServiceProviderId", type="symbol", name="ServiceProviderId", kind="property", path="src/entity/Order.ts")

    # Edges: things that depend on the symbol
    g.add_edge("file:src/entity/Order.ts", "symbol:ServiceProviderId", relation="defines")
    g.add_edge("file:src/service/OrderService.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/dto/OrderDto.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/repository/OrderRepository.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/controller/OrderController.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/utils/logger.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/utils/date.util.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/shared/constants.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/common/helpers.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:src/service/OrderService.spec.ts", "symbol:ServiceProviderId", relation="references")
    g.add_edge("file:tests/test_order.py", "symbol:ServiceProviderId", relation="references")

    return g


# --- GraphPruner ---


def test_pruner_removes_noise_nodes():
    """Noise nodes (utils, shared, helpers) should be deprioritized."""
    g = _build_test_graph()
    pruner = GraphPruner(PruningConfig(max_nodes=5, include_tests=False))
    result = pruner.prune_impact(g, "symbol:ServiceProviderId", depth=2)

    paths = [r.get("path", "") for r in result]
    # Core files should be present
    assert any("OrderService.ts" in p for p in paths)
    assert any("Order.ts" in p or "entity" in p for p in paths)
    # Noise should be filtered out or ranked low
    assert not any("logger" in p for p in paths[:3])


def test_pruner_excludes_tests_by_default():
    """Test files excluded when include_tests=False."""
    g = _build_test_graph()
    pruner = GraphPruner(PruningConfig(max_nodes=20, include_tests=False))
    result = pruner.prune_impact(g, "symbol:ServiceProviderId", depth=2)

    paths = [r.get("path", "") for r in result]
    assert not any(".spec." in p or "test_" in p for p in paths)


def test_pruner_includes_tests_when_configured():
    """Test files included when include_tests=True."""
    g = _build_test_graph()
    pruner = GraphPruner(PruningConfig(max_nodes=20, include_tests=True))
    result = pruner.prune_impact(g, "symbol:ServiceProviderId", depth=2)

    paths = [r.get("path", "") for r in result]
    assert any(".spec." in p or "test_" in p for p in paths)


def test_pruner_respects_max_nodes():
    """Result should not exceed max_nodes."""
    g = _build_test_graph()
    pruner = GraphPruner(PruningConfig(max_nodes=3))
    result = pruner.prune_impact(g, "symbol:ServiceProviderId", depth=2)
    assert len(result) <= 3


def test_pruner_priority_files_rank_higher():
    """Entity, DTO, Service files rank higher than utils."""
    g = _build_test_graph()
    pruner = GraphPruner(PruningConfig(max_nodes=10, include_tests=False))
    result = pruner.prune_impact(g, "symbol:ServiceProviderId", depth=2)

    if len(result) >= 3:
        top_3_paths = [r.get("path", "") for r in result[:3]]
        # At least one of entity/dto/service should be in top 3
        assert any(
            "entity" in p or "dto" in p or "service" in p or "repository" in p
            for p in top_3_paths
        )


def test_pruner_nonexistent_node():
    """Nonexistent node returns empty."""
    g = _build_test_graph()
    pruner = GraphPruner()
    result = pruner.prune_impact(g, "nonexistent:node", depth=2)
    assert result == []


def test_pruner_empty_graph():
    """Empty graph returns empty."""
    g = nx.DiGraph()
    pruner = GraphPruner()
    result = pruner.prune_impact(g, "anything", depth=2)
    assert result == []


# --- prune_dependency_paths ---


def test_prune_paths_keeps_priority():
    """Paths involving entity/DTO/service are always kept."""
    paths = [
        {"source": "OrderService", "target": "ServiceProviderId", "relation": "references"},
        {"source": "OrderDto", "target": "ServiceProviderId", "relation": "references"},
        {"source": "logger", "target": "ServiceProviderId", "relation": "references"},
    ]
    result = prune_dependency_paths(paths)
    sources = [p["source"] for p in result]
    assert "OrderService" in sources
    assert "OrderDto" in sources


def test_prune_paths_removes_noise_to_noise():
    """Paths connecting two noise nodes are removed."""
    paths = [
        {"source": "src/utils/a.ts", "target": "src/shared/b.ts", "relation": "imports"},
        {"source": "src/service/Order.ts", "target": "ServiceProviderId", "relation": "references"},
    ]
    result = prune_dependency_paths(paths)
    # noise→noise should be removed
    assert len(result) == 1
    assert result[0]["source"] == "src/service/Order.ts"


def test_prune_paths_respects_max_nodes():
    """Result limited by config max_nodes."""
    paths = [{"source": f"src/entity/file{i}.ts", "target": "X", "relation": "imports"} for i in range(100)]
    config = PruningConfig(max_nodes=10)
    result = prune_dependency_paths(paths, config=config)
    assert len(result) <= 10


def test_prune_paths_empty_input():
    """Empty paths returns empty."""
    assert prune_dependency_paths([]) == []
