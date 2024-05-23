# models/gesture_model.py

class GestureModel:
    def __init__(self, name, reference_points):
        self.name = name
        self.reference_points = reference_points

# Пример жеста
thumbs_up = GestureModel(
    "Thumbs Up",
    [
        (0.5, 0.2),
        (0.5, 0.1),
        (0.3, 0.3),
        (0.3, 0.5),
        (0.3, 0.7),
        (0.3, 0.9),
    ]
)
