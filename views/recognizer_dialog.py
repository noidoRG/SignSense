# views/recognizer_dialog.py

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
import cv2
import mediapipe as mp
import numpy as np
import json

class RecognizerDialog(QDialog):
    gesture_learnt = pyqtSignal()

    def __init__(self, gesture):
        super().__init__()

        self.gesture = gesture
        self.continue_pressed = False
        self.setWindowTitle("Распознаватель жестов")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.instruction_label = QLabel(f"Покажите жест: {gesture['gesture']}")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.similarity_label = QLabel("Процент сходства: 0%")
        self.layout.addWidget(self.similarity_label)

        self.button_layout = QHBoxLayout()
        self.back_button = QPushButton("Вернуться")
        self.back_button.clicked.connect(self.reject)
        self.continue_button = QPushButton("Продолжить")
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self.continue_action)
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.continue_button)
        self.layout.addLayout(self.button_layout)

        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.timer = self.startTimer(30)

    def timerEvent(self, event):
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
                self.similarity_label.setText(f"Процент сходства: {confidence:.2f}%")
                if confidence >= 70:
                    self.continue_button.setEnabled(True)
                    self.update_gesture_status()
                    self.gesture_learnt.emit()
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def recognize_gesture(self, landmarks):
        def normalize_landmarks(landmarks):
            wrist = landmarks[0]
            normalized_landmarks = []
            for lm in landmarks:
                normalized_landmarks.append({
                    'x': lm['x'] - wrist['x'],
                    'y': lm['y'] - wrist['y'],
                    'z': lm['z'] - wrist['z']
                })
            return normalized_landmarks

        def mirror_landmarks(landmarks):
            mirrored_landmarks = []
            for lm in landmarks:
                mirrored_landmarks.append({
                    'x': -lm['x'],
                    'y': lm['y'],
                    'z': lm['z']
                })
            return mirrored_landmarks

        def calculate_distance(landmarks1, landmarks2):
            array1 = np.array([[lm['x'], lm['y'], lm['z']] for lm in landmarks1])
            array2 = np.array([[lm['x'], lm['y'], lm['z']] for lm in landmarks2])
            return np.linalg.norm(array1 - array2)

        landmarks = [{'x': lm.x, 'y': lm.y, 'z': lm.z} for lm in landmarks]
        normalized_landmarks = normalize_landmarks(landmarks)
        mirrored_landmarks = mirror_landmarks(normalized_landmarks)

        min_distance = float('inf')
        gesture_name = "Жест не распознан"
        confidence = 0

        for variation in self.gesture['variations']:
            normalized_variation = normalize_landmarks(variation)
            distance = calculate_distance(normalized_landmarks, normalized_variation)
            mirrored_distance = calculate_distance(mirrored_landmarks, normalized_variation)
            if distance < min_distance:
                min_distance = distance
                gesture_name = self.gesture['gesture']
                confidence = 100 - min_distance * 100
            if mirrored_distance < min_distance:
                min_distance = mirrored_distance
                gesture_name = self.gesture['gesture']
                confidence = 100 - min_distance * 100

        return gesture_name, confidence

    def continue_action(self):
        self.continue_pressed = True
        self.accept()

    def update_gesture_status(self):
        with open(f"data/{self.gesture['gesture']}.json", 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['learnt'] = True
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()

    def closeEvent(self, event):
        self.killTimer(self.timer)
        self.cap.release()
        super().closeEvent(event)
