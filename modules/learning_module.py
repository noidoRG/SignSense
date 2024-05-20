from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QPushButton

class LearningModule(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        self.stacked_widget = QStackedWidget()
        
        self.new_gestures_widget = QWidget()
        self.repeat_gestures_widget = QWidget()
        
        self.stacked_widget.addWidget(self.new_gestures_widget)
        self.stacked_widget.addWidget(self.repeat_gestures_widget)
        
        self.layout.addWidget(self.stacked_widget)
        
        self.init_new_gestures()
        self.init_repeat_gestures()
        
        self.setLayout(self.layout)
        
    def init_new_gestures(self):
        layout = QVBoxLayout()
        
        instruction_label = QLabel("Инструкция по новым жестам...")
        next_button = QPushButton("Следующий жест")
        
        layout.addWidget(instruction_label)
        layout.addWidget(next_button)
        
        self.new_gestures_widget.setLayout(layout)

    def init_repeat_gestures(self):
        layout = QVBoxLayout()
        
        instruction_label = QLabel("Повторение изученных жестов...")
        next_button = QPushButton("Следующий жест")
        
        layout.addWidget(instruction_label)
        layout.addWidget(next_button)
        
        self.repeat_gestures_widget.setLayout(layout)
