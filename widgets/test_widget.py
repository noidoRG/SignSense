from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        self.gesture_label = QLabel("Покажите жест")
        self.timer_label = QLabel("Время: 10 сек")
        
        layout.addWidget(self.gesture_label)
        layout.addWidget(self.timer_label)
        
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 10
    
    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Время: {self.time_left} сек")
        if self.time_left == 0:
            self.timer.stop()
