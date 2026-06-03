from dataclasses import dataclass
from pathlib import Path

@dataclass
class ParsedFile:
    path: str
    language: str
    source: str
    tree: object | None = None

class BaseParser:
    language: str = "unknown"

    def parse(
        self, path: Path, source: str | None = None, rel_path: str | None = None,
    ) -> ParsedFile:
        """Parse a file.

        Args:
            path: Absolute path to read from disk.
            source: Optional source text (skips disk read).
            rel_path: Relative path to store in ParsedFile.path (defaults to str(path)).
        """
        text = source if source is not None else path.read_text(encoding="utf-8", errors="ignore")
        stored_path = rel_path if rel_path is not None else str(path)
        return ParsedFile(path=stored_path, language=self.language, source=text, tree=None)
