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
    query: str, project: str = "__default__", top_k: int = 10, max_tokens: int = 4000
) -> dict:
    """Retrieve code context within a token budget."""
    return TOOLS["get_context"](
        {"query": query, "project": project, "top_k": top_k, "max_tokens": max_tokens}
    )


@mcp.tool()
def analyze_impact(node: str, depth: int = 2) -> dict:
    """Analyze blast radius of a graph node (file or symbol)."""
    return TOOLS["analyze_impact"]({"node": node, "depth": depth})


@mcp.tool()
def find_references(symbol: str) -> dict:
    """Find all graph nodes referencing a symbol."""
    return TOOLS["find_references"]({"symbol": symbol})


@mcp.tool()
def explain_symbol(symbol: str) -> dict:
    """Summarize a symbol's presence in the codebase graph."""
    return TOOLS["explain_symbol"]({"symbol": symbol})


if __name__ == "__main__":
    mcp.run()
