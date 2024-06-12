# views/analyzer.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
import numpy as np
import json
import glob

class Analyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.result_label = QLabel("Нет жеста")
        self.layout.addWidget(self.result_label)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Инициализация MediaPipe Hands
        self.mp_hands = mp.solutions.hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Загрузка жестов
        self.gestures = self.load_gestures()

    def load_gestures(self):
        gestures = {}
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gesture_name = data['gesture']
                gestures[gesture_name] = data['variations']
        return gestures

    def start_video(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_video(self):
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                gesture, confidence = self.recognize_gesture(hand_landmarks.landmark)
                self.result_label.setText(f"{gesture} ({confidence:.2f}%)")
        else:
            self.result_label.setText("Нет жеста")

        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def normalize_landmarks(self, landmarks):
        wrist = landmarks[0]
        normalized_landmarks = []
        for lm in landmarks:
            normalized_landmarks.append({
                'x': lm.x - wrist.x,
                'y': lm.y - wrist.y,
                'z': lm.z - wrist.z
            })
        return normalized_landmarks

    def mirror_landmarks(self, landmarks):
        mirrored_landmarks = []
        for lm in landmarks:
            mirrored_landmarks.append({
                'x': -lm['x'],
                'y': lm['y'],
                'z': lm['z']
            })
        return mirrored_landmarks

    def calculate_distance(self, landmarks1, landmarks2):
        array1 = np.array([[lm['x'], lm['y'], lm['z']] for lm in landmarks1])
        array2 = np.array([[lm['x'], lm['y'], lm['z']] for lm in landmarks2])
        return np.linalg.norm(array1 - array2)

    def recognize_gesture(self, landmarks):
        normalized_landmarks = self.normalize_landmarks(landmarks)
        mirrored_landmarks = self.mirror_landmarks(normalized_landmarks)

        min_distance = float('inf')
        gesture_name = "Нет жеста"
        confidence = 0

        for gesture, variations in self.gestures.items():
            for variation in variations:
                normalized_variation = self.normalize_landmarks_from_dict(variation)
                distance = self.calculate_distance(normalized_landmarks, normalized_variation)
                mirrored_distance = self.calculate_distance(self.mirror_landmarks(normalized_variation), normalized_landmarks)
                if distance < min_distance:
                    min_distance = distance
                    gesture_name = gesture
                    confidence = 100 - min_distance * 100
                if mirrored_distance < min_distance:
                    min_distance = mirrored_distance
                    gesture_name = gesture
                    confidence = 100 - min_distance * 100

        return gesture_name, confidence

    def normalize_landmarks_from_dict(self, landmarks):
        wrist = landmarks[0]
        normalized_landmarks = []
        for lm in landmarks:
            normalized_landmarks.append({
                'x': lm['x'] - wrist['x'],
                'y': lm['y'] - wrist['y'],
                'z': lm['z'] - wrist['z']
            })
        return normalized_landmarks

    def showEvent(self, event):
        self.start_video()
        super().showEvent(event)

    def hideEvent(self, event):
        self.stop_video()
        super().hideEvent(event)
