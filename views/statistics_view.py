# views/statistics_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from controllers.statistics_controller import StatisticsController

class StatisticsView(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = StatisticsController()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.learnt_label = QLabel("Изучено жестов: 0/0")
        self.layout.addWidget(self.learnt_label)
        self.learnt_progress = QProgressBar()
        self.layout.addWidget(self.learnt_progress)

        self.mastered_label = QLabel("Освоено жестов: 0/0")
        self.layout.addWidget(self.mastered_label)
        self.mastered_progress = QProgressBar()
        self.layout.addWidget(self.mastered_progress)

        self.update_statistics()

    def update_statistics(self):
        stats = self.controller.get_statistics()

        learnt = stats["learnt"]
        mastered = stats["mastered"]
        total = stats["total"]

        self.learnt_label.setText(f"Изучено жестов: {learnt}/{total}")
        self.learnt_progress.setMaximum(total)
        self.learnt_progress.setValue(learnt)

        self.mastered_label.setText(f"Освоено жестов: {mastered}/{total}")
        self.mastered_progress.setMaximum(total)
        self.mastered_progress.setValue(mastered)
