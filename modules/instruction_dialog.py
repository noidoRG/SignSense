# modules/instruction_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
import os

class InstructionDialog(QDialog):
    def __init__(self, gesture):
        super().__init__()

        self.gesture = gesture
        self.setWindowTitle("Инструкция к жесту")
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image_label = QLabel()
        image_path = os.path.join("resources", "img", f"{gesture['gesture']}.jpg")
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.gesture_label = QLabel(gesture['gesture'])
        self.gesture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gesture_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.layout.addWidget(self.gesture_label)

        self.description_label = QLabel(gesture['description'])
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.description_label)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)
        self.layout.addLayout(self.button_layout)
