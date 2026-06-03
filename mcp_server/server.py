"""MCP stdio entrypoint for Cursor / Kiro.

Tool functions are plain synchronous Python functions registered via FastMCP.
"""
from mcp.server.fastmcp import FastMCP
from mcp_server.registry import TOOLS

mcp = FastMCP("ai-core")


@mcp.tool()
def search_code(query: str, project: str = "__default__", top_k: int = 10) -> dict:
    """Search indexed code by semantic similarity and keyword overlap."""
    return TOOLS["search_code"]({"query": query, "project": project, "top_k": top_k})


@mcp.tool()
def get_context(
    query: str, project: str = "__default__", top_k: int = 10, max_tokens: int = 12000
) -> dict:
    """Retrieve code context within a token budget."""
    return TOOLS["get_context"](
        {"query": query, "project": project, "top_k": top_k, "max_tokens": max_tokens}
    )


@mcp.tool()
def analyze_impact(node: str, project: str = "__default__", depth: int = 2) -> dict:
    """Analyze blast radius of a graph node (file or symbol)."""
    return TOOLS["analyze_impact"]({"node": node, "project": project, "depth": depth})


@mcp.tool()
def find_references(symbol: str, project: str = "__default__") -> dict:
    """Find all graph nodes referencing a symbol."""
    return TOOLS["find_references"]({"symbol": symbol, "project": project})


@mcp.tool()
def explain_symbol(symbol: str, project: str = "__default__") -> dict:
    """Summarize a symbol's presence in the codebase graph."""
    return TOOLS["explain_symbol"]({"symbol": symbol, "project": project})


@mcp.tool()
def reindex_project(project: str = "__default__") -> dict:
    """Trigger re-indexing for a project (clears caches)."""
    return TOOLS["reindex_project"]({"project": project})


if __name__ == "__main__":
    mcp.run()
