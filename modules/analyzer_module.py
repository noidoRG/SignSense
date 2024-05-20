from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
import cv2
import mediapipe as mp

class AnalyzerModule(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("content")
        
        self.layout = QVBoxLayout()
        
        self.instruction_label = QLabel("Покажите жест...")
        self.layout.addWidget(self.instruction_label)
        
        self.setLayout(self.layout)
        
        self.capture = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    
    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        
        self.display_image(frame)
    
    def display_image(self, img):
        qformat = QImage.Format.Format_RGB888
        out_image = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
        out_image = out_image.rgbSwapped()
        self.instruction_label.setPixmap(QPixmap.fromImage(out_image))
