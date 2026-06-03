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
     ├── MCP Tools
     └── MCP Resources
     │
     ▼
Codebase Intelligence Engine (intelligence_engine/)
     │
     ├── Intent Analyzer       (context/intent.py)
     ├── Retrieval Planner     (context/planner.py)
     ├── Context Builder       (context/context_builder.py)
     │
     ├── Tree-sitter           (parser/)
     ├── Symbol Extractor      (symbols/)
     ├── Chunker               (chunking/)
     ├── Embedder              (embedding/)
     ├── LanceDB               (storage/lancedb_store.py)
     ├── Symbol Index          (storage/symbol_index_store.py)
     ├── Relationship Index    (storage/relationship_index_store.py)
     ├── NetworkX Graph        (storage/graph_store.py)
     └── Retrieval Cache       (storage/retrieval_cache_store.py)
```

## Core Responsibilities

| Layer                   | Responsible for                                                                  |
| ----------------------- | -------------------------------------------------------------------------------- |
| **Cursor / Kiro**       | reasoning, code generation, debugging, refactoring, test generation              |
| **MCP Server**          | exposing tools, exposing resources, communication bridge                         |
| **Intelligence Engine** | Find the smallest possible context that still allows the LLM to answer correctly |

## Database / Storage Design

| Store                  | File                                  | Purpose                                                                           |
| ---------------------- | ------------------------------------- | --------------------------------------------------------------------------------- |
| **file_state**         | `storage/file_state_store.py`         | Track indexing state per file (incremental indexing, change detection)            |
| **symbol_index**       | `storage/symbol_index_store.py`       | Symbol metadata for fast lookup (find_symbol, explain_symbol, jump to definition) |
| **code_chunks**        | `storage/lancedb_store.py`            | Semantic retrieval via vector search (search_code, get_context)                   |
| **graph_edges**        | `storage/graph_store.py`              | Dependency graph relationships via NetworkX (analyze_impact, find_references)     |
| **relationship_index** | `storage/relationship_index_store.py` | Fast relationship lookup without full graph traversal (refactor, impact)          |
| **retrieval_cache**    | `storage/retrieval_cache_store.py`    | Avoid repeated retrieval work (TTL-based cache)                                   |

## MCP Tools

| Tool              | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `search_code`     | Semantic + keyword search in indexed code     |
| `get_context`     | Token-budgeted context retrieval per intent   |
| `find_references` | Find all references to a symbol               |
| `analyze_impact`  | Blast radius analysis for a symbol/file       |
| `explain_symbol`  | Summarize a symbol's presence in the codebase |
| `reindex_project` | Trigger re-indexing for a project             |

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
│       └── reindex_project.py
│
├── intelligence_engine/    # Codebase Intelligence Engine
│   ├── config/             # Settings (pydantic-settings, đọc .env)
│   │   └── settings.py
│   ├── project_loader/     # Load project config từ projects.json
│   │   ├── loader.py
│   │   └── project_config.py
│   ├── scanner/            # File scan + watcher + file state model
│   │   ├── scanner.py
│   │   ├── file_state.py   # FileState dataclass + hash_file + detect_language
│   │   └── watcher.py
│   ├── parser/             # Tree-sitter language parsers
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── languages/      # Per-language parser implementations
│   ├── symbols/            # Symbol & import extraction
│   │   ├── extractor.py
│   │   ├── models.py       # Symbol + ImportRef dataclasses
│   │   ├── imports.py
│   │   ├── references.py
│   │   └── routes.py
│   ├── chunking/           # Code chunking strategies
│   │   ├── chunker.py
│   │   └── models.py       # CodeChunk dataclass (with metadata)
│   ├── embedding/          # Vector embedding (sentence-transformers)
│   │   ├── embedder.py
│   │   └── providers.py
│   ├── storage/            # All persistence layers
│   │   ├── lancedb_store.py          # code_chunks (vector search)
│   │   ├── graph_store.py            # graph_edges (NetworkX)
│   │   ├── file_state_store.py       # file_state (incremental)
│   │   ├── symbol_index_store.py     # symbol_index (metadata lookup)
│   │   ├── relationship_index_store.py # relationship_index (fast lookup)
│   │   └── retrieval_cache_store.py  # retrieval_cache (TTL cache)
│   ├── graph/              # NetworkX code graph + analysis
│   │   ├── graph_builder.py
│   │   ├── impact_analyzer.py
│   │   ├── pruning.py
│   │   ├── reference_finder.py
│   │   └── relation_types.py  # All relation constants
│   ├── retrieval/          # Hybrid search + reranker
│   │   ├── hybrid_search.py
│   │   ├── reranker.py
│   │   └── retrieval_engine.py
│   ├── context/            # Token-budgeted context builder + orchestrator
│   │   ├── intent.py           # Intent Analyzer (section 6)
│   │   ├── planner.py          # Retrieval Planner (section 7)
│   │   ├── context_builder.py  # Context Builder (section 8)
│   │   ├── orchestrator.py     # Full pipeline orchestrator
│   │   ├── token_budget.py     # Token budget management
│   │   └── prompt_templates.py # Prompt templates for LLM
│   └── api/                # FastAPI HTTP interface (optional, debug)
│       ├── main.py
│       └── routes/
│
├── scripts/                # CLI utilities
│   ├── index_project.py    # Index một project (full)
│   ├── watch_project.py    # Watcher incremental (vector only)
│   ├── inspect_graph.py    # Debug graph data
│   ├── sync-ide.sh         # Sync rules + skills vào IDE
│   ├── sync-ide-rules.sh   # Sync rules only
│   ├── sync-ide-skills.sh  # Sync skills only
│   ├── link-global-ide.sh  # Symlink global IDE config
│   ├── verify.sh           # Run all verification checks
│   └── verify-*.sh         # Individual verification scripts
│
├── tests/                  # pytest test suite
│
├── data/                   # Runtime indexed data (gitignored)
│   ├── lancedb/            # code_chunks — vector embeddings
│   ├── graph/              # graph_edges — dependency graphs (NetworkX)
│   ├── file_state/         # file_state — file state tracking
│   ├── symbol_index/       # symbol_index — symbol metadata
│   ├── relationship_index/ # relationship_index — fast relationship lookup
│   └── retrieval_cache/    # retrieval_cache — cached retrieval results
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
│   ├── STRUCTURE.md        # Skills folder layout
│   ├── CONVENTIONS.md      # Skill authoring conventions
│   ├── SKILLS-REGISTRY.md  # Registry of all skills
│   ├── COMPOSITION.md      # How skills compose together
│   ├── references/         # Shared references across skills
│   └── <skill-name>/      # Individual skill folders
│
├── rules/                  # Agent rules
│   ├── cursor/             # Cursor .mdc — canonical, sửa tại đây
│   ├── kiro/               # Kiro steering — tự sinh, không sửa tay
│   ├── CONVENTIONS.md      # Rule authoring conventions
│   ├── QUICKSTART.md       # Quick reference for rules
│   └── RECOVERY.md         # Recovery procedures
│
└── rules.zip / skills.zip  # Optional bundles cho distribution
```

## Indexing Pipeline (section 5)

```text
Repo Files → Scanner → Tree-sitter Parser → Symbol Extractor → Chunker → Embedder → LanceDB + Graph + Indexes
```

## Context Layers (section 8)

| Layer | Name               | Content                                         |
| ----- | ------------------ | ----------------------------------------------- |
| 1     | Intent Context     | intent + query + target                         |
| 2     | Summary Context    | Natural language summary of findings            |
| 3     | Symbol Context     | Relevant symbols with reasons                   |
| 4     | Code Context       | Actual code chunks (most expensive)             |
| 5     | Dependency Context | Call chain / dependency paths                   |
| 6     | Impact Context     | Affected files + risk level + suggested actions |

## Token Optimization Strategy (section 9)

- **Chunking:** Send functions/methods/classes, not entire files
- **Reranker:** 20 candidates → 5 best chunks
- **Graph Pruning:** Remove utility noise, unrelated imports, deep chains
- **Ranking:** definition > direct references > caller/callee > DTO/entity > tests > utilities
- **Summaries:** Prefer summary string over full code when possible

## Opinionated Retrieval Rules (section 10)

Priority symbols: entity, dto, service, repository.
Lower priority: helpers, utils, logger, constants.

## Relation Types (section 4.4)

imports, exports, defines, calls, reads, writes, extends, implements, uses_model, uses_dto, route_to_handler

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
- **Data:** Folder `data/` gitignored — mỗi máy tự index.
