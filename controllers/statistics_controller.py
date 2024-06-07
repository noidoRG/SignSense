# controllers/statistics_controller.py

from models.statistics_model import StatisticsModel

class StatisticsController:
    def __init__(self):
        self.model = StatisticsModel()

    def get_statistics(self):
        learnt, mastered, total = self.model.count_gestures()
        return {
            "learnt": learnt,
            "mastered": mastered,
            "total": total
        }
