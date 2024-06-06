# add_gesture.py
from models.database import session, Gesture, Landmark

def add_gesture(name, landmarks):
    gesture = Gesture(name=name)
    session.add(gesture)
    session.commit()

    for index, (x, y) in enumerate(landmarks):
        landmark = Landmark(gesture_id=gesture.id, index=index, x=x, y=y)
        session.add(landmark)

    session.commit()

if __name__ == '__main__':
    thumb_up_landmarks = [
        (0.5, 0.2),
        (0.5, 0.1),
        (0.3, 0.3),
        (0.3, 0.5),
        (0.3, 0.7),
        (0.3, 0.9),
    ]
    add_gesture('thumbs_up', thumb_up_landmarks)

    # Добавьте другие жесты аналогичным образом
