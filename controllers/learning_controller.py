# controllers/learning_controller.py
from models.learning_model import LearningModel
from views.learning_view import LearningView

class LearningController:
    def __init__(self):
        self.model = LearningModel()
        self.view = LearningView()
        self.connect_signals()

    def connect_signals(self):
        # Пример связи сигналов и слотов
        self.view.some_button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        data = self.model.get_data()
        self.view.update(data)
