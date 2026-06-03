from intelligence_engine.context.context_builder import ContextBuilder


def test_context_builder():
    rows = [{"file_path": "a.py", "start_line": 1, "end_line": 1, "content": "x=1", "score": 0.5, "symbol": "x", "kind": "variable"}]
    chunks = ContextBuilder().build_chunks(rows, "x")
    assert len(chunks) == 1
    assert chunks[0]["file"] == "a.py"
    assert chunks[0]["content"] == "x=1"


def test_context_builder_respects_max_chunks():
    rows = [
        {"file_path": f"file{i}.py", "start_line": 1, "end_line": 1, "content": f"line{i}", "score": 0.5, "symbol": f"s{i}", "kind": "var"}
        for i in range(30)
    ]
    chunks = ContextBuilder().build_chunks(rows, "test")
    # Hard limit: max 15 chunks, max 5 files
    assert len(chunks) <= 15
    files = set(c["file"] for c in chunks)
    assert len(files) <= 5


def test_context_builder_entrypoints():
    rows = [
        {"file_path": "a.py", "start_line": 1, "end_line": 10, "content": "class A", "score": 0.8, "symbol": "A", "kind": "class"},
        {"file_path": "b.py", "start_line": 1, "end_line": 5, "content": "class B", "score": 0.1, "symbol": "B", "kind": "class"},
    ]
    entries = ContextBuilder().build_entrypoints(rows)
    # Only high-score entries (>= 0.25)
    assert len(entries) == 1
    assert entries[0]["file"] == "a.py"
