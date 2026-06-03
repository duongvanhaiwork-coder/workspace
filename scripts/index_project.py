"""Index a project — supports incremental mode (default) and full reindex (--full)."""
from pathlib import Path
import sys

from intelligence_engine.project_loader.loader import ProjectLoader
from intelligence_engine.scanner.scanner import Scanner
from intelligence_engine.parser.factory import ParserFactory
from intelligence_engine.symbols.extractor import SymbolExtractor
from intelligence_engine.symbols.imports import ImportExtractor
from intelligence_engine.symbols.routes import RouteExtractor
from intelligence_engine.chunking.chunker import Chunker
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.graph.graph_builder import GraphBuilder
from intelligence_engine.storage import (
    get_vector_store,
    get_graph_store,
    get_file_state_store,
    get_symbol_index_store,
    get_relationship_index_store,
)


def index_project(project_name: str, full: bool = False) -> None:
    project = ProjectLoader().get(project_name)
    root = project.resolved_path(Path.cwd())
    scanner = Scanner(project.exclude)
    all_states = scanner.scan(root)

    file_state_store = get_file_state_store()
    changed, deleted = file_state_store.diff(all_states, project=project_name)

    if not full and not changed and not deleted:
        print(f"project={project_name} — no changes detected, skipping.")
        return

    states_to_process = all_states if full else changed

    parser_factory = ParserFactory()
    sym_extractor = SymbolExtractor()
    imp_extractor = ImportExtractor()
    route_extractor = RouteExtractor()
    chunker = Chunker()
    embedder = Embedder()
    store = get_vector_store()

    # Parse all files once, cache results for both chunking and graph building
    parsed_cache: dict[str, tuple] = {}  # rel_path -> (symbols, imports, routes, chunks)

    for state in all_states:
        path = root / state.file_path
        parsed = parser_factory.get_parser(path).parse(path, rel_path=state.file_path)
        file_symbols = sym_extractor.extract(parsed)
        file_imports = imp_extractor.extract(parsed)
        file_routes = route_extractor.extract(parsed)
        file_chunks = chunker.chunk(parsed, file_symbols)
        parsed_cache[state.file_path] = (file_symbols, file_imports, file_routes, file_chunks)

    # Upsert only changed file chunks
    chunks_to_upsert = []
    for state in states_to_process:
        _, _, _, file_chunks = parsed_cache[state.file_path]
        chunks_to_upsert.extend(file_chunks)

    if chunks_to_upsert:
        store.upsert_chunks(
            chunks_to_upsert,
            embedder.embed_many([c.content for c in chunks_to_upsert]),
            project=project_name,
        )

    # Remove chunks for deleted files
    for del_path in deleted:
        store.delete_by_file(del_path, project=project_name)

    # Build graph from all parsed data
    all_symbols = []
    all_imports = []
    all_routes = []
    for symbols, imports, routes, _ in parsed_cache.values():
        all_symbols.extend(symbols)
        all_imports.extend(imports)
        all_routes.extend(routes)

    graph = GraphBuilder().build(all_symbols, all_imports, all_routes)
    get_graph_store().save(graph, project=project_name)

    # Populate symbol index
    sym_store = get_symbol_index_store()
    sym_entries = []
    for sym in all_symbols:
        sym_entries.append({
            "name": sym.name,
            "qualified_name": sym.qualified_name or sym.name,
            "kind": sym.kind,
            "file_path": sym.file_path,
            "line_start": sym.line_start,
            "line_end": sym.line_end,
            "signature": sym.signature,
        })
    sym_store.clear(project=project_name)
    if sym_entries:
        sym_store.upsert_batch(sym_entries, project=project_name)

    # Populate relationship index from graph edges
    rel_store = get_relationship_index_store()
    rel_store.clear(project=project_name)
    _build_relationship_index(
        rel_store, all_symbols, all_imports, graph, project_name,
    )

    # Mark all states as indexed before saving
    indexed_states = [s.mark_indexed() for s in all_states]
    file_state_store.save(indexed_states, project=project_name)

    mode = "full" if full else "incremental"
    print(
        f"indexed project={project_name} mode={mode} "
        f"processed_files={len(states_to_process)} total_files={len(all_states)} "
        f"chunks={len(chunks_to_upsert)} deleted_files={len(deleted)} "
        f"symbols={len(all_symbols)} imports={len(all_imports)} routes={len(all_routes)}"
    )


def _build_relationship_index(rel_store, all_symbols, all_imports, graph, project):
    """Build relationship index from graph edges per symbol."""
    from intelligence_engine.graph import relation_types as R

    # Build a map: symbol_name -> file_path
    sym_file_map: dict[str, str] = {}
    for sym in all_symbols:
        key = sym.qualified_name or sym.name
        sym_file_map[key] = sym.file_path

    # Traverse graph to build per-symbol relationships
    entries: dict[str, dict] = {}

    for node, data in graph.nodes(data=True):
        if data.get("type") != "symbol":
            continue
        name = data.get("name", "")
        if not name:
            continue

        entry = entries.setdefault(name, {
            "symbol": name,
            "file_path": data.get("path", sym_file_map.get(name, "")),
            "reads": [],
            "writes": [],
            "calls": [],
            "called_by": [],
            "uses_dto": [],
            "uses_model": [],
        })

        # Outgoing edges (what this symbol does)
        for succ in graph.successors(node):
            succ_data = graph.nodes[succ]
            edge = graph.edges[node, succ]
            relation = edge.get("relation", "")
            target_name = succ_data.get("name", "")
            if not target_name:
                continue

            if relation == R.CALLS:
                entry["calls"].append(target_name)
            elif relation == R.READS:
                entry["reads"].append(target_name)
            elif relation == R.WRITES:
                entry["writes"].append(target_name)
            elif relation == R.USES_DTO:
                entry["uses_dto"].append(target_name)
            elif relation == R.USES_MODEL:
                entry["uses_model"].append(target_name)

        # Incoming edges (what calls this symbol)
        for pred in graph.predecessors(node):
            pred_data = graph.nodes[pred]
            edge = graph.edges[pred, node]
            relation = edge.get("relation", "")
            source_name = pred_data.get("name", "")
            if not source_name or pred_data.get("type") != "symbol":
                continue

            if relation == R.CALLS:
                entry["called_by"].append(source_name)

    if entries:
        rel_store.upsert_batch(list(entries.values()), project=project)


if __name__ == "__main__":
    name = "business-lounge-api"
    full_reindex = False
    for arg in sys.argv[1:]:
        if arg == "--full":
            full_reindex = True
        else:
            name = arg
    index_project(name, full=full_reindex)
