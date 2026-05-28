# Cấu trúc repo (đã rút gọn)

Tài liệu inventory chi tiết từng file **không còn duy trì** tại đây.

## Tham chiếu

| Nội dung | File |
|----------|------|
| Tổng quan & lệnh nhanh | [README.md](README.md) |
| Cài đặt | [docs/SETUP.md](docs/SETUP.md) |
| Kiến trúc | [docs/architecture.md](docs/architecture.md) |
| Indexing | [docs/indexing-flow.md](docs/indexing-flow.md) |
| Retrieval | [docs/retrieval-flow.md](docs/retrieval-flow.md) |
| MCP tools | [docs/mcp-tools.md](docs/mcp-tools.md) |
| Thêm project | [docs/ADD-PROJECT.md](docs/ADD-PROJECT.md) |
| Roadmap | [docs/ROADMAP.md](docs/ROADMAP.md) |

## Cây thư mục (tóm tắt)

```text
Workspace/
├── intelligence-engine/   # FastAPI — index, search, graph
├── mcp-server/            # MCP HTTP bridge
├── projects/              # App repos (gitignored, clone local)
├── projects.json          # Cấu hình index (local, gitignored)
├── config/                # MCP templates
├── scripts/               # setup, index, verify
├── docs/
├── skills/                # Nguồn skills (canonical)
├── rules/
│   ├── cursor/            # Cursor rules .mdc (sửa tại đây)
│   └── kiro/              # Kiro steering (tự sinh)
└── .cursor/               # MCP config; rules/skills → `make sync-ide` → ~/.cursor/, ~/.kiro/
```
