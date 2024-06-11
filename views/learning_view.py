# views/learning_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import pyqtSignal
from views.instruction_dialog import InstructionDialog
from views.recognizer_dialog import RecognizerDialog
import glob
import json

class LearningView(QWidget):
    gesture_learnt = pyqtSignal()
    gesture_mastered = pyqtSignal()

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
            mastered_gestures = self.get_learnt_but_unmastered_gestures()
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
            recognizer_dialog.stop_video()  # Ensure video stops before next iteration
            if recognizer_dialog.continue_pressed:
                continue
            else:
                break

    def review_gestures(self):
        learnt_gestures = self.get_learnt_gestures()
        if not learnt_gestures:
            self.show_message("Нет изученных жестов.")
            return

        gestures = self.get_learnt_but_unmastered_gestures()
        if not gestures:
            if self.get_mastered_gestures_count() == self.get_total_gestures_count():
                self.show_message("Поздравляем! Вы освоили все жесты!")
            else:
                self.show_message("Вы освоили все изученные жесты! Так держать!")
            return

        for gesture in gestures:
            recognizer_dialog = RecognizerDialog(gesture, mode='master')
            recognizer_dialog.gesture_mastered.connect(self.update_statistics)
            recognizer_dialog.exec()
            recognizer_dialog.stop_video()  # Ensure video stops before next iteration
            if recognizer_dialog.continue_pressed:
                continue
            else:
                break

    def get_unlearnt_gestures(self):
        gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not data.get('learnt', False):
                    gestures.append(data)
        return gestures

    def get_learnt_gestures(self):
        gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('learnt', False):
                    gestures.append(data)
        return gestures

    def get_learnt_but_unmastered_gestures(self):
        gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('learnt', False) and not data.get('mastered', False):
                    gestures.append(data)
        return gestures

    def get_mastered_gestures_count(self):
        count = 0
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('mastered', False):
                    count += 1
        return count

    def get_total_gestures_count(self):
        return len(glob.glob("data/*.json"))

    def show_instruction(self, gesture):
        dialog = InstructionDialog(gesture)
        dialog.exec()

    def update_statistics(self):
        self.gesture_learnt.emit()
        self.gesture_mastered.emit()

    def show_message(self, message):
        dialog = QMessageBox()
        dialog.setWindowTitle("Сообщение")
        dialog.setText(message)
        dialog.exec()
