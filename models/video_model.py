# models/video_model.py

import cv2
import mediapipe as mp
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from models.gesture_recognizer import GestureRecognizer

class VideoModel(QObject):
    frame_ready = pyqtSignal(object)
    gesture_recognized = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.gesture_recognizer = GestureRecognizer()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(rgb_frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                    recognized_gestures = self.gesture_recognizer.recognize(hand_landmarks.landmark)
                    for gesture, recognized in recognized_gestures.items():
                        if recognized:
                            self.gesture_recognized.emit(gesture)
            
            self.frame_ready.emit(rgb_frame)

    def stop(self):
        self.timer.stop()
        self.cap.release()
