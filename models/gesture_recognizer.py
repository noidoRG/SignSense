# models/gesture_recognizer.py

import numpy as np

class GestureRecognizer:
    def __init__(self):
        self.gestures = {
            'thumbs_up': self.is_thumbs_up
        }

    def recognize(self, landmarks):
        recognized_gestures = {}
        for gesture, func in self.gestures.items():
            if func(landmarks):
                recognized_gestures[gesture] = True
            else:
                recognized_gestures[gesture] = False
        return recognized_gestures

    def is_thumbs_up(self, landmarks):
        # Простая логика для распознавания "палец вверх"
        thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
        index_tip = np.array([landmarks[8].x, landmarks[8].y])
        
        return thumb_tip[1] < index_tip[1]  # Проверка, что палец выше указательного пальца
