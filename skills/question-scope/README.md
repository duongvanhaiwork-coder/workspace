# Question Scope — Cách dùng

> **Ngôn ngữ:** File này là **tiếng Việt** (ngoại lệ duy nhất trong `skills/`). Các skill khác dùng tiếng Anh. Contract cho agent: **[SKILL.md](./SKILL.md)** (English).

Hướng dẫn **người dùng** chọn level, token, prompt và tài liệu trên disk. Agent đọc contract trong **[SKILL.md](./SKILL.md)** + **[references/](./references/)** khi cần. Rules Cursor (không cần path file): luôn bật **`question-scope`**, **`code-standards`**; khi cần handoff Superpowers → gõ **`@workflow`**.

**Liên quan:** [AGENTS.md](../../AGENTS.md) · **`superpowers`** · [STRUCTURE](../STRUCTURE.md) · rule IDs: [superpowers-supplement.md](references/superpowers-supplement.md)

### Cây quyết định token (1 dòng)

```text
Cần làm gì? → Chỉ hỏi / không sửa repo → /question-scope L1
            → Sửa nhanh, không ceremony → quick: … hoặc qs:off — …
            → Review/audit skill hoặc rule → qs:meta — … hoặc audit: — …
            → Patch vài file → /question-scope L2 — …
            → Feature bounded + Regression/Ship → /question-scope L3 — …
            → Multi-service / platform → /question-scope L4 — …
            → Chưa chắc L → /question-scope + mô tả (agent hỏi 4L, STOP)
            → L3/L4 nhưng bỏ worktree/plan SP → /question-scope L3 — … sp:off
            (Không dùng level Lx hay ?fix — không bật skill.)
```

## Mục lục

- [Cây quyết định token](#cây-quyết-định-token-1-dòng)
- [Cách gọi — chỉ `/question-scope`](#cách-gọi--chỉ-question-scope)
- [Prompt mẫu (copy-paste)](#prompt-mẫu-copy-paste)
- [Preset & anti-pattern](#preset--anti-pattern)
- [Một câu nhớ](#một-câu-nhớ)
- [Chọn level (L1–L4)](#chọn-level-l1l4)
- [Chưa gửi L trên lệnh](#chưa-gửi-l-trên-lệnh--agent-bắt-chọn-1-trong-4l)
- [Bật / tắt & trigger](#bật--tắt--trigger)
- [Superpowers supplement theo level](#superpowers-supplement-theo-level)
- [Tài liệu trên disk](#tài-liệu-trên-disk)
- [Luồng từng level](#luồng-từng-level-checklist-người-dùng)
- [Bug (thường L2)](#bug-thường-l2)
- [Cây quyết định nhanh](#cây-quyết-định-nhanh)
- [File trong thư mục này](#file-trong-thư-mục-này)

---

## Cách gọi — chỉ `/question-scope`

Đây là **cách duy nhất** team khuyến nghị bật skill (không dùng tiền tố `level` trong prompt).

| Bạn muốn | Gõ |
| -------- | --- |
| Chưa chắc L1–L4 | `/question-scope` + mô tả task → agent hỏi **chọn 1 trong 4L** → dừng chờ bạn |
| Đã chắc level | `/question-scope L2` + mô tả (thay `L2` bằng L1/L3/L4) |
| Không muốn ceremony 4L | `quick: …` hoặc `qs:off — …` |
| Review/audit skill hoặc rule (không chạy L1–L4) | `qs:meta — …` hoặc `audit: — …` |
| L3/L4 nhưng bỏ supplement SP | `/question-scope L3 — … sp:off` |

**Không còn hỗ trợ:** `level L2 — …` và `?fix …` — **không** bật skill. Dùng `/question-scope` hoặc `/question-scope L2`.

**Định dạng level:** bắt buộc có **khoảng trắng** — `/question-scope L2` (đúng), không `/question-scopeL2` (sai → agent hỏi lại 4L).

**Vị trí lệnh:** `/question-scope` chỉ nhận ở **đầu** hoặc **cuối** tin nhắn (sau trim) — không nhận giữa câu. Ví dụ đúng: `/question-scope L2 — fix auth` hoặc `fix auth /question-scope L2`. Sai: `Please /question-scope fix auth`.

**Review / audit skill** (ví dụ đường dẫn `skills/question-scope`, “đừng dùng `/question-scope` cho task này”) — **không** bật pipeline; khuyến nghị `qs:meta — …` hoặc `audit: — …` (hoặc `qs:off` nếu muốn chắc chắn).

---

## Prompt mẫu (copy-paste)

Thay `<mô tả>`, `@path`, ngày/slug. Bản tiếng Anh (cùng nội dung): [examples/sample-prompts.md](examples/sample-prompts.md).

| Tình huống | Dán vào chat |
| ---------- | ------------ |
| Sửa 1 dòng, không cần L1–L4 | `quick: <mô tả>` |
| Patch / bug vài file | `/question-scope L2 — <mô tả> (@file)` |
| Feature mới (API, module) | `/question-scope L3 — <mô tả>` |
| Migration / nhiều service | `/question-scope L4 — <mô tả>` |
| Chỉ hỏi, không sửa code | `/question-scope L1 — <câu hỏi>` |
| Chưa biết chọn L nào | `/question-scope` + mô tả task |
| Tắt ceremony scope | `qs:off — <mô tả>` |
| L3/L4 nhưng không worktree/plan SP | `/question-scope L3 — <mô tả>. sp:off` |
| Tiếp session cũ | `@docs/work/.../STATUS.md` + `/question-scope L3 — tiếp tục` (lệnh **đầu** hoặc **cuối** dòng) |

```text
quick: đổi "teh" thành "the" trong README.md
```

```text
/question-scope L2 — fix: API trả 400 khi thiếu field phone (@src/routes/user.ts).
```

```text
/question-scope L3 — thêm endpoint GET /orders/export trả CSV.

AC: auth bắt buộc; max 10k dòng. docs/work/2026-05-22-order-export/
```

```text
/question-scope

Cần upload ảnh sản phẩm max 5MB, lưu S3, URL public TTL 7 ngày.
```

```text
/question-scope L2 — bug: submit form trả 500 khi email trùng (@api/register.ts).
```

---

## Preset & anti-pattern

Bản tiếng Anh: [examples/sample-prompts.md § Presets](examples/sample-prompts.md#presets). Contract agent (Regression): [SKILL.md § Pipelines](./SKILL.md#pipelines-ui).

### Preset (copy-paste)

| Preset | Khi nào | Dán vào chat |
| ------ | ------- | ------------ |
| **Fast** | Typo, 1 dòng, **tắt scope** (không L1–L4, không `docs/work/`) | `quick: <mô tả>` |
| **Explain** | Chỉ hỏi, không sửa repo | `/question-scope L1 — <câu hỏi>` |
| **Patch** | Sửa/bug vài file, AC rõ | `/question-scope L2 — <mô tả> (@file)` |
| **Patch nhẹ** | L2 nhưng ít MD (một session, ≤ ~3 file) | `/question-scope L2 — <mô tả>. Rollup MD OK.` |
| **Feature** | Module/API/worker bounded + AC | `/question-scope L3 — <mô tả>` + AC; `docs/work/YYYY-MM-DD-<slug>/` |
| **Feature (ít SP)** | L3 nhưng không worktree/plan SP đầy đủ | `/question-scope L3 — <mô tả>. sp:off` |
| **System** | Multi-service, migration lớn | `/question-scope L4 — <mô tả>` |
| **Chọn L** | Chưa chắc L1–L4 — agent hỏi **4 option** (hoặc **2 option** nếu gray zone) | `/question-scope` + mô tả (lệnh **không** kèm L1–L4) |
| **Tiếp session** | Đang làm dở | `@docs/work/.../STATUS.md` + `/question-scope L3 — tiếp tục` |
| **Ý tưởng mơ hồ** | Chưa có problem statement / AC | `/question-scope` + mô tả rồi agent có thể chạy **orchestra-decision** trước khi hỏi 4L |

**Chỉ dùng `/question-scope`** — `?fix …` **không** bật skill.

### Ý tưởng mơ hồ (orchestra-decision)

Khi chưa có problem statement hoặc AC, agent có thể chạy skill **`orchestra-decision`** trước khi hỏi L1–L4:

```text
/question-scope

Cần upload ảnh sản phẩm — chưa rõ lưu S3 hay local, chưa có giới hạn dung lượng.
```

Sau khi có 2–4 dòng problem + outcome, agent quay lại **Suggest** + chọn L (thường L2 vs L3 hoặc 4L).

### Anti-pattern (tránh)

| Sai | Hậu quả | Làm đúng |
| --- | -------- | -------- |
| `level L2 — …` (không có `/question-scope`) | Scope **không** bật | `/question-scope L2 — …` |
| Câu dài không có `/question-scope` | Scope **không** bật | `/question-scope` hoặc `/question-scope L2 — …` |
| `/question-scope L2` + `quick:` cùng câu | Opt-out thắng — **không** chạy scope | Chỉ một: `quick:` **hoặc** `/question-scope L2` |
| `quick:` nhưng muốn L2 + rollup MD nhẹ | Scope **tắt** — không có STATUS/rollup | `/question-scope L2 — <mô tả>. Rollup MD OK.` (preset **Patch nhẹ**) |
| Chỉ `sp:off` không có `/question-scope` | Scope **không** tự bật | `/question-scope L3 — … sp:off` |
| `/question-scopeL2` (không space trước L) | Không preset L2 — agent hỏi 4L | `/question-scope L2 — …` |
| Audit/review skill, path `skills/question-scope` | Scope **không** bật (meta) | `qs:meta — …` hoặc `audit: — …` (hoặc `qs:off — …`) |
| Patch lớn nhưng kẹt L2 (module mới, >5 file) | Thiếu test/regression/ship | Escalate L3 hoặc gửi `/question-scope L3` |
| L3 nhưng không ghi AC / slug `docs/work/` | Agent đoán scope | AC 3–5 bullet + folder slug trong prompt |

### Checklist L2 ↔ L3 (5 câu)

Dùng khi **không chắc** patch hay feature. **Một câu “có” → nghiêng L3** (hoặc chọn L2 với `Ít ceremony` nếu cố ý nhẹ).

| # | Câu hỏi |
| - | ------- |
| 1 | Có **module/package/thư mục** top-level **mới**? |
| 2 | Có **worker / queue / cron / pipeline async** mới? |
| 3 | Dự kiến **> ~5 file** hoặc **nhiều session / nhiều PR**? |
| 4 | Có **nhiều endpoint**, tài liệu contract public, hoặc **versioning** API? |
| 5 | Cần **Regression + Ship** đầy đủ (không chỉ test vùng patch)? |

**Cả 5 đều “không”** → **`/question-scope L2`** hợp lý. Agent: [gray-zones.md § Quick checklist](references/gray-zones.md#quick-checklist-l2-vs-l3) · template [`l2-patch.md`](templates/phases/l2/l2-patch.md).

```text
/question-scope L2 — thêm POST /products/export CSV (cùng pattern GET /products). Ít ceremony.
```

```text
/question-scope L3 — module notifications/ (email + push stub), contract mới.
```

### Regression (L3/L4)

| Level | Mặc định chạy gì | Không bắt buộc (trừ khi AC yêu cầu) |
| ----- | ---------------- | ------------------------------------- |
| **L2** | **Verify** — test/smoke vùng patch + callers 1-hop | Cả suite repo / monorepo |
| **L3** | Test **module/package** đụng tới + integration **1-hop** gọi API/surface đổi; ghi lệnh trong `l3-02-build-prove.md` | Toàn bộ monorepo |
| **L4** | Test theo **service bị ảnh hưởng** (plan/validate); slice CI OK nếu ghi trong phase MD | “Chạy hết mọi thứ” không tên trong plan |

**L2 patch rủi ro cao** (shared lib, auth): vẫn L2 nhưng nhờ agent chạy suite rộng hơn trong Verify, hoặc chuyển **`/question-scope L3`** nếu cần Regression gate chính thức.

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

**Pipeline & playbook chi tiết:** [SKILL.md § Pipelines](./SKILL.md#pipelines-ui) · [references/playbooks.md](references/playbooks.md). **L4 đã có `/question-scope L4`:** bỏ bước Idea/Scope — bắt từ Context.

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

**Lượt đầu (gợi ý):** `/question-scope Lx` + symptom; L2 thêm **0–1** `@` file nghi ngờ. Agent **mở rộng** context sau **Spec** / plan / gate — không quét repo trước Spec (L2).

**Ví dụ L2:**

```text
/question-scope L2 — POST /register trả 400 khi thiếu phone.

@src/routes/register.ts
```

Chi tiết: [SKILL.md § Progressive context (JIT)](./SKILL.md#progressive-context-jit).

### Ranh giới level (heuristic — bạn có thể override)

Agent có thể gợi ý L3 cho “endpoint mới một file”; nếu muốn **nhẹ hơn** (ít phase, không bắt regression đầy đủ), ghi rõ **`/question-scope L2`**.

| Tình huống | Level thường gặp | Chọn nhẹ hơn |
| ---------- | ----------------- | ------------- |
| Chỉ giải thích / so sánh | **L1** | — |
| Sửa hoặc mở rộng code **đã có**, vài file | **L2** | `/question-scope L2` cả khi chỉ thêm 1 endpoint nếu không cần ceremony L3 |
| Module mới, API contract, worker, nhiều file | **L3** | — |
| Nhiều service, platform, migration lớn | **L4** | — |

Chi tiết gray zone: [references/gray-zones.md](references/gray-zones.md) · [SKILL.md § Level boundaries](./SKILL.md#level-boundaries-heuristic-user-may-override).

### Gray zone — chọn L khi ranh giới mơ

Agent **không** tự chọn level nặng hơn khi level nhẹ cũng hợp lý. Cursor: **AskQuestion** hai lựa chọn (L1/L2, L2/L3, hoặc L3/L4) rồi **dừng**.

| Cặp | Gợi ý nhanh |
| --- | ----------- |
| **L1 vs L2** | Chỉ giải thích → L1 · cần sửa code / AC → L2 |
| **L2 vs L3** | Dùng [Checklist L2 ↔ L3 (5 câu)](#checklist-l2--l3-5-câu) |
| **L3 vs L4** | [l3-vs-l4-diff.md](references/l3-vs-l4-diff.md) · một repo → L3 · multi-service + Validate → L4 |

**Chi tiết bảng:** [references/gray-zones.md](references/gray-zones.md) · checklist agent: [Quick checklist L2 vs L3](references/gray-zones.md#quick-checklist-l2-vs-l3).

---

## Chưa gửi L trên lệnh — agent bắt chọn 1 trong 4L

Khi bạn gõ **`/question-scope`** + mô tả mà lệnh **không** có `L1`…`L4` (tức không phải `/question-scope L2`):

1. Agent tóm **Idea** + **gợi ý** một L (không khóa).
2. Hiện **4 lựa chọn** — bạn **phải chọn một** (Cursor: `AskQuestion`; Kiro: list đánh số).
3. Agent **dừng** — chưa Spec / sửa code / `docs/work/` cho đến khi bạn trả lời `L2`, `chọn L3`, hoặc gửi lại `/question-scope L3 — …`
4. **Gray zone** (L1↔L2, L2↔L3, L3↔L4): chỉ **2 option** thay vì 4 — vẫn phải chọn trước khi làm tiếp.

| ID | Ý nghĩa |
| --- | ------- |
| **L1** | Chỉ trả lời / giải thích — không sửa repo |
| **L2** | Patch nhỏ — vài file |
| **L3** | Feature bounded — module, API, worker |
| **L4** | Hệ thống lớn — multi-service, migration |

**Bỏ qua bước chọn** nếu prompt đã có `/question-scope L2 — …` (hoặc L1/L3/L4) + mô tả.

```text
/question-scope

Cần API upload ảnh max 5MB, S3, URL TTL 7 ngày.
→ Agent: Idea + Suggest + 4 option → bạn trả lời L3 → mới bắt đầu pipeline L3
```

---

## Bật / tắt & trigger

| Token / cách | Tóm tắt |
| ------------ | ------- |
| `/question-scope L1`…`L4` | Scope bật, **không** hỏi 4 option — **cách chuẩn khi đã biết L** |
| `/question-scope` (không kèm L) | Idea → gợi ý → **chọn 1 trong 4L** → **STOP** |
| `quick:` / `qs:off` / `no-scope` | **Tắt** scope (fast path hoặc chat thường) |
| `qs:meta` / `audit:` | **Tắt** scope — audit/review skill hoặc rule (khuyến nghị khi rà soát) |
| `sp:off` / `no-sp` | Scope **bật** (khi đã có trigger), supplement **tắt** — không tự bật scope |
| `qs:off` + `/question-scope L2` cùng câu | **Opt-out thắng** — không chạy scope (xem SKILL § Conflicting tokens) |

Bảng đầy đủ: [SKILL.md § When this skill applies](./SKILL.md#when-this-skill-applies).

---

## Superpowers supplement theo level

Áp dụng **sau khi** đã có `/question-scope Lx`. Tóm tắt: **L3/L4** bật đầy đủ (worktree, TDD, verify…); **L2** tối thiểu (TDD + verify khi đổi behavior); **L1** không. Tắt: `sp:off` / `no-sp`.

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

1. Gửi `/question-scope L1` + câu hỏi (có `@file` nếu cần, tối đa 1–2 file).
2. Nhận trả lời trong chat.
3. (Tùy chọn) lưu `docs/answers/YYYY-MM-DD-<slug>.md`.

### L2

1. `/question-scope L2` + mô tả + `@file`.
2. Agent: Spec (AC; bug → root cause trước).
3. Patch → chạy test vùng ảnh hưởng → review.
4. Cập nhật `docs/work/…` (patch nhỏ có thể một file rollup).

### L3

1. `/question-scope L3` + AC mong muốn.
2. `docs/work/…` + define (plan) → **test cases trước code**.
3. Code → verify → **regression** → ship (rollout/rollback).
4. Cập nhật `STATUS.md` mỗi phase.

### L4

1. `/question-scope L4` — coi bước Idea/Scope đã xong.
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
/question-scope L2 — bug: submit form trả 500 khi email trùng (@api/register.ts).
```

Thêm ví dụ: mục [Prompt mẫu](#prompt-mẫu-copy-paste) ở trên.

---

## Cây quyết định nhanh

Text: mục dưới **Một câu nhớ** + bảng L ở trên. Flowchart + IDE: [references/level-picker.md](references/level-picker.md).

---

## File trong thư mục này

| File | Ai đọc |
| ---- | ------ |
| **README.md** (file này) | Người — preset, anti-pattern, checklist L2↔L3, Regression |
| **references/CHEATSHEET.md** | Người — one-pager tiếng Anh (trigger, token, level) |
| **examples/sample-prompts.md** | Người / agent — prompt mẫu (English) |
| **SKILL.md** | Agent — contract, gates, pipeline (core) |
| **references/** | Agent — gray-zone, playbooks, supplement, Kiro, testing ([index](references/README.md)) |
| **templates/phases/** | Agent copy khi tạo `docs/work/…` ([STRUCTURE.md](../STRUCTURE.md)) |

**Canonical:** Nếu README và SKILL.md lệch nhau, ưu tiên **SKILL.md** và **references/** (tiếng Anh).

