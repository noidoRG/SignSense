# controllers/dictionary_controller.py
from models.dictionary_model import DictionaryModel
from views.dictionary_view import DictionaryView

class DictionaryController:
    def __init__(self):
        self.model = DictionaryModel()
        self.view = DictionaryView()
        self.connect_signals()

    def connect_signals(self):
        # Пример связи сигналов и слотов
        self.view.some_button.clicked.connect(self.handle_button_click)
        

    def handle_button_click(self):
        data = self.model.get_data()
        self.view.update(data)
