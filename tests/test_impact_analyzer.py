import networkx as nx
from intelligence_engine.graph.impact_analyzer import ImpactAnalyzer


def test_analyze_direct_dependents():
    g = nx.DiGraph()
    g.add_node("file:a.py", type="file")
    g.add_node("file:b.py", type="file")
    g.add_node("module:a", type="module")
    # b.py imports module:a, a.py defines module:a
    g.add_edge("file:a.py", "module:a", relation="defines")
    g.add_edge("file:b.py", "module:a", relation="imports")

    # Analyze impact on module:a — who depends on it?
    result = ImpactAnalyzer().analyze(g, "module:a", depth=2)
    nodes = [r["node"] for r in result]
    assert "file:a.py" in nodes
    assert "file:b.py" in nodes


def test_analyze_nonexistent_node():
    g = nx.DiGraph()
    g.add_node("file:a.py", type="file")
    result = ImpactAnalyzer().analyze(g, "file:nonexistent.py", depth=2)
    assert result == []


def test_analyze_depth_limit():
    g = nx.DiGraph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "D")

    # depth=1 from D: only C should be impacted (reverse graph)
    result = ImpactAnalyzer().analyze(g, "D", depth=1)
    nodes = [r["node"] for r in result]
    assert "C" in nodes
    assert "B" not in nodes
