from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatisticsModule(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        self.stats_label = QLabel("Здесь будут отображаться статистические данные пользователя")
        self.layout.addWidget(self.stats_label)
        
        self.setLayout(self.layout)
