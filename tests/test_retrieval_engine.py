from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.storage.lancedb_store import LanceDBStore
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.chunking.models import CodeChunk


def test_search():
    store = LanceDBStore("/tmp/ai-core-test-lancedb")
    chunk = CodeChunk("1", "a.py", "python", "def hello(): pass", 1, 1, "hello")
    emb = Embedder()
    store.upsert_chunks([chunk], emb.embed_many([chunk.content]))
    results = HybridSearch(store, emb).search("hello", 1)
    assert results
    assert results[0]["symbol"] == "hello"
