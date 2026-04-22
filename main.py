import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from monitor.file_monitor import start_monitor
from response.action import take_action
from gui.panel import Panel

# Counters
created_count = 0
deleted_count = 0
encrypted_count = 0


def event_callback(event_type, path):
    global created_count, deleted_count, encrypted_count

    if event_type == "created":
        created_count += 1

        if path.endswith(".enc"):
            encrypted_count += 1

    elif event_type == "deleted":
        deleted_count += 1


class Controller:
    def __init__(self, panel):
        self.panel = panel
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loop)

    def start(self, folder):
        self.observer = start_monitor(event_callback, folder)
        self.timer.start(2000)

    def loop(self):
        global created_count, deleted_count, encrypted_count

        threat = None
        score = 0

        # 🔴 Mass Deletion
        if deleted_count >= 100:
            threat = "Mass Deletion Detected"
            score = 0.9

        # 🟣 Encryption
        elif encrypted_count >= 5:
            threat = "Encryption Activity Detected"
            score = 0.8

        # 🟡 Mass Creation
        elif created_count >= 20:
            threat = "Mass File Creation Detected"
            score = 0.6

        # Update UI
        self.panel.update_score(score)

        if threat:
            self.panel.update_status(threat, "red")

            allow_block = self.panel.show_permission()

            if allow_block:
                take_action()
        else:
            self.panel.update_status("SAFE", "green")

        # RESET COUNTS every cycle
        created_count = 0
        deleted_count = 0
        encrypted_count = 0


app = QApplication(sys.argv)

panel = Panel(None)
controller = Controller(panel)

panel.start_callback = controller.start

panel.show()
sys.exit(app.exec_())