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
│       └── explain_symbol.py
│
├── intelligence_engine/    # Codebase Intelligence Engine
│   ├── config/             # Settings (pydantic-settings, đọc .env)
│   ├── project_loader/     # Load project config từ projects.json
│   ├── scanner/            # File scan + watcher
│   ├── parser/             # Tree-sitter language parsers
│   ├── symbols/            # Symbol & import extraction
│   ├── chunking/           # Code chunking strategies
│   ├── embedding/          # Vector embedding (sentence-transformers)
│   ├── storage/            # LanceDB + Graph + FileState persistence
│   ├── graph/              # NetworkX code graph + pruning
│   ├── retrieval/          # Hybrid search + reranker
│   ├── context/            # Token-budgeted context builder + orchestrator
│   └── api/                # FastAPI HTTP interface (optional, debug)
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
│   ├── lancedb/            # Vector embeddings
│   ├── graph/              # Dependency graphs (NetworkX)
│   └── file_state/         # File state tracking (incremental)
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
