# views/analyzer_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap

class AnalyzerView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.video_label = QLabel()
        self.gesture_label = QLabel()
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.gesture_label)
        self.setLayout(self.layout)

    def update_frame(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    def update_gesture(self, gesture):
        self.gesture_label.setText(f"Распознанный жест: {gesture}")
