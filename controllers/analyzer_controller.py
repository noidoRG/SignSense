# controllers/analyzer_controller.py

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
import numpy as np
from views.analyzer_view import AnalyzerView

class AnalyzerController:
    def __init__(self):
        self.view = AnalyzerView()
        
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
        # Initialize Hand Tracking module from MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.thumb_up_reference = [
            (0.5, 0.2),  # Base of the thumb
            (0.5, 0.1),  # Tip of the thumb
            (0.3, 0.3),  # Tip of the index finger
            (0.3, 0.5),  # Tip of the middle finger
            (0.3, 0.7),  # Tip of the ring finger
            (0.3, 0.9)   # Tip of the pinky finger
        ]
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            results = self.hands.process(rgb_frame)
            
            # Draw landmarks on the hands
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            
            # Display the frame
            qt_img = self.convert_cv_qt(frame)
            self.view.update_frame(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_qt_format.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
