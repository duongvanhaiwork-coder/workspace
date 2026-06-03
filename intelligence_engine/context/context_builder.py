from .token_budget import TokenBudget


class ContextBuilder:
    def __init__(self, budget: TokenBudget | None = None) -> None:
        self.budget = budget or TokenBudget()

    def build(self, rows: list[dict]) -> str:
        used = 0
        parts: list[str] = []
        for row in rows:
            header = f"// FILE: {row.get('file_path')}:{row.get('start_line')}-{row.get('end_line')}"
            block = f"{header}\n{row.get('content', '')}"
            cost = self.budget.estimate(block)
            if used + cost > self.budget.max_tokens:
                break
            parts.append(block)
            used += cost
        return "\n\n---\n\n".join(parts)
