# modules/statistics.py

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QProgressBar, QSizePolicy
from PyQt6.QtCore import Qt
import glob
import json

class Statistics(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(20)

        self.learnt_label = QLabel()
        self.learnt_label.setObjectName("stat_label")
        self.learnt_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.learnt_progress = QProgressBar()
        self.learnt_progress.setObjectName("stat_progress")
        # self.learnt_progress.setTextVisible(False)
        self.learnt_progress.setFixedHeight(20)  # Установим фиксированную высоту
        self.learnt_progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.mastered_label = QLabel()
        self.mastered_label.setObjectName("stat_label")
        self.mastered_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.mastered_progress = QProgressBar()
        self.mastered_progress.setObjectName("stat_progress")
        # self.mastered_progress.setTextVisible(False)
        self.mastered_progress.setFixedHeight(20)  # Установим фиксированную высоту
        self.mastered_progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Добавляем элементы в сетку
        self.main_layout.addWidget(self.learnt_label, 0, 0)
        self.main_layout.addWidget(self.learnt_progress, 0, 1)
        self.main_layout.addWidget(self.mastered_label, 1, 0)
        self.main_layout.addWidget(self.mastered_progress, 1, 1)

        self.setLayout(self.main_layout)

        self.update_statistics()

    def update_statistics(self):
        learnt_count = 0
        mastered_count = 0
        total_count = len(glob.glob("data/*.json"))

        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('learnt'):
                    learnt_count += 1
                if data.get('mastered'):
                    mastered_count += 1

        self.learnt_label.setText(f"Изучено жестов: {learnt_count}/{total_count}")
        self.learnt_progress.setMaximum(total_count)
        self.learnt_progress.setValue(learnt_count)

        self.mastered_label.setText(f"Освоено жестов: {mastered_count}/{total_count}")
        self.mastered_progress.setMaximum(total_count)
        self.mastered_progress.setValue(mastered_count)
