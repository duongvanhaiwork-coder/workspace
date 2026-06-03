from fastapi import FastAPI
from intelligence_engine.api.routes import health, index, search, context, graph

app = FastAPI(title="AI Core", version="0.1.0")
app.include_router(health.router)
app.include_router(index.router, prefix="/index", tags=["index"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(context.router, prefix="/context", tags=["context"])
app.include_router(graph.router, prefix="/graph", tags=["graph"])
