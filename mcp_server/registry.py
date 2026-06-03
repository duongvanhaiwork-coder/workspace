from mcp_server.tools.search_code import search_code
from mcp_server.tools.get_context import get_context
from mcp_server.tools.analyze_impact import analyze_impact
from mcp_server.tools.find_references import find_references
from mcp_server.tools.explain_symbol import explain_symbol
from mcp_server.tools.reindex_project import reindex_project

TOOLS = {
    "search_code": search_code,
    "get_context": get_context,
    "analyze_impact": analyze_impact,
    "find_references": find_references,
    "explain_symbol": explain_symbol,
    "reindex_project": reindex_project,
}
