# views/learning_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import pyqtSignal
from views.instruction_dialog import InstructionDialog
from views.recognizer_dialog import RecognizerDialog
import glob
import json

class LearningView(QWidget):
    gesture_learnt = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.learn_gestures_button = QPushButton("Изучить жесты")
        self.learn_gestures_button.setToolTip("Изучить новые жесты")
        self.learn_gestures_button.clicked.connect(self.learn_gestures)

        self.review_gestures_button = QPushButton("Повторить жесты")
        self.review_gestures_button.setToolTip("Повторить изученные жесты")
        self.review_gestures_button.clicked.connect(self.review_gestures)

        self.layout.addWidget(self.learn_gestures_button)
        self.layout.addWidget(self.review_gestures_button)

    def learn_gestures(self):
        gestures = self.get_unlearnt_gestures()
        if not gestures:
            mastered_gestures = self.get_unmastered_gestures()
            if not mastered_gestures:
                self.show_message("Поздравляем! Вы выучили и освоили все жесты!")
            else:
                self.show_message("Вы изучили все жесты! Пора их повторить!")
            return

        for gesture in gestures:
            self.show_instruction(gesture)
            recognizer_dialog = RecognizerDialog(gesture)
            recognizer_dialog.gesture_learnt.connect(self.update_statistics)
            recognizer_dialog.exec()
            if recognizer_dialog.continue_pressed:
                continue
            else:
                break

    def review_gestures(self):
        pass  # Implement review gestures logic here

    def get_unlearnt_gestures(self):
        gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not data.get('learnt', False):
                    gestures.append(data)
        return gestures

    def get_unmastered_gestures(self):
        gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not data.get('mastered', False):
                    gestures.append(data)
        return gestures

    def show_instruction(self, gesture):
        dialog = InstructionDialog(gesture)
        dialog.exec()

    def update_statistics(self):
        self.gesture_learnt.emit()

    def show_message(self, message):
        dialog = QMessageBox()
        dialog.setWindowTitle("Сообщение")
        dialog.setText(message)
        dialog.exec()
