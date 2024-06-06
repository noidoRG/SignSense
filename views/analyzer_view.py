# views/analyzer_view.py

import cv2
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from controllers.analyzer_controller import AnalyzerController

class AnalyzerView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.result_label = QLabel("Нет жеста")
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

        self.controller = AnalyzerController()

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame_flipped = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)

        results = self.controller.process_frame(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture, confidence = self.controller.analyze_gesture(hand_landmarks.landmark)
                text = f"{gesture} ({confidence:.2f}%)" if confidence > 0 else gesture
                self.result_label.setText(text)
                
        else:
            self.result_label.setText("Нет жеста")

        height, width, channel = frame_flipped.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame_flipped.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)
