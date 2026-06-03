from dataclasses import dataclass

@dataclass
class CodeChunk:
    id: str
    file_path: str
    language: str
    content: str
    start_line: int
    end_line: int
    symbol: str | None = None
