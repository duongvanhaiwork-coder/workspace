# Workflow quickstart — Question-scope + Superpowers (tiếng Việt)

Hướng dẫn ngắn khi làm task trong Cursor/Kiro với skills/rules của repo này.

| Tài liệu | Ngôn ngữ | Đối tượng |
| -------- | -------- | --------- |
| [rules/QUICKSTART.md](../rules/QUICKSTART.md) | English | Rules + prompt ngắn |
| [skills/question-scope/README.md](../skills/question-scope/README.md) | Tiếng Việt | Prompt copy-paste (`question-scope` → `README.md`) |
| Skill **`question-scope`** (`skills/question-scope/SKILL.md`) | English | Contract agent L1–L4 (invoke-skill) |
| [rules/cursor/workflow.mdc](../rules/cursor/workflow.mdc) | English | Rule ID Superpowers (`@workflow`) |
| [AGENTS.md](../AGENTS.md) | English | Chính sách agent workspace |

## Sync (một lần / sau khi sửa skills hoặc rules)

```bash
cd /path/to/Workspace
make sync-ide
```

Symlink **chỉ** thư mục home (mọi project trên máy):

- `~/.cursor/rules` → `rules/cursor/`
- `~/.kiro/steering` → `rules/kiro/`
- `~/.cursor/skills`, `~/.kiro/skills` → `skills/`

Không symlink vào `Workspace/.cursor/` hay `Workspace/.kiro/`. `make link-global` = `make sync-ide`.

## Hai lớp (nhớ một câu)

| Lớp | Trả lời | Nguồn |
| --- | ------- | ----- |
| **Question-scope** | Làm **đến mức nào** (L1–L4), `docs/work/…`, gates | Rule `question-scope` + skill |
| **Superpowers supplement** | Làm **đúng chất lượng** (TDD, verify, plan, worktree…) | `@workflow` + skills |

**Mặc định:** L3/L4 → bật supplement. L2 → TDD + verify tối thiểu. L1 → không full Superpowers flow.

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

Thêm ví dụ dài: [skills/question-scope/README.md](../skills/question-scope/README.md).

## Token opt-out

| Token | Question-scope | Superpowers supplement |
| ----- | ---------------- | ---------------------- |
| `qs:off`, `no-scope` | Tắt | Tắt |
| `quick:` | Tắt (fast path) | Tắt |
| `qs:meta` / `audit:` | Tắt (audit/review) | Tắt |
| `sp:off`, `no-sp` | Bật | Tắt |
| `/question-scope Lx` | Bật, bỏ bước chọn 4 option | Theo level |

**Lưu ý:** `level Lx` và `?` **không** bật scope. Lệnh `/question-scope` chỉ ở **đầu hoặc cuối** tin nhắn (không giữa câu). Level cần **space**: `/question-scope L2` (không `/question-scopeL2`; nếu dính `L` agent nhắc `Detected /question-scopeL2 — use /question-scope L2`). Review/audit: `qs:meta — …` hoặc `audit: — …` (khuyến nghị). `quick:` **không** phải “L3 nhưng bỏ design” — dùng `/question-scope L3` + `sp:off`; **không** phải “L2 + rollup MD” — dùng `/question-scope L2` + “Rollup MD OK.”. Sau sửa contract trong repo AI Core: `make verify` (đủ cho hầu hết PR); spot-check 2–3 chat chỉ khi đổi trigger/meta (xem `behavioral-gates.md`); rồi `make sync-ide` + reload window/chat. Sau sync **không có** `scripts/` — chỉ rules + skills trong `~/.cursor/`.

## Tài liệu trên disk (repo đang sửa)

| Nội dung | Đường dẫn |
| -------- | --------- |
| STATUS, phase, blocker | `docs/work/YYYY-MM-DD-<slug>/` (L2–L4) |
| Spec design (tuỳ chọn) | `docs/specs/…` — link từ phase file |
| Plan task (tuỳ chọn) | `docs/plans/…` — link từ work folder |

Một nguồn sự thật — xem [skills/CONVENTIONS.md](../skills/CONVENTIONS.md).

## Luồng L3 điển hình

```text
/question-scope L3 → docs/work/ + STATUS
  → design-approval-gate (nếu lớn)
  → implementation-plan: architect-plan trong docs/work/ (B mặc định) HOẶC writing-plans → docs/plans/ (A)
  → isolated-workspace
  → execute-inline-checkpoints (B, mặc định) HOẶC execute-via-subagents (A, cần docs/plans/)
  → tdd-during-implementation
  → verify-before-done
  → finish-branch-options
```

## Bug (thường L2)

```text
/question-scope L2 — bug: <triệu chứng> (@files)
→ debug-root-cause-first → tdd-failing-repro → verify-fix-evidence
```

## Rule graph đầy đủ

Cursor: `@workflow` hoặc đọc `rules/cursor/workflow.mdc`.
