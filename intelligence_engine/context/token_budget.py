class TokenBudget:
    def __init__(self, max_tokens: int = 4000) -> None:
        self.max_tokens = max_tokens

    def estimate(self, text: str) -> int:
        return max(1, len(text) // 4)
