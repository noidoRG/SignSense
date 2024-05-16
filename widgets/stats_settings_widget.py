from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QSpinBox

class StatsSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        stats_layout = QFormLayout()
        self.total_gestures_label = QLabel("Всего жестов: 0")
        self.best_gesture_label = QLabel("Лучший жест: None")
        
        stats_layout.addRow("Всего жестов:", self.total_gestures_label)
        stats_layout.addRow("Лучший жест:", self.best_gesture_label)
        
        settings_layout = QFormLayout()
        self.similarity_threshold_spinbox = QSpinBox()
        self.similarity_threshold_spinbox.setRange(50, 100)
        self.similarity_threshold_spinbox.setValue(70)
        
        settings_layout.addRow("Порог сходства (%):", self.similarity_threshold_spinbox)
        
        layout.addLayout(stats_layout)
        layout.addLayout(settings_layout)
        
        self.setLayout(layout)
