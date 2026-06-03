from intelligence_engine.context.context_builder import ContextBuilder
from intelligence_engine.context.token_budget import TokenBudget
from mcp_server.tools.search_code import search_code


def get_context(args: dict) -> dict:
    max_tokens = int(args.get("max_tokens", 4000))
    result = search_code(args)
    budget = TokenBudget(max_tokens=max_tokens)
    context = ContextBuilder(budget=budget).build(result["items"])
    return {"context": context, "items": result["items"]}
