# Cấu trúc repo

Repo **AI Core** — Python MCP Server + Codebase Intelligence Engine, kèm skills + rules cho Cursor / Kiro.

## Tham chiếu

| Nội dung         | File                                             |
| ---------------- | ------------------------------------------------ |
| Tổng quan & lệnh | [README.md](README.md)                           |
| Agent policy     | [AGENTS.md](AGENTS.md)                           |
| Kiến trúc engine | [docs/architecture.md](docs/architecture.md)     |
| Indexing flow    | [docs/indexing-flow.md](docs/indexing-flow.md)   |
| Retrieval flow   | [docs/retrieval-flow.md](docs/retrieval-flow.md) |
| MCP tools spec   | [docs/mcp-tools.md](docs/mcp-tools.md)           |
| Project config   | [docs/project-config.md](docs/project-config.md) |
| Setup guide      | [docs/setup.md](docs/setup.md)                   |
| Rules layout     | [rules/CONVENTIONS.md](rules/CONVENTIONS.md)     |
| Skills layout    | [skills/STRUCTURE.md](skills/STRUCTURE.md)       |

## Architecture Overview

```text
Cursor / Kiro
     │
     │ MCP stdio
     ▼
Python MCP Server (mcp_server/)
     │
     ├── MCP Tools (search_code, get_context, analyze_impact, find_references, explain_symbol, reindex_project)
     │
     ▼
Codebase Intelligence Engine (intelligence_engine/)
     │
     ├── Intent Analyzer       (context/intent.py)
     ├── Retrieval Planner     (context/planner.py)
     ├── Orchestrator          (context/orchestrator.py)
     ├── Context Builder       (context/context_builder.py)
     │
     ├── Tree-sitter           (parser/)
     ├── Symbol Extractor      (symbols/)
     ├── Chunker               (chunking/)
     ├── Embedder              (embedding/)
     ├── Hybrid Search         (retrieval/hybrid_search.py)
     ├── Reranker              (retrieval/reranker.py)
     ├── Retrieval Engine      (retrieval/retrieval_engine.py)
     │
     ├── LanceDB Store         (storage/lancedb_store.py)        → data/lancedb/
     ├── Symbol Index Store    (storage/symbol_index_store.py)   → data/symbol_index/
     ├── Relationship Index    (storage/relationship_index_store.py) → data/relationship_index/
     ├── Graph Store           (storage/graph_store.py)          → data/graph/
     ├── File State Store      (storage/file_state_store.py)     → data/file_state/
     └── Retrieval Cache       (storage/retrieval_cache_store.py) → data/retrieval_cache/
```

## Core Responsibilities

| Layer                   | Responsible for                                                                  |
| ----------------------- | -------------------------------------------------------------------------------- |
| **Cursor / Kiro**       | reasoning, code generation, debugging, refactoring, test generation              |
| **MCP Server**          | exposing tools, communication bridge (stdio JSON-RPC)                            |
| **Intelligence Engine** | Find the smallest possible context that still allows the LLM to answer correctly |

## Database / Storage Design

| Store                  | File                                  | Purpose                                                                           |
| ---------------------- | ------------------------------------- | --------------------------------------------------------------------------------- |
| **file_state**         | `storage/file_state_store.py`         | Track indexing state per file (hash, mtime, status, last_indexed_at)              |
| **symbol_index**       | `storage/symbol_index_store.py`       | Symbol metadata for fast lookup (name, qualified_name, kind, signature)           |
| **code_chunks**        | `storage/lancedb_store.py`            | Semantic retrieval via vector search (content + embedding)                        |
| **graph_edges**        | `storage/graph_store.py`              | Dependency graph relationships via NetworkX (defines, imports, calls, reads)      |
| **relationship_index** | `storage/relationship_index_store.py` | Pre-computed per-symbol relationships (calls, called_by, reads, writes, uses_dto) |
| **retrieval_cache**    | `storage/retrieval_cache_store.py`    | TTL-based cache for repeated retrieval queries                                    |

## MCP Tools

| Tool              | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `search_code`     | Semantic + keyword search in indexed code     |
| `get_context`     | Token-budgeted context retrieval per intent   |
| `find_references` | Find all references to a symbol               |
| `analyze_impact`  | Blast radius analysis for a symbol/file       |
| `explain_symbol`  | Summarize a symbol's presence in the codebase |
| `reindex_project` | Clear caches and trigger re-index             |

## Output Schema — 6 Context Layers

`get_context` output theo architecture spec:

```json
{
  "meta": {
    "intent": "refactor",
    "confidence": 0.86,
    "token_budget": { "max": 12000, "used": 6800 }
  },
  "summary": "Layer 2 — natural language summary",
  "results": {
    "intent_context": { ... },       // Layer 1 — intent + query + target
    "symbols": [{ ... }],            // Layer 3 — relevant symbols + reasons
    "chunks": [{ ... }],             // Layer 4 — actual code (most tokens)
    "dependency_paths": [{ ... }],   // Layer 5 — call chain / deps
    "impact": { ... },               // Layer 6 — affected files + risk + actions
    "prompt_guidance": "..."         // LLM-specific instructions
  },
  "missing_context": ["..."]
}
```

| Layer | Field                 | Content                                         |
| ----- | --------------------- | ----------------------------------------------- |
| 1     | `intent_context`      | intent + query + target symbol                  |
| 2     | `summary` (top-level) | Natural language summary of findings            |
| 3     | `symbols`             | Relevant symbols with qualified_name + reason   |
| 4     | `chunks`              | Actual code chunks (function/method bodies)     |
| 5     | `dependency_paths`    | from → to + relation + reason                   |
| 6     | `impact`              | Affected files + risk level + suggested actions |

## Indexing Pipeline

```text
Scanner (detect files, hash, mtime)
  → Tree-sitter Parser (AST)
  → Symbol Extractor → symbol_index (name, qualified_name, kind, signature)
  → Import Extractor → graph_edges (imports relation)
  → Route Extractor → graph_edges (route relation)
  → Chunker → code_chunks (symbol, kind, content)
  → Embedder → code_chunks (vector embedding)
  → Graph Builder → graph_edges (defines, imports, route)
  → Relationship Index Builder → relationship_index (calls, called_by, reads, writes)
  → File State → file_state (status=indexed, last_indexed_at=now)
```

## Cây thư mục

```text
workspace/
├── AGENTS.md               # Agent policy cho Cursor / Kiro
├── README.md               # Tổng quan, cài đặt, hướng dẫn sử dụng
├── STRUCTOR.md             # File này — cấu trúc repo
├── pyproject.toml          # Python project config (ai-core)
├── projects.json           # Danh sách project cần index
├── docker-compose.yml      # Docker config (optional API)
├── Dockerfile              # Docker image
├── .env.example            # Mẫu biến môi trường
│
├── mcp_server/             # MCP stdio server (FastMCP)
│   ├── server.py           # Entrypoint — tool definitions
│   ├── registry.py         # Tool → handler mapping
│   └── tools/              # Từng tool implementation
│       ├── search_code.py
│       ├── get_context.py
│       ├── analyze_impact.py
│       ├── find_references.py
│       ├── explain_symbol.py
│       ├── reindex_project.py
│       └── output_schema.py  # Strict output wrapper (6 layers)
│
├── intelligence_engine/    # Codebase Intelligence Engine
│   ├── config/             # Settings (pydantic-settings, đọc .env)
│   │   └── settings.py
│   ├── project_loader/     # Load project config từ projects.json
│   │   ├── loader.py
│   │   └── project_config.py
│   ├── scanner/            # File scan + watcher + file state model
│   │   ├── scanner.py      # Scan files, populate last_modified_at
│   │   ├── file_state.py   # FileState dataclass + mark_indexed()
│   │   └── watcher.py      # Watchdog incremental watcher
│   ├── parser/             # Tree-sitter language parsers
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── languages/      # python, typescript, javascript, csharp
│   ├── symbols/            # Symbol & import extraction
│   │   ├── extractor.py    # Tree-sitter + regex fallback
│   │   ├── models.py       # Symbol + ImportRef dataclasses
│   │   ├── imports.py      # Import pattern matching
│   │   ├── references.py   # Text-based reference scanning
│   │   └── routes.py       # HTTP route extraction
│   ├── chunking/           # Code chunking strategies
│   │   ├── chunker.py      # Symbol-based + window fallback
│   │   └── models.py       # CodeChunk dataclass (symbol, kind, metadata)
│   ├── embedding/          # Vector embedding
│   │   ├── embedder.py     # Facade
│   │   └── providers.py    # HashEmbeddingProvider (local, deterministic)
│   ├── storage/            # All persistence layers
│   │   ├── __init__.py     # Singleton factories (get_*_store)
│   │   ├── lancedb_store.py          # code_chunks (vector search)
│   │   ├── graph_store.py            # graph_edges (NetworkX JSON)
│   │   ├── file_state_store.py       # file_state (incremental)
│   │   ├── symbol_index_store.py     # symbol_index (metadata lookup)
│   │   ├── relationship_index_store.py # relationship_index (fast lookup)
│   │   └── retrieval_cache_store.py  # retrieval_cache (TTL cache)
│   ├── graph/              # NetworkX code graph + analysis
│   │   ├── graph_builder.py     # Build graph from symbols + imports + routes
│   │   ├── impact_analyzer.py   # Reverse traversal for blast radius
│   │   ├── pruning.py           # Noise filtering + priority ranking
│   │   ├── reference_finder.py  # Find nodes by symbol name
│   │   └── relation_types.py    # All relation constants
│   ├── retrieval/          # Hybrid search + reranker
│   │   ├── hybrid_search.py     # Vector + keyword blend
│   │   ├── reranker.py          # Simple + CrossEncoder (fallback-safe)
│   │   └── retrieval_engine.py  # Unified facade for search + graph
│   ├── context/            # Token-budgeted context builder + orchestrator
│   │   ├── intent.py           # Intent Analyzer (keyword → QueryIntent)
│   │   ├── planner.py          # Retrieval Planner (intent → needs)
│   │   ├── orchestrator.py     # Full pipeline: plan → search → assemble layers
│   │   ├── context_builder.py  # Filter, rank, trim to token budget
│   │   ├── token_budget.py     # Token estimation (~4 chars/token)
│   │   └── prompt_templates.py # Intent-specific LLM guidance
│   └── api/                # FastAPI HTTP interface (optional, debug)
│       ├── main.py
│       └── routes/
│           ├── health.py
│           ├── index.py    # POST /index/{project} — trigger indexing
│           ├── search.py   # POST /search — vector search
│           ├── context.py  # POST /context — context builder
│           └── graph.py    # GET /graph/references, /graph/impact
│
├── scripts/                # CLI utilities
│   ├── index_project.py    # Index project (incremental or --full)
│   ├── watch_project.py    # Watcher incremental (vector only)
│   ├── inspect_graph.py    # Debug graph data
│   ├── sync-ide.sh         # Sync rules + skills vào IDE
│   ├── sync-ide-rules.sh   # Sync rules only
│   ├── sync-ide-skills.sh  # Sync skills only
│   ├── link-global-ide.sh  # Symlink global IDE config
│   ├── verify.sh           # Run all verification checks
│   └── verify-*.sh         # Individual verification scripts
│
├── tests/                  # pytest test suite (57 tests)
│   ├── test_chunker.py
│   ├── test_context_builder.py
│   ├── test_file_state_diff.py
│   ├── test_graph_builder.py
│   ├── test_graph_pruning.py
│   ├── test_impact_analyzer.py
│   ├── test_lancedb_store.py
│   ├── test_project_loader.py
│   ├── test_prompt_templates.py
│   ├── test_reranker.py
│   ├── test_retrieval_engine.py
│   ├── test_scanner.py
│   └── test_symbol_extractor.py
│
├── data/                   # Runtime indexed data (gitignored)
│   ├── lancedb/            # code_chunks — vector embeddings per project
│   ├── graph/              # graph_edges — NetworkX JSON per project
│   ├── file_state/         # file_state — tracking per project
│   ├── symbol_index/       # symbol_index — metadata per project
│   ├── relationship_index/ # relationship_index — fast lookup per project
│   └── retrieval_cache/    # retrieval_cache — TTL cache
│
├── docs/                   # Documentation
│   ├── architecture.md
│   ├── indexing-flow.md
│   ├── retrieval-flow.md
│   ├── mcp-tools.md
│   ├── project-config.md
│   └── setup.md
│
├── skills/                 # Canonical agent skills
│   ├── STRUCTURE.md
│   ├── CONVENTIONS.md
│   ├── SKILLS-REGISTRY.md
│   ├── COMPOSITION.md
│   ├── references/
│   └── <skill-name>/
│
├── rules/                  # Agent rules
│   ├── cursor/             # Cursor .mdc — canonical, sửa tại đây
│   ├── kiro/               # Kiro steering — tự sinh, không sửa tay
│   ├── CONVENTIONS.md
│   ├── QUICKSTART.md
│   └── RECOVERY.md
│
└── rules.zip / skills.zip  # Optional bundles cho distribution
```

## Token Optimization Strategy (section 9)

- **Chunking:** Send functions/methods/classes, not entire files
- **Reranker:** 20 candidates → top_k best chunks (default 10)
- **Graph Pruning:** Remove utility noise, unrelated imports, deep chains
- **Ranking:** definition > direct references > caller/callee > DTO/entity > tests > utilities
- **Summaries:** Prefer summary string over full code when possible
- **Token Budget:** Hard limit per request (default 12000 tokens)

## Opinionated Retrieval Rules (section 10)

Priority symbols: entity, dto, service, repository.
Lower priority: helpers, utils, logger, constants.

## Relation Types (section 4.4)

imports, exports, defines, calls, reads, writes, extends, implements, uses_model, uses_dto, route_to_handler

## Intent Classification

| Intent     | Trigger keywords                            | Output layers    |
| ---------- | ------------------------------------------- | ---------------- |
| `search`   | where, find, references, ở đâu, dùng ở      | 1, 2, 3          |
| `explain`  | how does, explain, flow, giải thích         | 1, 2, 4, 5       |
| `refactor` | rename, refactor, extract, đổi tên          | 1, 2, 3, 4, 5, 6 |
| `impact`   | impact, blast radius, ảnh hưởng, affected   | 1, 2, 5, 6       |
| `debug`    | why, debug, null, error, bug, tại sao       | 1, 2, 4, 5       |
| `test`     | test, spec, generate test, viết test        | 1, 2, 4          |
| `generate` | add field, create, generate, implement, tạo | 1, 2, 3, 4       |

## IDE sync

Sau `./scripts/sync-ide.sh`:

| Source (repo)   | Target (IDE)                            |
| --------------- | --------------------------------------- |
| `rules/cursor/` | `~/.cursor/rules/`                      |
| `rules/kiro/`   | `~/.kiro/steering/`                     |
| `skills/`       | `~/.cursor/skills/` + `~/.kiro/skills/` |

## Key conventions

- **Rules:** Sửa tại `rules/cursor/*.mdc` → `rules/kiro/` tự sinh. Không sửa kiro trực tiếp.
- **Skills:** Sửa tại `skills/<name>/`. Xem `skills/STRUCTURE.md` cho layout.
- **Docs:** Mỗi doc một concern. Thêm link vào bảng tham chiếu ở trên khi tạo doc mới.
- **Data:** Folder `data/` gitignored — mỗi máy tự index. All stores scoped per project.
- **Testing:** `python -m pytest tests/` — 57 tests, all passing.
