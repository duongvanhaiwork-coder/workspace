# Question Scope — Cách dùng

> **Ngôn ngữ:** File này là **tiếng Việt** (ngoại lệ duy nhất trong `skills/`). Các skill khác dùng tiếng Anh. Contract cho agent: **[SKILL.md](./SKILL.md)** (English).

Hướng dẫn **người dùng** chọn level, token, prompt và tài liệu trên disk. Agent đọc contract trong **[SKILL.md](./SKILL.md)** + **[references/](./references/)** khi cần. Rules Cursor (không cần path file): luôn bật **`question-scope`**, **`code-standards`**; khi cần handoff Superpowers → gõ **`@workflow`**.

**Liên quan:** [AGENTS.md](../../AGENTS.md) · **`superpowers`** · [STRUCTURE](../STRUCTURE.md) · rule IDs: [superpowers-supplement.md](references/superpowers-supplement.md)

---

## Prompt mẫu (copy-paste)

Thay `<mô tả>`, `@path`, ngày/slug. Bản tiếng Anh (cùng nội dung): [examples/sample-prompts.md](examples/sample-prompts.md).

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
| L3/L4 nhưng không worktree/plan SP | `level L3 — <mô tả>. sp:off` |
| Tiếp session cũ | `@docs/work/.../STATUS.md` + file phase + `tiếp tục level L3` |
| Hỏi bằng `?` (tight match) | `?fix <mô tả>` hoặc `fix <mô tả>?` |

```text
quick: đổi "teh" thành "the" trong README.md
```

```text
level L2 — fix: API trả 400 khi thiếu field phone (@src/routes/user.ts).
```

```text
level L3 — thêm endpoint GET /orders/export trả CSV.

AC: auth bắt buộc; max 10k dòng. docs/work/2026-05-22-order-export/
```

```text
/question-scope

Cần upload ảnh sản phẩm max 5MB, lưu S3, URL public TTL 7 ngày.
```

```text
level L2 — bug: submit form trả 500 khi email trùng (@api/register.ts).
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

### L là gì?

**L** = **Level** (mức **phạm vi** công việc). **L1**–**L4** càng cao thì pipeline, test, và tài liệu `docs/work/` càng đầy đủ — **không** có nghĩa “đọc nhiều file ngay từ câu đầu”. Context mở **dần theo bước** (xem [Context dần (JIT)](#context-dần-jit--tóm-tắt) và [SKILL.md § Progressive context](./SKILL.md#progressive-context-jit)).

| Level | Dùng khi | Sửa code? | Pipeline (tóm tắt) |
| ----- | -------- | --------- | ------------------- |
| **L1** | Giải thích, so sánh, đặt tên; không patch | Không | Context nhẹ → Answer |
| **L2** | Patch nhỏ, vài file, AC rõ | Có | Context → Spec → Patch → Verify → Review → MD |
| **L3** | Feature bounded (module, API, worker) | Có | Context → Spec → Plan → Test → Code → Verify → **Regression** → Review → Ship → MD |
| **L4** | Multi-service, migration lớn, AI platform | Có | **15 bước** Full Flow + Architecture / AI / Delivery |

**Gợi ý nhanh (không khóa):** chỉ hỏi → L1 · vài file / bug → L2 · feature mới có contract → L3 · hệ thống / nhiều service → L4.

**Pipeline & playbook chi tiết:** [SKILL.md § Pipelines](./SKILL.md#pipelines-ui) · [references/playbooks.md](references/playbooks.md). **L4 đã có `level L4`:** bỏ bước Idea/Scope — bắt từ Context.

**Map file phase (L2–L4):**

| Level | File phase |
| ----- | ---------- |
| L2 | `STATUS.md` + `l2-patch.md` (hoặc rollup một file) |
| L3 | `l3-01-define` (Context+Spec+Plan) → `l3-02-build-prove` (Test→…→Iterate) → `l3-03-ship` |
| L4 | `l4-00-frame` … `l4-05-ship` (xem [templates/phases/README.md](./templates/phases/README.md)) |

### Context dần (JIT) — tóm tắt

| Thuật ngữ | Ý nghĩa |
| --------- | ------- |
| **Symptom** | Bạn **viết** mô tả lỗi/AC trong chat — **không** cần `@`. |
| **Path từ user** | File/folder bạn **`@`** hoặc gõ path trong câu. |

**Lượt đầu (gợi ý):** `level Lx` + symptom; L2 thêm **0–1** `@` file nghi ngờ. Agent **mở rộng** context sau **Spec** / plan / gate — không quét repo trước Spec (L2).

**Ví dụ L2:**

```text
level L2 — POST /register trả 400 khi thiếu phone.

@src/routes/register.ts
```

Chi tiết: [SKILL.md § Progressive context (JIT)](./SKILL.md#progressive-context-jit).

### Ranh giới level (heuristic — bạn có thể override)

Agent có thể gợi ý L3 cho “endpoint mới một file”; nếu muốn **nhẹ hơn** (ít phase, không bắt regression đầy đủ), ghi rõ **`level L2`**.

| Tình huống | Level thường gặp | Chọn nhẹ hơn |
| ---------- | ----------------- | ------------- |
| Chỉ giải thích / so sánh | **L1** | — |
| Sửa hoặc mở rộng code **đã có**, vài file | **L2** | `level L2` cả khi chỉ thêm 1 endpoint nếu không cần ceremony L3 |
| Module mới, API contract, worker, nhiều file | **L3** | — |
| Nhiều service, platform, migration lớn | **L4** | — |

Chi tiết gray zone: [references/gray-zones.md](references/gray-zones.md) · [SKILL.md § Level boundaries](./SKILL.md#level-boundaries-heuristic-user-may-override).

### Gray zone — chọn L khi ranh giới mơ

Agent **không** tự chọn level nặng hơn khi level nhẹ cũng hợp lý. Cursor: **AskQuestion** hai lựa chọn (L1/L2, L2/L3, hoặc L3/L4) rồi **dừng**.

| Cặp | Gợi ý nhanh |
| --- | ----------- |
| **L1 vs L2** | Chỉ giải thích → L1 · cần sửa code / AC → L2 |
| **L2 vs L3** | Endpoint cùng module, ≤ ~5 file → L2 · module/worker mới → L3 |
| **L3 vs L4** | Một repo/service → L3 · nhiều service + Validate formal → L4 |

**Prompt override:**

```text
level L2 — thêm POST /products/export CSV (cùng pattern GET /products). Ít ceremony.
```

```text
level L3 — module notifications/ (email + push stub), contract mới.
```

**Chi tiết bảng:** [references/gray-zones.md](references/gray-zones.md) · checklist: [`l2-patch.md`](templates/phases/l2/l2-patch.md), [`l3-01-define.md`](templates/phases/l3/l3-01-define.md).

---

## Bật / tắt & trigger

| Token / cách | Tóm tắt |
| ------------ | ------- |
| `level L1`…`L4` | Scope bật, **không** hỏi 4 option — **nên dùng** |
| `/question-scope` | Idea → gợi ý → **4 option** → **STOP** |
| `quick:` / `qs:off` / `no-scope` | **Tắt** scope (fast path hoặc chat thường) |
| `sp:off` / `no-sp` | Scope **bật**, Superpowers supplement **tắt** |
| `?` + từ khóa dev | Giống `/question-scope` nếu **tight match** (không phải `ok?` cuối câu) |

Bảng đầy đủ: [SKILL.md § When this skill applies](./SKILL.md#when-this-skill-applies).

---

## Superpowers supplement theo level

Áp dụng **sau khi** đã có `level Lx`. Tóm tắt: **L3/L4** bật đầy đủ (worktree, TDD, verify…); **L2** tối thiểu (TDD + verify khi đổi behavior); **L1** không. Tắt: `sp:off` / `no-sp`.

| Level | Mặc định |
| ----- | -------- |
| L1 | Không |
| L2 | TDD + verify |
| L3 | worktree, TDD, execute **inline (B)**, verify, ship |
| L4 | Gần full flow + design gate / plan khi scope lớn |

**Execute:** **B** (mặc định L3, plan trong `docs/work/`) hoặc **A** (subagents — **cần** `docs/plans/…` từ `writing-plans`). Chi tiết rule ID: [superpowers-supplement.md](references/superpowers-supplement.md) · load **`@workflow`** trong chat.

**Agent:** Khi scope **chờ chọn L**, không chạy `brainstorming` / `writing-plans` / `using-git-worktrees` — xem **`superpowers`**.

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

Thêm ví dụ: mục [Prompt mẫu](#prompt-mẫu-copy-paste) ở trên.

---

## Cây quyết định nhanh

Text: mục dưới **Một câu nhớ** + bảng L ở trên. Flowchart + IDE: [references/level-picker.md](references/level-picker.md).

---

## File trong thư mục này

| File | Ai đọc |
| ---- | ------ |
| **README.md** (file này) | Người — hướng dẫn ngắn, link chi tiết |
| **examples/sample-prompts.md** | Người / agent — prompt mẫu (English) |
| **SKILL.md** | Agent — contract, gates, pipeline (core) |
| **references/** | Agent — gray-zone, playbooks, supplement, Kiro, testing ([index](references/README.md)) |
| **templates/phases/** | Agent copy khi tạo `docs/work/…` ([STRUCTURE.md](../STRUCTURE.md)) |

**Canonical:** Nếu README và SKILL.md lệch nhau, ưu tiên **SKILL.md** và **references/** (tiếng Anh).
