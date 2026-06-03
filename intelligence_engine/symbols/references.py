from dataclasses import dataclass

@dataclass
class Reference:
    symbol: str
    file_path: str
    line: int
    text: str

class ReferenceScanner:
    def find(self, symbol: str, file_path: str, source: str) -> list[Reference]:
        refs = []
        for i, line in enumerate(source.splitlines(), start=1):
            if symbol in line:
                refs.append(Reference(symbol, file_path, i, line.strip()))
        return refs
