# views/dictionary_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QScrollArea, QDialog, QDialogButtonBox, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
import glob
import json

class DictionaryView(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)
        self.load_gestures()

    def load_gestures(self):
        row = 0
        col = 0
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gesture_card = self.create_gesture_card(data)
                self.scroll_layout.addWidget(gesture_card, row, col)
                col += 1
                if col > 2:  # 3 cards per row
                    col = 0
                    row += 1

    def create_gesture_card(self, gesture):
        card = QPushButton()
        card.setObjectName("gesture_card")
        card.setStyleSheet("""

        """)

        card_layout = QVBoxLayout(card)

        name_label = QLabel(gesture['gesture'])
        name_label.setObjectName("mini_card_name")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_label)

        card.clicked.connect(lambda _, g=gesture: self.show_gesture_details(g))

        return card

    def show_gesture_details(self, gesture):
        dialog = GestureDetailsDialog(gesture)
        dialog.exec()

class GestureDetailsDialog(QDialog):

    def __init__(self, gesture):
        super().__init__()
        self.setWindowTitle(gesture['gesture'])
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        self.setLayout(QVBoxLayout())

        self.gesture = gesture

        image_label = QLabel()
        image_path = f"./resources/img/{gesture['gesture']}.jpg"
        pixmap = QPixmap(image_path).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(image_label)

        name_label = QLabel(gesture['gesture'])
        name_label.setObjectName("mini_card_name")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(name_label)

        description_label = QLabel(gesture['description'])
        description_label.setWordWrap(True)
        description_label.setFont(QFont("Rubik", 12))
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(description_label)


        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        self.layout().addWidget(buttons)