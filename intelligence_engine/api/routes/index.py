from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from intelligence_engine.project_loader.loader import ProjectLoader
from intelligence_engine.scanner.scanner import Scanner
from intelligence_engine.parser.factory import ParserFactory
from intelligence_engine.symbols.extractor import SymbolExtractor
from intelligence_engine.symbols.imports import ImportExtractor
from intelligence_engine.symbols.routes import RouteExtractor
from intelligence_engine.chunking.chunker import Chunker
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.graph.graph_builder import GraphBuilder
from intelligence_engine.storage import get_vector_store, get_graph_store, get_file_state_store

router = APIRouter()


class IndexRequest(BaseModel):
    full: bool = False


class IndexResponse(BaseModel):
    project: str
    mode: str
    processed_files: int
    total_files: int
    deleted_files: int
    chunks: int
    symbols: int
    imports: int
    routes: int


@router.post("/{project_name}", response_model=IndexResponse)
def index_project(project_name: str, req: IndexRequest | None = None):
    full = req.full if req else False
    project = ProjectLoader().get(project_name)
    root = project.resolved_path(Path.cwd())
    scanner = Scanner(project.exclude)
    all_states = scanner.scan(root)

    file_state_store = get_file_state_store()
    changed, deleted = file_state_store.diff(all_states, project=project_name)
    states_to_process = all_states if full else changed

    parser_factory = ParserFactory()
    sym_extractor = SymbolExtractor()
    imp_extractor = ImportExtractor()
    route_extractor = RouteExtractor()
    chunker = Chunker()
    embedder = Embedder()
    store = get_vector_store()

    # Parse all files once, cache for chunking + graph
    parsed_cache: dict[str, tuple] = {}
    for state in all_states:
        path = root / state.file_path
        parsed = parser_factory.get_parser(path).parse(path, rel_path=state.file_path)
        file_symbols = sym_extractor.extract(parsed)
        file_imports = imp_extractor.extract(parsed)
        file_routes = route_extractor.extract(parsed)
        file_chunks = chunker.chunk(parsed, file_symbols)
        parsed_cache[state.file_path] = (file_symbols, file_imports, file_routes, file_chunks)

    # Upsert chunks for changed files only
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

    # Cleanup deleted files
    for del_path in deleted:
        store.delete_by_file(del_path, project=project_name)

    # Build graph from all data
    all_symbols = []
    all_imports = []
    all_routes = []
    for symbols, imports, routes, _ in parsed_cache.values():
        all_symbols.extend(symbols)
        all_imports.extend(imports)
        all_routes.extend(routes)

    graph = GraphBuilder().build(all_symbols, all_imports, all_routes)
    get_graph_store().save(graph, project=project_name)
    file_state_store.save(all_states, project=project_name)

    mode = "full" if full else "incremental"
    return IndexResponse(
        project=project_name,
        mode=mode,
        processed_files=len(states_to_process),
        total_files=len(all_states),
        deleted_files=len(deleted),
        chunks=len(chunks_to_upsert),
        symbols=len(all_symbols),
        imports=len(all_imports),
        routes=len(all_routes),
    )
