from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class TranslatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        self.camera_label = QLabel("Камера")
        self.text_field = QTextEdit()
        
        layout.addWidget(self.camera_label)
        layout.addWidget(self.text_field)
        
        self.setLayout(layout)
