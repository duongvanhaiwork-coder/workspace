from pathlib import Path
from .file_state import FileState, hash_file

DEFAULT_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".cs"}

class Scanner:
    def __init__(self, exclude: list[str] | None = None, extensions: set[str] | None = None) -> None:
        self.exclude = set(exclude or [])
        self.extensions = extensions or DEFAULT_EXTENSIONS

    def should_skip(self, path: Path) -> bool:
        parts = set(path.parts)
        return bool(parts & self.exclude) or path.suffix not in self.extensions

    def scan(self, root: Path) -> list[FileState]:
        root = Path(root)
        states: list[FileState] = []
        for path in root.rglob("*"):
            if path.is_file() and not self.should_skip(path):
                rel = path.relative_to(root).as_posix()
                states.append(FileState(path=rel, sha256=hash_file(path), size=path.stat().st_size))
        return states
