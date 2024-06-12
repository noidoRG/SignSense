# modules/statistics.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
import glob
import json

class Statistics(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.learnt_label = QLabel()
        self.learnt_progress = QProgressBar()
        self.mastered_label = QLabel()
        self.mastered_progress = QProgressBar()

        self.layout.addWidget(self.learnt_label)
        self.layout.addWidget(self.learnt_progress)
        self.layout.addWidget(self.mastered_label)
        self.layout.addWidget(self.mastered_progress)

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
