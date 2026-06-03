from pathlib import Path
from intelligence_engine.parser.base import BaseParser, ParsedFile

try:
    import tree_sitter_language_pack as tslp
    _PARSER = tslp.get_parser("c_sharp")
    _TS_AVAILABLE = True
except Exception:
    _TS_AVAILABLE = False


class CSharpParser(BaseParser):
    language = "csharp"

    def parse(self, path: Path, source: str | None = None, rel_path: str | None = None) -> ParsedFile:
        text = source if source is not None else path.read_text(encoding="utf-8", errors="ignore")
        stored_path = rel_path if rel_path is not None else str(path)
        tree = None
        if _TS_AVAILABLE:
            tree = _PARSER.parse(text)
        return ParsedFile(path=stored_path, language=self.language, source=text, tree=tree)
