# controllers/settings_controller.py

from PyQt6.QtCore import QObject, pyqtSignal
import json
import glob

class SettingsController(QObject):
    learnt_reset = pyqtSignal()
    mastered_reset = pyqtSignal()

    def __init__(self):
        super().__init__()

    def reset_learnt_gestures(self):
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['learnt'] = False
                data['mastered'] = False
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
        self.learnt_reset.emit()

    def reset_mastered_gestures(self):
        for filename in glob.glob("data/*.json"):
            with open(filename, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['mastered'] = False
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
        self.mastered_reset.emit()
