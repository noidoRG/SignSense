from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget

class DictionaryModule(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск...")
        
        self.gestures_list = QListWidget()
        
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.gestures_list)
        
        self.setLayout(self.layout)
