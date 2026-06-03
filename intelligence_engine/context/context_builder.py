"""Context Builder — gom, lọc, xếp hạng, cắt token.

Responsibilities:
- Filter irrelevant results (low score, wrong domain)
- Rank by relevance to target
- Enforce hard limits: max 5 files, max 15 chunks
- Cut to token budget
- Sanitize symbol names
"""

from __future__ import annotations

from .token_budget import TokenBudget

# Hard output limits
MAX_FILES = 5
MAX_CHUNKS = 15
MAX_REFERENCES = 20
MAX_ENTRYPOINTS = 5
MAX_DEPENDENCY_PATHS = 10
MIN_RELEVANCE_SCORE = 0.1


class ContextBuilder:
    """Filter, rank, and trim retrieval results to fit output constraints."""

    def __init__(self, budget: TokenBudget | None = None) -> None:
        self.budget = budget or TokenBudget()

    def build_chunks(self, rows: list[dict], target: str) -> list[dict]:
        """Select top chunks within token budget and hard limits."""
        # Filter: only rows that are somewhat relevant
        relevant = [r for r in rows if r.get("score", 0) >= MIN_RELEVANCE_SCORE]
        if not relevant:
            relevant = rows[:MAX_CHUNKS]  # fallback: take top N even if low score

        # Deduplicate by file+start_line
        seen: set[str] = set()
        unique: list[dict] = []
        for row in relevant:
            key = f"{row.get('file_path', '')}:{row.get('start_line', 0)}"
            if key not in seen:
                seen.add(key)
                unique.append(row)

        # Limit files
        file_order: dict[str, int] = {}
        for row in unique:
            f = row.get("file_path", "")
            if f not in file_order:
                if len(file_order) >= MAX_FILES:
                    continue
                file_order[f] = len(file_order)

        # Build chunks within limits
        chunks: list[dict] = []
        used_tokens = 0
        for row in unique:
            if len(chunks) >= MAX_CHUNKS:
                break
            f = row.get("file_path", "")
            if f not in file_order:
                continue

            content = row.get("content", "")
            cost = self.budget.estimate(content)
            if used_tokens + cost > self.budget.max_tokens:
                break

            symbol = row.get("symbol", "")
            chunks.append({
                "file": f,
                "symbol": symbol if _valid_symbol(symbol) else "",
                "kind": row.get("kind", "unknown"),
                "line_start": row.get("start_line", 0),
                "line_end": row.get("end_line", 0),
                "reason": _chunk_reason(target, row),
                "content": content,
            })
            used_tokens += cost

        return chunks

    def build_entrypoints(self, rows: list[dict]) -> list[dict]:
        """First high-score result per file = entrypoint. Max 5."""
        seen: set[str] = set()
        entries: list[dict] = []
        for row in rows[:20]:
            f = row.get("file_path", "")
            if f in seen or row.get("score", 0) < 0.25:
                continue
            seen.add(f)
            symbol = row.get("symbol", "")
            entries.append({
                "file": f,
                "symbol": symbol if _valid_symbol(symbol) else "",
                "kind": row.get("kind", ""),
                "line_start": row.get("start_line", 0),
                "line_end": row.get("end_line", 0),
            })
            if len(entries) >= MAX_ENTRYPOINTS:
                break
        return entries

    def build_references(self, refs: list[dict]) -> list[dict]:
        """Trim and deduplicate references. Max 20."""
        seen: set[str] = set()
        out: list[dict] = []
        for ref in refs:
            key = f"{ref.get('file', '')}:{ref.get('line', 0)}"
            if key in seen:
                continue
            seen.add(key)
            out.append(ref)
            if len(out) >= MAX_REFERENCES:
                break
        return out

    def trim_dependency_paths(self, paths: list[dict]) -> list[dict]:
        """Deduplicate and limit dependency paths."""
        seen: set[str] = set()
        out: list[dict] = []
        for p in paths:
            key = f"{p.get('source', '')}→{p.get('target', '')}:{p.get('relation', '')}"
            if key in seen:
                continue
            seen.add(key)
            out.append(p)
            if len(out) >= MAX_DEPENDENCY_PATHS:
                break
        return out

    def used_tokens(self, chunks: list[dict]) -> int:
        return sum(self.budget.estimate(c.get("content", "")) for c in chunks)


def _valid_symbol(name: str) -> bool:
    if not name or len(name) > 80:
        return False
    return not any(ch in name for ch in ("\n", "{", "}", "()", ";"))


def _chunk_reason(target: str, row: dict) -> str:
    content = row.get("content", "").lower()
    if target.lower() in content:
        return f"Contains '{target}'"
    return "Semantically relevant"
