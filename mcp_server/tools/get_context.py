"""get_context — retrieve code context within token budget.

Delegates to Orchestrator which handles:
Intent Analyzer → Retrieval Planner → Search/Graph → Context Builder.

Output adapts to query intent but always includes:
{
    "summary": "...",
    "chunks": [...],
    "missing_context": [],
    "confidence": 0.82
}
Plus intent-specific fields (entrypoints, dependency_paths, etc).
"""

from intelligence_engine.context.orchestrator import Orchestrator


def get_context(args: dict) -> dict:
    query = args["query"]
    project = args.get("project", "__default__")
    max_tokens = int(args.get("max_tokens", 12000))
    top_k = int(args.get("top_k", 10))

    orchestrator = Orchestrator(project=project, max_tokens=max_tokens, top_k=top_k * 2)
    return orchestrator.run(query)
