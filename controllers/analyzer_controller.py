# controllers/analyzer_controller.py

from models.analyzer_model import AnalyzerModel

class AnalyzerController:
    def __init__(self):
        self.model = AnalyzerModel()

    def analyze_gesture(self, landmarks):
        return self.model.recognize_gesture(landmarks)

    def process_frame(self, frame):
        return self.model.process_frame(frame)
