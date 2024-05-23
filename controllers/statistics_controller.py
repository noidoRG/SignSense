# controllers/statistics_controller.py
from models.statistics_model import StatisticsModel
from views.statistics_view import StatisticsView

class StatisticsController:
    def __init__(self):
        self.model = StatisticsModel()
        self.view = StatisticsView()
        self.connect_signals()

    def connect_signals(self):
        # Пример связи сигналов и слотов
        # self.view.some_button.clicked.connect(self.handle_button_click)
        pass

    def handle_button_click(self):
        data = self.model.get_data()
        self.view.update(data)
