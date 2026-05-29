# Workflow quickstart — Question-scope + Superpowers (tiếng Việt)

Hướng dẫn ngắn khi làm task trong Cursor/Kiro với skills/rules của repo này.

| Tài liệu | Ngôn ngữ | Đối tượng |
| -------- | -------- | --------- |
| [rules/QUICKSTART.md](../rules/QUICKSTART.md) | English | Rules + prompt ngắn (cùng logic L3/L2) |
| [skills/question-scope/README.md](../skills/question-scope/README.md) | Tiếng Việt | Prompt copy-paste |
| Skill **`question-scope`** (`skills/question-scope/SKILL.md`) | English | Contract agent L1–L4 |
| [rules/cursor/workflow.mdc](../rules/cursor/workflow.mdc) | English | Rule ID Superpowers (`@workflow`) |
| [AGENTS.md](../AGENTS.md) | English | Chính sách agent workspace |

## Sync (một lần / sau khi sửa skills hoặc rules)

Lệnh chạy **chỉ** trong [README.md](../README.md) § *Lệnh chạy*:

- `./scripts/sync-ide.sh` — symlink skills + rules → `~/.cursor/`, `~/.kiro/`
- `./scripts/link-global-ide.sh` — alias cùng lệnh trên

Symlink **chỉ** thư mục home (mọi project trên máy):

- `~/.cursor/rules` → `rules/cursor/`
- `~/.kiro/steering` → `rules/kiro/`
- `~/.cursor/skills`, `~/.kiro/skills` → `skills/`

Không symlink vào `Workspace/.cursor/` hay `Workspace/.kiro/`.

## Hai lớp (nhớ một câu)

| Lớp | Trả lời | Nguồn |
| --- | ------- | ----- |
| **Question-scope** | Làm **đến mức nào** (L1–L4), `docs/work/…`, gates | Rule `question-scope` + skill |
| **Superpowers supplement** | Làm **đúng chất lượng** (TDD, verify, plan, worktree…) | `@workflow` + skills |

**Mặc định:** L3/L4 → bật supplement. L2 → TDD + verify tối thiểu. L1 → không full Superpowers flow.

**MCP discovery:** Rule `mcp-intelligence` (always-on) — MCP up → `get_context` / `search_code` / `analyze_impact`; MCP down → editor fallback. Opt-out: `mcp:off`, `no-mcp`.

## Chọn level

| Level | Khi nào |
| ----- | ------- |
| **L1** | Chỉ hỏi / giải thích, không sửa code |
| **L2** | Patch nhỏ, vài file, AC rõ |
| **L3** | Feature bounded (module, API, worker) |
| **L4** | Nhiều service, migration lớn, AI platform |

## Prompt mẫu (một dòng)

| Tình huống | Dán vào chat |
| ---------- | ------------ |
| Một dòng cực nhỏ | `quick: <mô tả>` |
| Patch / bug | `/question-scope L2 — <mô tả> (@file)` |
| Feature | `/question-scope L3 — <mô tả>` |
| Hệ thống lớn | `/question-scope L4 — <mô tả>` |
| Chưa chắc level | `/question-scope` + mô tả → chọn L1–L4 |
| Tắt ceremony scope | `qs:off — <mô tả>` |
| Có scope, không Superpowers | `/question-scope L3 — <task>. sp:off` |
| Có scope, không MCP discovery | thêm `mcp:off` hoặc `no-mcp` |

Thêm ví dụ dài: [skills/question-scope/README.md](../skills/question-scope/README.md).

## Token opt-out

| Token | Question-scope | Superpowers supplement |
| ----- | ---------------- | ---------------------- |
| `qs:off`, `no-scope` | Tắt | Tắt |
| `quick:` | Tắt (fast path) | Tắt |
| `qs:meta` / `audit:` | Tắt (audit/review) | Tắt |
| `sp:off`, `no-sp` | Bật | Tắt |
| `mcp:off`, `no-mcp` | Bật | — (editor fallback cho discovery) |
| `/question-scope Lx` | Bật, bỏ bước chọn 4 option | Theo level |

**Lưu ý:** `level Lx` và `?` **không** bật scope. Lệnh `/question-scope` chỉ ở **đầu hoặc cuối** tin nhắn. Level cần **space**: `/question-scope L2` (không `/question-scopeL2`). `quick:` **không** phải “L3 nhưng bỏ design” — dùng `/question-scope L3` + `sp:off`. Sau sửa contract trong repo này: `./scripts/verify.sh` (đủ cho hầu hết PR); spot-check 2–3 chat khi đổi trigger/meta (`behavioral-gates.md`); rồi `./scripts/sync-ide.sh` + reload window/chat.

## Tài liệu trên disk (repo đang sửa)

| Nội dung | Đường dẫn |
| -------- | --------- |
| STATUS, phase, blocker | `docs/work/YYYY-MM-DD-<slug>/` (L2–L4) |
| Spec design (tuỳ chọn) | `docs/specs/…` — link từ phase file |
| Plan task (tuỳ chọn) | `docs/plans/…` — link từ work folder |

Một nguồn sự thật — xem [skills/CONVENTIONS.md](../skills/CONVENTIONS.md).

## Luồng L3 điển hình (supplement bật)

Cùng logic với [rules/QUICKSTART.md](../rules/QUICKSTART.md):

```text
/question-scope L3 → docs/work/ + STATUS.md
  → brainstorming (nếu chưa có spec approve)
  → architect-plan (l3-01, B mặc định) | writing-plans → docs/plans/ (A)
  → generate-test (l3-02 TC table) — trước Code
  → using-git-worktrees
  → executing-plans (B) | subagent-driven-development (A)
  → test-driven-development (trong Code)
  → verification-before-completion
  → caveman-review → l3-03-ship → finishing-a-development-branch
```

## Bug (thường L2)

```text
/question-scope L2 — bug: <triệu chứng> (@files)
→ systematic-debugging → test-driven-development (repro)
→ verification-before-completion
```

## Rule graph đầy đủ

Cursor: `@workflow` hoặc đọc `rules/cursor/workflow.mdc`.
