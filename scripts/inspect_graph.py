from intelligence_engine.storage import get_graph_store

g = get_graph_store().load()
print(f"nodes={g.number_of_nodes()} edges={g.number_of_edges()}")
for node, data in list(g.nodes(data=True))[:50]:
    print(node, data)
