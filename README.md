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

# (Optional) Cài reranker cho retrieval chất lượng hơn
pip install -e '.[reranker]'
```

## Environment Variables

Xem `.env.example` để biết đầy đủ. Tất cả biến dùng prefix `AI_CORE_`.

| Biến                                  | Mô tả                                  | Mặc định                               |
| ------------------------------------- | -------------------------------------- | -------------------------------------- |
| `AI_CORE_PROJECTS_FILE`               | File danh sách project                 | `projects.json`                        |
| `AI_CORE_DATA_DIR`                    | Thư mục lưu indexed data               | `data`                                 |
| `AI_CORE_EMBEDDING_DIM`               | Chiều vector embedding                 | `384`                                  |
| `AI_CORE_USE_CROSS_ENCODER`           | Bật cross-encoder reranker             | `false`                                |
| `AI_CORE_RERANKER_MODEL`              | Model reranker (sentence-transformers) | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `AI_CORE_RERANKER_TOP_K`              | Số kết quả sau rerank                  | `10`                                   |
| `AI_CORE_GRAPH_MAX_DEPTH`             | Độ sâu traversal graph                 | `2`                                    |
| `AI_CORE_GRAPH_MAX_NODES`             | Số node tối đa trả về                  | `50`                                   |
| `AI_CORE_GRAPH_INCLUDE_TESTS`         | Bao gồm test files trong impact        | `false`                                |
| `AI_CORE_RETRIEVAL_CACHE_TTL_MINUTES` | TTL cache retrieval (phút)             | `30`                                   |

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
python scripts/index_project.py operator-api --full
python scripts/index_project.py vpid-mobile-api --full
```

### Indexing Pipeline

```text
Scanner (file_state: hash, mtime, language)
   → Tree-sitter Parser
   → Symbol Extractor (symbol_index: name, kind, file, lines, signature)
   → Chunker (code_chunks: symbol, kind, content + vector embedding)
   → Graph Builder (graph_edges: defines, imports, calls, reads, writes)
   → Relationship Index (per-symbol: calls, called_by, reads, writes, uses_dto)
   → Mark file_state: status=indexed, last_indexed_at=now
```

### Stores được populate khi index

| Store                  | Data                                                                                     |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| **file_state**         | file_path, content_hash, size_bytes, language, last_modified_at, last_indexed_at, status |
| **symbol_index**       | name, qualified_name, kind, file_path, line_start, line_end, signature                   |
| **code_chunks**        | chunk_id, file_path, symbol, kind, language, content, vector embedding                   |
| **graph_edges**        | NetworkX DiGraph: file→symbol (defines), file→module (imports), file→route               |
| **relationship_index** | symbol, file_path, reads, writes, calls, called_by, uses_dto, uses_model                 |
| **retrieval_cache**    | TTL-based cache cho repeated queries                                                     |

### Danh sách projects (projects.json)

| Project                | Path                                         | Languages              |
| ---------------------- | -------------------------------------------- | ---------------------- |
| business-lounge-api    | /Users/chanh/Projects/business-lounge-api    | TypeScript, JavaScript |
| business-lounge-job    | /Users/chanh/Projects/business-lounge-job    | TypeScript, JavaScript |
| business-lounge-portal | /Users/chanh/Projects/business-lounge-portal | JavaScript             |
| operator-api           | /Users/chanh/Projects/operator-api           | TypeScript, JavaScript |
| vpid-mobile-api        | /Users/chanh/Projects/vpid-mobile-api        | C#                     |

## Đồng bộ (Re-index)

Khi code trong project thay đổi, cần re-index để MCP có data mới.

### Re-index thủ công

```bash
python scripts/index_project.py business-lounge-api
```

### Watcher (incremental tự động)

Watcher theo dõi file thay đổi và cập nhật **vector index** tự động (chunks + embeddings).

> **Lưu ý:** Watcher không rebuild dependency graph, symbol index, hay relationship index — chạy `index_project.py` khi cần data đầy đủ (thêm/xóa import, đổi dependency structure).

```bash
python scripts/watch_project.py business-lounge-api
```

### Khi nào cần re-index?

| Thay đổi                           | Cần re-index?                                      |
| ---------------------------------- | -------------------------------------------------- |
| Sửa nội dung file                  | Có (watcher xử lý vector, graph cần full re-index) |
| Thêm/xóa/rename file               | Có                                                 |
| Thêm project mới vào projects.json | Có — chạy index project mới                        |
| Chỉ sửa config/env                 | Không                                              |

## Cấu hình MCP trong IDE

MCP chạy qua **stdio** — IDE tự spawn process, không cần bật server thủ công.

### Kiro

File: `~/.kiro/settings/mcp.json` hoặc `<workspace>/.kiro/settings/mcp.json`

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

| Tool              | Mục đích                                           |
| ----------------- | -------------------------------------------------- |
| `search_code`     | Tìm code theo semantic similarity + keyword        |
| `get_context`     | Lấy context trong budget token (dùng cho prompt)   |
| `analyze_impact`  | Phân tích blast radius trước khi sửa shared symbol |
| `find_references` | Tìm tất cả nơi reference đến symbol                |
| `explain_symbol`  | Tóm tắt symbol trong dependency graph              |
| `reindex_project` | Clear cache và trigger re-index                    |

## Output Schema (get_context)

`get_context` trả về 6 context layers theo architecture spec:

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

| Layer | Field trong results   | Mô tả                                           |
| ----- | --------------------- | ----------------------------------------------- |
| 1     | `intent_context`      | Intent + query + target symbol                  |
| 2     | (top-level `summary`) | Tóm tắt ngắn cho LLM                            |
| 3     | `symbols`             | Symbols liên quan + lý do                       |
| 4     | `chunks`              | Code thật sự (function/method body)             |
| 5     | `dependency_paths`    | Call chain / dependency flow                    |
| 6     | `impact`              | Affected files + risk level + suggested actions |

## Cách hoạt động (end-to-end)

```text
1. IDE mở → đọc mcp.json
2. Agent cần tìm code → IDE spawn: python -m mcp_server.server
3. Agent gọi tool qua stdin (JSON-RPC):
   search_code(query="AuthGuard", project="business-lounge-api")
4. MCP server → retrieval engine → semantic search LanceDB + graph traversal
5. Trả context qua stdout → Agent dùng để trả lời / edit code
6. Process sống suốt IDE session, tự tắt khi đóng IDE
```

## API server (optional)

Dùng cho debug/test ngoài IDE:

```bash
source .venv/bin/activate
uvicorn intelligence_engine.api.main:app --reload --port 8000
```

Hoặc qua Docker:

```bash
docker compose up
```

## IDE sync (skills + rules)

Sau khi chạy sync script, IDE rules và skills sẽ symlink vào repo này:

```bash
./scripts/sync-ide.sh
```

Kết quả: `~/.cursor/rules` → `rules/cursor/`, `~/.kiro/steering` → `rules/kiro/`, tương tự cho skills.

## Troubleshooting

| Vấn đề                                                       | Giải pháp                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------------ |
| `ModuleNotFoundError: No module named 'intelligence_engine'` | Chưa install: `pip install -e '.'`                                 |
| MCP không kết nối trong IDE                                  | Kiểm tra path python trong mcp.json trỏ đúng `.venv/bin/python`    |
| Search trả rỗng                                              | Project chưa index hoặc sai tên project                            |
| Index chậm với project lớn                                   | Bình thường — lần đầu parse toàn bộ, lần sau incremental nhanh hơn |
| Watcher không detect thay đổi                                | Kiểm tra exclude patterns trong projects.json                      |
| `zsh: no matches found: .[dev]`                              | Dùng quotes: `pip install -e '.[dev]'`                             |
| file_state status luôn pending                               | Cần re-index: `python scripts/index_project.py <name> --full`      |
