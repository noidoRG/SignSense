# views/settings_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from controllers.settings_controller import SettingsController

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = SettingsController()

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

    def reset_learnt_gestures(self):
        self.controller.reset_learnt_gestures()
        QMessageBox.information(self, "Сброс данных", "Данные об изученных жестах сброшены.")

    def reset_mastered_gestures(self):
        self.controller.reset_mastered_gestures()
        QMessageBox.information(self, "Сброс данных", "Данные об освоенных жестах сброшены.")
