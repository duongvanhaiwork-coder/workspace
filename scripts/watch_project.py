"""Watch a project directory and incrementally re-index changed files."""
from pathlib import Path
import time

from intelligence_engine.project_loader.loader import ProjectLoader
from intelligence_engine.scanner.scanner import Scanner
from intelligence_engine.scanner.watcher import Watcher
from intelligence_engine.parser.factory import ParserFactory
from intelligence_engine.symbols.extractor import SymbolExtractor
from intelligence_engine.symbols.imports import ImportExtractor
from intelligence_engine.symbols.routes import RouteExtractor
from intelligence_engine.chunking.chunker import Chunker
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.storage import get_vector_store, get_file_state_store

project = ProjectLoader().load_all()[0]
root = project.resolved_path(Path.cwd())
scanner = Scanner(project.exclude)
parser_factory = ParserFactory()
sym_extractor = SymbolExtractor()
imp_extractor = ImportExtractor()
route_extractor = RouteExtractor()
chunker = Chunker()
embedder = Embedder()
store = get_vector_store()


def on_change(path: Path) -> None:
    if scanner.should_skip(path):
        return
    try:
        rel = path.relative_to(root).as_posix()
        parsed = parser_factory.get_parser(path).parse(path, rel_path=rel)
    except (OSError, UnicodeDecodeError, ValueError):
        return

    # Remove old chunks for this file, then insert new ones
    store.delete_by_file(rel, project=project.name)

    file_symbols = sym_extractor.extract(parsed)
    chunks = chunker.chunk(parsed, file_symbols)
    if chunks:
        store.upsert_chunks(
            chunks, embedder.embed_many([c.content for c in chunks]), project=project.name
        )
    print(f"re-indexed: {rel} ({len(chunks)} chunks)")


def on_delete(path: Path) -> None:
    if scanner.should_skip(path):
        return
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return
    removed = store.delete_by_file(rel, project=project.name)
    print(f"deleted: {rel} (removed {removed} chunks)")


watcher = Watcher(root, on_change, on_delete)
watcher.start()
print(f"watching {root} (project={project.name})")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    watcher.stop()
    # Save final file state
    states = scanner.scan(root)
    get_file_state_store().save(states)
    print("stopped, file state saved.")
