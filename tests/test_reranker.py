"""Tests for reranker module — SimpleReranker and CrossEncoderReranker fallback."""

from intelligence_engine.retrieval.reranker import (
    SimpleReranker,
    CrossEncoderReranker,
    get_reranker,
)


# --- SimpleReranker ---


def test_simple_reranker_keyword_boost():
    """Rows containing query terms should rank higher than same-score rows without."""
    reranker = SimpleReranker()
    rows = [
        {"content": "def calculate_total(): pass", "score": 0.5},
        {"content": "if TotalAmount < 0: raise validated", "score": 0.5},
        {"content": "class Logger: pass", "score": 0.5},
    ]
    result = reranker.rerank("TotalAmount validated", rows)
    # Row with 2 keyword matches should rank highest among equal-score rows
    assert result[0]["content"] == "if TotalAmount < 0: raise validated"


def test_simple_reranker_top_k():
    """top_k should limit results."""
    reranker = SimpleReranker()
    rows = [{"content": f"item {i}", "score": 0.5 - i * 0.01} for i in range(20)]
    result = reranker.rerank("item", rows, top_k=5)
    assert len(result) == 5


def test_simple_reranker_empty():
    """Empty input returns empty output."""
    reranker = SimpleReranker()
    assert reranker.rerank("query", []) == []


def test_simple_reranker_preserves_rows():
    """All original row fields are preserved."""
    reranker = SimpleReranker()
    rows = [{"content": "hello world", "score": 0.8, "file_path": "a.py", "symbol": "hello"}]
    result = reranker.rerank("hello", rows)
    assert result[0]["file_path"] == "a.py"
    assert result[0]["symbol"] == "hello"


# --- CrossEncoderReranker fallback ---


def test_cross_encoder_fallback_when_no_sentence_transformers():
    """Without sentence-transformers installed, falls back to SimpleReranker."""
    reranker = CrossEncoderReranker(model_name="nonexistent/model")
    rows = [
        {"content": "def validate_amount(): pass", "score": 0.4},
        {"content": "class AmountService: pass", "score": 0.6},
    ]
    # Should not crash — falls back to SimpleReranker behavior
    result = reranker.rerank("validate amount", rows, top_k=2)
    assert len(result) <= 2
    assert all("content" in r for r in result)


def test_cross_encoder_empty_input():
    """Empty rows returns empty results."""
    reranker = CrossEncoderReranker()
    assert reranker.rerank("query", [], top_k=5) == []


# --- Factory ---


def test_get_reranker_simple():
    """Default factory returns SimpleReranker."""
    reranker = get_reranker(use_cross_encoder=False)
    assert isinstance(reranker, SimpleReranker)


def test_get_reranker_cross_encoder():
    """Factory with cross_encoder=True returns CrossEncoderReranker."""
    reranker = get_reranker(use_cross_encoder=True)
    assert isinstance(reranker, CrossEncoderReranker)


def test_get_reranker_custom_model():
    """Factory accepts custom model name."""
    reranker = get_reranker(use_cross_encoder=True, model_name="custom/model")
    assert isinstance(reranker, CrossEncoderReranker)
    assert reranker._model_name == "custom/model"
