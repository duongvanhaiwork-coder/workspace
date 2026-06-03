import networkx as nx
from intelligence_engine.symbols.models import Symbol, ImportRef
from intelligence_engine.symbols.routes import RouteSymbol
from . import relation_types as R

class GraphBuilder:
    def build(
        self,
        symbols: list[Symbol],
        imports: list[ImportRef],
        routes: list[RouteSymbol] | None = None,
    ) -> nx.DiGraph:
        g = nx.DiGraph()
        for s in symbols:
            file_node = f"file:{s.file_path}"
            sym_node = f"symbol:{s.name}:{s.file_path}:{s.start_line}"
            g.add_node(file_node, type="file", path=s.file_path)
            g.add_node(sym_node, type="symbol", name=s.name, kind=s.kind, path=s.file_path)
            g.add_edge(file_node, sym_node, relation=R.DEFINES)
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
        return g
