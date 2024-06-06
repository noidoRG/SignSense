# models/dictionary_model.py

import json
import glob

class DictionaryModel:
    def __init__(self):
        self.gestures = self.load_gestures()

    def load_gestures(self):
        gestures = []
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                gestures.append(data)
        return gestures

    def get_gestures(self):
        return self.gestures
