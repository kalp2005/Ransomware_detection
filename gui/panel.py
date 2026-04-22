from PyQt5 import QtWidgets
import subprocess
import os

class Panel(QtWidgets.QWidget):
    def __init__(self, start_callback, stop_callback):
        super().__init__()

        self.start_callback = start_callback
        self.stop_callback = stop_callback

        self.selected_folder = None
        self.is_running = False

        self.setWindowTitle("Ransomware Defense System")
        self.setGeometry(100, 100, 600, 500)

        layout = QtWidgets.QVBoxLayout()

        # STATUS
        self.status = QtWidgets.QLabel("Status: SAFE")
        self.status.setStyleSheet("color: green; font-size: 18px;")
        layout.addWidget(self.status)

        # SCORE
        self.score = QtWidgets.QLabel("Threat Score: 0%")
        layout.addWidget(self.score)

        # FOLDER
        self.folder_label = QtWidgets.QLabel("No folder selected")
        layout.addWidget(self.folder_label)

        self.folder_btn = QtWidgets.QPushButton("Select Folder")
        self.folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_btn)

        # START / STOP
        self.start_btn = QtWidgets.QPushButton("Start Monitoring")
        self.start_btn.clicked.connect(self.toggle_monitoring)
        layout.addWidget(self.start_btn)

        # SAFE ACTIONS
        layout.addWidget(QtWidgets.QLabel("Safe Actions"))

        self.single_create = QtWidgets.QPushButton("Create 1 File")
        self.single_create.clicked.connect(self.create_single)
        layout.addWidget(self.single_create)

        self.single_delete = QtWidgets.QPushButton("Delete 1 File")
        self.single_delete.clicked.connect(self.delete_single)
        layout.addWidget(self.single_delete)

        # ATTACK SIMULATION
        layout.addWidget(QtWidgets.QLabel("Attack Simulation"))

        self.create_btn = QtWidgets.QPushButton("Mass File Creation")
        self.create_btn.clicked.connect(lambda: self.run_attack("create"))
        layout.addWidget(self.create_btn)

        self.delete_btn = QtWidgets.QPushButton("Mass File Deletion")
        self.delete_btn.clicked.connect(lambda: self.run_attack("delete"))
        layout.addWidget(self.delete_btn)

        self.encrypt_btn = QtWidgets.QPushButton("Encryption Simulation")
        self.encrypt_btn.clicked.connect(lambda: self.run_attack("encrypt"))
        layout.addWidget(self.encrypt_btn)

        # 🔒 Disable buttons initially
        self.set_simulation_enabled(False)

        self.setLayout(layout)

    # 🔥 Enable/Disable simulation controls
    def set_simulation_enabled(self, enabled):
        self.single_create.setEnabled(enabled)
        self.single_delete.setEnabled(enabled)
        self.create_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
        self.encrypt_btn.setEnabled(enabled)

    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(f"Monitoring: {folder}")

    def toggle_monitoring(self):
        if not self.is_running:
            if not self.selected_folder:
                QtWidgets.QMessageBox.warning(self, "Error", "Select folder first!")
                return

            self.start_callback(self.selected_folder)
            self.start_btn.setText("Stop Monitoring")
            self.is_running = True

            # ✅ Enable simulation when running
            self.set_simulation_enabled(True)

        else:
            self.stop_callback()
            self.start_btn.setText("Start Monitoring")
            self.is_running = False
            self.update_status("STOPPED", "orange")

            # ❌ Disable again
            self.set_simulation_enabled(False)

    def run_attack(self, attack_type):
        if not self.is_running:
            QtWidgets.QMessageBox.warning(self, "Error", "Start monitoring first!")
            return

        subprocess.Popen([
            "python",
            "simulate_attack.py",
            self.selected_folder,
            attack_type
        ])

    def create_single(self):
        if not self.is_running:
            return

        path = os.path.join(self.selected_folder, "safe_file.txt")
        with open(path, "w") as f:
            f.write("safe")

    def delete_single(self):
        if not self.is_running:
            return

        files = os.listdir(self.selected_folder)
        if files:
            os.remove(os.path.join(self.selected_folder, files[0]))

    def update_status(self, text, color):
        self.status.setText(text)
        self.status.setStyleSheet(f"color: {color}; font-size: 18px;")

    def update_score(self, score):
        self.score.setText(f"Threat Score: {int(score * 100)}%")

    def show_permission(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Security Alert")
        msg.setText("Suspicious activity detected!")
        msg.setInformativeText("Do you want to BLOCK this activity?")

        block_btn = msg.addButton("Block", QtWidgets.QMessageBox.AcceptRole)
        allow_btn = msg.addButton("Allow", QtWidgets.QMessageBox.RejectRole)

        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()

        return msg.clickedButton() == block_btn