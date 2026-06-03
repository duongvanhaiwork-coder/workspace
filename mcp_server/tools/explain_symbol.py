from mcp_server.tools.find_references import find_references


def explain_symbol(args: dict) -> dict:
    symbol = args["symbol"]
    refs = find_references({"symbol": symbol})
    return {
        "symbol": symbol,
        "summary": (
            f"Symbol `{symbol}` appears in {len(refs['items'])} graph node(s). "
            "Use get_context for detailed code context."
        ),
        "references": refs["items"],
    }
