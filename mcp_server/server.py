"""MCP stdio entrypoint for Cursor / Kiro.

Tool functions are plain synchronous Python functions registered via FastMCP.
"""
from mcp.server.fastmcp import FastMCP
from mcp_server.registry import TOOLS

mcp = FastMCP("ai-core")


@mcp.tool()
def search_code(
    query: str,
    project: str = "__default__",
    top_k: int = 10,
    include_context: bool = False,
    max_tokens: int = 12000,
) -> dict:
    """Search indexed code by semantic similarity and keyword overlap.

    Use search_code only to find candidate files/symbols.
    Do NOT edit code based only on search_code results.
    After search_code returns relevant results, call get_context with the
    selected file_path/symbol to load full implementation and related context.

    Set include_context=true to automatically load full context inline
    (equivalent to search_code + get_context in one call). Use this when
    the intent is to modify or understand code implementation.

    Args:
        query: Natural language or symbol name to search for.
        project: Project name (last segment of workspace path).
        top_k: Maximum number of results to return.
        include_context: If true, auto-loads full context for top results.
        max_tokens: Token budget when include_context=true.
    """
    return TOOLS["search_code"]({
        "query": query,
        "project": project,
        "top_k": top_k,
        "include_context": include_context,
        "max_tokens": max_tokens,
    })


@mcp.tool()
def get_context(
    query: str, project: str = "__default__", top_k: int = 10, max_tokens: int = 12000
) -> dict:
    """Retrieve full code context within a token budget.

    Use get_context AFTER search_code, BEFORE answering implementation questions
    or making code changes. It returns full code, imports, references, callers,
    DTO/model/test context — everything needed to safely modify code.

    Call flow: search_code (find targets) → get_context (load full context) → edit.

    Args:
        query: Natural language query or symbol name.
        project: Project name (last segment of workspace path).
        top_k: Number of chunks to consider.
        max_tokens: Maximum token budget for returned context.
    """
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
