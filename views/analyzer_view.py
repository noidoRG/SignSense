# views/analyzer_view.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QImage, QPixmap

class AnalyzerView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.result_label = QLabel("Нет жеста: 0%")
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

    def update_image(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def update_label(self, text):
        self.result_label.setText(text)
