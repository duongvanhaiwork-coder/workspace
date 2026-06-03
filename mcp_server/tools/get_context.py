"""get_context — retrieve code context within token budget.

Delegates to Orchestrator which handles:
Intent Analyzer → Retrieval Planner → Search/Graph → Context Builder.

Output follows strict schema (section 12):
{
    "meta": { "intent", "confidence", "token_budget": { "max", "used" } },
    "summary": "...",
    "results": { ... },
    "missing_context": []
}
"""

from intelligence_engine.context.orchestrator import Orchestrator
from mcp_server.tools.output_schema import wrap_output


def get_context(args: dict) -> dict:
    query = args["query"]
    project = args.get("project", "__default__")
    max_tokens = int(args.get("max_tokens", 12000))
    top_k = int(args.get("top_k", 10))

    orchestrator = Orchestrator(project=project, max_tokens=max_tokens, top_k=top_k * 2)
    raw = orchestrator.run(query)

    # Extract fields for strict schema
    intent = raw.pop("intent", "search")
    confidence = raw.pop("confidence", 0.0)
    summary = raw.pop("summary", "")
    missing_context = raw.pop("missing_context", [])
    prompt_guidance = raw.pop("prompt_guidance", None)
    target = raw.pop("query", query)

    # Inject Layer 1 — Intent Context
    raw["intent_context"] = {
        "intent": intent,
        "query": query,
        "target": raw.pop("_target", target),
    }

    # Inject prompt_guidance for LLM
    if prompt_guidance:
        raw["prompt_guidance"] = prompt_guidance

    # Calculate used tokens from chunks
    chunks = raw.get("chunks", [])
    used_tokens = sum(max(1, len(c.get("content", "")) // 4) for c in chunks)

    return wrap_output(
        summary=summary,
        results=raw,
        missing_context=missing_context,
        intent=intent,
        confidence=confidence,
        max_tokens=max_tokens,
        used_tokens=used_tokens,
    )
