import tempfile
from pathlib import Path
from intelligence_engine.storage.file_state_store import FileStateStore
from intelligence_engine.scanner.file_state import FileState


def _make_store() -> FileStateStore:
    """Create a FileStateStore with a temp directory."""
    tmpdir = tempfile.mkdtemp()
    return FileStateStore(tmpdir)


def test_diff_new_files():
    store = _make_store()

    # No prior state — everything is new
    current = [
        FileState(file_path="a.py", content_hash="aaa", size_bytes=100),
        FileState(file_path="b.py", content_hash="bbb", size_bytes=200),
    ]
    changed, deleted = store.diff(current)
    assert len(changed) == 2
    assert deleted == []


def test_diff_unchanged():
    store = _make_store()

    states = [
        FileState(file_path="a.py", content_hash="aaa", size_bytes=100),
        FileState(file_path="b.py", content_hash="bbb", size_bytes=200),
    ]
    store.save(states)

    # Same scan — no changes
    changed, deleted = store.diff(states)
    assert changed == []
    assert deleted == []


def test_diff_modified():
    store = _make_store()

    store.save([
        FileState(file_path="a.py", content_hash="aaa", size_bytes=100),
        FileState(file_path="b.py", content_hash="bbb", size_bytes=200),
    ])

    # b.py changed hash
    current = [
        FileState(file_path="a.py", content_hash="aaa", size_bytes=100),
        FileState(file_path="b.py", content_hash="ccc", size_bytes=210),
    ]
    changed, deleted = store.diff(current)
    assert len(changed) == 1
    assert changed[0].file_path == "b.py"
    assert deleted == []


def test_diff_deleted():
    store = _make_store()

    store.save([
        FileState(file_path="a.py", content_hash="aaa", size_bytes=100),
        FileState(file_path="b.py", content_hash="bbb", size_bytes=200),
    ])

    # b.py removed from scan
    current = [FileState(file_path="a.py", content_hash="aaa", size_bytes=100)]
    changed, deleted = store.diff(current)
    assert changed == []
    assert deleted == ["b.py"]


def test_diff_mixed():
    store = _make_store()

    store.save([
        FileState(file_path="a.py", content_hash="aaa", size_bytes=100),
        FileState(file_path="b.py", content_hash="bbb", size_bytes=200),
    ])

    # a.py changed, b.py deleted, c.py new
    current = [
        FileState(file_path="a.py", content_hash="xxx", size_bytes=110),
        FileState(file_path="c.py", content_hash="ccc", size_bytes=50),
    ]
    changed, deleted = store.diff(current)
    changed_paths = [s.file_path for s in changed]
    assert "a.py" in changed_paths
    assert "c.py" in changed_paths
    assert deleted == ["b.py"]
