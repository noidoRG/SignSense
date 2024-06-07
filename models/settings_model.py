# models/settings_model.py

import json
import glob

class SettingsModel:
    def __init__(self):
        self.gestures_path = "data/*.json"

    def reset_learnt_gestures(self):
        for filename in glob.glob(self.gestures_path):
            with open(filename, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['learnt'] = False
                data['mastered'] = False
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()

    def reset_mastered_gestures(self):
        for filename in glob.glob(self.gestures_path):
            with open(filename, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['mastered'] = False
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
