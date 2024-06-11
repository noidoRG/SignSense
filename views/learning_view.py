# views/learning_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QSize, Qt
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

        self.button_text_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.learn_gestures_button = QPushButton(" Изучить жесты")
        self.learn_gestures_button.setObjectName("learn_gestures_button")
        self.learn_gestures_button.setToolTip("Изучить новые жесты")
        self.learn_gestures_button.setIcon(QIcon("./resources/icons/Learn.svg"))
        self.learn_gestures_button.setIconSize(QSize(32, 32))
        self.learn_gestures_button.clicked.connect(self.learn_gestures)

        self.review_gestures_button = QPushButton(" Повторить жесты")
        self.review_gestures_button.setObjectName("review_gestures_button")
        self.review_gestures_button.setToolTip("Повторить изученные жесты")
        self.review_gestures_button.setIcon(QIcon("./resources/icons/Review.svg"))
        self.review_gestures_button.setIconSize(QSize(32, 32))
        self.review_gestures_button.clicked.connect(self.review_gestures)

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.learn_gestures_button)
        self.button_layout.addSpacing(20)
        self.button_layout.addWidget(self.review_gestures_button)
        self.button_layout.addStretch(1)

        self.layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.layout.addLayout(self.button_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum))

        self.text_layout = QHBoxLayout()
        self.instruction_label = QLabel("Просмотр инструкции к жесту и оценивание демонстрируемого жеста")
        self.instruction_label.setObjectName("instruction_label")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setWordWrap(True)

        self.review_label = QLabel("Повторная оценка жестов, которые были изучены")
        self.review_label.setObjectName("review_label")
        self.review_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.review_label.setWordWrap(True)

        self.text_layout.addStretch(1)
        self.text_layout.addWidget(self.instruction_label)
        self.text_layout.addSpacing(40)
        self.text_layout.addWidget(self.review_label)
        self.text_layout.addStretch(1)

        self.button_text_layout.addLayout(self.button_layout)
        self.button_text_layout.addLayout(self.text_layout)
        self.layout.addLayout(self.button_text_layout)

        self.layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

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
        dialog.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        dialog.setText(message)
        dialog.exec()
