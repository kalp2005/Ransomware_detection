from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            self.callback("created", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.callback("deleted", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.callback("modified", event.src_path)


def start_monitor(callback, path):
    observer = Observer()
    handler = FileHandler(callback)
    observer.schedule(handler, path=path, recursive=True)
    observer.start()
    return observer