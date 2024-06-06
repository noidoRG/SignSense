# models/analyzer_model.py

import cv2
import mediapipe as mp
import json
import numpy as np
import glob

class AnalyzerModel:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.gestures = self.load_gestures()

    def load_gestures(self):
        gestures = {}
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gesture_name = data['gesture']
                gestures[gesture_name] = data['variations']
        return gestures

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

    def recognize_gesture(self, landmarks):
        min_distance = float('inf')
        gesture_name = "Sign unrecognized"
        
        landmarks = [{'x': lm.x, 'y': lm.y, 'z': lm.z} for lm in landmarks]
        normalized_landmarks = self.normalize_landmarks(landmarks)
        mirrored_landmarks = self.mirror_landmarks(normalized_landmarks)
        
        for gesture, variations in self.gestures.items():
            for variation in variations:
                normalized_variation = self.normalize_landmarks(variation)
                distance = self.calculate_distance(normalized_landmarks, normalized_variation)
                mirrored_distance = self.calculate_distance(mirrored_landmarks, normalized_variation)
                if distance < min_distance:
                    min_distance = distance
                    gesture_name = gesture
                if mirrored_distance < min_distance:
                    min_distance = mirrored_distance
                    gesture_name = gesture
        
        return gesture_name, 100 - min_distance * 100

    def process_frame(self, frame):
        results = self.hands.process(frame)
        return results
