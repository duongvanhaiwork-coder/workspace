# Cấu trúc repo

Repo **skills + rules** — không chứa intelligence-engine / mcp-server trong cây này.

## Tham chiếu

| Nội dung | File |
| -------- | ---- |
| Tổng quan & lệnh | [README.md](README.md) |
| Agent policy | [AGENTS.md](AGENTS.md) |
| Workflow (VI) | [docs/WORKFLOW-QUICKSTART.md](docs/WORKFLOW-QUICKSTART.md) |
| Rules layout | [rules/CONVENTIONS.md](rules/CONVENTIONS.md) |
| Skills layout | [skills/STRUCTURE.md](skills/STRUCTURE.md) |

## Cây thư mục

```text
Workspace/
├── AGENTS.md
├── README.md
├── docs/
│   └── WORKFLOW-QUICKSTART.md
├── scripts/               # sync-ide, verify (không symlink vào IDE)
├── skills/                # Canonical agent skills
├── rules/
│   ├── cursor/            # Cursor .mdc — sửa tại đây
│   ├── kiro/              # Kiro steering — tự sinh
│   ├── CONVENTIONS.md
│   └── QUICKSTART.md
└── rules.zip / skills.zip # optional bundles
```

**IDE:** Sau `./scripts/sync-ide.sh` → `~/.cursor/rules`, `~/.cursor/skills`, `~/.kiro/steering`, `~/.kiro/skills` trỏ vào repo.
