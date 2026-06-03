import json
from dataclasses import asdict
from pathlib import Path
from intelligence_engine.scanner.file_state import FileState


class FileStateStore:
    """Per-project file state persistence."""

    def __init__(self, base_dir: str | Path = "data/file_state") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _project_path(self, project: str) -> Path:
        safe_name = project.replace("/", "_").replace("\\", "_")
        return self.base_dir / f"{safe_name}.json"

    def load(self, project: str = "__default__") -> dict[str, FileState]:
        path = self._project_path(project)
        if not path.exists():
            return {}
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return {}
        data = json.loads(text)
        result = {}
        for k, v in data.items():
            # Remove project field (stored for reference but not part of FileState)
            v_copy = {key: val for key, val in v.items() if key != "project"}
            # Handle both old format (path/sha256/size)
            # and new format (file_path/content_hash/size_bytes)
            if "file_path" in v_copy:
                result[k] = FileState(**v_copy)
            else:
                # Migrate old format
                result[k] = FileState(
                    file_path=v_copy.get("path", k),
                    content_hash=v_copy.get("sha256", v_copy.get("content_hash", "")),
                    size_bytes=v_copy.get("size", v_copy.get("size_bytes", 0)),
                    language=v_copy.get("language", ""),
                    absolute_path=v_copy.get("absolute_path", ""),
                    last_modified_at=v_copy.get("last_modified_at", ""),
                    last_indexed_at=v_copy.get("last_indexed_at", ""),
                    status=v_copy.get("status", "indexed"),
                )
        return result

    def save(self, states: list[FileState], project: str = "__default__") -> None:
        data = {}
        for s in states:
            entry = asdict(s)
            entry["project"] = project
            data[s.file_path] = entry
        self._project_path(project).write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )

    def diff(
        self, current: list[FileState], project: str = "__default__",
    ) -> tuple[list[FileState], list[str]]:
        """Compare current scan with stored state.

        Returns:
            (changed, deleted) where changed includes new + modified files,
            and deleted is a list of paths no longer present.
        """
        old = self.load(project)
        current_map = {s.file_path: s for s in current}
        changed = [
            s for s in current
            if s.file_path not in old
            or old[s.file_path].content_hash != s.content_hash
        ]
        deleted = [p for p in old if p not in current_map]
        return changed, deleted
