from pathlib import Path
from dataclasses import dataclass
from watchdog.events import FileSystemEventHandler


@dataclass
class Watcher(FileSystemEventHandler):
    path: Path
    directory: str
    backends: object


w = Watcher(Path(), '', None)

w.on_any_event(None)
print(w)
