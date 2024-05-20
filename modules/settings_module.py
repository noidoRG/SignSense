from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QCheckBox

class SettingsModule(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        self.num_new_gestures_label = QLabel("Число жестов в уроке на изучение:")
        self.num_new_gestures = QSpinBox()
        self.num_new_gestures.setValue(3)
        
        self.num_repeat_gestures_label = QLabel("Число жестов в уроке на повторение:")
        self.num_repeat_gestures = QSpinBox()
        self.num_repeat_gestures.setValue(10)
        
        self.num_repeats_label = QLabel("Число повторений одного жеста в уроке:")
        self.num_repeats = QSpinBox()
        self.num_repeats.setValue(3)
        
        self.dark_mode_checkbox = QCheckBox("Ночной режим")
        
        self.layout.addWidget(self.num_new_gestures_label)
        self.layout.addWidget(self.num_new_gestures)
        self.layout.addWidget(self.num_repeat_gestures_label)
        self.layout.addWidget(self.num_repeat_gestures)
        self.layout.addWidget(self.num_repeats_label)
        self.layout.addWidget(self.num_repeats)
        self.layout.addWidget(self.dark_mode_checkbox)
        
        self.setLayout(self.layout)
