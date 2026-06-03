from dataclasses import dataclass

@dataclass
class Symbol:
    name: str
    kind: str
    file_path: str
    start_line: int
    end_line: int
    signature: str = ""

@dataclass
class ImportRef:
    module: str
    file_path: str
    line: int
