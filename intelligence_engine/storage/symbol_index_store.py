"""Symbol Index Store — symbol metadata storage (architecture section 4.2).

Stores symbol metadata for fast lookup by name, qualified_name, or file_path.
Separate from vector store (code_chunks) — this is for exact matching and navigation.

Schema per entry:
{
    "project": "business-lounge-api",
    "symbol_id": "business-lounge-api:OrderService.createOrder",
    "name": "createOrder",
    "qualified_name": "OrderService.createOrder",
    "kind": "method",
    "file_path": "src/services/order.service.ts",
    "line_start": 42,
    "line_end": 88,
    "signature": "async createOrder(dto: CreateOrderDto)"
}
"""

import json
from pathlib import Path
from typing import Any


class SymbolIndexStore:
    """Per-project symbol index persistence."""

    def __init__(self, base_dir: str | Path = "data/symbol_index") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, dict[str, dict[str, Any]]] = {}  # project -> {symbol_id -> entry}
        self._load_from_disk()

    def _project_path(self, project: str) -> Path:
        safe_name = project.replace("/", "_").replace("\\", "_")
        return self.base_dir / f"{safe_name}.json"

    def _load_from_disk(self) -> None:
        for file in self.base_dir.glob("*.json"):
            project = file.stem
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                self._index[project] = data
            except (json.JSONDecodeError, OSError):
                continue

    def _persist(self, project: str) -> None:
        data = self._index.get(project, {})
        self._project_path(project).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _get_entries(self, project: str) -> dict[str, dict[str, Any]]:
        return self._index.setdefault(project, {})

    def upsert(self, entry: dict[str, Any], project: str = "__default__") -> None:
        """Upsert a single symbol entry."""
        entries = self._get_entries(project)
        symbol_id = entry.get("symbol_id", f"{project}:{entry.get('qualified_name', entry['name'])}")
        entry["symbol_id"] = symbol_id
        entry["project"] = project
        entries[symbol_id] = entry
        self._persist(project)

    def upsert_batch(self, entries: list[dict[str, Any]], project: str = "__default__") -> None:
        """Upsert multiple entries at once."""
        store = self._get_entries(project)
        for entry in entries:
            symbol_id = entry.get("symbol_id", f"{project}:{entry.get('qualified_name', entry['name'])}")
            entry["symbol_id"] = symbol_id
            entry["project"] = project
            store[symbol_id] = entry
        self._persist(project)

    def find_by_name(self, name: str, project: str = "__default__") -> list[dict[str, Any]]:
        """Find all symbols matching a name (exact)."""
        entries = self._get_entries(project)
        return [e for e in entries.values() if e.get("name") == name]

    def find_by_qualified_name(self, qualified_name: str, project: str = "__default__") -> dict[str, Any] | None:
        """Find symbol by qualified_name (e.g. OrderService.createOrder)."""
        entries = self._get_entries(project)
        for e in entries.values():
            if e.get("qualified_name") == qualified_name:
                return e
        return None

    def find_by_file(self, file_path: str, project: str = "__default__") -> list[dict[str, Any]]:
        """Find all symbols in a file."""
        entries = self._get_entries(project)
        return [e for e in entries.values() if e.get("file_path") == file_path]

    def search(self, query: str, project: str = "__default__") -> list[dict[str, Any]]:
        """Fuzzy search symbols by name or qualified_name."""
        entries = self._get_entries(project)
        query_lower = query.lower()
        results = []
        for e in entries.values():
            name = (e.get("name") or "").lower()
            qname = (e.get("qualified_name") or "").lower()
            if query_lower in name or query_lower in qname:
                results.append(e)
        return results

    def delete_by_file(self, file_path: str, project: str = "__default__") -> int:
        """Remove all symbols belonging to a file."""
        entries = self._get_entries(project)
        to_remove = [sid for sid, e in entries.items() if e.get("file_path") == file_path]
        for sid in to_remove:
            del entries[sid]
        if to_remove:
            self._persist(project)
        return len(to_remove)

    def clear(self, project: str = "__default__") -> None:
        """Clear all entries for a project."""
        self._index[project] = {}
        self._persist(project)

    def count(self, project: str = "__default__") -> int:
        """Count total symbols indexed for a project."""
        return len(self._get_entries(project))
