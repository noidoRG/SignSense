# controllers/dictionary_controller.py

from models.dictionary_model import DictionaryModel

class DictionaryController:
    def __init__(self):
        self.model = DictionaryModel()

    def get_gestures(self):
        return self.model.get_gestures()
