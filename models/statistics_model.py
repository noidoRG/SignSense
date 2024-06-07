# models/statistics_model.py

import json
import glob

class StatisticsModel:
    def __init__(self):
        self.gestures_path = "data/*.json"

    def load_gestures(self):
        gestures = []
        for filename in glob.glob(self.gestures_path):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gestures.append(data)
        return gestures

    def count_gestures(self):
        gestures = self.load_gestures()
        total = len(gestures)
        learnt = sum(1 for gesture in gestures if gesture.get('learnt', False))
        mastered = sum(1 for gesture in gestures if gesture.get('mastered', False))
        return learnt, mastered, total
