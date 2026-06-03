# Architecture

Cursor/Kiro calls MCP stdio tools exposed by `mcp_server`. Tools delegate to the codebase intelligence engine.

## Layers

```text
┌─────────────────────────────────────────────────────────┐
│  IDE (Cursor / Kiro)                                    │
│  ─ stdio JSON-RPC ──────────────────────────────────    │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│  MCP Server  (mcp_server/)                              │
│  ├── server.py       FastMCP entrypoint                 │
│  ├── registry.py     tool name → handler mapping        │
│  └── tools/          one file per tool                  │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│  Intelligence Engine  (intelligence_engine/)            │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Retrieval Layer                                  │  │
│  │  ├── retrieval_engine.py  unified facade          │  │
│  │  ├── hybrid_search.py     vector + keyword        │  │
│  │  └── reranker.py          score boosting          │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Context Layer                                    │  │
│  │  ├── orchestrator.py  intent → plan → assemble    │  │
│  │  ├── intent.py        query classification        │  │
│  │  ├── planner.py       retrieval need mapping      │  │
│  │  ├── context_builder.py  filter/rank/trim         │  │
│  │  └── token_budget.py  token cost estimation       │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Storage Layer                                    │  │
│  │  ├── lancedb_store.py   vector store (per-project)│  │
│  │  ├── graph_store.py     NetworkX graph (per-proj) │  │
│  │  └── file_state_store.py  incremental diff state  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Indexing Pipeline                                │  │
│  │  ├── project_loader/  load projects.json          │  │
│  │  ├── scanner/         file discovery + watcher    │  │
│  │  ├── parser/          tree-sitter per language    │  │
│  │  ├── symbols/         symbol + import extraction  │  │
│  │  ├── chunking/        code chunk splitting        │  │
│  │  ├── embedding/       vector embedding            │  │
│  │  └── graph/           dependency graph builder    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### Indexing (offline)

```
projects.json → ProjectLoader → Scanner → Parser → SymbolExtractor
    → Chunker → Embedder → LanceDBStore (vectors, per-project)
    → GraphBuilder → GraphStore (graph, per-project)
    → FileStateStore (diff tracking, per-project)
```

### Query (runtime, per MCP tool call)

```
IDE → MCP Server → tool handler
    → RetrievalEngine.search() (vector + keyword via HybridSearch)
    → RetrievalEngine.load_graph() (NetworkX per-project)
    → ContextBuilder / Orchestrator (filter, rank, trim to budget)
    → JSON response → IDE
```

## Key Design Decisions

- **Per-project scoping:** vector store, graph, and file state are all isolated per project name.
- **Hash-based embedding fallback:** deterministic, no external API needed. Swap provider for production quality.
- **JSON graph persistence:** safe, inspectable, no pickle deserialization risk.
- **Incremental indexing:** FileStateStore tracks SHA-256 per file; only changed files get re-chunked/embedded.
- **Intent-aware retrieval:** Orchestrator classifies query intent and fetches only what that intent needs.
