# controllers/learning_controller.py

from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QMessageBox, QWidget
from views.instruction_dialog import InstructionDialog
from views.recognizer_dialog import RecognizerDialog
import glob
import json
import os

class LearningController:
    def __init__(self):
        self.unlearnt_gestures = []
        self.load_gestures()

    def load_gestures(self):
        self.unlearnt_gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not data['learnt']:
                    self.unlearnt_gestures.append(data)

    def start_learning(self):
        self.load_gestures()
        if self.unlearnt_gestures:
            self.show_instruction(self.unlearnt_gestures[0])
        else:
            self.show_completion_message()

    def show_instruction(self, gesture):
        instruction_dialog = InstructionDialog(gesture)
        instruction_dialog.exec()
        self.start_recognition(gesture)

    def start_recognition(self, gesture):
        recognizer_dialog = RecognizerDialog(gesture)
        if recognizer_dialog.exec():
            self.load_gestures()  # Reload gestures to update status
            self.unlearnt_gestures.pop(0)  # Remove the learnt gesture
            self.start_learning()
        else:
            # If recognition is cancelled, do not proceed
            pass

    def show_completion_message(self):
        if all(g['mastered'] for g in self.unlearnt_gestures):
            QMessageBox.information(None, "Поздравляем!", "Вы выучили и освоили все жесты!")
        else:
            QMessageBox.information(None, "Поздравляем!", "Вы изучили все жесты! Пора их повторить!")
