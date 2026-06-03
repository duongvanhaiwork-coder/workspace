import re
from dataclasses import dataclass
from intelligence_engine.parser.base import ParsedFile

ROUTE_RE = re.compile(r"\b(?:router|app)\.(get|post|put|patch|delete)\(['\"]([^'\"]+)['\"]")

@dataclass
class RouteSymbol:
    method: str
    path: str
    file_path: str
    line: int

class RouteExtractor:
    def extract(self, parsed: ParsedFile) -> list[RouteSymbol]:
        routes = []
        for i, line in enumerate(parsed.source.splitlines(), start=1):
            if m := ROUTE_RE.search(line):
                routes.append(RouteSymbol(m.group(1).upper(), m.group(2), parsed.path, i))
        return routes
