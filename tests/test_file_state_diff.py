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
        FileState("a.py", "aaa", 100),
        FileState("b.py", "bbb", 200),
    ]
    changed, deleted = store.diff(current)
    assert len(changed) == 2
    assert deleted == []


def test_diff_unchanged():
    store = _make_store()

    states = [
        FileState("a.py", "aaa", 100),
        FileState("b.py", "bbb", 200),
    ]
    store.save(states)

    # Same scan — no changes
    changed, deleted = store.diff(states)
    assert changed == []
    assert deleted == []


def test_diff_modified():
    store = _make_store()

    store.save([
        FileState("a.py", "aaa", 100),
        FileState("b.py", "bbb", 200),
    ])

    # b.py changed hash
    current = [
        FileState("a.py", "aaa", 100),
        FileState("b.py", "ccc", 210),
    ]
    changed, deleted = store.diff(current)
    assert len(changed) == 1
    assert changed[0].path == "b.py"
    assert deleted == []


def test_diff_deleted():
    store = _make_store()

    store.save([
        FileState("a.py", "aaa", 100),
        FileState("b.py", "bbb", 200),
    ])

    # b.py removed from scan
    current = [FileState("a.py", "aaa", 100)]
    changed, deleted = store.diff(current)
    assert changed == []
    assert deleted == ["b.py"]


def test_diff_mixed():
    store = _make_store()

    store.save([
        FileState("a.py", "aaa", 100),
        FileState("b.py", "bbb", 200),
    ])

    # a.py changed, b.py deleted, c.py new
    current = [
        FileState("a.py", "xxx", 110),
        FileState("c.py", "ccc", 50),
    ]
    changed, deleted = store.diff(current)
    changed_paths = [s.path for s in changed]
    assert "a.py" in changed_paths
    assert "c.py" in changed_paths
    assert deleted == ["b.py"]
