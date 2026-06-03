from dataclasses import dataclass
from pathlib import Path
import hashlib

@dataclass(frozen=True)
class FileState:
    path: str
    sha256: str
    size: int


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()
