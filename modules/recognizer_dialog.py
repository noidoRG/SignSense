# modules/recognizer_dialog.py

import cv2
import mediapipe as mp
import numpy as np
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
import json

class RecognizerDialog(QDialog):
    gesture_learnt = pyqtSignal()
    gesture_mastered = pyqtSignal()

    def __init__(self, gesture, mode='learn'):
        super().__init__()
        self.setWindowTitle("Распознаватель жестов")
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        self.gesture = gesture
        self.mode = mode
        self.continue_pressed = False

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.gesture_label = QLabel(f"Покажите жест: {gesture['gesture']}")
        self.gesture_label.setObjectName("gesture_label")
        self.gesture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gesture_label.setFont(QFont("Montserrat Alternates", 14, QFont.Weight.Bold))
        self.layout.addWidget(self.gesture_label)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.score_label = QLabel("Сходство: 0%")
        self.score_label.setObjectName("score_label")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.score_label)

        self.button_layout = QHBoxLayout()

        self.return_button = QPushButton("Вернуться")
        self.return_button.setObjectName("return_button")
        self.return_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.return_button)

        self.continue_button = QPushButton("Продолжить (>70%)")
        self.continue_button.setObjectName("continue_button")
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self.on_continue)
        self.button_layout.addWidget(self.continue_button)

        self.layout.addLayout(self.button_layout)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.mp_hands = mp.solutions.hands.Hands()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )

                gesture, confidence = self.recognize_gesture(hand_landmarks.landmark)
                self.update_gesture_status(gesture, confidence)
        else:
            self.score_label.setText("Сходство: 0%")

        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def recognize_gesture(self, landmarks):
        min_distance = float('inf')
        recognized_gesture = None

        landmarks = [{'x': lm.x, 'y': lm.y, 'z': lm.z} for lm in landmarks]
        normalized_landmarks = self.normalize_landmarks(landmarks)
        mirrored_landmarks = self.mirror_landmarks(normalized_landmarks)

        for variation in self.gesture['variations']:
            normalized_variation = self.normalize_landmarks(variation)
            distance = self.calculate_distance(normalized_landmarks, normalized_variation)
            mirrored_distance = self.calculate_distance(mirrored_landmarks, normalized_variation)
            if distance < min_distance:
                min_distance = distance
                recognized_gesture = self.gesture['gesture']
            if mirrored_distance < min_distance:
                min_distance = mirrored_distance
                recognized_gesture = self.gesture['gesture']

        confidence = 1 - min_distance
        return recognized_gesture, confidence

    def normalize_landmarks(self, landmarks):
        wrist = landmarks[0]
        normalized_landmarks = []
        for lm in landmarks:
            normalized_landmarks.append({
                'x': lm['x'] - wrist['x'],
                'y': lm['y'] - wrist['y'],
                'z': lm['z'] - wrist['z']
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

    def update_gesture_status(self, gesture, confidence):
        confidence_percentage = int(confidence * 100)
        self.score_label.setText(f"Сходство: {confidence_percentage}%")
        if confidence >= 0.7:
            self.score_label.setStyleSheet("color: green;")
            if not self.continue_button.isEnabled():
                self.continue_button.setEnabled(True)
                self.continue_button.setText("Продолжить")
                if self.mode == 'learn':
                    self.update_gesture_learnt()
                    self.gesture_learnt.emit()
                else:
                    self.update_gesture_mastered()
                    self.gesture_mastered.emit()
        else:
            self.score_label.setStyleSheet("color: #333333;")

    def update_gesture_learnt(self):
        with open(f"data/{self.gesture['gesture']}.json", 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['learnt'] = True
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()

    def update_gesture_mastered(self):
        with open(f"data/{self.gesture['gesture']}.json", 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['mastered'] = True
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()

    def on_continue(self):
        self.continue_pressed = True
        self.accept()

    def stop_video(self):
        self.timer.stop()
        self.cap.release()
        # try:
        #     self.mp_hands.close()
        # except:
        #     pass

    def closeEvent(self, event):
        self.stop_video()
        super().closeEvent(event)
