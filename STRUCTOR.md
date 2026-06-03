# Cấu trúc repo

Repo **AI Core** — Python MCP Server + Codebase Intelligence Engine, kèm skills + rules cho Cursor / Kiro.

## Tham chiếu

| Nội dung         | File                                         |
| ---------------- | -------------------------------------------- |
| Tổng quan & lệnh | [README.md](README.md)                       |
| Agent policy     | [AGENTS.md](AGENTS.md)                       |
| Kiến trúc engine | [docs/architecture.md](docs/architecture.md) |
| Rules layout     | [rules/CONVENTIONS.md](rules/CONVENTIONS.md) |
| Skills layout    | [skills/STRUCTURE.md](skills/STRUCTURE.md)   |

## Cây thư mục

```text
Workspace/
├── AGENTS.md
├── README.md
├── pyproject.toml          # Python project config
├── projects.json           # Danh sách project để index
├── mcp_server/             # MCP stdio server (FastMCP)
│   ├── server.py           # Entrypoint — tool definitions
│   ├── registry.py         # Tool → handler mapping
│   └── tools/              # Từng tool implementation
├── intelligence_engine/    # Codebase Intelligence Engine
│   ├── project_loader/     # Load project config
│   ├── scanner/            # File scan + watcher
│   ├── parser/             # Tree-sitter language parsers
│   ├── symbols/            # Symbol & import extraction
│   ├── chunking/           # Code chunking
│   ├── embedding/          # Vector embedding
│   ├── storage/            # LanceDB + Graph + FileState persistence
│   ├── graph/              # NetworkX code graph + analysis
│   ├── retrieval/          # Hybrid search + reranker
│   ├── context/            # Token-budgeted context builder
│   ├── config/             # Settings (pydantic-settings)
│   └── api/                # FastAPI HTTP interface (optional)
├── scripts/                # index_project, watch_project, sync-ide, verify
├── tests/                  # pytest test suite
├── data/                   # Runtime data (lancedb, graph, file_state)
├── docs/                   # Architecture & flow docs
├── skills/                 # Canonical agent skills
├── rules/
│   ├── cursor/             # Cursor .mdc — sửa tại đây
│   ├── kiro/               # Kiro steering — tự sinh
│   ├── CONVENTIONS.md
│   └── QUICKSTART.md
└── rules.zip / skills.zip  # optional bundles
```

**IDE:** Sau `./scripts/sync-ide.sh` → `~/.cursor/rules`, `~/.cursor/skills`, `~/.kiro/steering`, `~/.kiro/skills` trỏ vào repo.
