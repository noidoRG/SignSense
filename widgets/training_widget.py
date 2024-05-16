from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget

class TrainingWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        self.themes_list = QListWidget()
        themes = ["Алфавит", "Счёт", "Времена года", "Семья", "Быт"]
        self.themes_list.addItems(themes)
        
        layout.addWidget(self.themes_list)
        self.setLayout(layout)
