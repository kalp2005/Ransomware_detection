from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.logger import log

class FileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        log(f"Modified: {event.src_path}")
        self.callback("modified")

    def on_created(self, event):
        log(f"Created: {event.src_path}")
        self.callback("created")

def start_monitor(callback, path):
    observer = Observer()
    handler = FileHandler(callback)
    observer.schedule(handler, path=path, recursive=True)
    observer.start()
    return observer