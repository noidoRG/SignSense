from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class StatisticsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Statistics Module")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
