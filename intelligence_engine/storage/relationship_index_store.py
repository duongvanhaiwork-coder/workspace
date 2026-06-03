"""Relationship Index Store — fast relationship lookup (architecture section 4.5).

Provides pre-computed relationship summaries per symbol for:
- refactor impact (nhanh)
- caller/callee lookup
- DTO/model dependency

Instead of traversing the full NetworkX graph for every query,
this index stores a denormalized view per symbol.
"""

import json
from pathlib import Path
from typing import Any


class RelationshipIndexStore:
    """Per-project relationship index persistence.

    Schema per entry:
    {
        "symbol": "OrderService.createOrder",
        "file_path": "src/services/order.service.ts",
        "line_start": 42,
        "reads": ["CreateOrderDto.TotalAmount", ...],
        "writes": ["OrderEntity.TotalAmount", ...],
        "calls": ["OrderRepository.create", ...],
        "called_by": ["OrderController.create", ...],
        "uses_dto": ["CreateOrderDto"],
        "uses_model": ["OrderEntity"]
    }
    """

    def __init__(self, base_dir: str | Path = "data/relationship_index") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, dict[str, dict[str, Any]]] = {}  # project -> {key -> entry}
        self._load_from_disk()

    @staticmethod
    def _entry_key(entry: dict[str, Any]) -> str:
        """Generate unique key from symbol + file_path + line_start."""
        symbol = entry.get("symbol", "")
        file_path = entry.get("file_path", "")
        line_start = entry.get("line_start", 0)
        return f"{file_path}:{symbol}:{line_start}"

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

    def get(self, symbol: str, project: str = "__default__") -> dict[str, Any] | None:
        """Get relationship entry for a symbol (searches by qualified symbol name)."""
        entries = self._index.get(project, {})
        # Direct key match first
        if symbol in entries:
            return entries[symbol]
        # Search by symbol field
        for entry in entries.values():
            if entry.get("symbol") == symbol:
                return entry
        return None

    def upsert(self, entry: dict[str, Any], project: str = "__default__") -> None:
        """Upsert a single relationship entry."""
        if project not in self._index:
            self._index[project] = {}
        key = self._entry_key(entry)
        self._index[project][key] = entry
        self._persist(project)

    def upsert_batch(self, entries: list[dict[str, Any]], project: str = "__default__") -> None:
        """Upsert multiple entries at once."""
        if project not in self._index:
            self._index[project] = {}
        for entry in entries:
            key = self._entry_key(entry)
            self._index[project][key] = entry
        self._persist(project)

    def delete_by_file(self, file_path: str, project: str = "__default__") -> int:
        """Remove all entries for symbols in a given file."""
        if project not in self._index:
            return 0
        to_remove = [
            key for key, entry in self._index[project].items()
            if entry.get("file_path") == file_path
        ]
        for key in to_remove:
            del self._index[project][key]
        if to_remove:
            self._persist(project)
        return len(to_remove)

    def find_callers(self, symbol: str, project: str = "__default__") -> list[str]:
        """Find all symbols that call the given symbol."""
        entry = self.get(symbol, project)
        if entry:
            return entry.get("called_by", [])
        # Fallback: scan all entries
        callers = []
        for _, e in self._index.get(project, {}).items():
            if symbol in e.get("calls", []):
                callers.append(e["symbol"])
        return callers

    def find_readers(self, symbol: str, project: str = "__default__") -> list[str]:
        """Find all symbols that read the given symbol."""
        readers = []
        for _, e in self._index.get(project, {}).items():
            if symbol in e.get("reads", []):
                readers.append(e["symbol"])
        return readers

    def clear(self, project: str = "__default__") -> None:
        """Clear all entries for a project."""
        self._index[project] = {}
        self._persist(project)
