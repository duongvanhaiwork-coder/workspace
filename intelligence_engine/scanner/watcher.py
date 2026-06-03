from pathlib import Path
from typing import Callable
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ChangeHandler(FileSystemEventHandler):
    def __init__(
        self,
        on_change: Callable[[Path], None],
        on_delete: Callable[[Path], None] | None = None,
    ):
        self.on_change = on_change
        self.on_delete = on_delete

    def on_modified(self, event):
        if not event.is_directory:
            self.on_change(Path(event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            self.on_change(Path(event.src_path))

    def on_deleted(self, event):
        if not event.is_directory and self.on_delete:
            self.on_delete(Path(event.src_path))


class Watcher:
    def __init__(
        self,
        root: Path,
        on_change: Callable[[Path], None],
        on_delete: Callable[[Path], None] | None = None,
    ):
        self.root = Path(root)
        self.observer = Observer()
        self.handler = ChangeHandler(on_change, on_delete)

    def start(self) -> None:
        self.observer.schedule(self.handler, str(self.root), recursive=True)
        self.observer.start()

    def stop(self) -> None:
        self.observer.stop()
        self.observer.join()
