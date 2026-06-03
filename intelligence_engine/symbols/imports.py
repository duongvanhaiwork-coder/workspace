import re
from intelligence_engine.parser.base import ParsedFile
from .models import ImportRef

PATTERNS = [
    re.compile(r"^\s*import\s+(?:.*?\s+from\s+)?['\"](?P<module>[^'\"]+)['\"]"),
    re.compile(r"^\s*from\s+(?P<module>[\w\.]+)\s+import\s+"),
    re.compile(r"^\s*using\s+(?P<module>[\w\.]+)\s*;"),
    re.compile(r"require\(['\"](?P<module>[^'\"]+)['\"]\)"),
]

class ImportExtractor:
    def extract(self, parsed: ParsedFile) -> list[ImportRef]:
        refs: list[ImportRef] = []
        for i, line in enumerate(parsed.source.splitlines(), start=1):
            for pattern in PATTERNS:
                if m := pattern.search(line):
                    refs.append(ImportRef(m.group('module'), parsed.path, i))
        return refs
