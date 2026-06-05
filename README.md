# AI Core

Python MCP Server + Codebase Intelligence Engine cho Cursor / Kiro.

## Architecture

```text
Cursor / Kiro
   │
   │ MCP stdio
   ▼
Python MCP Server + Codebase Intelligence Engine
   ├── MCP Layer          → mcp_server/server.py (FastMCP stdio)
   ├── Project Loader     → intelligence_engine/project_loader/
   ├── Scanner / Watcher  → intelligence_engine/scanner/
   ├── Tree-sitter Parser → intelligence_engine/parser/
   ├── Symbol Extractor   → intelligence_engine/symbols/
   ├── Chunker            → intelligence_engine/chunking/
   ├── Embedder           → intelligence_engine/embedding/
   ├── LanceDB            → intelligence_engine/storage/ + data/lancedb/
   ├── NetworkX Graph     → intelligence_engine/graph/ + data/graph/
   ├── Retrieval Engine   → intelligence_engine/retrieval/
   ├── Context Builder    → intelligence_engine/context/
   └── MCP Tools          → mcp_server/tools/
       ├── search_code
       ├── get_context
       ├── analyze_impact
       ├── find_references
       ├── explain_symbol
       └── reindex_project
```

## Stack

| Layer         | Technology             | Chi tiết                                         |
| ------------- | ---------------------- | ------------------------------------------------ |
| **Parsing**   | Tree-sitter            | Parse function, class, method, route, model, DTO |
| **Embedding** | BAAI/bge-base-en-v1.5  | 768 dimensions, ML model                         |
| **Keyword**   | BM25                   | camelCase/snake_case tokenizer, term-frequency   |
| **Reranker**  | BAAI/bge-reranker-base | Cross-encoder, min-max normalized                |
| **Vector DB** | LanceDB                | JSON persistence, cosine similarity              |
| **Graph**     | NetworkX               | Relationship scoring, impact analysis            |
| **Chunking**  | Symbol-aware           | function/method/class/interface + metadata       |

## Retrieval Flow

```text
search_code (include_context=false — default)
  → vector search (bge-base-en-v1.5, top 50)
  → keyword search (BM25, top 50)
  → symbol index match
  → merge candidates
  → graph boost (callers, callees, DTO usage)
  → rerank (bge-reranker-base, top 30)
  → return top 5-10 + next_recommended_tool

search_code (include_context=true)
  → same as above
  → auto-call get_context internally
  → return search results + full context inline

get_context
  → intent classification (search/explain/refactor/impact/debug/test/generate)
  → retrieval plan (decides what data to fetch)
  → search layer (hybrid search + rerank)
  → graph layer (dependency paths, callers, impact)
  → context builder (filter, rank, trim to token budget)
  → return structured 6-layer context cho AI

find_references
  → exact match (symbol index)
  → graph edges (NetworkX)
  → vector search fallback (text match)
  → merge + deduplicate

analyze_impact
  → graph reverse traversal
  → pruning (remove noise: utils, helpers, loggers)
  → risk scoring
  → affected files + suggested actions

explain_symbol
  → symbol implementation (from search)
  → graph relationships (callers + callees + deps)
  → build summary
```

### Scoring Formula

```text
# Stage 1: Hybrid retrieval (4 signals)
hybrid = 0.35 * vector + 0.30 * BM25 + 0.20 * symbol_index + 0.15 * graph

# Stage 2: Cross-encoder reranker
final = 0.60 * cross_encoder + 0.30 * hybrid + 0.10 * symbol_bonus
```

## Yêu cầu

- Python >= 3.11
- macOS / Linux

## Cài đặt

```bash
cd /Users/chanh/workspace

# Tạo virtual environment
python -m venv .venv
source .venv/bin/activate

# Copy file env
cp .env.example .env

# Cài package (editable mode)
pip install -e '.[dev]'
```

## Environment Variables

Xem `.env.example` để biết đầy đủ. Tất cả biến dùng prefix `AI_CORE_`.

| Biến                                  | Mô tả                           | Mặc định                 |
| ------------------------------------- | ------------------------------- | ------------------------ |
| `AI_CORE_PROJECTS_FILE`               | File danh sách project          | `projects.json`          |
| `AI_CORE_DATA_DIR`                    | Thư mục lưu indexed data        | `data`                   |
| `AI_CORE_EMBEDDING_DIM`               | Chiều vector embedding          | `768`                    |
| `AI_CORE_EMBEDDING_MODEL`             | Model embedding                 | `BAAI/bge-base-en-v1.5`  |
| `AI_CORE_USE_CROSS_ENCODER`           | Bật cross-encoder reranker      | `true`                   |
| `AI_CORE_RERANKER_MODEL`              | Model reranker                  | `BAAI/bge-reranker-base` |
| `AI_CORE_RERANKER_TOP_K`              | Số kết quả sau rerank           | `10`                     |
| `AI_CORE_GRAPH_MAX_DEPTH`             | Độ sâu traversal graph          | `2`                      |
| `AI_CORE_GRAPH_MAX_NODES`             | Số node tối đa trả về           | `50`                     |
| `AI_CORE_GRAPH_INCLUDE_TESTS`         | Bao gồm test files trong impact | `false`                  |
| `AI_CORE_RETRIEVAL_CACHE_TTL_MINUTES` | TTL cache retrieval (phút)      | `30`                     |

## Index project

Index là bước bắt buộc — parse code, tạo embeddings, build dependency graph, populate symbol index và relationship index, lưu vào `data/`.

```bash
source .venv/bin/activate

# Index một project (incremental — chỉ xử lý file thay đổi)
python scripts/index_project.py <project-name>

# Full re-index (xóa cache, rebuild toàn bộ)
python scripts/index_project.py <project-name> --full

# Index tất cả projects
python scripts/index_project.py business-lounge-api --full
python scripts/index_project.py business-lounge-job --full
python scripts/index_project.py business-lounge-portal --full
```

### Indexing Pipeline

```text
Scanner (file_state: hash, mtime, language)
  → Tree-sitter Parser
  → Symbol Extractor (function, method, class, interface, enum)
  → Import/Call Extractor (import refs, call refs per symbol)
  → Chunker (symbol-aware: per function/method/class + metadata)
  → Embedder (bge-base-en-v1.5, prefix "kind: symbol_name\n" + content)
  → LanceDB (upsert vectors + metadata)
  → Graph Builder (defines, imports, calls edges)
  → Symbol Index (name, qualified_name, kind, file, lines, signature)
  → Relationship Index (calls, called_by, reads, writes, uses_dto)
  → Mark file_state: status=indexed, last_indexed_at=now
```

### Chunk Schema

Mỗi chunk là một đơn vị retrieval — index theo code structure, không phải fixed-size text:

```json
{
  "chunk_id": "sha1_hash",
  "file_path": "src/admin/services/BatchExceptionListService.service.ts",
  "language": "typescript",
  "symbol": "BatchExceptionListService.batchCreateExceptionListShortTerm",
  "kind": "method",
  "content": "public async batchCreateExceptionListShortTerm(...) { ... }",
  "line_start": 212,
  "line_end": 383,
  "metadata": {
    "imports": ["../../utils/convertTimeZone", "class-validator", "exceljs"],
    "calls": [
      "validatePartnerAccess",
      "validateFileMimeType",
      "airportLoungeExceptionListCreate"
    ],
    "class": "BatchExceptionListService",
    "type": "method"
  }
}
```

### Stores được populate khi index

| Store                     | Data                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| **file_state**            | file_path, content_hash, size_bytes, language, last_modified_at, last_indexed_at, status |
| **symbol_index**          | name, qualified_name, kind, file_path, line_start, line_end, signature                   |
| **code_chunks (LanceDB)** | chunk_id, file_path, symbol, kind, language, content, vector embedding, metadata         |
| **graph (NetworkX)**      | DiGraph: file→symbol (defines), file→module (imports), symbol→symbol (calls)             |
| **relationship_index**    | symbol, file_path, reads, writes, calls, called_by, uses_dto, uses_model                 |
| **retrieval_cache**       | TTL-based cache cho repeated queries                                                     |

### Danh sách projects (projects.json)

| Project                | Path                                         | Languages              |
| ---------------------- | -------------------------------------------- | ---------------------- |
| business-lounge-api    | /Users/chanh/Projects/business-lounge-api    | TypeScript, JavaScript |
| business-lounge-job    | /Users/chanh/Projects/business-lounge-job    | TypeScript, JavaScript |
| business-lounge-portal | /Users/chanh/Projects/business-lounge-portal | JavaScript             |

## Đồng bộ (Re-index)

Khi code trong project thay đổi, cần re-index để MCP có data mới.

### Re-index thủ công

```bash
# Incremental (chỉ file thay đổi)
python scripts/index_project.py business-lounge-api

# Full (rebuild tất cả)
python scripts/index_project.py business-lounge-api --full
```

### Reindex + Restart MCP

```bash
./scripts/reindex_and_restart.sh business-lounge-api --full
```

Script này sẽ reindex project rồi kill MCP server (Kiro auto-restart).

### Watcher (incremental tự động)

Watcher theo dõi file thay đổi và cập nhật **vector index** tự động (chunks + embeddings).

> **Lưu ý:** Watcher không rebuild dependency graph, symbol index, hay relationship index — chạy `index_project.py` khi cần data đầy đủ (thêm/xóa import, đổi dependency structure).

```bash
python scripts/watch_project.py business-lounge-api
```

### Khi nào cần re-index?

| Thay đổi                           | Cần re-index?                                      |
| ---------------------------------- | -------------------------------------------------- |
| Sửa nội dung function body         | Có (watcher xử lý vector, graph cần full re-index) |
| Thêm/xóa/rename file               | Có                                                 |
| Thêm/đổi import, thêm method mới   | Có (full — để rebuild graph + symbol index)        |
| Thêm project mới vào projects.json | Có — chạy index project mới                        |
| Chỉ sửa config/env                 | Không                                              |

## Cấu hình MCP trong IDE

MCP chạy qua **stdio** — IDE tự spawn process, không cần bật server thủ công.

### Kiro

File: `~/.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "intelligence_engine": {
      "command": "/Users/chanh/workspace/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/Users/chanh/workspace",
      "env": {
        "AI_CORE_PROJECTS_FILE": "projects.json",
        "AI_CORE_DATA_DIR": "data"
      },
      "disabled": false,
      "autoApprove": [
        "search_code",
        "get_context",
        "analyze_impact",
        "find_references",
        "explain_symbol"
      ]
    }
  }
}
```

### Cursor

File: `.cursor/mcp.json` trong workspace

```json
{
  "mcpServers": {
    "ai-core": {
      "command": "/Users/chanh/workspace/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/Users/chanh/workspace",
      "env": {
        "AI_CORE_PROJECTS_FILE": "projects.json",
        "AI_CORE_DATA_DIR": "data"
      }
    }
  }
}
```

## MCP Tools

| Tool              | Mục đích                                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| `search_code`     | Tìm candidates: vector + BM25 + symbol + graph → rerank. Gợi ý `get_context` qua `next_recommended_tool`. |
| `get_context`     | Load full context cho AI: search → expand → token budget. Dùng SAU search_code, TRƯỚC khi edit.           |
| `analyze_impact`  | Blast radius: graph traversal + risk scoring                                                              |
| `find_references` | Tìm references: symbol index + graph edges                                                                |
| `explain_symbol`  | Tóm tắt symbol: implementation + callers + side effects                                                   |
| `reindex_project` | Reload stores từ disk (sau khi chạy index_project.py)                                                     |

### Tool Call Flow (search → context → edit)

```text
Agent cần sửa code:
  1. search_code(query, project)     → tìm candidates, trả snippet ngắn + next_recommended_tool
  2. get_context(query, project)     → load full implementation + imports + callers + DTO/model
  3. Edit code                       → giờ agent có đủ context để sửa chính xác

Agent chỉ cần tìm file:
  1. search_code(query, project)     → đủ, không cần get_context

Shortcut (gộp 1 call):
  1. search_code(query, project, include_context=true)  → trả cả search results + full context
```

### search_code — Tool Design

**Parameters:**

| Param             | Type   | Default | Mô tả                                         |
| ----------------- | ------ | ------- | --------------------------------------------- |
| `query`           | string | —       | Natural language hoặc symbol name             |
| `project`         | string | —       | Project name (last segment of workspace path) |
| `top_k`           | int    | 10      | Số kết quả tối đa                             |
| `include_context` | bool   | false   | Tự động gọi get_context inline                |
| `max_tokens`      | int    | 12000   | Token budget khi include_context=true         |

**Output (include_context=false):**

```json
{
  "summary": "Found 3 result(s) for 'IntegrationJwtStrategy'...",
  "results": [
    {
      "file": "src/core/auth/strategies/integration-jwt-strategy.service.ts",
      "symbol": "IntegrationJwtStrategy",
      "kind": "class",
      "line_start": 12,
      "line_end": 61,
      "score": 0.788,
      "reason": "Contains: auth, strategy, jwt",
      "snippet": "export class IntegrationJwtStrategy extends PassportStrategy(...) { ... }"
    }
  ],
  "next_recommended_tool": {
    "name": "get_context",
    "reason": "Use get_context to load full implementation, imports, references, and related files before editing.",
    "input": {
      "query": "IntegrationJwtStrategy",
      "project": "business-lounge-api",
      "max_tokens": 12000
    }
  },
  "missing_context": [],
  "confidence": 0.95
}
```

**Output (include_context=true):**

```json
{
  "summary": "Found 3 result(s)...",
  "results": [{ "file", "symbol", "score", "snippet" }],
  "context": {
    "meta": { "intent": "search", "confidence": 0.86, "token_budget": { "max": 12000, "used": 4200 } },
    "summary": "...",
    "results": { "references": [...], "chunks": [...], "dependency_paths": [...] }
  },
  "missing_context": [],
  "confidence": 0.95
}
```

### Agent Guidance (3 lớp hướng dẫn)

| Lớp | Cơ chế                      | Mô tả                                                                 |
| --- | --------------------------- | --------------------------------------------------------------------- |
| 1   | **Tool description**        | Ghi rõ "Do NOT edit based only on search_code results"                |
| 2   | **`next_recommended_tool`** | Output tự gợi ý tool tiếp theo + input sẵn sàng copy-paste            |
| 3   | **`include_context`**       | Fallback: gộp search + context trong 1 call khi agent không gọi riêng |

## Output Schema (get_context)

`get_context` trả về 6 context layers:

```json
{
  "meta": {
    "intent": "refactor",
    "confidence": 0.86,
    "token_budget": { "max": 12000, "used": 6800 }
  },
  "summary": "...",
  "results": {
    "intent_context": { "intent", "query", "target" },
    "symbols": [{ "name", "qualified_name", "kind", "file", "line_start", "line_end", "reason" }],
    "chunks": [{ "file", "symbol", "kind", "line_start", "line_end", "reason", "content" }],
    "dependency_paths": [{ "from", "to", "relation", "reason" }],
    "impact": {
      "risk_level": "medium",
      "affected_files": [{ "file", "reason" }],
      "suggested_actions": ["..."]
    },
    "prompt_guidance": "..."
  },
  "missing_context": ["..."]
}
```

| Layer | Field              | Mô tả                                           |
| ----- | ------------------ | ----------------------------------------------- |
| 1     | `intent_context`   | Intent + query + target symbol                  |
| 2     | `summary`          | Tóm tắt ngắn cho LLM                            |
| 3     | `symbols`          | Symbols liên quan + lý do                       |
| 4     | `chunks`           | Code thật sự (function/method body)             |
| 5     | `dependency_paths` | Call chain / dependency flow                    |
| 6     | `impact`           | Affected files + risk level + suggested actions |

## Cách hoạt động (end-to-end)

```text
1. IDE mở → đọc mcp.json
2. Agent cần tìm code → IDE spawn: python -m mcp_server.server
3. Agent gọi tool qua stdin (JSON-RPC):

   # Bước 1: Tìm candidates
   search_code(query="IntegrationJwtStrategy", project="business-lounge-api")
   → trả snippet ngắn + next_recommended_tool gợi ý get_context

   # Bước 2: Load full context (nếu cần sửa code)
   get_context(query="IntegrationJwtStrategy", project="business-lounge-api")
   → trả full implementation + imports + callers + DTO/model

   # Hoặc gộp 1 bước:
   search_code(query="IntegrationJwtStrategy", project="business-lounge-api", include_context=true)
   → trả cả search results + full context inline

4. MCP server → hybrid search (vector + BM25 + symbol + graph) → rerank (bge-reranker-base)
5. Trả kết quả qua stdout → Agent dùng để trả lời / edit code
6. Process sống suốt IDE session, tự tắt khi đóng IDE
```

## Performance

| Metric                      | Value    |
| --------------------------- | -------- |
| First query (model loading) | ~22s     |
| Subsequent queries          | 0.5–1.0s |
| Index time (636 files)      | ~60s     |
| Embedding model memory      | ~450MB   |
| Reranker model memory       | ~1.1GB   |

## Upgrade Path

Khi cần chất lượng cao hơn, chỉ cần đổi config trong `.env`:

| Component | Current                 | Upgrade                                                |
| --------- | ----------------------- | ------------------------------------------------------ |
| Embedding | bge-base-en-v1.5 (768d) | Qwen3-Embedding-0.6B hoặc text-embedding-3-small (API) |
| Reranker  | bge-reranker-base       | bge-reranker-v2-m3 hoặc API-based                      |
| Vector DB | JSON persistence        | Native LanceDB hoặc Qdrant                             |

## IDE sync (skills + rules)

Sau khi chạy sync script, IDE rules và skills sẽ symlink vào repo này:

```bash
./scripts/sync-ide.sh
```

## Troubleshooting

| Vấn đề                                                             | Giải pháp                                                       |
| ------------------------------------------------------------------ | --------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'intelligence_engine'`       | Chưa install: `pip install -e '.'`                              |
| `ModuleNotFoundError: No module named 'tree_sitter_language_pack'` | Cần dùng `.venv` python, không phải system python               |
| MCP không kết nối trong IDE                                        | Kiểm tra path python trong mcp.json trỏ đúng `.venv/bin/python` |
| Search trả kết quả không liên quan                                 | Chạy `reindex_project` tool hoặc reindex script                 |
| Search trả rỗng                                                    | Project chưa index hoặc sai tên project                         |
| Index chậm lần đầu                                                 | Bình thường — embedding 2500+ chunks mất ~60s                   |
| MCP server dùng data cũ sau reindex                                | Gọi `reindex_project` tool hoặc reconnect MCP server            |
| `lru_cache` giữ settings cũ                                        | Restart MCP server (kill process + reconnect)                   |
| file_state status luôn pending                                     | Cần re-index: `python scripts/index_project.py <name> --full`   |
