from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import hashlib


@dataclass(frozen=True)
class FileState:
    file_path: str
    content_hash: str
    size_bytes: int
    language: str = ""
    absolute_path: str = ""
    last_modified_at: str = ""
    last_indexed_at: str = ""
    status: str = "pending"  # pending | indexed | error


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def detect_language(path: Path) -> str:
    """Detect language from file extension."""
    ext_map = {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".py": "python",
        ".cs": "csharp",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".vue": "vue",
        ".svelte": "svelte",
    }
    return ext_map.get(path.suffix.lower(), "")
