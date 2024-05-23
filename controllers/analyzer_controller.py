# controllers/analyzer_controller.py
import cv2
import mediapipe as mp
from PyQt6.QtCore import QTimer
from models.analyzer_model import AnalyzerModel
from views.analyzer_view import AnalyzerView

class AnalyzerController:
    def __init__(self):
        self.model = AnalyzerModel()
        self.view = AnalyzerView()

        # Инициализация MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Инициализация OpenCV
        self.cap = cv2.VideoCapture(0)

        # Таймер для обновления кадров
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Обработка кадра
        frame_flipped = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        gesture_name = "Нет жеста"
        resemblance_score = 0

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = [(landmark.x, landmark.y) for landmark in hand_landmarks.landmark]
            gesture_name, resemblance_score = self.model.check_gesture(landmarks)

        # Обновление представления
        self.view.update_image(frame_flipped)
        self.view.update_label(f'{gesture_name}: {resemblance_score:.2f}%')

    def close(self):
        self.cap.release()
