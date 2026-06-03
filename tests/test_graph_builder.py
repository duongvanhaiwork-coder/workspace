from intelligence_engine.graph.graph_builder import GraphBuilder
from intelligence_engine.graph import relation_types as R
from intelligence_engine.symbols.models import Symbol, ImportRef
from intelligence_engine.symbols.routes import RouteSymbol


def test_build_symbols_and_imports():
    symbols = [
        Symbol("MyClass", "class", "a.py", 1, 10, "MyClass"),
        Symbol("my_func", "function", "b.py", 5, 8, "my_func"),
    ]
    imports = [
        ImportRef("os", "a.py", 1),
        ImportRef("./b", "a.py", 2),
    ]
    graph = GraphBuilder().build(symbols, imports)

    assert "file:a.py" in graph
    assert "file:b.py" in graph
    assert "symbol:MyClass:a.py:1" in graph
    assert "symbol:my_func:b.py:5" in graph
    assert "module:os" in graph
    assert "module:./b" in graph

    # Check edges
    assert graph.has_edge("file:a.py", "symbol:MyClass:a.py:1")
    assert graph["file:a.py"]["symbol:MyClass:a.py:1"]["relation"] == R.DEFINES
    assert graph.has_edge("file:a.py", "module:os")
    assert graph["file:a.py"]["module:os"]["relation"] == R.IMPORTS


def test_build_with_routes():
    symbols = [Symbol("handler", "function", "routes.ts", 3, 6, "handler")]
    imports = []
    routes = [RouteSymbol("GET", "/api/users", "routes.ts", 3)]

    graph = GraphBuilder().build(symbols, imports, routes)

    assert "route:GET:/api/users" in graph
    assert graph.has_edge("file:routes.ts", "route:GET:/api/users")
    assert graph["file:routes.ts"]["route:GET:/api/users"]["relation"] == R.ROUTE


def test_build_empty():
    graph = GraphBuilder().build([], [], [])
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0
