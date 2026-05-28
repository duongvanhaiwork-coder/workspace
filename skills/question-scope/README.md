# Question Scope — Cách dùng

> **Ngôn ngữ:** File này là **tiếng Việt** (ngoại lệ duy nhất trong `skills/`). Các skill khác dùng tiếng Anh. Contract cho agent: **[SKILL.md](./SKILL.md)** (English).

Hướng dẫn **người dùng** chọn level, token, prompt và tài liệu trên disk. Agent đọc contract đầy đủ trong **[SKILL.md](./SKILL.md)** (mục **[Contents](./SKILL.md#contents)** — mục lục nhanh); rule Cursor luôn bật: `rules/question-scope.mdc`.

**Liên quan:** [Rules QUICKSTART (EN)](../../rules/QUICKSTART.md) · [Superpowers](../superpowers/SKILL.md) · [STRUCTURE](../STRUCTURE.md) · [workflow.mdc](../rules/workflow.mdc)

---

## Ví dụ câu lệnh — copy dán vào chat

Bảng một dòng → khối đầy đủ bên dưới. Thay `<mô tả>`, `@path`, ngày/slug cho task của bạn.

### Tra cứu nhanh

| Tình huống | Dán vào chat |
| ---------- | ------------ |
| Sửa 1 dòng, không cần L1–L4 | `quick: <mô tả>` |
| Patch / bug vài file | `level L2 — <mô tả> (@file)` |
| Feature mới (API, module) | `level L3 — <mô tả>` |
| Migration / nhiều service | `level L4 — <mô tả>` |
| Chỉ hỏi, không sửa code | `level L1 — <câu hỏi>` |
| Chưa biết chọn L nào | `/question-scope` + mô tả task |
| Biết L, shortcut | `/question-scope L2` + mô tả |
| Tắt ceremony scope | `qs:off — <mô tả>` |
| Có L3/L4 nhưng không worktree/plan SP | `level L3 — <mô tả>. sp:off` |
| Tiếp session cũ | `@docs/work/.../STATUS.md` + `@.../l3-02-build-prove.md` + `tiếp tục level L3` |
| Hỏi bằng `?` (tight match) | `?fix <mô tả>` hoặc `fix <mô tả>?` |

---

### `quick:` — không scope, làm ngay

```text
quick: đổi "teh" thành "the" trong README.md
```

```text
quick: xóa import không dùng trong @src/utils/date.ts
```

```text
quick: thêm comment giải thích hàm parseDate (@src/utils/date.ts)
```

---

### `level L1` — chỉ trả lời

```text
level L1 — giải thích luồng login từ @src/auth/login.ts đến session cookie.
```

```text
level L1 — so sánh dùng Redis cache vs in-memory cho rate limit API.
```

```text
level L1 — gợi ý tên biến cho trạng thái đơn: pending, paid, cancelled (@src/orders/types.ts).
```

```text
?explain tại sao middleware auth chạy trước validator (@src/middleware/auth.ts)
```

---

### `level L2` — patch / bug

```text
level L2 — fix: API trả 400 khi thiếu field phone (@src/routes/user.ts).
```

```text
level L2 — bug: test UserService.create fails sau đổi schema (@tests/user.service.test.ts @src/services/user.ts).
```

```text
level L2 — thêm validation email RFC trên POST /register (@src/routes/register.ts).
```

```text
level L2 — refactor: tách hàm validateInput ra @src/validators/common.ts, giữ behavior (@src/routes/order.ts).
```

```text
/fix lỗi typo message lỗi 404 (@src/i18n/en.json)
```

```text
/question-scope L2 — đổi default page size từ 20 → 50 trên GET /products (@src/routes/products.ts).
```

```text
/question-scope L2 — thêm unit test cho hàm calculateTax (@src/tax.ts @tests/tax.test.ts).
```

---

### `level L3` — feature bounded

```text
level L3 — thêm endpoint GET /orders/export trả CSV, filter theo ngày và status.

AC: auth bắt buộc; max 10k dòng; Content-Type text/csv.
docs/work/2026-05-22-order-export/ + STATUS + l3 phases.
Superpowers: worktree, TDD, verify.
```

```text
level L3 — worker gửi email nhắc thanh toán sau 24h, idempotent theo orderId.

sp:off — plan trong l3-01-define, không writing-plans/worktree.
```

```text
level L3 — module mới `notifications/` với interface push + email stub.

Repo: projects/my-app/. Test trước code.
```

```text
?implement API health check /healthz trả JSON { status, version } (@src/app.ts)
```

---

### `level L4` — hệ thống lớn

```text
level L4 — migration auth từ session cookie sang OIDC (3 service: api, worker, admin).

Backward compatible 2 tuần; rollout + rollback trong docs/work/.
Superpowers: design gate, writing-plans, TDD, verify, finish-branch.
```

```text
level L4 — thêm MCP indexing cho monorepo: chunking, embedding cache, observability.

Phased docs/work/2026-05-22-mcp-indexing/.
```

---

### `/question-scope` — agent gợi ý L1–L4

**Bước 1 — gửi:**

```text
/question-scope

Cần upload ảnh sản phẩm max 5MB, lưu S3, trả URL public có TTL 7 ngày.
```

**Bước 2 — sau khi agent đưa 4 option, trả một trong:**

```text
L3
```

```text
level L3 — tiếp tục upload ảnh S3 như mô tả trên.
```

---

### `qs:off` / `no-scope` — không chạy scope

```text
qs:off — review diff PR #42, tập trung security và SQL injection.
```

```text
no-scope — viết commit message ngắn cho thay đổi staged (Conventional Commits).
```

---

### `sp:off` — vẫn Lx, tắt Superpowers supplement

```text
level L3 — CRUD tag cho sản phẩm. sp:off — chỉ architect-plan trong docs/work/, không worktree.
```

```text
level L2 — fix null pointer khi cart rỗng. sp:off
```

---

### Tiếp session (đã có `docs/work/`)

```text
@projects/my-app/docs/work/2026-05-22-order-export/STATUS.md
@projects/my-app/docs/work/2026-05-22-order-export/l3-02-build-prove.md

level L3 — tiếp tục từ phase Build, chạy test regression phần export.
```

```text
@docs/work/2026-05-22-fix-login/STATUS.md

level L2 — tiếp patch, blocker: thiếu env AUTH_SECRET trong local.
```

---

### Meta — sửa skills/rules trong AI Core Workspace

```text
level L2 — cập nhật mô tả trigger trong @skills/question-scope/SKILL.md cho tight match.

docs/work/2026-05-22-qs-trigger-doc/ (Workspace repo).
```

```text
quick: sửa typo trong skills/question-scope/README.md
```

---

### Sau khi agent hỏi level (chỉ một từ)

```text
L1
```

```text
L2
```

```text
choose L3
```

```text
level L4
```

---

## Một câu nhớ

| Lớp | Trả lời |
| --- | ------- |
| **Question-scope** | Làm **đến mức nào** (L1–L4), gates, `docs/work/…` |
| **Superpowers supplement** | Làm **đúng chất lượng** (TDD, verify, worktree, plan…) — mặc định L3/L4, tối thiểu L2 |

Hai lớc **không thay nhau**. Scope chọn “bao nhiêu”; Superpowers (khi bật) chọn “làm bước đó thế nào”.

---

## Chọn level (L1–L4)

| Level | Dùng khi | Sửa code? | Pipeline (tóm tắt) |
| ----- | -------- | --------- | ------------------- |
| **L1** | Giải thích, so sánh, đặt tên; không patch | Không | Context nhẹ → Answer |
| **L2** | Patch nhỏ, vài file, AC rõ | Có | Context → Spec → Patch → Verify → Review → MD |
| **L3** | Feature bounded (module, API, worker) | Có | Context → Spec → Plan → Test → Code → Verify → **Regression** → Review → Ship → MD |
| **L4** | Multi-service, migration lớn, AI platform | Có | **15 bước** Full Flow + Architecture / AI / Delivery |

**Gợi ý nhanh (không khóa):** chỉ hỏi → L1 · vài file / bug → L2 · feature mới có contract → L3 · hệ thống / nhiều service → L4.

### Ranh giới level (heuristic — bạn có thể override)

Agent có thể gợi ý L3 cho “endpoint mới một file”; nếu muốn **nhẹ hơn** (ít phase, không bắt regression đầy đủ), ghi rõ **`level L2`**.

| Tình huống | Level thường gặp | Chọn nhẹ hơn |
| ---------- | ----------------- | ------------- |
| Chỉ giải thích / so sánh | **L1** | — |
| Sửa hoặc mở rộng code **đã có**, vài file | **L2** | `level L2` cả khi chỉ thêm 1 endpoint nếu không cần ceremony L3 |
| Module mới, API contract, worker, nhiều file | **L3** | — |
| Nhiều service, platform, migration lớn | **L4** | — |

**L3 vs L4 — bước Validate:**

- **L3 (bounded):** Không có phase Validate riêng — giả định / rủi ro ghi trong **`l3-01-define.md`** (Spec + assumptions). Phase **`l3-02-build-prove`**: **Regression bắt buộc** (không “if needed”).
- **L4:** Có **Validate** formal trong **`l4-01-discover.md`** (go/no-go, risks) trước khi design nặng — hợp lý cho scope lớn.

Contract đầy đủ (English): [SKILL.md § Level boundaries](./SKILL.md).

---

## Bật / tắt chế độ (token)

| Token | Question-scope | Superpowers supplement | Khi nào dùng |
| ----- | ---------------- | ---------------------- | ------------ |
| *(mặc định)* | Bật nếu trigger khớp | L3/L4 bật; L2 tối thiểu | Task dev bình thường |
| `level L1` … `level L4` | Bật, **bỏ** bước chọn 4 option | Theo level | Biết rõ độ lớn — **nên dùng thường xuyên** |
| `/question-scope` | Idea → gợi ý → **4 option** → agent **dừng** chờ bạn chọn | Chưa chạy feature flow cho đến khi có L | Chưa chắc L1–L4 |
| `/question-scope L2` | Giống `level L2` | Theo L2 | Shortcut |
| `qs:off` / `no-scope` | **Tắt** | Tắt | Không muốn ceremony scope |
| `quick:` | **Tắt** (fast path) | Tắt | Một dòng: typo, comment, đổi nhỏ |
| `sp:off` / `no-sp` | **Vẫn bật** L1–L4 | **Tắt** | Muốn scope + `docs/work/` nhưng không worktree / writing-plans |
| `?` + từ khóa dev | Giống `/question-scope` nếu **tight match** | Sau khi chọn L | Xem mục trigger bên dưới |

**Lưu ý:**

- `quick:` **không** phải “L3 nhưng bỏ design” → dùng `level L3` + `sp:off`.
- `?` một mình (`ok?`, `xong?`) → **không** kích hoạt scope.

---

## Khi nào skill tự chạy?

| Cách | Hành vi |
| ---- | ------- |
| `level Lx` / `/question-scope Lx` | Chạy pipeline Lx ngay |
| `/question-scope` (không level) | Idea → 4 option → **STOP** (chưa code) |
| `?fix …` hoặc `fix …?` (tight match) | Giống `/question-scope` |
| Câu dài, chỉ `?` ở cuối | **Không** kích hoạt — dùng `/question-scope` hoặc `level Lx` |

**Tight match:** Sau trim, có `?` + từ khóa dev (**fix**, **add**, **api**, **bug**, **test**, …) **và**:

- ký tự đầu là `?`, **hoặc**
- token chữ/số đầu tiên là từ khóa dev.

**Ví dụ không kích hoạt:** `Em đã sửa handler rồi, giờ deploy được chưa?`

---

## Superpowers supplement theo level

Áp dụng **sau khi** đã có `level Lx` (hoặc đã chọn L1–L4). Chi tiết rule ID: [workflow.mdc](../../rules/workflow.mdc).

| Level | Supplement (mặc định) | Không bật mặc định |
| ----- | --------------------- | ------------------ |
| **L1** | Không (có thể `explain-code`) | design gate, worktree, full plan |
| **L2** | TDD + verify khi đổi behavior | design gate, `writing-plans`, worktree |
| **L3** | worktree, TDD, execute **inline (B)**, verify, finish-branch | subagents (A) trừ khi có `docs/plans/…` |
| **L4** | Gần full: design gate, plan, TDD, verify, review | — |

**Execute hai nhánh (chỉ một):**

- **B (mặc định L3):** `executing-plans` — plan trong `docs/work/…` (architect-plan).
- **A:** `subagent-driven-development` — **cần** `docs/plans/YYYY-MM-DD-<feature>.md` từ `writing-plans`.

Tắt supplement: thêm `sp:off` hoặc `no-sp` vào prompt.

**Agent:** Khi scope đang **chờ chọn L**, không chạy brainstorming / writing-plans / worktree — xem [superpowers/SKILL.md § With question-scope](../superpowers/SKILL.md).

---

## Tài liệu trên disk

**`<target-repo>`** = repo bạn đang sửa (ví dụ `projects/my-app/`), không phải `Workspace/` trừ meta AI Core.

### Một nguồn sự thật (tránh lệch file)

| Mức | Đặt ở đâu |
| --- | --------- |
| L2, L3 nhỏ | AC + plan trong **`docs/work/YYYY-MM-DD-<slug>/`** |
| L3 lớn / L4 | Có thể thêm `docs/specs/…`, `docs/plans/…` — phase file **chỉ link**, không copy AC đầy đủ hai chỗ |

### Cấu trúc theo level

```text
docs/work/2026-05-22-my-feature/
  STATUS.md              ← đọc đầu session mới (@STATUS.md)
  l2-patch.md            ← L2
  l3-01-define.md        ← L3
  l3-02-build-prove.md
  l3-03-ship.md
  l4-00-frame.md …       ← L4
```

Template: [templates/phases/](./templates/phases/) · L1 tùy chọn: `docs/answers/…`

**Session mới:** `@docs/work/.../STATUS.md` + file phase hiện tại — không chỉ dựa chat cũ.

---

## Luồng từng level (checklist người dùng)

### L1

1. Gửi `level L1` + câu hỏi (có `@file` nếu cần, tối đa 1–2 file).
2. Nhận trả lời trong chat.
3. (Tùy chọn) lưu `docs/answers/YYYY-MM-DD-<slug>.md`.

### L2

1. `level L2` + mô tả + `@file`.
2. Agent: Spec (AC; bug → root cause trước).
3. Patch → chạy test vùng ảnh hưởng → review.
4. Cập nhật `docs/work/…` (patch nhỏ có thể một file rollup).

### L3

1. `level L3` + AC mong muốn.
2. `docs/work/…` + define (plan) → **test cases trước code**.
3. Code → verify → **regression** → ship (rollout/rollback).
4. Cập nhật `STATUS.md` mỗi phase.

### L4

1. `level L4` — coi bước Idea/Scope đã xong.
2. Discover → Define → Build (test design trước implement) → Prove → Ship.
3. `l4-05-ship.md`: Architecture / AI / Delivery khi áp dụng.

---

## Bug (thường L2)

Thứ tự trong pipeline:

1. Ghi **root cause** (Spec hoặc `STATUS.md`) — chưa sửa lung tung.
2. Test fail reproduce (nếu đổi behavior).
3. Fix → verify có log/output.

Prompt:

```text
level L2 — bug: submit form trả 500 khi email trùng (@api/register.ts).
```

Thêm ví dụ copy-paste: mục **[Ví dụ câu lệnh — copy dán vào chat](#ví-dụ-câu-lệnh--copy-dán-vào-chat)** ở đầu file.

---

## Cây quyết định nhanh

```text
Chỉ hỏi, không sửa code?
  └─ level L1

Sửa ≤ vài file, AC rõ?
  └─ level L2  (+ quick: nếu cực nhỏ và không cần docs/work)

Feature mới / API / module bounded?
  └─ level L3  (+ sp:off nếu không muốn worktree/plan SP)

Multi-service / migration / platform?
  └─ level L4

Muốn agent gợi ý L1–L4?
  └─ /question-scope  → chọn L → tiếp tục

Không muốn ceremony?
  └─ quick: …  hoặc  qs:off …
```

---

## Đồng bộ IDE (sau khi sửa skill)

```bash
./scripts/sync-ide.sh    # hoặc: make sync-ide
```

---

## File trong thư mục này

| File | Ai đọc |
| ---- | ------ |
| **README.md** (file này) | Người — cách dùng, prompt mẫu |
| **SKILL.md** | Agent — contract, gates, pipeline đầy đủ |
| **templates/phases/** | Agent copy khi tạo `docs/work/…` (chuẩn layout: [STRUCTURE.md](../STRUCTURE.md)) |

**Canonical:** Nếu README và SKILL.md lệch nhau, ưu tiên **SKILL.md**.
