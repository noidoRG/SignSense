# views/dictionary_view.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class DictionaryView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Dictionary Module")
        self.some_button = QPushButton("Click me")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.some_button)
        self.setLayout(self.layout)

    def update(self, data):
        self.label.setText(data)
