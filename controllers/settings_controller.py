# controllers/settings_controller.py
from models.settings_model import SettingsModel

class SettingsController:
    def __init__(self):
        self.model = SettingsModel()
        self.display_landmarks = False

    def reset_learnt_gestures(self):
        self.model.reset_learnt_gestures()

    def reset_mastered_gestures(self):
        self.model.reset_mastered_gestures()

    def set_display_landmarks(self, display):
        self.display_landmarks = display

    def get_display_landmarks(self):
        return self.display_landmarks