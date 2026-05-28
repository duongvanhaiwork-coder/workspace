---
name: orchestra-decision
description: Low-loop decision orchestration using a 4-quadrant matrix and a minimal retrieval workflow (classify -> predict sources -> pre-collect -> up to 2 passes by default). Use for prompt/SOP/rule design, AI helper or API design, and ambiguous requests that need fast convergence.
---

# Orchestra Decision (Low-loop Orchestrator)

## Instruction precedence (must follow)

Always apply instructions in this order:

1. System/developer constraints
2. User request and scope
3. This skill workflow

If higher-level instructions conflict with this skill, follow higher-level instructions and adapt the workflow.

**vs `brainstorming`:** **`orchestra-decision`** picks direction fast (Q1–Q4, 2–5 options, one decision) when the problem is still fuzzy. **`brainstorming`** produces an approved **design spec** section-by-section — use after scope/level is clear or when building a new feature needs full design gate.

## Quick start

When a request arrives, avoid jumping into broad implementation immediately. Run this pipeline first and keep retrieval/clarification loops minimal.

### Phase 1 — Classify and understand

Produce these three items first (short and explicit):

- **Goal**: one-sentence deliverable
- **Constraints**: format, platform, timeline, risk, scope
- **Output shape**: expected final artifact (plan, API contract, code changes, prompt template, etc.)

Then assign one quadrant:

- **Q1 Inspiration**: user is blank and needs exploration (diverge hard)
- **Q2 Seed**: user has a vague idea (guided divergence)
- **Q3 Unpack**: user knows intent but logic is complex (stepwise converge)
- **Q4 Exact Mold**: exact structure or strict format is required (converge hard)

### Phase 2 — Predict source shortlist (before reading)

Create a shortlist (up to 4 sources). Priority:

1. User-referenced paths (for example `@src/...`)
2. Repo `README`, config, and applicable rules (`question-scope`, `code-standards`, `@workflow`, stack rules by file type)
3. `docs/orchestra/INDEX.md` and `docs/orchestra/collect-before.md` **only if they exist**
4. Optional workspace app manifest (e.g. `projects.json`) when the task touches indexed multi-repo setups — skip if absent.

If orchestra docs are missing (usual case), skip step 3 and continue.

### Phase 3 — Pre-collect minimum context

Collect only enough context to pick a safe approach:

- **Task type**: ideation, decision, implementation, operations
- **Default policy**: for example tutoring vs direct answer, retention vs deletion
- **Hard blockers**: auth, permissions, compliance, required output format
- **Latency/SLA**: only if it changes solution shape

**Stop condition**: once you can select quadrant + output shape + default policy safely.

### Phase 4 — Retrieval passes (default max 2)

- **Pass 1**: read entry docs or the single most relevant file.
- **Gate: enough signal?**
  - **Yes**: proceed.
  - **No**: do one of:
    - Ask 1-2 hard-blocker questions only, then proceed.
    - Or run **Pass 2** (one extra high-value source), then proceed.

Optional **Pass 3** is allowed only when:

- there is a clear technical blocker, and
- blocker cannot be resolved by 1-2 concise questions.

Avoid further loops unless the user explicitly requests deep research.

### Phase 5 — Orchestrate (Diverge -> Converge -> Decide)

Use only the minimum breadth needed:

- **Diverge**: propose 2-5 realistic options
- **Converge**: evaluate with 3-7 explicit criteria
- **Decide**: choose one, list risks, list concrete next actions

## Output contract (concise first)

Default structure:

- **Quadrant**: chosen quadrant and short reason
- **Assumptions**: only if needed
- **Options**: 2-5
- **Decision**: one recommended path with trade-offs
- **Next actions**: concrete executable steps

If response is long, split:

- **Part 1**: decision + next actions
- **Part 2**: details only when necessary or requested

## Quality gate before sending

Check quickly:

- Is the decision justified by explicit criteria?
- Are major risks and constraints stated?
- Are next actions directly executable?
- Is the response aligned with user output shape?

## UX live text (progress only, no chain-of-thought)

If user asks for live text, stream status updates only (no detailed hidden reasoning). Example statuses:

- "Reading request..."
- "Identifying constraints..."
- "Choosing diverge/converge tactic..."
- "Drafting options..."
- "Scoring against criteria..."
- "Summarizing recommendation..."

Provide brief rationale summaries; do not reveal chain-of-thought.

## Examples

### Example A — Feature request (enrollment cancellation)

**Input**: "Add a feature so students can cancel their enrollment"

**Expected behavior**:

- Phase 1 likely maps to **Q2 Seed** or **Q3 Unpack**
- Ask at most 1-2 hard-blocker questions (status update vs deletion, backend-only vs full-stack)
- Compare options (status-cancel, soft-delete, hard-delete), choose one, list next actions

### Example B — AI helper API tool (Node + streaming progress)

**Input**: "I want an AI homework-helper API with model options and live streaming progress"

**Expected behavior**:

- Phase 1 likely maps to **Q3 Unpack**
- Decide default policy (tutor vs direct answer), or ask exactly one hard-blocker question
- Output API contract with:
  - endpoints (sync + stream)
  - request schema (input, options: model/effort/timeBudget)
  - streaming event types (status/plan/result/error)
  - loop stop conditions

## Additional resources

- Use when present:
  - `docs/orchestra/INDEX.md`
  - `docs/orchestra/collect-before.md`
- If not found, skip and continue with user-provided paths and repo conventions.

