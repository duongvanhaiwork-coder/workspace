from fastapi import APIRouter
from pydantic import BaseModel
from intelligence_engine.embedding.embedder import Embedder
from intelligence_engine.storage import get_vector_store
from intelligence_engine.retrieval.hybrid_search import HybridSearch
from intelligence_engine.retrieval.reranker import SimpleReranker

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    project: str = "__default__"
    top_k: int = 10


@router.post("")
def search(req: SearchRequest):
    store = get_vector_store()
    rows = HybridSearch(store, Embedder()).search(req.query, req.top_k * 2, project=req.project)
    return {"items": SimpleReranker().rerank(req.query, rows)[:req.top_k]}
