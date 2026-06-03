from pathlib import Path
from .base import BaseParser
from .languages.python_parser import PythonParser
from .languages.javascript_parser import JavaScriptParser
from .languages.typescript_parser import TypeScriptParser
from .languages.csharp_parser import CSharpParser

class ParserFactory:
    EXTENSION_MAP = {
        ".py": PythonParser,
        ".js": JavaScriptParser,
        ".jsx": JavaScriptParser,
        ".ts": TypeScriptParser,
        ".tsx": TypeScriptParser,
        ".cs": CSharpParser,
    }

    def get_parser(self, path: str | Path) -> BaseParser:
        cls = self.EXTENSION_MAP.get(Path(path).suffix, BaseParser)
        return cls()
