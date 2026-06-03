# AI Core

Python MCP Server + Codebase Intelligence Engine for Cursor / Kiro.

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
       └── explain_symbol
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
pip install -e .[dev]
```

## Index project

Index là bước bắt buộc — parse code, tạo embeddings, build dependency graph, lưu vào `data/`.

### Index một project

```bash
source .venv/bin/activate
python scripts/index_project.py <project-name>
```

### Index tất cả projects

```bash
source .venv/bin/activate
python scripts/index_project.py business-lounge-api
python scripts/index_project.py business-lounge-job
python scripts/index_project.py business-lounge-portal
python scripts/index_project.py operator-api
python scripts/index_project.py vpid-mobile-api
```

### Danh sách projects (projects.json)

| Project                | Path                                         | Language   |
| ---------------------- | -------------------------------------------- | ---------- |
| business-lounge-api    | /Users/chanh/Projects/business-lounge-api    | TypeScript |
| business-lounge-job    | /Users/chanh/Projects/business-lounge-job    | TypeScript |
| business-lounge-portal | /Users/chanh/Projects/business-lounge-portal | JavaScript |
| operator-api           | /Users/chanh/Projects/operator-api           | TypeScript |
| vpid-mobile-api        | /Users/chanh/Projects/vpid-mobile-api        | C#         |

## Đồng bộ (Re-index)

Khi code trong project thay đổi (thêm file, sửa logic, refactor), cần re-index để MCP có data mới.

### Cách 1: Re-index thủ công

Chạy lại lệnh index cho project đã thay đổi:

```bash
source .venv/bin/activate
python scripts/index_project.py business-lounge-api
```

### Cách 2: Watcher (tự động incremental)

Watcher theo dõi file thay đổi và cập nhật index tự động:

```bash
source .venv/bin/activate
python scripts/watch_project.py business-lounge-api
```

Watcher chạy liên tục — mở terminal riêng hoặc dùng background process:

```bash
nohup python scripts/watch_project.py business-lounge-api &
```

### Khi nào cần re-index?

| Thay đổi                           | Cần re-index?               |
| ---------------------------------- | --------------------------- |
| Sửa nội dung file                  | Có (watcher xử lý tự động)  |
| Thêm/xóa file                      | Có                          |
| Thêm project mới vào projects.json | Có — chạy index project mới |
| Chỉ sửa config/env                 | Không                       |
| Rename/move file                   | Có                          |

## Cấu hình MCP trong IDE

MCP chạy qua **stdio** — IDE tự spawn process Python, không cần bật server thủ công.

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
        "AI_CORE_DATA_DIR": "data",
        "AI_CORE_EMBEDDING_DIM": "384"
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
        "AI_CORE_DATA_DIR": "data",
        "AI_CORE_EMBEDDING_DIM": "384"
      }
    }
  }
}
```

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

## MCP Tools

| Tool              | Mục đích                                           |
| ----------------- | -------------------------------------------------- |
| `search_code`     | Tìm code theo semantic similarity + keyword        |
| `get_context`     | Lấy context trong budget token (dùng cho prompt)   |
| `analyze_impact`  | Phân tích blast radius trước khi sửa shared symbol |
| `find_references` | Tìm tất cả nơi reference đến symbol                |
| `explain_symbol`  | Tóm tắt symbol trong dependency graph              |

## API server (optional, cho debug/test)

```bash
source .venv/bin/activate
uvicorn intelligence_engine.api.main:app --reload --port 8000
```

Hoặc dùng Docker:

```bash
docker compose up
```

## Cấu trúc thư mục

```text
workspace/
├── mcp_server/           # MCP stdio server + tool registry
│   ├── server.py         # FastMCP entrypoint
│   ├── registry.py       # Tool → function mapping
│   └── tools/            # Từng tool một file
├── intelligence_engine/  # Core engine
│   ├── api/              # HTTP API (optional)
│   ├── chunking/         # Code chunker
│   ├── config/           # Engine config
│   ├── context/          # Context builder
│   ├── embedding/        # Vector embedder
│   ├── graph/            # NetworkX graph builder
│   ├── parser/           # Tree-sitter parser
│   ├── project_loader/   # Load projects.json
│   ├── retrieval/        # Retrieval engine (search + graph)
│   ├── scanner/          # File scanner
│   ├── storage/          # LanceDB storage
│   └── symbols/          # Symbol extractor
├── scripts/              # CLI scripts
│   ├── index_project.py  # Index một project
│   └── watch_project.py  # Watcher incremental
├── data/                 # Indexed data (gitignored)
│   ├── lancedb/          # Vector embeddings
│   ├── graph/            # Dependency graphs
│   └── file_state/       # File state tracking
├── projects.json         # Danh sách projects
├── .env                  # Environment variables
└── pyproject.toml        # Python package config
```

## Troubleshooting

| Vấn đề                                                       | Giải pháp                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------------ |
| `ModuleNotFoundError: No module named 'intelligence_engine'` | Chưa install: `pip install -e .`                                   |
| MCP không kết nối trong IDE                                  | Kiểm tra path python trong mcp.json trỏ đúng `.venv/bin/python`    |
| Search trả rỗng                                              | Project chưa index hoặc sai tên project                            |
| Index chậm với project lớn                                   | Bình thường — lần đầu parse toàn bộ, lần sau incremental nhanh hơn |
| Watcher không detect thay đổi                                | Kiểm tra exclude patterns trong projects.json                      |
