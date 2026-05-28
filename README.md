# AI Core

Code intelligence cho AI IDE (Cursor / Kiro): indexing, vector search, context, dependency graph.

**Chiến lược:** [cá nhân trước](docs/SETUP.md) → [team sau](docs/TEAM.md) (mỗi người một máy local, cùng stack).

## Bắt đầu nhanh

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
# chỉnh projects.json cho repo của bạn
./scripts/index-all.sh
```

Chi tiết: **[docs/SETUP.md](docs/SETUP.md)**

**Workflow agent (question-scope + Superpowers):** **[docs/WORKFLOW-QUICKSTART.md](docs/WORKFLOW-QUICKSTART.md)** · policy: **[AGENTS.md](AGENTS.md)**

## Thành phần

| Thành phần | Vai trò |
|------------|---------|
| `mcp-server` | HTTP tools cho IDE |
| `mcp-bridge.mjs` | MCP stdio ↔ HTTP |
| `intelligence-engine` | FastAPI — index, search, graph |
| `intelligence-worker` | Background indexing (Redis/RQ) |
| `ollama` | Embeddings local |
| `projects/` | Source code cần phân tích (clone local, không commit) |
| `projects.json` | Cấu hình project (local, không commit) |
| `skills/` | Agent skills (nguồn chính) |
| `rules/cursor/` | Cursor rules `.mdc` (nguồn chính) |
| `rules/kiro/` | Kiro steering (tự sinh từ `rules/cursor/`) |
| `.cursor/rules/`, `.cursor/skills/` | Symlink → `rules/`, `skills/` |
| `.kiro/steering/`, `.kiro/skills/` | Symlink → `rules/kiro/`, `skills/` |

## Lệnh Make

Chạy từ **thư mục gốc** `Workspace/` (nơi có `Makefile`):

```bash
make setup      # = ./scripts/setup.sh
make ide-config # = ./scripts/install-ide-config.sh
make sync-ide   # = ./scripts/sync-ide.sh
make up         # docker compose up
make index      # = ./scripts/index-all.sh
make verify     # = ./scripts/verify.sh
make health
make logs
```

## Scripts (`scripts/`)

Thư mục này chứa **7 file shell** (`.sh`) — automation cho cài đặt, IDE, indexing và kiểm tra chất lượng. Không có script nào khác ở đây; mỗi file một nhiệm vụ rõ.

### Quan hệ giữa các script

```text
setup.sh
  ├── install-ide-config.sh
  │     └── sync-ide.sh
  │           ├── sync-ide-skills.sh
  │           └── sync-ide-rules.sh
  └── docker compose up …

index-all.sh     →  gọi MCP (cần stack đang chạy)
verify.sh        →  độc lập, không cần Docker
```

### Bảng tóm tắt

| File | Làm gì (một câu) | Cần Docker? | Make |
|------|------------------|-------------|------|
| `setup.sh` | Onboarding toàn bộ máy mới | Có | `make setup` |
| `install-ide-config.sh` | Cài MCP + sync rules/skills cho IDE | Không | `make ide-config` |
| `sync-ide.sh` | Sync cả skills và rules | Không | `make sync-ide` |
| `sync-ide-skills.sh` | Chỉ sync skills | Không | — |
| `sync-ide-rules.sh` | Chỉ sync rules | Không | — |
| `index-all.sh` | Index tất cả project | Có (stack chạy) | `make index` |
| `verify.sh` | Test + lint + build local | Không | `make verify` |

---

### `setup.sh` — Cài đặt lần đầu (onboarding)

**Ý nghĩa:** Đưa máy từ “vừa clone repo” → “chạy được AI Core end-to-end”.

**Làm gì:**

| Bước | Hành động | Kết quả |
|------|-----------|---------|
| 1 | Tạo `.env` từ `.env.example` | Biến môi trường cho Docker/engine |
| 2 | Tạo `projects.json` từ `projects.json.example` | Danh sách repo cần index |
| 3 | Gọi `install-ide-config.sh` | Cursor/Kiro + symlink rules/skills |
| 4 | `docker compose up -d --build` | Redis, Ollama, engine, worker, MCP |
| 5 | Chờ health engine `:8000` và MCP `:3000` | Xác nhận stack sống |
| 6 | `ollama pull nomic-embed-text` | Model embedding cho vector search |

**Khi chạy:** Máy mới, lần đầu dùng AI Core, hoặc reset môi trường local.

**Sau khi chạy:** Sửa `projects.json`, clone app vào `projects/`, rồi `./scripts/index-all.sh`.

---

### `install-ide-config.sh` — Cấu hình Cursor / Kiro

**Ý nghĩa:** Cho IDE biết cách nói chuyện với MCP server `ai-core` trên máy bạn.

**Làm gì:**

| Đầu ra | Nguồn | Ghi chú |
|--------|-------|---------|
| `.cursor/mcp.json` | `config/cursor-mcp.json` | File generate — **không commit** |
| `.kiro/settings/mcp.json` | `config/kiro-mcp.json.template` | Path tương đối `../../mcp-server/mcp-bridge.mjs` (từ `.kiro/settings/`) |
| Symlink rules/skills | Gọi `sync-ide.sh` | Nếu có `skills/` hoặc `rules/cursor/` |

**Khi chạy:** Đổi đường dẫn workspace, cài Cursor/Kiro mới, hoặc MCP không kết nối sau khi move folder.

**Không làm:** Không start Docker (dùng `make up` hoặc `setup.sh`).

---

### `sync-ide.sh` — Đồng bộ rules + skills (entry point)

**Ý nghĩa:** Một lệnh để cập nhật toàn bộ cấu hình IDE sau khi bạn sửa nguồn `skills/` hoặc `rules/cursor/`.

**Làm gì:**

1. `rules/cursor/<stem>.mdc` → sinh `rules/kiro/<stem>.md` (cùng tên, trong repo)
2. Symlink **chỉ** thư mục home IDE:
   - `~/.cursor/rules/` → `rules/cursor/`
   - `~/.kiro/steering/` → `rules/kiro/`
   - `~/.cursor/skills/`, `~/.kiro/skills/` → `skills/`

**Không** tạo symlink trong `Workspace/.cursor/` hay `Workspace/.kiro/` (gitignore). Alias: `make link-global` = `make sync-ide`.

**Khi chạy:** Thêm/xóa skill, sửa `rules/cursor/*.mdc`, hoặc symlink IDE bị hỏng.

---

### `sync-ide-skills.sh` — Symlink agent skills

**Ý nghĩa:** `skills/` là **nguồn duy nhất**; Cursor và Kiro chỉ “trỏ tới” đó, không copy nội dung.

**Làm gì:**

- Symlink cả thư mục `~/.cursor/skills` và `~/.kiro/skills` → `Workspace/skills/`

**Khi chạy:** Thêm skill mới (vd. `skills/my-skill/SKILL.md`) hoặc sau khi restore `skills/`.

**Cảnh báo:** Không xóa `skills/` — IDE sẽ mất toàn bộ skill (symlink gãy).

---

### `sync-ide-rules.sh` — Symlink rules + sinh bản Kiro

**Ý nghĩa:** Một bộ quy tắc coding cho Cursor (`.mdc`); Kiro dùng format khác nên được **tự động convert**.

**Làm gì:**

| Bước | Chi tiết |
|------|----------|
| 1 | Đọc `rules/cursor/*.mdc` (frontmatter: `globs`, `alwaysApply`, …) |
| 2 | Sinh `rules/kiro/<stem>.md` (1:1 với cursor; frontmatter Kiro: `inclusion`, `fileMatchPattern`) |
| 3 | Symlink `~/.cursor/rules` → `rules/cursor/` |
| 4 | Symlink `~/.kiro/steering` → `rules/kiro/` |

**Sửa tay:** Chỉ `rules/cursor/*.mdc`. **Không sửa** `rules/kiro/` — sẽ bị ghi đè khi sync.

**Khi chạy:** Đổi convention Python/TS/React/C# hoặc thêm rule mới.

---

### `index-all.sh` — Index mọi project

**Ý nghĩa:** Đẩy job indexing vào queue (worker) để engine quét code, tạo embedding và code graph — phục vụ `search_code`, `get_context`, `analyze_impact` trong IDE.

**Làm gì:**

1. Đọc tên project từ `projects.json` (hoặc file trong `PROJECTS_CONFIG`)
2. Kiểm tra MCP healthy tại `MCP_SERVER_URL`
3. Với từng project: `POST /tools/index-project` với `{ project, force }`
4. Worker xử lý nền — theo dõi: `docker compose logs -f intelligence-worker`

**Biến môi trường:**

| Biến | Mặc định | Ý nghĩa |
|------|----------|---------|
| `MCP_SERVER_URL` | `http://localhost:3000` | URL MCP server |
| `FORCE_INDEX` | `false` | `true` = xóa index cũ, index lại từ đầu |
| `PROJECTS_CONFIG` | `projects.json` | File cấu hình danh sách project |

**Ví dụ:**

```bash
./scripts/index-all.sh
FORCE_INDEX=true ./scripts/index-all.sh
```

**Khi chạy:** Sau clone repo app, merge lớn, đổi cấu trúc folder, hoặc search MCP trả rỗng.

---

### `verify.sh` — Kiểm tra chất lượng code (không Docker)

**Ý nghĩa:** Chạy cùng loại kiểm tra như CI trên máy local — nhanh, không cần Ollama/Redis.

**Làm gì:**

| Phần | Lệnh | Mục đích |
|------|------|----------|
| `intelligence-engine` | `ruff check src` | Lint Python |
| | `pytest -q` | Unit test engine |
| `mcp-server` | `npm ci` + `npm run build` | Build TypeScript MCP |

Tự tạo `.venv` trong `intelligence-engine/` nếu chưa có.

**Khi chạy:** Trước commit/PR, sau sửa engine hoặc MCP, debug CI fail local.

**Không làm:** Không test integration Docker, không test embedding thật.

## Docs

- [SETUP.md](docs/SETUP.md) — cài đặt cá nhân (bắt đầu ở đây)
- [TEAM.md](docs/TEAM.md) — mở rộng team (sau này)
- [ADD-PROJECT.md](docs/ADD-PROJECT.md) — thêm repo
- [ROADMAP.md](docs/ROADMAP.md) — giai đoạn 1 / 2
- [architecture.md](docs/architecture.md)
- [mcp-tools.md](docs/mcp-tools.md)
- [retrieval-flow.md](docs/retrieval-flow.md)
