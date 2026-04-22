import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from monitor.file_monitor import start_monitor
from monitor.process_monitor import check_process
from ml.model import train_model
from ml.predictor import predict
from response.action import take_action
from gui.panel import Panel

model = train_model()
file_events = 0


def event_callback(event):
    global file_events
    file_events += 1


class Controller:
    def __init__(self, panel):
        self.panel = panel
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loop)

    def start(self, folder):
        self.observer = start_monitor(event_callback, folder)
        self.timer.start(3000)

    def loop(self):
        global file_events

        cpu_flag = check_process()
        features = [file_events, cpu_flag]

        threat_score = predict(model, features)

        self.panel.update_score(threat_score)

        if threat_score > 0.6:
            self.panel.update_status("THREAT DETECTED", "red")

            if self.panel.show_permission():
                take_action()
        else:
            self.panel.update_status("SAFE", "green")

        file_events = 0


app = QApplication(sys.argv)

panel = Panel(None)
controller = Controller(panel)

panel.start_callback = controller.start

panel.show()
sys.exit(app.exec_())