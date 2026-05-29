# Confirmation prompts (question-scope)

**All AI IDEs** — same shape on Cursor, Kiro, Windsurf, Copilot, JetBrains AI, Claude Code, and any other host. Presentation: native multi-option picker **when available**, else numbered list — [host-ui.md](./host-ui.md).

Agents often present options that are **too thin** (bare `L2` / `L3`, or “JSON vs redirect” with no context). This file is the **required shape** for user confirmations when scope is active.

**When to read:**

| Moment | Section |
| ------ | ------- |
| `/question-scope` **without** `Lx` — before any Spec/Patch/Code | [§ A Level pick](#a-level-pick-idea--suggest--options) |
| After `Level: Lx` header — ambiguous **how** to build | [§ B Clarifying options (§12)](#b-clarifying-options-12) |
| Work exceeds chosen L | [§ C Escalation re-pick](#c-escalation-re-pick) |

**Related:** canonical level labels [level-picker.md](./level-picker.md) · §12 rules [clarifying-options.md](./clarifying-options.md) · runtime STOP [level-picker-runtime.md](./level-picker-runtime.md).

**Not the same as `brainstorming`:** pickers confirm **one fork** with trade-offs; brainstorming approves a **full spec** over multiple turns — see [§ Grounding & viability](#grounding--viability-without-full-brainstorming).

---

## Grounding & viability (without full brainstorming)

**Question:** How are proposed options **feasible** if we skip `brainstorming` for level pick and §12?

**Answer:** Options need **clear trade-offs** + **honest source** (repo **or** idea) + **user pick (STOP)** + **verify after implement**. They do **not** all have to come from existing code.

### Two valid sources for §12 options

| Source | When to use | Label (pick one per option) |
| ------ | ----------- | --------------------------- |
| **Repo-grounded** | Extending a pattern already in the codebase | **`Fits repo:`** `<path or pattern>` |
| **Idea-driven** | A real alternative shape — product, architecture, or UX the user might want even if **not** in repo yet | **`New here:`** `<short note>` — greenfield in this repo is OK |

**Both** can appear in the **same** §12 block (e.g. “extend existing JSON callback” vs “new queue-based async flow”). Do **not** force every option to cite existing code.

**Idea-driven ≠ fabricated:** each option must be a **genuine fork** the user would recognize (not four random stacks). Viability = constraints + trade-offs + user choice, not “already implemented somewhere.”

### What each layer validates

| Layer | What it proves | How |
| ----- | -------------- | --- |
| **Level pick (L1–L4)** | Right **amount of ceremony** | Heuristics + [gray-zones.md](./gray-zones.md) + **For this task:** |
| **§12 options** | Right **fork** (repo or idea) | Name · behavior · trade-off · **Fits repo** *or* **New here** + user pick |
| **After pick** | Choice was implementable | Spec records D1; **Patch → Verify → tests**; refine if wrong |
| **Full design** (many open ideas) | Whole feature shape | **`brainstorming`** — not required for every §12 block |

### Before listing §12 options

**Always (no repo read required):**

- **Decision** + **Why it matters**
- **2–4** meaningful forks (2–3 usually enough) + **`Other — I'll specify`**
- Per option: behavior + **trade-off** (effort, risk, ops, client, tests)
- Per option: **`Fits repo:`** *or* **`New here:`** — never imply code exists when it does not

**When repo helps** (optional JIT — [progressive-context-jit.md](./progressive-context-jit.md)):

- Comparing **extend existing** vs **new approach**
- User asked “what do we have today?” or `@` paths
- Security/auth/money paths where stack rules need a real anchor

Then read **≤3** sources (neighbor handler, config, same concern elsewhere). Skip wide grep if options are purely product-level and user has not asked for code survey.

**Constraints** (apply to **all** options, repo or idea): rule **`code-standards`**, stack rules, security, stated AC, team/env limits. Idea-driven options state which constraint bites (e.g. “needs new worker → lean L3”).

### Level pick — what “viability” means here

Level options are **pre-vetted pipeline packages** ([level-picker.md](./level-picker.md)), not implementation designs. Viability = **honest fit to the user message** via:

- Structured **Idea** (Goal / Where / Done when)
- **Suggest** tied to the message (not generic “few files”)
- **For this task:** on each L
- Gray-zone **You get / You skip** table when two levels fit

If the user’s ask is **not** a level decision (e.g. “Postgres or Mongo?”) → **do not** use level pick; use §12 **after** `Level: Lx` or **`brainstorming`** if the whole feature is undefined.

### When options are **not** grounded enough

| Situation | Action |
| --------- | ------ |
| Idea vague (no outcome) **before** L pick | **`orchestra-decision`** → one decision → return to level pick |
| **L3–L4**, no spec, many open product questions | **`brainstorming`** (design gate) — not §12 alone |
| **One** fork, module unknown | §12 with **idea-driven** options + trade-offs, or ask user to `@` files — **do not** fake **Fits repo** |
| **Many** competing product directions | **`brainstorming`** (or `orchestra-decision` before L pick) — not §12 alone |
| User already chose in message | **Skip** §12 (`clarify:off` or AC explicit) |
| Spec/design **already approved** via `brainstorming` or attached plan | **Skip** §12 for the same decision — only **new** TBDs in plan delta |

### After `brainstorming` — do not duplicate §12

When the user **approved** a spec from **`brainstorming`** (or an attached plan with AC):

- Decisions captured in `docs/specs/…` / plan are **done** — do **not** run §12 again for the same fork (e.g. JSON vs redirect already in approved spec).
- Run §12 only for **new** open items: plan **TBD**, Cursor/host Plan unresolved bullets, or a **changed** requirement.
- If the approved spec is silent on one critical fork → update spec (minimal delta) **or** one §12 block for **that** gap only — not a full re-brainstorm.

### User confirmation = feasibility gate

**STOP** means the user (not the agent) accepts one option. Agent records in **Decisions** / Spec. Wrong pick surfaces in **Verify** / tests — fix in **Iterate**, not by re-running §12 for the same D1 unless requirements change.

**Do not** label an option “recommended” unless repo policy or security requires it — state **why** in one line.

---

## A. Level pick (Idea + Suggest + options)

### Output order (required)

1. `Using question-scope — level picker.` (or `— Lx` if preset — then **skip** steps 2–5)
2. **Idea** (structured — not one vague sentence)
3. **Suggest** (heuristic — user may override)
4. **Gray zone** line (only when a pair from [gray-zones.md](./gray-zones.md) fits)
5. **Options** — 2 (gray) or 4 (default); each label = canonical string + **task clause** (structured picker **or** numbered list — same text)
6. **STOP** — explicit: no Spec / Patch / Code / `docs/work/` until pick (required on **every** host)

### Idea (structured)

Use **3–5 short bullets** (not a wall of prose):

| Bullet | Content |
| ------ | ------- |
| **Goal** | What the user wants (verb + object), in their words |
| **Where** | Module, API, surface, or repo area (infer from message; say “unclear” if unknown) |
| **Done when** | Observable outcome (response, file, behavior) |
| **Out of scope** (if any) | What we are **not** doing in this pick (optional) |
| **Open** (if any) | Missing AC detail that does **not** block **level** pick (save §12 for after L is chosen) |

### Suggest (one block)

```text
Suggest: L2 (lean) — <one reason tied to this message, not generic “few files”>
```

If gray zone applies:

```text
Gray zone: L2 ↔ L3 — <one line why both fit; name the pair>
Suggest: L2 or L3 — <which you lean toward and why; user chooses>
```

**Do not** lock the level in Suggest. **Do not** start Spec/Patch because Suggest said L2.

### Options — task-tailored labels

1. Copy the **canonical** `Lx — … · …` string from [level-picker.md § Option copy](./level-picker.md#option-copy-required--user-must-read-before-pick).
2. Append **one** task-specific clause (same option, still ≤ ~3 lines total):

```text
For this task: <what they get if they pick this L — files, ceremony, tests, docs>
```

**Structured picker (when host provides):** put the **full** string (canonical + `For this task:`) in each option **label** field — [host-ui.md](./host-ui.md).

### Gray zone — add a comparison (recommended)

After the two option labels, add a **compact** table so the user can decide without re-reading pipelines:

| If you pick | You get | You skip |
| ----------- | ------- | -------- |
| **L2** | … task-specific … | … |
| **L3** | … task-specific … | … |

### Worked example — export on existing users API

**User:** `/question-scope Add GET /users/export CSV`

```text
Using question-scope — level picker.

**Idea**
- **Goal:** Add GET export that returns users as CSV from the existing users API.
- **Where:** Existing users module / route layer (not a new service).
- **Done when:** Authenticated client can download CSV with expected columns.
- **Open:** Column set and pagination — can nail in Spec after you pick L.

**Suggest:** L2 or L3 — export on an **existing** API is the L2↔L3 gray zone; lean **L2** if you want a small PR with TC in Spec; lean **L3** if you want Plan, `l3-02` Test gate, Regression, and Ship notes.

**Gray zone: L2 ↔ L3**

| If you pick | You get | You skip |
| ----------- | ------- | -------- |
| **L2** | Spec (+ TC) → patch route/service/tests → scoped Verify | Phased `l3-*`, full Regression + Ship ceremony |
| **L3** | `docs/work/…`, Plan → **Test** (`l3-02`) before Code → Regression + Ship | Lightest path — more process |

Choose one:

1. **L2 — Extend existing pattern** · TC in Spec if behavior change · Scoped Verify (no full Regression gate) · **For this task:** one new GET on users module, likely route + service + test.
2. **L3 — New module/API/worker** · Plan → **Test** (`l3-02`) before Code → Regression + Ship · **For this task:** phased folder, RED tests before handler, rollout in `l3-03`.

STOP — reply `L2`, `L3`, or `/question-scope L3 — …` (same task). No Spec/Patch until you pick.
```

### Level pick — do not

| Bad | Good |
| --- | ---- |
| `Pick L1–L4` with no Idea | Structured **Idea** first |
| Buttons labeled only `L2`, `L3` | Full pipeline note + **For this task:** |
| Auto-start Spec because Suggest said L2 | **STOP** until explicit pick |
| Four options when only L2↔L3 fits | Exactly **two** labeled options |
| §12 JSON vs redirect in same turn as level pick | Level pick **first**; §12 **after** header |

---

## B. Clarifying options (§12)

Runs **after** `Level: Lx | Pipeline: …` when **how** to build is still ambiguous. Full rules: [clarifying-options.md](./clarifying-options.md).

### Decision scan (before Patch / Test / Code)

Scan the user message and draft Spec/Plan. If any row is **unclear** and changes contract, tests, security, or UX → run §12 (one decision per turn when possible):

| Area | Example fork |
| ---- | ------------- |
| **API / contract** | JSON body vs redirect vs webhook payload |
| **Auth / session** | Cookie vs bearer; shared session store |
| **Errors / idempotency** | Retry-safe POST; duplicate handling |
| **Storage / infra** | S3 vs local; queue vs sync |
| **UX / client** | SPA reads response vs deep link |
| **Rollout** | Feature flag vs big-bang (when AC silent) |

**Skip §12** when AC or attached plan already decides (use **`clarify:off`** only to skip picker when scope is on but AC is explicit).

### Output order (required)

1. `Using question-scope — clarifying options (§12).` (optional but clear)
2. **Decision:** one question headline (ends with `?`)
3. **Why it matters:** 1–2 lines — what breaks if we guess (AC, tests, security, client)
4. **Options:** 2–4 labeled choices; each = **name · behavior · trade-off**
5. Last option: **`Other — I'll specify`**
6. **STOP** — no Patch / new-contract Test / Code until pick

### Option label shape (§12)

```text
<Short name> — <behavior> · <trade-off> · Fits repo: <path/pattern>   OR   New here: <greenfield note>
```

**Do not** use bare `A` / `B`. **Do not** label **Fits repo** on an idea that does not exist in the codebase — use **New here**. See [Grounding & viability](#grounding--viability-without-full-brainstorming).

### Worked example — OAuth callback (L2)

**User:** `/question-scope L2 — Zalo OAuth callback. JSON for SPA or redirect? Implement now.`

```text
Level: L2 | Pipeline: Context → Spec (+ TC if behavior change) → Patch → Verify → Review → MD

Using question-scope — clarifying options (§12).

**Decision:** How should the Zalo OAuth **callback** respond after provider redirects back?

**Why it matters:** Drives handler return type, tests (assert JSON vs `302`), and SPA integration — cannot Patch safely without this.

Choose one:

1. **JSON body** — `{ success, link }` for SPA · Simpler SPA read after redirect · **Fits repo:** `<path>` if neighbor already returns JSON; else **New here:** standard SPA callback (no existing handler yet) · **Tests:** JSON schema.
2. **HTTP 302 redirect** — deep link `app://…` · Better native/deep-link UX · **Fits repo:** if OAuth callbacks already redirect; else **New here:** new redirect contract · **Tests:** `Location` header.
3. **Server-side session only** — set cookie, SPA loads `/me` later · **New here:** different product shape; more server state · **Fits repo:** only if session pattern exists — cite or **New here**.
4. **Other — I'll specify**

STOP — no Patch until you pick or describe option 4.
```

### Record the answer

In Spec, plan delta, or phase MD:

```markdown
## Decisions
- **D1 (chosen):** <option label or user Other text> — blocks: callback contract
```

---

## C. Escalation re-pick

When work **exceeds** the chosen L:

1. **One line why** (e.g. “needs new worker → above L2”).
2. Re-present **adjacent pair** with same **task-tailored** labels + comparison table.
3. **STOP** until confirm.

Do **not** silently upgrade to L3/L4 or downgrade to L2.

---

## Host UI summary

See [host-ui.md](./host-ui.md). **Every IDE:** full labels + **STOP**. **Optional:** host native multi-option picker with the **same** label text as chat fallback.

**Never** mix level pick and §12 in one picker block (any host).
