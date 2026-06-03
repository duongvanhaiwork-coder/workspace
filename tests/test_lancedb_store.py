from intelligence_engine.storage.lancedb_store import LanceDBStore
from intelligence_engine.chunking.models import CodeChunk
from intelligence_engine.embedding.embedder import Embedder


def test_upsert_and_search():
    store = LanceDBStore("/tmp/ai-core-test-store")
    emb = Embedder()
    chunk = CodeChunk("1", "a.py", "python", "def hello(): pass", 1, 1, "hello")
    store.upsert_chunks([chunk], emb.embed_many([chunk.content]), project="test")
    results = store.search(emb.embed_text("hello"), top_k=5, project="test")
    assert len(results) == 1
    assert results[0]["symbol"] == "hello"


def test_upsert_replaces_existing():
    store = LanceDBStore("/tmp/ai-core-test-store2")
    emb = Embedder()
    chunk_v1 = CodeChunk("id1", "a.py", "python", "def hello(): v1", 1, 1, "hello")
    chunk_v2 = CodeChunk("id1", "a.py", "python", "def hello(): v2", 1, 1, "hello")

    store.upsert_chunks([chunk_v1], emb.embed_many([chunk_v1.content]), project="test")
    store.upsert_chunks([chunk_v2], emb.embed_many([chunk_v2.content]), project="test")

    results = store.search(emb.embed_text("hello"), top_k=10, project="test")
    assert len(results) == 1
    assert "v2" in results[0]["content"]


def test_delete_by_file():
    store = LanceDBStore("/tmp/ai-core-test-store3")
    emb = Embedder()
    c1 = CodeChunk("1", "a.py", "python", "def foo(): pass", 1, 1, "foo")
    c2 = CodeChunk("2", "a.py", "python", "def bar(): pass", 2, 2, "bar")
    c3 = CodeChunk("3", "b.py", "python", "def baz(): pass", 1, 1, "baz")

    store.upsert_chunks([c1, c2, c3], emb.embed_many([c.content for c in [c1, c2, c3]]), project="test")

    removed = store.delete_by_file("a.py", project="test")
    assert removed == 2

    results = store.search(emb.embed_text("anything"), top_k=10, project="test")
    assert len(results) == 1
    assert results[0]["file_path"] == "b.py"


def test_project_isolation():
    store = LanceDBStore("/tmp/ai-core-test-store4")
    emb = Embedder()
    c1 = CodeChunk("1", "a.py", "python", "project one", 1, 1, None)
    c2 = CodeChunk("2", "b.py", "python", "project two", 1, 1, None)

    store.upsert_chunks([c1], emb.embed_many([c1.content]), project="proj1")
    store.upsert_chunks([c2], emb.embed_many([c2.content]), project="proj2")

    r1 = store.search(emb.embed_text("project"), top_k=10, project="proj1")
    r2 = store.search(emb.embed_text("project"), top_k=10, project="proj2")

    assert len(r1) == 1
    assert r1[0]["file_path"] == "a.py"
    assert len(r2) == 1
    assert r2[0]["file_path"] == "b.py"
