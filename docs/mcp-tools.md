# MCP Tools

| Tool              | Purpose                                                                                    | Key params                       |
| ----------------- | ------------------------------------------------------------------------------------------ | -------------------------------- |
| `search_code`     | Tìm code theo semantic similarity + keyword overlap                                        | `query`, `project`, `top_k`      |
| `get_context`     | Lấy context trong budget token, intent-aware (search/explain/refactor/debug/test/generate) | `query`, `project`, `max_tokens` |
| `analyze_impact`  | Phân tích blast radius trước khi sửa shared symbol/file                                    | `node`, `project`, `depth`       |
| `find_references` | Tìm tất cả nơi reference đến symbol (graph + vector search)                                | `symbol`, `project`              |
| `explain_symbol`  | Tóm tắt symbol: kind, file, dependencies, callers, calls                                   | `symbol`, `project`              |

## Output contract (common fields)

Mỗi tool luôn trả về:

```json
{
  "summary": "Human-readable summary",
  "missing_context": ["What data was unavailable"],
  "confidence": 0.82
}
```

Plus tool-specific fields (xem docstring trong `mcp_server/tools/*.py`).
