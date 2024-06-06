# views/dictionary_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QDialog, QDialogButtonBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from controllers.dictionary_controller import DictionaryController

class GestureDialog(QDialog):
    def __init__(self, gesture):
        super().__init__()
        self.setWindowTitle(gesture['gesture'])
        
        layout = QVBoxLayout()

        # Image
        image_path = f"resources/img/{gesture['gesture']}.jpg"
        image_label = QLabel()
        image_label.setObjectName("gesture_image")
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Gesture name
        name_label = QLabel(gesture['gesture'])
        name_label.setObjectName("gesture_name")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        # Gesture description
        description_label = QLabel(gesture['description'])
        description_label.setObjectName("gesture_description")
        description_label.setWordWrap(True)  # Enable word wrap
        layout.addWidget(description_label)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setObjectName("ok_button")
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)

class DictionaryView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.controller = DictionaryController()

        self.gesture_list = QListWidget()
        self.gesture_list.setIconSize(QSize(64, 64))
        self.gesture_list.itemClicked.connect(self.show_gesture_dialog)

        self.layout.addWidget(self.gesture_list)

        self.load_gestures()

    def load_gestures(self):
        gestures = self.controller.get_gestures()
        for gesture in gestures:
            item = QListWidgetItem(gesture['gesture'])
            item.setIcon(QIcon(f"resources/img/{gesture['gesture']}.jpg"))
            item.setData(1, gesture)  # Store the gesture data in the item
            self.gesture_list.addItem(item)

    def show_gesture_dialog(self, item):
        gesture = item.data(1)
        dialog = GestureDialog(gesture)
        dialog.exec()
