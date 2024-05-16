from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SandboxWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        self.camera_label = QLabel("Камера")
        self.result_label = QLabel("Результат: ")
        
        layout.addWidget(self.camera_label)
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)
