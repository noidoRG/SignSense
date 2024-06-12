# views/settings.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
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
        reply = QMessageBox.question(self, "Подтверждение сброса", "Вы уверены, что хотите сбросить данные об изученных жестах?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.reset_learnt_gestures()

    def confirm_reset_mastered(self):
        reply = QMessageBox.question(self, "Подтверждение сброса", "Вы уверены, что хотите сбросить данные об освоенных жестах?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
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
