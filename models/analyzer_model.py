# models/analyzer_model.py
import numpy as np

class AnalyzerModel:
    def __init__(self):
        # Хранение эталонных жестов
        self.gestures = {
            'thumbs_up': [
                (0.5, 0.2),  # Base of the thumb
                (0.5, 0.1),  # Tip of the thumb
                (0.3, 0.3),  # Tip of the index finger
                (0.3, 0.5),  # Tip of the middle finger
                (0.3, 0.7),  # Tip of the ring finger
                (0.3, 0.9),  # Tip of the pinky finger
            ]
        }

    def check_gesture(self, landmarks):
        for name, reference in self.gestures.items():
            if len(landmarks) < len(reference):
                continue
            dissimilarity_score = sum(np.linalg.norm(np.array(landmarks[i]) - np.array(reference[i]))
                                      for i in range(len(reference))) / len(reference)
            resemblance_score = 1 - dissimilarity_score
            if resemblance_score > 0.4:  # Порог для распознавания жеста
                return name, resemblance_score * 100
        return "Нет жеста", 0
