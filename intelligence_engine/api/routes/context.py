from fastapi import APIRouter
from pydantic import BaseModel
from intelligence_engine.context.context_builder import ContextBuilder
from intelligence_engine.context.token_budget import TokenBudget
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.storage import get_vector_store
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.retrieval.reranker import SimpleReranker

router = APIRouter()


class ContextRequest(BaseModel):
    query: str
    project: str = "__default__"
    top_k: int = 10
    max_tokens: int = 4000


@router.post("")
def get_context(req: ContextRequest):
    store = get_vector_store()
    rows = HybridSearch(store, Embedder()).search(req.query, req.top_k * 2, project=req.project)
    rows = SimpleReranker().rerank(req.query, rows)[:req.top_k]
    budget = TokenBudget(max_tokens=req.max_tokens)
    return {"context": ContextBuilder(budget=budget).build(rows), "items": rows}
