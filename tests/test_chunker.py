from intelligence_engine.parser.base import ParsedFile
from intelligence_engine.chunking.chunker import Chunker

def test_chunker_window():
    chunks = Chunker().chunk(ParsedFile("a.py", "python", "print(1)"))
    assert len(chunks) == 1
