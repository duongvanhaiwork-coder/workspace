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
        return {k: FileState(**v) for k, v in data.items()}

    def save(self, states: list[FileState], project: str = "__default__") -> None:
        self._project_path(project).write_text(
            json.dumps({s.path: asdict(s) for s in states}, indent=2), encoding="utf-8"
        )

    def diff(self, current: list[FileState], project: str = "__default__") -> tuple[list[FileState], list[str]]:
        """Compare current scan with stored state.

        Returns:
            (changed, deleted) where changed includes new + modified files,
            and deleted is a list of paths no longer present.
        """
        old = self.load(project)
        current_map = {s.path: s for s in current}
        changed = [s for s in current if s.path not in old or old[s.path].sha256 != s.sha256]
        deleted = [p for p in old if p not in current_map]
        return changed, deleted
