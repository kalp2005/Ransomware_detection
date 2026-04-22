import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from monitor.file_monitor import start_monitor
from gui.panel import Panel
from utils.backup import create_backup, restore_backup

events = []
current_folder = None


def event_callback(event_type, path):
    global events

    events.append({
        "type": event_type,
        "path": path,
        "time": time.time()
    })


class Controller:
    def __init__(self, panel):
        self.panel = panel
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loop)
        self.observer = None

    def start(self, folder):
        global current_folder

        if self.observer:
            return

        current_folder = folder

        # 🔥 INITIAL SNAPSHOT
        create_backup(folder)

        self.observer = start_monitor(event_callback, folder)
        self.timer.start(2000)

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

        self.timer.stop()

    def rollback(self):
        global current_folder

        if current_folder:
            restore_backup(current_folder)

    def update_snapshot(self):
        global current_folder

        if current_folder:
            create_backup(current_folder)

    def loop(self):
        global events

        current_time = time.time()

        events = [e for e in events if current_time - e["time"] <= 5]

        created = sum(1 for e in events if e["type"] == "created")
        deleted = sum(1 for e in events if e["type"] == "deleted")
        encrypted = sum(1 for e in events if e["path"].endswith(".enc"))

        threat = None
        score = 0

        if deleted >= 100:
            threat = f"Mass Deletion ({deleted})"
            score = 0.95
        elif encrypted >= 5:
            threat = f"Encryption Activity ({encrypted})"
            score = 0.85
        elif created >= 20:
            threat = f"Mass Creation ({created})"
            score = 0.7

        self.panel.update_score(score)

        if threat:
            self.panel.update_status(threat, "red")

            block = self.panel.show_permission()

            if block:
                # ❌ BLOCK → RESTORE
                self.rollback()
                self.panel.update_status("System Restored (Blocked)", "orange")

            else:
                # ✅ ALLOW → UPDATE SNAPSHOT
                self.update_snapshot()
                self.panel.update_status("Allowed & Snapshot Updated", "blue")

            # clear events after decision
            events = []

        else:
            self.panel.update_status("SAFE", "green")


app = QApplication(sys.argv)

panel = Panel(None, None)
controller = Controller(panel)

panel.start_callback = controller.start
panel.stop_callback = controller.stop

panel.show()
sys.exit(app.exec_())