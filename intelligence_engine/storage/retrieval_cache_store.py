"""Retrieval Cache Store — avoid repeated retrieval work (architecture section 4.6).

Cache key: project + intent + query + symbol
TTL-based expiration to invalidate stale results.

Schema per entry:
{
    "cache_key": "business-lounge-api:refactor:ServiceProviderId",
    "project": "business-lounge-api",
    "intent": "refactor",
    "query": "Rename ServiceProviderId to ProviderId",
    "result": { ... },
    "created_at": "2026-06-03T10:10:00Z",
    "expires_at": "2026-06-03T10:40:00Z"
}
"""

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


class RetrievalCacheStore:
    """In-memory + disk-persisted retrieval cache with TTL."""

    DEFAULT_TTL_MINUTES = 30

    def __init__(self, base_dir: str | Path = "data/retrieval_cache") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, dict[str, Any]] = {}
        self._load_from_disk()

    def _cache_file(self) -> Path:
        return self.base_dir / "cache.json"

    def _load_from_disk(self) -> None:
        path = self._cache_file()
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._cache = data
        except (json.JSONDecodeError, OSError):
            self._cache = {}

    def _persist(self) -> None:
        self._cache_file().write_text(
            json.dumps(self._cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @staticmethod
    def _make_key(project: str, intent: str, query: str, symbol: str = "") -> str:
        """Generate cache key from project + intent + query + symbol."""
        raw = f"{project}:{intent}:{query}:{symbol}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def get(
        self, project: str, intent: str, query: str, symbol: str = ""
    ) -> dict[str, Any] | None:
        """Get cached result if it exists and is not expired."""
        key = self._make_key(project, intent, query, symbol)
        entry = self._cache.get(key)
        if not entry:
            return None
        expires_at = datetime.fromisoformat(entry["expires_at"])
        if datetime.now(timezone.utc) > expires_at:
            del self._cache[key]
            self._persist()
            return None
        return entry.get("result")

    def put(
        self,
        project: str,
        intent: str,
        query: str,
        result: dict[str, Any],
        symbol: str = "",
        ttl_minutes: int | None = None,
    ) -> None:
        """Store a retrieval result in the cache."""
        key = self._make_key(project, intent, query, symbol)
        ttl = ttl_minutes or self.DEFAULT_TTL_MINUTES
        now = datetime.now(timezone.utc)
        self._cache[key] = {
            "cache_key": f"{project}:{intent}:{symbol or query[:50]}",
            "project": project,
            "intent": intent,
            "query": query,
            "symbol": symbol,
            "result": result,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(minutes=ttl)).isoformat(),
        }
        self._persist()

    def invalidate_project(self, project: str) -> int:
        """Invalidate all cache entries for a project (e.g. after reindex)."""
        to_remove = [k for k, v in self._cache.items() if v.get("project") == project]
        for k in to_remove:
            del self._cache[k]
        if to_remove:
            self._persist()
        return len(to_remove)

    def clear(self) -> None:
        """Clear entire cache."""
        self._cache = {}
        self._persist()
