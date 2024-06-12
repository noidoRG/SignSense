# modules/settings.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon
import json
import glob

class Settings(QWidget):
    learnt_reset = pyqtSignal()
    mastered_reset = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.reset_learnt_button = QPushButton("Сбросить данные об изученных жестах")
        self.reset_learnt_button.clicked.connect(self.confirm_reset_learnt)
        self.layout.addWidget(self.reset_learnt_button)

        self.reset_mastered_button = QPushButton("Сбросить данные об освоенных жестах")
        self.reset_mastered_button.clicked.connect(self.confirm_reset_mastered)
        self.layout.addWidget(self.reset_mastered_button)


    def confirm_reset_learnt(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтверждение сброса")
        msg_box.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        msg_box.setText("Вы уверены, что хотите сбросить данные об изученных жестах?")
        
        yes_button = QPushButton("Да")
        yes_button.setObjectName("yes_button")
        no_button = QPushButton("Нет")
        no_button.setObjectName("no_button")
        
        msg_box.addButton(yes_button, QMessageBox.ButtonRole.YesRole)
        msg_box.addButton(no_button, QMessageBox.ButtonRole.NoRole)
        
        reply = msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            self.reset_learnt_gestures()

    def confirm_reset_mastered(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтверждение сброса")
        msg_box.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        msg_box.setText("Вы уверены, что хотите сбросить данные об освоенных жестах?")
        
        yes_button = QPushButton("Да")
        no_button = QPushButton("Нет")
        
        msg_box.addButton(yes_button, QMessageBox.ButtonRole.YesRole)
        msg_box.addButton(no_button, QMessageBox.ButtonRole.NoRole)
        
        reply = msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            self.reset_mastered_gestures()

# Работа с JSON
    def reset_learnt_gestures(self):
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['learnt'] = False
                data['mastered'] = False
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
        self.learnt_reset.emit()
        QMessageBox.information(self, "Сброс данных", "Данные об изученных жестах сброшены.")


    def reset_mastered_gestures(self):
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['mastered'] = False
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
        self.mastered_reset.emit()
        QMessageBox.information(self, "Сброс данных", "Данные об освоенных жестах сброшены.")
