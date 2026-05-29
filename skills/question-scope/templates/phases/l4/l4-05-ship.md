# L4 — Phase 5: Ship

**Canonical steps:** Refine, Document (Architecture / AI / Delivery)

**Order:** Fill delivery/rollout/rollback below → then **`finishing-a-development-branch`** after Prove/Verify green (fresh verify; merge / PR / keep / discard). Record git choice below.

## Refine (no behavior change)

- …

### Refine checklist

- [ ] No new acceptance `Then`; only readability / perf-safe tweaks
- [ ] Dead code / debug logs removed from touched files

---

## Document — Architecture layer

### Dependency graph

- *Example:* `gateway` → `billing-service` → `postgres`; MCP client only talks to `gateway`.

### Domain boundaries

- *Example:* `Billing` context owns invoices; `Identity` owns tokens — no cross-aggregate writes.

### Scalability

- *Example:* Stateless API replicas; queue for webhook bursts; shard key = `tenantId`.

### Observability

- *Example:* Structured logs with `trace_id`; RED metrics on `/checkout`; alert on p95 > 500ms.

### Security (architecture)

- *Example:* mTLS service-to-service; secrets from vault; no PII in info logs.

### Deployment

- *Example:* Blue/green on k8s; health `/ready` waits for DB migration job.

### Rollback

- *Example:* Revert Helm release N-1; feature flag OFF removes new code path.

### Cost estimation

- *Example:* +$40/mo vector index; +2M tokens/mo at peak — within budget X.

---

## Document — AI layer (if applicable; else mark N/A)

### Token optimization

- *Example:* Summarize tool results >2k tokens before second model call.

### Memory / context strategy

- *Example:* Sliding window last 10 turns; pin system + tool schema.

### Retrieval strategy

- *Example:* Hybrid BM25 + embeddings; top-k=8 with MMR dedupe.

### Embedding strategy

- *Example:* `text-embedding-3-small`; batch embed on file save.

### Chunking

- *Example:* 512 tokens / 64 overlap; split on headings for docs.

### Caching

- *Example:* Redis 5m TTL for identical queries; invalidate on write.

---

## Document — Delivery layer

### Rollout strategy

- *Example:* 1% canary 24h → 50% → 100% with error budget gate.

### Migration strategy

- *Example:* Expand (new column nullable) → backfill job → contract switch → contract (drop old).

### Backward compatibility

- *Example:* API v1 clients ignore unknown fields; old mobile min version 2.3.

---

## Links

- PR / release: …
- Runbooks / dashboards: …

## Pre-merge review (L4 supplement)

- [ ] **`caveman-review`** logged in `l4-04-prove.md`
- [ ] **`requesting-code-review`** done (formal subagent + `prompts/code-reviewer.md`) **or** explicitly waived in `STATUS.md`
- [ ] Critical / Important findings fixed or accepted with reason

## Ship checklist (`finishing-a-development-branch`)

- [ ] Tests green — evidence in prove/build phase files
- [ ] Pre-merge review complete (section above) when supplement on
- [ ] **`finishing-a-development-branch`** — user chose: merge | PR | keep | discard
- [ ] Worktree / release branch state documented (if used)
- [ ] Architecture + Delivery sections filled or explicitly N/A
- [ ] AI section filled or **N/A (no AI in scope)**
- [ ] `STATUS.md` marked **complete**; all phase files state = done
