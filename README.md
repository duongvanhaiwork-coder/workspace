# AI Core — Skills & rules

Canonical **agent skills** (`skills/`) and **IDE rules** (`rules/cursor/`) for Cursor and Kiro. Use them in any repo via global symlink sync.

**Agent policy:** [AGENTS.md](AGENTS.md) · **Workflow (Vietnamese):** [docs/WORKFLOW-QUICKSTART.md](docs/WORKFLOW-QUICKSTART.md) · **Rules quickstart (English):** [rules/QUICKSTART.md](rules/QUICKSTART.md)

## Bắt đầu nhanh

```bash
cd /path/to/Workspace
./scripts/sync-ide.sh    # symlink skills + rules → ~/.cursor/, ~/.kiro/
```

Reload cửa sổ Cursor hoặc mở chat mới sau khi sửa rule always-on.

## Thành phần

| Thành phần | Vai trò |
| ---------- | ------- |
| `skills/` | Agent playbooks (`SKILL.md` per skill) — nguồn chính |
| `rules/cursor/` | Cursor rules `.mdc` — nguồn chính (sửa tại đây) |
| `rules/kiro/` | Kiro steering — **tự sinh** từ `rules/cursor/` (không sửa tay) |
| `scripts/` | Sync IDE + verify contract (không cài vào `~/.cursor/`) |
| `AGENTS.md` | Chính sách agent workspace |
| `docs/` | Hướng dẫn người (VD: WORKFLOW-QUICKSTART) |

**Always-on rules (mọi session):** `code-standards`, `mcp-intelligence`, `question-scope`. Stack rules (`typescript`, `react`, …) theo loại file. Workflow graph: `@workflow` (on demand).

**MCP intelligence:** Khi AI Core MCP (`ai-core`) kết nối, dùng `get_context` / `search_code` / `analyze_impact` trước grep; khi không có MCP → editor fallback (`rules/cursor/mcp-intelligence.mdc`). Opt-out: `mcp:off`, `no-mcp`.

## Lệnh chạy (nguồn duy nhất)

**Chính sách:** Mọi lệnh `./scripts/…` cho repo này **chỉ ghi ở README này**. `skills/` và `rules/` mô tả hành vi agent — **không** lặp lệnh; chỉ trỏ về mục này khi cần vận hành repo.

Chạy từ thư mục gốc `Workspace/`:

| Lệnh | Làm gì |
| ---- | ------ |
| `./scripts/sync-ide.sh` | Sinh `rules/kiro/` + symlink `~/.cursor/rules`, `~/.kiro/steering`, skills |
| `./scripts/link-global-ide.sh` | Alias của `sync-ide.sh` (tùy chọn `IDE_GLOBAL_ROOT=…`) |
| `./scripts/sync-ide-skills.sh` | Chỉ symlink skills |
| `./scripts/sync-ide-rules.sh` | Chỉ sinh kiro + symlink rules |
| `./scripts/verify.sh` | Kiểm tra skills, rules, question-scope contract |

### `./scripts/verify.sh`

Gọi lần lượt:

| Script | Kiểm tra |
| ------ | -------- |
| `scripts/verify-skills-structure.sh` | Cấu trúc `skills/`, YAML `SKILL.md` |
| `scripts/verify-skills-audit.sh` | Invocation modes, links, anti-patterns |
| `scripts/verify-question-scope-triggers.sh` | Parser fixtures, rule ↔ SKILL mirror |
| `scripts/verify-question-scope-behavior.sh` | Behavioral anchors trong SKILL + templates |
| `scripts/hint-question-scope-behavioral-eval.sh` | Gợi ý spot-check (không fail) |

**Khi chạy:** Trước merge/PR sửa `skills/` hoặc `rules/`; sau đổi question-scope triggers/tokens/parsing.

### Script tùy chọn (question-scope)

| Script | Khi dùng |
| ------ | -------- |
| `./scripts/check-question-scope-session.sh` | Sau sync — so `~/.cursor/rules/question-scope.mdc` vs repo |
| `./scripts/run-question-scope-behavioral-eval.sh` | In checklist spot-check LLM (không bắt buộc merge) |

## Đồng bộ skills & rules vào IDE

**Nguồn chính:** `skills/` và `rules/cursor/*.mdc`. Cursor/Kiro đọc bản cài qua symlink dưới home — **không** tự cập nhật khi chỉ sửa file trong repo.

| Thay đổi | Cần `./scripts/sync-ide.sh`? |
| -------- | ------------------------------ |
| Sửa `skills/**` | Có |
| Sửa `rules/cursor/*.mdc` | Có — sinh lại `rules/kiro/` + symlink |
| Chỉ sửa `docs/`, `AGENTS.md` | Không (trừ khi đổi contract cần `verify`) |

**Sau khi sync:**

1. **Reload cửa sổ Cursor** hoặc **chat mới** — rule cache trong chat cũ có thể lỗi thời.
2. Chỉ **rules + skills** vào `~/.cursor/` — **không** có `scripts/`; chạy `verify` trong repo gốc.
3. Symlink **chỉ** home: `~/.cursor/rules` → `rules/cursor/`, `~/.kiro/steering` → `rules/kiro/`, skills → `skills/`. **Không** symlink vào `Workspace/.cursor/` hay `Workspace/.kiro/`.

Chi tiết từng script: mục [Lệnh chạy](#lệnh-chạy-nguồn-duy-nhất) và `scripts/sync-ide.sh`.

## Scripts (`scripts/`)

| File | Làm gì |
| ---- | ------ |
| `sync-ide.sh` | Entry: sync skills + rules |
| `sync-ide-skills.sh` | Symlink `~/.cursor/skills`, `~/.kiro/skills` |
| `sync-ide-rules.sh` | `cursor/*.mdc` → `kiro/*.md` + symlink steering |
| `link-global-ide.sh` | Alias `sync-ide.sh` |
| `verify.sh` | Entry: toàn bộ verify contract |
| `verify-*.sh` | Từng bước verify (gọi từ `verify.sh`) |
| `check-question-scope-session.sh` | So rule đã sync vs repo |
| `run-question-scope-behavioral-eval.sh` | Checklist spot-check thủ công |
| `lib/question-scope-contract.sh` | Shared helpers cho verify |

## Docs

| File | Nội dung |
| ---- | -------- |
| [docs/WORKFLOW-QUICKSTART.md](docs/WORKFLOW-QUICKSTART.md) | Question-scope + Superpowers (tiếng Việt) |
| [rules/QUICKSTART.md](rules/QUICKSTART.md) | Cùng workflow (English) |
| [rules/CONVENTIONS.md](rules/CONVENTIONS.md) | Rule authoring, polarity |
| [skills/CONVENTIONS.md](skills/CONVENTIONS.md) | Skill authoring, composition |
| [skills/STRUCTURE.md](skills/STRUCTURE.md) | Layout thư mục skill |
| [STRUCTOR.md](STRUCTOR.md) | Cây repo tóm tắt |
