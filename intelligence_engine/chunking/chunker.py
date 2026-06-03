import hashlib
from intelligence_engine.parser.base import ParsedFile
from intelligence_engine.symbols.models import Symbol
from .models import CodeChunk


class Chunker:
    def chunk(self, parsed: ParsedFile, symbols: list[Symbol] | None = None) -> list[CodeChunk]:
        lines = parsed.source.splitlines()
        if symbols:
            chunks = []
            for s in symbols:
                content = "\n".join(lines[max(s.start_line - 1, 0):s.end_line])
                chunks.append(self._make(parsed, content, s.start_line, s.end_line, s.name))
            return chunks
        return self._by_window(parsed, lines)

    def _by_window(self, parsed: ParsedFile, lines: list[str], size: int = 120) -> list[CodeChunk]:
        chunks = []
        for start in range(0, len(lines), size):
            end = min(start + size, len(lines))
            chunks.append(self._make(parsed, "\n".join(lines[start:end]), start + 1, end, None))
        return chunks

    def _make(self, parsed: ParsedFile, content: str, start: int, end: int, symbol: str | None) -> CodeChunk:
        raw = f"{parsed.path}:{start}:{end}:{symbol or ''}:{content[:64]}"
        cid = hashlib.sha1(raw.encode()).hexdigest()
        return CodeChunk(cid, parsed.path, parsed.language, content, start, end, symbol)
