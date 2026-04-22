from PyQt5 import QtWidgets, QtCore
import subprocess

class Panel(QtWidgets.QWidget):
    def __init__(self, start_callback):
        super().__init__()

        self.start_callback = start_callback
        self.selected_folder = None

        self.setWindowTitle("Ransomware Defense System")
        self.setGeometry(100, 100, 600, 400)

        layout = QtWidgets.QVBoxLayout()

        # STATUS
        self.status = QtWidgets.QLabel("Status: SAFE")
        self.status.setStyleSheet("color: green; font-size: 18px;")
        layout.addWidget(self.status)

        # THREAT SCORE
        self.score = QtWidgets.QLabel("Threat Score: 0%")
        layout.addWidget(self.score)

        # SELECTED FOLDER DISPLAY
        self.folder_label = QtWidgets.QLabel("No folder selected")
        layout.addWidget(self.folder_label)

        # SELECT FOLDER BUTTON
        self.folder_btn = QtWidgets.QPushButton("Select Folder")
        self.folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_btn)

        # START BUTTON
        self.start_btn = QtWidgets.QPushButton("Start Monitoring")
        self.start_btn.clicked.connect(self.start)
        layout.addWidget(self.start_btn)

        # SIMULATION SECTION
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

        self.setLayout(layout)

    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder
            self.folder_label.setText(f"Monitoring: {folder}")

    def start(self):
        if not self.selected_folder:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a folder first!")
            return

        self.start_callback(self.selected_folder)

    def run_attack(self, attack_type):
        if not self.selected_folder:
            QtWidgets.QMessageBox.warning(self, "Error", "Select folder first!")
            return

        subprocess.Popen([
            "python",
            "simulate_attack.py",
            self.selected_folder,
            attack_type
        ])

    def update_status(self, text, color):
        self.status.setText(text)
        self.status.setStyleSheet(f"color: {color}; font-size: 18px;")

    def update_score(self, score):
        self.score.setText(f"Threat Score: {int(score * 100)}%")

    def show_permission(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Permission",
            "Threat detected! Block it?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        return reply == QtWidgets.QMessageBox.Yes