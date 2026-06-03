from dataclasses import dataclass, field


@dataclass
class CodeChunk:
    chunk_id: str
    file_path: str
    language: str
    content: str
    line_start: int
    line_end: int
    symbol: str | None = None
    kind: str = ""  # method | class | function | property
    summary: str = ""
    metadata: dict = field(default_factory=dict)
    # metadata keys: imports, reads, calls, tags
