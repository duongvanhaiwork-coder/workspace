import json
from dataclasses import asdict
from pathlib import Path
from typing import Any
import math


class LanceDBStore:
    """Vector store with project scoping and JSON-file persistence.

    In-memory dict for fast access; persists to disk on upsert/delete so data
    survives server restarts. Replace internals with real lancedb table in production.
    """

    def __init__(self, path: str | Path = "data/lancedb") -> None:
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._rows: dict[str, dict[str, dict[str, Any]]] = {}  # project -> {id -> row}
        self._load_from_disk()

    def _project_file(self, project: str) -> Path:
        safe_name = project.replace("/", "_").replace("\\", "_")
        return self.path / f"{safe_name}.json"

    def _load_from_disk(self) -> None:
        """Load all persisted project data from disk on startup."""
        for file in self.path.glob("*.json"):
            project = file.stem
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                self._rows[project] = data
            except (json.JSONDecodeError, OSError):
                continue

    def reload(self, project: str) -> None:
        """Reload a single project's data from disk (after external reindex)."""
        file = self._project_file(project)
        if file.exists():
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                self._rows[project] = data
            except (json.JSONDecodeError, OSError):
                pass

    def _persist(self, project: str) -> None:
        """Write project data to disk."""
        rows = self._rows.get(project, {})
        self._project_file(project).write_text(
            json.dumps(rows, ensure_ascii=False), encoding="utf-8"
        )

    def _get_rows(self, project: str = "__default__") -> dict[str, dict[str, Any]]:
        return self._rows.setdefault(project, {})

    def upsert_chunks(
        self, chunks, embeddings: list[list[float]], project: str = "__default__"
    ) -> None:
        rows = self._get_rows(project)
        for chunk, vector in zip(chunks, embeddings):
            row = asdict(chunk)
            row["vector"] = vector
            # Use chunk_id as the row key
            row_id = row.get("chunk_id", row.get("id", ""))
            rows[row_id] = row
        self._persist(project)

    def delete_by_file(self, file_path: str, project: str = "__default__") -> int:
        """Remove all chunks belonging to a file. Returns count of removed rows."""
        rows = self._get_rows(project)
        to_remove = [rid for rid, row in rows.items() if row.get("file_path") == file_path]
        for rid in to_remove:
            del rows[rid]
        if to_remove:
            self._persist(project)
        return len(to_remove)

    def search(
        self, query_vector: list[float], top_k: int = 10, project: str = "__default__"
    ) -> list[dict[str, Any]]:
        rows = self._get_rows(project)
        scored = []
        for row in rows.values():
            score = self._cosine(query_vector, row["vector"])
            # Exclude vector from results to reduce response size
            result = {k: v for k, v in row.items() if k != "vector"}
            result["score"] = score
            scored.append(result)
        return sorted(scored, key=lambda r: r["score"], reverse=True)[:top_k]

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)) or 1.0
        nb = math.sqrt(sum(y * y for y in b)) or 1.0
        return dot / (na * nb)
