import json
from dataclasses import asdict
from pathlib import Path
from intelligence_engine.scanner.file_state import FileState

class FileStateStore:
    def __init__(self, path: str | Path = "data/file_state/state.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, FileState]:
        if not self.path.exists():
            return {}
        text = self.path.read_text(encoding="utf-8").strip()
        if not text:
            return {}
        data = json.loads(text)
        return {k: FileState(**v) for k, v in data.items()}

    def save(self, states: list[FileState]) -> None:
        self.path.write_text(json.dumps({s.path: asdict(s) for s in states}, indent=2), encoding="utf-8")

    def diff(self, current: list[FileState]) -> tuple[list[FileState], list[str]]:
        """Compare current scan with stored state.

        Returns:
            (changed, deleted) where changed includes new + modified files,
            and deleted is a list of paths no longer present.
        """
        old = self.load()
        current_map = {s.path: s for s in current}
        changed = [s for s in current if s.path not in old or old[s.path].sha256 != s.sha256]
        deleted = [p for p in old if p not in current_map]
        return changed, deleted
